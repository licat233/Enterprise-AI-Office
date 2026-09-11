# Enterprise AI Office — Agent Deployment Golden Path

This is the primary execution entry point for an AI engineering agent deploying Enterprise AI Office.

Read `AGENTS.md` first. Read `docs/COMPLETENESS.md` and `config/capabilities.yaml` before resolving target state. Use `docs/DEPLOYMENT.md` for implementation detail and `docs/ACCEPTANCE-TESTS.md` for validation.

## 1. Goal

A single deployment request should be enough for a capable AI engineering agent to drive the requested deployment from host inspection to its declared readiness level.

The agent may stop for genuine human input such as missing credentials, an OS permission that requires human approval, an unresolved destructive conflict, or a company-specific business choice that is absent from configuration.

The agent must not stop merely to ask whether to perform a phase that is already required by this Golden Path.

## 2. Readiness levels

The adopting company's configuration declares one target:

```text
core-ready
configured-ready
production-ready
```

Semantics are defined in `docs/COMPLETENESS.md`.

In short:

```text
CORE READY
= baseline employee workflow works

CONFIGURED READY
= Core Ready + every company-enabled capability deployed and accepted

PRODUCTION READY
= Configured Ready + production recovery/security/operations controls accepted
```

Do not stop at Core Ready when the requested target is higher.

## 3. Core employee path

The baseline employee workflow is:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes `general` Profile
→ WeKnora MCP/API
→ grounded company answer + source
```

The baseline deployment contains:

```text
Control plane
└── Hermes default/admin Profile

Employee plane
├── Open WebUI
├── company group `all-employees` (display: `All Employees`)
├── General Assistant
└── Hermes `general` Profile

Knowledge
└── company-defined WeKnora Knowledge Base(s)
```

Repository templates are a capability library, not a deployment checklist.

## 4. Validated reference stack

The current reproducible Core version/commit authority is `config/validated-stack.yaml`. The historical `state/DEPLOYMENT-STATE.md` contains validation evidence from multiple past phases and is not a second version authority:

```text
Host: Apple Silicon macOS
Container runtime: OrbStack / Docker
WeKnora: v0.8.0
Hermes Agent: v0.21.0, host-native
Open WebUI: v0.11.3
Employee Hermes long-term memory: disabled
```

For a deployment intended to reproduce this path, use the tested versions unless the task explicitly includes upgrade qualification. Do not silently replace a tested version with `main`, `latest`, or a newer release during the same deployment.

Optional components not present in the first reference deployment require their own compatibility check and exact version/commit recording when enabled.

### 4.1 Deterministic Core acquisition

Do not infer upstream repositories or installation methods from product names.
Read `config/validated-stack.yaml` and acquire the exact validated component
commit/runtime before configuration.

For the current baseline:

#### WeKnora

```sh
: "${RUNTIME_ROOT:?set RUNTIME_ROOT to the approved deployment runtime root}"
mkdir -p "${RUNTIME_ROOT}/upstream"
git clone https://github.com/Tencent/WeKnora.git "${RUNTIME_ROOT}/upstream/WeKnora"
git -C "${RUNTIME_ROOT}/upstream/WeKnora" checkout --detach 1edcd54b43606d9079bb36650efe3f68707a79ea
git -C "${RUNTIME_ROOT}/upstream/WeKnora" rev-parse HEAD
```

The checkout must resolve exactly to the component `commit` in
`config/validated-stack.yaml`. Its tag `v0.8.0` is verified to point to that
commit. For the upstream Compose runtime set `WEKNORA_VERSION=0.8.0` in the
protected/runtime WeKnora environment, then apply the repository WeKnora
adapter and provisioning contract. Do not use `latest`.

#### Hermes Agent

Hermes `0.21.0` is the package version at the validated commit; the upstream
repository has no validated `v0.21.0` tag for this baseline. Pin by commit.

Use the official installer **from the same pinned commit** rather than the
moving installer on `main`:

```sh
HERMES_COMMIT=f1ccf436a27522c1bb5d36383a6f13b950676338
curl -fsSL "https://raw.githubusercontent.com/NousResearch/hermes-agent/${HERMES_COMMIT}/scripts/install.sh" \
  | bash -s -- --commit "${HERMES_COMMIT}" --skip-setup
