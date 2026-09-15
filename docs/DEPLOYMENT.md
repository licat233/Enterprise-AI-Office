# Deployment Reference

This document provides implementation detail for `DEPLOY.md`.

For deployment, the binding execution model is:

```text
AGENTS.md
→ DEPLOY.md
→ docs/COMPLETENESS.md
→ active company configuration
→ config/capabilities.yaml
→ implementation adapters/playbooks
→ docs/ACCEPTANCE-TESTS.md
→ deployment state
```

Do not expand the system from examples, and do not stop at the core path when the configured readiness level requires more.

## 1. Readiness model

A deployment declares one target:

```text
core-ready
configured-ready
production-ready
```

### Core Ready

The baseline employee path works:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes `general`
→ WeKnora MCP/API
→ grounded company answer + source
```

### Configured Ready

Core Ready remains PASS and every optional capability enabled by company configuration is deployed, secured, accepted, and recorded.

### Production Ready

Configured Ready remains PASS and applicable production recovery/security/access/operations controls are implemented and accepted.

See `docs/COMPLETENESS.md` for the full contract.

## 2. First validated core target

```text
Apple Silicon macOS
│
├── Host-native
│   └── Hermes Agent
│
└── OrbStack / Docker
    ├── WeKnora
    └── Open WebUI
```

The reproducibility baseline is machine-readable in `config/validated-stack.yaml`:

- WeKnora `v0.8.0`;
- Hermes Agent: `rolling-validated` (current accepted reference `0.21.2 / v2026.9.11`);
- Open WebUI `v0.11.3`.

WeKnora and Open WebUI are tested exact reference versions. Hermes uses a rolling-validated policy rather than a permanent version pin. Do not silently change a running Hermes deployment; resolve one exact candidate commit per install/upgrade transaction and validate it before promotion.

Optional components not present in the first reference demo require version-specific upstream verification when enabled.

Core upstream identity and acquisition policy are machine-readable in
`config/validated-stack.yaml`. Use `DEPLOY.md §4.1`. For Hermes, resolve the
configured upstream tracking ref once at transaction start and freeze that exact
candidate commit for the transaction; do not follow a moving ref mid-deployment.

## 3. Pre-deployment inventory

Before mutation record/inspect:

- OS/version and CPU architecture;
- RAM and free disk;
- container runtime/version;
- Git and required runtime tools;
- existing Hermes state;
- existing Enterprise AI Office runtime directories;
- protected config/secrets location;
- intended employee/admin access method.

Run `scripts/preflight.sh` first.

The script distinguishes EAO Core prerequisites from optional/operator tools:
missing Git, Docker, Docker Compose, Python 3, curl, bash, or an unreachable
Docker daemon is a Core blocker; missing Node/npm/Hermes/Codex/Claude/GitHub CLI
at pre-install time is only optional/current-state discovery.

The exact validated reference host family is Apple Silicon macOS with
OrbStack-provided Docker/Compose. A different Docker-compatible runtime may be
used only with explicit compatibility revalidation of host bridging, Compose/
volume behavior, file permissions, and restart/recovery semantics.

For an existing deployment, reconcile runtime reality with its protected operational state created from `state/DEPLOYMENT-STATE.template.md` before changing it. Treat the repository's `state/DEPLOYMENT-STATE.md` only as historical sanitized evidence.

## 4. Runtime layout

Suggested macOS reference layout:

```text
/Users/Shared/enterprise-ai-office/
├── ops/
├── runtime/
│   ├── WeKnora/
│   ├── open-webui/
│   └── optional-component-checkouts/
├── company-skills/
├── backup-work/
└── logs/
```

Hermes should use its supported upstream home convention unless the deployment has a justified alternative.

Secrets and private company values remain outside the public repository.

## 5. Resolve company target before installation

Read the active company config and `config/capabilities.yaml`.

Baseline objects:

```text
Hermes Profiles
├── default/admin
└── general

Open WebUI groups
├── All-Employees
└── AI-Admins

