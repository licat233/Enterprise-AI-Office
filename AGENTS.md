# AGENTS.md — Enterprise AI Office Agent Operating Contract

This repository is intentionally designed to be read, developed, installed from, and maintained by AI engineering agents as well as humans.

If you are an AI agent asked to design, extend, validate, deploy, debug, upgrade, or maintain Enterprise AI Office, this file is the highest-priority repository-local operating contract.

## 1. Mission

Enterprise AI Office is a reusable **system blueprint + installation blueprint** for building a self-hosted enterprise AI workspace around:

- WeKnora for enterprise knowledge;
- Hermes Agent for the primary agent runtime;
- Open WebUI for multi-user employee Web access;
- hermes-webui for Hermes administration when enabled;
- Codex and Claude Code for specialized software-engineering execution when enabled;
- MCP as the preferred integration boundary;
- Hermes Profiles, Skills, Kanban, Cron, Bot Mode, and Gateway where the adopting company actually needs them.

The repository must ultimately let a capable AI engineering agent answer two questions from repository evidence alone, plus genuine company-private inputs when deployment is requested:

```text
1. What is the Enterprise AI Office supposed to be?
2. How do I install, configure, secure, validate, and operate it for this company?
```

Repository development therefore has two major design responsibilities:

```text
System Design
→ define the product/architecture/capability/security model

Installation Design
→ turn that approved design into an agent-readable and agent-executable installation/acceptance contract
```

A **real company deployment is a separate consumer activity**. It is not the automatic next step of repository development and must not be inferred merely because the installation blueprint exists.

ARMOR is the first reference implementation. Company/reference material is evidence and example, not a universal deployment default.

## 2. Authority and required reading

Before making a material change, read the documents relevant to the task in this order:

1. `README.md`
2. `AGENTS.md`
3. `state/PROJECT-PHASE.yaml`
4. `DEPLOY.md` for installation-blueprint design or an explicitly activated real deployment task
5. `docs/COMPLETENESS.md` for readiness/completion semantics
6. `config/company.example.yaml` or the real company-private configuration when a deployment task exists
7. `config/capabilities.yaml` for capability closure
8. `config/validated-stack.yaml` for the reproducibility baseline
9. `docs/ARCHITECTURE.md`
10. `docs/DEPLOYMENT.md`
11. `docs/SECURITY.md`
12. `docs/PROFILE-STANDARD.md`
13. `docs/KNOWLEDGE.md`
14. `docs/CLIENT-RBAC.md`
15. `docs/BACKUP-RESTORE.md` when production/recovery is in scope
16. `docs/UPGRADE.md` when versions change
17. `docs/ACCEPTANCE-TESTS.md`
18. `state/DEPLOYMENT-STATE.md` when operating an existing deployment
19. `state/CHANGELOG.md` when changing an existing deployment
20. the relevant company/reference material under `reference/` when useful

### Blueprint lifecycle and real-deployment gate — interpret before acting

`state/PROJECT-PHASE.yaml` is the sole repository authority for the current **blueprint-development phase** and for whether a **real deployment task** is active.

These are different concepts.

```text
Blueprint lifecycle
system_design
→ installation_design
→ blueprint_validation
→ release_ready

Real deployment task
inactive by default
→ active only for an explicitly requested real target
```

Do not infer either a blueprint transition or a real deployment task from:

- repository momentum;
- previous assistant assumptions;
- prototype/adaptor code existing;
- tests passing;
- an installation/implementation plan existing;
- deployment documents existing;
- acceptance contracts existing;
- a provider having been selected;
- phrases such as `continue`, `keep going`, `start`, `begin`, `next`, `proceed`, `继续`, `开始`, `开始吧`, `下一步`, or `好的`.

Continuation language means:

> **Continue valid work inside the current blueprint phase.**

It does not authorize a blueprint-phase transition and it does not activate a real deployment task.

#### Current blueprint phase

Read `blueprint_lifecycle.current_phase` from `state/PROJECT-PHASE.yaml`.

