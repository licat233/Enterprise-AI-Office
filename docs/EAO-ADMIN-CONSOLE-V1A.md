# EAO Administrator Console v1A

Status: REVIEW PLANE ACCEPTED / KNOWLEDGE MUTATION BLOCKED / DISABLED

This contract defines the smallest governed administrator entry point for
Enterprise AI Office. It composes existing Open WebUI, Hermes, WeKnora,
ToolScout, MCP control-plane, Git/PR, and review patterns. It does not create
a separate admin platform.

Production closure: `EAO Administrators → EAO Admin → maintainer` is the
accepted administrator-only review/governance plane. Knowledge Mutation
through EAO Admin is `BLOCKED / DISABLED` because replay/audit durability was
not accepted on the current Open WebUI v0.11.3 + WeKnora v0.8.0 stack. The
approval Action and operation-envelope code remain reference artifacts only;
they are not required or accepted for production mutation.

## 1. Authority and phase

The repository's current authority remains:

- AGENTS.md;
- state/PROJECT-PHASE.yaml;
- the current deployment/configuration standards;
- the current capability registry and acceptance suite.

Current main includes the README/AGENTS/REPRODUCE/VALIDATE/eao-manifest authority
chain plus the current lifecycle and deployment/reference-status contracts. This
capability uses those current authorities and does not invent a second one.

This is repository capability work in the current release_ready phase. It does
not declare final RELEASE READY, authorize validation on a target, activate
real_deployment_task, or authorize a live Mac Studio mutation.

## 2. Capability request and reuse pass

### Requested outcome

An authorized EAO administrator can submit a URL, Git repository, PDF, DOCX,
text, Skill package, Tool reference, or MCP/backend reference and receive a
governed review/recommendation. Knowledge candidates receive classification,
provenance, duplicate/conflict, metadata, and read-only retrieval review;
Knowledge Mutation through EAO Admin is blocked. Skill, Tool, and MCP changes remain
repository proposals through the external short-lived branch and PR workflow;
the EAO runtime repository path is currently blocked because no approved typed
repository capability is selected.

### Existing capabilities inspected

| Existing capability | Reuse decision | Boundary |
| --- | --- | --- |
| Open WebUI | REUSE_EXISTING | human identity, group/resource ACL, conversational surface, native confirmation UI |
| Hermes Profiles/Skills | REUSE_EXISTING | maintainer role, shared intake Skill, Profile-scoped tools |
| WeKnora | REUSE_EXISTING | Company Knowledge authority, read-only retrieval and review evidence |
| ToolScout | REUSE_EXISTING | first review for installed/commodity tools |
| MCP/control-plane registry | REUSE_EXISTING | typed capability registration and Profile exposure binding |
| Git + repository workflow | REUSE_EXISTING as authority | canonical Skill/Tool/config source, branches, PRs, CI; no selected typed EAO runtime binding |
| Existing HumanActor/email approval pattern | REUSE_EXISTING as reference | future mutation review only; not accepted as current durable mutation control |
| New admin portal/service/database | REJECT | no verified gap and explicitly disallowed by the v1A scope |

### Verified gap

The repository has employee and control-plane building blocks, but no
dedicated administrator-only conversational Profile, intake Skill, group-bound
Assistant contract, or non-email generic operation-envelope primitive.

### Smallest additions

- the maintainer Profile template plus least-privilege Hermes routing overlay;
- the shared eao-resource-intake Skill;
- the EAO Admin Open WebUI provisioning contract;
- the disabled/reference-only Open WebUI Knowledge Approval Action;
- a side-effect-free operation-envelope/hash helper and offline tests;
- explicit reuse of Enterprise Web Research for source inspection and ToolScout for tool review;
- capability/configuration/acceptance/readiness wiring.

No database, workflow engine, scheduler, vector store, IAM layer, admin portal,
generic runtime reconciler, or replacement knowledge authority is added.

## 3. v1A scope

v1A provides:

- a dedicated Hermes maintainer Profile displayed as EAO Admin;
- an EAO Administrators Open WebUI group and private Assistant resource;
- repository authority and CI/readiness evidence may be reviewed through the
  external repository workflow; the EAO runtime has no repository read/search
  binding;
- first-step classification into Knowledge, Skill, Tool, MCP/External Backend,
  or Unsupported/Ignore;
