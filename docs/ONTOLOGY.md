# Enterprise Ontology Contract v0

Status: draft architecture contract
Version: 0.3.0
Date: 2026-09-06

This document defines the minimum Ontology contract for Enterprise AI Office.

It converts the findings in `docs/ONTOLOGY-RESEARCH.md` into a reusable architecture contract while deliberately avoiding premature runtime implementation.

Version 0.2.0 incorporated the first machine-readable schema experiment under `ontology/examples/sales-inquiry.yaml`, which demonstrated that write governance alone is insufficient: read visibility, cross-object traversal, and read-operation authorization must also be explicit parts of the contract.

Version 0.3.0 incorporates the second machine-readable experiment under `ontology/examples/content-publication.yaml`, which demonstrated that approval must identify the exact subject state it authorizes when that subject can change between review and execution. An approval detached from immutable subject evidence can become stale while still looking valid.

This contract does **not** authorize a new database, graph engine, reasoning service, or custom orchestration platform. It does not replace WeKnora, Hermes Agent, Open WebUI, MCP, existing RBAC, or existing Profile capability boundaries.

Until an enabled enterprise-system integration requires runtime enforcement, this document is a **design-time contract only**.

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

> How should Enterprise AI Office represent business objects, relationships, authority, visibility, governed reads, business actions, constraints, approvals, tool bindings, and audit requirements so Agents can operate on enterprise systems safely and consistently?

The immediate goal is to standardize the model before selecting or building any runtime.

---

## 2. Scope

The minimum Enterprise Ontology model covers:

```text
Object Types
Properties
Relation Types
Object Visibility
Read Operations
Traversal Authorization
Authority
Named Actions
Preconditions
Effects
Actor / Permission Requirements
Approval Requirements
Approval Subject Binding
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

Critical read/write/approval invariants must eventually be enforced deterministically outside the LLM when the corresponding operation becomes operational.

### 4.4 Authorization fails closed

No applicable policy, unresolved actor identity, unresolved authority, unresolved visibility rule, unresolved traversal authorization, unresolved tool binding, unresolved approval subject, or unresolved required approval must not silently become allow.

This applies to both reads and writes.

### 4.5 Read authorization must be closed over the actual data path

Authorization to read one Object Type does not automatically authorize related objects reached through a relation.

If a read operation filters, projects, joins, traverses, or evaluates a precondition using another Object Type, Property, or Relation, the authorization decision must include that actual read path.

For example:

```text
search Inquiry
+ filter Customer.country
+ filter Product.product_family
```

requires authorization for the relevant Inquiry, Customer, Product, and relation reads. Entry-point authorization alone is insufficient.

### 4.6 Approval must bind to the subject state it authorizes

When an approval governs a mutable artifact or object that may change before execution, approval evidence must identify the exact subject state being authorized.

Depending on the domain, that may include:

```text
object id
revision/version
content hash
material property snapshot
state transition
quote total / commercial terms
other immutable evidence sufficient to identify the approved subject
```

A later change to any material approved input must invalidate or bypass neither the approval nor the review step.

For example:

```text
Content revision 7 approved
→ content changes to revision 8
→ revision 7 approval MUST NOT authorize publication of revision 8
```

The same principle applies to other mutable approved subjects such as quotations, purchase orders, specifications, external messages, or destructive plans when their material content may change after review.

Do not require hashes or version tokens mechanically when the subject is already immutable or approval and execution are one atomic trusted operation. Use the minimum binding evidence needed to prevent stale approval reuse.

### 4.7 AI may propose; humans govern; runtime enforces

Ontology changes may be suggested from runtime evidence, user corrections, audits, or domain review.

They must not automatically alter the active production contract.

### 4.8 Knowledge reasoning and business mutation are separate concerns

A knowledge graph or GraphRAG system does not by itself provide safe operational actions.

An Operational Ontology does not by itself replace knowledge retrieval or deep domain reasoning.

---

## 5. Object Types

An Object Type represents a stable business concept whose instances may be referenced, queried, related, reviewed, approved, or acted upon.

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
ReviewDecision
PublicationRecord
```

