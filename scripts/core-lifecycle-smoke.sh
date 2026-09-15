#!/usr/bin/env bash
set -euo pipefail

# Core lifecycle smoke test for an already-authorized EAO deployment.
# Read-only by default. Pass --confirm-recreate to exercise component recreate.
#
# Required:
#   EAIO_RUNTIME_ROOT=/absolute/deployment/runtime_root
#
# Optional:
#   OPENWEBUI_URL=http://127.0.0.1:3000
#   WEKNORA_FRONTEND_URL=http://127.0.0.1:8088
#
# This script does not restart Docker/the host; those remain explicit recovery tests.

CONFIRM=0
if [ "${1:-}" = "--confirm-recreate" ]; then
  CONFIRM=1
elif [ "${1:-}" != "" ]; then
  echo "Usage: EAIO_RUNTIME_ROOT=/path $0 [--confirm-recreate]" >&2
  exit 2
fi

: "${EAIO_RUNTIME_ROOT:?set EAIO_RUNTIME_ROOT to deployment.runtime_root}"

WK_DIR="${EAIO_RUNTIME_ROOT}/runtime/WeKnora"
OW_DIR="${EAIO_RUNTIME_ROOT}/runtime/OpenWebUI"
OW_COMPOSE="${EAIO_OPENWEBUI_COMPOSE_FILE:-$OW_DIR/docker-compose.bootstrap.yml}"
[ -f "$OW_COMPOSE" ] || OW_COMPOSE="$OW_DIR/docker-compose.yml"

WEKNORA_FRONTEND_URL="${WEKNORA_FRONTEND_URL:-http://127.0.0.1:8088}"
OPENWEBUI_URL="${OPENWEBUI_URL:-http://127.0.0.1:3000}"

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "PASS: $*"; }

[ -d "$WK_DIR" ] || fail "missing WeKnora runtime: $WK_DIR"
[ -f "$WK_DIR/docker-compose.yml" ] || fail "missing WeKnora compose"
[ -f "$WK_DIR/docker-compose.eaio-override.yml" ] || fail "missing EAO WeKnora override"
[ -f "$OW_COMPOSE" ] || fail "missing Open WebUI compose"

wk_project="$(docker inspect WeKnora-app --format '{{index .Config.Labels "com.docker.compose.project"}}')"
ow_project="$(docker inspect eaio-open-webui --format '{{index .Config.Labels "com.docker.compose.project"}}')"
[ "$wk_project" = "weknora" ] || fail "WeKnora compose project drift: $wk_project"
[ "$ow_project" = "eaio-openwebui" ] || fail "Open WebUI compose project drift: $ow_project"
pass "Compose project identities"

pg_volume="$(docker inspect WeKnora-postgres --format '{{range .Mounts}}{{if eq .Destination "/var/lib/postgresql/data"}}{{.Name}}{{end}}{{end}}')"
files_volume="$(docker inspect WeKnora-app --format '{{range .Mounts}}{{if eq .Destination "/data/files"}}{{.Name}}{{end}}{{end}}')"
ow_volume="$(docker inspect eaio-open-webui --format '{{range .Mounts}}{{if eq .Destination "/app/backend/data"}}{{.Name}}{{end}}{{end}}')"
[ -n "$pg_volume" ] || fail "WeKnora PostgreSQL volume not found"
[ -n "$files_volume" ] || fail "WeKnora files volume not found"
[ -n "$ow_volume" ] || fail "Open WebUI data volume not found"
pass "Persistent volumes: $pg_volume | $files_volume | $ow_volume"

grep -q '^SYSTEM_AES_KEY=' "$WK_DIR/.env" || fail "SYSTEM_AES_KEY missing from WeKnora runtime env"
docker inspect WeKnora-app --format '{{range .Config.Env}}{{println .}}{{end}}' | grep -q '^SYSTEM_AES_KEY='   || fail "SYSTEM_AES_KEY missing from WeKnora app container"
pass "WeKnora encryption-key presence"

probe_weknora() {
  local code
  code="$(curl -sS -o /tmp/eao-lifecycle-wk -w '%{http_code}' "$WEKNORA_FRONTEND_URL/api/v1/models" || true)"
  [ "$code" != "000" ] && [ "$code" != "502" ] && [ "$code" != "503" ] && [ "$code" != "504" ]     || fail "WeKnora frontend proxy unhealthy: HTTP $code"
}

probe_openwebui() {
  curl -fsS --max-time 10 "$OPENWEBUI_URL/" >/dev/null     || fail "Open WebUI HTTP probe failed"
}

probe_weknora
probe_openwebui
pass "Core HTTP routing"

if [ "$CONFIRM" -eq 0 ]; then
  echo "INFO: read-only smoke complete; use --confirm-recreate for lifecycle exercise"
  exit 0
fi

cd "$WK_DIR"

docker compose -f docker-compose.yml -f docker-compose.eaio-override.yml   up -d --force-recreate --no-deps app >/dev/null
for _ in $(seq 1 30); do
  h="$(docker inspect WeKnora-app --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}')"
  [ "$h" = "healthy" ] && break
  sleep 2
done
[ "$(docker inspect WeKnora-app --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}')" = "healthy" ]   || fail "WeKnora app did not become healthy"
sleep 11
probe_weknora
pass "WeKnora app recreate without frontend restart"

docker compose -f docker-compose.yml -f docker-compose.eaio-override.yml   up -d --force-recreate --no-deps frontend >/dev/null
sleep 3
docker exec WeKnora-frontend nginx -t >/dev/null
probe_weknora
pass "WeKnora frontend recreate"

cd "$OW_DIR"
docker compose -f "$OW_COMPOSE" up -d --force-recreate --no-deps open-webui >/dev/null
for _ in $(seq 1 30); do
  h="$(docker inspect eaio-open-webui --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}')"
  [ "$h" = "healthy" ] && break
  sleep 2
done
probe_openwebui

[ "$(docker inspect WeKnora-postgres --format '{{range .Mounts}}{{if eq .Destination "/var/lib/postgresql/data"}}{{.Name}}{{end}}{{end}}')" = "$pg_volume" ]   || fail "PostgreSQL volume identity changed"
[ "$(docker inspect WeKnora-app --format '{{range .Mounts}}{{if eq .Destination "/data/files"}}{{.Name}}{{end}}{{end}}')" = "$files_volume" ]   || fail "WeKnora files volume identity changed"
[ "$(docker inspect eaio-open-webui --format '{{range .Mounts}}{{if eq .Destination "/app/backend/data"}}{{.Name}}{{end}}{{end}}')" = "$ow_volume" ]   || fail "Open WebUI data volume identity changed"

pass "Recreate preserved all persistent-volume identities"