```

After installation, verify the installed checkout resolves to
`HERMES_COMMIT`, then apply the repository-managed default/general Profile
configuration. Do not run `hermes update` during the same reproduction task.

#### Open WebUI

Open WebUI does not require an upstream source checkout for the validated
runtime. The repository Compose adapter already pins the official image:

```text
ghcr.io/open-webui/open-webui:v0.11.3
```

The upstream tag `v0.11.3` is verified to point to source commit
`2a960a59fe1dbbd35282f0556b3666d81102e781`, matching the component commit
in `config/validated-stack.yaml`.

Provide the required protected administrator environment values, then use:

```sh
docker compose -f infrastructure/open-webui/docker-compose.yml pull
docker compose -f infrastructure/open-webui/docker-compose.yml up -d
```

If any resolved upstream ref, package version, image tag, or checkout differs
from `config/validated-stack.yaml`, stop as version drift. Do not silently
continue with a nearby release.

### 4.2 Post-acquisition Core identity assertions

Liveness is not identity. Before configuration is treated as a reproduction of
the validated Core, prove the acquired/running runtime matches
`config/validated-stack.yaml`.

#### WeKnora

```sh
: "${RUNTIME_ROOT:?set RUNTIME_ROOT to the approved deployment runtime root}"
WEKNORA_DIR="${RUNTIME_ROOT}/upstream/WeKnora"

test "$(git -C "${WEKNORA_DIR}" rev-parse HEAD)" = "1edcd54b43606d9079bb36650efe3f68707a79ea"
test "$(docker inspect -f '{{.Config.Image}}' WeKnora-app)" = "wechatopenai/weknora-app:0.8.0"
```

#### Hermes Agent

Resolve the actual installed source checkout; do not assume a path when the
installer used an explicit directory or an FHS/root layout.

```sh
: "${HERMES_SOURCE_DIR:?set HERMES_SOURCE_DIR to the actual Hermes source checkout}"

test "$(git -C "${HERMES_SOURCE_DIR}" rev-parse HEAD)" = "f1ccf436a27522c1bb5d36383a6f13b950676338"
hermes --version | grep -F "0.21.0"
```

#### Open WebUI

```sh
test "$(docker inspect -f '{{.Config.Image}}' eaio-open-webui)" = "ghcr.io/open-webui/open-webui:v0.11.3"
```

A failed assertion is a version/runtime-identity failure, even if the service
returns HTTP 200. Resolve the mismatch or perform an explicit upgrade
qualification; do not waive the assertion as "close enough."

## 5. Required inputs

Before mutation, resolve from the company configuration or protected operator input:

- company identity and timezone;
- `deployment.target_readiness`;
- model/provider credentials actually required by the selected stack; a local-only embedding path may require no cloud embedding credential;
- administrator provisioning method/credential;
- employee access scope;
- enabled optional capabilities and their company-specific parameters;
- protected runtime/secrets location.

Generate internal service secrets when safe to do so and store them outside Git with restrictive permissions.

If a required external credential, identity-provider registration, platform token, workspace choice, or other real authority is missing, report exactly what is missing and stop with:

```text
BLOCKED — REQUIRED INPUT: <specific input>
```

Do not guess.

## 6. Phase A — Inspect

1. Read the required repository documents from `AGENTS.md`.
2. Run `scripts/preflight.sh` and inspect any existing installation before changing it.
3. Record OS, architecture, memory, disk, container runtime, Git, existing Hermes state, and runtime directories.
4. Reconcile an existing deployment against its protected operational state created from `state/DEPLOYMENT-STATE.template.md` before mutation. Use public historical/reference state only as evidence, never as the live target state.

Exit condition: the target host and existing state are understood.

## 7. Phase B — Resolve target and capability closure

1. Read the company configuration.
2. Read `config/capabilities.yaml`.
3. Resolve the requested readiness level.
4. Start from `default/admin + general` as the Profile baseline.
5. Build the exact enabled capability set from company configuration.
6. For every enabled capability, resolve its implementation path, required protected inputs, acceptance test, and state fields.
7. Resolve exact component versions/runtime paths.
8. Produce an internal capability closure table before mutation.

Do not infer organization structure or optional features from repository templates.

Exit condition: there is one unambiguous target state; every enabled capability has an implementation/acceptance path; required human inputs are resolved.

## 8. Phase C — Deploy WeKnora

1. Deploy the pinned WeKnora release using the supported upstream deployment plus the repository adapter.
2. Keep database/cache/parser internals private.
3. Persist database and uploaded documents.

### Core model-role rule

For the baseline Enterprise AI Office employee path, **WeKnora does not need every model type configured**.

The baseline split of responsibility is:

```text
Hermes reasoning / final answer
→ Hermes-selected reasoning model

