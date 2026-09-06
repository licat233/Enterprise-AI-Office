# Enterprise Ontology Contract v0

Status: draft architecture contract
Version: 0.1.0
Date: 2026-09-06

This document defines the minimum Ontology contract for Enterprise AI Office.

It converts the findings in `docs/ONTOLOGY-RESEARCH.md` into a reusable architecture contract while deliberately avoiding premature runtime implementation.

This contract does **not** authorize a new database, graph engine, reasoning service, or custom orchestration platform. It does not replace WeKnora, Hermes Agent, Open WebUI, MCP, existing RBAC, or existing Profile capability boundaries.

Until a writable enterprise-system integration requires runtime enforcement, this document is a **design-time contract only**.

If this document conflicts with `AGENTS.md`, the active company configuration, an approved architecture decision, or actual security constraints, the higher-priority contract wins.

---

## 1. Purpose

Enterprise AI Office already defines:

```text
WeKnora → authoritative company knowledge
Hermes  → agent reasoning and work execution
Open WebUI → employee identity and Web access
Profiles / MCP → capability boundaries
```

The Ontology contract addresses a different problem:

> How should Enterprise AI Office represent business objects, relationships, authority, business actions, constraints, tool bindings, and audit requirements so Agents can operate on enterprise systems safely and consistently?

The immediate goal is to standardize the model before selecting or building any runtime.

---

## 2. Scope

The minimum Enterprise Ontology model covers:

```text
Object Types
Properties
Relation Types
Authority
Named Actions
Preconditions
Effects
Actor / Permission Requirements
Approval Requirements
Tool Bindings
Audit Policy
Versioning
```

The contract may later expand only when a real business requirement justifies it.

---

## 3. Non-goals

This contract does not require:

- RDF;
- OWL;
- SPARQL;
- SHACL;
- Neo4j;
- TypeDB;
- OpenSPG/KAG;
- a dedicated Ontology database;
- a separate Agent framework;
- automatic knowledge-graph construction;
- automatic ontology evolution;
- replacing WeKnora retrieval;
- replacing Hermes Skills or SOUL;
- replacing Open WebUI identity/RBAC;
- replacing Profile-scoped tool or credential isolation.

A future implementation may use one of these technologies, but only after a concrete requirement demonstrates that the existing stack plus a thin contract/runtime cannot solve the problem cleanly.

---

## 4. Core principles

### 4.1 One authority per mutable fact

Every mutable business property must have a declared authority.

The model must be able to answer:

```text
Who owns this value?
Where is the System of Record?
May Enterprise AI Office write it?
Is it derived rather than directly owned?
```

Do not allow two systems to become silently authoritative for the same fact.

### 4.2 Named business actions over generic mutation

Prefer narrow business operations such as:

```text
assign_inquiry
send_follow_up
approve_quote
publish_article
```

over generic primitives such as:

```text
execute_sql
update_record
call_any_api
```

The Agent-facing operation space should be no broader than the approved business-operation space.

### 4.3 Critical business rules must not live only in prompts

SOUL and Skills may explain policy and guide reasoning.

Critical mutation rules must eventually be enforced deterministically outside the LLM when the corresponding action becomes operational.

### 4.4 Authorization fails closed

No applicable policy, unresolved actor identity, unresolved authority, unresolved tool binding, or unresolved required approval must not silently become allow.

### 4.5 AI may propose; humans govern; runtime enforces

Ontology changes may be suggested from runtime evidence, user corrections, audits, or domain review.

They must not automatically alter the active production contract.

### 4.6 Knowledge reasoning and business mutation are separate concerns

A knowledge graph or GraphRAG system does not by itself provide safe operational actions.

An Operational Ontology does not by itself replace knowledge retrieval or deep domain reasoning.

---

## 5. Object Types

An Object Type represents a stable business concept whose instances may be referenced, queried, related, or acted upon.

Examples may include:

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

Do not define object types merely for taxonomy completeness.

Create an Object Type only when at least one real workflow needs to:

- identify instances;
- read properties;
- traverse relationships;
- apply business rules;
- execute or audit actions.

Each Object Type should define at minimum:

```text
id
name
primary key / stable identity source
description
properties
relations
authority defaults if any
```

---

