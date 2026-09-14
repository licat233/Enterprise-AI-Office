# EAO Administrator Console v1A Acceptance

This is the conditional acceptance contract for
capabilities.eao_administrator_console.enabled: true. It applies only on an
explicitly authorized validation/deployment target. Offline tests prove only
the repository contract.

## Preconditions

    [ ] active private company configuration selects the capability
    [ ] target readiness and target host are explicit
    [ ] protected Hermes/Open WebUI/WeKnora bindings are resolved
    [ ] no real secret is printed, committed, or included in model context
    [ ] v1/v2 frozen baseline is preserved

## RBAC and Profile boundary

    [ ] authorized EAO administrator sees and uses EAO Admin
    [ ] ordinary General employee cannot see or invoke EAO Admin
    [ ] Operations employee cannot see or invoke EAO Admin
    [ ] ordinary Sales/Procurement/unrelated groups cannot invoke it
    [ ] direct unauthorized Open WebUI resource/model access fails closed
    [ ] direct unauthorized maintainer route access fails closed
    [ ] maintainer cannot reach Hermes default/admin
    [ ] maintainer cannot switch Profile
    [ ] maintainer has no generic shell/terminal
    [ ] maintainer has no unrestricted filesystem
    [ ] maintainer has no Docker, SSH, sudo/root, or generic browser
    [ ] raw secrets are absent from tools, output, logs, and Git

## Resource intake

    [ ] URL classifies as Knowledge/Skill/Tool/MCP/Unsupported correctly
    [ ] Git repository classifies without mutation
    [ ] PDF/DOCX/text classifies without mutation
    [ ] Skill package classifies without mutation
    [ ] Tool/backend reference classifies without mutation
    [ ] classification does not change WeKnora, Git, Open WebUI, Hermes, or runtime state
    [ ] Capability Reuse Pass records inspected capabilities and exact gap

## Knowledge intake

    [ ] Company Authoritative vs External Reference is explicit
    [ ] duplicate/version/supersession check passes
    [ ] authoritative conflict is surfaced and remains inactive
    [ ] exact metadata/source fingerprint is preserved
    [ ] trusted approval binds to the exact immutable operation plan and server-side HMAC signature
    [ ] WeKnora contributor credential is an official v0.8.0 scoped key with full_access=false, exactly ingest + retrieve, and an explicit non-empty knowledge_base_ids allow-list
    [ ] scoped contributor key ingests into the allowed Knowledge Base
    [ ] scoped contributor key can GET /api/v1/knowledge/:id for knowledge in the allowed Knowledge Base
    [ ] scoped contributor key can inspect parse_status through GET /api/v1/knowledge/:id
    [ ] out-of-scope Knowledge Base access is denied
    [ ] Knowledge Base lifecycle/admin operations remain denied
    [ ] owner/admin credentials, tenant/system admin, MCP admin, and direct database access remain unavailable
    [ ] bounded WeKnora contributor operation succeeds
    [ ] ingestion completes
    [ ] parsing completes
    [ ] indexing completes
    [ ] representative fact is retrievable directly
    [ ] source evidence is correct
    [ ] normal Hermes retrieval returns the same evidence
    [ ] failed parse/index remains inactive
    [ ] unknown information is not invented

## Skill and Tool review

    [ ] Skill Capability Reuse Pass runs
    [ ] actual Skill source and referenced files are inspected
    [ ] dependency/network/filesystem/process/credential/license review is recorded
    [ ] unsafe user-controlled shell/code/path/admin behavior is rejected
    [ ] recommendation is one of REUSE_EXISTING/EXTEND_EXISTING/NEW_CAPABILITY/REJECT
    [ ] ToolScout review occurs before Tool installation/reimplementation
    [ ] Tool is classified Local Utility/Agent Tool or MCP/External Backend/Development Tool
    [ ] no automatic Tool-to-MCP conversion occurs
    [ ] MCP operations are narrow and Profile-bound when justified
    [ ] v1A MCP/backend review is review-only; no registration/exposure/install mutation binding is implied
    [ ] positive and negative Profile access tests pass

## Repository workflow

    [ ] material change starts from current main
    [ ] short-lived task branch is used
    [ ] capability request and repository records reuse/gap/security/rollback impact
    [ ] no direct material push to main
    [ ] external repository workflow remains the authority for PR/HEAD/CI/Readiness
    [ ] EAO runtime does not claim repository PR preparation is deployable
    [ ] runtime reconciliation is a separate gate

Repository runtime path status:

    BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED

A future typed repository binding must independently prove reviewed-HEAD
binding, changed-HEAD invalidation, negative access tests, Repository Readiness,
and human review before it can enter the v1A runtime operation set.

## Deterministic approval and replay

    [ ] model-generated actor/group/approval/hash values have no authority
    [ ] trusted Open WebUI server-side HumanActor is resolved
    [ ] exact operation fields are shown before approval
    [ ] approval TTL is bounded (default and maximum 30 minutes)
    [ ] canonical plan is bound to a protected server-side HMAC signature
    [ ] protected signing-key reference is resolved server-side and the key value is absent from model/browser-visible payloads
    [ ] missing, invalid, or wrong-key signature is denied
    [ ] expired approval is denied
    [ ] changed plan/current state/target is denied
    [ ] unauthorized human is denied
    [ ] Cancel creates no effect
    [ ] repeated completed operation_id returns existing/current result
    [ ] OUTCOME_UNKNOWN becomes RECONCILIATION_REQUIRED
    [ ] unknown outcome is not blindly retried

## Frozen baseline and runtime gate

    [ ] Operations remains unchanged
    [ ] general employee RBAC remains unchanged

Baseline assertion: Operations and General employee RBAC are unchanged.
    [ ] default/admin remains control-plane only
    [ ] Cron/Kanban/Messaging remain OFF for maintainer v1A
    [ ] no EAO Runtime Reconciler exists in v1A
    [ ] repository/offline PASS is not reported as runtime deployment
    [ ] state records exact evidence or BLOCKED — REQUIRED INPUT

## Result

Record:

    PASS — EAO ADMIN CONSOLE V1A

only when all enabled-target tests pass. Otherwise report the specific failed
boundary, or BLOCKED — REQUIRED INPUT: <specific item> when protected external
authority is missing.
