# AGENTS.md — Enterprise AI Office Agent Operating Contract

This repository is intentionally designed to be read and maintained by AI engineering agents as well as humans.

If you are an AI agent asked to deploy, modify, debug, upgrade, or extend Enterprise AI Office, this file is the highest-priority repository-local operating contract.

## 1. Mission

Enterprise AI Office is a reusable blueprint and implementation framework for building a self-hosted enterprise AI workspace around:

- WeKnora for enterprise knowledge;
- Hermes Agent for the primary agent runtime;
- Open WebUI for multi-user employee Web access;
- hermes-webui for Hermes administration;
- Codex and Claude Code for specialized software-engineering execution;
- MCP as the preferred integration boundary;
- Hermes Profiles, Skills, Kanban, Cron, Bot Mode, and Gateway for role-based work, automation, and messaging.

ARMOR is the first reference implementation. Do not treat ARMOR-specific values as universal defaults.

## 2. Required reading order

Before making any material change, read in this order:

1. `README.md`
2. `AGENTS.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DEPLOYMENT.md`
5. `docs/SECURITY.md`
6. `docs/PROFILE-STANDARD.md`
7. `docs/KNOWLEDGE.md`
8. `docs/CLIENT-RBAC.md`
9. `docs/BACKUP-RESTORE.md`
10. `docs/UPGRADE.md`
11. `docs/ACCEPTANCE-TESTS.md`
12. `state/DEPLOYMENT-STATE.md` when operating an existing deployment
13. `state/CHANGELOG.md` when changing an existing deployment
14. the relevant company/reference implementation under `reference/`

If a referenced file does not exist yet, do not invent its contents silently. Record the gap and create it only when it is part of the requested work.

## 3. Frozen architecture intent

Do not silently replace the approved v1 architecture.

Current core roles are:

| Responsibility | Default component |
| --- | --- |
| Enterprise knowledge | WeKnora |
| Primary agent runtime | Hermes Agent |
| Employee Web client | Open WebUI |
| Hermes administrative client | hermes-webui |
| Role / department agents | Hermes Profiles |
| Knowledge bridge | WeKnora MCP / supported API |
| Durable agent work | Hermes Kanban |
| Scheduled automation | Hermes Cron |
| Coding execution | Codex + Claude Code |
| Messaging access | Hermes Gateway |
| Deployment truth | this repository + `state/DEPLOYMENT-STATE.md` |

Implementation details may change to match current upstream releases. Component responsibility and security boundaries may not be changed without an explicit architecture decision.

## 4. Source-of-truth rules

Do not let multiple systems become authoritative for the same class of information.

- Company knowledge: WeKnora.
- Agent identity / behavior: Hermes Profile configuration, SOUL, Skills, Tools, MCP.
- Human user identity and employee Web access: Open WebUI.
- Durable agent task state: Hermes Kanban.
- Scheduled agent work: Hermes Cron.
- Deployment configuration and operational history: this repository and deployment state files.
- ARMOR `armor-memory`: independent from this project unless a later approved integration is documented.

## 5. Critical conceptual boundaries

### Profile is not a user

A Hermes Profile is an AI role or specialist, not an employee account.

Do not create one Profile per employee by default.

### Profile is not a sandbox

Hermes Profile isolation separates Hermes state. It does not automatically restrict host filesystem, shell, Docker, Git, browser, or credential access.

Security requires both human RBAC and least-privilege Profile tools/credentials.

### Knowledge is not memory

Durable company facts belong in WeKnora. Do not duplicate product specifications, company policy, or other authoritative facts into every Profile memory.

### Employee portal is not admin console

Open WebUI is the employee-facing multi-user surface. hermes-webui is an administrative control surface and must not be exposed as the normal employee client.

## 6. Default deployment posture

The initial reference deployment is:

```text
Host OS
├── Hermes Agent
├── Codex
└── Claude Code

Containers
├── WeKnora
└── Open WebUI
```

Hermes stays host-native initially because controlled engineering Profiles may need local Git, repositories, Codex, Claude Code, and host tools.

Do not containerize Hermes merely for aesthetic consistency if doing so makes coding/runtime integration harder.

## 7. Upstream-first rule

For every implementation choice, use this order:

1. existing official upstream capability;
2. official extension or integration mechanism;
3. configuration;
4. thin adapter;
5. custom infrastructure only when the previous options cannot solve a real requirement.

Do not fork WeKnora, Hermes Agent, Open WebUI, or hermes-webui by default.

## 8. No feature-collection architecture

Do not add a component merely because it exists or is popular.

Before introducing a major new component such as LiteLLM, Dify, n8n, LangGraph, Qdrant, Neo4j, another Web UI, another auth proxy, or a synchronization service, document:

- the concrete business problem;
- why the current stack cannot solve it;
- expected benefit;
- new operational cost;
- new failure modes;
- new security/data boundary;
- backup/restore requirements;
- removal/rollback path.

If the justification is weak, default to `Not now`.

## 9. Configuration minimality and clean-state rule

Build each deployment from the adopting company's actual requirements, not from every example, template, reference role, optional integration, or previously tested capability present in this repository.