WeKnora knowledge retrieval
→ Embedding model
```

For Core deployment, use this model-role matrix:

| WeKnora model role | Core requirement | Enable when |
| --- | --- | --- |
| Embedding | **Required** | always for vectorized knowledge retrieval |
| KnowledgeQA / Chat | **Not required by default** | only when a selected WeKnora workflow itself must generate answers, such as direct WeKnora Ask/Chat behavior |
| Rerank | **Disabled by default** | only after measured retrieval quality shows ranking problems that justify it |
| VLLM / multimodal model | **Disabled by default** | only when a selected document/image workflow requires model-based visual understanding |
| ASR | **Disabled by default** | only when audio transcription is an actual company requirement |

Do not configure a cloud Chat/KnowledgeQA model merely because WeKnora exposes that model type. In the baseline architecture, Hermes is already the reasoning/answer layer and should consume WeKnora retrieval evidence directly.

A valid Core architecture is therefore:

```text
Open WebUI
→ Hermes `general`
→ selected Hermes reasoning model
→ WeKnora retrieval
   → selected Embedding model
```

This avoids an unnecessary nested path such as:

```text
Hermes reasoning model
→ WeKnora Chat model
→ knowledge retrieval
```

unless that extra WeKnora reasoning layer is explicitly required by the chosen workflow.

### Embedding provider choice

4. Resolve the embedding execution mode before asking for a provider credential:
   - **remote API** when minimizing host resource use and provider dependence/cost are acceptable;
   - **local Ollama** when the host has sufficient headroom and reducing recurring embedding API cost / external data flow is preferred.
5. Treat providers such as DashScope as optional model providers, not mandatory Enterprise AI Office components. If local embedding is selected and no WeKnora Chat/KnowledgeQA role is required, no DashScope credential is needed for Core.
6. For local multilingual Chinese/English deployments on a capable Apple Silicon host, start with a small mature model rather than a multi-billion-parameter embedding model. Current guidance:
   - `bge-m3` is the validated local choice for the first real Mac Studio deployment;
   - `qwen3-embedding:0.6b` remains a lighter fallback candidate when host resource efficiency is a stronger constraint.
7. Qualify the local candidate with a small representative corpus and a few real queries. Do not create a large benchmark project unless the first candidate shows a real retrieval or resource problem.
8. Record the selected embedding model and dimension before production-scale ingestion. Do not silently change them after indexing; changing embeddings normally requires reindexing.
9. Create only Knowledge Bases declared by company configuration.
10. Validate ingestion/retrieval with a small non-sensitive seed document before continuing.

See `docs/KNOWLEDGE.md` for embedding deployment trade-offs and `docs/DEPLOYMENT-PRACTICES.md` for lessons from real installations.

Exit condition: WeKnora is healthy and retrieval returns the seeded source. A separate WeKnora Chat/KnowledgeQA model is not an exit requirement unless the active company workflow explicitly enables a WeKnora feature that depends on it.

## 9. Phase D — Deploy Hermes

1. Install the pinned Hermes release through §4.1 and prove runtime identity through §4.2.
2. Reconcile the privileged default/admin control plane plus baseline `general` Profile through `infrastructure/hermes/PROVISIONING.md`.
3. On a fresh target create `general` using upstream Profile management with bundled-Skill opt-out; on an existing target reconcile it in place.
4. Create specialist Profiles only when selected by company configuration, using the generic specialist template plus the selected role SOUL.
5. Register only the approved WeKnora MCP/API surface for each knowledge-enabled employee Profile.
6. Give normal employee Profiles least-privilege tools unless their declared work requires more.
7. Use a distinct API credential for every employee-facing Profile and prove pairwise isolation.
8. Keep employee long-term memory disabled unless the configured memory capability passes its isolation gate.
9. Keep the shared API listener owned by the default Profile in the multiplex baseline and serve only the explicit Profile allowlist.

Exit condition: every enabled employee Profile responds through its supported API with its intended capability boundary; the served set matches desired state; `general` answers a grounded company query with source evidence.

## 10. Phase E — Deploy Open WebUI and baseline RBAC

1. Deploy the pinned Open WebUI release with persistent state.
2. Provision the administrator using the validated bootstrap mechanism.
3. Keep open self-signup disabled unless company policy explicitly enables it.
4. Reconcile Open WebUI groups from `employee_access.web.groups`, preserving the company logical ID → display name → runtime group UUID mapping. The generic baseline is `all-employees` → `All Employees` and `ai-admins` → `AI Administrators`.
5. Create server-side employee Assistant connections to the matching Hermes employee Profiles.
6. Never expose Hermes default/admin as an ordinary employee Assistant.
7. Apply the configured ordinary employee permissions. The validated baseline is:
   - normal chat: enabled;
   - history: enabled;
   - file upload: enabled unless company policy disables it;
   - user System Prompt editing: disabled;
   - Advanced Parameters editing: disabled.
8. Create specialist groups/resources only from company configuration.

Exit condition: ordinary employee accounts see only permitted Assistants and can use General Assistant successfully.

## 11. Phase F — Core employee acceptance

Run Part A of `docs/ACCEPTANCE-TESTS.md` from the actual employee-facing UI as well as the required backend boundaries.

Do not substitute service health checks for employee-client validation.

Exit condition: `CORE READY` is PASS.

If the requested target is `core-ready`, continue to state recording/reporting. Otherwise continue.

## 12. Phase G — Close every enabled capability

For each company-enabled conditional capability in `config/capabilities.yaml`:

1. open its referenced implementation playbook/adapter;
2. resolve version-specific upstream behavior against the selected pinned release;
3. deploy/configure only that requested capability;
4. enforce the documented security boundary;
5. run the matching conditional acceptance test;
6. record actual state/evidence.

Typical capability paths include:

```text
specialist Profiles → Profile standard + generic Profile templates
hermes-webui         → infrastructure/hermes-webui/
coding delegation    → infrastructure/coding-agents/
Kanban / Cron        → infrastructure/hermes/features/
messaging            → infrastructure/hermes/features/
remote access / SSO  → infrastructure/access/
long-term memory     → Profile/RBAC memory isolation rules
```

An enabled capability may not be silently skipped, disabled, or deferred to obtain a green result.

Exit condition: all enabled conditional capabilities PASS or execution stops at a specific blocker/failure.

When Core Ready and all enabled conditional capabilities pass, record `CONFIGURED READY`.

If the requested target is `configured-ready`, continue to state recording/reporting. Otherwise continue.

## 13. Phase H — Production readiness closure

For `production-ready`, implement and validate the production controls selected by the capability registry and company configuration:

- production knowledge/data boundary review;
- backup plus protected/off-primary-disk recovery strategy;
- isolated restore validation;
- startup/recovery policy;
- secrets protection/recovery;
- network and admin access review;
- operational health/ownership;
- representative production parsing/Golden Questions/security tests.

Use:

- `docs/BACKUP-RESTORE.md`;
- `docs/SECURITY.md`;
- `docs/OPERATIONS.md`;
- `scripts/backup.sh`;
- `scripts/restore.sh`;
- `scripts/health-check.sh`;
- Part C of `docs/ACCEPTANCE-TESTS.md`.

Exit condition: all applicable production controls PASS and `PRODUCTION READY` can be supported by evidence.

## 14. Phase I — Record and report

For a fresh deployment, copy `state/DEPLOYMENT-STATE.template.md` into the
deployment's **protected operational storage** and record actual runtime truth
there.

The reference backup/restore path expects the protected operational copy at
`${EAIO_RUNTIME_DIR}/state/deployment-state.md`. If the deployment deliberately
stores it elsewhere, set `EAIO_DEPLOYMENT_STATE_FILE` for backup operations and
record that non-secret location/boundary in the operational state.

Do **not** overwrite the repository's `state/DEPLOYMENT-STATE.md`: that file is
the historical sanitized demo record. Do not put private runtime IDs, network
identity, credentials, employee data, or company-private configuration into the
public repository merely to satisfy state recording.

The protected operational state should record:

- requested and achieved readiness;
- component versions/commits and exact runtime identity;
- paths/storage;
- WeKnora logical-ID → runtime-ID mappings and non-secret retrieval-key record metadata;
- Hermes served Profile set, Profile → API route/model ID, logical KB scopes, and non-secret credential reference names;
- Open WebUI logical group ID → display name → runtime UUID mappings and Profile/model ACL mappings;
- model/provider roles;
- capability enablement table;
- memory state;
- network/access boundary;
- backup/recovery state when applicable;
- acceptance results;
- known limitations.

When an explicitly authorized reference deployment needs a public status update,
publish only a sanitized summary through the existing public status/evidence
contract. Never treat the public summary as the protected runtime state store.

Record material reusable repository changes in `state/CHANGELOG.md` when
operating an existing deployment; keep company-private runtime-only changes in
the protected operational record.

Report one of:

```text
CORE READY
CONFIGURED READY
PRODUCTION READY
BLOCKED — REQUIRED INPUT: <specific missing authority/input>
FAIL — <specific failed boundary>
```

Never report a higher readiness level while a required lower level or enabled capability remains unresolved.

## 15. Dry-run mode

When asked to validate deployability without installing anything:

1. run read-only preflight;
2. read company configuration and capability registry;
3. resolve exact target state and requested readiness;
4. build the capability closure table;
5. resolve versions and implementation paths;
6. produce phase-by-phase actions and expected evidence;
7. identify only genuine required human inputs;
8. do not mutate the host.

A dry run is successful only when the agent can reach an unambiguous execution plan for every enabled capability without inventing company requirements.

## 16. Final rule

The repository should make routine integration decisions for the deployment agent.

Human intervention is for missing authority, secrets, permissions, or real business choices — not for reminding the agent to connect components, configure baseline RBAC, implement an already-enabled capability, run acceptance, or record deployment state.