When it is `system_design`, stay focused on what the system should be: product behavior, architecture, capability scope, authority, security, Ontology, user workflows, upstream choices, acceptance criteria, and design-support prototypes.

When it becomes `installation_design`, design how a capable AI agent should install the approved system: deployment sequencing, configuration contracts, scripts, idempotency, secret-input boundaries, rollback/recovery, clean-host instructions, and installation-time acceptance.

**Installation design is still repository design work. It does not authorize installation onto a real company system.**

When it becomes `blueprint_validation`, an explicitly approved isolated/clean validation target may be used to prove that a fresh AI agent can understand and reproduce the blueprint. Validation authorization must identify the target; it does not imply production deployment.

#### Real deployment task

Read `real_deployment_task.active` from `state/PROJECT-PHASE.yaml` and the actual human request.

A real deployment requires:

```text
explicit human request
+
explicit real target
+
company-private configuration/authority as needed
```

Without that combination, do not request or use real provider credentials, connect real mailboxes/business systems, bind real employees/accounts/Profiles, or mutate a live/production environment merely to continue blueprint development.

Missing real credentials are never blockers for system-design or installation-design work because credentials belong to a real deployment or explicitly approved validation task.

If the next apparent step would cross the current blueprint phase, continue with the closest valid work inside the current phase or state that the next blueprint phase requires explicit human direction. If the next apparent step would touch a real company instance, do not do it unless a real deployment task has been explicitly activated.

When the task is part of the current v2 Communication & Follow-up milestone, also read before mutation:

```text
docs/V2-SCOPE.md
docs/V2-DESIGN-REVIEW.md
docs/V2-PHASE-STATUS.md
docs/V2-IMPLEMENTATION-PLAN.md
```

Treat `docs/V2-IMPLEMENTATION-PLAN.md` as an installation-blueprint planning artifact. Its existence does not mean the current blueprint phase has advanced and does not activate a real deployment.

For v2 email work, additionally read the concrete provider capability paths referenced by `config/capabilities.yaml`, treating them as design-support prototypes, installation-blueprint artifacts, validation assets, or deployment assets according to the current blueprint phase and deployment-task state.

For an explicitly activated real deployment, `DEPLOY.md` becomes the execution contract. `docs/COMPLETENESS.md` defines readiness. `config/capabilities.yaml` maps enabled capabilities to installation and acceptance paths.

The root-level ARMOR v1 design document and content under `reference/` are non-normative reference material. They must not override `AGENTS.md`, `state/PROJECT-PHASE.yaml`, `DEPLOY.md`, current generic standards, the adopting company's active configuration, or actual runtime state.

If a referenced installation artifact is missing while designing the installation blueprint, treat that as a blueprint completeness defect. If it is missing for an enabled capability during a real deployment, treat that as a deployment-blocking repository defect. Do not silently invent a different architecture.

## 3. Frozen architecture intent

Do not silently replace the approved architecture.

| Responsibility | Default component |
| --- | --- |
| Blueprint lifecycle / deployment-task gate | `state/PROJECT-PHASE.yaml` |
| Enterprise knowledge | WeKnora |
| Primary agent runtime | Hermes Agent |
| Employee Web client | Open WebUI |
| Hermes administrative client | hermes-webui when enabled |
| AI work roles | Hermes Profiles |
| Knowledge bridge | WeKnora MCP / supported API |
| Governed external business state | Selected provider/System of Record through an enabled narrow capability |
| EAO-owned operational governance evidence | Capability/Ontology layer only where explicitly defined |
| Durable agent work | Hermes Kanban when enabled |
| Scheduled automation | Hermes Cron when enabled |
| Coding execution | Codex + Claude Code when enabled |
| Messaging access | Hermes Gateway when enabled |
| Blueprint authority | this repository's current contracts and machine-readable state |
| Real deployment truth | active private company config + this repository + actual runtime/deployment state |

Implementation details may change to match selected upstream releases. Component responsibilities and security boundaries may not change without an explicit architecture decision.