## 6. Properties

A Property is a typed value belonging to an Object Type.

A Property definition should support, where relevant:

```text
name
type
required / optional
sensitivity
mutability
authority
source binding
validation constraints
```

Example:

```yaml
properties:
  status:
    type: string
    authority: crm
    mutable: true
  ai_summary:
    type: string
    authority: enterprise-ai-office
    mutable: true
```

The contract should avoid duplicating detailed validation rules until a real integration needs them.

---

## 7. Relation Types

Relations describe business meaning between Object Types.

Examples:

```text
Customer submits Inquiry
Inquiry relates_to Product
Inquiry owned_by Employee
Quote created_from Inquiry
Project uses Product
```

Relations should be explicit when business rules, traversal, permissions, or actions depend on them.

A relation may later require:

```text
source type
target type
cardinality
authority
properties on the relation
validity period
```

Do not force every real-world association into the Ontology if no workflow uses it.

---

## 8. Authority model

Every operational property or relation should resolve to one of the following authority classes.

### 8.1 `source-backed`

A real external System of Record owns the value.

Examples:

```text
Inquiry.status → CRM
Product.base_price → ERP/PIM
Employee.identity → IdP
```

Enterprise AI Office may read it and may write it only through an explicitly approved write-back Action.

### 8.2 `ontology-owned`

Enterprise AI Office owns the value because no external System of Record does.

Examples may include:

```text
Inquiry.ai_summary
Inquiry.ai_triage_note
Content.ai_review_state
```

This class should be used sparingly. It must not become a shadow copy of source-system state.

### 8.3 `derived`

The value is computed from other authoritative data or rules.

Examples:

```text
Inquiry.days_open
Customer.open_inquiry_count
Project.risk_summary
```

Derived data must retain enough provenance to explain its inputs or rule version when material.

### 8.4 Unresolved authority

If authority cannot be determined for a mutable field required by an Action, the correct result is:

```text
BLOCKED — AUTHORITY UNRESOLVED
```

Do not guess ownership.

---

## 9. Named Actions

A Named Action is the only approved abstraction for a business-state mutation governed by the Ontology.

Examples:

```text
assign_inquiry
send_follow_up
create_quote
approve_quote
publish_article
update_product_spec
```

An Action contract should support:

```text
name
target object type
parameters
actor requirements
preconditions
approval requirements
effects
authority/write-back target
tool binding
failure behavior
audit policy
```

An Action is not merely a prompt instruction.

When runtime enforcement exists, all callers should pass through the same Action contract rather than duplicating rules separately for chat, automation, messaging, or another client.

---

## 10. Preconditions

Preconditions are deterministic requirements evaluated before a governed business Action executes.

Examples:

```text
Inquiry.status != closed
Quote.total <= actor.approval_limit
Customer.email exists
Required evidence has been retrieved
Required prior step completed
Human approval exists
```

A failed precondition should return a structured denial rather than only prose.

Example result:

```json
{
  "allowed": false,
  "code": "MISSING_APPROVAL",
  "message": "Manager approval is required before this quote can be submitted."
}
```

Minimum design requirement:

```text
PASS
DENY
BLOCKED
```

A future runtime may also support advisory/log-only rules, but they must be distinguishable from enforced rules.

---

## 11. Effects

Effects describe the intended state changes of a successful Action.

They should distinguish:

```text
external source-system mutation
ontology-owned mutation
derived-state invalidation/recalculation
notification/delivery side effect
audit event
```

Effects are part of the Action contract so the system can reason about expected outcomes and reconciliation.

Do not treat an arbitrary tool call as proof that the intended business effect occurred.

---

## 12. Actor and permission requirements

The Ontology must not replace the existing human identity and Profile capability model.

A future Action decision should combine:

```text
Human identity / RBAC
+
Hermes Profile capability boundary
+
Business Action rule
```

The system should be able to distinguish at least:

```text
human actor
Profile / Agent actor
service / automation actor
```

A natural-language request must not grant a new role, credential, or approval level.

If trusted actor identity cannot be propagated to the Action layer where the rule requires it, the Action must fail closed.

---

## 13. Approval requirements

Some Actions may require explicit approval.

The contract should support at least:

```text
none
explicit-human-approval
role-based-approval
```

Do not create approval bureaucracy for low-risk actions.

Approval should be required only where real business policy, financial risk, external publication, destructive impact, or legal/compliance responsibility justifies it.

An LLM deciding that “approval probably exists” is not approval.

---

## 14. Tool bindings

A Tool Binding connects a Named Action or read operation to an actual supported integration.

Example:

```text
send_follow_up
    ↓
crm.send_follow_up
```

or:

```text
publish_article
    ↓
cms.publish_article
```

Bindings should be explicit and narrow.

The Ontology contract should not depend on raw database access when a supported API/MCP/action surface exists.

Existing Enterprise AI Office policy still applies:

```text
official upstream capability
→ official extension/integration
→ configuration
→ thin adapter
→ custom infrastructure only if required
```

---

## 15. Agent-facing tool surface

Where practical, Agent-facing tools should reflect approved domain operations.

Preferred:

```text
search_inquiry
get_inquiry
assign_inquiry
send_follow_up
```

Avoid exposing broad mutation tools whose parameters allow the Agent to bypass business semantics.

The absence of a generic write tool is a security feature, not a limitation to work around.

---

## 16. Audit contract

A governed business Action should be auditable whether it succeeds or is rejected.

A future runtime audit record should be capable of storing:

```text
timestamp
actor identity
Profile / Agent identity
action name
target object / id
parameters or safe parameter summary
rule / contract version
decision
applied / rejected / blocked
structured reason code
external system result reference
reconciliation state
```

Do not store secrets unnecessarily in audit records.

Audit does not replace source-system native logs; it links the Enterprise AI Office decision to the external operation.

---

## 17. Write-back and reconciliation

When an Action mutates a source-backed property, the external System of Record remains authoritative.

A future runtime must therefore define how it handles:

```text
idempotency
pending invocation
external success + local failure
local success + external failure
retry policy
reconciliation
compensation / rollback where possible
```

A simple local state update after an external write is not automatically transactionally safe.

Do not claim strong consistency unless the actual integration provides it.

---

## 18. Provenance

Material derived facts and governed changes should preserve enough provenance to answer:

```text
What source or rule produced this?
Which contract version applied?
When did it become valid?
What changed it?
```

Existing WeKnora source provenance remains the authority for document-backed knowledge.

Ontology provenance should complement, not duplicate, that source evidence.

---

## 19. Versioning and change governance

Ontology definitions should be version-controlled.

A future machine-readable contract should use explicit version identifiers.

Changes that alter:

- authority;
- business-action eligibility;
- approval requirements;
- actor permissions;
- destructive effects;
- external-system bindings;

must be treated as architecture/security-sensitive changes.

Recommended evolution model:

```text
runtime/user evidence
→ candidate
→ human/domain review
→ draft version
→ validation
→ explicit activation
```

No autonomous process may directly change the active production Ontology based only on LLM inference or user correction text.

---

## 20. Machine-readable representation

The contract intentionally does not choose a final schema language yet.

The first machine-readable representation should be simple, reviewable, and Git-friendly.

YAML is an acceptable starting point if it can represent the required concepts clearly.

Illustrative example only:

```yaml
schema_version: 0.1.0

domain: sales

objects:
  Inquiry:
    primary_key: id
    properties:
      status:
        type: string
        authority:
          class: source-backed
          system: crm
      ai_summary:
        type: string
        authority:
          class: ontology-owned
          system: enterprise-ai-office

  Customer:
    primary_key: id

relations:
  inquiry_customer:
    from: Inquiry
    to: Customer
    predicate: submitted_by

actions:
  send_follow_up:
    target: Inquiry
    parameters:
      inquiry_id:
        type: string
    preconditions:
      - rule: inquiry.status != closed
        code: INQUIRY_CLOSED
    approval:
      mode: none
    authority:
      system: crm
    tool_binding:
      tool: crm.send_follow_up
    audit:
      enabled: true
```

This example is a shape demonstration, not a frozen schema and not an instruction to implement a CRM integration.

---

## 21. First validation scenario

Do not model the entire company at once.

The first schema experiment should use one narrow real-world flow:

```text
Customer
   ↓ submits
Inquiry
   ↓ relates_to
Product
   ↓
Follow-up Action
```

