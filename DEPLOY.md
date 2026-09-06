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
├── All-Employees group
├── General Assistant
└── Hermes `general` Profile

Knowledge
└── company-defined WeKnora Knowledge Base(s)
```

Repository templates are a capability library, not a deployment checklist.

## 4. Validated reference stack

The first validated core path is recorded in `config/validated-stack.yaml` and `state/DEPLOYMENT-STATE.md`:

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

## 5. Required inputs

Before mutation, resolve from the company configuration or protected operator input:

- company identity and timezone;
- `deployment.target_readiness`;
- model/provider credentials required by the selected stack;
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
4. Reconcile an existing deployment with `state/DEPLOYMENT-STATE.md` before mutation.

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
4. Configure the required embedding/chat model roles.
5. Create only Knowledge Bases declared by company configuration.
6. Validate ingestion/retrieval with a small non-sensitive seed document before continuing.

Exit condition: WeKnora is healthy and retrieval returns the seeded source.

## 9. Phase D — Deploy Hermes

1. Install/configure the pinned Hermes release using its supported upstream method.
2. Preserve privileged default/admin as control-plane only.
3. Create `general` from the repository SOUL/config templates.
4. Create specialist Profiles only when selected by company configuration, using the generic specialist template plus the selected role SOUL.
5. Register WeKnora through supported MCP/API integration.
6. Give normal employee Profiles least-privilege retrieval tools unless their declared work requires more.
7. Use a distinct API credential for every employee-facing Profile.
8. Keep employee long-term memory disabled unless the configured memory capability passes its isolation gate.
9. Configure explicit served-Profile allowlisting when supported by the selected release.

Exit condition: every enabled employee Profile responds through its supported API with its intended capability boundary; `general` answers a grounded company query with source evidence.

## 10. Phase E — Deploy Open WebUI and baseline RBAC

1. Deploy the pinned Open WebUI release with persistent state.
2. Provision the administrator using the validated bootstrap mechanism.
3. Keep open self-signup disabled unless company policy explicitly enables it.
4. Create baseline groups `All-Employees` and `AI-Admins`.
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

Update `state/DEPLOYMENT-STATE.md` with actual runtime truth:

- requested and achieved readiness;
- component versions/commits;
- paths/storage;
- enabled Knowledge Bases;
- enabled Profiles;
- groups/Assistant mappings;
- model/provider roles;
- capability enablement table;
- memory state;
- network/access boundary;
- backup/recovery state when applicable;
- acceptance results;
- known limitations.

Record material changes in `state/CHANGELOG.md` when operating an existing deployment.

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
