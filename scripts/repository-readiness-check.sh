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
  docs/V2-STAGE-CONTRACTS.md \
  docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md \
  docs/V2-GOVERNANCE-RUNTIME.md \
  docs/V2-SEND-RECONCILIATION.md \
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
  infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md \
  infrastructure/open-webui/V2-APPROVAL-ACTION.md \
  infrastructure/open-webui/v2_approve_draft_action.py \
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
  infrastructure/email/governance/README.md \
  infrastructure/email/governance/schema.sql \
  infrastructure/email/governance/migrations/002_send_reconciliation.sql \
  infrastructure/email/governance/test_schema.py \
  infrastructure/email/governance/test_send_reconciliation.py \
  infrastructure/email/tencent-exmail/README.md \
  infrastructure/email/tencent-exmail/imap_readonly_mcp.py \
  infrastructure/email/tencent-exmail/imap.env.example \
  infrastructure/email/tencent-exmail/test_imap_readonly.py \
  infrastructure/email/tencent-exmail/smtp_send_adapter.py \
  infrastructure/email/tencent-exmail/smtp.env.example \
  infrastructure/email/tencent-exmail/test_smtp_send_adapter.py \
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
require_text docs/V2-STAGE-CONTRACTS.md 'STAGE CONTRACTS FROZEN' 'v2 ID-3 stage contracts are frozen'
require_text docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md 'IDENTITY / AUTHORIZATION INSTALLATION CONTRACT FROZEN' 'v2 ID-4 identity contract is frozen'
require_text docs/V2-GOVERNANCE-RUNTIME.md 'GOVERNANCE RUNTIME CONTRACT FROZEN' 'v2 ID-5 governance runtime contract is frozen'
require_text docs/V2-SEND-RECONCILIATION.md 'SEND / RECONCILIATION INSTALLATION CONTRACT FROZEN' 'v2 ID-6 send/reconciliation contract is frozen'

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
require_text config/company.example.yaml 'forwarder_credential_ref:' 'Company config exposes trusted-forwarder credential reference'
require_text config/company.private.example.yaml 'client_credential_ref:' 'Private overlay uses symbolic email credential reference'
require_text config/company.private.example.yaml 'openwebui-governance-forwarder-token' 'Private overlay uses symbolic governance forwarder credential'
require_text config/company.private.example.yaml 'email.send' 'Private overlay demonstrates operation-scoped mailbox grants'
require_text config/.env.example 'EAIO_GOVERNANCE_URL' 'Runtime bindings expose private Governance URL'
require_text config/.env.example 'EAIO_TRUSTED_FORWARDER_TOKEN' 'Runtime bindings expose protected forwarder token'
require_text config/capabilities.yaml 'docs/V2-CONFIG-PROTECTED-INPUTS.md' 'Email capability has protected-input contract'
require_text config/capabilities.yaml 'docs/V2-STAGE-CONTRACTS.md' 'Email capability has stage closure contract'
require_text config/capabilities.yaml 'docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md' 'Email capability has identity authorization contract'
require_text config/capabilities.yaml 'docs/V2-GOVERNANCE-RUNTIME.md' 'Email capability has governance runtime contract'
require_text config/capabilities.yaml 'docs/V2-SEND-RECONCILIATION.md' 'Email capability has send/reconciliation contract'
require_text config/capabilities.yaml 'governance_runtime_contract:' 'Email capability declares governance runtime closure'
require_text config/capabilities.yaml 'send_reconciliation_contract:' 'Email capability declares send/reconciliation closure'
require_text config/capabilities.yaml 'infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md' 'Email capability has Open WebUI communication provisioning path'
require_text config/capabilities.yaml 'infrastructure/open-webui/v2_approve_draft_action.py' 'Email capability has deterministic approval Action template'
require_text config/capabilities.yaml 'infrastructure/email/governance/schema.sql' 'Email capability has governance SQLite schema'
require_text config/capabilities.yaml 'infrastructure/email/governance/migrations/002_send_reconciliation.sql' 'Email capability has send/reconciliation schema migration'
require_text config/capabilities.yaml 'infrastructure/email/governance/test_schema.py' 'Email capability has governance offline test'
require_text config/capabilities.yaml 'infrastructure/email/governance/test_send_reconciliation.py' 'Email capability has send/reconciliation offline test'
require_text config/capabilities.yaml 'infrastructure/email/tencent-exmail/smtp_send_adapter.py' 'Email capability has narrow SMTP provider adapter'
require_text config/capabilities.yaml 'infrastructure/email/tencent-exmail/test_smtp_send_adapter.py' 'Email capability has SMTP adapter offline test'
require_text config/capabilities.yaml 'mandatory_when_enabled:' 'Email capability declares mandatory stage closure'
require_text config/capabilities.yaml 'stage_4_governed_send' 'Email capability requires governed-send stage'
require_text config/capabilities.yaml 'open-webui-governance-forwarder-credential' 'Email capability declares forwarder secret class'
require_text config/capabilities.yaml 'required_secret_classes:' 'Email capability declares required secret classes'
require_text infrastructure/email/governance/schema.sql 'draft_review_bindings' 'Governance schema binds review message to exact Draft'
require_text infrastructure/email/governance/schema.sql 'approval_claims' 'Governance schema enforces approval claim record'
require_text infrastructure/email/governance/migrations/002_send_reconciliation.sql 'logical_sends' 'ID-6 migration persists logical sends'
require_text infrastructure/email/governance/migrations/002_send_reconciliation.sql 'send_attempts' 'ID-6 migration persists provider attempts'
require_text infrastructure/email/governance/migrations/002_send_reconciliation.sql 'send_reconciliations' 'ID-6 migration persists reconciliation evidence'
require_text infrastructure/email/governance/test_schema.py 'PASS — v2 governance SQLite/hash/review-binding contract' 'Governance offline test has deterministic PASS marker'
require_text infrastructure/email/governance/test_send_reconciliation.py 'PASS — v2 send/reconciliation SQLite contract' 'Send/reconciliation offline test has deterministic PASS marker'
require_text infrastructure/email/tencent-exmail/smtp_send_adapter.py 'OUTCOME_UNKNOWN' 'SMTP adapter exposes ambiguous-outcome classification'
require_text infrastructure/email/tencent-exmail/smtp_send_adapter.py 'session.data(message_bytes)' 'SMTP adapter has explicit DATA boundary'
require_text infrastructure/email/tencent-exmail/test_smtp_send_adapter.py 'test_timeout_after_data_begins_is_unknown' 'SMTP adapter tests ambiguous DATA timeout'
require_text infrastructure/email/tencent-exmail/test_smtp_send_adapter.py 'test_any_recipient_rejection_aborts_before_data' 'SMTP adapter tests all-recipient-before-DATA rule'
require_text infrastructure/open-webui/v2_approve_draft_action.py '"type": "confirmation"' 'Approval Action uses native Open WebUI confirmation dialog'
require_text infrastructure/open-webui/v2_approve_draft_action.py '/v1/actions/resolve-current-review' 'Approval Action resolves server-owned review subject'
require_text infrastructure/open-webui/v2_approve_draft_action.py '/v1/actions/approve-current-review' 'Approval Action commits exact reviewed subject'
require_text docs/acceptance/TENCENT-EXMAIL.md 'Stage 1 — read-only email' 'Provider acceptance maps tests to v2 stages'
require_text docs/acceptance/TENCENT-EXMAIL.md 'OUTCOME_UNKNOWN cannot create another attempt' 'Provider acceptance blocks blind retry after ambiguous send'
require_text infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md '{{USER_ID}}' 'Open WebUI communication path forwards authenticated user ID'
require_text infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md '{{USER_GROUP_IDS}}' 'Open WebUI communication path forwards current group IDs'
require_text infrastructure/email/tencent-exmail/README.md 'previous direct Hermes MCP registration template is no longer the reference path' 'Provider playbook rejects obsolete direct Hermes registration'
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
