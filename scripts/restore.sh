#!/usr/bin/env bash
set -euo pipefail

# Guarded restore-materialization helper for the validated local demo.
#
# This command restores a backup into a new, explicitly named test target and
# new Docker volumes. It never stops, overwrites, or removes the live demo.
# Full service bring-up and RBAC/MCP smoke tests remain an operator-verified
# step because the target ports and Hermes supervisor policy are host-specific.

umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
EAIO_RUNTIME_DIR="${EAIO_RUNTIME_DIR:-/Users/Shared/enterprise-ai-office/runtime}"
GOVERNANCE_RESTORE_HELPER="$REPO_ROOT/infrastructure/email/governance/restore_state.py"

usage() {
  cat <<'USAGE'
Usage:
  scripts/restore.sh BACKUP_DIRECTORY NEW_TEST_DIRECTORY --confirm-isolated

The target directory must not already exist. The command restores the backup
manifest, runtime configuration, Hermes/Profile material, protected credential
archive, WeKnora/Open WebUI file volumes, the WeKnora PostgreSQL dump, and v2
Governance SQLite state when that conditional capability exists in the backup.
It does not touch the live Compose projects, live Hermes, or any provider send path.
USAGE
}

fail() {
  printf 'FAIL %-30s %s\n' "$1" "${2:-}" >&2
  exit 1
}

pass() {
  printf 'PASS %-30s %s\n' "$1" "${2:-}"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "command ${1}" "not found"
}

require_file() {
  [ -f "$1" ] || fail "file" "missing: $1"
}

env_value() {
  local key="$1"
  local file="$2"
  local value
  value="$(awk -v wanted="$key" '
    /^[[:space:]]*(#|$)/ { next }
    {
      line = $0
      sub(/^[[:space:]]*export[[:space:]]+/, "", line)
      split(line, fields, "=")
      if (fields[1] == wanted) {
        sub(/^[^=]*=/, "", line)
        print line
        exit
      }
    }
  ' "$file")"
  value="${value#\"}"
  value="${value%\"}"
  value="${value#\'}"
  value="${value%\'}"
  [ -n "$value" ] || fail "environment ${key}" "missing in protected restored env"
  printf '%s' "$value"
}

manifest_value() {
  local key="$1"
  sed -n "s/^${key}: //p" "$BACKUP_DIR/MANIFEST.txt" | sed -n '1p'
}

wait_for_postgres() {
  local container="$1"
  local user="$2"
  local db="$3"
  local attempt
  for attempt in $(seq 1 45); do
    # The ParadeDB image can briefly accept connections during its
    # initdb/bootstrap phase. Wait for the entrypoint's final hand-off before
    # restoring, otherwise pg_restore races the bootstrap shutdown.
    if docker logs "$container" 2>&1 | rg -q 'PostgreSQL init process complete; ready for start up\.' \
      && docker exec "$container" pg_isready --username="$user" --dbname="$db" >/dev/null 2>&1; then
      return 0
    fi
    sleep 2
  done
  fail "temporary PostgreSQL" "did not accept connections"
}

if [ "$#" -ne 3 ] || [ "$3" != "--confirm-isolated" ]; then
  usage >&2
  exit 2
fi

require_command docker
require_command tar
require_command awk
require_command sed
require_command shasum
require_command rg

BACKUP_DIR="$(cd -- "$1" 2>/dev/null && pwd)" || fail "backup" "directory is not readable"
target_arg="$2"
target_parent="$(dirname -- "$target_arg")"
require_directory() {
  [ -d "$1" ] || fail "directory" "missing: $1"
}
require_directory "$target_parent"
TARGET_ROOT="$(cd -- "$target_parent" && pwd)/$(basename -- "$target_arg")"

case "$TARGET_ROOT" in
  /|"$EAIO_RUNTIME_DIR"|"$EAIO_RUNTIME_DIR/WeKnora"|"$EAIO_RUNTIME_DIR/open-webui"|"$HOME/.hermes")
    fail "target guard" "refusing live or broad target: $TARGET_ROOT"
    ;;
esac
[ ! -e "$TARGET_ROOT" ] && [ ! -L "$TARGET_ROOT" ] || fail "target guard" "target already exists: $TARGET_ROOT"
[ "$TARGET_ROOT" != "$BACKUP_DIR" ] || fail "target guard" "target cannot equal backup directory"