Do not define object types merely for taxonomy completeness.

Create an Object Type only when at least one real workflow needs to:

- identify instances;
- read properties;
- traverse relationships;
- apply business rules;
- review/approve an exact subject;
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
visibility/read requirements when access is not universally allowed
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
read restrictions when more specific than the object default
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

Property-level read restrictions should be added only when a real sensitivity or authorization boundary requires them; do not create field-level policy complexity for every property by default.

Where approval validity depends on a property, the approved value or a stable version/hash that covers it should be included in the approval subject binding.

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
Content has_review ReviewDecision
Content published_as PublicationRecord
```

Relations should be explicit when business rules, traversal, permissions, approvals, or actions depend on them.

A relation may later require:

```text
source type
target type
cardinality
authority
properties on the relation
validity period
read/traversal requirements
```

Do not force every real-world association into the Ontology if no workflow uses it.

### 7.1 Object Visibility

Object Visibility defines whether an actor is allowed to discover or read instances of an Object Type.

Visibility is distinct from data Authority:

```text
Authority  → who owns the fact and may change it
Visibility → who may see the fact/object
```

A source-backed object may still be hidden from an otherwise authenticated employee.

The default posture for enterprise operational objects should be fail closed unless a broader visibility rule is explicitly justified.

A machine-readable object definition should be able to express, where relevant:

```text
default visibility decision
required entitlement / role / group
actor or tenant scope
owner-based scope
sensitivity-driven restrictions
property-specific overrides
```

Illustrative shape:

```yaml
objects:
  Inquiry:
    visibility:
      default: deny
      read_requirements:
        - entitlement: sales.inquiry.read
```

Do not treat UI hiding as visibility enforcement. Direct read paths must obey the same effective policy.

If a visibility decision requires trusted human identity and that identity cannot be resolved at the enforcement point, the read must fail closed.

### 7.2 Read Operations

A Read Operation is an explicitly modeled way to query or retrieve Ontology objects without changing authoritative business state.

Examples:

```text
search_inquiries
get_inquiry
list_open_quotes
get_customer
get_content_for_review
get_publication_history
```

Read Operations are useful when a query has business semantics, cross-object filters, or authorization requirements that are broader than a generic object lookup.

A Read Operation should support, where relevant:

```text
name
target Object Type
actor requirements
allowed filters
allowed projections
allowed traversals
result visibility policy
tool/API/MCP binding
structured denial behavior
```

A read-only operation does not automatically need a dedicated Ontology Runtime. Existing upstream APIs/MCP tools may enforce the contract when they can do so reliably.

### 7.3 Traversal Authorization

Traversal Authorization governs access when a read or Action follows a relation or evaluates data on a related object.

Authorization must be closed over the actual traversal path.

Example:

```text
search_inquiries
  target: Inquiry
  filter: Customer.country
  filter: Product.product_family
```

The operation must not assume that `sales.inquiry.read` grants implicit access to Customer or Product data.

The effective read decision must satisfy all applicable requirements for:

```text
source object
traversed relation
target object
properties actually read
operation-specific entitlements
```

The same rule applies inside Action Preconditions and approval validation. If `send_follow_up` checks `Customer.email`, the Action requires authorization to read that Customer data. If `publish_content` checks a related `ReviewDecision`, the publishing operation must be authorized to read the review evidence it relies on.

A traversal must not become an authorization bypass merely because the related object is reachable from an authorized object.

Where policy for a required traversal is unresolved, the operation should return a structured deny/block result rather than silently omitting the check.

---

## 8. Authority model

Every operational property or relation should resolve to one of the following authority classes.

### 8.1 `source-backed`

A real external System of Record owns the value.

Examples:

```text
Inquiry.status → CRM
Product.base_price → ERP/PIM
PublicationRecord.external_url → CMS
Employee.identity → IdP
```

Enterprise AI Office may read it only when visibility/read authorization permits and may write it only through an explicitly approved write-back Action.

### 8.2 `ontology-owned`

Enterprise AI Office owns the value because no external System of Record does.

Examples may include:

```text
Inquiry.ai_summary
Inquiry.ai_triage_note
Content.lifecycle_state
ReviewDecision
```

This class should be used sparingly. It must not become a shadow copy of source-system state.

### 8.3 `derived`

The value is computed from other authoritative data or rules.

Examples:

```text
Inquiry.days_open
Customer.open_inquiry_count
Content.content_hash
Project.risk_summary
```

Derived data must retain enough provenance to explain its inputs or rule version when material.

Derived values must not expose source data to an actor who was not authorized to read the underlying or resulting information according to the effective policy.

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
approve_content
publish_content
update_product_spec
```

