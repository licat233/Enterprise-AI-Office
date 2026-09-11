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

COMPANY_CONFIG="${EAIO_COMPANY_CONFIG:-$REPO_ROOT/private/company.yaml}"

company_yaml_runtime_root() {
  local config="$1"
  [ -f "$config" ] || return 0
  awk '
    /^deployment:[[:space:]]*$/ { in_deployment=1; next }
    in_deployment && /^[^[:space:]]/ { in_deployment=0 }
    in_deployment && /^[[:space:]]+runtime_root:[[:space:]]*/ {
      line=$0
      sub(/^[^:]*:[[:space:]]*/, "", line)
      sub(/^"/, "", line)
      sub(/"$/, "", line)
      print line
      exit
    }
  ' "$config"
}

company_yaml_capability_enabled() {
  local config="$1"
  [ -f "$config" ] || return 0
  awk '
    /^capabilities:[[:space:]]*$/ { in_capabilities=1; next }
    in_capabilities && /^[^[:space:]]/ { in_capabilities=0 }
    in_capabilities && /^[[:space:]]{2}media_transcription:[[:space:]]*$/ { in_media=1; next }
    in_media && /^[[:space:]]{2}[A-Za-z0-9_]+:/ { in_media=0 }
    in_media && /^[[:space:]]{4}enabled:[[:space:]]*true[[:space:]]*$/ { print "true"; exit }
  ' "$config"
}
MEDIA_TRANSCRIPTION_ENABLED="$(company_yaml_capability_enabled "$COMPANY_CONFIG")"
resolve_dir() {
  local explicit="$1"
  shift
  if [ -n "$explicit" ]; then
    printf '%s' "$explicit"
    return
  fi
  local candidate
  for candidate in "$@"; do
    if [ -d "$candidate" ]; then
      printf '%s' "$candidate"
      return
    fi
  done
  printf '%s' "${1:-}"
}

discover_container() {
  local explicit="$1"
  local service="$2"
  local fallback_regex="$3"
  local found
  if [ -n "$explicit" ]; then
    printf '%s' "$explicit"
    return
  fi
  found="$(docker ps --filter "label=com.docker.compose.service=$service" \
    --format '{{.Names}}' | sed -n '1p')"
  if [ -n "$found" ]; then
    printf '%s' "$found"
    return
  fi
  docker ps --format '{{.Names}}' | awk -v pattern="$fallback_regex" \
    '$0 ~ pattern {print; exit}'
}

CONFIG_RUNTIME_ROOT="$(company_yaml_runtime_root "$COMPANY_CONFIG")"
EAIO_RUNTIME_DIR="${EAIO_RUNTIME_DIR:-${CONFIG_RUNTIME_ROOT:-$REPO_ROOT/runtime}}"
if [ -d "$EAIO_RUNTIME_DIR/runtime" ] && { [ -d "$EAIO_RUNTIME_DIR/runtime/WeKnora" ] || [ -d "$EAIO_RUNTIME_DIR/runtime/weknora" ]; }; then
  EAIO_RUNTIME_DIR="$EAIO_RUNTIME_DIR/runtime"
fi
HERMES_HOME="${HERMES_HOME:-${HOME}/.hermes}"
OPENWEBUI_RUNTIME_DIR="${EAIO_OPENWEBUI_RUNTIME_DIR:-$(resolve_dir "" \
  "$EAIO_RUNTIME_DIR/OpenWebUI" "$EAIO_RUNTIME_DIR/open-webui")}"
WEKNORA_DIR="${EAIO_WEKNORA_RUNTIME_DIR:-$(resolve_dir "" \
  "$EAIO_RUNTIME_DIR/WeKnora" "$EAIO_RUNTIME_DIR/weknora")}"
WEKNORA_ENV_FILE="$WEKNORA_DIR/.env"
BACKUP_ROOT="${EAIO_BACKUP_ROOT:-${EAIO_RUNTIME_DIR}/backups}"
DEPLOYMENT_STATE_FILE="${EAIO_DEPLOYMENT_STATE_FILE:-${EAIO_RUNTIME_DIR}/state/deployment-state.md}"
POSTGRES_CONTAINER="${WEKNORA_POSTGRES_CONTAINER:-}"
WEKNORA_APP_CONTAINER="${WEKNORA_APP_CONTAINER:-}"
OPENWEBUI_CONTAINER="${OPENWEBUI_CONTAINER:-}"
RUNTIME_CREDENTIALS_DIR="${EAIO_RUNTIME_CREDENTIALS_DIR:-${EAIO_RUNTIME_DIR}/credentials}"
LAUNCH_AGENT_PLIST="${HERMES_LAUNCH_AGENT_PLIST:-${HOME}/Library/LaunchAgents/ai.hermes.gateway.plist}"
GOVERNANCE_STATE_DB="${EAIO_GOVERNANCE_STATE_DB:-${EAIO_RUNTIME_DIR}/email-governance/state.sqlite3}"
GOVERNANCE_BACKUP_HELPER="$REPO_ROOT/infrastructure/email/governance/backup_state.py"
COMPANY_CONFIG_MANIFEST_LINE="- Active company configuration: not present in backup source"
LAUNCH_AGENT_MANIFEST_LINE="- Hermes LaunchAgent definition: not present in backup source"
CREDENTIALS_MANIFEST_LINE="not separately configured; re-enter from protected stores"
OPENWEBUI_ENV_MANIFEST_LINE="- Open WebUI protected runtime environment: not present in backup source"
MEDIA_TRANSCRIPTION_MANIFEST_LINE="- Media transcription reviewed transcripts: not enabled / state absent"
DEPLOYMENT_STATE_MANIFEST_LINE="- Protected operational deployment state: not present in backup source"

OPENWEBUI_COMPOSE_FILE="${EAIO_OPENWEBUI_COMPOSE_FILE:-}"
if [ -z "$OPENWEBUI_COMPOSE_FILE" ]; then
  for candidate in \
    "$OPENWEBUI_RUNTIME_DIR/docker-compose.yml" \
    "$OPENWEBUI_RUNTIME_DIR/docker-compose.yaml" \
    "$OPENWEBUI_RUNTIME_DIR/docker-compose.bootstrap.yml"; do
    if [ -f "$candidate" ]; then
      OPENWEBUI_COMPOSE_FILE="$candidate"
      break
    fi
  done
fi
if [ -z "$OPENWEBUI_COMPOSE_FILE" ]; then
  for candidate in "$OPENWEBUI_RUNTIME_DIR"/docker-compose*.yml; do
    [ -f "$candidate" ] || continue
    OPENWEBUI_COMPOSE_FILE="$candidate"
    break
  done
fi

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
require_directory "$WEKNORA_DIR"
require_directory "$OPENWEBUI_RUNTIME_DIR"
require_directory "$HERMES_HOME"
require_file "$WEKNORA_ENV_FILE"
require_file "$OPENWEBUI_COMPOSE_FILE"

POSTGRES_CONTAINER="$(discover_container "$POSTGRES_CONTAINER" postgres 'postgres')"
WEKNORA_APP_CONTAINER="$(discover_container "$WEKNORA_APP_CONTAINER" app 'weknora.*app')"
OPENWEBUI_CONTAINER="$(discover_container "$OPENWEBUI_CONTAINER" open-webui 'open-webui')"
[ -n "$POSTGRES_CONTAINER" ] || fail "container discovery" "PostgreSQL container not found"
[ -n "$WEKNORA_APP_CONTAINER" ] || fail "container discovery" "WeKnora app container not found"
[ -n "$OPENWEBUI_CONTAINER" ] || fail "container discovery" "Open WebUI container not found"
require_running_container "$POSTGRES_CONTAINER"
require_running_container "$WEKNORA_APP_CONTAINER"
require_running_container "$OPENWEBUI_CONTAINER"

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
mkdir -p "$DEST/weknora" "$DEST/open-webui" "$DEST/hermes" "$DEST/secrets" \
  "$DEST/governance" "$DEST/config" "$DEST/state"
chmod 700 "$DEST" "$DEST/weknora" "$DEST/open-webui" "$DEST/hermes" "$DEST/secrets" "$DEST/governance" "$DEST/state"
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
WEKNORA_CONFIG_ITEMS=()
for item in .env config skills docker-compose.yml docker-compose.yaml \
  docker-compose.eaio.yml docker-compose.eaio.override.yml \
  docker-compose.eaio-override.yml mcp-server; do
  [ -e "$WEKNORA_DIR/$item" ] && WEKNORA_CONFIG_ITEMS+=("$item")
done
[ "${#WEKNORA_CONFIG_ITEMS[@]}" -gt 0 ] \
  || fail "WeKnora config" "no runtime configuration files found"
tar -czf "$DEST/weknora/runtime-config.tar.gz" -C "$WEKNORA_DIR" \
  "${WEKNORA_CONFIG_ITEMS[@]}"
cp "$OPENWEBUI_COMPOSE_FILE" "$DEST/open-webui/docker-compose.yml"
if [ -f "$OPENWEBUI_RUNTIME_DIR/.env" ]; then
  cp "$OPENWEBUI_RUNTIME_DIR/.env" "$DEST/open-webui/.env"
  OPENWEBUI_ENV_MANIFEST_LINE="- Open WebUI protected runtime environment: open-webui/.env"
  pass "Open WebUI runtime env" "protected .env archived without printing values"
else
  warn "Open WebUI runtime env" "not present: $OPENWEBUI_RUNTIME_DIR/.env"
fi
pass "WeKnora config" "runtime .env, config, skills, Compose, MCP"
pass "Open WebUI config" "Compose manifest and protected runtime env when present"

if [ -f "$COMPANY_CONFIG" ]; then
  cp "$COMPANY_CONFIG" "$DEST/config/company.yaml"
  COMPANY_CONFIG_MANIFEST_LINE="- Active company configuration: config/company.yaml"
  pass "Company configuration" "protected active config archived"
else
  warn "Company configuration" "not present: $COMPANY_CONFIG"
fi

if [ -f "$DEPLOYMENT_STATE_FILE" ]; then
  cp "$DEPLOYMENT_STATE_FILE" "$DEST/state/deployment-state.md"
  DEPLOYMENT_STATE_MANIFEST_LINE="- Protected operational deployment state: state/deployment-state.md"
  pass "Deployment state" "protected operational handoff/evidence state archived"
else
  warn "Deployment state" "not present: $DEPLOYMENT_STATE_FILE"
fi

# Hermes archive includes every present employee Profile, gateway configuration,
# state databases, MCP/Skills configuration, and OAuth/provider state required
# for recovery. The archive is intentionally private.
HERMES_ITEMS=()
for item in .env config.yaml SOUL.md auth.json state.db gateway_state.json state profiles skills; do
  [ -e "$HERMES_HOME/$item" ] && HERMES_ITEMS+=("$item")
done
[ "${#HERMES_ITEMS[@]}" -gt 0 ] \
  || fail "Hermes state" "no Hermes runtime state found"
tar --exclude='*.sock' -czf "$DEST/hermes/runtime.tar.gz" -C "$HERMES_HOME" \
  "${HERMES_ITEMS[@]}"
tar -czf "$DEST/hermes/repository-profiles-skills.tar.gz" -C "$REPO_ROOT" \
  profiles skills
if [ -f "$LAUNCH_AGENT_PLIST" ]; then
  cp "$LAUNCH_AGENT_PLIST" "$DEST/hermes/ai.hermes.gateway.plist"
  LAUNCH_AGENT_MANIFEST_LINE="- Hermes LaunchAgent definition: hermes/ai.hermes.gateway.plist"
  pass "Hermes LaunchAgent" "protected supervisor definition archived"
else
  warn "Hermes LaunchAgent" "not present: $LAUNCH_AGENT_PLIST"
fi
pass "Hermes state" "Profiles, gateway config, state, Skills/MCP"
# Media transcription is conditional. Successful jobs clean their temporary
# audio, while reviewed Markdown transcripts are durable deployment material
# and must be included in future encrypted backup generations when enabled.
if [ "$MEDIA_TRANSCRIPTION_ENABLED" = true ] && [ -d "$EAIO_RUNTIME_DIR/media-transcription/transcripts" ]; then
  mkdir -p "$DEST/media-transcription"
  tar -czf "$DEST/media-transcription/transcripts.tar.gz" \
    -C "$EAIO_RUNTIME_DIR/media-transcription" transcripts
  MEDIA_TRANSCRIPTION_MANIFEST_LINE="- Media transcription reviewed transcripts: media-transcription/transcripts.tar.gz"
  pass "Media transcripts" "reviewed transcript archive"
elif [ "$MEDIA_TRANSCRIPTION_ENABLED" = true ]; then
  warn "Media transcripts" "enabled but transcript directory absent"
else
  pass "Media transcripts" "disabled / state absent"
fi

# Runtime credential inventory is recoverable but never copied into Git or the
# non-secret manifest. Keep it in a separate restricted archive when the
# deployment provides one; otherwise recovery must re-enter credentials from
# protected stores.
if [ -d "$RUNTIME_CREDENTIALS_DIR" ]; then
  tar -czf "$DEST/secrets/runtime-credentials.tar.gz" -C "$EAIO_RUNTIME_DIR" \
    "$(basename "$RUNTIME_CREDENTIALS_DIR")"
  CREDENTIALS_MANIFEST_LINE="secrets/runtime-credentials.tar.gz"
  pass "Secret recovery" "restricted local archive; values not printed"
else
  warn "Secret recovery" "separate runtime credential directory absent; protected stores remain external"
fi

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
$OPENWEBUI_ENV_MANIFEST_LINE
- Hermes Profiles, state, gateway configuration, Skills/MCP: hermes/runtime.tar.gz
- Repository Profile templates and Skills: hermes/repository-profiles-skills.tar.gz
$LAUNCH_AGENT_MANIFEST_LINE
- Protected runtime credentials: $CREDENTIALS_MANIFEST_LINE
$COMPANY_CONFIG_MANIFEST_LINE
$DEPLOYMENT_STATE_MANIFEST_LINE
$MEDIA_TRANSCRIPTION_MANIFEST_LINE
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
