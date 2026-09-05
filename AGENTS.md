# AGENTS.md — Enterprise AI Office Agent Operating Contract

This repository is intentionally designed to be read and maintained by AI engineering agents as well as humans.

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

ARMOR is the first reference implementation. Do not treat ARMOR-specific values as universal defaults.

## 2. Required reading order

Before making any material change, read in this order:

1. `README.md`
2. `AGENTS.md`
3. `DEPLOY.md` when the task includes deployment or deployment planning
4. `docs/ARCHITECTURE.md`
5. `docs/DEPLOYMENT.md`
6. `docs/SECURITY.md`
7. `docs/PROFILE-STANDARD.md`
8. `docs/KNOWLEDGE.md`
9. `docs/CLIENT-RBAC.md`
10. `docs/BACKUP-RESTORE.md`
11. `docs/UPGRADE.md`
12. `docs/ACCEPTANCE-TESTS.md`
13. `state/DEPLOYMENT-STATE.md` when operating an existing deployment
14. `state/CHANGELOG.md` when changing an existing deployment
15. the relevant company/reference implementation under `reference/`

If a referenced file does not exist yet, do not invent its contents silently. Record the gap and create it only when it is part of the requested work.

For deployment tasks, `DEPLOY.md` is the execution contract. Detailed documents may add implementation detail but must not override its baseline target, phase order, or completion semantics.

## 3. Frozen architecture intent

Do not silently replace the approved architecture.

Current core responsibilities are:

| Responsibility | Default component |
| --- | --- |
| Enterprise knowledge | WeKnora |
| Primary agent runtime | Hermes Agent |
| Employee Web client | Open WebUI |
| Hermes administrative client | hermes-webui when enabled |
| AI work roles | Hermes Profiles |
| Knowledge bridge | WeKnora MCP / supported API |
| Durable agent work | Hermes Kanban when enabled |
| Scheduled automation | Hermes Cron when enabled |
| Coding execution | Codex + Claude Code when enabled |
| Messaging access | Hermes Gateway when enabled |
| Deployment truth | this repository + `state/DEPLOYMENT-STATE.md` |

Implementation details may change to match current upstream releases. Component responsibility and security boundaries may not be changed without an explicit architecture decision.

## 4. Source-of-truth rules

Do not let multiple systems become authoritative for the same class of information.

- Company knowledge: WeKnora.
- Agent identity / behavior: Hermes Profile configuration, SOUL, Skills, Tools, MCP.
- Human user identity and employee Web access: Open WebUI.
- Durable agent task state: Hermes Kanban when enabled.
- Scheduled agent work: Hermes Cron when enabled.
- Deployment configuration and operational history: this repository and deployment state files.
- ARMOR `armor-memory`: independent from this project unless a later approved integration is documented.

## 5. Critical conceptual boundaries

### Profile is not a user

A Hermes Profile is an AI role or specialist, not an employee account.

Do not create one Profile per employee by default.

### Core Profiles vs specialist Profiles

The baseline Profile model is:

```text
default/admin  → privileged control plane
general        → baseline employee-facing assistant
```

Additional specialist Profiles are opt-in and must be justified by actual company work, knowledge, tool, credential, automation, model, memory, or risk boundaries.

### Profile is not a sandbox

Hermes Profile isolation separates Hermes state. It does not automatically restrict host filesystem, shell, Docker, Git, browser, or credential access.

Security requires both human RBAC and least-privilege Profile tools/credentials.

### Knowledge is not memory

Durable company facts belong in WeKnora. Do not duplicate product specifications, company policy, or other authoritative facts into every Profile memory.

### Employee portal is not admin console

Open WebUI is the employee-facing multi-user surface. hermes-webui is an administrative control surface and must not be exposed as the normal employee client.

## 6. Deployment execution rule

For deployment work, follow `DEPLOY.md` from inspection through employee-client acceptance and deployment-state recording.

A single deployment request should normally drive the complete Core Ready workflow without repeated human reminders.

Stop for human input only when execution genuinely requires external authority or information, such as:

- missing credentials;
- OS permission requiring human approval;
- unresolved destructive conflict;
- a real company-specific business choice absent from configuration.

Do not pause merely to ask whether to perform an already-defined deployment phase, create baseline RBAC, connect the baseline components, run employee-client acceptance, or record deployment state.

## 7. Default deployment posture

The first validated Core Ready path is:

```text
Host OS
└── Hermes Agent

Containers
├── WeKnora
└── Open WebUI
```

On the validated Apple Silicon macOS path, Hermes remains host-native because controlled technical roles may later need local repositories, Git, Codex, Claude Code, and host tools.

Do not enable optional components merely because the repository documents them.

## 8. Upstream-first rule

For every implementation choice, use this order:

1. existing official upstream capability;
2. official extension or integration mechanism;
3. configuration;
4. thin adapter;
5. custom infrastructure only when the previous options cannot solve a real requirement.

Do not fork WeKnora, Hermes Agent, Open WebUI, or hermes-webui by default.

## 9. No feature-collection architecture

Do not add a component merely because it exists or is popular.

Before introducing a major new component, document:

- the concrete business problem;
- why the current stack cannot solve it;
- expected benefit;
- new operational cost;
- new failure modes;
- new security/data boundary;
- backup/restore requirements;
- removal/rollback path.

If the justification is weak, default to `Not now`.

## 10. Configuration minimality and clean-state rule

Build each deployment from the adopting company's actual requirements, not from every example, template, reference role, optional integration, or previously tested capability present in this repository.

Repository templates are a library, not a deployment checklist. Instantiate an optional Profile, group, Knowledge Base, Skill, integration, automation, or service only when the company configuration or a real operating requirement justifies it.

When correcting or simplifying the design, make maintained normative documentation describe the intended current state cleanly. Do not preserve obsolete decisions as permanent negative rules, explanatory scars, or special-case warnings unless the historical fact is operationally necessary for safety, migration, compatibility, rollback, or incident response.

Prefer a general positive rule that prevents a class of mistakes over a growing list of prohibitions against individual past mistakes. Git history and deployment changelogs carry history when history is needed.

## 11. Do not over-minimize either

Do not remove useful foundations merely to make the stack look smaller.

Keep mature upstream components when they solve a real requirement of the selected deployment.

## 12. Version discipline

Do not blindly track floating `main` / `latest` tags.

For a reproducible deployment, prefer the validated stack recorded by the Golden Path unless the task explicitly includes upgrade qualification.

When changing versions:

- inspect the current stable upstream release;
- review release notes and breaking changes;
- test compatibility;
- pin the tested version or exact commit where practical;
- record the deployed version in `state/DEPLOYMENT-STATE.md`.

Do not silently combine a deployment task with an unrequested major upgrade.

## 13. Pre-change inspection

Before modifying an existing deployment:

1. inspect repository status;
2. read `state/DEPLOYMENT-STATE.md`;
3. inspect running Docker services;
4. inspect Hermes status and Profiles;
5. identify secrets/config locations without printing secrets;
6. check backup freshness before risky changes.

Do not assume the machine matches the documentation. Reconcile documentation with reality first.

## 14. Change risk classes

### Low risk

Examples:

- documentation corrections;
- non-security SOUL wording;
- adding a non-privileged Skill;
- adding a normal employee account.

Flow: inspect → change → verify → record if material.

### High risk

Examples:

- embedding-model change;
- database migration;
- storage migration;
- core component major upgrade;
- Profile tool or credential privilege expansion;
- RBAC changes affecting sensitive roles;
- destructive knowledge operations.

Flow: inspect → backup → plan → change → verify → rollback if needed → document.

## 15. Secrets rules

Never commit:

- `.env` files containing credentials;
- API keys;
- DB passwords;
- Redis passwords;
- OAuth secrets;
- bot tokens;
- SSH private keys;
- cloud credentials;
- model-provider credentials.

Do not print full credentials in logs or final reports.

Templates must use placeholders.