require_file "$BACKUP_DIR/MANIFEST.txt"
require_file "$BACKUP_DIR/SHA256SUMS"
for artifact in \
  weknora/postgres.dump \
  weknora/data-files.tar.gz \
  weknora/runtime-config.tar.gz \
  open-webui/data.tar.gz \
  open-webui/docker-compose.yml \
  hermes/runtime.tar.gz \
  hermes/repository-profiles-skills.tar.gz \
  hermes/ai.hermes.gateway.plist \
  secrets/runtime-credentials.tar.gz; do
  require_file "$BACKUP_DIR/$artifact"
done

(cd "$BACKUP_DIR" && shasum -a 256 -c SHA256SUMS >/dev/null) \
  || fail "checksums" "backup contents do not match SHA256SUMS"
pass "checksums" "$BACKUP_DIR/SHA256SUMS"

WEKNORA_IMAGE="$(manifest_value 'WeKnora image')"
POSTGRES_IMAGE="$(manifest_value 'PostgreSQL image')"
OPENWEBUI_IMAGE="$(manifest_value 'Open WebUI image')"
[ -n "$WEKNORA_IMAGE" ] || fail "manifest" "WeKnora image is missing"
[ -n "$OPENWEBUI_IMAGE" ] || fail "manifest" "Open WebUI image is missing"
if [ -z "$POSTGRES_IMAGE" ]; then
  POSTGRES_IMAGE="$(docker inspect --format '{{.Config.Image}}' WeKnora-postgres 2>/dev/null || true)"
fi
[ -n "$POSTGRES_IMAGE" ] || fail "manifest" "PostgreSQL image is missing and live image is unavailable"

docker image inspect "$WEKNORA_IMAGE" >/dev/null 2>&1 \
  || fail "image" "WeKnora image is not present locally: $WEKNORA_IMAGE"
docker image inspect "$POSTGRES_IMAGE" >/dev/null 2>&1 \
  || fail "image" "PostgreSQL image is not present locally: $POSTGRES_IMAGE"
docker image inspect "$OPENWEBUI_IMAGE" >/dev/null 2>&1 \
  || fail "image" "Open WebUI image is not present locally: $OPENWEBUI_IMAGE"

mkdir -p "$TARGET_ROOT/weknora" "$TARGET_ROOT/open-webui" "$TARGET_ROOT/hermes" \
  "$TARGET_ROOT/repository" "$TARGET_ROOT/runtime" "$TARGET_ROOT/secrets"
chmod 700 "$TARGET_ROOT" "$TARGET_ROOT"/*

tar -xzf "$BACKUP_DIR/weknora/runtime-config.tar.gz" -C "$TARGET_ROOT/weknora"
tar -xzf "$BACKUP_DIR/hermes/runtime.tar.gz" -C "$TARGET_ROOT/hermes"
tar -xzf "$BACKUP_DIR/hermes/repository-profiles-skills.tar.gz" -C "$TARGET_ROOT/repository"
tar -xzf "$BACKUP_DIR/secrets/runtime-credentials.tar.gz" -C "$TARGET_ROOT/runtime"
cp "$BACKUP_DIR/open-webui/docker-compose.yml" "$TARGET_ROOT/open-webui/docker-compose.yml"
cp "$BACKUP_DIR/MANIFEST.txt" "$TARGET_ROOT/MANIFEST.txt"
cp "$BACKUP_DIR/SHA256SUMS" "$TARGET_ROOT/SHA256SUMS"
find "$TARGET_ROOT" -type f -exec chmod 600 {} +
find "$TARGET_ROOT" -type d -exec chmod 700 {} +
pass "runtime material" "$TARGET_ROOT"

# v2 Email Governance is conditional. Materialize its SQLite snapshot into a
# new isolated target and preserve unresolved send evidence; restoring must not
# start the service or retry provider sends.
if [ -f "$BACKUP_DIR/governance/state.sqlite3" ]; then
  require_command python3
  require_file "$GOVERNANCE_RESTORE_HELPER"
  mkdir -p "$TARGET_ROOT/runtime/email-governance"
  chmod 700 "$TARGET_ROOT/runtime/email-governance"
  python3 "$GOVERNANCE_RESTORE_HELPER" \
    "$BACKUP_DIR/governance/state.sqlite3" \
    "$TARGET_ROOT/runtime/email-governance/state.sqlite3"
  pass "Email Governance restore" "$TARGET_ROOT/runtime/email-governance/state.sqlite3"
else
  pass "Email Governance restore" "not enabled / state absent in backup"
fi

slug="$(basename -- "$TARGET_ROOT" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-*//; s/-*$//')"
[ -n "$slug" ] || fail "target name" "target basename has no usable characters"
prefix="eaio-restore-${slug}"
POSTGRES_VOLUME="${prefix}-postgres-data"
WEKNORA_DATA_VOLUME="${prefix}-data-files"
OPENWEBUI_VOLUME="${prefix}-open-webui-data"
PG_CONTAINER="${prefix}-postgres"

