#!/bin/sh
set -eu

# Static Enterprise AI Office blueprint/deployability contract check.
# This does not install software, advance the blueprint lifecycle, activate a
# real deployment task, or prove a runtime deployment works. It verifies that
# the repository still contains the contracts/adapters/playbooks and lifecycle
# gates required for safe AI-agent behavior.
#
# Portable/public use:
#   EAO_REPOSITORY_ONLY=1 sh scripts/repository-readiness-check.sh
#
# The default non-repository-only mode is retained for the ARMOR reference
# runtime lineage and may expect protected private/department-profile evidence.
# Fresh clones and other-company blueprint work must use repository-only mode.

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PASS=0
FAIL=0
REPOSITORY_ONLY=${EAO_REPOSITORY_ONLY:-0}

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

require_no_text() {
  rel="$1"
  text="$2"
  label="$3"
  if [ ! -f "$ROOT/$rel" ]; then
    fail "$label" "$rel missing"
  elif grep -F "$text" "$ROOT/$rel" >/dev/null 2>&1; then
    fail "$label" "forbidden reference found in $rel"
  else
    pass "$label"
  fi
}

require_absent() {
  rel="$1"
  label="$2"
  if [ ! -e "$ROOT/$rel" ]; then
    pass "$label"
  else
    fail "$label" "$rel must not be active"
  fi
}

printf '%s\n' 'Enterprise AI Office Repository Readiness'
printf '%s\n' '----------------------------------------'
if [ "$REPOSITORY_ONLY" = "1" ]; then
  printf '%s\n' 'Mode: public repository-only'
else
  printf '%s\n' 'Mode: reference/runtime-inclusive (protected ARMOR profile evidence may be required)'
fi

# Agent contract, blueprint lifecycle authority, and declarative inputs.
for path in \
  README.md \
  README.zh-CN.md \
  AGENTS.md \
  REPRODUCE.md \
  VALIDATE.md \
  validation/FRESH-AGENT-TASK.md \
  validation/scorecard.yaml \
  validation/REPORT.template.md \
  scripts/validate-fresh-agent-kit.py \
  scripts/check-yaml-syntax.sh \
  scripts/check-repository-links.py \
  scripts/check-declarative-paths.py \
  scripts/check-capability-acceptance.py \
  scripts/check-capability-selectors.py \
  scripts/check-validated-stack-consistency.py \
  scripts/check-public-repository-hygiene.py \
  scripts/check-frozen-baselines.py \
  scripts/run-public-offline-tests.sh \
  config/eao-manifest.yaml \
  docs/CAPABILITY-REUSE-PASS.md \
  docs/README.md \
  docs/REPOSITORY-GOVERNANCE.md \
  docs/DEPLOYMENT-PRACTICES.md \
  state/REAL-DEPLOYMENT-STATUS.md \
  reference/armor/reference-index.yaml \
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
  docs/V2-RECOVERY-CLEAN-HOST.md \
  docs/V2-INSTALLATION-DESIGN-REVIEW.md \
  config/company.example.yaml \
  config/company.private.example.yaml \
  config/capabilities.yaml \
  config/mcp-registry.yaml \
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
  infrastructure/hermes/PROVISIONING.md \
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
  infrastructure/email/governance/backup_state.py \
  infrastructure/email/governance/restore_state.py \
  infrastructure/email/governance/test_schema.py \
  infrastructure/email/governance/test_send_reconciliation.py \
  infrastructure/email/governance/test_recovery.py \
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
  scripts/restore.sh \
  scripts/phase4a_migration_check.py \
  scripts/phase4c_runtime_check.py \
  scripts/test_phase4c_runtime.py \
  scripts/phase5a_social_runtime_check.py \
  scripts/test_phase5a_social.py \
  scripts/phase5b_mic_runtime_check.py \
  scripts/test_phase5b_mic.py \
  scripts/test_phase5b1_mic_authority.py \
  scripts/test_phase5b2_mic_authority_dedup.py \
  scripts/phase5c_operations_skills_triage_check.py \
  scripts/phase5d_product_materials_check.py \
  scripts/test_phase5d_product_materials.py \
  scripts/phase6_web_research_check.py \
  docs/PHASE5B.2-MIC-SKILL-VAULT-AUTHORITY-DEDUPLICATION.md \
  docs/PHASE5D-WEBSITE-PRODUCT-MATERIALS-MIGRATION.md \
  skills/shared/department/armor-memory/scripts/armor-route.py \
  skills/shared/department/armor-memory/scripts/armor-vault-mcp.py \
  skills/shared/department/armor-mic-product-optimization/SKILL.md \
  skills/shared/department/armor-website-product-materials/SKILL.md \
  skills/shared/department/armor-social-media-pipeline/SKILL.md \
  skills/shared/department/armor-video-content-rules/SKILL.md \
  skills/shared/toolscout/SKILL.md
do
  require_file "$path"
done

for path in \
  infrastructure/web-research/adapter.py \
  infrastructure/web-research/test_adapter.py \
  docs/ENTERPRISE-WEB-RESEARCH-V1.md
do
  require_file "$path"
done

