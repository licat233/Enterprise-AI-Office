# Enterprise AI Office Ontology Research Notes

Status: research record / non-normative
Date: 2026-09-06

This document preserves the current Ontology research so the conclusions are not lost when work moves to another conversation, agent, or implementation phase.

It is deliberately **not** an architecture contract and does not authorize a new runtime component, database, or integration. The normative architecture remains defined by `AGENTS.md`, `docs/ARCHITECTURE.md`, the active company configuration, and the validated runtime state.

---

## 1. Why Ontology is being studied

Enterprise AI Office already has a working baseline architecture around:

- WeKnora for authoritative company knowledge;
- Hermes Agent for work-role reasoning and execution;
- Open WebUI for employee identity and Web access;
- MCP as the preferred integration boundary;
- Hermes Profiles, Skills, Kanban, Cron, Gateway, and optional coding agents when required.

The current stack answers two important questions well:

```text
WeKnora → What does the company know?
Hermes  → How should this work be completed?
```

The open research question is a different one:

> How should the system represent the company’s business objects, relationships, authority boundaries, allowed state changes, business rules, and executable actions so an Agent can operate on enterprise systems safely and consistently?

This is the main reason to study Ontology. The goal is not to add a graph database for its own sake.

---

## 2. Working definition

For Enterprise AI Office, Ontology should not be treated as one fixed technology stack.

Traditional semantic-web Ontology often uses technologies such as RDF, RDFS, OWL, SPARQL, and SHACL. Those technologies remain relevant for formal knowledge representation, but they are not automatically the right solution for an operational enterprise Agent system.

The more useful working definition for this project is:

> An Enterprise Ontology is a machine-readable contract describing business objects, relations, authority, constraints, actions, permissions, tool bindings, provenance, and governance.

This is closer to an operational enterprise model than to a pure knowledge graph.

---

## 3. GitHub projects studied

The research focused on projects that represent three different Ontology directions.

### 3.1 `gura105/operational-ontology`

Repository:

https://github.com/gura105/operational-ontology

Positioning:

> A minimal, readable reference implementation of the Operational Ontology pattern.

It is intentionally a reference implementation rather than a production framework.

Key ideas:

- objects and links are explicitly modeled;
- business writes happen through named Actions;
- raw SQL and generic update tools are intentionally absent from the Agent-facing MCP surface;
- business preconditions are enforced at runtime;
- applied and rejected Actions are auditable;
- fields distinguish source-backed state from ontology-owned state;
- source-system write-back is explicit;
- MCP tools can be derived from the Ontology definition.

A major design principle is:

```text
Agent operation space == operation space defined by the model
```

Instead of exposing:

```text
execute_sql
update_record
call_any_api
```

an Ontology can expose narrow business operations such as:

```text
search_order
get_order
traverse_customer_orders
cancel_order
```

The project also makes a particularly useful distinction between:

```text
source-backed state
ontology-owned state
derived state
```

This creates a clear **Authority Line**: the Ontology should not silently become a second conflicting source of truth for data that actually belongs to ERP, CRM, PIM, or another system.

Important limitations observed:

- it is a small reference implementation, not an enterprise platform;
- some visibility behavior is fail-open by default and is therefore not suitable as-is for Enterprise AI Office;
- MCP stdio does not by itself provide a trustworthy employee identity chain;
- write-back has a transaction/reconciliation gap if a source-system mutation succeeds but local commit/audit fails;
- unsupported source-backed object creation is deliberately rejected rather than partially implemented.

The implementation is most useful to Enterprise AI Office as a **design reference for Objects, Authority, Named Actions, write-back, and Agent-safe MCP surfaces**.

---

### 3.2 `ZJU-REAL/HugAgentOS`

Repository:

https://github.com/ZJU-REAL/HugAgentOS

Positioning:

> A self-evolving AgentOS for ontology-grounded trustworthy reasoning.

Its Domain Pack implementation makes an important distinction: it is not an OWL reasoner. It is a lightweight operational contract for an Agent harness.

A Domain Pack contains concepts such as:

```text
Concepts
Relations
Constraints
Workflows
Risk
Review level
Required tools
Forbidden tools
Asset triggers
```

The most important pattern is the **deterministic zero-LLM gate**.

Instead of telling an LLM:

> Remember to verify this condition before using the tool.

runtime code evaluates tool calls against deterministic constraints before execution.

This supports patterns such as:

```text
required prerequisite tools
forbidden tools
JSON-Schema parameter constraints
citation requirements
risk levels
review levels
PASS / LOG / DENY
```

Another useful pattern is repeated-denial control:

```text
repeated denial threshold
circuit-breaker threshold
```