The experiment should test whether the contract can express:

```text
object identity
relations
property authority
read scope
named Action
preconditions
actor requirement
approval requirement
tool binding
audit expectation
```

No production mutation is required for the first experiment.

---

## 22. Runtime activation trigger

Do not add an Ontology Runtime merely because this contract exists.

Runtime enforcement becomes a real requirement when Enterprise AI Office is granted the ability to change external business state through integrations such as:

```text
CRM
ERP
PIM
CMS
email
social publishing
other operational systems
```

A read-only integration does not automatically require a full Operational Ontology Runtime.

Before the first writable integration is enabled, perform an implementation decision using the repository's normal architecture rules.

At that point evaluate, in order:

1. whether the upstream system already provides a safe action/permission/workflow layer;
2. whether Hermes native capabilities can enforce the required boundary;
3. whether a thin deterministic Action Gate is sufficient;
4. whether a proven external Ontology/governance component is justified;
5. only then whether a new custom runtime is necessary.

---

## 23. Relationship to existing Enterprise AI Office components

### WeKnora

Remains the enterprise knowledge platform.

Ontology does not replace document retrieval, source evidence, parsing, embedding, or Knowledge Base management.

### Hermes Agent

Remains the primary Agent runtime.

Ontology may later constrain or shape Hermes tool execution, but should not duplicate Hermes as a second Agent platform.

### Open WebUI

Remains the baseline employee Web identity/client layer.

Ontology does not replace user authentication, group/resource RBAC, or conversation history.

### Hermes Profiles

Remain the AI-role and coarse capability boundary.

Ontology may add business-action constraints inside the already-authorized Profile capability space.

### SOUL and Skills

Remain important behavioral and workflow guidance.

They should explain business context and reasoning, but critical enforced mutation rules should not exist only as prompt text.

### MCP / APIs

Remain preferred integration boundaries.

Ontology should narrow and govern the exposed business operation space rather than encourage direct database coupling.

---

## 24. Readiness impact

This contract does not change the existing readiness definitions.

Current deployments may still reach:

```text
CORE READY
CONFIGURED READY
PRODUCTION READY
```

without an Ontology Runtime when no enabled capability requires governed business mutation.

Ontology is not deployment debt when the company has no writable enterprise-system requirement.

When a future enabled capability depends on Ontology enforcement, that capability must then receive:

```text
implementation path
security boundary
acceptance test
deployment-state records
```

through the existing capability-closure process.

---

## 25. Anti-patterns

Avoid:

- installing a graph database before a real use case exists;
- calling GraphRAG an Operational Ontology;
- duplicating ERP/CRM/PIM state into an AI-owned shadow database without clear authority;
- exposing generic write/SQL tools to ordinary Agents;
- encoding critical business invariants only in System Prompt or SOUL;
- allowing user text to become authorization;
- allowing LLM-generated Ontology changes to activate automatically;
- modeling every department, noun, and relationship before a workflow needs them;
- creating a new runtime when the upstream system already enforces the required action rules.

---

## 26. Minimum contract checklist

Before describing a future domain model as an Enterprise Ontology, confirm it can answer:

```text
[ ] What business Object Types exist for this workflow?
[ ] What stable identity identifies each object?
[ ] Which Properties matter?
[ ] Which Relations matter?
[ ] Who owns each mutable Property/Relation?
[ ] Which facts are source-backed, ontology-owned, or derived?
[ ] What Named Actions may change state?
[ ] What deterministic Preconditions apply?
[ ] Who may perform the Action?
[ ] Is human approval required?
[ ] Which real tool/API/MCP binding performs the Action?
[ ] What Effects are expected?
[ ] How are denial/failure reasons represented?
[ ] What must be audited?
[ ] How is the contract versioned and activated?
```

If these questions cannot be answered, the model is not yet ready to govern operational business actions.

---

## 27. Next implementation step

The next step after this contract is **not** to build a runtime.

Create one small, machine-readable example for the `Customer → Inquiry → Product → Follow-up` flow and use it to test whether the contract is clear enough in practice.

Only after that schema experiment should Enterprise AI Office decide whether the representation needs a formal schema language, validator, or runtime enforcement layer.