require_text 'ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范.md' 'status: historical-reference' 'Legacy ARMOR v1 document is historical'
require_text 'ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范.md' 'Historical reference only — not the current execution contract.' 'Legacy ARMOR v1 document does not claim current authority'
require_text docs/REPOSITORY-GOVERNANCE.md '`main` is the canonical public blueprint state' 'Repository governance defines main authority'
require_text config/eao-manifest.yaml 'machine_readable_index: reference/armor/reference-index.yaml' 'Project manifest exposes ARMOR reference index'
require_text config/eao-manifest.yaml 'authority: config/validated-stack.yaml' 'Manifest delegates Core version truth to validated stack'
require_text DEPLOY.md 'current reproducible Core version/commit authority is `config/validated-stack.yaml`' 'Golden Path names validated-stack as sole current Core version authority'
require_text state/DEPLOYMENT-STATE.md 'Version-authority note:' 'Historical Hermes 0.21.1 observation is explicitly scoped'
require_text state/REAL-DEPLOYMENT-STATUS.md 'future reference-runtime version changes must' 'Current reference status requires explicit version transition evidence'
require_text docs/UPGRADE.md 'protected operational state created from state/DEPLOYMENT-STATE.template.md' 'Upgrade flow reads protected operational state'
require_no_text docs/UPGRADE.md '16. Update DEPLOYMENT-STATE' 'Upgrade flow does not write ambiguous historical deployment state'
require_text docs/OPERATIONS.md 'not the live operational state store' 'Operations distinguishes public historical state from live state'
require_text docs/DEPLOYMENT.md 'Treat the repository' 'Detailed deployment distinguishes historical from protected operational state'
require_text config/eao-manifest.yaml 'deployment_state_template: state/DEPLOYMENT-STATE.template.md' 'Manifest exposes protected deployment-state template'
require_text config/eao-manifest.yaml 'duplication_policy: do_not_copy_component_versions_or_host_runtime_values_here' 'Manifest forbids Core version duplication'
require_text config/validated-stack.yaml 'status: current-reference-baseline' 'Validated stack marks current reference baseline'
require_text config/validated-stack.yaml 'alternative_inherits_reference_qualification: false' 'Validated stack prevents compatible runtime from inheriting reference qualification'
require_text config/validated-stack.yaml 'first_validated_on: 2026-09-06' 'Validated stack distinguishes first qualification date'
require_text config/validated-stack.yaml 'reference_runtime_last_confirmed_on: 2026-09-11' 'Validated stack records current reference runtime confirmation'
require_text config/validated-stack.yaml 'does_not_claim_new_clean_host_validation: true' 'Runtime confirmation does not impersonate clean-host validation'
require_text config/validated-stack.yaml 'upgrade_policy: docs/UPGRADE.md' 'Validated stack delegates upgrades to upgrade policy'
require_text config/validated-stack.yaml 'upstream_repository: https://github.com/Tencent/WeKnora.git' 'Validated stack records WeKnora upstream provenance'
require_text config/validated-stack.yaml 'upstream_repository: https://github.com/NousResearch/hermes-agent.git' 'Validated stack records Hermes upstream provenance'
require_text config/validated-stack.yaml 'source_ref_type: commit_only_no_version_tag' 'Validated stack does not invent a Hermes version tag'
require_text config/validated-stack.yaml 'upstream_repository: https://github.com/open-webui/open-webui.git' 'Validated stack records Open WebUI upstream provenance'
require_text DEPLOY.md '### 4.1 Deterministic Core acquisition' 'Golden Path defines deterministic Core acquisition'
require_text DEPLOY.md 'Exact reference container runtime: OrbStack-provided Docker + Compose' 'Golden Path identifies exact reference container runtime'
require_text scripts/preflight.sh 'fail "$label" "required for EAO Core; not found"' 'Preflight fails on missing Core prerequisites'
require_text scripts/preflight.sh 'docker compose plugin is required for EAO Core' 'Preflight requires Docker Compose'
require_text scripts/preflight.sh 'optional capability/operator tool not found' 'Preflight distinguishes optional tooling'
require_text DEPLOY.md '### 4.2 Post-acquisition Core identity assertions' 'Golden Path distinguishes liveness from runtime identity'
require_text DEPLOY.md 'state/DEPLOYMENT-STATE.template.md' 'Golden Path uses protected deployment-state template'
require_text DEPLOY.md '${EAIO_RUNTIME_DIR}/state/deployment-state.md' 'Golden Path aligns protected state with backup default'
require_text DEPLOY.md 'EAIO_DEPLOYMENT_STATE_FILE' 'Golden Path documents protected state backup override'
require_no_text DEPLOY.md 'Update `state/DEPLOYMENT-STATE.md` with actual runtime truth' 'Golden Path never writes real runtime truth into historical public state'
require_text state/DEPLOYMENT-STATE.template.md 'Do **not** overwrite the repository' 'Deployment-state template protects historical public state'
require_text docs/ARCHITECTURE.md 'protected operational copy created from `state/DEPLOYMENT-STATE.template.md` + real runtime' 'Architecture points live state to protected operational record'
require_text docs/ARCHITECTURE.md 'Historical sanitized deployment evidence' 'Architecture distinguishes historical public evidence'
require_text docs/ACCEPTANCE-TESTS.md 'protected operational record created from `state/DEPLOYMENT-STATE.template.md`' 'Acceptance evidence uses protected operational state'
require_text docs/COMPLETENESS.md 'protected operational deployment state created from `state/DEPLOYMENT-STATE.template.md`' 'Configured Ready records state privately'
require_text docs/V2-RECOVERY-CLEAN-HOST.md 'protected operational state created from `state/DEPLOYMENT-STATE.template.md`' 'v2 Email recovery uses protected operational state'
require_text docs/V2-RECOVERY-CLEAN-HOST.md 'not an allowed live Email runtime-state store' 'v2 Email recovery rejects public historical state as live store'
require_text docs/V2-DESIGN-REVIEW.md 'protected operational state created from DEPLOYMENT-STATE.template' 'v2 design review uses protected observed-state authority'
require_text docs/V2-IMPLEMENTATION-PLAN.md 'protected operational state created from state/DEPLOYMENT-STATE.template.md' 'v2 implementation plan uses protected observed-state authority'
require_text docs/V2-CONFIG-PROTECTED-INPUTS.md '`state/DEPLOYMENT-STATE.md` is not the live state store.' 'v2 protected-input contract separates historical and live state'
require_no_text docs/V2-RECOVERY-CLEAN-HOST.md '`state/DEPLOYMENT-STATE.md` or the protected equivalent records non-secret truth' 'v2 recovery no longer permits public historical state as live evidence'
require_text docs/CLIENT-RBAC.md 'do not use the historical sanitized `state/DEPLOYMENT-STATE.md` as the live RBAC evidence store' 'RBAC evidence stays out of public historical state'
require_no_text docs/ARCHITECTURE.md '| Current deployment state | `state/DEPLOYMENT-STATE.md` + real runtime |' 'Architecture does not revive public historical state as live authority'
require_no_text THIRD_PARTY_NOTICES.md 'record the exact repository and commit/version in `state/DEPLOYMENT-STATE.md`' 'Third-party provenance does not write runtime state into public history'
require_text state/DEPLOYMENT-STATE.template.md 'Company logical KB ID' 'Deployment-state template records WeKnora logical/runtime handoff'
require_text state/DEPLOYMENT-STATE.template.md 'Hermes served-set / route handoff' 'Deployment-state template records Hermes route handoff'
require_text state/DEPLOYMENT-STATE.template.md 'Group runtime mappings' 'Deployment-state template records Open WebUI group runtime mapping'
require_text scripts/backup.sh 'EAIO_DEPLOYMENT_STATE_FILE' 'Backup supports protected operational deployment state'
require_text scripts/backup.sh 'state/deployment-state.md' 'Backup archives protected deployment-state handoff artifact'
require_text scripts/restore.sh 'state/deployment-state.md' 'Restore materializes protected deployment-state handoff artifact'
require_text docs/BACKUP-RESTORE.md 'Protected operational deployment state' 'Backup contract includes protected deployment state'
require_text docs/ACCEPTANCE-TESTS.md 'protected operational deployment-state/handoff record backed up' 'Production acceptance requires deployment-state backup'
require_text config/company.example.yaml 'require_off_primary_disk_copy: true' 'Generic production schema requires off-primary backup copy'
require_text docs/BACKUP-RESTORE.md 'final `PRODUCTION READY` acceptance' 'Backup standard distinguishes final Production Ready evidence'
require_text docs/BACKUP-RESTORE.md 'restore must be sourced' 'Production Ready requires restore from approved off-primary copy'
require_text docs/ACCEPTANCE-TESTS.md 'off-primary copy checksum/integrity verified after transfer' 'Production acceptance verifies transferred backup integrity'
require_text docs/ACCEPTANCE-TESTS.md 'final isolated restore source is the approved off-primary copy' 'Production acceptance requires external-copy restore source'
require_text state/DEPLOYMENT-STATE.template.md 'Last isolated restore source' 'Protected state records restore source'
require_text validation/scorecard.yaml 'off_primary_restore_evidence_when_production_ready' 'Fresh-Agent runtime scorecard checks off-primary restore evidence'
require_text VALIDATE.md 'approved off-primary copy' 'Authorized validation checks independent backup evidence'
require_text DEPLOY.md 'infrastructure/hermes/PROVISIONING.md' 'Golden Path uses Hermes provisioning contract'
require_text docs/CLIENT-RBAC.md 'Company logical ID' 'Client RBAC distinguishes company group IDs from display names'
require_text DEPLOY.md 'company logical ID → display name → runtime group UUID' 'Golden Path preserves three-layer group identity'
require_no_text DEPLOY.md 'Create baseline groups `All-Employees` and `AI-Admins`' 'Golden Path does not invent transformed Open WebUI group names'
require_text infrastructure/open-webui/PROVISIONING.md 'company logical ID' 'Open WebUI provisioning preserves three-layer group identity'
require_text infrastructure/open-webui/PROVISIONING.md 'BLOCKED — AMBIGUOUS STATE' 'Open WebUI group reconciliation fails closed on ambiguity'
require_text infrastructure/open-webui/PROVISIONING.md 'container → host Hermes bridge acceptance' 'Open WebUI provisioning proves backend-to-Hermes bridge'
require_text infrastructure/open-webui/PROVISIONING.md '### 3.1 Pinned API-route provenance' 'Open WebUI provisioning records pinned API route provenance'
require_text infrastructure/open-webui/PROVISIONING.md '2a960a59fe1dbbd35282f0556b3666d81102e781' 'Open WebUI provisioning provenance matches validated source commit'
require_text docs/UPGRADE.md 'backend/open_webui/main.py' 'Open WebUI upgrade requires route-prefix requalification'
require_text docs/UPGRADE.md 'routers/auths.py' 'Open WebUI upgrade requires auth route requalification'
require_text docs/ACCEPTANCE-TESTS.md 'Open WebUI backend can reach the configured host-native Hermes Profile route' 'Core acceptance requires container-to-Hermes bridge'
require_text DEPLOY.md 'backend model enumeration rather than only host-side curl' 'Compatible runtime revalidation uses backend bridge evidence'
require_text infrastructure/open-webui/PROVISIONING.md 'It does **not** own authoritative EAO company' 'Open WebUI provisioning does not duplicate company knowledge'
require_text infrastructure/open-webui/PROVISIONING.md 'EAO-managed Open WebUI native company Knowledge attachments: none' 'Open WebUI provisioning records no EAO duplicate knowledge attachment'
require_text docs/KNOWLEDGE.md 'Open WebUI is not a second company Knowledge authority' 'Knowledge contract keeps WeKnora authoritative'
require_text docs/ACCEPTANCE-TESTS.md 'General Assistant authoritative company knowledge resolves through Hermes → WeKnora' 'Core acceptance checks authoritative knowledge path'
require_text infrastructure/open-webui/PROVISIONING.md 'Do not create a second group whose name is a transformed logical' 'Open WebUI provisioning blocks duplicate transformed group names'
require_text infrastructure/hermes/PROVISIONING.md 'hermes profile create general --no-skills --no-alias' 'Hermes provisioning creates narrow General Profile without bundled Skills'
require_text infrastructure/hermes/PROVISIONING.md '### 3.1 Pinned Hermes behavior provenance' 'Hermes provisioning records pinned behavior provenance'
require_text infrastructure/hermes/PROVISIONING.md 'f1ccf436a27522c1bb5d36383a6f13b950676338' 'Hermes provisioning provenance matches validated source commit'
require_text infrastructure/hermes/PROVISIONING.md 'Profile requests resolve that Profile' 'Hermes provisioning provenance scopes named Profile credentials'
require_text infrastructure/hermes/PROVISIONING.md 'default/owner key' 'Hermes provisioning provenance blocks default-key inheritance'
require_text docs/UPGRADE.md 'hermes_cli/subcommands/profile.py' 'Hermes upgrade requires Profile CLI requalification'
require_text docs/UPGRADE.md 'gateway/platforms/api_server.py' 'Hermes upgrade requires API server behavior requalification'
require_text infrastructure/hermes/PROVISIONING.md 'Do **not** set `API_SERVER_ENABLED=true` on `general`' 'Hermes provisioning keeps shared listener on default Profile'
require_text infrastructure/hermes/PROVISIONING.md 'default/admin key → /p/general/...                  DENY' 'Hermes provisioning requires Profile credential isolation'
require_text infrastructure/hermes/PROVISIONING.md 'GET /p/general/v1/models' 'Hermes provisioning validates named Profile model identity'
require_text docs/ACCEPTANCE-TESTS.md 'Core runtime identity matches `config/validated-stack.yaml`' 'Core acceptance requires exact runtime identity'
require_text scripts/health-check.sh 'does not prove the exact validated component identity/version/commit' 'Health check does not impersonate identity verification'
require_text DEPLOY.md 'Do not infer upstream repositories or installation methods from product names.' 'Golden Path blocks upstream guessing'
require_text infrastructure/open-webui/docker-compose.yml 'Derived pin: config/validated-stack.yaml -> Open WebUI' 'Open WebUI compose identifies validated-stack derived pin'
require_text infrastructure/weknora/docker-compose.demo.override.yml 'Derived pin: config/validated-stack.yaml -> WeKnora' 'WeKnora override identifies validated-stack derived pin'
require_text infrastructure/hermes/default.config.example.yaml 'Derived schema pin: config/validated-stack.yaml -> Hermes Agent' 'Hermes default example identifies validated-stack derived pin'
require_text infrastructure/hermes/general.config.example.yaml 'Derived schema pin: config/validated-stack.yaml -> Hermes Agent' 'Hermes general example identifies validated-stack derived pin'
require_no_text config/eao-manifest.yaml 'weknora: v0.8.0' 'Manifest does not duplicate WeKnora version'
require_no_text config/eao-manifest.yaml 'hermes_agent: 0.21.0' 'Manifest does not duplicate Hermes version'
require_no_text config/eao-manifest.yaml 'open_webui: v0.11.3' 'Manifest does not duplicate Open WebUI version'
require_text reference/armor/reference-index.yaml 'normative: false' 'ARMOR reference index is non-normative'
require_text reference/armor/reference-index.yaml 'deployable_company_config: false' 'ARMOR reference index is non-deployable'
require_text reference/armor/reference-index.yaml 'status: deployed_frozen_reference' 'ARMOR reference index records Operations reference lane'
require_text reference/armor/reference-index.yaml 'status: deployed_validated_reference' 'ARMOR reference records deployed Media Transcription'
require_text reference/armor/reference-index.yaml 'enabled_in_current_ARMOR_reference: true' 'ARMOR reference distinguishes deployed optional Media Transcription'
require_text README.md 'Media Transcription optional capability' 'English README surfaces current Media Transcription status'
require_text README.zh-CN.md 'Media Transcription 可选能力' 'Chinese README surfaces current Media Transcription status'
require_text reference/armor/reference-index.yaml 'live_mailbox_deployment_claim: false' 'ARMOR reference index does not claim live mailbox deployment'
require_text reference/armor/reference-index.yaml 'Do not infer Operations as a generic EAO default.' 'ARMOR reference index blocks generic Operations inheritance'

