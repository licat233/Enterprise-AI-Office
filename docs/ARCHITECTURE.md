# Enterprise AI Office Architecture

Status: v1 architecture baseline

This document defines the reusable architecture of Enterprise AI Office. Company-specific values belong under `reference/` or deployment configuration, not in this generic contract.

## 1. Goal

Enterprise AI Office is an AI work layer for a company, not merely a chatbot or RAG demo.

The system should let employees ask for work in natural language while the agent runtime decides whether the task requires company knowledge, a role-specific workflow, a tool, durable task orchestration, scheduled work, or a specialist coding agent.

## 2. Reference topology

```text
                         Employees
                             │
              ┌──────────────┼──────────────┐
              │              │              │
          Open WebUI      Messaging      Other approved
          Web client      platforms       clients
              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                      Hermes Agent
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
     WeKnora              Codex              Claude Code
        │
        ▼
 Enterprise Knowledge

Admin control plane:
AI Admin → hermes-webui / Hermes CLI / WeKnora Admin / Open WebUI Admin
```

## 3. Component responsibilities

### WeKnora — enterprise knowledge platform

Owns document ingestion, parsing, chunking, embedding, hybrid retrieval, reranking, citations, metadata, and Knowledge Base management.

WeKnora answers: **What does the company know?**

### Hermes Agent — primary work runtime

Owns task reasoning, Profiles, SOUL, Skills, tools, MCP integrations, agent memory, Kanban, Cron, Bot Mode, and messaging Gateway behavior.

Hermes answers: **How should this work be completed?**

### Open WebUI — employee Web access

Owns human Web identity, groups, RBAC/resource access, chat UX, and conversation history for the employee-facing browser surface.

Open WebUI is not the source of company knowledge and not the authority for Hermes Profile configuration.

### hermes-webui — administrative Hermes surface

Used by AI administrators and authorized maintainers to manage Hermes capabilities. It is not the default employee client because it exposes machine-level/profile-level administration.

### Codex and Claude Code — specialist software engineering workers

Used when Hermes determines that a task requires repository-aware software engineering. They should not become the primary employee interface.

### Hermes Kanban — durable agent work state

Owns persistent multi-agent tasks, handoffs, review, retries, blocking, comments, attachments, and agent work queues.

### Hermes Cron — scheduled agent work

Owns recurring and one-shot scheduled jobs, routine execution, and delivery of scheduled results.

### Hermes Gateway — external access and delivery

Owns supported messaging/platform adapters and API server ingress. It can route messages to appropriate Profiles.

### This repository — architecture and operations truth

Owns the intended architecture, deployment contract, templates, validation rules, operational state template, and upgrade/backup standards.

## 4. Source-of-truth matrix

| Information class | Authority |
| --- | --- |
| Company facts, manuals, SOPs, product specifications | WeKnora |
| AI role behavior and identity | Hermes Profile / SOUL |
| Reusable agent workflows | Hermes Skills |
| Tool/integration permissions | Hermes Profile configuration / MCP |
| Employee Web identity and access | Open WebUI |
| Durable multi-agent tasks | Hermes Kanban |
| Scheduled routines | Hermes Cron |
| Current deployment state | `state/DEPLOYMENT-STATE.md` + real runtime |
| Architecture intent | `docs/ARCHITECTURE.md` + `AGENTS.md` |

## 5. Hermes Profile model

A Profile is an AI role or specialist.

Typical company Profiles may include:

```text
general
sales
qc
marketing
engineering
operations
```

A Profile may have its own:

- `config.yaml`;
- `.env`;
- `SOUL.md`;
- model/provider settings;
- Skills;
- MCP servers;
- tools/toolsets;
- credentials;
- memory;
- sessions;
- Cron jobs;
- logs/state.

Profiles must be created because a distinct role, capability, permission boundary, or persistent specialist identity exists — not merely because another employee exists.

## 6. Human identity model

Human identity is distinct from AI role identity.

```text
Human user
→ employee group / authorization
→ employee-facing assistant
→ Hermes Profile
```

Example:

```text
Alice (Sales) ─┐
Bob (Sales)   ─┼→ Sales Group → Sales Assistant → `sales` Profile
Carol (Sales) ─┘
```

One human may be authorized for multiple Profiles. One Profile may serve many humans.

## 7. Knowledge model

Enterprise knowledge belongs in WeKnora.

Do not use Profile memory as a substitute for a company knowledge base.