Repository templates are a library, not a deployment checklist. Instantiate an optional Profile, group, Knowledge Base, Skill, integration, automation, or service only when the company configuration or a real operating requirement justifies it.

When correcting or simplifying the design, make the maintained documentation describe the intended current state cleanly. Do not preserve obsolete decisions as permanent negative rules, explanatory scars, or special-case warnings unless the historical fact is itself operationally necessary for safety, migration, compatibility, rollback, or incident response.

Prefer a general positive rule that prevents a class of mistakes over a growing list of prohibitions against individual past mistakes. Git history and deployment changelogs carry history when history is needed; normative architecture and configuration documents should primarily describe how the system is meant to work now.

## 10. Do not over-minimize either

Do not remove useful production foundations merely to make the stack look smaller.

PostgreSQL, Redis, RBAC, backups, hybrid retrieval, reranking, and other mature upstream components should remain when they solve real operational needs.

## 11. Version discipline

Production must not blindly track floating `main` / `latest` tags.

For each core component:

- inspect the current stable upstream release;
- review release notes and breaking changes;
- pin the tested version or exact commit where practical;
- record the deployed version in `state/DEPLOYMENT-STATE.md`.

Do not enable unattended automatic upgrades for production core components.

## 12. Pre-change inspection

Before modifying an existing deployment:

1. inspect repository status;
2. read `state/DEPLOYMENT-STATE.md`;
3. inspect running Docker services;
4. inspect Hermes status and Profiles;
5. confirm current upstream versions;
6. identify secrets/config locations without printing secrets;
7. check backup freshness for risky changes.

Do not assume the machine matches the documentation. Reconcile documentation with reality first.

## 13. Change risk classes

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

## 14. Secrets rules

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

## 15. Tool privilege rules

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

## 16. Knowledge access rule

Hermes should access WeKnora through supported MCP/API surfaces.

Do not couple Hermes directly to WeKnora's PostgreSQL schema.

Do not make WeKnora Agent an unnecessary extra reasoning hop for every knowledge lookup. Prefer direct retrieval tools for straightforward knowledge access.

## 17. User / Profile mapping rule

Employee identity lives in Open WebUI or the enterprise messaging platform.

AI work roles live in Hermes Profiles.

Typical mapping:

```text
Employee group → permitted Assistant → matching Hermes Profile
```

The baseline employee-facing Profile is `general`. Add specialist mappings only for roles the adopting company actually uses.

Do not confuse UI visibility with security. Verify direct unauthorized access is blocked.

## 18. Memory safety rule

Shared department Profile memory must never become an uncontrolled cross-user private-data channel.

Before enabling employee long-term memory, run the cross-user isolation tests in `docs/ACCEPTANCE-TESTS.md`.

If isolation cannot be proven, disable employee long-term memory and rely on per-user conversation history until a safe mechanism is validated.

## 19. Destructive operations

Do not perform destructive operations based on inference alone.

Examples requiring explicit intent and appropriate backup:

- deleting a production Knowledge Base;
- deleting Hermes Profiles;
- deleting Docker volumes;
- resetting databases;
- deleting backup generations;
- hard-resetting unknown Git changes;
- `docker system prune -a` on a production host;
- irreversible storage migration.

## 20. Reboot and recovery requirement

A deployment is not considered complete until it survives a host reboot and restores required services, Profiles, knowledge access, schedules, and employee access.

## 21. Documentation synchronization

If you materially change architecture, deployment, Profile policy, RBAC, network exposure, backup, upgrade behavior, or upstream integration, update the corresponding documentation in the same change.

Do not allow production reality to drift silently away from repository documentation.

## 22. Completion standard

Never declare the system complete merely because containers started.

Use `docs/ACCEPTANCE-TESTS.md`.

At minimum verify the capabilities that are enabled for that deployment, including:

- knowledge ingestion and retrieval;
- citations;
- Hermes Profile routing;
- per-Profile API-key isolation;
- Open WebUI RBAC;
- cross-user memory isolation or deliberate memory disablement;
- least-privilege tools;
- Codex / Claude Code delegation where enabled;
- Kanban persistence where enabled;
- Cron execution where enabled;
- backup and restore;
- host reboot recovery.

Do not add optional capabilities merely to satisfy an acceptance checklist; tests follow the configured system, not the other way around.

## 23. When documentation conflicts with current upstream behavior

Upstream projects evolve quickly.

If a command, API path, configuration field, or deployment mechanism in this repository is outdated:

1. verify the current official upstream documentation/source;
2. find the closest supported equivalent;
3. preserve this repository's architectural intent and security boundary;
4. implement the smallest compatible adjustment;
5. update the relevant documentation;
6. record the deployed reality in `state/DEPLOYMENT-STATE.md`.

Do not reinterpret an implementation mismatch as permission to redesign the system.

## 24. Final operating principle

Build the smallest system that completely solves the current requirement, using mature capabilities and preserving future evolution.

Do not over-engineer.
Do not under-engineer.
Do not silently redesign.
Verify before declaring success.
