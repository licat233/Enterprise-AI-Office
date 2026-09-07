# Enterprise AI Office

> An agent-readable and agent-executable **system blueprint + installation blueprint** for building a governed, self-hosted enterprise AI workspace around **WeKnora + Hermes Agent + Open WebUI**, with capability-driven extensions for specialized AI roles, coding agents, automation, messaging, enterprise identity, and governed business-system actions.

**[简体中文 README](./README.zh-CN.md)**

## Project status at a glance

| Milestone / capability | Status |
| --- | --- |
| v1 core employee path | ✅ Validated reference implementation |
| v2 System Design | ✅ Complete |
| v2 Installation Design | ✅ Complete |
| ID-1 Installation Architecture | ✅ Complete |
| ID-2 Config / Protected Inputs | ✅ Complete |
| ID-3 Stage / Capability Closure | ✅ Complete |
| ID-4 Identity / Authorization | ✅ Complete |
| ID-5 Governance Runtime | ✅ Complete |
| ID-6 Governed Send / Reconciliation | ✅ Complete |
| ID-7 Recovery / Clean-host Acceptance | ✅ Complete |
| Installation Design Final Review | ✅ PASS |
| Blueprint Validation | ⏳ Not yet opened |
| Release Ready | ⏳ Not yet opened |
| Real company deployment task | ⛔ Inactive |

> **Important:** “implemented” in this README means the repository contains the corresponding system design, installation contract, reference adapters/scripts, schemas, or validated core assets. It does **not** mean the v2 email workflow has already been deployed to a real company mailbox.

Authoritative lifecycle state: [`state/PROJECT-PHASE.yaml`](state/PROJECT-PHASE.yaml).

## Architecture overview

![Enterprise AI Office v2 architecture](./enterprise-ai-office-architecture.svg)

The validated v1 employee path is intentionally independent from the governed v2 communication path:

```text
Employee
  ↓
Open WebUI
  ├─ General Assistant
  │    ↓
  │  Hermes `general`
  │    ↓
  │  WeKnora
  │
  └─ Communication Assistant
       ├─ Hermes `communication` Profile for reasoning
       └─ Open WebUI server-side governed Email actions/tools
            ↓
          eao-email-governance
            ├─ Governance SQLite
            └─ Email Provider
```

A v2 Email failure must not break:

```text
Open WebUI → General Assistant → Hermes general → WeKnora
```

## What this repository already implements

### 1. Validated core enterprise-AI employee path

The validated core stack provides:

- **Open WebUI** as the employee-facing web client;
- **Hermes Agent** as the Agent runtime;
- **WeKnora** as the authoritative company-knowledge layer;
- grounded answers with source evidence;
- Open WebUI user/group/Assistant access controls;
- distinct Hermes Profile API boundaries;
- least-privilege employee tool exposure;
- conversation history and controlled file-upload behavior;
- backup / isolated restore reference procedures.

