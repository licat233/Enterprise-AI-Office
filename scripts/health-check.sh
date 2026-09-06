#!/bin/sh
set -u

# Enterprise AI Office read-only health check.
# Configure optional endpoints/thresholds via environment variables.

PASS=0
WARN=0
FAIL=0

say_pass() {
  PASS=$((PASS + 1))
  printf '%-28s %s\n' "$1" "PASS${2:+ - $2}"
}

say_warn() {
  WARN=$((WARN + 1))
  printf '%-28s %s\n' "$1" "WARN${2:+ - $2}"
}

say_fail() {
  FAIL=$((FAIL + 1))
  printf '%-28s %s\n' "$1" "FAIL${2:+ - $2}"
}

check_http() {
  label="$1"
  url="$2"

  if [ -z "$url" ]; then
    say_warn "$label" "health URL not configured"
    return
  fi

  if ! command -v curl >/dev/null 2>&1; then
    say_warn "$label" "curl not installed"
    return
  fi

  code=$(curl -L -sS -o /dev/null -w '%{http_code}' --connect-timeout 3 --max-time 8 "$url" 2>/dev/null || true)
  case "$code" in
    2??|3??) say_pass "$label" "HTTP $code" ;;
    000|'')  say_fail "$label" "unreachable: $url" ;;
    *)       say_fail "$label" "HTTP $code" ;;
  esac
}

printf '%s\n' 'Enterprise AI Office Health Check'
printf '%s\n' '---------------------------------'

# Disk usage of root filesystem. This is a host-level warning only; deployments
# may later add specific data-volume checks.
DISK_WARN_PERCENT=${EAIO_DISK_WARN_PERCENT:-70}
DISK_FAIL_PERCENT=${EAIO_DISK_FAIL_PERCENT:-85}

disk_used=$(df -P / 2>/dev/null | awk 'NR==2 {gsub("%", "", $5); print $5}')
if [ -n "${disk_used:-}" ]; then
  if [ "$disk_used" -ge "$DISK_FAIL_PERCENT" ] 2>/dev/null; then
    say_fail "Host disk" "${disk_used}% used"
  elif [ "$disk_used" -ge "$DISK_WARN_PERCENT" ] 2>/dev/null; then
    say_warn "Host disk" "${disk_used}% used"
  else
    say_pass "Host disk" "${disk_used}% used"
  fi
else
  say_warn "Host disk" "unable to determine usage"
fi

# Docker check.
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    say_pass "Docker" "daemon reachable"
  else
    say_fail "Docker" "CLI present but daemon unreachable"
  fi
else
  say_warn "Docker" "not installed or not in PATH"
fi

# HTTP services. URLs are intentionally configurable because upstream ports and
# health paths may change between tested releases.
check_http "Open WebUI" "${OPEN_WEBUI_HEALTH_URL:-}"
check_http "WeKnora" "${WEKNORA_HEALTH_URL:-}"
check_http "Hermes API" "${HERMES_HEALTH_URL:-}"

if [ -n "${HERMES_WEBUI_HEALTH_URL:-}" ]; then
  check_http "hermes-webui" "$HERMES_WEBUI_HEALTH_URL"
fi

# v2 Email Governance is conditional. Absence of a configured health URL means
# the capability is not being checked by this generic helper; it must not make a
# v1-only deployment fail merely because Email is disabled.
if [ -n "${EAIO_GOVERNANCE_HEALTH_URL:-}" ]; then
  check_http "Email Governance" "$EAIO_GOVERNANCE_HEALTH_URL"
fi

# Hermes CLI status.
if command -v hermes >/dev/null 2>&1; then
  if hermes status >/dev/null 2>&1; then
    say_pass "Hermes CLI/status" "available"
  else
    say_warn "Hermes CLI/status" "command exists but status failed"
  fi
else
  say_warn "Hermes CLI/status" "hermes not in PATH"
fi

# Optional backup freshness marker.
if [ -n "${EAIO_BACKUP_SUCCESS_MARKER:-}" ]; then
  marker="$EAIO_BACKUP_SUCCESS_MARKER"
  max_age_hours=${EAIO_BACKUP_MAX_AGE_HOURS:-36}

  if [ ! -e "$marker" ]; then
    say_fail "Backup freshness" "marker missing: $marker"
  else
    now=$(date +%s)
    if stat -f %m "$marker" >/dev/null 2>&1; then
      modified=$(stat -f %m "$marker")
    elif stat -c %Y "$marker" >/dev/null 2>&1; then
      modified=$(stat -c %Y "$marker")
    else
      modified=''
    fi

    if [ -z "$modified" ]; then
      say_warn "Backup freshness" "cannot read marker timestamp"
    else
      age_seconds=$((now - modified))
      max_seconds=$((max_age_hours * 3600))
      age_hours=$((age_seconds / 3600))
      if [ "$age_seconds" -gt "$max_seconds" ]; then
        say_fail "Backup freshness" "last marker ${age_hours}h ago"
      else
        say_pass "Backup freshness" "last marker ${age_hours}h ago"
      fi
    fi
  fi
else
  say_warn "Backup freshness" "marker not configured"
fi

printf '%s\n' '---------------------------------'
printf 'Summary: %s PASS, %s WARN, %s FAIL\n' "$PASS" "$WARN" "$FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 2
fi

if [ "$WARN" -gt 0 ]; then
  exit 1
fi

exit 0