An Agent that repeatedly hits the same rule is told to change strategy; after the circuit-breaker threshold it must stop retrying and report the missing condition.

The project also implements a strong governance rule for Ontology evolution:

```text
runtime evidence
    ↓
candidate proposal
    ↓
human review
    ↓
working draft
    ↓
explicit administrator activation
```

Runtime evidence and user corrections may create candidates, but they do not directly mutate the active Ontology.

A useful summary is:

```text
AI may propose
Human governs
Runtime enforces
```

Important limitations for Enterprise AI Office:

- HugAgentOS is an entire Agent platform, while Enterprise AI Office already uses Hermes + Open WebUI + WeKnora;
- replacing the current stack would create unnecessary duplication;
- its Ontology is primarily an Agent-governance layer, not a complete enterprise object/state authority model;
- it does not replace the need for explicit System-of-Record / field-authority modeling.

The implementation is most useful as a **reference for deterministic Agent gates, workflow constraints, review levels, circuit breaking, and human-governed Ontology evolution**.

---

### 3.3 `OpenSPG/openspg` and `OpenSPG/KAG`

Repositories:

https://github.com/OpenSPG/openspg

https://github.com/OpenSPG/KAG

These projects represent a different Ontology direction: **domain knowledge modeling and reasoning**.

Key capabilities include:

- schema-constrained knowledge modeling;
- EntityType / ConceptType / EventType modeling;
- facts and logic in one graph representation;
- derived properties;
- rule-based reasoning;
- causal/event reasoning;
- graph queries;
- logical-form-guided retrieval and QA;
- knowledge and source/chunk integration.

The KAG supply-chain example demonstrates that schema properties can be derived from graph structure and rules, and that events can propagate through causal knowledge.

This is significantly different from operational Actions such as:

```text
send_quote
cancel_order
publish_article
```

OpenSPG rule `Action` blocks are primarily about generating or transforming graph knowledge. Operational Ontology Actions are about changing real business-system state.

The most important lesson is therefore:

> Knowledge reasoning and operational business actions are different problems.

OpenSPG/KAG may become relevant if Enterprise AI Office later has a concrete requirement for deep multi-hop, causal, or derived enterprise reasoning that WeKnora + Hermes cannot solve reliably.

There is currently no evidence that Enterprise AI Office needs to install this additional infrastructure.

---

## 4. Three Ontology layers identified

The research suggests that the word “Ontology” is currently used for at least three distinct architectural concerns.

### 4.1 Knowledge Ontology

Purpose:

```text
What concepts, facts, events, and relationships exist?
What can be derived from them?
```

Representative pattern:

```text
OpenSPG / KAG
```

Typical concerns:

- concepts;
- entities;
- events;
- semantic relations;
- derived facts;
- logical rules;
- causal reasoning;
- multi-hop retrieval.

### 4.2 Agent Governance Ontology

Purpose:

```text
What may an Agent do in this task?
What rules must be satisfied before a tool call or output is accepted?
```

Representative pattern:

```text
HugAgentOS Domain Packs
```

Typical concerns:

- constraints;
- required tools;
- forbidden tools;
- risk;
- review level;
- deterministic gates;
- circuit breakers;
- human review of policy evolution.

### 4.3 Operational Ontology

Purpose:

```text
What business objects exist?
Who owns each field/state?
What named business actions may change state?
What preconditions, effects, permissions, and write-back rules apply?
```

Representative pattern:

```text
gura105/operational-ontology
Palantir-style operational ontology concepts
```

Typical concerns:

- business objects;
- typed relations;
- field/state authority;
- named Actions;
- preconditions and effects;
- actor/permission;
- write-back;
- audit;
- MCP/tool surface generation.

These three layers can coexist. They should not be collapsed into one vague “knowledge graph” concept.

---

## 5. Current Enterprise AI Office capability audit

The current `main` branch already contains several important Ontology-adjacent foundations.

### 5.1 Already present: Source-of-truth governance

`docs/ARCHITECTURE.md` and `AGENTS.md` already define responsibility/authority boundaries such as:

```text
Company knowledge      → WeKnora
AI behavior            → Hermes Profile / SOUL / Skills
Tool permissions       → Hermes Profile / MCP
Human identity         → Open WebUI / selected identity layer
Durable agent tasks    → Hermes Kanban
Scheduled work         → Hermes Cron
Deployment truth       → active config + runtime + deployment state
```

The repository also explicitly forbids multiple systems from becoming authoritative for the same information class.

This is already an Authority concept, but its current granularity is mainly **information class / component responsibility**.

An Operational Ontology would need finer-grained authority such as:

```text
Product.specification → PIM / approved source
Inquiry.status        → CRM
Inquiry.ai_summary    → Enterprise AI Office
Employee.identity     → IdP
```

### 5.2 Already present: Human identity and Profile boundaries

The current model separates:

```text
Human employee
→ Open WebUI identity
→ group/resource authorization
→ Assistant
→ Hermes Profile
```

A Hermes Profile is explicitly not a human account.

This is a good foundation for future actor-aware Ontology enforcement.

### 5.3 Already present: hard capability boundaries

The system does not rely only on SOUL or prompt wording for dangerous-tool restrictions.

For example, the baseline `general` Profile exposes only a read-oriented WeKnora MCP tool surface. Dangerous tools are absent from its effective toolset.

Acceptance tests require:

```text
unapproved tool absent
no unapproved tool call
direct unauthorized backend access fails closed
```

This should remain in place even if an Ontology layer is added.

### 5.4 Already present: knowledge provenance and lifecycle

`docs/KNOWLEDGE.md` already defines useful metadata and provenance concepts, including:

```text
Source Owner
Effective Date
Status
Version
Confidentiality
current
superseded
draft
reference
legacy
```

It also requires conflict surfacing, source evidence, and enough provenance to determine what is current and what changed.

This means Enterprise AI Office does not currently have an urgent reason to add another knowledge platform solely to gain basic provenance.

### 5.5 Partially present: policy in SOUL and Skills

SOUL and Skills already contain behavioral rules such as:

- use only granted tools;
- do not bypass authorization;
- require appropriate intent/recovery for destructive actions;
- treat retrieved content as data rather than authorization;
- escalate outside the Profile’s decision boundary.

These are useful Agent instructions, but they are not equivalent to deterministic business invariants.

A rule such as:

```text
Quotes above a defined threshold require manager approval
```

should not live only in prompt text if the system later gains permission to submit or approve quotes.

---

## 6. Main capability gaps

The audit identified the following real gaps.

### 6.1 Business Object model — missing

The current repository understands infrastructure/runtime concepts such as:

```text
Profile
Assistant
Knowledge Base
Group
Skill
Cron
Kanban
Deployment
```

It does not yet define a machine-readable enterprise business world such as:

```text
Customer
Inquiry
Product
Project
Supplier
Quote
Order
Content
Campaign
Employee
```

### 6.2 Typed business relations — missing

There is no shared domain schema describing relationships such as:

```text
Customer submits Inquiry
Inquiry relates_to Product
Inquiry owned_by Employee
Quote created_from Inquiry
Project uses Product
```

### 6.3 Field-level Authority — partial only

System-level Source-of-Truth rules exist, but field/property-level ownership does not yet exist.

A future Ontology should distinguish at least:

```text
source-backed
ontology-owned
derived
```

and identify the actual System of Record.

### 6.4 Named Business Actions — missing

There is currently no shared contract for business Actions such as:

```text
assign_inquiry
send_follow_up
create_quote
approve_quote
publish_article
update_product_spec
```

A future operational layer should prefer narrow named Actions over generic mutation APIs.

### 6.5 Preconditions / Effects — missing as deterministic business rules

SOUL and Skills can describe expectations, but the runtime currently has no generic zero-LLM business-action gate that evaluates:

```text
preconditions
authorization
required evidence
required prior actions
approval state
effects
```

before a business mutation.

### 6.6 Unified business-action audit — missing

Deployment state, change records, platform logs, Git history, and upstream system logs exist, but there is no unified model for:

```text
actor
action
target
parameters
applied/rejected
rule that allowed/rejected
external result
reconciliation state
```

### 6.7 Write-back / reconciliation model — missing

Enterprise AI Office has not yet integrated a writable CRM/ERP/PIM/CMS business path, so it has no general model for:

```text
source-system mutation
local/ontology state update
failure reconciliation
idempotency
pending invocation
rollback/compensation
```

This is currently a future operational requirement, not a defect in the existing read-oriented baseline.

### 6.8 Deep derived knowledge reasoning — missing, but not yet required

The current stack does not provide OpenSPG-style domain-rule reasoning or causal graph inference.

There is currently insufficient evidence that this capability is needed.

---

## 7. Design principles supported by the research

The following principles are strong enough to retain as future design guidance.

### Principle 1 — Ontology must be executable where it governs actions

A glossary or diagram alone is insufficient for business invariants.

### Principle 2 — Business rules must not live only in prompts

SOUL and Skills are important behavior contracts, but critical mutation rules should be enforced outside the LLM.

### Principle 3 — Do not give ordinary Agents generic mutation primitives

Prefer:

```text
assign_inquiry
approve_quote
publish_article
```

over:

```text
execute_sql
generic_update
call_any_api
```