require_text docs/REPOSITORY-GOVERNANCE.md 'require a pull request before merge' 'Repository governance defines PR protection target'
require_text THIRD_PARTY_NOTICES.md '`licat233/toolscout`' 'Third-party notices include current ToolScout provenance'
require_text THIRD_PARTY_NOTICES.md '`h4ckf0r0day/obscura`' 'Third-party notices include current Obscura provenance'
require_text THIRD_PARTY_NOTICES.md '`QwenAudio/SenseVoice`' 'Third-party notices resolve SenseVoice source provenance'
require_text THIRD_PARTY_NOTICES.md '`iic/SenseVoiceSmall`' 'Third-party notices record SenseVoice runtime model identity'
require_text THIRD_PARTY_NOTICES.md 'source-code MIT license as the license for every' 'Third-party notices separate SenseVoice source and model terms'
require_text infrastructure/media-transcription/README.md '`QwenAudio/SenseVoice`' 'Media transcription contract records SenseVoice upstream identity'

require_text scripts/README.md 'EAO_REPOSITORY_ONLY=1 sh scripts/repository-readiness-check.sh' 'Scripts README documents portable readiness mode'
require_text scripts/repository-readiness-check.sh 'Fresh clones and other-company blueprint work must use repository-only mode.' 'Readiness script documents reference-specific full mode'

