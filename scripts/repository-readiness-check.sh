#!/bin/sh
set -eu

# Static Enterprise AI Office blueprint/deployability contract check.
# This does not install software, advance the blueprint lifecycle, activate a
# real deployment task, or prove a runtime deployment works. It verifies that
# the repository still contains the contracts/adapters/playbooks and lifecycle
# gates required for safe AI-agent behavior.

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

# Agent contract, blueprint lifecycle authority, and declarative inputs.
for path in \
  README.md \
  AGENTS.md \
  state/PROJECT-PHASE.yaml \
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
  docs/V2-SCOPE.md \
  docs/V2-EMAIL-DESIGN.md \
  docs/V2-COMMUNICATION-FOLLOWUP-DESIGN.md \
  docs/V2-DESIGN-REVIEW.md \
  docs/V2-PHASE-STATUS.md \
  docs/V2-IMPLEMENTATION-PLAN.md \
  docs/V2-INSTALLATION-ARCHITECTURE.md \
  docs/V2-CONFIG-PROTECTED-INPUTS.md \
  config/company.example.yaml \
  config/company.private.example.yaml \
  config/capabilities.yaml \
  config/validated-stack.yaml \
  config/.env.example \
  state/DEPLOYMENT-STATE.template.md
do
  require_file "$path"
done

# Core installation-blueprint assets.
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

# Conditional capability closure/design-support assets.
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
  infrastructure/access/OPEN-WEBUI-OIDC.md \
  infrastructure/email/tencent-exmail/README.md \
  infrastructure/email/tencent-exmail/imap_readonly_mcp.py \
  infrastructure/email/tencent-exmail/imap.env.example \
  infrastructure/email/tencent-exmail/hermes.mcp.example.yaml \
  infrastructure/email/tencent-exmail/test_imap_readonly.py \
  docs/acceptance/TENCENT-EXMAIL.md \
  ontology/examples/email-communication.yaml
do
  require_file "$path"
done

# Production/deployment control helpers that the installation blueprint may use.
for path in \
  scripts/preflight.sh \
  scripts/health-check.sh \
  scripts/backup.sh \
  scripts/restore.sh
do
  require_file "$path"
done

# Guard against blueprint-lifecycle / real-deployment semantic drift.
require_text state/PROJECT-PHASE.yaml 'repository_role: blueprint_repository' 'Repository role is blueprint repository'
require_text state/PROJECT-PHASE.yaml 'current_phase: installation_design' 'Current blueprint phase is installation design'
require_text state/PROJECT-PHASE.yaml 'status: complete' 'System design remains complete'
require_text state/PROJECT-PHASE.yaml 'status: active' 'Installation design is active'
require_text state/PROJECT-PHASE.yaml 'blueprint_validation' 'Blueprint lifecycle includes validation'
require_text state/PROJECT-PHASE.yaml 'implicit_transition_allowed: false' 'Implicit blueprint transition is disabled'
require_text state/PROJECT-PHASE.yaml 'real_deployment_task:' 'Real deployment has a separate gate'
require_text state/PROJECT-PHASE.yaml 'active: false' 'No real deployment task is active by default'
require_text state/PROJECT-PHASE.yaml 'requires_explicit_target: true' 'Real deployment requires an explicit target'
require_text state/PROJECT-PHASE.yaml 'Installation design means designing how an AI agent will install the system; it does not mean performing a real installation.' 'Installation design is not real installation'
require_text AGENTS.md 'system blueprint + installation blueprint' 'Agent contract defines dual blueprint mission'
require_text AGENTS.md 'A real company deployment is a separate consumer activity' 'Agent contract separates deployment from blueprint work'
require_text AGENTS.md 'Installation blueprint is not a live installation' 'Agent contract prevents installation-design drift'
require_text AGENTS.md 'Blueprint milestones' 'Agent contract separates blueprint maturity'
require_text AGENTS.md 'Deployed-system readiness' 'Agent contract separates deployment readiness'
require_text docs/V2-PHASE-STATUS.md 'BLUEPRINT PHASE: INSTALLATION DESIGN' 'v2 status matches installation-design phase'
require_text docs/V2-PHASE-STATUS.md 'SYSTEM DESIGN: COMPLETE' 'v2 status preserves completed system design'
require_text docs/V2-PHASE-STATUS.md 'REAL DEPLOYMENT TASK: INACTIVE' 'v2 status says real deployment inactive'
require_text docs/V2-INSTALLATION-ARCHITECTURE.md 'INSTALLATION ARCHITECTURE FROZEN' 'v2 ID-1 installation architecture is frozen'
require_text docs/V2-CONFIG-PROTECTED-INPUTS.md 'CONFIG / SECRET INPUT CONTRACT FROZEN' 'v2 ID-2 protected-input contract is frozen'

