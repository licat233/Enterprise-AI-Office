# Enterprise AI Office

> An agent-readable and agent-executable blueprint for building a self-hosted enterprise AI workspace with **WeKnora + Hermes Agent + Open WebUI + MCP**, plus company-selected Profiles, administration, coding agents, automation, messaging, identity, and production controls.

Enterprise AI Office is a public architecture and implementation project for companies that want an internal AI work system around their own knowledge, roles, workflows, tools, employees, and security boundaries.

The practical goal is:

> **Give this repository to a capable AI engineering agent, provide the company deployment configuration and protected credentials/authority it genuinely needs, and let the agent drive the system to the requested readiness level without repeated human reminders about routine implementation steps.**

ARMOR is the first reference implementation. The project itself remains generic.

## Deploy with an AI agent

For deployment or deployment planning, use this order:

1. [`AGENTS.md`](AGENTS.md) — highest-priority repository-local operating contract.
2. [`DEPLOY.md`](DEPLOY.md) — deployment Golden Path.
3. [`docs/COMPLETENESS.md`](docs/COMPLETENESS.md) — readiness/completion contract.
4. active company configuration, based on [`config/company.example.yaml`](config/company.example.yaml).
5. [`config/capabilities.yaml`](config/capabilities.yaml) — capability closure registry.
6. [`config/validated-stack.yaml`](config/validated-stack.yaml) — validated core reproducibility baseline.
7. referenced infrastructure playbooks/adapters.
8. [`docs/ACCEPTANCE-TESTS.md`](docs/ACCEPTANCE-TESTS.md) — evidence gates.

When the task is specifically about the current v2 milestone, also read:

1. [`docs/V2-SCOPE.md`](docs/V2-SCOPE.md)
2. [`docs/V2-DESIGN-REVIEW.md`](docs/V2-DESIGN-REVIEW.md)
3. [`docs/V2-IMPLEMENTATION-PLAN.md`](docs/V2-IMPLEMENTATION-PLAN.md)
4. [`docs/V2-IMPLEMENTATION-STATUS.md`](docs/V2-IMPLEMENTATION-STATUS.md)
5. the provider-specific capability artifacts referenced by `config/capabilities.yaml`

The intended interaction is one deployment request, not a sequence of prompts reminding the agent to connect WeKnora, create Profiles, configure RBAC, implement an already-enabled optional capability, test the employee client, or record state.

Human input remains legitimate for real deployment tasks that require authority the agent cannot invent: model/API credentials, mailbox/client credentials, OS permission approval, IdP/app registration, enterprise messaging credentials, private-access authority, destructive conflicts, and real company business choices missing from configuration.

## What does “complete” mean?

Complete is **configuration-relative**, not “install every feature in the repository”.

```text
CORE READY
= baseline employee workflow works

CONFIGURED READY
= Core Ready
  + every capability enabled by this company is deployed and accepted

PRODUCTION READY
= Configured Ready
  + applicable production recovery/security/access/operations controls pass
```

This avoids both failure modes:

```text
under-build
→ stop after basic chat while configured capabilities are missing

feature collection
→ install Sales/QC/Kanban/Cron/SSO/etc. that the company never requested
```

The company chooses the target with:

```yaml
deployment:
  target_readiness: production-ready
```

See [`docs/COMPLETENESS.md`](docs/COMPLETENESS.md).

## Core employee workflow

```text
Employee
   ↓
Open WebUI
   ↓
General Assistant
   ↓
Hermes `general` Profile
   ↓
WeKnora
   ↓
grounded company answer + source
```

Baseline objects are deliberately small:

```text
Hermes control plane
└── default/admin Profile

Employee plane
├── Open WebUI
├── All-Employees group
├── General Assistant
└── general Profile

Knowledge
└── company-defined WeKnora Knowledge Base(s)
```

## Capability-driven extension

Optional capability playbooks are available for company-selected needs such as:

| Capability | Implementation path |
| --- | --- |
| Specialist Profiles | `docs/PROFILE-STANDARD.md` + generic Hermes specialist templates |
| Hermes admin Web UI | `infrastructure/hermes-webui/` |
| Codex / Claude Code delegation | `infrastructure/coding-agents/` |
| Kanban | `infrastructure/hermes/features/` |
| Cron | `infrastructure/hermes/features/` |
| Enterprise messaging | `infrastructure/hermes/features/` |
| Tencent Enterprise Mail | `infrastructure/email/tencent-exmail/` when selected |
| Remote/private access | `infrastructure/access/` |
| SSO / enterprise identity | `infrastructure/access/` |
| Employee long-term memory | Profile/RBAC isolation rules and acceptance gate |

[`config/capabilities.yaml`](config/capabilities.yaml) maps each enabled capability to its implementation path, required external inputs, acceptance test, and state fields.

An enabled capability cannot be silently skipped to reach a green result. A disabled capability must not be instantiated merely because a template exists.

## Current v2 milestone

The current controlled expansion milestone is:

> **Communication & Follow-up**

Frozen design:

```text
one governed email operational loop
+
Open WebUI remains primary employee surface
+
optional one messaging surface later
+
Hermes-native follow-up automation only after the email loop is proven
+
Ontology governance for the real read/write boundary
```

The design review is PASS and frozen. **v2 is currently still in the design stage; real implementation/deployment is not authorized.** [`docs/V2-IMPLEMENTATION-PLAN.md`](docs/V2-IMPLEMENTATION-PLAN.md) is the future staged implementation blueprint, not the current execution state.

Current design/prototype state:

```text
provider selected for ARMOR reference design: Tencent Enterprise Mail
future Stage 1 surface: search_email + get_email
read-only adapter/test/playbook: present as design-support prototypes
real provider runtime: not activated
mailbox credentials: not required now
SMTP/customer-facing send: not implemented or authorized
```

See [`docs/V2-IMPLEMENTATION-STATUS.md`](docs/V2-IMPLEMENTATION-STATUS.md) for the current design/prototype evidence status.

The candidate Stage 1 Agent-facing surface is deliberately limited to:

```text
search_email
get_email
```

Offline deterministic tests may be used during design to prove that the proposed adapter can remain read-only. They do not create a requirement to connect a mailbox. Real mailbox credentials, Profile binding, IMAP runtime acceptance, and SMTP are deferred until ARMOR explicitly opens a future implementation/deployment gate.

v2 does **not** reopen the entire deferred-feature list. CRM, ERP, Calendar, employee long-term memory, n8n, extra vector databases, local-LLM infrastructure, graph databases, broad autonomous external actions, and multiple messaging platforms remain outside the initial milestone unless a concrete blocking requirement justifies a separate decision.

## Reference architecture

| Layer | Technology | Responsibility |
| --- | --- | --- |
| Enterprise Knowledge | **WeKnora** | Documents, retrieval, source evidence, Knowledge Bases |
| Primary Agent Runtime | **Hermes Agent** | Profiles, SOUL, Skills, tools, MCP, orchestration |
| Employee Web Client | **Open WebUI** | Human users, groups, RBAC, chat, history |
| Hermes Admin Client | **hermes-webui** when enabled | Privileged Hermes administration |
| AI Work Roles | **Hermes Profiles** | Role/capability boundaries |
| Knowledge Bridge | **WeKnora MCP / supported API** | Hermes-to-knowledge integration |
| Governed Operational Integrations | provider-specific capability when enabled | Narrow business reads/actions under capability/Ontology/security contract |
| Durable Agent Work | **Hermes Kanban** when enabled | Persistent multi-Agent task coordination |
| Automation | **Hermes Cron** when enabled | Scheduled Agent work |
| Coding Execution | **Codex + Claude Code** when enabled | Specialist software engineering |
| Messaging | **Hermes Gateway** when enabled | Enterprise messaging access/delivery |
| Operations/Governance | **This repository** | Desired state, deployment contract, security, recovery, acceptance |

## Core design rules

### One responsibility, one authority