for volume in "$POSTGRES_VOLUME" "$WEKNORA_DATA_VOLUME" "$OPENWEBUI_VOLUME"; do
  if docker volume inspect "$volume" >/dev/null 2>&1; then
    fail "volume guard" "temporary volume already exists: $volume"
  fi
  docker volume create "$volume" >/dev/null
done

DB_USER="$(env_value DB_USER "$TARGET_ROOT/weknora/.env")"
DB_NAME="$(env_value DB_NAME "$TARGET_ROOT/weknora/.env")"
DB_PASSWORD="$(env_value DB_PASSWORD "$TARGET_ROOT/weknora/.env")"

docker run -d --name "$PG_CONTAINER" \
  -e "POSTGRES_USER=$DB_USER" \
  -e "POSTGRES_PASSWORD=$DB_PASSWORD" \
  -e "POSTGRES_DB=$DB_NAME" \
  -v "$POSTGRES_VOLUME:/var/lib/postgresql/data" \
  "$POSTGRES_IMAGE" >/dev/null
wait_for_postgres "$PG_CONTAINER" "$DB_USER" "$DB_NAME"

docker exec -i -e "PGPASSWORD=$DB_PASSWORD" "$PG_CONTAINER" \
  sh -c 'cat > /tmp/eaio-restore.dump' < "$BACKUP_DIR/weknora/postgres.dump"
docker exec -e "PGPASSWORD=$DB_PASSWORD" "$PG_CONTAINER" \
  pg_restore --clean --if-exists --no-owner --no-privileges \
  --username="$DB_USER" --dbname="$DB_NAME" /tmp/eaio-restore.dump
docker exec "$PG_CONTAINER" rm -f /tmp/eaio-restore.dump
pass "PostgreSQL restore" "$PG_CONTAINER / $POSTGRES_VOLUME"

docker run --rm -i -v "$WEKNORA_DATA_VOLUME:/data/files" --entrypoint tar "$WEKNORA_IMAGE" \
  -xzf - -C /data/files < "$BACKUP_DIR/weknora/data-files.tar.gz"
pass "WeKnora files" "$WEKNORA_DATA_VOLUME"

docker run --rm -i -v "$OPENWEBUI_VOLUME:/app/backend/data" --entrypoint tar "$OPENWEBUI_IMAGE" \
  -xzf - -C /app/backend/data < "$BACKUP_DIR/open-webui/data.tar.gz"
pass "Open WebUI data" "$OPENWEBUI_VOLUME"

cat > "$TARGET_ROOT/RESTORE-NEXT-STEPS.txt" <<EOF
This target was materialized by scripts/restore.sh.

Target: $TARGET_ROOT
PostgreSQL container: $PG_CONTAINER
PostgreSQL volume: $POSTGRES_VOLUME
WeKnora file volume: $WEKNORA_DATA_VOLUME
Open WebUI data volume: $OPENWEBUI_VOLUME
Governance state: $TARGET_ROOT/runtime/email-governance/state.sqlite3 (only when present in backup)

The live demo was not stopped or modified. To complete an isolated service
test, create a temporary Compose project from $TARGET_ROOT/weknora/docker-compose.yml,
remove fixed container_name entries, choose unused loopback ports, and point
Hermes Profile MCP URLs at that temporary WeKnora API. If Governance state is
present, start a compatible Governance runtime only after inspecting unresolved
send/reconciliation evidence; restore itself never retries or sends email.
Then run the acceptance checks in docs/ACCEPTANCE-TESTS.md and the applicable
v2 acceptance contracts. Do not expose the restored target externally.
EOF
chmod 600 "$TARGET_ROOT/RESTORE-NEXT-STEPS.txt"
pass "restore materialized" "$TARGET_ROOT"
printf '%s\n' "Temporary resources are intentionally left for inspection; remove only these exact named resources after validation:"
printf '  docker rm -f %s\n' "$PG_CONTAINER"
printf '  docker volume rm %s %s %s\n' "$POSTGRES_VOLUME" "$WEKNORA_DATA_VOLUME" "$OPENWEBUI_VOLUME"