- Capability Reuse Pass integration;
- bounded Knowledge review, recommendation, metadata preparation, and read-only WeKnora verification;
- actual-source Skill review and recommendation;
- ToolScout-first Tool review and recommendation through the maintainer review-only subset;
- public URL/GitHub source inspection through Enterprise Web Research web_search/web_fetch only;
- uploaded file review through Open WebUI transient attachment/context handling without generic filesystem access;
- narrow MCP/backend review without automatic exposure;
- bounded server-side Knowledge approval/ingestion using Open WebUI authenticated context + HMAC + WeKnora scoped contributor API;
- repository branch/PR preparation is
  BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED in v1A and is not in the
  runtime operation set;
- deterministic, server-side HumanActor approval for material mutations;
- repository/offline acceptance and readiness evidence.

v1A explicitly does not include generic runtime mutation. It does not expose
arbitrary shell, terminal, filesystem, Docker, package-manager, browser,
computer-use, SSH, sudo/root, raw secret, profile-switch, generic GitHub admin,
destructive deletion, or EAO Runtime Reconciler actions.

## 4. Maintainer Profile contract

| Field | v1A contract |
| --- | --- |
| Canonical name | maintainer |
| Display name | EAO Admin |
| Human access | authorized EAO Administrators users/groups only |
| Memory | OFF |
| Cron / Kanban / Messaging Gateway | OFF |
| Generic terminal/filesystem/browser | DENY |
| Docker / SSH / sudo/root | DENY |
| default/admin switching | DENY |
| Raw secrets | DENY |
| Knowledge | read-only WeKnora retrieval in Hermes; no EAO Admin contributor write path |
| Source inspection | Enterprise Web Research web_search + web_fetch only; no raw browser/provider surface |
| Tool review | ToolScout review-only subset; no maintainer ToolScout memory-write tools |
| Repository | runtime repository operations blocked until an approved typed capability is selected |
| Allowed work | classify, review, inspect, and recommend; material operation fields are re-derived server-side |
| Material mutation | BLOCKED / DISABLED through EAO Admin; no accepted production mutation path |

Profile isolation is not host sandboxing. The runtime must enforce the tool
boundary in Hermes/Open WebUI/control-plane configuration, not only in SOUL
text.

## 5. Open WebUI authorization

When the capability is enabled by company configuration:

    EAO Administrators
      → read/use
      → EAO Admin Assistant
      → Hermes maintainer route

No grant is made to All-Employees, Operations Employees, ordinary
Sales/Procurement groups, or unrelated employee groups. The privileged Hermes
default/admin route is not the EAO Admin route.

Acceptance must prove both UI and backend behavior:

| Principal | Expected result |
| --- | --- |
| authorized EAO administrator | sees and uses EAO Admin |
| ordinary General employee | cannot see or invoke EAO Admin |
| Operations employee | cannot see or invoke EAO Admin |
| direct unauthorized Assistant/model request | fail closed |
| maintainer attempt to reach default/admin | deny |
| missing/forged HumanActor context | deny |

UI hiding is not a security boundary.

## 6. Intake workflow

Every resource follows:

    submit
    → classify, read-only
    → Capability Reuse Pass
    → current authority review
    → source/provenance/license/security/dependency review
    → proposed action + risk/impact
    → exact review/recommendation result
    → read-only verification
    → acceptance evidence

Classification itself cannot create or modify a Knowledge document, Skill, Tool,
MCP registration, Profile, branch, PR, or runtime state.

### Knowledge

Use WeKnora for read-only Company Knowledge review and retrieval verification.
The accepted path is:

    source review
    → classification and provenance
    → duplicate/supersession/conflict check
    → exact metadata/recommendation preparation
    → read-only retrieval verification
    → review result

Distinguish Company Authoritative and External Reference, preserve source
identity/fingerprint/version/owner/effective-date/status/confidentiality, and
surface conflicts rather than silently reconciling them. Do not report new
Knowledge as ACTIVE through EAO Admin.

Knowledge Mutation through EAO Admin is explicitly:

    BLOCKED / DISABLED
    BLOCKED — REPLAY/AUDIT DURABILITY NOT ACCEPTED ON CURRENT STACK

The v0.8.0 scoped contributor routes and the Open WebUI Action remain
reference-only material for a future separately approved replacement path.
Do not invoke them, shorten operation markers, enable audit, add a ledger or
database, patch Open WebUI/WeKnora, or substitute filesystem/Vault state.

### Skill

Inspect actual source, including SKILL.md, references, scripts, templates,
dependencies, environment variables, network/filesystem/process behavior,
credentials, license, upstream source, and pinned version/commit. Check
overlap and return only:

    REUSE_EXISTING | EXTEND_EXISTING | NEW_CAPABILITY | REJECT