| Information | Authority |
| --- | --- |
| Company knowledge | WeKnora |
| Agent behavior/role config | Hermes Profiles / SOUL / Skills / Tools / MCP |
| Employee Web identity/access | Open WebUI / selected enterprise identity layer |
| External business-system state | selected provider/System of Record |
| EAO-owned operational governance evidence | Enterprise AI Office capability/Ontology layer where explicitly defined |
| Durable Agent tasks | Hermes Kanban when enabled |
| Scheduled work | Hermes Cron when enabled |
| Desired deployment | active company configuration |
| Actual deployment | real runtime + deployment state |

### Profile is not a user

A Hermes Profile represents an AI work role/capability boundary, not an employee account.

```text
Employee A ─┐
Employee B ─┼→ General Assistant → `general`
Employee C ─┘
```

Create a specialist Profile only when distinct work, knowledge, tools, credentials, automation, model, memory, or risk boundaries require it.

### Profile is not a sandbox

Profile state isolation does not automatically restrict all host access.

Security requires:

```text
Human RBAC
+
Profile least-privilege capabilities/credentials
+
workspace/OS/container boundaries where required
```

### Knowledge is not memory

```text
WeKnora
= authoritative shared company knowledge

Hermes memory
= optional role/user continuity subject to isolation rules
```

### Upstream first

```text
official upstream capability
→ official integration
→ configuration
→ thin adapter/playbook
→ custom infrastructure only when necessary
```

### Real use drives evolution

```text
sound baseline
→ complete configured deployment
→ real employee usage
→ concrete problem
→ smallest justified improvement
```

## First validated core stack

The first real reference validation used:

```text
Host: Apple Silicon macOS
Container runtime: OrbStack / Docker
WeKnora: v0.8.0
Hermes Agent: v0.21.0, host-native
Open WebUI: v0.11.3
Employee Hermes long-term memory: disabled
```

It proved the core employee path, grounded source-backed knowledge, Open WebUI RBAC, Profile API isolation, least-privilege employee tools, conversation history/file upload, and backup/restore behavior.

Machine-readable baseline: [`config/validated-stack.yaml`](config/validated-stack.yaml).

Actual reference-instance evidence: [`state/DEPLOYMENT-STATE.md`](state/DEPLOYMENT-STATE.md).

A fresh deployment should use [`state/DEPLOYMENT-STATE.template.md`](state/DEPLOYMENT-STATE.template.md) rather than copying reference-instance roles/capabilities.

## Repository self-check

Without installing anything:

```sh
sh scripts/repository-readiness-check.sh
```

This checks that the deployment contracts, capability registry, core adapters, conditional playbooks, v2 email design-support artifacts, acceptance gates, state template, and production-control helpers are structurally present.

It does **not** authorize implementation or replace deterministic adapter execution or real runtime acceptance when a future deployment begins.

## Documentation map

