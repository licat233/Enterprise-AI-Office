#!/usr/bin/env bash
set -euo pipefail

# Enterprise AI Office backup helper for the validated local demo.
#
# This script intentionally discovers Docker volume names from the running
# containers. It is not a universal WeKnora/Open WebUI backup implementation.
# Review the deployed upstream versions before reusing it elsewhere.

umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

EAIO_RUNTIME_DIR="${EAIO_RUNTIME_DIR:-/Users/Shared/enterprise-ai-office/runtime}"
HERMES_HOME="${HERMES_HOME:-${HOME}/.hermes}"
OPENWEBUI_RUNTIME_DIR="${OPENWEBUI_RUNTIME_DIR:-${EAIO_RUNTIME_DIR}/open-webui}"
BACKUP_ROOT="${EAIO_BACKUP_ROOT:-${EAIO_RUNTIME_DIR}/backups}"
POSTGRES_CONTAINER="${WEKNORA_POSTGRES_CONTAINER:-WeKnora-postgres}"
WEKNORA_APP_CONTAINER="${WEKNORA_APP_CONTAINER:-WeKnora-app}"
OPENWEBUI_CONTAINER="${OPENWEBUI_CONTAINER:-eaio-open-webui}"
LAUNCH_AGENT_PLIST="${HERMES_LAUNCH_AGENT_PLIST:-${HOME}/Library/LaunchAgents/ai.hermes.gateway.plist}"
GOVERNANCE_STATE_DB="${EAIO_GOVERNANCE_STATE_DB:-${EAIO_RUNTIME_DIR}/email-governance/state.sqlite3}"
GOVERNANCE_BACKUP_HELPER="$REPO_ROOT/infrastructure/email/governance/backup_state.py"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
DEST="${1:-${BACKUP_ROOT}/${STAMP}}"

pass() {
  printf 'PASS %-30s %s\n' "$1" "${2:-}"
}

warn() {
  printf 'WARN %-29s %s\n' "$1" "${2:-}" >&2
}

fail() {
  printf 'FAIL %-30s %s\n' "$1" "${2:-}" >&2
  exit 1
}

on_error() {
  printf 'FAIL backup aborted near line %s\n' "$LINENO" >&2
}

trap on_error ERR

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "command ${1}" "not found"
}

require_file() {
  [ -f "$1" ] || fail "file" "missing required file: $1"
}

require_directory() {
  [ -d "$1" ] || fail "directory" "missing required directory: $1"
}

require_running_container() {
  local container="$1"
  local running
  running="$(docker inspect --format '{{.State.Running}}' "$container" 2>/dev/null || true)"
  [ "$running" = true ] || fail "container ${container}" "not running"
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
  [ -n "$value" ] || fail "environment ${key}" "missing in protected runtime env"
  printf '%s' "$value"
}

volume_name() {
  local container="$1"
  local destination="$2"
  local template
  case "$destination" in
    /data/files)
      template='{{range .Mounts}}{{if eq .Destination "/data/files"}}{{.Name}}{{end}}{{end}}'
      ;;
    /var/lib/postgresql/data)
      template='{{range .Mounts}}{{if eq .Destination "/var/lib/postgresql/data"}}{{.Name}}{{end}}{{end}}'
      ;;
    /app/backend/data)
      template='{{range .Mounts}}{{if eq .Destination "/app/backend/data"}}{{.Name}}{{end}}{{end}}'
      ;;
    *)
      fail "volume discovery" "unsupported mount destination: $destination"
      ;;
  esac
  docker inspect --format "$template" "$container"
}

archive_volume() {
  local container="$1"
  local image="$2"
  local mount_path="$3"
  local output="$4"
  docker run --rm --volumes-from "${container}:ro" --entrypoint tar "$image" \
    -czf - -C "$mount_path" . > "$output"
  [ -s "$output" ] || fail "volume archive" "empty archive: $output"
}

require_command docker
require_command tar
require_command awk
require_command shasum
require_directory "$EAIO_RUNTIME_DIR"
require_directory "$OPENWEBUI_RUNTIME_DIR"
require_directory "$HERMES_HOME"
require_file "$EAIO_RUNTIME_DIR/WeKnora/.env"
require_file "$OPENWEBUI_RUNTIME_DIR/docker-compose.yml"
require_file "$LAUNCH_AGENT_PLIST"
require_directory "$EAIO_RUNTIME_DIR/credentials"

require_running_container "$POSTGRES_CONTAINER"
require_running_container "$WEKNORA_APP_CONTAINER"
require_running_container "$OPENWEBUI_CONTAINER"