require_no_text config/.env.example '/Users/armor' 'Generic env template has no ARMOR home path'
require_no_text infrastructure/web-research/adapter.py '/Users/armor' 'Web Research adapter has portable path defaults'
require_no_text infrastructure/hermes/operations-routing.example.yaml '/Users/armor' 'Operations routing example has no ARMOR home path'

require_text config/mcp-registry.yaml 'runtime_state_scope: sanitized_ARMOR_reference_snapshot' 'MCP registry marks reference runtime snapshot'
require_text config/mcp-registry.yaml 'fresh_deployment_rule: recompute_runtime_and_health_do_not_inherit_reference_flags' 'MCP registry blocks reference runtime inheritance'
require_text config/README.md 'A fresh deployment must recompute' 'Config guide explains MCP runtime recomputation'

require_text .github/workflows/repository-readiness.yml 'actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4' 'Repository CI pins checkout action'
require_text .github/workflows/repository-readiness.yml 'persist-credentials: false' 'Repository CI does not persist checkout credentials'
require_text .github/workflows/repository-readiness.yml 'runs-on: ubuntu-24.04' 'Repository CI pins runner image family'
require_text .github/workflows/repository-readiness.yml 'fetch-depth: 0' 'Repository CI fetches full history for frozen baselines'
require_text .github/workflows/repository-readiness.yml 'contents: read' 'Repository CI keeps read-only contents permission'

require_no_text config/README.md 'limited to its existing' 'Config guide has no obsolete WeKnora-only Operations claim'
require_text config/README.md 'The reusable baseline does not require an `operations` Profile at all.' 'Config guide distinguishes ARMOR Operations reference exposure'
require_text docs/OPERATIONS.md 'For the ARMOR reference implementation it is closed/frozen' 'Operations manual records current Web Research reference state'

# Guard against blueprint-lifecycle / real-deployment semantic drift.
require_text state/PROJECT-PHASE.yaml 'repository_role: blueprint_repository' 'Repository role is blueprint repository'
require_text state/PROJECT-PHASE.yaml 'current_phase: installation_design' 'Current blueprint phase remains installation design'
require_text state/PROJECT-PHASE.yaml 'completion_milestone: INSTALLATION DESIGN COMPLETE' 'Installation design completion milestone exists'
require_text state/PROJECT-PHASE.yaml 'transition_ready: true' 'Installation design is transition-ready only after explicit direction'
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
require_text docs/V2-PHASE-STATUS.md 'INSTALLATION DESIGN: COMPLETE' 'v2 status records completed installation design'
require_text docs/V2-PHASE-STATUS.md 'REAL DEPLOYMENT TASK: INACTIVE' 'v2 status says real deployment inactive'
require_text docs/V2-INSTALLATION-ARCHITECTURE.md 'INSTALLATION ARCHITECTURE FROZEN' 'v2 ID-1 installation architecture is frozen'
require_text docs/V2-CONFIG-PROTECTED-INPUTS.md 'CONFIG / SECRET INPUT CONTRACT FROZEN' 'v2 ID-2 protected-input contract is frozen'
require_text docs/V2-STAGE-CONTRACTS.md 'STAGE CONTRACTS FROZEN' 'v2 ID-3 stage contracts are frozen'
require_text docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md 'IDENTITY / AUTHORIZATION INSTALLATION CONTRACT FROZEN' 'v2 ID-4 identity contract is frozen'
require_text docs/V2-GOVERNANCE-RUNTIME.md 'GOVERNANCE RUNTIME CONTRACT FROZEN' 'v2 ID-5 governance runtime contract is frozen'
require_text docs/V2-SEND-RECONCILIATION.md 'SEND / RECONCILIATION INSTALLATION CONTRACT FROZEN' 'v2 ID-6 send/reconciliation contract is frozen'
require_text docs/V2-RECOVERY-CLEAN-HOST.md 'RECOVERY / CLEAN-HOST INSTALLATION CONTRACT FROZEN' 'v2 ID-7 recovery/clean-host contract is frozen'
require_text docs/V2-INSTALLATION-DESIGN-REVIEW.md 'INSTALLATION DESIGN FINAL REVIEW: PASS' 'v2 installation design final review passed'

