# Enterprise AI Office

> An agent-readable blueprint for building a self-hosted enterprise AI workspace with **WeKnora + Hermes Agent + Open WebUI + MCP**, with optional Codex, Claude Code, Kanban, Cron, messaging, and other role-specific capabilities.

Enterprise AI Office is a public architecture and implementation project for companies that want to build an internal AI office system around their own knowledge, roles, workflows, tools, and employees.

The long-term goal is practical:

> **A company should be able to give this repository to a capable AI engineering agent, provide the required company configuration and protected credentials, and have the agent deploy, configure, validate, operate, and safely evolve the system without repeated human reminders about routine implementation steps.**

ARMOR is the first reference implementation and validation environment. The project itself is intended to remain reusable by other companies.

## Deploy with an AI agent

If the task is to deploy or plan a deployment, start here:

1. [`AGENTS.md`](AGENTS.md) — highest-priority repository-local operating contract.
2. [`DEPLOY.md`](DEPLOY.md) — agent deployment Golden Path and completion semantics.
3. [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) — detailed implementation reference.
4. [`docs/ACCEPTANCE-TESTS.md`](docs/ACCEPTANCE-TESTS.md) — deeper validation for enabled capabilities.

The intended interaction is one deployment request, not a sequence of prompts reminding the agent to connect WeKnora, create the baseline Hermes Profile, configure Open WebUI RBAC, test the employee client, and record deployment state.

Human input is still expected when genuinely required for credentials, OS permissions, destructive conflicts, or company-specific business choices that are not present in configuration.

## What are we building?

Enterprise AI Office is an AI work layer for a company:

```text
Employee
   │
   ▼
Open WebUI / approved messaging surface
   │
   ▼
Hermes Agent
   │
   ├── WeKnora company knowledge
   ├── Role-specific Skills
   ├── Approved tools / MCP
   ├── Optional memory
   ├── Optional Kanban / Cron
   └── Optional specialist coding agents
```

The baseline employee workflow is:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes `general` Profile
→ WeKnora
→ grounded answer + source
```

## Reference architecture

| Layer | Technology | Responsibility |
| --- | --- | --- |
| Enterprise Knowledge | **WeKnora** | Document ingestion, retrieval, source evidence, enterprise knowledge |
| Primary Agent Runtime | **Hermes Agent** | Profiles, SOUL, Skills, tools, MCP, orchestration |
| Employee Web Client | **Open WebUI** | Users, groups, RBAC, chat interface, conversation history |
| Hermes Admin Client | **hermes-webui** | Administrative Hermes control surface when enabled |
| Role Architecture | **Hermes Profiles** | AI work roles with distinct behavior/capability boundaries |
| Knowledge Bridge | **WeKnora MCP / supported API** | Hermes-to-knowledge integration |
| Durable Agent Work | **Hermes Kanban** | Optional persistent multi-agent task coordination |
| Automation | **Hermes Cron** | Optional scheduled agent work |
| Coding Execution | **Codex + Claude Code** | Optional software-engineering execution |
| Messaging | **Hermes Gateway** | Optional enterprise messaging access |
| Operations & Governance | **This repository** | Architecture, deployment state, security, backup, upgrade, maintenance rules |

## Baseline vs optional capabilities

A baseline deployment starts with:

```text
Hermes control plane
└── default/admin Profile

Employee plane
├── Open WebUI
├── All-Employees group
├── General Assistant
└── Hermes `general` Profile

Knowledge
└── company-defined WeKnora Knowledge Base(s)
```

Specialist Profiles, department groups, additional Knowledge Bases, Skills, Codex/Claude Code delegation, Kanban, Cron, messaging, remote access, SSO, and employee Hermes long-term memory are added only when the adopting company's configuration or real operating requirements justify them.

Repository templates are a library, not a deployment checklist.

## Core design rules

### One responsibility, one authority

| Information | Authority |
| --- | --- |
| Company knowledge | WeKnora |
| Agent behavior and role configuration | Hermes Profiles / SOUL / Skills / Tools / MCP |
| Employee identity and Web access | Open WebUI |
| Durable agent task state | Hermes Kanban when enabled |
| Scheduled agent work | Hermes Cron when enabled |
| Deployment and operations state | this repository + deployment state |

### Profile is not a user account

A Hermes Profile represents an AI work role, not an individual employee.

```text
Employee A ─┐
Employee B ─┼──→ General Assistant ─→ Hermes `general` Profile
Employee C ─┘
```

Create specialist Profiles only when distinct work, knowledge, tool, credential, automation, model, memory, or risk boundaries require them.

### Profile is not a security sandbox

Profile isolation separates Hermes state; it does not automatically restrict all host filesystem or operating-system access.

Security requires:

```text
Human RBAC
+
Profile-level least-privilege tools and credentials
```

### Knowledge is not memory

```text
WeKnora
= authoritative shared company knowledge