Knowledge
└── company-defined shared employee Knowledge Base(s)
```

Then build a capability closure table for every enabled optional capability.

Typical conditional capabilities are:

- specialist Profiles;
- hermes-webui;
- Codex/Claude Code delegation;
- Kanban;
- Cron;
- messaging;
- remote/private access;
- SSO/enterprise identity;
- employee Hermes long-term memory.

A template/playbook existing in the repository is not sufficient reason to enable it.

An enabled capability cannot be silently skipped.

## 6. WeKnora

Use the selected pinned upstream release plus `infrastructure/weknora/`.

Requirements:

- persistent database and uploaded documents;
- service-to-service routing by Compose service name/Docker DNS, never by a remembered container IP;
- WeKnora frontend proxying that survives backend container recreation without requiring a frontend restart;
- internal database/cache/parser services not publicly exposed;
- only the model roles required by the selected workflow configured;
- only configured Knowledge Bases created;
- non-sensitive seed document ingested and retrieved before Hermes integration.

### 6.1 Container lifecycle and host-service networking

Use `infrastructure/weknora/docker-compose.eaio.override.yml` with the pinned upstream Compose runtime. The EAO frontend wrapper keeps the upstream image/entrypoint but makes the `app` upstream dynamically resolvable through Docker DNS, preventing stale-IP `502` failures after backend recreation.

Operational rules:

```text
Compose project name  = stable deployment identity
Compose service name  = stable service identity
named volume identity = persistent state identity
container IP          = disposable implementation detail
```

Never encode a Docker-assigned `172.x/192.168.x` container IP into Nginx, application configuration, deployment state, or runbooks.

The validated baseline freezes WeKnora project identity as `weknora` and Open
WebUI as `eaio-openwebui`. Do not let a changed checkout/working-directory name
silently create a second set of named volumes.

The WeKnora runtime must preserve `SYSTEM_AES_KEY` as a protected continuity
secret. Database recovery with a different/missing key is incomplete because
encrypted credentials may become unreadable while records remain present.

When a containerized WeKnora service calls a process running on the macOS host, `localhost` points back to that container. On the validated Docker Desktop/OrbStack-style path, use `host.docker.internal:<port>` and verify it from inside the actual WeKnora container. If the endpoint is protected by WeKnora SSRF validation, put the trusted host/CIDR in the container-visible `SSRF_WHITELIST_EXTRA` configuration and recreate the affected service through Compose.

### 6.2 Core model responsibilities

The Enterprise AI Office Core path deliberately separates reasoning from retrieval:

```text
Hermes
→ reasoning / answer generation

WeKnora
→ knowledge ingestion / indexing / retrieval / source evidence
```

Therefore the baseline WeKnora model configuration is intentionally minimal:

| Model role | Core default | Purpose |
| --- | --- | --- |
| Embedding | **Required** | vectorize documents and retrieval queries |
| KnowledgeQA / Chat | **Not configured by default** | only needed when WeKnora itself must generate an answer or run a Chat/Ask workflow |
| Rerank | **Disabled** | optional second-stage ranking when measured retrieval quality requires it |
| VLLM / multimodal | **Disabled** | optional visual/model-assisted document workflows |
| ASR | **Disabled** | optional audio transcription workflows |

Do not confuse "WeKnora supports this model type" with "Enterprise AI Office Core requires this model type."

For the normal employee path, Hermes receives retrieved WeKnora evidence and its own selected reasoning model produces the final answer. A separate WeKnora Chat/KnowledgeQA model would duplicate reasoning and add another provider/cost/failure boundary unless a concrete WeKnora-native workflow needs it.

### 6.3 Embedding may be remote or local

Embedding is an independent provider/runtime choice.

Supported deployment patterns include:

```text
Remote:
WeKnora → cloud Embedding API

