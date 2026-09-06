# Enterprise AI Office v2 — Governed Email Design

Status: approved design / non-runtime
Version: 0.1.0
Date: 2026-09-06

This document defines the design contract for the first Enterprise AI Office v2 operational workflow: governed employee email assistance.

It is intentionally **not** a deployment guide. No mailbox credential, real mailbox access, Hermes Profile binding, SMTP sender, or production runtime is authorized by this document.

Use with:

- `docs/V2-SCOPE.md`
- `docs/ONTOLOGY.md`
- `ontology/examples/email-communication.yaml`
- `infrastructure/email/tencent-exmail/README.md` for provider research only

---

## 1. Design objective

v2 should prove one narrow operational progression:

```text
Employee asks for help
        ↓
Authorized email context is read
        ↓
Company facts are grounded from WeKnora when needed
        ↓
A reply draft is prepared
        ↓
A human sees the exact final outbound content
        ↓
The human explicitly approves that exact draft revision
        ↓
A narrow send action executes
        ↓
Provider result + EAO governance evidence are recorded
```

This must be possible without requiring CRM, ERP, Calendar, a graph database, another workflow engine, employee long-term memory, or autonomous outbound communication.

---

## 2. Provider boundary

For the ARMOR reference implementation, the selected provider is Tencent Enterprise Mail.

Logical authority remains simple:

```text
mailbox / folders / received messages / delivery result
→ Tencent Enterprise Mail

company facts / product facts / SOP
→ WeKnora

reviewable reply drafts / approval evidence / governance decision
→ Enterprise AI Office

scheduled reminders / persistent Agent work
→ Hermes Cron / Kanban when enabled
```

Enterprise AI Office must not become a shadow mailbox, CRM, or customer database.

Provider-specific protocol mechanics belong to the later implementation phase. The design only requires a narrow read surface and a governed send binding.

---

## 3. Minimal object model

The initial workflow needs only four operational concepts.

### 3.1 Mailbox

Represents one provider mailbox explicitly selected by company configuration.

Authority:

```text
source-backed → email provider
```

Knowing a mailbox address is not authorization to read it.

### 3.2 EmailMessage

Represents one provider-backed message needed by the workflow.

Authority:

```text
source-backed → email provider
```

Email content is operational communication context. It is not automatically authoritative company knowledge and must not be bulk-ingested into WeKnora by default.

### 3.3 DraftReply

Represents one reviewable outbound reply revision prepared by Enterprise AI Office.

Authority:

```text
ontology-owned → Enterprise AI Office
```

For approval purposes, a presented DraftReply revision is immutable. A material edit creates a new revision and a new content hash/equivalent approval subject.

### 3.4 SendApproval

Represents explicit trusted-human approval for one exact DraftReply revision.

Authority:

```text
ontology-owned → Enterprise AI Office governance layer
```

Approval must identify the human approver and the exact outbound subject state it authorizes.

The initial v2 design does **not** introduce:

```text
Customer
Contact
Lead
Opportunity
CRM record
Calendar event
generalized Communication object
```

Those belong to later versions only if real use requires them.

---

## 4. Relationships

Only policy-relevant relationships are modeled:

```text
Mailbox contains EmailMessage
DraftReply replies_to EmailMessage
SendApproval authorizes DraftReply
```

v2 deliberately avoids a first-class `EmailThread` object. Thread context can initially be reconstructed from provider/message identifiers and message headers. Add a durable thread object only if a real workflow later requires independent thread state.

---

## 5. Read operations

Initial logical reads are:

```text
search_email
get_email
```

Effective authorization is the intersection of:

```text
trusted human identity / RBAC
+
Hermes Profile capability
+
Mailbox / EmailMessage visibility policy
+
operation-specific authorization
+
provider credential scope
```

A Profile having an email read tool does not imply every employee using that Profile may read every configured mailbox.

If trusted human identity or mailbox scope cannot be resolved, the read fails closed.

---

## 6. Draft preparation

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

The approval subject must cover all material outbound fields in the initial milestone:

```text
sender mailbox
To
Cc when enabled
subject
body
source/reply message identity
```

Attachments and Bcc are outside the initial v2 milestone unless separately approved later.

---

## 7. Human approval

Logical operation:

```text
approve_reply_draft
```

Approval evidence must establish at least:

```text
trusted human actor
DraftReply identity
exact draft revision / content hash or equivalent immutable evidence
time of approval
applicable Ontology/contract version
```

Natural-language inference by the LLM is not approval.

If any material outbound field changes after approval, the prior approval becomes stale and cannot authorize the edited reply.

---

## 8. Governed send action

The only initial externally visible write is:

```text
send_approved_reply
```

It is a Named Action. A generic SMTP/send-anything primitive must not be exposed to the ordinary Agent operation surface.

Required preconditions include:

```text
trusted human actor resolved
DraftReply exists
source EmailMessage exists and is readable
valid SendApproval exists
SendApproval covers the exact current DraftReply revision/content hash
sender mailbox is authorized
recipient/subject/body/source message match the approved draft
provider binding is resolved at implementation time
```

Expected structured failure classes include:

```text
ACTOR_UNRESOLVED
DRAFT_NOT_FOUND
SOURCE_MESSAGE_NOT_FOUND
VALID_APPROVAL_NOT_FOUND
APPROVAL_STALE
MAILBOX_NOT_AUTHORIZED
PROVIDER_BINDING_UNRESOLVED
```

No autonomous customer-facing send is authorized in the initial v2 milestone.

---

## 9. Failure and retry semantics

Email sending is an external side effect. The design must not pretend that generic retry provides exactly-once delivery.

For an ambiguous send outcome:

```text
uncertain provider outcome
→ do not blindly retry
→ mark reconciliation required
→ inspect provider evidence / Sent state / provider log where available
→ human or deterministic reconciliation decides the next action
```

For the initial pilot, duplicate avoidance is more important than automatic retry speed.

---

## 10. Audit model

EAO audit records governance evidence; it does not duplicate the mailbox.

A governed send should make it possible to answer:

```text
who requested the action
which trusted human approved it
which Profile executed it
which mailbox/source message was involved
which draft revision/hash was approved
which Ontology/operation contract version applied
what decision was reached
what provider result/reference was observed
whether reconciliation is pending
```

Do not store mailbox credentials or unnecessary full message bodies in audit records.

Provider-side mail records remain provider evidence and should be referenced rather than copied wholesale.

---

## 11. Follow-up boundary

v2 does not create an Ontology-owned mini CRM just to remember follow-ups.

When follow-up automation is later enabled:

```text
scheduled reminder state → Hermes Cron
persistent multi-step Agent task → Hermes Kanban
```

The email Ontology may reference the relevant message/draft/action identity, but it does not become a second scheduler or task database.

Initial automation should remind or summarize. It must not bypass the human approval requirement for customer-facing sends.

---

## 12. Agent-facing operation surface

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

The operation surface is a design contract. Exact MCP/tool implementation is selected later using the upstream-first rule.

---

## 13. Identity boundary

v2 must distinguish:

```text
human actor
Hermes Profile / Agent actor
provider mailbox/service credential
```

They are not interchangeable.

The mailbox credential proves access to the provider; it does not prove which employee asked for or approved the action.

A production send path therefore requires trusted human identity propagation or another deterministic approval mechanism that can bind the approval evidence to a real authorized person.

---

## 14. Implementation-phase gate

Design completion does not authorize deployment.

Before any real mailbox is connected, a later implementation decision must resolve:

```text
actual pilot mailbox authorization
human/user scope
Hermes Profile scope
credential mechanism and protected secret location
provider endpoint/protocol details
read enforcement
trusted actor propagation
approval persistence/enforcement
send binding
reconciliation implementation
runtime audit persistence
acceptance evidence
```

Until that gate is explicitly opened:

```text
no credential generation required
no real mailbox connection required
no real IMAP test required
no SMTP/send required
no runtime Profile binding required
```

---

## 15. Definition of design complete

The v2 email design is complete when:

```text
[ ] provider responsibility is clear
[ ] minimal object model is frozen
[ ] Source-of-Truth boundaries are clear
[ ] read operations and authorization closure are defined
[ ] draft ownership is defined
[ ] exact human-approval binding is defined
[ ] send is a narrow Named Action
[ ] ambiguous send/retry semantics are defined
[ ] audit boundary is defined
[ ] follow-up does not create a shadow CRM
[ ] implementation/runtime questions are explicitly deferred to the implementation gate
```

A design-complete v2 email workflow may still have zero access to any real mailbox.
