# Enterprise AI Office Architecture

Status: v1 architecture baseline

This document defines the reusable architecture of Enterprise AI Office. Company-specific values belong in deployment configuration or the appropriate reference/private layer, not in this generic contract.

## 1. Goal

Enterprise AI Office is an AI work layer for a company, not merely a chatbot or RAG demo.

The baseline lets an employee use an approved client to reach a Hermes work role that can retrieve authoritative company knowledge from WeKnora and return a grounded answer with source evidence.

Additional workflows, tools, automation, specialist agents, coding workers, and messaging surfaces are extensions enabled only when required.

## 2. Baseline topology

```text
Employee
   │
   ▼
Open WebUI
   │
   ▼
General Assistant
   │
   ▼
Hermes `general` Profile
   │
   ▼
WeKnora MCP / supported API
   │
   ▼
Company Knowledge
```

Control plane:

```text
AI Administrator
→ Hermes default/admin Profile + approved admin surfaces
```

Optional extensions may add specialist Profiles, messaging, Kanban, Cron, Codex, Claude Code, or other approved integrations without changing the baseline responsibility boundaries.

## 3. Component responsibilities

### WeKnora — enterprise knowledge platform

Owns document ingestion, parsing, chunking, embedding, retrieval, source traceability, metadata, and Knowledge Base management.

WeKnora answers: **What does the company know?**

### Hermes Agent — primary work runtime

Owns task reasoning, Profiles, SOUL, Skills, approved tools, MCP integrations, and optional memory/automation capabilities.

Hermes answers: **How should this work be completed?**

### Open WebUI — employee Web access

Owns human Web identity, groups, RBAC/resource access, chat UX, attachments where enabled, and conversation history.

Open WebUI is not the source of company knowledge and not the authority for Hermes Profile configuration.

### hermes-webui — optional administrative Hermes surface

Used by AI administrators and authorized maintainers when enabled. It is not the ordinary employee client.

### Codex and Claude Code — optional software-engineering workers

Used only when an authorized technical role requires repository-aware engineering execution.

### Hermes Kanban — optional durable agent work state

Used when multi-step work needs persistent assignment, handoff, review, blocking, or restart survival.

### Hermes Cron — optional scheduled work

Used for recurring or one-shot automation owned by an appropriate Profile.

### Hermes Gateway — ingress/delivery layer

Provides the API server used by Open WebUI and optional messaging/platform adapters.

### This repository — architecture and operations contract

Owns deployment intent, standards, reusable templates/adapters, acceptance rules, and deployment-state format.

## 4. Source-of-truth matrix

| Information class | Authority |
| --- | --- |
| Company facts, manuals, SOPs, specifications | WeKnora |
| AI role behavior and identity | Hermes Profile / SOUL |
| Reusable agent workflows | Hermes Skills |
| Tool/integration permissions | Hermes Profile configuration / MCP |
| Employee Web identity and access | Open WebUI |
| Durable agent tasks | Hermes Kanban when enabled |
| Scheduled routines | Hermes Cron when enabled |
| Current deployment state | `state/DEPLOYMENT-STATE.md` + real runtime |
| Architecture intent | `AGENTS.md` + this document |

## 5. Hermes Profile model

A Profile is an AI work role, not a human user or a department record.

Baseline:

```text
default/admin  # privileged control plane
general        # baseline employee-facing assistant
```

Create an additional specialist Profile only when a distinct requirement exists, such as:

- different work behavior/SOUL;
- different knowledge access;
- different tools or credentials;
- different model or memory policy;
- different automation ownership;
- different risk boundary.

A Profile may have its own config, secrets, SOUL, Skills, MCP servers, tools, credentials, sessions, memory, automation, and state.

The optional templates under `profiles/` are examples available for reuse, not a list of Profiles that a deployment should instantiate.

## 6. Human identity model

Human identity is separate from AI role identity.

```text
Human employee
→ Open WebUI user
→ authorized group/resource
→ Assistant
→ Hermes Profile
```

Baseline:

```text
ordinary employee
→ All-Employees
→ General Assistant
→ `general`
```

A company may add specialist mappings when its real authorization model requires them. One Profile may serve many humans, and one human may be authorized for multiple Profiles.

## 7. Knowledge model

Enterprise knowledge belongs in WeKnora.

A baseline deployment may begin with one shared employee Knowledge Base, for example:

```text
Company Knowledge
```

