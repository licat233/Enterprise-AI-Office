# Enterprise AI Office v2 — Design Review

Status: design review passed / design frozen / runtime not authorized
Version: 1.0
Date: 2026-09-06

This document records the architecture review of the initial Enterprise AI Office v2 milestone.

It freezes the design intent for later implementation while explicitly **not** authorizing real mailbox access, credentials, runtime Profile binding, SMTP sending, messaging deployment, or automation deployment.

Reviewed documents:

- `docs/V2-SCOPE.md`
- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-COMMUNICATION-FOLLOWUP-DESIGN.md`
- `docs/ONTOLOGY.md`
- `ontology/examples/email-communication.yaml`
- existing capability / security / RBAC contracts

---

## 1. v2 frozen theme

```text
Enterprise AI Office v2
= Communication & Follow-up
```

The milestone upgrades v1 from primarily:

```text
Ask AI
→ grounded answer
```

toward one governed operational loop:

```text
read authorized communication context
→ prepare work
→ human review/approval
→ narrow external action
→ preserve evidence
→ optional internal follow-up
```

v2 is not a general enterprise-system integration release.

---

## 2. Scope review

### Approved core

```text
one external business-system type: email
one governed reply/send loop
Ontology contract applied to the real email workflow
Open WebUI remains primary employee surface
Hermes Cron for simple reminders/summaries
optional one messaging platform later
Kanban only when a real multi-step workflow requires it
```

### Explicitly not restored in initial v2

```text
CRM
ERP
PIM
Calendar
employee long-term memory
SSO expansion unless independently required
armor-memory synchronization
n8n / another workflow engine
extra vector database
local-LLM infrastructure project
graph database / generic Ontology Runtime
large monitoring stack
multiple messaging platforms
autonomous customer-facing send
```

Result:

```text
PASS — scope remains materially smaller than the deferred v1 feature backlog.
```

---

## 3. Source-of-Truth review

The design does not create competing authorities.

```text
Company/product/SOP facts          → WeKnora
Human Web identity/access          → Open WebUI or selected trusted identity surface
Agent role/capability              → Hermes Profile
Mailbox/messages/delivery result   → email provider
DraftReply / SendApproval evidence → EAO governance/Ontology layer
Simple scheduled reminder state    → Hermes Cron
Persistent multi-step Agent work   → Hermes Kanban when actually enabled
Actual deployment state            → runtime + DEPLOYMENT-STATE
```

No mailbox mirror, CRM shadow database, second scheduler, or duplicate knowledge store is introduced.

Result:

```text
PASS — Source-of-Truth boundaries remain coherent.
```

---

## 4. Ontology review

The email design reactivates Ontology for a real selected operational domain rather than conceptual completeness.

Minimal model:

```text
Mailbox          source-backed
EmailMessage     source-backed
DraftReply       ontology-owned
SendApproval     ontology-owned
```

Policy-relevant relations only:

```text
Mailbox contains EmailMessage
DraftReply replies_to EmailMessage
SendApproval authorizes DraftReply
```

A first-class Customer, Contact, Lead, Opportunity, CRM record, Calendar event, or EmailThread object is not required for the initial workflow.

Result:

```text
PASS — model is operationally sufficient without domain expansion.
```

---

## 5. Operation-surface review

Approved conceptual operation surface:

```text
Reads
  search_email
  get_email

EAO governance/local operations
  prepare_reply_draft
  approve_reply_draft

External Named Action
  send_approved_reply
```

Intentionally absent:

```text
generic IMAP command
generic SMTP send
send arbitrary email
mailbox delete/move/flag mutation
bulk/campaign send
raw SQL
```

Result:

```text
PASS — Agent operation space is narrower than provider protocol capability.
```

---

## 6. Human-approval review

Customer-facing send remains human-in-the-loop.

Approval must bind to the exact material outbound subject:

```text
sender mailbox
To
Cc when enabled
subject
body
source/reply message identity
draft revision/content hash or equivalent immutable evidence
```

Material edits invalidate prior approval.

Natural-language inference by the LLM cannot manufacture approval.

Result:

```text
PASS — stale approval and autonomous-send risks are explicitly closed at design level.
```

---

## 7. Failure-semantics review

The design does not assume exactly-once SMTP delivery.

For ambiguous provider outcome:

```text
no blind retry
→ reconciliation required
→ inspect provider evidence
→ decide next action
```

Result:

```text
PASS — duplicate-send risk is treated as an external-side-effect problem rather than hidden behind generic retry.
```

---

## 8. Employee-entry review

Open WebUI remains the primary v2 employee interface.

A future messaging integration is optional and limited to one selected platform. It must reuse the same Profile/Ontology/business-action policy rather than creating a second workflow implementation.

If a messaging identity cannot be mapped to a trusted authorized human, that channel cannot approve or execute governed sends.

Result:

```text
PASS — v2 does not create a second employee platform requirement.
```

---

## 9. Follow-up automation review

Default:

```text
simple reminder / summary → Hermes Cron
```

Kanban activation trigger:

```text
persistent multi-step Agent work across time/roles/review
```

Not allowed:

```text
create a new scheduler
create a mini CRM to store follow-up lifecycle
use Cron/Kanban to bypass send approval
```

Result:

```text
PASS — automation reuses existing authorities and remains subordinate to the governed send path.
```

---

## 10. Implementation-prototype boundary

Provider research and a read-only IMAP prototype may exist in the repository, but they are not normative design authority.

The frozen design intentionally specifies:

```text
required business operations
security/identity/approval boundaries
Source-of-Truth ownership
failure semantics
acceptance expectations
```

without freezing:

```text
exact MCP library/runtime implementation
exact IMAP code path
exact SMTP library
exact secret store
exact human approval UI
exact audit persistence backend
exact Profile name
exact pilot mailbox credential
```

Implementation must follow upstream-first selection at the time deployment is actually authorized.

Result:

```text
PASS — prototype code does not define architecture.
```

---

## 11. Remaining implementation-time decisions

These are intentionally deferred and do not block design freeze:

```text
real pilot mailbox authorization
credential/client-password mechanism
trusted human identity propagation mechanism
specific Hermes Profile and employee RBAC mapping
exact provider endpoints/network behavior
read adapter/tool implementation choice
approval evidence persistence mechanism
send transport/tool binding
provider-result reconciliation mechanics
runtime audit persistence
one messaging platform selection, if any
specific Cron reminder workflow, if any
```

They must be resolved before the relevant runtime capability is enabled.

---

## 12. Implementation gate

Design freeze does **not** mean implementation starts automatically.

Implementation may begin only after an explicit implementation/deployment task opens the gate.

Until then:

```text
no mailbox credential required
no real mailbox connection required
no real IMAP read required
no SMTP send required
no real Profile binding required
no messaging credentials required
no Cron/Kanban runtime change required
```

---

## 13. Frozen v2 rollout order

When implementation is authorized later, use this order:

```text
1. preserve/verify v1 baseline
2. read-only authorized email context
3. draft preparation
4. trusted human approval evidence
5. governed send_approved_reply action
6. audit/reconciliation acceptance
7. simple internal follow-up reminder/summary
8. optional one-platform messaging entry/delivery
9. Kanban only if proven necessary
```

Do not parallelize optional features merely to make v2 look more complete.

---

## 14. Review result

```text
V2 DESIGN REVIEW: PASS
V2 DESIGN STATUS: FROZEN
RUNTIME STATUS: NOT AUTHORIZED
```

The design is intentionally small enough to implement as a controlled v2 without reopening the full deferred v1 feature backlog.
