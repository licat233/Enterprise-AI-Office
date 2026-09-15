# EAO Administrator Console v1A Acceptance

This is the conditional acceptance contract for the accepted administrator
review plane when `capabilities.eao_administrator_console.enabled: true`.
It applies only on an explicitly authorized validation target. Offline tests
prove only the repository contract. Knowledge Mutation through EAO Admin is
not part of the accepted baseline and remains `BLOCKED / DISABLED`.

Production blocker: `BLOCKED — REPLAY/AUDIT DURABILITY NOT ACCEPTED ON CURRENT
STACK`. Open WebUI v0.11.3 message/meta durability and the current WeKnora
v0.8.0 native candidate did not qualify durable replay reconciliation, and
Open WebUI native audit is disabled. Do not redesign or enable those paths in
this acceptance.

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

    [ ] maintainer Enterprise Web Research surface exposes exactly web_search + web_fetch for source inspection
    [ ] maintainer ToolScout surface exposes exactly advise_tool_use/query_registry/detect_candidates/check_conflicts/doctor
    [ ] maintainer does not receive ToolScout record_memory or recall_memory
    [ ] raw Firecrawl/Obscura/CloakBrowser/browser tools remain unavailable to maintainer
    [ ] URL classifies as Knowledge/Skill/Tool/MCP/Unsupported correctly
    [ ] Git repository classifies without mutation
    [ ] PDF/DOCX/text classifies without mutation
    [ ] Skill package classifies without mutation
    [ ] Tool/backend reference classifies without mutation
    [ ] classification does not change WeKnora, Git, Open WebUI, Hermes, or runtime state
    [ ] Capability Reuse Pass records inspected capabilities and exact gap

## Knowledge review (mutation blocked)

The accepted v1A Knowledge scope is classification, provenance, confidentiality,
duplicate/supersession/conflict review, exact metadata/recommendation
preparation, and read-only WeKnora retrieval/verification. It does not include
Knowledge Mutation through EAO Admin.

    [ ] Company Authoritative vs External Reference is explicit
    [ ] duplicate/version/supersession check passes
    [ ] authoritative conflict is surfaced and remains inactive
    [ ] exact metadata/source fingerprint is preserved
    [N/A] Open WebUI approval Action and server-side HumanActor binding are reference-only; not accepted mutation authority
    [N/A] contributor credential and WeKnora write routes are retired/disabled for EAO Admin
    [ ] existing Company Knowledge can be read through the bounded WeKnora retrieval path
    [ ] read-only WeKnora retrieval can GET /api/v1/knowledge/:id and inspect parse_status
    [ ] out-of-scope Knowledge Base access is denied
    [ ] Knowledge Base lifecycle/admin operations remain denied
    [ ] owner/admin credentials, tenant/system admin, MCP admin, and direct database access remain unavailable
    [N/A] bounded WeKnora contributor operation, ingestion, parsing, and indexing are blocked
    [ ] representative fact is retrievable directly
    [ ] source evidence is correct
    [ ] normal Hermes retrieval returns the same evidence for existing Company Knowledge
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

## Deterministic approval and replay (reference-only / not accepted)

    [ ] model-generated actor/group/approval/hash values have no authority
    [N/A] trusted Open WebUI server-side HumanActor mutation binding is not accepted on the current stack
    [ ] exact operation fields are shown before approval
    [ ] approval TTL is bounded (default and maximum 30 minutes)
    [ ] canonical plan is bound to a protected server-side HMAC signature
    [ ] protected signing-key reference is resolved server-side and the key value is absent from model/browser-visible payloads
    [ ] missing, invalid, or wrong-key signature is denied
    [ ] expired approval is denied
    [ ] changed plan/current state/target is denied
    [ ] source edit/replacement between confirmation display and commit is denied
    [ ] removed EAO Administrators membership between display and commit is denied
    [ ] unauthorized human is denied
    [ ] Cancel creates no effect
    [N/A] sanitized OUTCOME_UNKNOWN replay marker is not accepted as durable production evidence
    [ ] replay metadata contains no contributor key, HMAC key, or trusted signature
    [N/A] repeated completed operation_id reconciliation is not qualified
    [ ] OUTCOME_UNKNOWN with a known knowledge_id reconciles through GET /api/v1/knowledge/:id
    [N/A] OUTCOME_UNKNOWN reconciliation is not qualified and must not be retried
    [ ] unknown outcome is not blindly retried

## Frozen baseline and runtime gate

    [ ] Operations remains unchanged
    [ ] general employee RBAC remains unchanged

Baseline assertion: Operations and General employee RBAC are unchanged.
    [ ] default/admin remains control-plane only
    [ ] Cron/Kanban/Messaging remain OFF for maintainer v1A
    [ ] maintainer WeKnora contributor credential is absent from Hermes Profile/MCP environment
    [ ] EAO Admin contributor credential is absent from maintainer and retired/disabled in the runtime
    [ ] no EAO Runtime Reconciler exists in v1A
    [ ] repository/offline PASS is not reported as runtime deployment
    [ ] state records exact evidence, including review-plane PASS and mutation BLOCKED / DISABLED

## Result

Record:

    PASS — EAO ADMIN CONSOLE V1A REVIEW PLANE; KNOWLEDGE MUTATION BLOCKED / DISABLED

only when all enabled-target tests pass. Otherwise report the specific failed
boundary, or BLOCKED — REQUIRED INPUT: <specific item> when protected external
authority is missing.