Create additional Knowledge Bases only when semantic domain, permission boundary, lifecycle, or operational ownership materially requires separation.

Use folders/tags/metadata inside an existing Knowledge Base before creating unnecessary top-level Knowledge Bases.

Do not use Profile memory as a substitute for authoritative company knowledge.

## 8. Knowledge bridge

Preferred integration:

```text
Hermes
  │
  │ MCP / supported API
  ▼
WeKnora
```

Use a least-privilege, read-oriented retrieval surface for normal employee Profiles.

Do not bind Hermes directly to WeKnora's internal database schema.

## 9. Employee Web client mapping

Open WebUI exposes only authorized Assistant resources.

Baseline:

```text
All-Employees → General Assistant → `general`
```

Additional mappings are generated from company configuration rather than inferred from template names or an assumed organization chart.

Global employee permissions should remain minimal. UI hiding is not a security boundary; direct unauthorized access must fail closed.

## 10. Hermes API routing

The validated architecture uses Hermes Profile routing through supported Gateway mechanisms.

Every employee-facing Profile must use its own API credential. Cross-Profile credential use must fail closed.

The privileged default/admin Profile must not be exposed as a normal employee Assistant.

## 11. Memory model

Keep these scopes separate:

### Company knowledge
WeKnora.

### Profile operating memory
Optional Hermes Profile memory, only when its sharing/isolation semantics are appropriate for the role.

### Individual conversation history
Open WebUI user-scoped conversation history.

Employee Hermes long-term memory is disabled by baseline policy until cross-user isolation is proven for the exact deployed client/runtime path.

## 12. Tool security model

Security has two dimensions:

```text
Human RBAC
+
Profile capability boundary
```

A normal employee Profile should not automatically receive unrestricted terminal, filesystem writes, Docker/system control, GitHub administration, coding-agent delegation, or broad credentials.

Grant stronger tools only to a role whose work actually requires them and only with an explicit workspace/credential boundary.

## 13. Optional technical Profile

A company may create a restricted technical/engineering Profile when repository or host work is a real requirement.

Such a Profile may receive terminal, files, Git, GitHub, Codex, or Claude Code only after workspace, repository-instruction, credential, and acceptance boundaries are defined.

## 14. Optional Kanban

Use Kanban when the work itself needs durable coordination or state.

Do not enable it merely because Hermes supports it, and do not treat it as an employee-wide project-management system without a separately designed access model.

## 15. Optional Cron

Enable Cron when the company has a real scheduled automation requirement.

Cron jobs are owned by an appropriate Profile/system role rather than assumed to be private employee schedules.

## 16. Optional messaging

Enable only messaging platforms the company actually uses.

Use supported identity/allowlist/pairing and deterministic Profile routing. Do not default to allow-all access.

## 17. Deployment model

First validated reference posture:

```text
Host-native
└── Hermes Agent

Containers
├── WeKnora
└── Open WebUI
```

Optional host-native coding workers may be installed when required.

The architecture may later support other hosts while preserving the same component responsibilities.

## 18. Network boundaries

Baseline exposure principles:

- Open WebUI: employee-accessible only on the approved network/access layer.
- WeKnora UI: knowledge maintainers/admins as required.
- Hermes employee API: internal/trusted client path only.
- administrative surfaces: admin only.
- PostgreSQL/Redis/parser/internal services: internal only.

Do not expose raw data stores or privileged endpoints to employees or the public Internet.

## 19. Architecture invariants

Unless an explicit architecture decision changes them:

1. WeKnora is the enterprise knowledge platform.
2. Hermes is the primary agent runtime.
3. Open WebUI is the baseline employee Web client.
4. Human identity is separate from Hermes Profile identity.
5. Default/admin is separated from the employee `general` Profile.
6. Knowledge uses supported integration surfaces rather than direct DB coupling.
7. Powerful tools are granted by justified role, not globally.
8. Optional capabilities are enabled by real requirements, not by template availability.
9. Versions used for reproducible deployments are pinned/tested.
10. Production recovery/security controls are validated before claiming Production Ready.
11. Real company usage drives future additions.

## 20. Future evolution

Potential additions may include ERP, CRM, email, calendars, workflow systems, model gateways, local inference, observability, SSO, extra retrieval infrastructure, or memory integration.

None are automatic requirements.

Each addition must pass the architecture/change rules in `AGENTS.md`.
