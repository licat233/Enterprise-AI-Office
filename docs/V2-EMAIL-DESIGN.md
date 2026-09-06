# Enterprise AI Office v2 — Governed Email Design

Status: baseline system design complete / non-runtime
Version: 0.2.0
Date: 2026-09-06

This document defines the completed baseline system-design contract for the first Enterprise AI Office v2 operational workflow: governed employee email assistance.

It is intentionally **not** an installation or deployment guide. No mailbox credential, real mailbox access, Hermes Profile binding, SMTP sender, or production runtime is authorized by this document.

Use with:

- `docs/V2-SCOPE.md`
- `docs/ONTOLOGY.md`
- `ontology/examples/email-communication.yaml`
- `docs/V2-COMMUNICATION-FOLLOWUP-DESIGN.md`
- `docs/CLIENT-RBAC.md`
- `infrastructure/email/tencent-exmail/README.md` for reference-provider research only

---

## 1. Design objective

v2 proves one narrow operational progression:

```text
Employee asks for help
        ↓
Trusted HumanActor is resolved
        ↓
Authorized email context is read
        ↓
Company facts are grounded from WeKnora when needed
        ↓
A reply draft is prepared
        ↓
The human sees the exact final outbound content
        ↓
The human explicitly approves that exact draft revision
        ↓
A narrow governed send action executes
        ↓
Provider result + EAO governance evidence are recorded
        ↓
Optional internal follow-up reminder
```

This must remain possible without CRM, ERP, Calendar, a graph database, another workflow engine, employee long-term memory, a new employee portal, or autonomous customer-facing communication.

---

## 2. Provider and Source-of-Truth boundary

For the ARMOR reference design, the selected reference provider is Tencent Enterprise Mail.

Logical authority remains:

```text
mailbox / received messages / provider delivery result
→ Email Provider

company / product / SOP facts
→ WeKnora

human Web identity / employee entry access
→ Open WebUI or selected trusted identity layer

Agent role / capability boundary
→ Hermes Profile

reviewable reply drafts / approval evidence / governance decision
→ Enterprise AI Office governance layer

scheduled reminders
→ Hermes Cron

persistent multi-step Agent work
→ Hermes Kanban only when justified
```

Enterprise AI Office must not become a shadow mailbox, CRM, customer database, second scheduler, or duplicate knowledge store.

Provider-specific protocol mechanics belong to later Installation Design. Reference-provider selection does not authorize any real provider connection.

---

## 3. Minimal object model

The initial workflow needs only four operational concepts.

### 3.1 Mailbox

Represents one provider mailbox explicitly selected by company configuration.

Authority:

```text
source-backed → email provider
```

Knowing a mailbox identifier/address is not authorization to read or send through it.

### 3.2 EmailMessage

Represents one provider-backed message needed by the workflow.

Authority:

```text
source-backed → email provider
```

Email content is operational communication context. It is not automatically authoritative company knowledge and must not be bulk-ingested into WeKnora by default.

### 3.3 DraftReply

Represents one EAO-owned reviewable outbound reply revision.

Authority:

```text
ontology-owned → Enterprise AI Office
```

A presented DraftReply revision is immutable for approval purposes. Any material edit creates a new revision and new content hash/equivalent immutable approval subject.

### 3.4 SendApproval

Represents explicit trusted-human approval for one exact DraftReply revision/hash.

Authority:

```text
ontology-owned → Enterprise AI Office governance layer
```

Approval identifies the trusted human approver and the exact outbound subject state it authorizes.

The initial v2 design does **not** introduce:

```text
HumanActor as an Email business object
Customer
Contact
Lead
Opportunity
CRM record
Calendar event
EmailThread
FollowUp
generalized Communication object
```

HumanActor is an authorization principal, not a fifth Email Ontology business object. Thread context is reconstructed from provider/message identifiers and headers when needed. Simple follow-up schedule state belongs to Hermes Cron.

---

## 4. Relationships

Only policy-relevant relationships are modeled:

```text
Mailbox contains EmailMessage
DraftReply replies_to EmailMessage
SendApproval authorizes DraftReply
```

Add additional durable objects or relations only when a real workflow proves they are necessary.

---

## 5. Human identity model

v2 must keep three identities separate:

```text
HumanActor
= the trusted human principal requesting/reviewing/approving an operation

Hermes Profile / Agent actor
= the AI role and capability boundary used to perform work

Mailbox / provider credential
= the technical credential that allows provider access
```