## 4. Source-of-truth rules

Do not let multiple systems become authoritative for the same information class.

- Current blueprint phase and real-deployment-task gate: `state/PROJECT-PHASE.yaml`.
- System/installation design intent: current normative repository contracts.
- Company knowledge: WeKnora.
- Agent identity/behavior: Hermes Profile configuration, SOUL, Skills, Tools, MCP.
- Human identity and employee Web access: Open WebUI or the explicitly selected enterprise identity layer.
- External operational business state: the selected provider/System of Record.
- Enterprise AI Office-owned approval/draft/governance evidence: only where an approved capability/Ontology contract explicitly defines it.
- Durable agent task state: Hermes Kanban when enabled.
- Scheduled agent work: Hermes Cron when enabled.
- Desired real deployment state: active private company deployment configuration.
- Actual real deployment state: real runtime + deployment-specific state record.
- ARMOR `armor-memory`: independent unless a later approved integration says otherwise.

## 5. Critical conceptual boundaries

### Profile is not a user

A Hermes Profile is an AI role/specialist, not an employee account. Do not create one Profile per employee by default.

### Core vs specialist Profiles

Baseline:

```text
default/admin  → privileged control plane
general        → baseline employee-facing Assistant
```

Create specialist Profiles only when actual work, knowledge, tool, credential, automation, model, memory, or risk boundaries justify them.

### Profile is not a sandbox

Hermes Profile isolation separates Hermes state; it does not automatically restrict host filesystem, terminal, Docker, Git, browser, or external CLI credentials.

Security requires human RBAC plus least-privilege Profile capabilities and, where needed, OS/container/workspace isolation.

### Knowledge is not memory

Durable company facts belong in WeKnora. Do not duplicate product specifications, policies, or SOPs into every Profile memory/SOUL.

### Employee portal is not admin console

Open WebUI is the baseline employee multi-user surface. hermes-webui is an administrative surface and must not be exposed as the ordinary employee portal.

### Provider credential is not human authority

A mailbox, API, or service credential proves access to a provider. It does not prove which employee requested or approved an operation.

Governed external actions that require human authority must preserve trusted human identity/approval evidence separately from provider credentials.

### Prototype is not deployment

A repository prototype can be useful design evidence without being installed, enabled, authorized, or even selected for the final installation blueprint.

Passing offline tests proves only the tested design/prototype property. It does not advance the blueprint lifecycle and does not activate a real deployment task.

### Installation blueprint is not a live installation

Scripts, adapters, Compose files, configuration templates, acceptance contracts, and deployment playbooks may be authored and validated as repository artifacts. Their existence means the blueprint is becoming more installable; it does not mean any real company instance is being changed.

## 6. Deployment readiness rule

This section applies to an explicitly approved blueprint-validation target or an explicitly activated real deployment task, not merely because the repository is in installation-design work.

Every real/validation deployment must have an explicit target readiness from its company/validation configuration:

```text
core-ready
configured-ready
production-ready
```

Use `docs/COMPLETENESS.md` for semantics.

An explicitly authorized deployment request should drive the target to the requested readiness level without repeated human reminders about routine deployment phases.

Do not stop at `CORE READY` when the configured target is `CONFIGURED READY` or `PRODUCTION READY`.

During an authorized deployment, stop for human input only when execution genuinely requires external authority or information, such as:

- missing protected credentials;
- mailbox/provider authorization;
- OS permission requiring human approval;
- unresolved destructive conflict;
- identity-provider/application registration;
- messaging-platform application credentials;
- an actual company business choice absent from configuration.

Do not pause merely to ask whether to perform a defined deployment phase, configure baseline RBAC, connect components, implement an already-enabled capability, run acceptance, or record state.

This deployment-momentum rule must never be used to advance the blueprint lifecycle or activate a real deployment task.

## 7. Capability closure rule

During system/installation design, use `config/capabilities.yaml` to ensure the blueprint has a coherent path from capability intent to installation and acceptance. This is repository-design work and needs no real credential.

