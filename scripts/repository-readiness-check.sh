#!/bin/sh
set -eu

# Static Enterprise AI Office repository deployability check.
# This does not install software or prove a runtime deployment works. It verifies
# that the repository still contains the contracts/adapters/playbooks required
# for an AI agent to resolve Core/Configured/Production deployment paths.

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PASS=0
FAIL=0

pass() {
  PASS=$((PASS + 1))
  printf '%-48s PASS\n' "$1"
}

fail() {
  FAIL=$((FAIL + 1))
  printf '%-48s FAIL - %s\n' "$1" "$2"
}

require_file() {
  rel="$1"
  if [ -f "$ROOT/$rel" ]; then
    pass "$rel"
  else
    fail "$rel" "missing"
  fi
}

require_text() {
  rel="$1"
  text="$2"
  label="$3"
  if [ ! -f "$ROOT/$rel" ]; then
    fail "$label" "$rel missing"
  elif grep -F "$text" "$ROOT/$rel" >/dev/null 2>&1; then
    pass "$label"
  else
    fail "$label" "expected reference not found in $rel"
  fi
}

printf '%s\n' 'Enterprise AI Office Repository Readiness'
printf '%s\n' '----------------------------------------'

# Agent execution contract and declarative inputs.
for path in \
  README.md \
  AGENTS.md \
  DEPLOY.md \
  docs/COMPLETENESS.md \
  docs/ARCHITECTURE.md \
  docs/DEPLOYMENT.md \
  docs/ACCEPTANCE-TESTS.md \
  docs/SECURITY.md \
  docs/PROFILE-STANDARD.md \
  docs/KNOWLEDGE.md \
  docs/CLIENT-RBAC.md \
  docs/BACKUP-RESTORE.md \
  docs/OPERATIONS.md \
  docs/UPGRADE.md \
  config/company.example.yaml \
  config/capabilities.yaml \
  config/validated-stack.yaml \
  config/.env.example \
  state/DEPLOYMENT-STATE.template.md
do
  require_file "$path"
done

# Core implementation assets.
for path in \
  infrastructure/weknora/README.md \
  infrastructure/weknora/PROVISIONING.md \
  infrastructure/hermes/README.md \
  infrastructure/hermes/default.config.example.yaml \
  infrastructure/hermes/default.env.example \
  infrastructure/hermes/general.config.example.yaml \
  infrastructure/hermes/general.env.example \
  infrastructure/open-webui/README.md \
  infrastructure/open-webui/PROVISIONING.md \
  infrastructure/open-webui/docker-compose.yml
do
  require_file "$path"
done

# Conditional capability closure assets.
for path in \
  infrastructure/hermes/specialist.config.example.yaml \
  infrastructure/hermes/specialist.env.example \
  infrastructure/hermes-webui/README.md \
  infrastructure/coding-agents/README.md \
  infrastructure/coding-agents/technical-profile.config.example.yaml \
  infrastructure/hermes/features/README.md \
  infrastructure/hermes/features/MESSAGING.md \
  infrastructure/hermes/features/EMPLOYEE-MEMORY.md \
  infrastructure/access/README.md \
  infrastructure/access/OPEN-WEBUI-OIDC.md
do
  require_file "$path"
done

# Production control helpers.
for path in \
  scripts/preflight.sh \
  scripts/health-check.sh \
  scripts/backup.sh \
  scripts/restore.sh
do
  require_file "$path"
done

# Guard against high-impact contract drift.
require_text DEPLOY.md 'config/capabilities.yaml' 'Golden Path uses capability registry'
require_text DEPLOY.md 'PRODUCTION READY' 'Golden Path reaches Production Ready'
require_text AGENTS.md 'CONFIGURED READY' 'Agent contract knows Configured Ready'
require_text docs/ACCEPTANCE-TESTS.md 'Configured Ready result' 'Acceptance has Configured Ready gate'
require_text docs/ACCEPTANCE-TESTS.md 'Enterprise identity / SSO' 'Acceptance covers SSO when enabled'
require_text docs/ACCEPTANCE-TESTS.md 'Hermes administrative Web UI' 'Acceptance covers hermes-webui when enabled'
require_text config/company.example.yaml 'target_readiness:' 'Company config declares readiness target'
require_text config/company.example.yaml 'capabilities:' 'Company config declares optional capabilities'
require_text config/capabilities.yaml 'infrastructure/weknora/PROVISIONING.md' 'Core capability has WeKnora provisioning path'
require_text config/capabilities.yaml 'infrastructure/open-webui/PROVISIONING.md' 'Core capability has Open WebUI provisioning path'
require_text config/capabilities.yaml 'infrastructure/hermes/features/MESSAGING.md' 'Messaging capability has pinned execution path'
require_text config/capabilities.yaml 'infrastructure/hermes/features/EMPLOYEE-MEMORY.md' 'Employee memory capability has fail-closed gate'
require_text config/capabilities.yaml 'infrastructure/access/OPEN-WEBUI-OIDC.md' 'SSO capability has pinned OIDC execution path'
require_text infrastructure/weknora/PROVISIONING.md '"capabilities": ["retrieve"]' 'WeKnora contract scopes runtime retrieval key'
require_text infrastructure/weknora/PROVISIONING.md 'BLOCKED — MIGRATION REQUIRED' 'WeKnora contract blocks unsafe embedding drift'
require_text infrastructure/hermes/features/MESSAGING.md 'hermes gateway setup' 'Messaging contract uses native Hermes setup'
require_text infrastructure/hermes/features/EMPLOYEE-MEMORY.md 'BLOCKED — REQUIRED INPUT' 'Employee memory gate fails closed without isolation'
require_text config/capabilities.yaml 'technical-profile.config.example.yaml' 'Coding capability has executable Profile template'
require_text README.md 'CONFIGURED READY' 'README explains configured completeness'

printf '%s\n' '----------------------------------------'
printf 'Summary: %s PASS, %s FAIL\n' "$PASS" "$FAIL"
printf '%s\n' 'Static PASS means repository execution paths are present; it does not replace real runtime acceptance.'

if [ "$FAIL" -gt 0 ]; then
  exit 2
fi

exit 0