They are not interchangeable.

HumanActor is resolved from Open WebUI or another explicitly trusted identity surface. EAO does not create a second employee directory or authentication system for v2.

The minimum logical HumanActor identity is:

```text
actor_id
identity_source
identity_subject
```

Display name and email may be carried as metadata but are not the security authority by themselves.

If trusted human identity cannot be resolved where an operation requires it:

```text
ACTOR_UNRESOLVED
→ fail closed
```

Exact identity propagation technology is deferred to Installation Design.

---

## 6. Mailbox-scoped permission model

Mailbox is the authorization resource for the v2 email domain.

Baseline human permissions are:

```text
email.read
email.draft
email.approve
email.send
```

They are independent permissions. `email.read` covers the initial `search_email` and `get_email` read surface; split search/body-read further only if real use later requires it.

A grant is logically scoped as:

```text
HumanActor or trusted Group
→ Mailbox
→ one or more email permissions
```

Personal and shared mailboxes use the same model. Group-derived grants may be used where the existing trusted identity layer supplies them; v2 does not create a new Group/IAM service.

No explicit effective grant means deny.

Effective authorization is the intersection of:

```text
trusted HumanActor
+
Mailbox-scoped human permission
+
Hermes Profile capability
+
object / relation visibility required by the actual data path
+
operation-specific authorization
+
provider credential scope
+
Action preconditions
+
valid SendApproval where required
```

A Profile having an email tool does not imply every employee using that Profile may access every configured mailbox.

A provider credential proving technical mailbox access does not grant human authorization.

Mailbox scope must constrain the actual provider/query data path; do not search an unauthorized mailbox and merely hide results in the UI afterward.

Governed operations re-evaluate current permission at execution time. A prior DraftReply or SendApproval does not permanently preserve a permission that has since been revoked.

---

## 7. Read operations

Initial logical reads are:

```text
search_email
get_email
```

Both require:

```text
trusted HumanActor
email.read on the relevant Mailbox
Hermes Profile read capability
applicable object/relation visibility
provider credential scope
```

If actor identity or mailbox scope cannot be resolved, the read fails closed.

Read-only access is not authorization to draft, approve, or send.

---

## 8. Draft preparation and revision model

Logical operation:

```text
prepare_reply_draft
```

The Agent may combine:

```text
authorized EmailMessage context
+
WeKnora evidence
+
Profile / Skill behavior
```

to construct a proposed reply.

Draft creation has no provider-side send effect.

`prepare_reply_draft` requires at least:

```text
email.read
+
email.draft
```

within the source/sender Mailbox scope.

The approval subject covers all material outbound fields in the initial milestone:

```text
sender mailbox
To
Cc when enabled
subject
body
source/reply message identity
revision
```

Attachments and Bcc remain outside the initial v2 milestone.

A material edit never silently mutates the previously reviewed subject. It creates a new revision/hash:

```text
revision N / hash A
↓ material edit
revision N+1 / hash B
```

Any approval bound to revision N cannot authorize revision N+1.

---

## 9. Human approval model

Logical operation:

```text
approve_reply_draft
```

Natural-language inference by the LLM is not formal approval evidence.

Phrases such as `OK`, `可以`, `发吧`, or `send it` may express conversational intent, but customer-facing send authority is created only through a deterministic approval operation on the exact presented DraftReply.

Approval evidence establishes at least:

```text
approval_id
approved_by_actor_id
DraftReply identity
exact draft revision
exact draft content hash / immutable equivalent
approved_at
applicable governance/Ontology contract version
```

The approver must have:

```text
trusted HumanActor identity
email.approve on the relevant Mailbox
draft visibility
```

Self-approval is allowed by default in the v2 baseline when the same actor has the required `read / draft / approve / send` permissions. Second-person approval is a future policy extension, not a baseline requirement.

The approver and the actor who later triggers send may be different authorized humans.

---

## 10. Approval lifecycle

The baseline SendApproval lifecycle supports these logical states:

```text
ACTIVE
STALE
REVOKED
CONSUMED
```

`EXPIRED` may be supported later when a company policy defines approval TTL; exact TTL is not a system-design blocker.

Rules:

```text
approval created for exact revision/hash
→ ACTIVE

material DraftReply edit creates new revision/hash
→ old approval becomes STALE

human revokes before external send execution begins
→ REVOKED

send_approved_reply claims approval for one logical send operation
→ CONSUMED
```