Core workflow:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes `general` Profile
→ WeKnora
→ grounded company answer + source
```

### 2. Agent-readable installation blueprint

The repository includes:

- [`AGENTS.md`](AGENTS.md): repository-local AI Agent operating contract;
- [`DEPLOY.md`](DEPLOY.md): installation/deployment Golden Path;
- [`config/capabilities.yaml`](config/capabilities.yaml): machine-readable capability registry;
- public company configuration schema and private-overlay shape;
- protected-input / secret-reference rules;
- lifecycle gates separating blueprint work from real deployment;
- Core / Configured / Production readiness semantics;
- global and provider-specific acceptance contracts;
- backup, restore, health-check, recovery, and state-recording helpers.

### 3. v2 governed Communication & Email loop

The v2 blueprint defines and provides reference assets for:

```text
search email
→ read email
→ prepare DraftReply
→ exact human review
→ deterministic SendApproval
→ governed send
→ provider result
→ reconciliation when ambiguous
→ optional internal follow-up
```

Current repository capabilities include:

- `Mailbox`, `EmailMessage`, `DraftReply`, `SendApproval` domain model;
- trusted **HumanActor** identity boundary;
- mailbox-scoped `email.read / email.draft / email.approve / email.send` authorization;
- Open WebUI trusted server-side identity forwarding;
- deterministic approval Action using exact persisted draft content;
- immutable DraftReply revision + content-hash binding;
- one logical-send claim per approval;
- append-oriented governance evidence;
- protected reconciliation control path;
- failure-safe `SENT / CONFIRMED_NOT_SENT / OUTCOME_UNKNOWN` semantics.

### 4. Thin EAO Email Governance runtime

v2 introduces one new EAO-owned runtime responsibility:

```text
eao-email-governance
```

Reference persistence:

```text
SQLite
<runtime_root>/runtime/email-governance/state.sqlite3
```

It covers:

- immutable DraftReply revisions;
- review bindings;
- SendApproval evidence;
- ApprovalClaim / one-logical-send enforcement;
- logical send and provider-attempt records;
- normalized provider results;
- reconciliation evidence;
- governance audit events;
- schema migration and recovery contracts.

### 5. Tencent Enterprise Mail reference provider

Repository assets include:

- read-only IMAP adapter candidate;
- non-mutating read safety tests;
- narrow SMTP send adapter;
- fake-SMTP deterministic tests;
- provider environment templates;
- provider-specific acceptance plan;
- ambiguous-send / duplicate-send safety contract.

The baseline does not expose generic “send anything” access.

### 6. Recovery and rollback

The repository defines:

- Governance SQLite consistent backup;
- isolated Governance restore;
- schema-version fail-closed behavior;
- unresolved-send recovery without automatic retry;
- optional full-stack backup integration for v2 Email;
- v1-compatible backup behavior when v2 Email is disabled;
- capability rollback levels;
- clean-host installation sequence;
- installer second-run convergence rules;
- failure-injection acceptance expectations;
- v1 preservation after v2 rollback/failure.

## Deliberate scope reductions and deferred capabilities

This section preserves **historical architecture decisions** that were made specifically to keep Enterprise AI Office understandable, maintainable, and low-risk.

These items are not “forgotten features.” They were intentionally **rejected, reduced, or deferred** because the initial system did not need them. A future milestone may reintroduce one only when a real business requirement justifies the added complexity.

The detailed v2 scope contract remains [`docs/V2-SCOPE.md`](docs/V2-SCOPE.md).

| Capability / idea | Current decision | Why it was reduced or deferred | Revisit only when… |
| --- | --- | --- | --- |
| CRM | Deferred / out of baseline | The governed communication loop can be proven without customer-master data, lead/opportunity models, or CRM synchronization | a real inquiry/sales workflow requires CRM-backed objects/actions |
| ERP | Deferred / out of baseline | Would add a large authority, integration, and master-data boundary unrelated to the first communication loop | a real operational workflow cannot be completed without ERP data/actions |
| PIM | Deferred / out of baseline | WeKnora already covers company/product knowledge needed by the baseline; a PIM integration would add another system of record | product-master synchronization becomes an observed requirement |
| Calendar integration | Deferred | Simple follow-up reminders can use Hermes Cron; Calendar is not needed to prove governed email | scheduling/meeting actions become a real core workflow |
| Employee long-term memory | Disabled / deferred | User isolation and privacy boundaries must be proven before re-enabling it | isolation is validated and real employee continuity value justifies it |
| SSO expansion | Deferred unless independently required | Open WebUI already provides the reference identity surface; expanding identity infrastructure would enlarge scope | production access requirements actually require enterprise SSO |
| `armor-memory` synchronization | Deferred | Would create a second continuity/memory integration problem before the baseline needs it | a concrete cross-system memory requirement exists |
| n8n / another workflow engine | Rejected for baseline | Hermes Cron/Kanban already cover the narrow scheduling and durable-task needs | a workflow is proven that existing Hermes capabilities cannot safely express |
| Second scheduler | Rejected | Hermes Cron is already the scheduling authority | Cron is demonstrably insufficient for a required workflow |
| Additional vector database / new RAG layer | Rejected for baseline | WeKnora is already the company-knowledge authority; another vector store would duplicate state and maintenance | measured retrieval limits cannot be solved inside WeKnora/upstream |
| Prometheus/Grafana-style large observability stack | Deferred | Small-system health checks and operating procedures are sufficient at the current scale | operating scale or incidents justify dedicated observability infrastructure |
| Local-LLM infrastructure project | Deferred | Model-hosting infrastructure is independent from proving the Enterprise AI Office architecture | privacy/cost/offline requirements make local inference a real deployment need |
| Custom Agent framework | Rejected | Hermes already owns Agent runtime/orchestration; building another framework would duplicate the core platform | Hermes cannot satisfy a demonstrated essential capability |
| Graph database / generic Ontology Runtime | Rejected for baseline | Ontology is currently a governance/design contract; a graph runtime would add a new database/reasoning platform without proven need | a real cross-system workflow requires graph-native enforcement/query semantics |
| Dedicated employee portal | Rejected | Open WebUI already provides the employee surface | a required employee workflow cannot be safely delivered through Open WebUI |
| New IAM / employee directory | Rejected | Open WebUI / selected enterprise identity remains the HumanActor source; a second IAM would duplicate identity state | a real identity requirement cannot be satisfied by the selected upstream identity layer |
| Multiple messaging platforms | Reduced to at most one optional surface | Every extra channel multiplies identity, routing, support, and acceptance complexity | real employee adoption evidence justifies another channel |
| Multiple new external business systems | Reduced to Email only in v2 | One external system is enough to prove the governed operational pattern without integration sprawl | a later milestone selects a concrete second business system |
| Autonomous customer-facing send | Rejected for baseline | External communication is a material side effect and requires deterministic human approval | a future explicit risk/policy decision authorizes a different governance model |
| Generic SMTP / arbitrary IMAP-write tools | Rejected | Generic protocol access bypasses Named Actions, mailbox scope, approval, and audit boundaries | no expected baseline case; any exception requires a new security review |
| Mailbox mirror / shadow customer database | Rejected | Email Provider remains authoritative for mailbox/message state; duplicating the mailbox creates synchronization and privacy burden | a proven provider limitation makes bounded local state unavoidable |
| PostgreSQL / Redis / event bus for Email Governance | Rejected for baseline | One thin single-host Governance service + SQLite is sufficient and much easier to recover and maintain | scale/concurrency evidence proves SQLite is no longer adequate |
| First-class `EmailThread` object | Not added | Thread context can be reconstructed from provider identifiers/headers | durable thread semantics become necessary for policy/workflow |
| First-class `FollowUp` object / mini CRM | Not added | Simple follow-up state belongs to Hermes Cron; durable multi-step work can use Kanban | real business state requires a durable domain object beyond Cron/Kanban |
| Email attachments | Deferred | Adds content handling, malware/privacy, storage, approval-hash, and provider complexity | a real approved use case requires governed attachments |
| Email Bcc | Deferred | Not needed for the first governed send loop and expands approval/material-state semantics | an approved workflow requires it |

The scope-control rule is:

> **Do not re-add a removed/deferred capability merely because it is technically possible. Reintroduce it only when observed business value exceeds the additional security, maintenance, and operational complexity.**

## Current v2 installation-design result

| ID | Work package | Result |
| --- | --- | --- |
| ID-1 | Installation architecture + v1 preservation | ✅ Complete |
| ID-2 | Company config + protected-input contract | ✅ Complete |
| ID-3 | Stage sequencing + capability closure | ✅ Complete |
| ID-4 | Trusted identity + mailbox authorization propagation | ✅ Complete |
| ID-5 | Draft / approval governance runtime | ✅ Complete |
| ID-6 | Governed send + reconciliation | ✅ Complete |
| ID-7 | Rollback / recovery / clean-host acceptance | ✅ Complete |

Final review: [`docs/V2-INSTALLATION-DESIGN-REVIEW.md`](docs/V2-INSTALLATION-DESIGN-REVIEW.md).

Current repository state is intentionally:

```text
current_phase: installation_design
installation_design.status: complete
installation_design.transition_ready: true
blueprint_validation.status: not_opened
real_deployment_task.active: false
```

Completion does **not** automatically change lifecycle phase or authorize a real deployment.

## What is planned next

### Next blueprint milestone — Blueprint Validation

The next major repository task is to prove that a **fresh capable AI engineering agent** can consume this repository without hidden chat context and reproduce the intended system on an explicitly approved clean validation target.

Blueprint Validation should verify:

- clean-host preflight and target-state resolution;
- deterministic v1 installation / preservation;
- v2 capability installation sequence;
- protected-input handling;
- identity / authorization propagation;
- governance runtime initialization and migration;
- provider adapters with synthetic or controlled inputs;
- stage-by-stage acceptance;
- backup / restore;
- restart / failure recovery;
- installer re-run convergence;
- v2 rollback with v1 preservation;
- evidence recording sufficient for a new agent to continue safely.

### Later repository milestone — Release Ready

After Blueprint Validation findings are resolved:

- consolidate validation evidence;
- fix genuine reproducibility gaps;
- harden only where validation proves necessary;
- declare `RELEASE READY` when the repository adequately explains both system intent and installation execution.

### Future capabilities outside the current baseline

Potential later extensions, only when justified by real usage:

- Stage 5 simple communication follow-up through Hermes Cron;
- Stage 6 employee messaging surface;
- additional Email providers;
- governed attachments;
- governed Bcc support;
- richer operator reconciliation tooling;
- broader enterprise-system integrations;
- additional identity-provider-specific playbooks.

## Lifecycle vs deployment readiness

### Blueprint maturity

```text
SYSTEM DESIGN COMPLETE          ✅
INSTALLATION DESIGN COMPLETE    ✅
BLUEPRINT VALIDATED             ⏳
RELEASE READY                   ⏳
```

### Deployment-target readiness

```text
CORE READY
= baseline employee workflow works

