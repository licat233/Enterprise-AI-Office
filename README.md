# Enterprise AI Office

> An agent-readable blueprint for building a self-hosted enterprise AI workspace with **WeKnora + Hermes Agent + Open WebUI + Codex + Claude Code + MCP**.

Enterprise AI Office is a public architecture and implementation project for companies that want to build an internal AI office system around their own knowledge, roles, workflows, tools, and employees.

The long-term goal is deliberately practical:

> **A company should be able to give this repository to a capable AI engineering agent, let the agent read the repository, and have it understand how to deploy, configure, validate, operate, and safely evolve the complete system.**

ARMOR is the first reference implementation and real-world validation environment for this architecture. The project itself, however, is intended to become reusable by other companies rather than remain ARMOR-specific.

## 中文简介

Enterprise AI Office 的目标，是提供一套**任何公司都可以参考、部署和持续迭代的企业 AI 办公系统蓝图**。

项目采用 Agent-first 的建设方式：仓库不仅面向人类管理员，也面向 Hermes、Codex、Claude Code 等 AI Agent。未来一个合格的执行 Agent 应该能够通过阅读本仓库，理解系统架构、组件职责、安全边界、部署顺序、验收标准和长期维护规则，并据此完成整套系统的搭建与维护。

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

An employee should be able to ask for work in natural language while the system decides whether it needs to:

- search company knowledge;
- reason over multiple internal documents;
- use a department-specific workflow;
- call an internal or external tool;
- create or continue a durable task;
- run scheduled work;
- delegate a software-engineering task to Codex or Claude Code;
- return a result with appropriate evidence and access boundaries.

---

## Reference architecture

The current v1 architecture is built around the following stack:

| Layer | Technology | Responsibility |
| --- | --- | --- |
| Enterprise Knowledge | **WeKnora** | Document ingestion, parsing, retrieval, reranking, citations, enterprise knowledge |
| Primary Agent Runtime | **Hermes Agent** | Reasoning, Profiles, SOUL, Skills, Tools, Memory, MCP, orchestration |
| Employee Web Client | **Open WebUI** | Users, groups, RBAC, chat interface and employee-facing access |
| Hermes Admin Client | **hermes-webui** | Administrative access to Hermes configuration and all Profiles |
| Role Architecture | **Hermes Profiles** | Department / specialist agents with isolated role configuration |
| Knowledge Bridge | **WeKnora MCP** | Supported agent-to-knowledge integration boundary |
| Durable Agent Work | **Hermes Kanban** | Persistent multi-agent task coordination |
| Automation | **Hermes Cron** | Scheduled and recurring agent work |
| Coding Execution | **Codex + Claude Code** | Software engineering, repository changes, testing and debugging |
| Messaging / Remote Access | **Hermes Gateway** | Feishu, WeCom, Weixin and other supported messaging surfaces |
| Operations & Governance | **This repository** | Architecture, deployment state, configuration standards, backup, upgrade and maintenance rules |

High-level topology:

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

## Why this architecture?

The components have intentionally different responsibilities.

### WeKnora is the knowledge layer

Company facts, product specifications, SOPs, manuals, policies, training material and other durable organizational knowledge belong in the enterprise knowledge platform.

### Hermes is the work runtime

Hermes is not used merely as a chat wrapper. Its Profiles, Skills, SOUL, Memory, MCP support, Kanban, Cron, Bot Mode and Gateway make it the primary runtime for department and specialist agents.

Examples:

```text
sales profile
qc profile
marketing profile
engineering profile
```

Each Profile can have its own role, Skills, tools, credentials, memory and operating rules.

### Open WebUI is the employee portal

`hermes-webui` exposes machine-level Hermes administration and is therefore not treated as the normal multi-user employee client.

Open WebUI provides the user / group / RBAC layer so employees only receive access to the assistants that their role permits.

### Codex and Claude Code are specialist workers

They are not intended to be the main employee interface. Hermes delegates appropriate engineering work to them while retaining the higher-level task and organizational context.

---

## Core design rules

### 1. One responsibility, one authority

Do not let multiple components compete to become the source of truth for the same thing.

| Information | Authority |
| --- | --- |
| Company knowledge | WeKnora |
| Agent behavior and role configuration | Hermes Profiles / SOUL / Skills / Tools / MCP |
| Employee identity and Web access | Open WebUI |
| Durable agent task state | Hermes Kanban |
| Deployment and operations state | Enterprise-AI-Office repository |

### 2. Profile is not a user account

A Hermes Profile represents an **AI role**, not an individual employee.

```text
Sales Employee A ─┐
Sales Employee B ─┼──→ Sales Assistant ─→ sales Hermes Profile
Sales Employee C ─┘
```

Human identity remains in the employee access layer.

### 3. Profiles are not security sandboxes

Profile isolation separates Hermes state. It does not, by itself, restrict all host filesystem or operating-system access.

Security therefore requires both:

```text
User / Group RBAC
+
Profile-level least-privilege tools and credentials
```

Normal employee Profiles should not automatically receive raw terminal, unrestricted filesystem, system administration, Docker, or coding-agent access.

### 4. Knowledge is not memory

Enterprise facts should not be copied into every department Profile's memory.

```text
WeKnora
= shared company knowledge

Hermes Profile Memory
= role-specific working experience / context
```