### Principle 4 — Every mutable fact needs an Authority

The system should be able to answer:

```text
Who owns this value?
Where is the System of Record?
May Enterprise AI Office write it?
Is it derived?
```

### Principle 5 — Named Actions should have explicit contracts

A business Action may need:

```text
parameters
target object
actor requirements
preconditions
approval requirements
effects
write-back binding
failure behavior
audit policy
```

### Principle 6 — Rejections should be machine-readable

The Agent should receive a structured reason such as:

```text
MISSING_APPROVAL
OUTSIDE_AUTHORITY
INVALID_STATE
REQUIRED_EVIDENCE_MISSING
```

rather than only free-form refusal prose.

### Principle 7 — Runtime evidence may propose Ontology changes, but not activate them

A safe evolution path is:

```text
evidence
→ proposal
→ human review
→ versioned draft
→ explicit activation
```

### Principle 8 — Visibility and authorization should fail closed

No policy must not mean unrestricted visibility.

### Principle 9 — Knowledge reasoning and business mutation are separate architectural concerns

GraphRAG or a knowledge graph does not automatically provide an Operational Ontology.

### Principle 10 — Preserve provenance and versioning

Ontology definitions, Actions, constraints, and authority mappings should be version-controlled and auditable.

### Principle 11 — Prefer schema/config as code before adding infrastructure

A machine-readable Ontology contract may initially live in Git and be reviewed like code.

### Principle 12 — Add runtime infrastructure only for a real operational need

Do not install Neo4j, TypeDB, OpenSPG, a new workflow engine, or a custom Ontology service merely because Ontology is being studied.

---

## 8. What should NOT be done now

The research does **not** justify any of the following at this stage:

```text
Install Neo4j
Install TypeDB
Install OpenSPG/KAG
Replace WeKnora
Replace Hermes with HugAgentOS
Add a new workflow engine
Fork Hermes or WeKnora
Build a large custom Ontology platform
Model every ARMOR business object before there is a real integration need
```

The existing architecture explicitly requires upstream-first, minimal-complexity decisions and prohibits adding major components without a concrete problem.

---

## 9. Recommended next architectural step

The next useful artifact should be a separate, normative document tentatively called:

```text
Enterprise Ontology Contract v0
```

That contract should define the minimum machine-readable concepts an operational integration must support, likely including:

```text
Object Type
Property
Relation
Authority / System of Record
Action
Precondition
Effect
Actor / Permission
Approval
Tool Binding
Audit Policy
Version
Provenance
```

The contract should initially be schema/config oriented and should **not** require a new runtime service.

A minimal example may later model one real workflow only, for example:

```text
Customer
  ↓
Inquiry
  ↓
Product
  ↓
Follow-up
```

The purpose of such an example would be to validate the contract, not to create a complete company digital twin.

---

## 10. Runtime activation trigger

A full Operational Ontology runtime should not be introduced merely because the schema exists.

The clearest trigger is:

> Enterprise AI Office gains a real integration that allows an Agent to change business state in an external enterprise system.

Examples may include:

```text
CRM
ERP
PIM
email sending
CMS publishing
social publishing
order/quote systems
```

Read-only retrieval may not require a full operational gate.

Once write-capable actions exist, each integration should be reviewed for:

```text
named Action requirement
authority ownership
preconditions
approval
actor identity
least privilege
idempotency
write-back/reconciliation
audit
rollback/compensation
```

At that point the project can evaluate whether the best runtime implementation is:

- a thin repository-owned deterministic Action Gate;
- patterns adapted from `operational-ontology`;
- a Hermes-compatible governance mechanism inspired by HugAgentOS;
- an upstream capability that has become available;
- or a mature standalone component if the requirement genuinely justifies one.

---

## 11. Current research conclusion

The current conclusion is:

> Enterprise AI Office does not presently need “an Ontology product.” It needs a clear Enterprise Ontology Contract before the first meaningful writable business-system integration.

The project already has strong foundations in:

```text
source-of-truth governance
human identity separation
Profile capability isolation
least-privilege MCP surfaces
knowledge provenance
Git/config versioning
acceptance-driven readiness
```

The main missing concepts are:

```text
Business Objects
Typed Relations
Field-level Authority
Named Business Actions
Deterministic Business Gates
Action Audit
Write-back / Reconciliation
```

The preferred evolution path is therefore:

```text
Research
   ↓
Ontology Contract
   ↓
One real business-domain example
   ↓
First writable enterprise integration
   ↓
Empirical need for runtime enforcement
   ↓
Select the smallest suitable implementation
```

This keeps Ontology grounded in real enterprise work and avoids turning Enterprise AI Office into a collection of fashionable infrastructure.