An Action contract should support:

```text
name
target object type
parameters
actor requirements
read/traversal requirements used by preconditions
preconditions
approval requirements
approval subject binding when applicable
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
Approved subject version/hash == current subject version/hash
```

Precondition evaluation does not bypass read authorization. Every object/property used to decide a precondition must be readable under the effective actor/operation policy.

When an Action depends on prior approval for a mutable subject, precondition evaluation must verify that the approval still matches the current subject state.

A failed precondition should return a structured denial rather than only prose.

Example result:

```json
{
  "allowed": false,
  "code": "VALID_APPROVAL_NOT_FOUND",
  "message": "The current object version is not covered by a valid approval."
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

Where an Action is approval-gated, the resulting audit/effect linkage should preserve which approval evidence authorized that exact execution.

---

## 12. Actor and permission requirements

The Ontology must not replace the existing human identity and Profile capability model.

A future governed operation decision should combine:

```text
Human identity / RBAC
+
Hermes Profile capability boundary
+
Object / Property / Relation visibility
+
Read Operation or Business Action rule
```

The system should be able to distinguish at least:

```text
human actor
Profile / Agent actor
service / automation actor
```

A natural-language request must not grant a new role, credential, entitlement, or approval level.

If trusted actor identity cannot be propagated to the operation layer where the rule requires it, the operation must fail closed.

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

### 13.1 Approval evidence

Approval evidence should be explicit enough to establish at least:

```text
who approved
what was approved
when it was approved
what approval role/authority applied
which Ontology/contract rule governed the approval
```

The evidence may be represented by an immutable review/approval record, an upstream workflow record, a signed/verified approval reference, or another trustworthy mechanism appropriate to the integration.

Do not treat free-form assistant text such as “approved” as authoritative approval evidence.

### 13.2 Approval subject binding

When the approved subject can change after review, the approval evidence must bind to the exact subject state that was reviewed.

Possible binding fields include:

```text
object id
revision/version
content hash
material field snapshot
commercial total/terms
state transition
other stable subject fingerprint
```

Example:

```yaml
approval:
  mode: explicit-human-approval
  binding:
    object_id: ContentItem.content_id
    revision: ContentItem.revision
    content_hash: ContentItem.content_hash
```

A later material change must make the previous approval inapplicable unless the governing business system explicitly defines a safe equivalent mechanism.

A stale approval must produce a structured denial such as:

```text
VALID_APPROVAL_NOT_FOUND
STALE_APPROVAL
APPROVED_SUBJECT_MISMATCH
```

The exact code is domain-specific; the fail-closed behavior is not.

### 13.3 Approval validation at execution time

Approval should be checked at the point where the governed side effect is about to occur, not only when a review step originally completed.

A publication, order submission, quote release, external send, or destructive action should therefore verify that:

```text
approval exists
approval actor/role is valid
approval subject matches the current target state
approval has not been revoked/expired when such lifecycle exists
required approval evidence is readable and trustworthy
```

Do not allow approval to become a reusable blanket capability token unrelated to the subject it originally authorized.

---

## 14. Tool bindings

A Tool Binding connects a Named Action or Read Operation to an actual supported integration.

Example:

```text
send_follow_up
    ↓
