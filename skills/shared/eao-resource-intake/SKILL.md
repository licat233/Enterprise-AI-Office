# EAO Resource Intake

Status: company-owned shared Skill artifact for the `maintainer` Profile.

## Role

Provide the governed, read-first orchestration for EAO administrator resource intake. This Skill is policy and workflow guidance; it is not a shell wrapper, package manager, approval database, or runtime reconciler.

## Prerequisites

- authenticated Open WebUI user in the configured `EAO Administrators` group;
- the `maintainer` Profile and private `EAO Admin` Assistant;
- current repository authority and capability registry;
- supported read-only WeKnora retrieval path for review/verification;
- bounded Enterprise Web Research source-inspection path (web_search + web_fetch only);
- existing MCP/control-plane registry for review-only MCP/backend assessment;
- ToolScout-first review path for proposed Tools or commodity utilities;
- protected non-secret runtime state recording that Knowledge Mutation through EAO Admin is disabled.

If a prerequisite is missing, stop with `BLOCKED — REQUIRED INPUT` or `BLOCKED — TYPED CAPABILITY NOT AVAILABLE`. Do not substitute generic shell, direct database writes, or an unapproved HTTP client.

## Intake Contract

For each URL, Git repository, PDF, DOCX, text, Skill package, Tool homepage/repository, or MCP/backend reference:

```text
receive
→ classify (read-only)
→ Capability Reuse Pass
→ current-authority review
→ source/security/provenance review
→ proposed action + risk/impact summary
→ exact metadata/state recommendation
→ read-only verification evidence
→ acceptance evidence
```

Classification must produce exactly one primary class:

| Class | Initial authority | v1A disposition |
| --- | --- | --- |
| Knowledge | WeKnora + source provenance | review/recommendation and read-only verification; mutation blocked |
| Skill | Git + actual source/license/dependency review | recommendation; external repository PR workflow only |
| Tool | ToolScout-first + official source | recommendation; external repository PR workflow only |
| MCP / External Backend | official API/MCP + MCP control plane | narrow registration proposal; no automatic exposure |
| Unsupported / Ignore | current repository policy | no mutation |

## Capability Reuse Pass

Record:

1. the requested business outcome;
2. existing EAO/upstream capabilities inspected;
3. exact overlap and reuse decision;
4. the smallest verified gap;
5. architecture, security, maintenance, rollback, and frozen-baseline impact.

Use one of `REUSE_EXISTING`, `EXTEND_EXISTING`, `NEW_CAPABILITY`, or `REJECT`. “Useful” is not a sufficient reason to install a new Skill or Tool.

Expected reuse order:

```text
Open WebUI → Hermes Profiles/Skills → WeKnora → ToolScout → MCP control plane → Git/PR workflow → existing approval/security patterns
```

Do not add a new service, database, scheduler, vector store, IAM layer, or admin portal without repository evidence of a real gap and an explicit architecture decision.

## Knowledge Path

For a Knowledge candidate:

1. identify the source and calculate a stable source fingerprint;
2. label it `Company Authoritative` or `External Reference`;
3. review confidentiality, owner, version, effective date, status, and license/provenance;
4. check duplicate, supersession, and authoritative conflict state;
5. prepare metadata for the configured `Company Knowledge` Base;
6. prepare the exact metadata/state recommendation from the current review context;
7. show the source fingerprint, target recommendation, risks, and evidence to the authenticated administrator;
8. perform read-only retrieval verification for existing Company Knowledge and record source evidence;
9. leave failed or conflicting material inactive and surface the conflict; do not mutate through EAO Admin.

The pinned WeKnora v0.8.0 contributor path and its write credential are
reference-only and retired/disabled for this baseline. Knowledge Mutation
through EAO Admin is `BLOCKED / DISABLED` with reason `BLOCKED — REPLAY/AUDIT
DURABILITY NOT ACCEPTED ON CURRENT STACK`. Prepare exact metadata/state for a
direct approved external/manual path once one is defined; do not invent one.

Knowledge ingestion does not authorize Knowledge Base deletion, embedding/reranker changes, bulk destructive deletion, or direct database writes.

## Skill Review Path

Inspect actual source before recommending anything:

- public URL/GitHub source inspection uses only the bounded Enterprise Web Research web_search/web_fetch surface;
- uploaded PDF/DOCX/text content is reviewed through Open WebUI's existing transient attachment/context path; the model receives no generic filesystem path;
- private/authenticated repository review is BLOCKED in v1A while the typed repository path remains unresolved;
- inspect `SKILL.md`, referenced documents, scripts, templates, dependencies, package metadata, environment variables, network calls, filesystem/process behavior, credentials, external services, license, upstream source, and pinned version/commit;
- whether user-controlled values can become shell commands, executable code, arbitrary filesystem destinations, or administrative operations;
- overlap with existing company/upstream Skills and the canonical Git source-of-truth path.

Return only `REUSE_EXISTING`, `EXTEND_EXISTING`, `NEW_CAPABILITY`, or `REJECT`. A runtime-only installation is never canonical. Approved new or adapted Skills require a short-lived branch, PR, Repository Readiness, review, merge, and runtime reconciliation as a separate later gate.

## Tool Review Path

ToolScout-first is mandatory:

```text
determine requested operation
→ inspect installed/approved capability with ToolScout
→ reuse existing capability when adequate
→ otherwise review official upstream and exact version/license
→ classify Local Utility / Agent Tool or MCP / External Backend / Development Tool
→ propose the smallest bounded interface
```

The maintainer ToolScout surface is review-only and limited to
`advise_tool_use`, `query_registry`, `detect_candidates`,
`check_conflicts`, and `doctor`. It does not expose ToolScout memory-write
tools or any install/execute primitive.

For a local utility, the model selects only an approved logical Tool ID; an execution layer resolves the reviewed recipe. Never expose model-controlled `brew install`, `pip install`, `npm install`, arbitrary download-and-execute, or package-manager primitives.

Do not convert every Tool into MCP. When an MCP or external backend is justified, register it through the existing control plane, bind credentials narrowly, expose only required operations, and test positive and negative Profile access.

## Repository Path

For material Skill, Tool, MCP definition, or configuration changes, the
external repository workflow remains:

main
→ short-lived task branch
→ PR with reuse/security/rollback records
→ Repository Readiness PASS
→ human review/approval
→ merge
→ runtime reconciliation/acceptance

The EAO runtime repository path is currently:
BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED. It is not part of the v1A
runtime operation set. No shell or arbitrary HTTP fallback is allowed.

Direct push to `main`, force push, unseen-commit merge, or runtime-only canonical state is forbidden.

## Approval and Replay Safety

The model may recommend an action but never supplies approval authority.
The trusted Open WebUI server-side Action derives the HumanActor from the
current authenticated user and group context and re-derives the exact knowledge
source from the current owned chat branch. The Action computes the source
fingerprint, operation_id, target, expected current state, plan hash and HMAC
binding server-side, then rechecks authorization/source/current state after the
native confirmation dialog. It enforces a bounded TTL (default and maximum 30
minutes).

Material changes invalidate approval, including source fingerprint, upstream commit, dependency set, PR HEAD/CI state, Tool version/recipe, credentials/security scope, Profile exposure, target, or expected current state changes.

The operation-envelope and approval Action artifacts are reference-only. Their
replay/audit durability is not accepted on the current stack, so no EAO Admin
mutation, operation marker, or reconciliation claim is active. Do not invoke
the Action, retry `OUTCOME_UNKNOWN` or any unknown outcome, or use chat metadata as a ledger. The
HMAC key, contributor key, and trusted signature remain unavailable to the
maintainer model.

## Forbidden Capabilities

This Skill never grants or invokes:

- generic shell/terminal, arbitrary filesystem, Docker, SSH, sudo/root, or code execution;
- raw secrets or unrestricted provider administration;
- arbitrary GitHub administration or direct `main` mutation;
- deletion/reset/prune operations;
- a second knowledge authority, approval database, workflow engine, scheduler, or runtime reconciler;
- automatic Profile switching or employee-wide exposure.

## Verification

Report evidence for classification, reuse, source review, plan hash, approval decision, operation result, and acceptance. Repository/offline PASS is not runtime acceptance. If the actual Open WebUI/WeKnora/MCP binding is not present on an explicitly authorized target, report `BLOCKED` rather than claiming activation.