# Guard against high-impact deployment/capability contract drift.
require_text DEPLOY.md 'config/capabilities.yaml' 'Golden Path uses capability registry'
require_text REPRODUCE.md 'infrastructure/weknora/PROVISIONING.md' 'Reproduction Stage B uses WeKnora provisioning contract'
require_text REPRODUCE.md 'infrastructure/hermes/PROVISIONING.md' 'Reproduction Stage C uses Hermes provisioning contract'
require_text REPRODUCE.md 'infrastructure/open-webui/PROVISIONING.md' 'Reproduction Stage D uses Open WebUI provisioning contract'
require_text REPRODUCE.md 'state/DEPLOYMENT-STATE.template.md' 'Reproduction contract includes protected deployment-state template'
require_text AGENTS.md 'the `core_provisioning` map in `config/eao-manifest.yaml`' 'Agent contract requires manifest Core provisioning map'
require_text REPRODUCE.md '### Stage F — resolve enabled conditional capabilities' 'Reproduction contract separates conditional capabilities'
require_text REPRODUCE.md 'If a capability is not enabled for the target, do not install it merely because the' 'Reproduction contract blocks reference-driven over-installation'
require_text config/eao-manifest.yaml 'reference_presence_does_not_imply_enablement: true' 'Manifest blocks reference capability inheritance'
require_text config/eao-manifest.yaml 'instantiate_only_capabilities_explicitly_enabled_for_target' 'Manifest encodes conditional capability rule'
require_text DEPLOY.md 'PRODUCTION READY' 'Golden Path reaches Production Ready'
require_text AGENTS.md 'CONFIGURED READY' 'Agent contract knows Configured Ready'
require_text docs/ACCEPTANCE-TESTS.md 'Configured Ready result' 'Acceptance has Configured Ready gate'
require_text docs/ACCEPTANCE-TESTS.md 'Enterprise identity / SSO' 'Acceptance covers SSO when enabled'
require_text docs/ACCEPTANCE-TESTS.md 'Hermes administrative Web UI' 'Acceptance covers hermes-webui when enabled'
require_text config/company.example.yaml 'target_readiness:' 'Company config declares readiness target'
require_text config/company.example.yaml 'capabilities:' 'Company config declares optional capabilities'
require_text config/company.example.yaml 'profile_allowlists:' 'Generic company MCP allowlist is profile-scoped'
require_text config/company.example.yaml 'general:' 'Generic company MCP allowlist binds declared general Profile'
require_no_text config/company.example.yaml 'operations_allowlist:' 'Generic company schema does not predeclare ARMOR Operations'
require_text config/company.private.example.yaml 'profile_allowlists:' 'Private overlay uses profile-scoped MCP allowlists'
require_no_text config/company.private.example.yaml 'operations_allowlist:' 'Private example does not invent Operations Profile'
require_text config/company.example.yaml 'mailbox_grants:' 'Company config exposes mailbox-scoped grants'
require_text config/company.example.yaml 'send_requires_human_approval: true' 'Email config defaults to human-approved sends'
require_text config/company.example.yaml 'forwarder_credential_ref:' 'Company config exposes trusted-forwarder credential reference'
require_text config/company.private.example.yaml 'client_credential_ref:' 'Private overlay uses symbolic email credential reference'
require_text config/company.private.example.yaml 'openwebui-governance-forwarder-token' 'Private overlay uses symbolic governance forwarder credential'
require_text config/company.example.yaml 'core_provisioning:' 'Company schema declares Core provisioning protected-input slots'
require_text config/company.example.yaml 'weknora-owner-provisioning-credentials' 'Company schema declares WeKnora owner provisioning secret class'
require_text config/company.private.example.yaml 'weknora-owner-password:' 'Private example declares WeKnora owner symbolic secret ref'
require_text config/company.private.example.yaml 'weknora-db-password:' 'Private example declares WeKnora DB symbolic secret ref'
require_text config/company.private.example.yaml 'weknora-jwt-secret:' 'Private example declares WeKnora JWT symbolic secret ref'
require_text config/company.private.example.yaml 'hermes-default-api-key:' 'Private example declares Hermes default symbolic secret ref'
require_text config/company.private.example.yaml 'hermes-general-api-key:' 'Private example declares Hermes general symbolic secret ref'
require_text config/company.private.example.yaml 'openwebui-admin-password:' 'Private example declares Open WebUI admin symbolic secret ref'
require_text config/.env.example 'DB_PASSWORD=<GENERATE_STRONG_SECRET>' 'Core env uses native WeKnora DB_PASSWORD binding'
require_text config/.env.example 'REDIS_PASSWORD=<GENERATE_STRONG_SECRET>' 'Core env uses native WeKnora REDIS_PASSWORD binding'
require_text config/.env.example 'JWT_SECRET=<GENERATE_STRONG_SECRET>' 'Core env requires strong WeKnora JWT secret'
require_no_text config/.env.example 'WEKNORA_DB_PASSWORD=' 'Core env does not invent unsupported WeKnora DB variable'
require_text docs/V2-CONFIG-PROTECTED-INPUTS.md '### 6.1 Core provisioning secret-reference baseline' 'Protected-input contract defines Core symbolic refs'
require_text infrastructure/weknora/PROVISIONING.md 'core_provisioning.weknora.runtime_secret_refs' 'WeKnora provisioning consumes Core symbolic refs'
require_text infrastructure/hermes/PROVISIONING.md 'core_provisioning.hermes.default_api_key_ref' 'Hermes provisioning consumes Core symbolic refs'
require_text infrastructure/open-webui/PROVISIONING.md 'core_provisioning.open_webui.admin_identity' 'Open WebUI provisioning consumes Core symbolic refs'
require_text config/company.private.example.yaml 'email.send' 'Private overlay demonstrates operation-scoped mailbox grants'
require_text config/.env.example 'EAIO_GOVERNANCE_URL' 'Runtime bindings expose private Governance URL'
require_text config/.env.example 'EAIO_GOVERNANCE_STATE_DB' 'Runtime bindings expose Governance SQLite state path'
require_text config/.env.example 'EAIO_GOVERNANCE_HEALTH_URL' 'Runtime bindings expose optional Governance health URL'
require_text config/.env.example 'EAIO_TRUSTED_FORWARDER_TOKEN' 'Runtime bindings expose protected forwarder token'
require_text config/capabilities.yaml 'docs/V2-CONFIG-PROTECTED-INPUTS.md' 'Email capability has protected-input contract'
require_text config/mcp-registry.yaml 'anysearch:' 'Phase 4A registry contains anysearch'
require_text config/mcp-registry.yaml 'OPERATIONS_READ' 'Phase 4A registry classifies anysearch'
require_text config/mcp-registry.yaml 'firecrawl-mcp:' 'Phase 4A registry contains firecrawl'
require_text config/mcp-registry.yaml 'obscura:' 'Phase 4A registry contains obscura'
require_text config/mcp-registry.yaml 'paddle_ocr:' 'Phase 4A registry contains Paddle OCR'
require_text config/mcp-registry.yaml 'toolscout:' 'Phase 4A registry contains ToolScout'
require_text config/mcp-registry.yaml 'upstream_repository: h4ckf0r0day/obscura' 'Obscura registry records upstream repository'
require_text config/mcp-registry.yaml 'upstream_release: v0.2.2' 'Obscura registry records validated release'
require_text config/mcp-registry.yaml 'upstream_repository: licat233/toolscout' 'ToolScout registry records upstream repository'
require_text config/mcp-registry.yaml 'upstream_release: v1.0.0' 'ToolScout registry records validated release'
require_text config/mcp-registry.yaml 'schema_version: 2' 'Phase 4C registry records runtime truth'
require_text config/mcp-registry.yaml 'SHARED_AGENT_INFRASTRUCTURE' 'ToolScout is shared agent infrastructure'
require_text config/mcp-registry.yaml 'adapter_required: true' 'Firecrawl requires the Enterprise-owned adapter'
require_text config/mcp-registry.yaml 'raw_tools_exposed_to_operations: false' 'Raw Firecrawl tools are not Operations-exposed'
require_text config/mcp-registry.yaml 'scope: raw_firecrawl_mcp_entry_only' 'Raw Firecrawl blocker has explicit health scope'
require_text config/mcp-registry.yaml 'enterprise-web-research' 'Enterprise Web Research adapter remains registered'
require_text config/mcp-registry.yaml 'does_not_apply_to:' 'Raw Firecrawl blocker is scoped away from employee adapter'
require_text docs/MCP-CONTROL-PLANE.md 'does **not** mean employee Web Research is broken' 'Control-plane guide distinguishes raw and adapter health'
require_text config/mcp-registry.yaml 'armor-vault-scoped-router:' 'Scoped Vault Router is registered'
require_text skills/shared/department/armor-memory/scripts/route.sh 'armor-route.py' 'ARMOR memory wrapper resolves local Router'
require_text skills/shared/department/armor-memory/scripts/armor-vault-mcp.py 'save_article_package' 'Scoped Article save tool is present'
require_text skills/shared/department/armor-memory/scripts/armor-vault-mcp.py 'save_social_package' 'Scoped Social save tool is present'
require_text skills/shared/department/armor-memory/scripts/armor-vault-mcp.py 'save_mic_product_package' 'Scoped MIC save tool is present'
require_text skills/shared/department/armor-memory/scripts/armor-vault-mcp.py 'save_website_product_materials_package' 'Scoped Website Product Materials save tool is present'
require_text skills/shared/department/armor-memory/scripts/armor-route.py 'mic-product' 'MIC product route is present'
require_text skills/shared/department/armor-memory/scripts/armor-route.py 'product-materials' 'Website Product Materials route is present'
require_text skills/shared/department/armor-memory/SKILL.md 'product-materials' 'ARMOR memory Skill documents Product Materials routing'
require_text skills/shared/department/armor-website-product-materials/SKILL.md 'ARMOR-Website-Product-Materials-Standard-v1.0.md' 'Product Materials Skill references the canonical Vault Standard'
require_text skills/shared/department/armor-website-product-materials/SKILL.md 'PRODUCT_AUTHORITY_REVIEW_REQUIRED' 'Product Materials Skill has the authority blocker'
require_text skills/shared/department/armor-website-product-materials/SKILL.md 'save_website_product_materials_package' 'Product Materials Skill binds the scoped save'
require_text docs/PHASE5D-WEBSITE-PRODUCT-MATERIALS-MIGRATION.md 'Website Product Materials: PASS' 'Phase 5D report records migration status'
require_text scripts/test_phase5d_product_materials.py 'PRODUCT_AUTHORITY_REVIEW_REQUIRED' 'Phase 5D tests cover authority review'
require_text scripts/phase5d_product_materials_check.py 'Operations receives the exact scoped Router tool allowlist' 'Phase 5D runtime check covers the scoped allowlist'
require_text skills/shared/department/armor-product-visual/SKILL.md 'ARMOR-Product-Visual-Standard-v1.0.md' 'Product Visual Skill references the canonical Vault Standard'
require_text skills/shared/department/armor-product-visual/SKILL.md 'READY_FOR_GENERATION' 'Product Visual Skill is a generation handoff only'
require_text skills/shared/department/armor-product-visual/SKILL.md 'save_product_visual_package' 'Product Visual Skill binds the scoped save'
require_text skills/shared/department/armor-product-visual/SKILL.md 'Agent Delegate' 'Product Visual keeps delegation out of scope'
require_text skills/shared/department/armor-memory/scripts/armor-route.py 'product-visual' 'Product Visual route is present'
require_text skills/shared/department/armor-memory/scripts/armor-vault-mcp.py 'save_product_visual_package' 'Scoped Product Visual save tool is present'
require_text skills/shared/department/armor-memory/scripts/armor-vault-mcp.py 'PRODUCT_VISUAL_REQUIRED_FILES' 'Product Visual closed contract is present'
require_text config/mcp-registry.yaml 'product_visual_write_scope:' 'Product Visual write boundary is registered'
require_text config/capabilities.yaml 'armor_product_visual:' 'Product Visual capability is registered'
require_text config/capabilities.yaml 'enterprise_web_research:' 'Enterprise Web Research capability is registered'
require_text config/capabilities.yaml 'enabled_when: capabilities.enterprise_web_research.enabled == true' 'Web Research uses typed company selector'
require_text config/capabilities.yaml 'source: company_configuration' 'Generic capability selector paths are machine-checkable'
require_text config/capabilities.yaml 'path: capabilities.email.provider' 'Compound Email selector records provider path'
require_text config/capabilities.yaml 'rule: any_employee_facing_profile_beyond_general' 'Specialist Profile selector records structural rule'
require_text config/capabilities.yaml 'section: Stage 3 — Final Acceptance & Freeze' 'Web Research closes against final frozen acceptance'
require_text config/capabilities.yaml 'scope: ARMOR_reference_specific' 'ARMOR-specific workflow selector scope is explicit'
require_text config/capabilities.yaml 'generic_company_schema_field: none' 'ARMOR-specific workflows do not pollute generic company schema'
require_text config/mcp-registry.yaml 'enterprise-web-research:' 'Enterprise Web Research adapter is registered'
require_text docs/ENTERPRISE-WEB-RESEARCH-V1.md 'UNTRUSTED_WEB_CONTENT' 'Web Research trust boundary is documented'
require_text docs/ENTERPRISE-WEB-RESEARCH-V1.md 'Stage 1 status: `CLOSED / PASS`' 'Web Research Stage 1 is closed'
require_text docs/ENTERPRISE-WEB-RESEARCH-V1.md 'Stage 2 status: `CLOSED / PASS`' 'Web Research Stage 2 is closed'
require_file scripts/test_phase5e_product_visual.py
require_file scripts/phase5e_product_visual_check.py
require_text docs/PHASE5E-ARMOR-PRODUCT-VISUAL-MIGRATION.md 'Phase 5E: PASS' 'Phase 5E migration record is closed'
require_file docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md
require_file docs/POST-V1.0-BACKLOG.md
require_file docs/inventory/legacy-operations-skills-triage.csv
require_text README.md 'Enterprise Operations Capability Baseline v1.0' 'README links the frozen Operations baseline'
require_text docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md 'Enterprise Operations Capability Baseline v1.0: FROZEN' 'Final Operations baseline is frozen'
require_text docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md 'Hermes Skills Migration v1.0: CLOSED' 'Hermes Skills Migration v1.0 is closed'
require_text docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md 'Multi-Agent Orchestration: EXPERIMENTAL_HOLD' 'Final acceptance preserves Agent Delegate hold'
require_text docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md 'Operations Hermes Memory: OFF' 'Final acceptance preserves Operations Memory OFF'
require_text docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md 'save_product_visual_package' 'Final acceptance records Product Visual Router save'
if grep -F 'KEEP_MIGRATE' "$ROOT/docs/inventory/legacy-operations-skills-triage.csv" >/dev/null 2>&1; then
  fail 'Final migration ledger has no KEEP_MIGRATE rows' 'unresolved v1.0 migration rows remain'