crm.send_follow_up
```

or:

```text
search_inquiries
    ↓
crm.search_inquiries
```

or:

```text
publish_content
    ↓
cms.publish_content
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
search_inquiries
get_inquiry
assign_inquiry
send_follow_up
get_content_for_review
approve_content
publish_content
```

Avoid exposing broad mutation tools whose parameters allow the Agent to bypass business semantics.

For reads, prefer an operation whose supported filters/traversals and visibility behavior are known over an unrestricted query surface when the latter would bypass domain authorization.

For approval-gated writes, avoid tools that permit the caller to supply arbitrary “approval=true” flags without verifiable approval evidence.

The absence of a generic write tool is a security feature, not a limitation to work around.

---

## 16. Audit contract

A governed business Action should be auditable whether it succeeds or is rejected.

Security-sensitive or policy-relevant denied Read Operations may also need audit evidence when required by the real deployment policy.

A future runtime audit record should be capable of storing:

```text
timestamp
actor identity
Profile / Agent identity
operation/action name
target object / id
parameters or safe parameter summary
rule / contract version
decision
applied / rejected / blocked
structured reason code
approval reference when applicable
approved subject version/hash/snapshot reference when applicable
external system result reference
reconciliation state when applicable
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

For approval-gated effects, retries must not silently substitute a different target version than the one originally approved.

---

## 18. Provenance

Material derived facts, approvals, and governed changes should preserve enough provenance to answer:

```text
What source or rule produced this?
Which contract version applied?
When did it become valid?
What changed it?
Which approval authorized this exact side effect when approval was required?
```

Existing WeKnora source provenance remains the authority for document-backed knowledge.

Ontology provenance should complement, not duplicate, that source evidence.

---

## 19. Versioning and change governance

Ontology definitions should be version-controlled.

A future machine-readable contract should use explicit version identifiers.

Changes that alter:

- authority;
- object/property/relation visibility;
- read-operation eligibility;
- traversal authorization;
- business-action eligibility;
- approval requirements;
- approval subject binding semantics;
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
schema_version: 0.3.0

domain: content

objects:
  ContentItem:
    primary_key: content_id
    visibility:
      default: deny
      read_requirements:
        - entitlement: marketing.content.read
    properties:
      revision:
        type: integer
        authority:
          class: ontology-owned
          system: enterprise-ai-office
      content_hash:
        type: string
        authority:
          class: derived

  ReviewDecision:
    primary_key: review_id
    visibility:
      default: deny
      read_requirements:
        - entitlement: marketing.content.review.read

actions:
  publish_content:
    target: ContentItem
    actor_requirements:
      entitlements:
        - marketing.content.read
        - marketing.content.review.read
        - marketing.publish
    preconditions:
      - rule: valid approved ReviewDecision exists for current revision/hash
        code: VALID_APPROVAL_NOT_FOUND
    approval:
      mode: role-based-approval
      binding:
        revision: ContentItem.revision
        content_hash: ContentItem.content_hash
    tool_binding:
      operation: cms.publish_content
    audit:
      enabled: true
```

This example is a shape demonstration, not a frozen schema and not an instruction to implement a CMS integration.

Fuller design experiments are maintained under:

- `ontology/examples/sales-inquiry.yaml`
- `ontology/examples/content-publication.yaml`

---

## 21. Validation experiments

Do not model the entire company at once.

### 21.1 Sales Inquiry experiment

The first schema experiment uses:

```text
Customer
   ↓ submits
Inquiry
   ↓ relates_to
Product
   ↓
Follow-up Action
```

It demonstrated one concrete contract correction:

> authorization must be closed over the full data path, not only the entry-point Object Type.

For example, an Inquiry search that filters `Customer.country` and `Product.product_family` must explicitly satisfy the relevant Customer/Product read requirements. An Action precondition that reads `Customer.email` must do the same.

### 21.2 Content Publication experiment

The second schema experiment uses:

```text
ContentItem
   ↓ has_review