WEKNORA_DIR="$EAIO_RUNTIME_DIR/WeKnora"
WEKNORA_ENV_FILE="$WEKNORA_DIR/.env"
DB_USER="$(env_value DB_USER "$WEKNORA_ENV_FILE")"
DB_NAME="$(env_value DB_NAME "$WEKNORA_ENV_FILE")"
DB_PASSWORD="$(env_value DB_PASSWORD "$WEKNORA_ENV_FILE")"
WEKNORA_VERSION="$(env_value WEKNORA_VERSION "$WEKNORA_ENV_FILE")"

POSTGRES_VOLUME="$(volume_name "$POSTGRES_CONTAINER" /var/lib/postgresql/data)"
WEKNORA_DATA_VOLUME="$(volume_name "$WEKNORA_APP_CONTAINER" /data/files)"
OPENWEBUI_VOLUME="$(volume_name "$OPENWEBUI_CONTAINER" /app/backend/data)"
[ -n "$POSTGRES_VOLUME" ] || fail "volume discovery" "PostgreSQL volume not found"
[ -n "$WEKNORA_DATA_VOLUME" ] || fail "volume discovery" "WeKnora data volume not found"
[ -n "$OPENWEBUI_VOLUME" ] || fail "volume discovery" "Open WebUI volume not found"

WEKNORA_IMAGE="$(docker inspect --format '{{.Config.Image}}' "$WEKNORA_APP_CONTAINER")"
POSTGRES_IMAGE="$(docker inspect --format '{{.Config.Image}}' "$POSTGRES_CONTAINER")"
OPENWEBUI_IMAGE="$(docker inspect --format '{{.Config.Image}}' "$OPENWEBUI_CONTAINER")"
HERMES_VERSION="$(hermes --version 2>/dev/null | sed -n '1p')"
REPO_COMMIT="$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || true)"
DOCKER_VERSION="$(docker version --format '{{.Server.Version}}')"
COMPOSE_VERSION="$(docker compose version --short)"

[ ! -e "$DEST" ] || fail "destination" "already exists: $DEST"
mkdir -p "$DEST/weknora" "$DEST/open-webui" "$DEST/hermes" "$DEST/secrets" "$DEST/governance"
chmod 700 "$DEST" "$DEST/weknora" "$DEST/open-webui" "$DEST/hermes" "$DEST/secrets" "$DEST/governance"
pass "destination" "$DEST"

# PostgreSQL is backed up logically, rather than by copying a live database
# volume. The password is passed to the container without being printed.
docker exec -e "PGPASSWORD=${DB_PASSWORD}" "$POSTGRES_CONTAINER" \
  pg_dump --username="$DB_USER" --dbname="$DB_NAME" --format=custom \
  --no-owner --no-privileges > "$DEST/weknora/postgres.dump"
[ -s "$DEST/weknora/postgres.dump" ] || fail "PostgreSQL dump" "empty dump"
docker exec -i "$POSTGRES_CONTAINER" pg_restore --list --format=custom \
  < "$DEST/weknora/postgres.dump" > "$DEST/weknora/postgres.contents.txt"
[ -s "$DEST/weknora/postgres.contents.txt" ] || fail "PostgreSQL validation" "dump has no inspectable contents"
pass "PostgreSQL" "logical dump and pg_restore listing"

# Docker volumes are exported through the existing running images. This keeps
# the source containers untouched and avoids assuming OrbStack VM paths exist
# on the macOS host.
archive_volume "$WEKNORA_APP_CONTAINER" "$WEKNORA_IMAGE" /data/files \
  "$DEST/weknora/data-files.tar.gz"
pass "WeKnora documents" "$WEKNORA_DATA_VOLUME"

archive_volume "$OPENWEBUI_CONTAINER" "$OPENWEBUI_IMAGE" /app/backend/data \
  "$DEST/open-webui/data.tar.gz"
pass "Open WebUI data" "$OPENWEBUI_VOLUME"

# Include the exact runtime configuration used by the tested Compose project,
# including protected provider configuration. The backup destination is created
# with mode 700/umask 077 and is not a repository path.
tar -czf "$DEST/weknora/runtime-config.tar.gz" -C "$WEKNORA_DIR" \
  .env config skills docker-compose.yml docker-compose.eaio.yml mcp-server
cp "$OPENWEBUI_RUNTIME_DIR/docker-compose.yml" "$DEST/open-webui/docker-compose.yml"
pass "WeKnora config" "runtime .env, config, skills, Compose, MCP"
pass "Open WebUI config" "Compose manifest"

