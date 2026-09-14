# EAO Resource Intake

Status: company-owned shared Skill artifact for the `maintainer` Profile.

## Role

Provide the governed, read-first orchestration for EAO administrator resource intake. This Skill is policy and workflow guidance; it is not a shell wrapper, package manager, approval database, or runtime reconciler.

## Prerequisites

- authenticated Open WebUI user in the configured `EAO Administrators` group;
- the `maintainer` Profile and private `EAO Admin` Assistant;
- current repository authority and capability registry;
- supported WeKnora contributor/retrieval API when Knowledge ingestion is requested;
- existing MCP/control-plane registry for capability registration;
- ToolScout-first review path for proposed Tools or commodity utilities;
- protected server-side operation-plan/approval binding.

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
→ immutable operation plan
→ trusted approval when material mutation is required
→ bounded typed operation only
→ acceptance evidence
```

Classification must produce exactly one primary class:

| Class | Initial authority | v1A disposition |
| --- | --- | --- |
| Knowledge | WeKnora + source provenance | bounded contributor ingestion after approval |
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
6. create an immutable operation envelope;
7. show the exact plan to the authenticated administrator and require trusted approval;
8. use only the bounded WeKnora contributor operation;
9. require parse/index completion, direct retrieval, source evidence, and normal Hermes retrieval before `ACTIVE`;
10. leave failed or conflicting material inactive and surface the conflict.

The pinned WeKnora v0.8.0 contributor path is the official API with a
separate tenant API key carrying exactly ingest and retrieve plus an
explicit non-empty Knowledge Base allow-list. Its v1A routes are file, URL, and
manual knowledge creation, plus knowledge status retrieval. It must keep
full_access=false and must not use manage_kbs, manage_agents, manage_models, MCP
admin, tenant/system admin, platform, or runtime-management capabilities.

Knowledge ingestion does not authorize Knowledge Base deletion, embedding/reranker changes, bulk destructive deletion, or direct database writes.

## Skill Review Path

Inspect actual source before recommending anything:

- `SKILL.md`, referenced documents, scripts, templates, dependencies, package metadata, environment variables, network calls, filesystem/process behavior, credentials, external services, license, upstream source, and pinned version/commit;
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

The model may prepare a plan but never approves it. A trusted Open WebUI
server-side action derives the HumanActor from the current authenticated user
and group context, rechecks authorization, verifies the immutable plan hash,
trusted server-side HMAC signature, and expected current state, and enforces a
bounded TTL (default 30 minutes and maximum).

Material changes invalidate approval, including source fingerprint, upstream commit, dependency set, PR HEAD/CI state, Tool version/recipe, credentials/security scope, Profile exposure, target, or expected current state changes.

Every mutation carries a stable `operation_id`. A replay of a completed operation returns the existing/current result. `OUTCOME_UNKNOWN` becomes `RECONCILIATION_REQUIRED` and must not be blindly retried.

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