For every capability that the blueprint supports, resolve where applicable:

```text
capability intent
→ upstream/native mechanism
→ installation playbook/adapter
→ company-private inputs required at deployment time
→ security boundary
→ acceptance test
→ deployment-state evidence
```

During a real deployment, derive the exact enabled capability set from the active private company configuration and `config/capabilities.yaml`.

An enabled capability must not be silently omitted, disabled, replaced, or deferred merely to reach a green result during an authorized deployment.

If it cannot be completed safely because genuine external input/authority is unavailable, report:

```text
BLOCKED — REQUIRED INPUT: <specific input>
```

If its implementation or acceptance fails, report the specific failed boundary.

Disabled capabilities are not deployment debt and must not be enabled for completeness.

### v2 staged installation blueprint

`docs/V2-IMPLEMENTATION-PLAN.md` describes the intended future installation/deployment sequence for v2.

While the blueprint lifecycle remains `system_design`, that sequence helps identify installation requirements but must not pull the project prematurely into installation-design work.

When the human advances the blueprint lifecycle to `installation_design`, the repository may design and build the scripts/configuration/playbooks needed for this sequence without touching a real provider:

```text
Stage 0  preserve/verify v1 baseline
Stage 1  bounded read-only email
Stage 2  DraftReply preparation
Stage 3  trusted human approval evidence
Stage 4  governed send_approved_reply
Stage 5  optional simple follow-up
Stage 6  optional one messaging surface
```

Real provider/runtime acceptance inside those stages occurs only on an explicitly approved validation target or real deployment target.

Customer-facing send remains unavailable until the trusted-human approval design and later runtime acceptance both pass on an authorized target.

## 8. Default deployment posture

The first validated core reference path is:

```text
Host OS
└── Hermes Agent

Containers
├── WeKnora
└── Open WebUI
```

On the validated Apple Silicon macOS path, Hermes remains host-native. Optional administrative, coding, automation, messaging, identity, access, and operational integration capabilities are added only when selected by company configuration during a real deployment, while the repository may contain installation-blueprint artifacts for them beforehand.

## 9. Upstream-first rule

For design and installation choices use this order:

1. official upstream capability;
2. official extension/integration mechanism;
3. configuration;
4. thin repository adapter/playbook;
5. custom infrastructure only when the prior choices cannot solve a real requirement.

Do not fork WeKnora, Hermes Agent, Open WebUI, or hermes-webui by default.

For an optional capability not present in the first validated demo, inspect the exact selected upstream release before freezing its installation path and re-check at real deployment time where version drift matters.

Prototype code is not architecture authority. Re-check upstream capability during installation design and real deployment, and keep a local prototype only when it remains the smallest correct implementation.

## 10. No feature-collection architecture

Do not add a component merely because it exists, is popular, or has a template here.

Before introducing a new major component, establish:

- concrete business problem;
- why current stack/native capability is insufficient;
- expected benefit;
- operational cost;
- failure modes;
- security/data boundary;
- backup/restore impact;
- removal/rollback path.

If the justification is weak, use `Not now`.

## 11. Configuration minimality and clean-state rule

Design deployments from actual company requirements, not from every example, template, reference role, optional integration, or previously tested capability.

Repository templates/playbooks are a library and installation contract, not a mandate to install every capability.

Normative documentation should describe the intended current state cleanly. Do not preserve obsolete decisions as permanent negative rules or explanatory scars unless history is operationally necessary for safety, migration, compatibility, rollback, or incident response.

Prefer one positive general rule over a growing list of prohibitions against individual past mistakes.

## 12. Do not under-engineer

Minimality does not mean omitting a capability, security boundary, acceptance test, or production control required by the blueprint or by an adopting company's requested readiness.

For repository development, build the smallest blueprint that completely explains the approved system and how to install it.

For a real deployment, build the smallest system that completely satisfies the configured target.

## 13. Version discipline