# Guard against high-impact deployment/capability contract drift.
require_text DEPLOY.md 'config/capabilities.yaml' 'Golden Path uses capability registry'
require_text DEPLOY.md 'PRODUCTION READY' 'Golden Path reaches Production Ready'
require_text AGENTS.md 'CONFIGURED READY' 'Agent contract knows Configured Ready'
require_text docs/ACCEPTANCE-TESTS.md 'Configured Ready result' 'Acceptance has Configured Ready gate'
require_text docs/ACCEPTANCE-TESTS.md 'Enterprise identity / SSO' 'Acceptance covers SSO when enabled'
require_text docs/ACCEPTANCE-TESTS.md 'Hermes administrative Web UI' 'Acceptance covers hermes-webui when enabled'
require_text config/company.example.yaml 'target_readiness:' 'Company config declares readiness target'
require_text config/company.example.yaml 'capabilities:' 'Company config declares optional capabilities'
require_text config/company.example.yaml 'mailbox_grants:' 'Company config exposes mailbox-scoped grants'
require_text config/company.example.yaml 'send_requires_human_approval: true' 'Email config defaults to human-approved sends'
require_text config/company.private.example.yaml 'client_credential_ref:' 'Private overlay uses symbolic email credential reference'
require_text config/company.private.example.yaml 'email.send' 'Private overlay demonstrates operation-scoped mailbox grants'
require_text config/capabilities.yaml 'docs/V2-CONFIG-PROTECTED-INPUTS.md' 'Email capability has protected-input contract'
require_text config/capabilities.yaml 'required_secret_classes:' 'Email capability declares required secret classes'
require_text config/capabilities.yaml 'infrastructure/weknora/PROVISIONING.md' 'Core capability has WeKnora provisioning path'
require_text config/capabilities.yaml 'infrastructure/open-webui/PROVISIONING.md' 'Core capability has Open WebUI provisioning path'
require_text config/capabilities.yaml 'infrastructure/hermes/features/MESSAGING.md' 'Messaging capability has pinned execution path'
require_text config/capabilities.yaml 'infrastructure/hermes/features/EMPLOYEE-MEMORY.md' 'Employee memory capability has fail-closed gate'
require_text config/capabilities.yaml 'infrastructure/access/OPEN-WEBUI-OIDC.md' 'SSO capability has pinned OIDC execution path'
require_text config/capabilities.yaml 'email_tencent_exmail:' 'Capability registry contains Tencent Exmail integration'
require_text config/capabilities.yaml 'infrastructure/email/tencent-exmail/imap_readonly_mcp.py' 'Email capability has read-only adapter path'
require_text config/capabilities.yaml 'docs/acceptance/TENCENT-EXMAIL.md' 'Email capability has provider acceptance path'
require_text config/capabilities.yaml 'ontology/examples/email-communication.yaml' 'Email capability has ontology design fixture'
require_text infrastructure/email/tencent-exmail/imap_readonly_mcp.py 'readonly=True' 'Email adapter opens mailbox read-only'
require_text infrastructure/email/tencent-exmail/imap_readonly_mcp.py 'BODY.PEEK[]' 'Email adapter uses non-Seen body fetch'
require_text infrastructure/email/tencent-exmail/test_imap_readonly.py 'test_folder_scope_fails_closed' 'Email adapter has fail-closed folder test'
require_text infrastructure/email/tencent-exmail/test_imap_readonly.py 'test_get_email_uses_body_peek' 'Email adapter has BODY.PEEK safety test'
require_text docs/V2-DESIGN-REVIEW.md 'V2 DESIGN STATUS: FROZEN' 'v2 core design review remains frozen'
require_text infrastructure/weknora/PROVISIONING.md '"capabilities": ["retrieve"]' 'WeKnora contract scopes runtime retrieval key'
require_text infrastructure/weknora/PROVISIONING.md 'BLOCKED — MIGRATION REQUIRED' 'WeKnora contract blocks unsafe embedding drift'
require_text infrastructure/hermes/features/MESSAGING.md 'hermes gateway setup' 'Messaging contract uses native Hermes setup'
require_text infrastructure/hermes/features/EMPLOYEE-MEMORY.md 'BLOCKED — REQUIRED INPUT' 'Employee memory gate fails closed without isolation'
require_text config/capabilities.yaml 'technical-profile.config.example.yaml' 'Coding capability has executable Profile template'
require_text README.md 'CONFIGURED READY' 'README explains configured completeness'

printf '%s\n' '----------------------------------------'
printf 'Summary: %s PASS, %s FAIL\n' "$PASS" "$FAIL"
printf '%s\n' 'Static PASS means blueprint and deployment contracts are present; it does not advance blueprint phase, activate a real deployment, or replace target runtime acceptance.'

if [ "$FAIL" -gt 0 ]; then
  exit 2
fi

exit 0