# Hermes archive includes the active employee Profiles, gateway configuration,
# state databases, MCP/Skills configuration, and OAuth/provider state required
# for recovery. The archive is intentionally private.
tar --exclude='*.sock' -czf "$DEST/hermes/runtime.tar.gz" -C "$HERMES_HOME" \
  .env config.yaml SOUL.md auth.json state.db gateway_state.json state \
  profiles/general profiles/sales profiles/qc skills
tar -czf "$DEST/hermes/repository-profiles-skills.tar.gz" -C "$REPO_ROOT" \
  profiles skills
cp "$LAUNCH_AGENT_PLIST" "$DEST/hermes/ai.hermes.gateway.plist"
pass "Hermes state" "Profiles, gateway config, state, Skills/MCP"

# Runtime credential inventory is recoverable but never copied into Git or the
# non-secret manifest. Keep it in a separate restricted archive.
tar -czf "$DEST/secrets/runtime-credentials.tar.gz" -C "$EAIO_RUNTIME_DIR" credentials
pass "Secret recovery" "restricted local archive; values not printed"

# v2 Email Governance is conditional. When its SQLite state exists, snapshot it
# through SQLite's online backup API rather than copying the live WAL database.
# A v1-only deployment must continue to back up successfully when this state is absent.
GOVERNANCE_MANIFEST_LINE="- Email Governance SQLite: not enabled / state absent"
if [ -f "$GOVERNANCE_STATE_DB" ]; then
  require_command python3
  require_file "$GOVERNANCE_BACKUP_HELPER"
  python3 "$GOVERNANCE_BACKUP_HELPER" \
    "$GOVERNANCE_STATE_DB" "$DEST/governance/state.sqlite3"
  GOVERNANCE_MANIFEST_LINE="- Email Governance SQLite snapshot: governance/state.sqlite3"
  pass "Email Governance" "$GOVERNANCE_STATE_DB"
else
  warn "Email Governance" "not enabled / state absent: $GOVERNANCE_STATE_DB"
fi

cat > "$DEST/MANIFEST.txt" <<EOF
Enterprise AI Office backup manifest
Backup timestamp (UTC): $STAMP
Host OS: $(uname -s)
Host architecture: $(uname -m)
Docker Engine: $DOCKER_VERSION
Docker Compose: $COMPOSE_VERSION
Repository commit: ${REPO_COMMIT:-unavailable}
WeKnora version: $WEKNORA_VERSION
WeKnora image: $WEKNORA_IMAGE
PostgreSQL image: $POSTGRES_IMAGE
Open WebUI image: $OPENWEBUI_IMAGE
Hermes version: $HERMES_VERSION
Backup components:
- WeKnora PostgreSQL logical dump: weknora/postgres.dump
- WeKnora uploaded/original document storage: weknora/data-files.tar.gz
- WeKnora runtime configuration and MCP server: weknora/runtime-config.tar.gz
- Open WebUI persistent application data: open-webui/data.tar.gz
- Open WebUI Compose configuration: open-webui/docker-compose.yml
- Hermes Profiles, state, gateway configuration, Skills/MCP: hermes/runtime.tar.gz
- Repository Profile templates and Skills: hermes/repository-profiles-skills.tar.gz
- Hermes LaunchAgent definition: hermes/ai.hermes.gateway.plist
- Protected runtime credentials: secrets/runtime-credentials.tar.gz
$GOVERNANCE_MANIFEST_LINE
Discovered Docker volumes:
- PostgreSQL: $POSTGRES_VOLUME
- WeKnora documents: $WEKNORA_DATA_VOLUME
- Open WebUI data: $OPENWEBUI_VOLUME
Security note: secret values are not recorded in this manifest. The secrets archive is restricted local backup material and must be moved to encrypted independent storage for production use.
EOF

: > "$DEST/SHA256SUMS"
while IFS= read -r file; do
  [ "$file" = "$DEST/SHA256SUMS" ] && continue
  relative="${file#${DEST}/}"
  shasum -a 256 "$file" | awk -v path="$relative" '{print $1 "  " path}' >> "$DEST/SHA256SUMS"
done < <(find "$DEST" -type f | sort)

find "$DEST" -type f -exec chmod 600 {} +
find "$DEST" -type d -exec chmod 700 {} +

pass "manifest" "$DEST/MANIFEST.txt"
pass "checksums" "$DEST/SHA256SUMS"
pass "backup complete" "$DEST"