Do not blindly track floating `main` / `latest` tags for reproducible installation blueprints or deployments.

For the validated core path, prefer `config/validated-stack.yaml` unless the task explicitly includes upgrade qualification.

When changing/selecting versions:

- inspect the official upstream release/source;
- review breaking changes;
- verify compatibility with the requested capability;
- pin the tested version/commit where practical;
- update the installation blueprint when commands/configuration change;
- record deployed reality in deployment-specific state when a real deployment exists.

Do not silently combine ordinary deployment with an unrequested major upgrade.

## 14. Pre-change inspection

Before modifying an existing real deployment in an explicitly activated deployment task:

1. inspect repository status;
2. read actual deployment state;
3. inspect running services/containers;
4. inspect Hermes and Profiles;
5. identify secret/config locations without printing secrets;
6. check backup freshness before risky changes;
7. reconcile documentation with runtime reality.

Actual runtime is evidence of what exists; desired company config defines what should exist. Blueprint design does not require inspecting or mutating a live runtime merely because this checklist exists.

## 15. Change risk classes

### Low risk

Examples: repository documentation corrections, synthetic fixture changes, non-security blueprint wording; or low-impact runtime changes inside an explicitly authorized deployment task.

Flow:

```text
inspect → change → verify → record if material
```

### High risk

Examples: embedding-model change, database/storage migration, core major upgrade, Profile privilege expansion, sensitive RBAC change, destructive knowledge operation, enabling a provider credential with new external data/write authority.

Flow during a real deployment:

```text
inspect → backup → plan → change → verify → rollback if needed → record
```

A risk class never activates a real deployment task by itself.

## 16. Secrets and public-repository privacy rules

Never commit or expose:

- production `.env` credentials;
- API keys;
- database/cache passwords;
- mailbox/client-specific passwords;
- OAuth/client secrets;
- messaging tokens;
- SSH private keys;
- cloud credentials;
- model-provider credentials;
- real employee or personal email addresses used as deployment identifiers;
- real employee phone numbers or private account identifiers;
- customer-private identities or contact details used merely as examples/test fixtures.

Public documentation, examples, fixtures, and tests must use synthetic identifiers such as `example.invalid` unless an identifier is intentionally public organizational contact information and its inclusion is explicitly approved.

Real deployment identifiers belong in private company configuration/runtime state, not this public repository.

Protected values belong in approved secret storage/runtime locations with restrictive permissions.

## 17. Tool privilege rules

Normal employee Profiles default to no unrestricted:

- terminal;
- filesystem writes;
- Docker/system control;
- GitHub administration;
- Codex/Claude Code delegation;
- raw credential access;
- generic provider/admin mutation primitives.

Grant stronger capabilities only to roles whose declared work requires them, with explicit workspace, provider, data, and credential boundaries.

## 18. Knowledge access rule

Hermes should access WeKnora through supported MCP/API surfaces, not direct database coupling.

Prefer direct read-oriented retrieval for straightforward knowledge work. Add another reasoning layer only when it solves a measured requirement.

Operational email/provider data is not automatically authoritative company knowledge and must not be bulk-copied into WeKnora merely to simplify access.

## 19. User/Profile mapping rule

Human identity lives in Open WebUI or the selected enterprise identity/messaging surface. AI work roles live in Hermes Profiles.

```text
Employee group → permitted Assistant → matching Hermes Profile
```

Baseline employee Profile is `general`. Add specialist mappings only for configured real roles.

UI visibility is not a security boundary by itself; the installation/acceptance blueprint must define direct unauthorized-access tests, and real deployment acceptance must execute them.

## 20. Memory safety rule

Shared Profile memory must not become an uncontrolled cross-user private-data channel.

Keep employee Hermes long-term memory disabled in the blueprint baseline unless the exact selected user/session-scoping mechanism has a defined two-user isolation acceptance path and has been validated before production use.

Open WebUI conversation history is independent and may remain enabled.

## 21. Destructive operations

Do not perform destructive operations based on inference alone.

