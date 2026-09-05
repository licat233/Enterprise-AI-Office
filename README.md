# Enterprise AI Office

> An agent-readable blueprint for building a self-hosted enterprise AI workspace with **WeKnora + Hermes Agent + Open WebUI + Codex + Claude Code + MCP**.

Enterprise AI Office is a public architecture and implementation project for companies that want to build an internal AI office system around their own knowledge, roles, workflows, tools, and employees.

The long-term goal is deliberately practical:

> **A company should be able to give this repository to a capable AI engineering agent, let the agent read the repository, and have it understand how to deploy, configure, validate, operate, and safely evolve the complete system.**

ARMOR is the first reference implementation and real-world validation environment. The project itself is intended to be reusable by other companies rather than remain ARMOR-specific.

## 中文简介

Enterprise AI Office 的目标，是提供一套**任何公司都可以参考、部署和持续迭代的企业 AI 办公系统蓝图**。

项目采用 Agent-first 的建设方式：仓库不仅面向人类管理员，也面向 Hermes、Codex、Claude Code 等 AI Agent。一个合格的执行 Agent 应该能够通过阅读本仓库，理解系统架构、组件职责、安全边界、部署顺序、验收标准和长期维护规则，并据此搭建和维护整套系统。

ARMOR 是本项目的首个真实企业参考实现，但不是项目本身的唯一适用对象。

---

## What are we building?

Not another chatbot.

Enterprise AI Office is designed as an **AI work layer for a company**:

```text
Employee
   │
   ▼
Employee Client / Messaging
   │
   ▼
Hermes Agent
   │
   ├── Company Knowledge
   ├── Role-specific Skills
   ├── Tools / MCP
   ├── Memory
   ├── Kanban
   ├── Cron Automation
   └── Specialized Coding Agents
```

An employee should be able to ask for work in natural language while the system decides whether it needs to search company knowledge, use a department workflow, call a tool, create durable work, run scheduled automation, or delegate software engineering to Codex / Claude Code.

---

## Reference architecture

| Layer | Technology | Responsibility |
| --- | --- | --- |
| Enterprise Knowledge | **WeKnora** | Document ingestion, parsing, retrieval, reranking, citations and enterprise knowledge |
| Primary Agent Runtime | **Hermes Agent** | Reasoning, Profiles, SOUL, Skills, Tools, Memory, MCP and orchestration |
| Employee Web Client | **Open WebUI** | Users, groups, RBAC, chat interface and employee-facing access |
| Hermes Admin Client | **hermes-webui** | Administrative access to Hermes configuration and all Profiles |
| Role Architecture | **Hermes Profiles** | Department / specialist agents with isolated role configuration |
| Knowledge Bridge | **WeKnora MCP / supported API** | Agent-to-knowledge integration boundary |
| Durable Agent Work | **Hermes Kanban** | Persistent multi-agent task coordination |
| Automation | **Hermes Cron** | Scheduled and recurring agent work |
| Coding Execution | **Codex + Claude Code** | Software engineering, repository changes, testing and debugging |
| Messaging / Remote Access | **Hermes Gateway** | Feishu, WeCom, Weixin and other supported messaging surfaces |
| Operations & Governance | **This repository** | Architecture, deployment state, security, backup, upgrade and maintenance rules |

```text
                         Employees
                             │
              ┌──────────────┼──────────────┐
              │              │              │
          Open WebUI       Feishu        WeCom / Weixin
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                      Hermes Agent
                             │
             ┌───────────────┼────────────────┐
             │               │                │
         WeKnora          Codex          Claude Code
             │
             ▼
      Company Knowledge

Admin-only control surface:
AI Administrator → hermes-webui → Full Hermes management
```

---

## Core design rules

### One responsibility, one authority