| Document | Purpose |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | AI agent operating contract |
| [`DEPLOY.md`](DEPLOY.md) | deployment execution Golden Path |
| [`docs/COMPLETENESS.md`](docs/COMPLETENESS.md) | Core/Configured/Production readiness semantics |
| [`docs/V2-SCOPE.md`](docs/V2-SCOPE.md) | controlled v2 Communication & Follow-up scope |
| [`docs/V2-EMAIL-DESIGN.md`](docs/V2-EMAIL-DESIGN.md) | frozen governed email business/authority design |
| [`docs/V2-COMMUNICATION-FOLLOWUP-DESIGN.md`](docs/V2-COMMUNICATION-FOLLOWUP-DESIGN.md) | employee entry and follow-up boundaries |
| [`docs/V2-DESIGN-REVIEW.md`](docs/V2-DESIGN-REVIEW.md) | frozen v2 architecture review |
| [`docs/V2-IMPLEMENTATION-PLAN.md`](docs/V2-IMPLEMENTATION-PLAN.md) | future staged implementation blueprint; implementation not currently authorized |
| [`docs/V2-IMPLEMENTATION-STATUS.md`](docs/V2-IMPLEMENTATION-STATUS.md) | current v2 design/prototype evidence and phase boundary |
| [`config/company.example.yaml`](config/company.example.yaml) | generic company desired-state schema |
| [`config/capabilities.yaml`](config/capabilities.yaml) | capability implementation/acceptance registry |
| [`config/validated-stack.yaml`](config/validated-stack.yaml) | validated core version baseline |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | component responsibilities/boundaries |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | detailed deployment reference |
| [`docs/SECURITY.md`](docs/SECURITY.md) | trust/secrets/least-privilege rules |
| [`docs/PROFILE-STANDARD.md`](docs/PROFILE-STANDARD.md) | Hermes Profile design/governance |
| [`docs/KNOWLEDGE.md`](docs/KNOWLEDGE.md) | WeKnora knowledge governance |
| [`docs/CLIENT-RBAC.md`](docs/CLIENT-RBAC.md) | employee identity/group/Assistant mapping |
| [`docs/ONTOLOGY.md`](docs/ONTOLOGY.md) | operational object/read/action governance contract |
| [`docs/ACCEPTANCE-TESTS.md`](docs/ACCEPTANCE-TESTS.md) | readiness evidence suite |
| [`docs/acceptance/TENCENT-EXMAIL.md`](docs/acceptance/TENCENT-EXMAIL.md) | provider-specific governed email acceptance design |
| [`docs/BACKUP-RESTORE.md`](docs/BACKUP-RESTORE.md) | production recovery controls |
| [`docs/OPERATIONS.md`](docs/OPERATIONS.md) | routine operations/troubleshooting |
| [`docs/UPGRADE.md`](docs/UPGRADE.md) | version/upgrade discipline |
| [`infrastructure/README.md`](infrastructure/README.md) | adapter/playbook policy and map |
| [`state/DEPLOYMENT-STATE.template.md`](state/DEPLOYMENT-STATE.template.md) | clean fresh-deployment state format |

## Project status

The repository now contains:

- a validated core architecture and employee workflow;
- machine-readable core version baseline;
- agent deployment Golden Path;
- explicit Core/Configured/Production readiness semantics;
- machine-readable capability closure registry;
- core WeKnora/Hermes/Open WebUI adapters;
- generic specialist Profile templates;
- playbooks for hermes-webui, Codex/Claude Code, Kanban, Cron, messaging, remote access, and SSO;
- production backup/restore/health controls;
- conditional acceptance gates;
- a clean fresh-deployment state template;
- static repository deployability self-check;
- an Enterprise Ontology design/governance contract plus structural validator;
- a frozen v2 Communication & Follow-up design;
- Tencent Enterprise Mail provider research plus read-only prototype/test artifacts retained to reduce future implementation uncertainty.

Still not claimed:

- a universal one-command installer/compiler;
- empirical proof that a completely new AI agent has already executed the newly consolidated full path on a second clean host;
- pre-validation of every possible vendor-specific IdP, messaging provider, model provider, host OS, private-access service, or email provider;
- authorization to connect the ARMOR mailbox during the current design stage;
- real Tencent Enterprise Mail Stage 1 runtime acceptance;
- completion of the v2 draft/approval/send operational loop.

Those are not excuses for manual routine prompting during a real deployment. Once a deployment task is explicitly opened, the agent must follow the repository until it reaches the requested readiness level, asks only for genuine external authority/input, or reports a specific failure.

The next real fresh-host deployment is the appropriate end-to-end empirical validation; there is no need to reinstall a working demo solely to produce that evidence.

## ARMOR reference

ARMOR-specific design/lessons live under [`reference/armor/`](reference/armor/). Reference material must not override the generic deployment contract or another adopter's configuration.

## What this project is not

This project is not intended to become:

- a new RAG engine;
- a new Agent framework;
- a WeKnora/Hermes/Open WebUI fork;
- a clone of Codex/Claude Code;
- a component collection where every possible feature is installed.

Its value is the integration architecture, capability-driven desired state, agent execution contract, thin upstream adapters/playbooks, security/recovery standards, acceptance evidence, and operating discipline around mature projects.

## License

This repository is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

Independent upstream software retains its own licenses/terms. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) before distribution or rebranding.