ReviewDecision
   ↓ authorizes exact revision/hash
publish_content
   ↓
PublicationRecord
```

It demonstrated a second contract correction:

> approval must bind to the exact mutable subject state it authorizes.

A prior approval for content revision/hash A must not authorize later revision/hash B merely because both belong to the same `ContentItem`.

The experiment also revealed a pure structural schema mistake during review: an idempotency key referenced an undeclared `target`. This is evidence that a lightweight structural validator may now provide practical value as examples grow.

No production mutation is required for either experiment.

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

A read-only integration does not automatically require a full Operational Ontology Runtime, but any read integration must still preserve the effective visibility and authorization guarantees of the source system and Enterprise AI Office policy.

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

Ontology may add object/read/action constraints inside the already-authorized Profile capability space.

### SOUL and Skills

Remain important behavioral and workflow guidance.

They should explain business context and reasoning, but critical enforced read/write/approval invariants should not exist only as prompt text.

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

without an Ontology Runtime when no enabled capability requires governed operational integration.

Ontology is not deployment debt when the company has no such requirement.

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
- exposing unrestricted read/query surfaces that bypass object or traversal authorization;
- assuming access to a source object grants access to every related object;
- evaluating Action preconditions with data the actor is not authorized to read;
- treating “approved once” as approval for every future version of a mutable subject;
- accepting an approval flag with no verifiable actor/subject evidence;
- retrying an approval-gated external side effect against a different subject version;
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
[ ] What is the default visibility of each operational Object Type?
[ ] Which entitlements/roles/scopes are required to read each relevant Object/Property?
[ ] What named Read Operations are exposed?
[ ] Which filters, projections, and traversals may each Read Operation use?
[ ] Does authorization close over every Object/Relation/Property actually read?
[ ] Who owns each mutable Property/Relation?
[ ] Which facts are source-backed, ontology-owned, or derived?
[ ] What Named Actions may change state?
[ ] What deterministic Preconditions apply?
[ ] Are all data reads used by those Preconditions authorized?
[ ] Who may perform the Action?
[ ] Is human/role approval required?
[ ] What exact subject/version/state does that approval authorize?
[ ] How is stale approval detected and rejected when the subject changes?
[ ] Which real tool/API/MCP binding performs the operation?
[ ] What Effects are expected?
[ ] How are denial/failure reasons represented?
[ ] What approval/action evidence must be audited?
[ ] How is the contract versioned and activated?
```

If these questions cannot be answered, the model is not yet ready to govern operational business reads and actions.

---

## 27. Next implementation step

Two schema experiments now exist and have both produced concrete contract corrections:

```text
sales-inquiry.yaml       → read/traversal authorization closure
content-publication.yaml → approval subject/version binding
```

The experiments have also produced at least two manual consistency findings:

```text
cross-object read entitlement omission
undeclared idempotency-key reference
```

This is enough evidence to justify evaluating a **lightweight repository-local structural validator**.

The validator, if added, should remain deliberately narrow. It should detect mechanical schema drift rather than become an Ontology Runtime or policy engine.

Candidate checks include:

```text
unknown Object references
unknown Property references
unknown Relation references
unknown system references
missing Authority on mutable properties/relations
missing fail-closed visibility declaration on operational objects
Read Operation traversal to unknown relations
cross-object filters/projections without explicit read entitlements where the example declares them
Action target/precondition/effect references to unknown objects/properties
approval binding references to unknown subject fields
idempotency/reference expressions using undeclared action parameters or known actor/object fields
invalid contract/schema version values
```

Do not make the validator execute business rules, connect to CRM/CMS/ERP, generate tools, or freeze every optional YAML field.

No Ontology Runtime, database, or new service should be introduced as part of this validator step.