| Information | Authority |
| --- | --- |
| Company knowledge | WeKnora |
| Agent behavior and role configuration | Hermes Profiles / SOUL / Skills / Tools / MCP |
| Employee identity and Web access | Open WebUI |
| Durable agent task state | Hermes Kanban |
| Scheduled agent work | Hermes Cron |
| Deployment and operations state | this repository + deployment state |

### Profile is not a user account

A Hermes Profile represents an **AI role**, not an individual employee.

```text
Sales Employee A ─┐
Sales Employee B ─┼──→ Sales Assistant ─→ sales Hermes Profile
Sales Employee C ─┘
```

### Profile is not a security sandbox

Profile isolation separates Hermes state; it does not automatically restrict all host filesystem or operating-system access.

Security requires:

```text
User / Group RBAC
+
Profile-level least-privilege tools and credentials
```

### Knowledge is not memory

```text
WeKnora
= shared company knowledge

Hermes Profile Memory
= role-specific operating experience / context
```

### Prefer upstream capabilities

```text
Official capability
→ official integration / extension
→ configuration
→ thin adapter
→ custom infrastructure only when truly necessary
```

### Real usage drives versions

```text
sound stack
→ v1
→ real employee usage
→ concrete problems
→ smallest justified improvement
→ v2 → v3 → ...
```

---

## Documentation map

**AI agents should start with [`AGENTS.md`](AGENTS.md).** It is the repository-local operating contract for deployment and maintenance.

| Document | Purpose |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Highest-priority AI agent execution and maintenance contract |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Generic system architecture, component responsibilities and invariants |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | End-to-end deployment sequence and integration blueprint |
| [`docs/SECURITY.md`](docs/SECURITY.md) | Trust boundaries, secrets, tool least privilege, data and network security |
| [`docs/PROFILE-STANDARD.md`](docs/PROFILE-STANDARD.md) | How to create and govern Hermes Profiles, SOUL, Skills, memory and tools |
| [`docs/KNOWLEDGE.md`](docs/KNOWLEDGE.md) | WeKnora knowledge organization, ingestion, retrieval and governance |
| [`docs/CLIENT-RBAC.md`](docs/CLIENT-RBAC.md) | Open WebUI user/group/assistant mapping and multi-user isolation |
| [`docs/OPERATIONS.md`](docs/OPERATIONS.md) | Routine system operation, troubleshooting and handover |
| [`docs/BACKUP-RESTORE.md`](docs/BACKUP-RESTORE.md) | Backup scope, retention, disaster recovery and restore verification |
| [`docs/UPGRADE.md`](docs/UPGRADE.md) | Version discipline, upgrade workflow and rollback rules |
| [`docs/ACCEPTANCE-TESTS.md`](docs/ACCEPTANCE-TESTS.md) | Production readiness test suite |
| [`state/DEPLOYMENT-STATE.md`](state/DEPLOYMENT-STATE.md) | Template for recording the actual deployed system |
| [`state/CHANGELOG.md`](state/CHANGELOG.md) | Material deployment-change history template |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | Upstream project/license boundaries |
| [`reference/armor/README.md`](reference/armor/README.md) | ARMOR reference implementation index |

---

## Agent-readable by design

A deployment or maintenance agent should be able to determine from this repository:

- what must be installed;
- what must **not** be installed by default;
- which component owns each responsibility;
- how Profiles should be created;
- how knowledge is exposed to Hermes;
- how employees are mapped to authorized assistants;
- which tools each role may use;
- how the system is tested before production;
- how configuration/data are backed up;
- how upgrades are performed and rolled back;
- which architecture decisions an agent is not allowed to silently change.

The repository documentation is intentionally explicit because it is meant to survive handover between different AI agents and human maintainers.

---

## Current repository structure