A new or adapted Skill is canonical only after review, a short-lived branch,
PR, Repository Readiness PASS, human review/merge, and later runtime
reconciliation.

### Tool and MCP/backend

Tool review is ToolScout-first. Classify the result as Local Utility, Agent
Tool/MCP, External Backend, or Development Tool. Select an approved logical
Tool ID rather than accepting model-controlled install commands. Do not
automatically turn a Tool into MCP. A justified MCP/backend receives only the
required typed operations, narrow credentials, intended Profile bindings, and
positive/negative access tests through the existing control plane.

## 7. Operation Envelope (reference-only; mutation blocked)

Every material operation has:

- operation_id;
- operation type;
- exact source identity and source fingerprint;
- target;
- material change summary;
- security impact;
- Profile-exposure impact;
- runtime impact;
- expected current state;
- immutable plan hash;
- trusted server-side HMAC plan signature;
- creation and expiry timestamps.

The default approval TTL is 30 minutes and is enforced as a maximum. A future
company configuration may explicitly select a lower TTL only within the bounded
1–30 minute range. The trusted HMAC signature binds the canonical plan and its
plan hash using a protected server-side key; the signature and key are not
model/browser-visible normal fields. Material changes invalidate the plan,
including source/version/commit, dependencies, PR HEAD or CI state, Tool
recipe, credential/security scope, Profile exposure, target, or expected state.

The model cannot provide or forge:

- HumanActor identity;
- group membership;
- approval state;
- plan hash;
- expiry;
- current-state evidence.

The trusted Action and envelope described here are retained as reference-only
artifacts. Their Open WebUI message/meta replay evidence did not survive the
healthy post-Action lifecycle, the WeKnora-native candidate exceeded the
deployed 50-character channel limit, and native Open WebUI audit was disabled.
Therefore no production mutation, approval, replay marker, or reconciliation
claim may be made from this section. Do not invoke the Action or retry an
unknown outcome; prepare exact metadata/state for a separately approved
external/manual path once one is defined.

## 8. Repository and runtime gates

Repository approval and runtime activation are separate:

    reviewed resource
    → short-lived branch
    → PR
    → Repository Readiness PASS
    → review/merge to main
    → separately authorized runtime reconciliation
    → target acceptance

The real target must be explicitly authorized after re-reading
state/PROJECT-PHASE.yaml. A repository implementation does not authorize
Mac Studio runtime mutation. The v1A repository path is explicitly
BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED; do not substitute shell,
GitHub administration, or an arbitrary HTTP client. v1A stops before generic
runtime reconciliation;
v1B may add a narrow typed reconciler only after v1A acceptance is PASS.

## 9. Rollback and frozen baseline

Rollback is capability-specific:

- Knowledge: status/version replacement or supersession;
- Skill: remove Profile exposure, reconcile, and validate;
- Tool/MCP: disable dependent capability first, then use an approved recipe;
- repository: revert through Git history/PR.

No generic reverse-shell-command rollback exists. general, Operations,
employee RBAC, the frozen v1/v2 baselines, and default/admin control-plane
separation remain unchanged. Reusing Enterprise Web Research for maintainer
does not expose raw Firecrawl/Obscura/CloakBrowser tools; reusing ToolScout does
not expose its memory-write tools to maintainer.

## 10. Evidence and status

The deployment record must contain only non-secret evidence:

- Profile/Assistant/group mappings;
- Knowledge target and ingestion/retrieval evidence;
- review/reuse decisions;
- source/version/license/dependency findings;
- ToolScout result;
- repository branch/PR/CI/readiness state from the external workflow, plus the
  unresolved typed-repository blocker;
- operation IDs, plan hashes, trusted-binding verification, approval outcome,
  TTL/invalidation result;
- runtime result when a separately authorized target exists.

Repository/offline PASS is not runtime acceptance. Without an authorized target
and protected private configuration, report BLOCKED — REQUIRED INPUT or
repository/design implementation only; never claim EAO Admin deployed.

## 11. v1B boundary

Only after v1A acceptance is fully PASS may a separately approved typed
reconciler consume canonical approved repository state. Its operations may be
apply_skill, disable_skill, install_tool, reconcile_profile, reconcile_mcp,
and run_acceptance with typed IDs only. It must never accept a raw shell
command, arbitrary path, Docker command, or package-manager command.
v1B is not implemented by this document.
