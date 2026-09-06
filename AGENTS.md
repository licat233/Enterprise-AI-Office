# AGENTS.md — Enterprise AI Office Agent Operating Contract

This repository is intentionally designed to be read, deployed, and maintained by AI engineering agents as well as humans.

If you are an AI agent asked to deploy, modify, debug, upgrade, or extend Enterprise AI Office, this file is the highest-priority repository-local operating contract.

## 1. Mission

Enterprise AI Office is a reusable blueprint and implementation framework for building a self-hosted enterprise AI workspace around:

- WeKnora for enterprise knowledge;
- Hermes Agent for the primary agent runtime;
- Open WebUI for multi-user employee Web access;
- hermes-webui for Hermes administration when enabled;
- Codex and Claude Code for specialized software-engineering execution when enabled;
- MCP as the preferred integration boundary;
- Hermes Profiles, Skills, Kanban, Cron, Bot Mode, and Gateway where the adopting company actually needs them.

ARMOR is the first reference implementation. Company/reference material is evidence and example, not a universal deployment default.

## 2. Authority and required reading

Before making a material change, read the documents relevant to the task in this order:

1. `README.md`
2. `AGENTS.md`
3. `state/PROJECT-PHASE.yaml`
4. `DEPLOY.md` only for deployment or deployment planning that the phase gate permits
5. `docs/COMPLETENESS.md` for readiness/completion semantics
6. `config/company.example.yaml` or the real company-private configuration
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

### Project phase gate — interpret before acting

`state/PROJECT-PHASE.yaml` is the sole repository authority for the current **work phase** and its authorization boundary.

Do not infer phase from:

- repository momentum;
- previous assistant assumptions;
- prototype/adaptor code existing;
- tests passing;
- an implementation plan existing;
- deployment documents existing;
- acceptance contracts existing;
- a provider having been selected;
- phrases such as `continue`, `keep going`, `start`, `begin`, `next`, `proceed`, `继续`, `开始`, `开始吧`, `下一步`, or `好的`.

Continuation language means:

> **Continue valid work inside the current phase.**

It does not authorize a phase transition.

A transition from design to implementation/deployment requires explicit human intent that the phase itself is changing. The examples in `state/PROJECT-PHASE.yaml` are illustrative; the decisive property is explicit phase-changing intent, not any exact magic phrase.

When the phase is `design`:

```text
allowed
→ research
→ architecture/product design
→ documentation
→ threat/authorization modeling
→ Ontology/schema work
→ sanitized examples / synthetic fixtures
→ offline prototypes
→ offline tests/static validation
→ future implementation planning
→ acceptance-test design

not authorized
→ real credentials
→ real personal/employee identifiers in the public repository
→ real provider/mailbox/business-system access
→ real employee/Profile/provider binding
→ real IMAP/SMTP runtime
→ production/live runtime mutation
→ customer-facing actions
```

Missing runtime credentials are not blockers during design because runtime access is outside the current phase.

If the next apparent step would cross the phase boundary, do not perform it and do not ask for credentials merely to maintain momentum. Continue with the closest valid work inside the current phase or explain that the remaining step belongs to a future phase.

When the task is part of the current v2 Communication & Follow-up milestone, also read before mutation:

```text
docs/V2-SCOPE.md
docs/V2-DESIGN-REVIEW.md
docs/V2-PHASE-STATUS.md
docs/V2-IMPLEMENTATION-PLAN.md
```

Read the phase status before treating the implementation plan as executable. The implementation plan is future architecture while `state/PROJECT-PHASE.yaml` remains `phase: design`.

For v2 email work, additionally read the concrete provider capability paths referenced by `config/capabilities.yaml`, treating them as design-support prototypes or implementation artifacts according to the current phase.

For an authorized deployment task, `DEPLOY.md` is the execution contract. `docs/COMPLETENESS.md` defines what readiness means. `config/capabilities.yaml` maps enabled capabilities to implementation and acceptance paths.

The root-level ARMOR v1 design document and content under `reference/` are non-normative reference material. They must not override `AGENTS.md`, `state/PROJECT-PHASE.yaml`, `DEPLOY.md`, current generic standards, the adopting company's active configuration, or actual runtime state.

If a referenced implementation artifact is missing for an enabled capability during an authorized implementation/deployment phase, treat that as a repository deployability defect. Do not silently invent a different architecture.

## 3. Frozen architecture intent

Do not silently replace the approved architecture.

| Responsibility | Default component |
| --- | --- |
| Current work phase | `state/PROJECT-PHASE.yaml` |
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
| Deployment truth | active company config + this repository + actual runtime/deployment state |

Implementation details may change to match selected upstream releases. Component responsibilities and security boundaries may not change without an explicit architecture decision.

## 4. Source-of-truth rules

Do not let multiple systems become authoritative for the same information class.