```text
Enterprise-AI-Office/
├── AGENTS.md
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── OPERATIONS.md
│   ├── SECURITY.md
│   ├── PROFILE-STANDARD.md
│   ├── KNOWLEDGE.md
│   ├── CLIENT-RBAC.md
│   ├── BACKUP-RESTORE.md
│   ├── UPGRADE.md
│   └── ACCEPTANCE-TESTS.md
├── reference/
│   └── armor/
│       └── README.md
├── state/
│   ├── DEPLOYMENT-STATE.md
│   └── CHANGELOG.md
└── ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范.md
```

The next implementation layer will add reusable company configuration, Profile/SOUL templates, infrastructure examples, health/backup tooling, and machine-executable validation.

---

## Current status

The repository is in the **architecture-complete / implementation-bootstrap** stage.

### Completed baseline

- v1 technology stack and responsibility boundaries;
- AI agent operating contract;
- generic architecture;
- deployment blueprint;
- security model;
- Hermes Profile standard;
- knowledge governance standard;
- employee client/RBAC model;
- operations manual;
- backup/restore standard;
- upgrade/rollback standard;
- production acceptance tests;
- deployment-state and changelog templates;
- first ARMOR reference design;
- Apache-2.0 project license and third-party license boundary documentation.

### Not yet complete

- generic company configuration schema;
- reusable Profile / SOUL templates;
- reusable Skill templates;
- reproducible infrastructure manifests/examples;
- environment templates;
- automated health checks;
- backup/restore scripts;
- acceptance-test automation;
- one-command deployment.

Do not interpret the current repository as a finished installer.

---

## Reference implementation: ARMOR

ARMOR is the first company using this architecture as a real deployment target.

Start here:

- [`reference/armor/README.md`](reference/armor/README.md)
- [ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范](<ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范.md>)

The ARMOR material is a concrete implementation reference. Other companies must configure their own organization rather than blindly copy ARMOR-specific values.

---

## Intended deployment model

The first reference deployment targets a company-owned Mac Studio, but the architecture is not intended to be permanently Mac-only.

```text
Host OS
├── Hermes Agent
├── Codex
└── Claude Code

Containers
├── WeKnora
└── Open WebUI
```

Hermes is initially kept close to the host because restricted Engineering Profiles may need controlled access to local repositories, Git, Codex, Claude Code and host tools.

Future Linux/server deployment support should preserve the same component boundaries.

---

## What this project is not

This project is not intended to become:

- a new RAG engine;
- a new general-purpose Agent framework;
- a replacement for WeKnora;
- a fork of Hermes Agent;
- a fork of Open WebUI;
- a clone of Codex or Claude Code;
- an architecture that adds a new service for every possible feature.

The value of this repository is the **integration architecture, governance, deployment model, reusable configuration and enterprise operating standard** built around mature upstream projects.

---

## Architecture change policy

Before adding a major component such as a vector database, workflow engine, orchestration framework, model gateway, proxy, SSO system, or synchronization service, answer:

1. What concrete business problem exists?
2. Why can the current stack not solve it?
3. What measurable benefit does the new component provide?
4. What new failure modes does it introduce?
5. What is the maintenance burden?
6. What data/security boundary changes?
7. How is it backed up and restored?
8. How can it be removed later?

If the benefit is not clearly greater than the cost and risk, the default is:

> **Not now.**

---

## License

This repository is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

This license covers this project's original documentation, templates, scripts, configuration examples and other original content. Independent upstream software keeps its own license and terms.

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) before distributing or rebranding a deployment. In particular, Open WebUI currently uses its own license with branding conditions that adopters should review for their deployment size and intended branding.

---

## Immediate roadmap

1. Define a generic company configuration schema.
2. Add reusable Hermes Profile / SOUL templates.
3. Add shared and department Skill templates.
4. Add reproducible WeKnora / Open WebUI infrastructure examples.
5. Add health, backup and restore scripts.
6. Automate key acceptance tests.
7. Deploy the ARMOR reference implementation.
8. Feed real operational findings back into the generic project.

The goal is not to predict every future requirement.

The goal is to build a foundation that companies can actually operate, understand, maintain and improve.