CONFIGURED READY
= Core Ready
  + every company-enabled capability is deployed and accepted

PRODUCTION READY
= Configured Ready
  + applicable recovery/security/access/operations controls pass
```

## Source-of-truth map

| Information | Authority |
| --- | --- |
| Blueprint lifecycle / real deployment gate | `state/PROJECT-PHASE.yaml` |
| System & installation blueprint | normative repository contracts |
| Company knowledge | WeKnora |
| Agent role / behavior / tools | Hermes Profiles / SOUL / Skills / tools |
| Employee Web identity/access | Open WebUI / selected enterprise identity layer |
| Mailbox and provider delivery facts | Email Provider |
| Draft / approval / governed-send evidence | EAO Governance layer |
| Durable Agent tasks | Hermes Kanban when enabled |
| Scheduled work | Hermes Cron when enabled |
| Desired deployment | company-private active configuration |
| Actual deployment | runtime + deployment state |

## Core design rules

### Human identity is not an Agent Profile

```text
HumanActor
≠ Hermes Profile
≠ provider/mailbox credential
```

### Knowledge is not memory

```text
WeKnora = authoritative shared company knowledge
Hermes memory = optional continuity state subject to isolation rules
```

### Natural language is not formal approval

A free-form message such as “send it” may express intent, but formal SendApproval must come through the deterministic trusted-human action path.

### Ambiguous external side effects fail safe

```text
SENT
→ never retry