- Current project work phase: `state/PROJECT-PHASE.yaml`.
- Company knowledge: WeKnora.
- Agent identity/behavior: Hermes Profile configuration, SOUL, Skills, Tools, MCP.
- Human identity and employee Web access: Open WebUI or the explicitly selected enterprise identity layer.
- External operational business state: the selected provider/System of Record.
- Enterprise AI Office-owned approval/draft/governance evidence: only where an approved capability/Ontology contract explicitly defines it.
- Durable agent task state: Hermes Kanban when enabled.
- Scheduled agent work: Hermes Cron when enabled.
- Desired deployment state: active company deployment configuration.
- Actual deployment state: real runtime + `state/DEPLOYMENT-STATE.md`.
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

### Prototype is not implementation

A repository prototype can be useful design evidence without being deployed, enabled, authorized, or even selected for final implementation.

Passing offline tests proves only the tested design/prototype property. It does not change the project phase and does not authorize runtime acceptance.

## 6. Deployment readiness rule

This section applies only after `state/PROJECT-PHASE.yaml` authorizes implementation/deployment.

Every new deployment must have an explicit target readiness from company configuration:

```text
core-ready
configured-ready
production-ready
```

Use `docs/COMPLETENESS.md` for semantics.

An explicitly authorized deployment request should drive the system to the requested readiness level without repeated human reminders about routine phases.

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

This deployment momentum rule must never be used to cross a project phase boundary. During design, it does not authorize implementation or credential requests.

## 7. Capability closure rule

This section becomes executable for real runtime capability closure only when the phase gate authorizes implementation/deployment.

Before mutation, derive the exact enabled capability set from the active company configuration and `config/capabilities.yaml`.

For every enabled capability resolve:

```text
requested state
→ implementation playbook/adapter
→ exact upstream behavior/version
→ required protected inputs
→ security boundary
→ acceptance test
→ deployment-state fields
```

An enabled capability must not be silently omitted, disabled, replaced, or deferred merely to reach a green result during an authorized implementation/deployment.

If it cannot be completed safely because genuine external input/authority is unavailable, report:

```text
BLOCKED — REQUIRED INPUT: <specific input>
```

If its implementation or acceptance fails, report the specific failed boundary.

Disabled capabilities are not deployment debt and must not be enabled for completeness.

### v2 future staged implementation gate

`docs/V2-IMPLEMENTATION-PLAN.md` defines the future order **after** implementation is explicitly authorized.

While `state/PROJECT-PHASE.yaml` remains `phase: design`, the sequence below is planning information only and must not be executed against a real provider:

```text
Stage 1 read-only email
→ deterministic adapter tests
→ bounded real runtime acceptance
→ READ-ONLY EMAIL PASS
→ only then Stage 2 draft implementation
```

The existence of Stage 1 prototype code or passing offline tests does not move the project into Stage 1 runtime work.

Customer-facing send remains unavailable until the future trusted-human approval stage passes and the governed send action is accepted.

Do not create SMTP/send capability as a convenience while the phase gate does not authorize implementation or while the future Stage 1 runtime boundary remains unresolved.

## 8. Default deployment posture

The first validated core reference path is:

```text
Host OS
└── Hermes Agent

Containers
├── WeKnora
└── Open WebUI
```

On the validated Apple Silicon macOS path, Hermes remains host-native. Optional administrative, coding, automation, messaging, identity, access, and operational integration capabilities are added only when selected by company configuration during an authorized implementation/deployment.

## 9. Upstream-first rule

For implementation choices use this order:

1. official upstream capability;
2. official extension/integration mechanism;
3. configuration;
4. thin repository adapter/playbook;
5. custom infrastructure only when the prior choices cannot solve a real requirement.

Do not fork WeKnora, Hermes Agent, Open WebUI, or hermes-webui by default.

For an optional capability not present in the first validated demo, inspect the exact selected upstream release before activation and record its version/commit where practical.

Prototype code is not architecture authority. Re-check upstream capability at actual implementation time and keep a local prototype only when it remains the smallest correct implementation.

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

Build each deployment from actual company requirements, not from every example, template, reference role, optional integration, or previously tested capability.

Repository templates/playbooks are a library, not a deployment checklist.

Normative documentation should describe the intended current state cleanly. Do not preserve obsolete decisions as permanent negative rules or explanatory scars unless history is operationally necessary for safety, migration, compatibility, rollback, or incident response.

Prefer one positive general rule over a growing list of prohibitions against individual past mistakes.

## 12. Do not under-engineer

Minimality does not mean omitting a company-enabled capability, security boundary, acceptance test, or production control required by the requested readiness level once implementation/deployment is authorized.

Build the smallest system that completely satisfies the configured target inside the current authorized phase.

## 13. Version discipline

Do not blindly track floating `main` / `latest` tags for reproducible deployments.

For the validated core path, prefer `config/validated-stack.yaml` unless the task explicitly includes upgrade qualification.

When changing/selecting versions:

- inspect the official upstream release/source;
- review breaking changes;
- verify compatibility with the requested capability;
- pin the tested version/commit where practical;
- record deployed reality in `state/DEPLOYMENT-STATE.md` when runtime deployment exists.

Do not silently combine ordinary deployment with an unrequested major upgrade.

## 14. Pre-change inspection

Before modifying an existing deployment in an authorized implementation/deployment phase:

1. inspect repository status;
2. read actual deployment state;
3. inspect running services/containers;
4. inspect Hermes and Profiles;
5. identify secret/config locations without printing secrets;
6. check backup freshness before risky changes;
7. reconcile documentation with runtime reality.

Actual runtime is evidence of what exists; desired company config defines what should exist. During design, do not inspect or mutate live runtime merely because this checklist exists.

## 15. Change risk classes

### Low risk

Examples: documentation corrections, non-security SOUL wording, non-privileged Skill additions, normal employee account changes during an authorized runtime phase.

Flow:

```text
inspect → change → verify → record if material
```

### High risk

Examples: embedding-model change, database/storage migration, core major upgrade, Profile privilege expansion, sensitive RBAC change, destructive knowledge operation, enabling a provider credential with new external data/write authority.

Flow:

```text
inspect → backup → plan → change → verify → rollback if needed → record
```

The phase gate precedes both risk classes. A low-risk runtime change is still not authorized during a design-only phase.

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

UI visibility is not a security boundary by itself; verify direct unauthorized access fails during the authorized runtime acceptance phase.

## 20. Memory safety rule

Shared Profile memory must not become an uncontrolled cross-user private-data channel.

Keep employee Hermes long-term memory disabled unless the exact deployed user/session-scoping mechanism passes the cross-user isolation tests in `docs/ACCEPTANCE-TESTS.md`.

Open WebUI conversation history is independent and may remain enabled.

## 21. Destructive operations

Do not perform destructive operations based on inference alone.

Explicit intent and appropriate backup are required for operations such as deleting production Knowledge Bases, Profiles, persistent volumes/databases, backup generations, unknown Git work, irreversible migrations, or destructive provider operations.

A generic continuation instruction never constitutes destructive or phase-transition authority.

## 22. Documentation synchronization

When architecture, project phase, deployment, Profile policy, RBAC, network exposure, backup, upgrade behavior, capability registry, upstream integration, Ontology operation contract, or current v2 phase changes materially, update the corresponding documentation/registry in the same change.

For a phase transition, update `state/PROJECT-PHASE.yaml` first and then synchronize `docs/V2-PHASE-STATUS.md` and any phase-dependent wording.

Do not allow runtime reality, phase authority, or machine-readable capability contracts to drift silently from prose standards.

## 23. Completion semantics

These readiness semantics describe deployed systems and become actionable only when implementation/deployment is authorized.

### Core Ready

Core employee path and Part A acceptance pass.

### Configured Ready

Core Ready remains PASS and every company-enabled conditional capability in `config/capabilities.yaml` is implemented, secured, accepted, and recorded.

### Production Ready

Configured Ready remains PASS and applicable production recovery, security, access, secrets, knowledge, and operations controls pass Part C acceptance.

Never use vague `complete` without naming the achieved readiness level.

Do not confuse `DESIGN COMPLETE` or a frozen design with `CORE READY`, `CONFIGURED READY`, or `PRODUCTION READY`.

## 24. Acceptance discipline

During design, acceptance documents may be authored and offline/static tests may be executed without activating providers.

During an authorized implementation/deployment, use `docs/ACCEPTANCE-TESTS.md` and provider-specific acceptance documents according to actual enabled capabilities.

Do not instantiate an optional feature to satisfy a test section. Conversely, do not skip the test for a capability that the company configuration enabled during an authorized implementation.

Runtime evidence matters more than configuration intent once runtime work is authorized: test the real employee client, actual MCP retrieval, actual authorization boundary, actual provider behavior for enabled operational integrations, actual harmless Cron/Kanban/coding run when enabled, and actual restore for Production Ready.

Offline/unit tests are necessary where defined but do not replace provider/runtime authorization tests, and they do not authorize those runtime tests.

## 25. Upstream mismatch rule

If a repository command/config field no longer matches the selected upstream release:

1. verify official upstream documentation/source;
2. find the closest supported equivalent;
3. preserve this repository's architecture/security intent;
4. make the smallest compatible adjustment;
5. update the relevant adapter/playbook;
6. record deployed reality when applicable.

Do not reinterpret implementation drift as permission to redesign the system or cross the current phase boundary.

## 26. Final operating principle

Build the smallest system that completely satisfies the configured company requirement and requested readiness level using mature upstream capabilities **inside the phase explicitly authorized by the human**.

Do not over-engineer.
Do not under-engineer.
Do not silently redesign.
Do not silently downgrade enabled capabilities.
Do not infer a phase transition from momentum or continuation wording.
Verify before declaring success.
