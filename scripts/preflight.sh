#!/bin/sh
set -u

# Enterprise AI Office deployment preflight.
# Read-only: inventories the host before any installation or mutation.

PASS=0
WARN=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '%-28s PASS%s\n' "$1" "${2:+ - $2}"; }
warn() { WARN=$((WARN + 1)); printf '%-28s WARN%s\n' "$1" "${2:+ - $2}"; }
fail() { FAIL=$((FAIL + 1)); printf '%-28s FAIL%s\n' "$1" "${2:+ - $2}"; }

check_cmd() {
  label="$1"
  cmd="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    path=$(command -v "$cmd")
    pass "$label" "$path"
  else
    warn "$label" "not found"
  fi
}

printf '%s\n' 'Enterprise AI Office Preflight'
printf '%s\n' '-----------------------------'

# OS
os_name=$(uname -s 2>/dev/null || echo unknown)
os_arch=$(uname -m 2>/dev/null || echo unknown)
pass "OS" "$os_name / $os_arch"

if [ "$os_name" = "Darwin" ]; then
  mac_ver=$(sw_vers -productVersion 2>/dev/null || true)
  [ -n "$mac_ver" ] && pass "macOS version" "$mac_ver" || warn "macOS version" "unknown"
fi

# Hostname
host_name=$(hostname 2>/dev/null || true)
[ -n "$host_name" ] && pass "Hostname" "$host_name" || warn "Hostname" "unknown"

# Root disk free space
if df -Pk / >/dev/null 2>&1; then
  disk_line=$(df -Pk / | awk 'NR==2')
  used=$(printf '%s\n' "$disk_line" | awk '{print $5}')
  avail_kb=$(printf '%s\n' "$disk_line" | awk '{print $4}')
  pass "Root disk" "used $used, available ${avail_kb} KB"
else
  warn "Root disk" "unable to inspect"
fi

# Memory (best effort, platform-specific)
if [ "$os_name" = "Darwin" ] && command -v sysctl >/dev/null 2>&1; then
  mem_bytes=$(sysctl -n hw.memsize 2>/dev/null || true)
  if [ -n "$mem_bytes" ]; then
    mem_gb=$((mem_bytes / 1024 / 1024 / 1024))
    pass "Memory" "${mem_gb} GB"
  else
    warn "Memory" "unable to inspect"
  fi
elif [ -r /proc/meminfo ]; then
  mem_kb=$(awk '/MemTotal:/ {print $2}' /proc/meminfo)
  mem_gb=$((mem_kb / 1024 / 1024))
  pass "Memory" "${mem_gb} GB"
else
  warn "Memory" "unable to inspect"
fi

check_cmd "Git" git
check_cmd "Docker CLI" docker
check_cmd "Python" python3
check_cmd "Node" node
check_cmd "npm" npm
check_cmd "Hermes" hermes
check_cmd "Codex" codex
check_cmd "Claude Code" claude
check_cmd "GitHub CLI" gh
check_cmd "curl" curl

# Docker daemon
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    pass "Docker daemon" "reachable"
  else
    warn "Docker daemon" "CLI found, daemon not reachable"
  fi
fi

# Existing Hermes state
if [ -d "${HOME}/.hermes" ]; then
  warn "Existing Hermes home" "${HOME}/.hermes exists; inspect before changing"
else
  pass "Existing Hermes home" "none detected"
fi

# Existing common runtime directory
if [ -d "/Users/Shared/enterprise-ai-office" ]; then
  warn "EAIO runtime dir" "/Users/Shared/enterprise-ai-office exists; inspect before changing"
elif [ "$os_name" = "Darwin" ]; then
  pass "EAIO runtime dir" "not present"
fi

# Git repository sanity if run from project checkout
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  branch=$(git branch --show-current 2>/dev/null || true)
  changes=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  pass "Ops repository" "branch ${branch:-unknown}, ${changes:-0} local change(s)"
else
  warn "Ops repository" "script not run inside a Git checkout"
fi

printf '%s\n' '-----------------------------'
printf 'Summary: %s PASS, %s WARN, %s FAIL\n' "$PASS" "$WARN" "$FAIL"
printf '%s\n' 'Warnings are expected for optional components. Inspect existing installations before any mutation.'

if [ "$FAIL" -gt 0 ]; then
  exit 2
fi

if [ "$WARN" -gt 0 ]; then
  exit 1
fi

exit 0