CONFIRMED_NOT_SENT
→ controlled retry may be allowed inside the same logical send

OUTCOME_UNKNOWN
→ RECONCILIATION_REQUIRED
→ no blind retry
```

### Upstream first

```text
official upstream capability
→ official integration
→ configuration
→ thin adapter/playbook
→ custom infrastructure only when necessary
```

## First validated core stack

```text
Host: Apple Silicon macOS
Container runtime: OrbStack / Docker
WeKnora: v0.8.0
Hermes Agent: v0.21.0, host-native
Open WebUI: v0.11.3
Employee Hermes long-term memory: disabled
```

Machine-readable baseline: [`config/validated-stack.yaml`](config/validated-stack.yaml).

Reference-instance evidence: [`state/DEPLOYMENT-STATE.md`](state/DEPLOYMENT-STATE.md).

A fresh deployment should use [`state/DEPLOYMENT-STATE.template.md`](state/DEPLOYMENT-STATE.template.md).

## Install with an AI agent

For blueprint validation or an explicitly authorized deployment, read in this order:

1. [`AGENTS.md`](AGENTS.md)
2. [`state/PROJECT-PHASE.yaml`](state/PROJECT-PHASE.yaml)
3. [`DEPLOY.md`](DEPLOY.md)
4. [`docs/COMPLETENESS.md`](docs/COMPLETENESS.md)
5. active company configuration based on [`config/company.example.yaml`](config/company.example.yaml)
6. [`config/capabilities.yaml`](config/capabilities.yaml)
7. [`config/validated-stack.yaml`](config/validated-stack.yaml)
8. referenced infrastructure playbooks / adapters
9. [`docs/ACCEPTANCE-TESTS.md`](docs/ACCEPTANCE-TESTS.md)

For v2 Email specifically, continue with:

1. [`docs/V2-SCOPE.md`](docs/V2-SCOPE.md)
2. [`docs/V2-EMAIL-DESIGN.md`](docs/V2-EMAIL-DESIGN.md)
3. [`docs/V2-INSTALLATION-ARCHITECTURE.md`](docs/V2-INSTALLATION-ARCHITECTURE.md)
4. [`docs/V2-CONFIG-PROTECTED-INPUTS.md`](docs/V2-CONFIG-PROTECTED-INPUTS.md)
5. [`docs/V2-STAGE-CONTRACTS.md`](docs/V2-STAGE-CONTRACTS.md)
6. [`docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`](docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md)
7. [`docs/V2-GOVERNANCE-RUNTIME.md`](docs/V2-GOVERNANCE-RUNTIME.md)
8. [`docs/V2-SEND-RECONCILIATION.md`](docs/V2-SEND-RECONCILIATION.md)
9. [`docs/V2-RECOVERY-CLEAN-HOST.md`](docs/V2-RECOVERY-CLEAN-HOST.md)
10. [`docs/V2-INSTALLATION-DESIGN-REVIEW.md`](docs/V2-INSTALLATION-DESIGN-REVIEW.md)

## Capability-driven extension

Optional capabilities are installed only when selected by company configuration.

| Capability | Reference path |
| --- | --- |
| Specialist Profiles | `docs/PROFILE-STANDARD.md` + Hermes specialist templates |
| Hermes admin Web UI | `infrastructure/hermes-webui/` |
| Codex / Claude Code delegation | `infrastructure/coding-agents/` |
| Kanban / Cron / Messaging | `infrastructure/hermes/features/` |
| Tencent Enterprise Mail | `infrastructure/email/tencent-exmail/` |
| Remote/private access / SSO | `infrastructure/access/` |
| Employee long-term memory | Profile/RBAC isolation gate |

An enabled capability may not be silently skipped to manufacture a green result. A disabled capability should not be instantiated merely because a template exists.

## Repository self-check

```sh
sh scripts/repository-readiness-check.sh
```

Relevant offline v2 contract checks:

```sh
python3 infrastructure/email/governance/test_schema.py
python3 infrastructure/email/governance/test_send_reconciliation.py
python3 infrastructure/email/governance/test_recovery.py
python3 infrastructure/email/tencent-exmail/test_imap_readonly.py
python3 infrastructure/email/tencent-exmail/test_smtp_send_adapter.py
```

Static/offline PASS is blueprint evidence only. It does not replace acceptance on an explicitly approved validation/deployment target.

## Documentation map

| Document | Purpose |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | AI agent operating contract |
| [`state/PROJECT-PHASE.yaml`](state/PROJECT-PHASE.yaml) | blueprint lifecycle + real deployment gate |
| [`DEPLOY.md`](DEPLOY.md) | installation/deployment Golden Path |
| [`docs/COMPLETENESS.md`](docs/COMPLETENESS.md) | readiness semantics |
| [`docs/V2-PHASE-STATUS.md`](docs/V2-PHASE-STATUS.md) | current v2 blueprint status |
| [`docs/V2-SCOPE.md`](docs/V2-SCOPE.md) | v2 scope + explicit reductions / non-goals |
| [`docs/V2-EMAIL-DESIGN.md`](docs/V2-EMAIL-DESIGN.md) | governed email system design |
| [`docs/V2-DESIGN-REVIEW.md`](docs/V2-DESIGN-REVIEW.md) | System Design final review |
| [`docs/V2-INSTALLATION-ARCHITECTURE.md`](docs/V2-INSTALLATION-ARCHITECTURE.md) | ID-1 architecture / v1 preservation |
| [`docs/V2-CONFIG-PROTECTED-INPUTS.md`](docs/V2-CONFIG-PROTECTED-INPUTS.md) | ID-2 config + secret-input contract |
| [`docs/V2-STAGE-CONTRACTS.md`](docs/V2-STAGE-CONTRACTS.md) | ID-3 stage closure contracts |
| [`docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`](docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md) | ID-4 trusted identity / authorization propagation |
| [`docs/V2-GOVERNANCE-RUNTIME.md`](docs/V2-GOVERNANCE-RUNTIME.md) | ID-5 governance runtime |
| [`docs/V2-SEND-RECONCILIATION.md`](docs/V2-SEND-RECONCILIATION.md) | ID-6 governed send / reconciliation |
| [`docs/V2-RECOVERY-CLEAN-HOST.md`](docs/V2-RECOVERY-CLEAN-HOST.md) | ID-7 recovery / clean-host contract |
| [`docs/V2-INSTALLATION-DESIGN-REVIEW.md`](docs/V2-INSTALLATION-DESIGN-REVIEW.md) | Installation Design final review |
| [`docs/ONTOLOGY.md`](docs/ONTOLOGY.md) | governed operational object/action contract |
| [`docs/ACCEPTANCE-TESTS.md`](docs/ACCEPTANCE-TESTS.md) | deployment readiness evidence suite |
| [`docs/acceptance/TENCENT-EXMAIL.md`](docs/acceptance/TENCENT-EXMAIL.md) | Tencent Exmail acceptance contract |
| [`docs/BACKUP-RESTORE.md`](docs/BACKUP-RESTORE.md) | backup / restore standard |
| [`docs/OPERATIONS.md`](docs/OPERATIONS.md) | operations / troubleshooting |
| [`docs/SECURITY.md`](docs/SECURITY.md) | trust / secrets / least privilege |
| [`state/DEPLOYMENT-STATE.template.md`](state/DEPLOYMENT-STATE.template.md) | clean deployment state template |

## What this project is not

Enterprise AI Office is not intended to become:

- a new RAG engine;
- a new general Agent framework;
- a WeKnora / Hermes / Open WebUI fork;
- a CRM or ERP;
- a generic workflow engine;
- a replacement for Codex or Claude Code;
- an “install every feature” component collection.

Its value is the **system design + installation design**, capability-driven desired state, governance boundaries, thin upstream adapters, recovery rules, acceptance evidence, and operating discipline around mature projects.

## ARMOR reference

ARMOR is the first reference implementation, while the project itself remains generic.

ARMOR-specific design and lessons belong under [`reference/armor/`](reference/armor/) and must not override another adopter's private configuration.

## License

Licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

Independent upstream software retains its own licenses and terms. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).