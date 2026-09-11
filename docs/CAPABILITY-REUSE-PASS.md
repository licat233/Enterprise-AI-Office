# Capability Reuse Pass

> Mandatory decision gate before adding a new component, service, database, Skill, MCP server, scheduler, workflow engine, browser stack, memory layer, or external integration to Enterprise AI Office.

## Why this exists

Enterprise AI Office deliberately prefers a small number of clear authorities:

- Open WebUI for the employee Web surface and human-facing resource access;
- Hermes Agent for Agent runtime, Profiles, Skills, Cron, Kanban, Gateway, and supported orchestration;
- WeKnora for shared enterprise knowledge;
- narrow approved capability adapters for external systems and governed side effects.

The system becomes harder to secure, reproduce, upgrade, and recover every time a second tool is introduced for a responsibility that an existing component already owns.

Therefore a new capability is not justified merely because a tool exists or is popular.

## Mandatory search order

Before proposing a new implementation, inspect in this order:

1. Existing EAO repository capability, script, adapter, or runbook.
2. Hermes native capability.
3. Installed, migrated, or frozen Hermes Skills.
4. Open WebUI native capability.
5. WeKnora native capability.
6. Existing EAO email/governance capability where relevant.
7. Official upstream capability or supported integration of the selected component.
8. A thin adapter around an existing authority.
9. New infrastructure only after every earlier option is proven insufficient.

Do not state that “EAO cannot do X” until this pass has been completed against repository and, where relevant, runtime evidence.

## Required decision record

For a material new capability, record at least:

| Field | Required answer |
| --- | --- |
| Business requirement | What concrete work cannot currently be completed? |
| Existing EAO check | Which current capabilities were inspected? |
| Hermes native check | Is there a Profile, Skill, Cron, Kanban, Gateway, MCP, or other native path? |
| Existing Skill check | Which installed/frozen Skills were inspected? |
| Open WebUI check | Can the employee/client requirement be handled natively? |
| WeKnora check | Can the knowledge requirement be handled without another RAG/vector layer? |
| Official upstream check | Does the selected upstream already provide the capability? |
| Gap | What exact requirement remains unsatisfied? |
| Proposed addition | Smallest change that closes only that gap |
| New authority/state | Does it introduce a new database, scheduler, credential store, user directory, queue, or source of truth? |
| Security impact | New privileges, external side effects, secrets, network listeners, or data exposure |
| Maintenance impact | Upgrade, backup, monitoring, recovery, and operator burden |
| Rollback | How the addition can be removed while preserving the existing system |
| Acceptance | Observable test proving the capability works and its boundaries hold |

If the gap cannot be stated precisely, do not add the component.

## Decision rule

Prefer:

```text
reuse existing capability
→ enable/configure upstream capability
→ reuse approved Skill
→ narrow thin adapter
→ new infrastructure only as last resort
```

A new component is justified only when:

```text
measurable business value
>
security + maintenance + recovery + cognitive complexity
```

## Examples

### Scheduling

Bad default:

```text
Need a daily job
→ add n8n / Airflow / another scheduler
```

Required pass:

```text
Need a daily job
→ check Hermes Cron
→ use Hermes Cron if it safely expresses the job
```

A second scheduler requires a demonstrated Hermes limitation.

### Durable Agent work

Before adding a task queue or workflow database, check Hermes Kanban and the existing EAO governance layer.

### Knowledge

Before adding another vector database, RAG framework, or document store, check WeKnora and the existing WeKnora MCP/API path.

Company knowledge remains authoritative in WeKnora unless an explicit architecture decision changes that boundary.

### Employee portal

Before creating a new employee application, check whether Open WebUI can safely provide the required workflow and RBAC.

### Memory

Do not use Agent memory to repair a missing company fact, workflow rule, source-governance problem, or runtime configuration defect. Repair the owning source instead.

### Web research

Before installing another search/browser stack, inspect the frozen Enterprise Web Research capability and the existing Hermes Operations route.

### Email

Before adding a generic IMAP/SMTP Agent tool, inspect the governed email capability. External send is a material side effect and must preserve human authority, approval evidence, and reconciliation behavior.

## Prohibited shortcuts

The following are not acceptable reasons for adding infrastructure:

- “It is easier for the Agent.”
- “The tool is popular.”
- “We might need it later.”
- “The Mac Studio has enough resources.”
- “The current component has not been checked yet.”
- “A second source of truth would be convenient.”
- “The feature can be implemented faster than learning the existing capability.”

## Agent behavior

When an AI Agent receives a new feature request:

1. Read `config/eao-manifest.yaml` and `config/capabilities.yaml`.
2. Search the repository for an existing implementation or frozen decision.
3. Inspect the relevant Hermes native feature and installed Skills.
4. Inspect relevant upstream documentation/version behavior when necessary.
5. Prefer configuration or reuse over construction.
6. If a real gap remains, propose the smallest addition and make its new operational burden explicit.
7. Preserve rollback and acceptance evidence.

The result of a Capability Reuse Pass may legitimately be:

```text
NO NEW COMPONENT REQUIRED
```

That is often the preferred outcome.