Local:
WeKnora → Ollama → local Embedding model
```

A cloud provider such as DashScope is optional. It is not an Enterprise AI Office dependency by itself.

If the deployment uses local embedding and does not enable a WeKnora-native Chat/KnowledgeQA workflow, there is no reason to request a DashScope API key merely to complete Core.

The current ARMOR Mac Studio reference uses:

```text
WeKnora v0.8.0
→ local Ollama
→ qwen3-embedding:0.6b
→ 1024 dimensions
```

The original Mac Studio qualification used `bge-m3` successfully; that evidence remains useful historical validation, but the current runtime has migrated to `qwen3-embedding:0.6b` to reduce local-model ecosystem complexity while keeping the embedding role lightweight. For fresh ARMOR-like deployments, use the current Qwen3 embedding baseline unless measured quality or compatibility evidence justifies another model.

Do not default to 4B/8B embedding models without measured need. Embedding changes on an existing Knowledge Base are migrations and normally require a compatible reindex/reingestion path.

### 6.4 Retrieval tuning

Start with upstream/default retrieval capabilities. Add reranking or alternate retrieval infrastructure only when the configured requirement or measured retrieval quality justifies it.

The ARMOR reference currently enables local reranking with `Qwen3-Reranker-0.6B` through a small host-local `llama-server` endpoint. This is a deployment choice, not a Core requirement, and does not justify introducing another orchestration platform.

Embedding changes are high risk because reindexing may be required. Select and record the embedding model and vector dimension before production-scale ingestion whenever possible.

For WeKnora v0.8.0 local Ollama embedding, re-check the version-specific `truncate_prompt_tokens` behavior documented in `docs/KNOWLEDGE.md` / `docs/DEPLOYMENT-PRACTICES.md` rather than assuming a value of `0` means unlimited.

## 7. WeKnora → Hermes knowledge bridge

Use supported WeKnora MCP/API surfaces.

Normal business Profiles should receive only the retrieval operations needed for their allowed Knowledge Bases.

The repository's baseline Hermes templates use a read-only WeKnora MCP whitelist.

Do not give normal knowledge flows direct SQL/database coupling.

For the Core path, prefer retrieval/read operations over a WeKnora-native Ask/Chat operation unless the active workflow explicitly requires WeKnora to perform its own answer generation.

## 8. Hermes baseline

Use `infrastructure/hermes/` with the transaction-scoped rolling-validated Hermes candidate.

Core Profile/Gateway reconciliation is defined in
`infrastructure/hermes/PROVISIONING.md`. It covers fresh-profile creation,
existing-profile reconciliation, bundled-Skill opt-out for the baseline
`general` Profile, shared multiplex Gateway ownership, Profile-scoped API
credentials, effective tool checks, and the Hermes → WeKnora seed retrieval.

Baseline:

- default/admin retained as privileged control plane;
- `general` created from `profiles/general/SOUL.md` plus baseline config template;
- WeKnora MCP registered;
- distinct employee Profile API credential;
- least-privilege API toolset;
- employee long-term memory disabled until proven isolated;
- explicit served-Profile allowlist where supported;
- default/admin not exposed to employee client.

## 9. Specialist Profiles

When active company configuration declares an employee-facing specialist Profile:

1. start from `infrastructure/hermes/specialist.config.example.yaml` and `.env.example`;
2. select the appropriate SOUL/template or define the role cleanly;
3. define employee group mapping;
4. define Knowledge Base scope;
5. define effective tools/credentials;
6. define model/memory policy;
7. create a distinct API credential;
8. add it to the served allowlist as appropriate;
9. expose only its intended employee Assistant resource;
10. run specialist RBAC/credential/behavior acceptance.

Do not infer specialist roles from the optional templates directory.

## 10. Skills

Use company-owned shared Skills through supported external directories where practical.

A Profile receives only Skills relevant to its actual work.

Authoritative company facts belong in WeKnora rather than being duplicated into SOUL/Skill prose.

## 11. Tool least privilege

Normal employee Profiles default to no unrestricted:

- terminal;
- filesystem writes;
- Docker/system control;
- GitHub administration;
- Codex/Claude Code delegation;
- raw credentials.

Privileged technical capabilities require an explicit role, workspace, and credential boundary.

## 12. Open WebUI

Use `infrastructure/open-webui/` and a pinned/tested release.

Baseline:

- persistent data;
- deterministic initial admin provisioning;
- open signup disabled unless explicitly required;
- `All-Employees` and `AI-Admins` groups;
- server-side General Assistant connection to Hermes `general`;
- Profile API keys kept server-side;
- default/admin not exposed;
- minimal employee permissions.

Validated employee baseline:

```text
Chat                     enabled
History                  enabled
File Upload              enabled unless company policy disables it
Chat System Prompt       disabled
Advanced Chat Parameters disabled
```

Specialist groups/resources are created only from company configuration.

## 13. Core employee acceptance

Use a real ordinary employee account and Part A of `docs/ACCEPTANCE-TESTS.md`.

Backend health is not enough. Validate actual login, Assistant visibility, grounded answer/source, follow-up, history, file upload when enabled, admin non-exposure, and dangerous-tool denial.

Likewise, service liveness is not runtime identity. Before `CORE READY`, run
the post-acquisition identity assertions in `DEPLOY.md §4.2` so WeKnora,
Hermes, and Open WebUI are proven to match `config/validated-stack.yaml`.

When Part A passes, `CORE READY` may be recorded.

If target readiness is higher, continue.

## 14. Capability closure for Configured Ready

For every enabled conditional capability, follow the implementation path in `config/capabilities.yaml`.

### hermes-webui

Use `infrastructure/hermes-webui/README.md`.

Pin a compatible upstream commit/version, keep the surface administrative and narrowly exposed, and run its conditional acceptance.

### Coding delegation

Use `infrastructure/coding-agents/README.md`.

Enable only authorized technical Profiles and explicit workspaces. Validate Codex/Claude Code in disposable/harmless repositories before real work.

### Kanban / Cron / messaging

Use `infrastructure/hermes/features/README.md` and the selected Hermes release's native features.

Do not add another workflow/scheduler/messaging framework when Hermes' native capability satisfies the requirement.

### Remote/private access and SSO

Use `infrastructure/access/README.md`.

The company must select/authorize the external access method or identity provider. Do not invent enterprise credentials or public exposure policy.

### Employee long-term memory

Use `docs/CLIENT-RBAC.md` / `docs/PROFILE-STANDARD.md`. Enable only after exact deployed user scoping passes isolation tests.

When all enabled Part B capabilities pass and state is recorded, `CONFIGURED READY` may be declared.

## 15. External input/blocker behavior

Some complete deployments necessarily depend on external authority:

- IdP/OIDC application registration;
- enterprise messaging application/bot credentials;
- private-access account/tunnel approval;
- model-provider credentials actually required by the selected model roles;
- approved repository/workspace paths;
- OS permissions requiring human approval.

When such input is required and unavailable, report exactly:

```text
BLOCKED — REQUIRED INPUT: <specific item>
```

Do not silently disable the requested capability and do not replace it with an unrelated provider.

## 16. Network posture

Conceptual trust path:

```text
Employee → Open WebUI
Open WebUI → authorized Hermes employee Profile API
Hermes → WeKnora MCP/API
AI Admin → protected admin surfaces
```

Keep PostgreSQL, Redis, parser workers, secret stores, and privileged raw routes private.

Remote access must use the configured approved boundary rather than public exposure by convenience.

## 17. Production Ready closure

When `deployment.target_readiness: production-ready`, continue after Configured Ready.

Implement/verify applicable production controls using:

- `docs/BACKUP-RESTORE.md`;
- `docs/SECURITY.md`;
- `docs/OPERATIONS.md`;
- `scripts/backup.sh`;
- `scripts/restore.sh`;
- `scripts/health-check.sh`;
- Part C of `docs/ACCEPTANCE-TESTS.md`.

Production closure includes the configured backup/restore strategy, isolated restore evidence, startup/recovery policy, secrets/access review, representative company knowledge/security testing, and operational ownership.

Do not equate container/service startup with Production Ready.

## 18. Deployment state

For a fresh deployment, start from `state/DEPLOYMENT-STATE.template.md` when available rather than copying the MacBook reference instance.

Record actual runtime truth:

- requested/achieved readiness;
- host/runtime;
- exact component versions;
- model/provider roles;
- Knowledge Bases;
- Profiles;
- groups/Assistant mappings;
- capability closure table;
- memory state;
- network/access boundary;
- production recovery controls where applicable;
- acceptance results;
- known limitations.

For an existing deployment, update its existing deployment state rather than replacing history with a template.

## 19. Dry-run planning

A dry run should resolve without host mutation:

```text
host
→ requested readiness
→ core versions/runtime
→ company Knowledge Bases
→ Profiles/groups
→ enabled capability closure
→ required protected inputs
→ implementation playbooks
→ acceptance evidence required
→ final state/report format
```

If the plan still contains routine questions such as “should I configure the enabled messaging capability?” the repository/configuration has not been followed correctly.

## 20. Final statuses

```text
CORE READY
CONFIGURED READY
PRODUCTION READY
BLOCKED — REQUIRED INPUT: <specific input>
FAIL — <specific failed boundary>
```

Use the highest status actually supported by evidence and never silently downgrade a configured target.