else
  pass 'Final migration ledger has no KEEP_MIGRATE rows'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/.symlink_manifest 'armor-product-visual -> /Users/armor/Enterprise-AI-Office/skills/shared/department/armor-product-visual' 'Profile manifest exposes Product Visual canonically'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-skills.csv 'armor-product-visual,PRIVILEGED_OR_EXTERNAL' 'Profile enables the canonical Product Visual entrypoint'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-tools.csv 'save_product_visual_package' 'Profile enables the scoped Product Visual save tool'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/config.yaml 'save_product_visual_package' 'Live Profile binds the scoped Product Visual save tool'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/config.yaml 'image_gen' 'Operations keeps image generation explicitly disabled'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/config.yaml 'delegation' 'Operations keeps delegation explicitly disabled'
fi
require_text skills/shared/department/armor-mic-product-optimization/SKILL.md 'mic-product-edit-context/v1' 'MIC Skill honors current edit-page extraction'
require_text skills/shared/department/armor-mic-product-optimization/SKILL.md 'BLOCKED_SOURCE' 'MIC Skill fails closed when Standard is unavailable'
require_text skills/shared/department/armor-mic-product-optimization/SKILL.md 'MIC_AUTHORITY_REVIEW_REQUIRED' 'MIC Skill has authority review gate'
require_text skills/shared/department/armor-mic-product-optimization/SKILL.md 'Exact technical values must ultimately resolve' 'MIC adapter preserves technical fact safety'
require_text skills/shared/department/armor-mic-product-optimization/SKILL.md 'save_mic_product_package' 'MIC adapter binds scoped save'
require_absent skills/shared/department/mic-product-fill 'No duplicate shared MIC fill Skill is active'
require_absent skills/shared/department/mic-product-audit 'No duplicate shared MIC audit Skill is active'
require_absent skills/shared/department/mic-product-detail-page 'No duplicate shared MIC detail Skill is active'
require_text docs/PHASE4C-ARMOR-RUNTIME-CLOSURE.md 'ARMOR_ARCH_ROOT' 'Phase 4C Router closure is documented'
require_text skills/shared/department/armor-social-media-pipeline/SKILL.md '02-Projects/Workspaces/Marketing/Social-Media/' 'Social Skill declares lifecycle-neutral Router target'
require_text skills/shared/department/armor-social-media-pipeline/SKILL.md 'save_social_package' 'Social Skill declares scoped save boundary'
require_text skills/shared/department/armor-social-media-pipeline/SKILL.md 'ai-writing-audit' 'Social Skill reuses the canonical audit'
require_text skills/shared/department/armor-video-content-rules/SKILL.md 'transcript' 'Video rules preserve transcript-first handling'
require_absent skills/shared/department/armor-social-media-workflow 'No competing Social workflow Skill is active'
require_text docs/PHASE5A-ARMOR-SOCIAL-MEDIA-MIGRATION.md 'authority: CANONICAL' 'Phase 5A records canonical Social authority'
require_text docs/PHASE5A-ARMOR-SOCIAL-MEDIA-MIGRATION.md 'save_social_package' 'Phase 5A documents the scoped Social save'
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/.symlink_manifest 'armor-social-media-pipeline -> /Users/armor/Enterprise-AI-Office/skills/shared/department/armor-social-media-pipeline' 'Profile manifest exposes Social canonically'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-skills.csv 'armor-social-media-pipeline,PRIVILEGED_OR_EXTERNAL' 'Profile enables the canonical Social entrypoint'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-tools.csv 'save_social_package' 'Profile enables the scoped Social save tool'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/config.yaml 'save_social_package' 'Live Profile binds the scoped Social save tool'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/.symlink_manifest 'armor-mic-product-optimization -> /Users/armor/Enterprise-AI-Office/skills/shared/department/armor-mic-product-optimization' 'Profile manifest exposes MIC canonically'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-skills.csv 'armor-mic-product-optimization,PRIVILEGED_OR_EXTERNAL' 'Profile enables the canonical MIC entrypoint'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-tools.csv 'save_mic_product_package' 'Profile enables the scoped MIC save tool'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/config.yaml 'save_mic_product_package' 'Live Profile binds the scoped MIC save tool'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/.symlink_manifest 'armor-website-product-materials -> /Users/armor/Enterprise-AI-Office/skills/shared/department/armor-website-product-materials' 'Profile manifest exposes Product Materials canonically'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-skills.csv 'armor-website-product-materials,PRIVILEGED_OR_EXTERNAL' 'Profile enables the canonical Product Materials entrypoint'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-tools.csv 'save_website_product_materials_package' 'Profile enables the scoped Product Materials save tool'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/config.yaml 'save_website_product_materials_package' 'Live Profile binds the scoped Product Materials save tool'
fi
require_text docs/PHASE5B-ARMOR-MIC-PRODUCT-OPTIMIZATION-MIGRATION.md 'MIC authority: CANONICAL' 'Phase 5B records canonical MIC authority'
require_text docs/PHASE5B-ARMOR-MIC-PRODUCT-OPTIMIZATION-MIGRATION.md 'Automatic MIC editing enabled: NO' 'Phase 5B records no automatic MIC editing'
require_text scripts/test_phase5b_mic.py 'publication_performed: false' 'MIC acceptance fixture forbids publication'
require_text docs/PHASE5B.2-MIC-SKILL-VAULT-AUTHORITY-DEDUPLICATION.md 'CANONICAL' 'Phase 5B.2 records canonical Vault ownership'
require_text docs/PHASE5B.2-MIC-SKILL-VAULT-AUTHORITY-DEDUPLICATION.md 'EXECUTION_ADAPTER' 'Phase 5B.2 records Skill adapter ownership'
require_text skills/shared/department/armor-mic-product-optimization/SKILL.md 'ARMOR-MIC-Product-Optimization-Standard-v1.0.md' 'MIC Skill references the canonical Vault Standard'
require_text skills/shared/department/armor-mic-product-optimization/SKILL.md 'Never silently fall back to an embedded duplicate rule set' 'MIC Skill has no detailed SOP fallback copy'
require_text scripts/test_phase5b1_mic_authority.py 'conflicting Datasheet value' 'MIC authority regression covers conflicting technical values'
require_text scripts/test_phase5b2_mic_authority_dedup.py 'not_embedded_sop' 'MIC de-duplication regression covers the thin adapter role'
require_text scripts/phase5a_social_runtime_check.py 'publication_performed: false' 'Social acceptance fixture forbids publication'
require_text config/mcp-registry.yaml 'employee_exposure_default: disabled' 'Phase 4A registry defaults employee exposure off'
require_text config/mcp-registry.yaml 'operations_allowlist:' 'Phase 4A registry declares Operations allowlist'
require_text docs/MCP-CONTROL-PLANE.md 'The machine-readable authority is' 'Current MCP control-plane interpretation exists'
require_text docs/PHASE4A-ARMOR-MIGRATION.md 'one Codex Final Editorial Pass' 'Phase 4A Article lifecycle is documented'
require_text skills/shared/department/armor-website-article-pipeline/SKILL.md '02-Projects/Workspaces/Website/Articles/' 'Article Skill declares Router source target'
require_text skills/shared/department/armor-website-article-pipeline/SKILL.md 'ai-writing-audit v0.3.1' 'Article Skill pins audit version'
require_file scripts/phase4b_runtime_check.py
require_file scripts/test_phase4b_runtime_check.py
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/.symlink_manifest 'ai-writing-audit -> /Users/armor/Enterprise-AI-Office/skills/shared/department/ai-writing-audit' 'Profile manifest exposes ai-writing-audit canonically'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/.symlink_manifest 'armor-website-article-pipeline -> /Users/armor/Enterprise-AI-Office/skills/shared/department/armor-website-article-pipeline' 'Profile manifest exposes Article canonically'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-skills.csv 'ai-writing-audit,SAFE_BASELINE' 'Profile enables the audit dependency'
fi
if [ "$REPOSITORY_ONLY" != "1" ]; then
  require_text private/department-profile/enabled-skills.csv 'armor-website-article-pipeline,PRIVILEGED_OR_EXTERNAL' 'Profile enables the canonical Article entrypoint'