### 5. Prefer upstream capabilities over custom infrastructure

Decision order:

```text
Existing official capability
        ↓
Official integration / extension
        ↓
Configuration
        ↓
Thin adapter
        ↓
Custom infrastructure only when truly necessary
```

### 6. Real usage drives versions

The project does not attempt to design the final perfect system in v1.

```text
choose a sound stack
        ↓
build v1
        ↓
real employee usage
        ↓
observe concrete problems
        ↓
make the smallest justified improvement
        ↓
v2 → v3 → v4 → ...
```

---

## Agent-readable by design

This repository is intended to become executable documentation for AI engineering agents.

A future deployment or maintenance agent should be able to determine from the repository:

- what must be installed;
- what must **not** be installed;
- which component owns each responsibility;
- how Profiles should be created;
- how knowledge is exposed to Hermes;
- how employee access is isolated;
- which tools each role may use;
- how the system is tested before production;
- how configuration is backed up;
- how upgrades are performed and rolled back;
- which architecture decisions an agent is not allowed to silently change.

The repository will therefore evolve toward a structure similar to:

```text
Enterprise-AI-Office/
├── AGENTS.md
├── README.md
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
├── profiles/
├── skills/
├── infrastructure/
├── scripts/
└── state/
```

This is the target repository model, not a claim that all of these files already exist today.

---

## Current status

The repository is currently in the **architecture / bootstrap stage**.

What exists today:

- the initial Enterprise AI Office architecture;
- the first ARMOR reference design;
- the selected v1 technology stack;
- component boundaries;
- Profile architecture principles;
- knowledge / agent / client separation;
- deployment and maintenance requirements;
- initial security and acceptance-test principles.

What is **not** yet complete:

- a generic company configuration layer;
- `AGENTS.md` implementation guardrails;
- reusable deployment manifests;
- environment templates;
- automated health checks;
- backup / restore scripts;
- full acceptance-test automation;
- one-command deployment.

Do not interpret the current repository as a finished installer.

The next project phase is to turn the approved architecture into a reusable, AI-agent-executable repository.

---

## Reference implementation: ARMOR

ARMOR is the first company using this architecture as a real deployment target.

The current detailed design is available here:

- [ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范](<ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范.md>)

The ARMOR document is valuable as a concrete reference implementation, but future generic deployment instructions must separate:

```text
Reusable Enterprise AI Office architecture
```

from:

```text
ARMOR-specific organization, paths, Profiles, credentials and business rules
```

A company adopting this project should configure its own organization rather than blindly copying ARMOR-specific values.

---

## Intended deployment model

The first reference deployment targets a company-owned Mac Studio, but the architecture is not intended to be permanently Mac-only.

The current reference approach is:

```text
Host OS
├── Hermes Agent
├── Codex
└── Claude Code

Containers
├── WeKnora
└── Open WebUI
```

Hermes is initially kept close to the host because engineering Profiles may need controlled access to local repositories, Git, Codex, Claude Code and host tools.

Future Linux/server deployment support should preserve the same architecture boundaries instead of creating a different product.

---

## What this project is not

This project is not intended to become:

- a new RAG engine;
- a new general-purpose Agent framework;
- a replacement for WeKnora;
- a fork of Hermes Agent;
- a fork of Open WebUI;
- a custom clone of Codex or Claude Code;
- an architecture that adds a new service for every possible feature.

The value of this repository is the **integration architecture, governance, deployment model and reusable enterprise operating standard** built around mature upstream projects.

---

## Architecture change policy

Before adding another major component such as a new vector database, workflow engine, orchestration framework, proxy, SSO system or synchronization service, the proposal must answer:

1. What concrete business problem exists?
2. Why can the current stack not solve it?
3. What measurable benefit does the new component provide?
4. What new failure modes does it introduce?
5. What is the maintenance burden?
6. What data or security boundary changes?
7. How is it backed up and restored?
8. How can it be removed later?

If the benefit is not clearly greater than the operational cost and risk, the default decision is:

> **Not now.**

---

## Upstream projects

Enterprise AI Office is an integration and operating architecture built on independent upstream projects, including:

- Tencent WeKnora
- Nous Research Hermes Agent
- Open WebUI
- hermes-webui
- OpenAI Codex
- Anthropic Claude Code
- Model Context Protocol (MCP)

Each upstream project has its own license, release cycle and security model. Production deployments should pin tested versions rather than blindly follow floating `latest` / `main` releases.

---

## License

This repository is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for the full license text.

The repository license applies to the original documentation, templates, scripts, configuration examples and other project content published here. Independent upstream projects such as WeKnora, Hermes Agent, Open WebUI, Codex and Claude Code remain governed by their own licenses and terms.

---

## Project direction

The immediate roadmap is intentionally narrow:

1. Convert the ARMOR reference design into generic architecture documents.
2. Add `AGENTS.md` so AI agents have a deterministic maintenance contract.
3. Define the reusable repository structure and company configuration boundary.
4. Create reproducible deployment instructions for WeKnora, Hermes and Open WebUI.
5. Add Profile / Skills / RBAC templates.
6. Add health, backup, restore and acceptance-test tooling.
7. Deploy the ARMOR reference implementation.
8. Feed real operational findings back into the generic project.

The goal is not to predict every future requirement.

The goal is to build a foundation that companies can actually operate, understand, maintain and improve.