Hermes Profile memory
= optional role/user operating continuity, subject to isolation rules
```

### Prefer mature upstream capabilities

```text
Official capability
→ official integration / extension
→ configuration
→ thin adapter
→ custom infrastructure only when truly necessary
```

### Real usage drives evolution

```text
sound baseline
→ usable deployment
→ real employee usage
→ concrete problem
→ smallest justified improvement
```

## Documentation map

| Document | Purpose |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Highest-priority AI agent execution and maintenance contract |
| [`DEPLOY.md`](DEPLOY.md) | Agent deployment Golden Path |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System architecture and component responsibilities |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Detailed deployment reference |
| [`docs/SECURITY.md`](docs/SECURITY.md) | Trust boundaries, secrets, least privilege, network security |
| [`docs/PROFILE-STANDARD.md`](docs/PROFILE-STANDARD.md) | Hermes Profile design and governance |
| [`docs/KNOWLEDGE.md`](docs/KNOWLEDGE.md) | WeKnora knowledge organization and governance |
| [`docs/CLIENT-RBAC.md`](docs/CLIENT-RBAC.md) | Open WebUI user/group/assistant mapping |
| [`docs/OPERATIONS.md`](docs/OPERATIONS.md) | Routine operation and troubleshooting |
| [`docs/BACKUP-RESTORE.md`](docs/BACKUP-RESTORE.md) | Backup and restore controls |
| [`docs/UPGRADE.md`](docs/UPGRADE.md) | Version and upgrade discipline |
| [`docs/ACCEPTANCE-TESTS.md`](docs/ACCEPTANCE-TESTS.md) | Validation suite for enabled capabilities |
| [`config/company.example.yaml`](config/company.example.yaml) | Generic declarative company configuration example |
| [`profiles/README.md`](profiles/README.md) | Reusable Profile template rules |
| [`infrastructure/README.md`](infrastructure/README.md) | Upstream-version-pinned adapter policy |
| [`state/DEPLOYMENT-STATE.md`](state/DEPLOYMENT-STATE.md) | Actual deployment/runtime truth |

## First validated reference path

The first working reference deployment used:

```text
Host: Apple Silicon macOS
Container runtime: OrbStack / Docker
WeKnora: v0.8.0
Hermes Agent: v0.21.0, host-native
Open WebUI: v0.11.3
Employee Hermes long-term memory: disabled
```

This deployment proved the core employee path, grounded WeKnora access, source visibility, Open WebUI RBAC, Profile API isolation, least-privilege employee tools, conversation history, file upload, and backup/restore behavior.

The exact runtime record is in [`state/DEPLOYMENT-STATE.md`](state/DEPLOYMENT-STATE.md). It is evidence from one validated deployment, not a source of universal company defaults.

## Current project status

The project has moved beyond architecture-only documentation:

- the core architecture has been implemented and functionally validated once;
- the employee client path has passed a real local demo;
- reusable Profile/configuration/security rules exist;
- a deployment Golden Path now consolidates the steps that previously required multiple follow-up instructions;
- tested deployment adapters and operational scripts exist for the validated reference environment.

Still not claimed:

- a generic one-command installer;
- fully autonomous fresh-host deployment validation after the Golden Path consolidation;
- production readiness for every host/platform/provider combination;
- automatic configuration of every optional integration.

The next real fresh-host deployment should be used as the next end-to-end validation opportunity rather than reinstalling solely for testing.

## Reference implementation: ARMOR

ARMOR is the first company using this architecture as a real deployment target.

See [`reference/armor/README.md`](reference/armor/README.md).

Company-specific configuration should remain in the appropriate private/protected deployment layer rather than becoming generic defaults in this public repository.

## What this project is not

This project is not intended to become:

- a new RAG engine;
- a new general-purpose Agent framework;
- a replacement for WeKnora;
- a fork of Hermes Agent;
- a fork of Open WebUI;
- a clone of Codex or Claude Code;
- an architecture that adds a new service for every possible feature.

The value of this repository is the integration architecture, deployment contract, governance, reusable configuration, validated adapters, and operating standard around mature upstream projects.

## License

This repository is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

Independent upstream software keeps its own license and terms. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) before distributing or rebranding a deployment.