fi
require_text docs/PHASE4B-ARMOR-RUNTIME-CLOSURE.md 'SCOPED_ROUTER_WRITE_BLOCKED' 'Phase 4B records the scoped Router blocker'
require_text config/capabilities.yaml 'docs/V2-STAGE-CONTRACTS.md' 'Email capability has stage closure contract'
require_text config/capabilities.yaml 'docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md' 'Email capability has identity authorization contract'
require_text config/capabilities.yaml 'docs/V2-GOVERNANCE-RUNTIME.md' 'Email capability has governance runtime contract'
require_text config/capabilities.yaml 'docs/V2-SEND-RECONCILIATION.md' 'Email capability has send/reconciliation contract'
require_text config/capabilities.yaml 'docs/V2-RECOVERY-CLEAN-HOST.md' 'Email capability has recovery/clean-host contract'
require_text config/capabilities.yaml 'governance_runtime_contract:' 'Email capability declares governance runtime closure'
require_text config/capabilities.yaml 'send_reconciliation_contract:' 'Email capability declares send/reconciliation closure'
require_text config/capabilities.yaml 'recovery_clean_host_contract:' 'Email capability declares recovery/clean-host closure'
require_text config/capabilities.yaml 'infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md' 'Email capability has Open WebUI communication provisioning path'
require_text config/capabilities.yaml 'infrastructure/open-webui/v2_approve_draft_action.py' 'Email capability has deterministic approval Action template'
require_text config/capabilities.yaml 'infrastructure/email/governance/schema.sql' 'Email capability has governance SQLite schema'
require_text config/capabilities.yaml 'infrastructure/email/governance/migrations/002_send_reconciliation.sql' 'Email capability has send/reconciliation schema migration'
require_text config/capabilities.yaml 'infrastructure/email/governance/backup_state.py' 'Email capability has Governance backup helper'
require_text config/capabilities.yaml 'infrastructure/email/governance/restore_state.py' 'Email capability has Governance restore helper'
require_text config/capabilities.yaml 'infrastructure/email/governance/test_schema.py' 'Email capability has governance offline test'
require_text config/capabilities.yaml 'infrastructure/email/governance/test_send_reconciliation.py' 'Email capability has send/reconciliation offline test'
require_text config/capabilities.yaml 'infrastructure/email/governance/test_recovery.py' 'Email capability has recovery offline test'
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
require_text infrastructure/email/governance/test_recovery.py 'PASS — v2 governance backup/restore/recovery contract' 'Recovery offline test has deterministic PASS marker'
require_text infrastructure/email/governance/backup_state.py 'src.backup(dst)' 'Governance backup uses SQLite online backup API'
require_text infrastructure/email/governance/restore_state.py 'RECONCILIATION_REQUIRED' 'Governance restore preserves unresolved-send safety'
require_text scripts/backup.sh 'GOVERNANCE_BACKUP_HELPER' 'Full backup conditionally includes Governance snapshot'
require_text scripts/restore.sh 'GOVERNANCE_RESTORE_HELPER' 'Isolated restore conditionally materializes Governance state'
require_text scripts/health-check.sh 'EAIO_GOVERNANCE_HEALTH_URL' 'Health helper supports optional Governance service'
require_text state/DEPLOYMENT-STATE.template.md '## v2 Email Governance' 'Deployment state has v2 Email governance evidence section'
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
require_text infrastructure/weknora/PROVISIONING.md '### 3.1 Pinned API-route provenance' 'WeKnora provisioning records pinned API route provenance'
require_text infrastructure/weknora/PROVISIONING.md 'GET <BASE>/auth/config' 'WeKnora provisioning resolves auth policy before bootstrap'
require_text infrastructure/weknora/PROVISIONING.md 'POST <BASE>/auth/register' 'WeKnora provisioning supports policy-authorized fresh owner bootstrap'
require_text infrastructure/weknora/PROVISIONING.md 'do not flip the server to self_serve just for automation' 'WeKnora provisioning preserves deployed auth policy'
require_text infrastructure/weknora/PROVISIONING.md 'registration produces a tenantless identity' 'WeKnora provisioning fails closed on unresolved tenant authority'
require_text infrastructure/weknora/PROVISIONING.md 'DEPLOY.md §4.1' 'WeKnora provisioning requires acquisition before reconciliation'
require_text infrastructure/weknora/PROVISIONING.md 'DEPLOY.md §4.2' 'WeKnora provisioning requires runtime identity before reconciliation'
require_no_text infrastructure/weknora/PROVISIONING.md 'first validated core baseline' 'WeKnora provisioning does not retain stale baseline semantics'
require_text infrastructure/weknora/PROVISIONING.md '1edcd54b43606d9079bb36650efe3f68707a79ea' 'WeKnora provisioning provenance matches validated source commit'
require_text docs/UPGRADE.md 'internal/router/router.go' 'WeKnora upgrade requires route requalification'
require_text docs/UPGRADE.md 'routes_auth_tenant.go' 'WeKnora upgrade requires tenant/auth route requalification'
require_text infrastructure/weknora/PROVISIONING.md 'BLOCKED — MIGRATION REQUIRED' 'WeKnora contract blocks unsafe embedding drift'
require_text infrastructure/hermes/features/MESSAGING.md 'hermes gateway setup' 'Messaging contract uses native Hermes setup'
require_text infrastructure/hermes/features/EMPLOYEE-MEMORY.md 'BLOCKED — REQUIRED INPUT' 'Employee memory gate fails closed without isolation'
require_text config/capabilities.yaml 'technical-profile.config.example.yaml' 'Coding capability has executable Profile template'
require_text README.md 'CONFIGURED READY' 'README explains configured completeness'

if [ "$REPOSITORY_ONLY" != "1" ]; then
  phase4a_python=python3
  if [ "$phase4a_python" = python3 ] && [ -x /Users/armor/.hermes/hermes-agent/venv/bin/python ]; then
    phase4a_python=/Users/armor/.hermes/hermes-agent/venv/bin/python
  fi

  if "$phase4a_python" "$ROOT/scripts/phase4a_migration_check.py"; then
    pass 'Phase 4A Article/MCP migration contract'
  else
    fail 'Phase 4A Article/MCP migration contract' 'offline migration checker failed'
  fi
else
  printf '%s\n' 'Repository-only mode: private deployment/profile checks skipped by design.'
fi

printf '%s\n' '----------------------------------------'
printf 'Summary: %s PASS, %s FAIL\n' "$PASS" "$FAIL"
printf '%s\n' 'Static PASS means blueprint and deployment contracts are present; it does not advance blueprint phase, activate a real deployment, or replace target runtime acceptance.'

if [ "$FAIL" -gt 0 ]; then
  exit 2
fi

exit 0