A stale or revoked approval remains historical governance evidence; it is not deleted.

One SendApproval authorizes only one logical send operation. It is not a reusable general send token.

---

## 11. Governed send action

The only initial externally visible write is:

```text
send_approved_reply
```

It is a Named Action. A generic SMTP/send-anything primitive must not be exposed to the ordinary Agent operation surface.

Required preconditions include:

```text
trusted HumanActor resolved
current actor has email.send on sender Mailbox
Hermes Profile has email.send capability
DraftReply exists and is visible
source EmailMessage exists and is readable
valid ACTIVE SendApproval exists
SendApproval covers exact current DraftReply revision/hash
sender / To / Cc / subject / body / source match the approved draft
provider credential scope permits sender Mailbox
provider binding is resolved at implementation time
```

Expected structured failure classes include:

```text
ACTOR_UNRESOLVED
DRAFT_NOT_FOUND
SOURCE_MESSAGE_NOT_FOUND
VALID_APPROVAL_NOT_FOUND
APPROVAL_STALE
APPROVAL_REVOKED
MAILBOX_NOT_AUTHORIZED
PROVIDER_BINDING_UNRESOLVED
```

No autonomous customer-facing send is authorized in the initial v2 milestone.

---

## 12. Draft / approval / send state machine

The employee-visible happy path is:

```text
DRAFT
↓
PRESENTED_FOR_REVIEW
↓
APPROVED
↓
SEND_PENDING
↓
SENT
```

Internally, DraftReply state, SendApproval state, and send execution state remain separate concerns rather than one oversized status field.

A send execution receives a stable logical execution identity and supports the baseline outcomes:

```text
SEND_PENDING
SENT
FAILED_NOT_SENT
RECONCILIATION_REQUIRED
```

The approval is claimed/consumed before the external side effect is attempted so an uncertain provider result cannot leave a reusable approval that causes duplicate sends.

A logical send operation is forever bound to one exact DraftReply revision/hash.

---

## 13. Failure, retry, and reconciliation semantics

Email sending is an external side effect. The design does not pretend generic retry provides exactly-once delivery.

For an ambiguous provider outcome:

```text
uncertain provider outcome
→ do not blindly retry
→ RECONCILIATION_REQUIRED
→ inspect provider evidence / Sent state / provider log where available
→ determine actual result
```

Reconciliation may resolve to:

```text
SENT
or
FAILED_NOT_SENT
```

A controlled retry is allowed only after the system has trustworthy evidence that the prior provider attempt did not send the message, and it remains part of the same logical send operation for the same exact DraftReply revision/hash.

If the DraftReply is materially edited before retry, the old logical send operation cannot send the new revision. A new review, approval, and logical send are required.

Duplicate avoidance is more important than automatic retry speed.

---

## 14. Employee UX baseline

The primary employee surface remains Open WebUI.

Natural language is appropriate for:

```text
searching for mail
selecting context
asking for a draft
requesting edits
requesting reminders/follow-up
```

Deterministic interaction is required for formal approval.

Before approval, the employee must be able to see the exact material outbound content:

```text
sender mailbox
To
Cc when present
subject
body
```

The default baseline interaction may present:

```text
[Edit]
[Approve & Send]
```

`Approve & Send` may be one employee interaction while internally performing two governed operations in order:

```text
approve_reply_draft
↓
send_approved_reply
```

If the employee says `发吧` or similar natural language, the system may interpret intent and surface/focus the exact draft for approval, but it must not manufacture SendApproval from LLM inference alone.

User-facing send outcomes are deliberately simple:

```text
SENT
→ confirm successful send

FAILED_NOT_SENT
→ explain that the message was not sent; controlled retry may be offered

RECONCILIATION_REQUIRED
→ explain that send result is uncertain and do not offer blind retry
```

The employee should not need to understand Ontology, content hashes, SMTP, MCP, or internal RBAC closure to use the workflow.

---

## 15. Audit and governance model

EAO audit stores governance evidence; it does not duplicate the mailbox.

Governance evidence must make it possible to answer:

```text
who requested the operation
who approved it
who triggered/executed the governed action
which Hermes Profile participated
which Mailbox/source message was involved
which exact draft revision/hash was approved
which approval authorized the send
which governance/Ontology contract version applied
what allow/deny/block decision was reached
what provider result/reference was observed
whether reconciliation was required and how it resolved
```

