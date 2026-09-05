# Enterprise AI Office — Agent Deployment Golden Path

This is the primary execution entry point for an AI engineering agent deploying Enterprise AI Office.

Read `AGENTS.md` first. Use `docs/DEPLOYMENT.md` for implementation detail and `docs/ACCEPTANCE-TESTS.md` for deeper validation.

## 1. Goal

A single deployment request should be enough for a capable AI engineering agent to drive the deployment from host inspection to a validated employee workflow.

The agent may stop for genuine human input such as missing credentials, an OS permission that requires human approval, an unresolved destructive conflict, or company-specific business choices that are not present in configuration.

The agent should not stop merely to ask whether to perform steps that are already part of this Golden Path.

## 2. Core Ready target

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
└── WeKnora
```

Additional Profiles, groups, Knowledge Bases, Skills, integrations, automation, coding workers, or messaging are added only when the company configuration requires them.

## 3. Validated reference stack

The machine-readable reproducibility baseline is [`config/validated-stack.yaml`](config/validated-stack.yaml).

The first validated Golden Path is based on the successful local reference deployment recorded in `state/DEPLOYMENT-STATE.md`:

```text
Host: Apple Silicon macOS
Container runtime: OrbStack / Docker
WeKnora: v0.8.0
Hermes Agent: v0.21.0, host-native
Open WebUI: v0.11.3
Employee Hermes long-term memory: disabled
```

These versions are a reproducibility baseline, not permanent project requirements.

For a deployment intended to reproduce the validated path, use the tested versions unless the task explicitly includes upgrade qualification. Do not silently replace a tested version with `main`, `latest`, or a newer release during the same deployment.

## 4. Required inputs

Before mutation, resolve from the company configuration or protected operator input:

- company identity and timezone;
- model/provider credentials required by the selected stack;
- administrator identity/credential provisioning method;
- intended employee access scope;
- any explicitly requested specialist roles or optional integrations;
- protected runtime/secrets location.

Use `config/company.example.yaml` as the public schema reference and `config/.env.example` as the non-secret input inventory. Real deployment values belong in a protected company-specific layer.

Generate internal service secrets when safe to do so and store them outside Git with restrictive permissions.

If a required external credential is missing, report exactly what is missing and stop with `BLOCKED — REQUIRED INPUT` rather than guessing.

## 5. Execution contract

Execute the following phases in order. Do not declare completion after installation alone.

### Phase A — Inspect

1. Read the required repository documents from `AGENTS.md`.
2. Run `scripts/preflight.sh` and inspect any existing installation before changing it.
3. Record OS, architecture, memory, disk, container runtime, Git, existing Hermes state, and runtime directories.
4. Reconcile an existing deployment with `state/DEPLOYMENT-STATE.md` before mutation.

Exit condition: the target host and existing state are understood.

### Phase B — Resolve target state

1. Read the company configuration.
2. Read `config/validated-stack.yaml` for the tested reference versions and baseline feature posture.
3. Start from the baseline `default/admin + general` Profile model.
4. Build only the groups, Knowledge Bases, Profiles, Skills, tools, and integrations required by that configuration.
5. Resolve runtime paths and protected secret locations.
6. Identify all required secrets without printing them.

Exit condition: there is one unambiguous target state and no unresolved required input.

### Phase C — Deploy WeKnora

1. Deploy the pinned WeKnora release using the supported upstream deployment plus `infrastructure/weknora/` guidance.
2. Keep database/cache services internal.
3. Persist database and uploaded documents.
4. Configure the required embedding/chat model roles.
5. Create only the Knowledge Bases declared by company configuration.
6. Validate document ingestion and retrieval with a small non-sensitive seed document before continuing.

Exit condition: WeKnora is healthy and retrieval returns the seeded source.

### Phase D — Deploy Hermes

1. Install/configure the pinned Hermes release host-native for the validated macOS path.
2. Use the baseline artifacts in `infrastructure/hermes/` as the starting configuration:
   - `default.config.example.yaml`;
   - `default.env.example`;
   - `general.config.example.yaml`;
   - `general.env.example`.
3. Preserve the privileged default/admin Profile as control-plane only.
4. Create the `general` employee Profile from `profiles/general/SOUL.md`.
5. Fill the WeKnora MCP path/URL/key placeholders with protected deployment values.
6. Add specialist Profiles only when requested by company configuration.
7. Keep normal employee API toolsets least-privilege; the baseline General template exposes only the approved read-only WeKnora MCP surface.
8. Use a distinct API credential for every employee-facing Profile.
9. Keep employee long-term memory disabled until the documented cross-user isolation gate passes.

Exit condition: the `general` Profile answers a grounded company query through its supported API and exposes source evidence.

### Phase E — Deploy Open WebUI

1. Deploy the pinned Open WebUI release using `infrastructure/open-webui/docker-compose.yml` as the validated reference adapter, reviewing it against the selected pinned release before reuse.
2. Persist Open WebUI state.
3. Provision the administrator, then disable open self-signup unless company policy says otherwise.
4. Create baseline groups `All-Employees` and `AI-Admins`.
5. Create a server-side General Assistant connection to the Hermes `general` Profile.
6. Do not expose the Hermes default/admin Profile as an employee assistant.
7. Set ordinary employee permissions to the validated baseline:
   - normal chat: enabled;
   - history: enabled;
   - file upload: enabled unless company policy disables it;
   - user System Prompt editing: disabled;
   - Advanced Parameters editing: disabled.
8. Add specialist groups and assistant connections only from company configuration.

Exit condition: a normal employee account sees only permitted assistants and can use General Assistant successfully.

### Phase F — Employee workflow acceptance

From the real employee client, verify:

1. employee login;
2. General Assistant visibility;
3. normal chat;
4. grounded WeKnora answer;
5. readable source evidence;
6. follow-up context;
7. conversation history after refresh/re-login;
8. file upload when enabled;
9. default/admin is not exposed;
10. employee Profile has no unapproved terminal/system tools;
11. unauthorized direct resource access fails closed.

Do not substitute backend health checks for the employee-client test.

Exit condition: all enabled Core Ready checks pass.

### Phase G — Record and report

1. Update `state/DEPLOYMENT-STATE.md` with the actual deployed versions, paths, enabled Profiles, access model, memory state, and acceptance results.
2. Record material deployment changes in `state/CHANGELOG.md` when operating an existing deployment.
3. Report one of:

```text
CORE READY
BLOCKED — REQUIRED INPUT
FAIL — <specific failed boundary>
```

Do not report `CORE READY` while an enabled core acceptance check is unresolved.

## 6. Core Ready vs Production Ready

`CORE READY` proves the basic enterprise AI office workflow works for employees.

`PRODUCTION READY` is a separate higher bar. Depending on the deployment it may additionally require:

- production knowledge and access review;
- protected/off-host backup and restore validation;
- startup/reboot recovery policy;
- remote/private access controls;
- enterprise identity/SSO if required;
- monitoring/operational ownership;
- production secrets handling;
- optional integrations actually used by the company.

Do not add optional systems merely to make the deployment look more complete.

## 7. Dry-run mode

When asked to validate deployability without installing anything:

1. run read-only preflight;
2. read company configuration and `config/validated-stack.yaml`;
3. resolve the exact target state, versions, runtime paths, and protected inputs;
4. map every Golden Path phase to the repository artifact or pinned upstream mechanism that implements it;
5. produce the phase-by-phase actions and expected exit evidence;
6. identify only genuine required human inputs;
7. do not mutate the host.

A dry run is successful only if the agent can reach an unambiguous execution plan without inventing company requirements.

## 8. Final rule

The repository should make routine deployment decisions for the agent.

Human intervention is for missing authority, secrets, permissions, or real business choices — not for reminding the agent to connect the components, configure baseline RBAC, test the employee client, or record deployment state.