Recommended initial Knowledge Base categories are examples, not hard-coded requirements:

```text
Company & Brand
Products & Technical
Sales & Marketing
Operations & SOP
```

Split Knowledge Bases primarily when semantic domain or permission boundary materially differs.

## 8. Knowledge bridge

Preferred integration:

```text
Hermes
  │
  │ MCP / supported API
  ▼
WeKnora
```

Do not bind Hermes directly to the internal WeKnora database schema.

For straightforward retrieval, prefer read-oriented search/document tools. Use a nested WeKnora Agent only when its own reasoning workflow adds real value.

## 9. Employee Web client mapping

Open WebUI should expose private assistant resources mapped to authorized groups.

Example:

```text
All Employees → General Assistant → `general`
Sales         → Sales Assistant   → `sales`
QC            → QC Assistant      → `qc`
Marketing     → Marketing Assistant → `marketing`
Engineering   → Engineering Assistant → `engineering`
```

Global defaults should be minimal. Group permissions then add required capabilities.

## 10. Hermes API routing

The architecture supports Hermes multi-Profile API routing through supported Gateway/Profile mechanisms.

Each employee-facing Profile must use its own API credential. Cross-Profile use of credentials must fail closed.

Do not expose the privileged/default administrative Profile to normal employees.

## 11. Memory model

Memory has three different scopes and they must not be conflated:

### Company knowledge
WeKnora.

### Department/specialist experience
Hermes Profile memory, only when it is safe and intentionally shared.

### Individual user interaction history
Employee client conversation history and, only after verification, a user-scoped Hermes memory mechanism.

If cross-user long-term memory isolation cannot be proven, do not enable shared employee long-term memory.

## 12. Tool security model

Security is two-dimensional:

```text
Human RBAC
+
Profile capability boundary
```

A user may only access authorized Profiles, and each Profile may only use tools/credentials required for its role.

A normal business Profile should not automatically receive:

- unrestricted terminal;
- unrestricted filesystem writes;
- Docker/system control;
- GitHub administration;
- Codex/Claude Code;
- broad enterprise credentials.

## 13. Engineering Profile

A restricted Engineering Profile may receive stronger capabilities such as terminal, files, Git, GitHub, Codex, and Claude Code.

It still requires explicit workspace boundaries, repository instructions, and least-privilege credentials.

## 14. Kanban model

Kanban is for durable agent work that must survive context limits, restarts, handoffs, review, or human intervention.

Use direct delegation for short synchronous reasoning tasks. Use Kanban when the task itself needs persistent state.

Kanban is not automatically an employee-wide project management/RBAC product.

## 15. Cron model

Cron jobs are Profile-owned automation.

A department Profile's recurring routines should be treated as department/system automation, not automatically as private user schedules.

## 16. Messaging model

Hermes Gateway may expose approved Profiles through enterprise messaging platforms.

Enable only platforms the adopting company actually uses.

Use allowlists, pairing, enterprise identity, and explicit routing. Do not default to allow-all production messaging.

## 17. Deployment model

Initial reference posture:

```text
Host-native:
- Hermes Agent
- Codex
- Claude Code

Containerized:
- WeKnora standard stack
- Open WebUI
```

The architecture should also be portable to Linux/server deployment later without changing component responsibilities.

## 18. Network boundaries

Recommended default exposure:

- Open WebUI: employee-accessible on approved network.
- WeKnora UI: knowledge maintainers/admins as required.
- Hermes API: internal only; employee access should normally flow through approved clients.
- hermes-webui: admin only.
- PostgreSQL/Redis/DocReader: internal only.

Do not expose raw data stores to employees or the public Internet.

## 19. Architecture invariants

The following are v1 invariants unless an explicit architecture decision changes them:

1. WeKnora remains the enterprise knowledge platform.
2. Hermes remains the primary agent runtime.
3. Human identity is separate from Hermes Profile identity.
4. Employee Web access is separated from Hermes administration.
5. Knowledge access uses supported integration surfaces, not direct DB coupling.
6. Powerful tools are granted by role, not globally.
7. Production versions are pinned/tested rather than blindly floating.
8. Backup and restore are first-class production requirements.
9. Real company usage drives future architecture additions.

## 20. Future evolution

Potential future additions may include ERP, CRM, email, calendars, workflow systems, model gateways, local inference, observability, SSO, additional vector infrastructure, or memory integration.

None are automatic v1 requirements.

Each must pass the Architecture Change Gate defined in `AGENTS.md`.