Baseline governance evidence is append-oriented. Later state changes such as approval revoke/stale or reconciliation resolution do not erase the historical event that preceded them.

Audit records must not contain:

```text
mailbox password
OAuth token
API key
SMTP credential
raw session/JWT secret
unnecessary full incoming/outgoing message bodies
unnecessary attachments
```

Provider-side mail records remain provider evidence and should be referenced rather than copied wholesale.

Audit access is separately authorized. Ordinary employee workflow visibility does not imply global governance-audit access.

Retention is company-configurable. Audit retention and mailbox retention are distinct policies.

Technical runtime logs and governance audit are different concerns; v2 system design defines the governance evidence, not a new observability/SIEM platform.

---

## 16. Follow-up boundary

v2 does not create an Ontology-owned mini CRM just to remember follow-ups.

When follow-up automation is later enabled:

```text
scheduled reminder state → Hermes Cron
persistent multi-step Agent task → Hermes Kanban
```

Initial automation may read authorized communication context, summarize, remind, or prepare a future draft. It must not bypass the human approval requirement for customer-facing sends.

---

## 17. Agent-facing operation surface

Conceptual v2 surface:

```text
Reads
  search_email
  get_email

Local/governance operations
  prepare_reply_draft
  approve_reply_draft

External Named Action
  send_approved_reply
```

Intentionally absent:

```text
generic_imap_command
generic_smtp_send
send_arbitrary_email
mailbox_delete
mailbox_move
mailbox_flag_write
bulk_send
campaign_send
execute_sql
```

The operation surface is a system-design contract. Exact MCP/tool implementation is selected later using the upstream-first rule.

---

## 18. Baseline invariants

The v2 email workflow freezes these minimum invariants:

```text
1. HumanActor, Hermes Profile, and provider credential are distinct authorities.
2. Human email permissions are scoped to Mailbox and read/draft/approve/send are independent.
3. Authorization fails closed when required identity, scope, visibility, binding, or approval cannot be resolved.
4. Every outbound governed send references exactly one DraftReply revision/hash.
5. Formal approval is deterministic evidence, not LLM-inferred conversational intent.
6. Material edit creates a new revision/hash and invalidates the old approval for the new revision.
7. One SendApproval authorizes one logical send operation only.
8. Ambiguous provider outcome never triggers blind retry.
9. SENT is concluded only from trustworthy send/provider evidence.
10. Audit preserves governance evidence without becoming a mailbox archive.
11. Simple follow-up uses Hermes Cron and cannot bypass send approval.
12. v2 does not require a new identity service, RBAC platform, workflow engine, CRM, or employee portal.
```

---

## 19. Deferred hardening / Installation Design decisions

System Design completion does not require resolving:

```text
exact JWT/OIDC/trusted identity propagation mechanism
exact provider protocol/API/MCP library
exact secret store
exact audit persistence backend
exact approval TTL
second-person approval policy
retry backoff implementation
provider-specific delivery status mapping
attachments / Bcc / scheduled send
manager approval hierarchy
ABAC / dynamic risk policy
SIEM / compliance analytics
```

These may be resolved during later Installation Design, hardening, or a future version only when required.

---

## 20. Installation-phase gate

System Design completion does not authorize deployment.

Before any real mailbox is connected, later Installation Design and an independently authorized real deployment task must resolve the concrete installation/runtime details relevant to the adopting company.

Until a real deployment task is explicitly activated:

```text
no real credential required
no real mailbox connection required
no real IMAP read required
no SMTP/send required
no real employee/Profile binding required
no production Cron/Kanban change required
```

---

## 21. Definition of baseline system design complete

The v2 governed-email baseline is complete because the design now defines:

```text
[x] provider and Source-of-Truth responsibility
[x] minimal object model
[x] trusted HumanActor boundary
[x] Mailbox-scoped read/draft/approve/send permission model
[x] read operations and authorization closure
[x] DraftReply ownership/revision semantics
[x] deterministic exact human-approval binding
[x] approval lifecycle baseline
[x] narrow send_approved_reply Named Action
[x] send state / failure / reconciliation semantics
[x] employee UX flow
[x] audit/governance boundary
[x] follow-up boundary without shadow CRM
[x] explicit deferred Installation Design/runtime decisions
```

A system-design-complete v2 email workflow may still have zero access to any real mailbox.