## 16. Tool privilege rules

Normal employee Profiles must not receive unrestricted host capabilities by default.

Default-deny powerful capabilities such as:

- arbitrary terminal execution;
- unrestricted filesystem writes;
- Docker control;
- system configuration;
- GitHub administration;
- Codex / Claude Code delegation;
- raw credential access.

Grant powerful capabilities only to roles whose actual work requires them, with an explicit workspace and credential boundary.

## 17. Knowledge access rule

Hermes should access WeKnora through supported MCP/API surfaces.

Do not couple Hermes directly to WeKnora's PostgreSQL schema.

Prefer direct retrieval tools for straightforward knowledge access rather than adding an unnecessary reasoning hop.

## 18. User / Profile mapping rule

Employee identity lives in Open WebUI or the enterprise messaging platform.

AI work roles live in Hermes Profiles.

Typical mapping:

```text
Employee group → permitted Assistant → matching Hermes Profile
```

The baseline employee-facing Profile is `general`. Add specialist mappings only for roles the adopting company actually uses.

Do not confuse UI visibility with security. Verify direct unauthorized access is blocked.

## 19. Memory safety rule

Shared Profile memory must never become an uncontrolled cross-user private-data channel.

Before enabling employee long-term memory, run the cross-user isolation tests in `docs/ACCEPTANCE-TESTS.md`.

If isolation cannot be proven, disable employee long-term memory and rely on per-user conversation history until a safe mechanism is validated.

## 20. Destructive operations

Do not perform destructive operations based on inference alone.

Examples requiring explicit intent and appropriate backup include deleting production Knowledge Bases, Profiles, Docker volumes, databases, backup generations, unknown Git changes, or performing irreversible storage migrations.

## 21. Documentation synchronization

If you materially change architecture, deployment, Profile policy, RBAC, network exposure, backup, upgrade behavior, or upstream integration, update the corresponding documentation in the same change.

Do not allow runtime reality to drift silently away from repository documentation.

## 22. Completion semantics

### Core Ready

For a new baseline deployment, `CORE READY` means the enabled core employee workflow in `DEPLOY.md` passes end to end:

```text
employee login
→ permitted Assistant
→ Hermes Profile
→ WeKnora grounded answer + source
```

It also requires baseline RBAC, least-privilege tools, employee-client checks, and deployment-state recording.

### Production Ready

`PRODUCTION READY` is a higher bar and requires the production controls relevant to that deployment, such as backup/restore, startup/recovery, external access controls, production secrets, operational ownership, and any enabled optional integrations.

Do not block a bounded functional/demo task on unrelated optional production capabilities. Do not call a production deployment ready merely because it reached Core Ready.

## 23. Acceptance discipline

Use `docs/ACCEPTANCE-TESTS.md`, but run tests according to the capabilities actually enabled by the deployment.

At minimum for Core Ready verify:

- knowledge ingestion and retrieval;
- source evidence;
- Hermes `general` routing;
- employee Web RBAC;
- default/admin non-exposure;
- least-privilege tools;
- deliberate employee-memory disablement or proven isolation;
- real employee-client chat and history.

For optional capabilities such as specialist Profiles, Codex/Claude Code, Kanban, Cron, messaging, remote access, or long-term memory, run their acceptance sections only when they are enabled.

## 24. When documentation conflicts with current upstream behavior

Upstream projects evolve quickly.

If a command, API path, configuration field, or deployment mechanism in this repository is outdated:

1. verify the current official upstream documentation/source;
2. find the closest supported equivalent;
3. preserve this repository's architectural intent and security boundary;
4. implement the smallest compatible adjustment;
5. update the relevant documentation;
6. record deployed reality in `state/DEPLOYMENT-STATE.md`.

Do not reinterpret an implementation mismatch as permission to redesign the system.

## 25. Final operating principle

Build the smallest system that completely solves the current requirement, using mature capabilities and preserving future evolution.

Do not over-engineer.
Do not under-engineer.
Do not silently redesign.
Verify before declaring success.