Explicit intent and appropriate backup are required for operations such as deleting production Knowledge Bases, Profiles, persistent volumes/databases, backup generations, unknown Git work, irreversible migrations, or destructive provider operations.

A generic continuation instruction never constitutes destructive or real-deployment authority.

## 22. Documentation synchronization

When architecture, blueprint phase, installation design, Profile policy, RBAC, network exposure, backup, upgrade behavior, capability registry, upstream integration, Ontology operation contract, or deployment semantics change materially, update the corresponding documentation/registry in the same change.

For a blueprint-phase transition, update `state/PROJECT-PHASE.yaml` first and then synchronize `docs/V2-PHASE-STATUS.md` and any phase-dependent wording.

For a real deployment, record instance-specific reality outside public examples according to the deployment-state/privacy contract.

Do not allow runtime reality, blueprint authority, or machine-readable capability contracts to drift silently from prose standards.

## 23. Completion semantics

Keep blueprint completion separate from deployed-system readiness.

### Blueprint milestones

```text
SYSTEM DESIGN COMPLETE
INSTALLATION DESIGN COMPLETE
BLUEPRINT VALIDATED
RELEASE READY
```

These describe repository maturity.

### Deployed-system readiness

```text
CORE READY
CONFIGURED READY
PRODUCTION READY
```

These describe an explicitly approved validation/deployment target.

#### Core Ready

Core employee path and Part A acceptance pass.

#### Configured Ready

Core Ready remains PASS and every company-enabled conditional capability in `config/capabilities.yaml` is implemented, secured, accepted, and recorded.

#### Production Ready

Configured Ready remains PASS and applicable production recovery, security, access, secrets, knowledge, and operations controls pass Part C acceptance.

Never use vague `complete` without naming which maturity/readiness class was achieved.

Do not confuse `SYSTEM DESIGN COMPLETE` or `INSTALLATION DESIGN COMPLETE` with `CORE READY`, `CONFIGURED READY`, or `PRODUCTION READY`.

## 24. Acceptance discipline

During system design, acceptance criteria may be authored and offline/static tests may be executed to validate design assumptions.

During installation design, acceptance contracts, test harnesses, synthetic fixtures, and installation checks may be authored without activating real providers.

During blueprint validation, execute the appropriate installation and acceptance path only on the explicitly approved validation target.

During a real deployment, use `docs/ACCEPTANCE-TESTS.md` and provider-specific acceptance documents according to actual enabled capabilities.

Do not instantiate an optional feature merely to satisfy a test section. Conversely, do not skip the test for a capability that the company configuration enabled during a real deployment.

Runtime evidence matters more than configuration intent once an authorized target exists: test the real/validation employee client, actual MCP retrieval, actual authorization boundary, actual provider behavior for enabled operational integrations, actual harmless Cron/Kanban/coding run when enabled, and actual restore when the target requires Production Ready.

Offline/unit tests are necessary where defined but do not replace target runtime acceptance, and they do not activate a target by themselves.

## 25. Upstream mismatch rule

If a repository command/config field no longer matches the selected upstream release:

1. verify official upstream documentation/source;
2. find the closest supported equivalent;
3. preserve this repository's architecture/security intent;
4. make the smallest compatible adjustment;
5. update the relevant blueprint adapter/playbook;
6. record deployed reality when applicable.

Do not reinterpret implementation drift as permission to redesign the system, advance the blueprint lifecycle, or activate a real deployment.

## 26. Final operating principle

Develop the smallest **system blueprint + installation blueprint** that completely explains the approved Enterprise AI Office using mature upstream capabilities.

When a real deployment is explicitly requested, use that blueprint to build the smallest system that completely satisfies the adopting company's configured target.

Do not over-engineer.
Do not under-engineer.
Do not silently redesign.
Do not silently downgrade enabled capabilities.
Do not infer blueprint transitions or real deployment from momentum or continuation wording.
Verify before declaring either blueprint maturity or deployment readiness.
