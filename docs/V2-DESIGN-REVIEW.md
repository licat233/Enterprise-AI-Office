# Enterprise AI Office v2 — System Design Final Review

Status: final system design review passed / baseline complete / runtime not authorized
Version: 1.1
Date: 2026-09-06

This document records the final System Design review of the Enterprise AI Office v2 baseline milestone.

The review closes the v2 `system_design` milestone at baseline level. It does **not** transition the blueprint lifecycle to `installation_design`, does not authorize real mailbox access, credentials, runtime Profile binding, SMTP sending, messaging deployment, automation deployment, or any real company deployment.

Reviewed contracts include:

- `docs/V2-SCOPE.md`
- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-COMMUNICATION-FOLLOWUP-DESIGN.md`
- `docs/ONTOLOGY.md`
- `ontology/examples/email-communication.yaml`
- `docs/CLIENT-RBAC.md`
- existing capability / security / RBAC contracts

---

## 1. Review objective

The final review is intentionally narrow:

```text
check structural completeness
check cross-module consistency
check Source-of-Truth integrity
check scope control
identify true blockers only
```

It is not a new optimization phase. Non-blocking hardening and implementation details are deferred so v2 System Design can actually complete.

---

## 2. v2 frozen theme

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
trusted HumanActor
→ read authorized communication context
→ prepare DraftReply
→ human review
→ deterministic exact approval
→ narrow governed send
→ provider result / reconciliation evidence
→ optional internal follow-up
```

Result:

```text
PASS
```

---

## 3. Scope review

Approved core remains deliberately small:

```text
one new external business-system type: email
one governed reply/send loop
Open WebUI remains primary employee surface
Ontology contract applied only where the email workflow needs governance
Hermes Cron for simple reminders/summaries
optional one messaging platform later
Kanban only for genuinely persistent multi-step Agent work
```

Explicitly not required for v2 baseline:

```text
CRM
ERP
PIM
Calendar
employee long-term memory
new identity service
new RBAC platform
new employee portal
n8n / another workflow engine
extra vector database
local-LLM infrastructure project
graph database / generic Ontology Runtime
large monitoring/SIEM platform
multiple messaging platforms
autonomous customer-facing send
```

Result:

```text
PASS — no scope expansion is required to close the v2 operational loop.
```

---

## 4. Source-of-Truth review

The completed baseline keeps one authority per operational concern:

```text
Company/product/SOP facts          → WeKnora
Human Web identity/access          → Open WebUI or selected trusted identity layer
Agent role/capability              → Hermes Profile
Mailbox/messages/delivery result   → email provider
DraftReply / SendApproval evidence → EAO governance/Ontology layer
Simple scheduled reminder state    → Hermes Cron
Persistent multi-step Agent work   → Hermes Kanban when actually enabled
Actual deployment state            → runtime + DEPLOYMENT-STATE
```

No mailbox mirror, CRM shadow database, second scheduler, duplicate identity directory, or duplicate knowledge store is introduced.

Result:

```text
PASS
```

---

## 5. Minimal Ontology review

The baseline operational object model is:

```text
Mailbox          source-backed
EmailMessage     source-backed
DraftReply       ontology-owned
SendApproval     ontology-owned
```

Policy-relevant relations remain:

```text
Mailbox contains EmailMessage
DraftReply replies_to EmailMessage
SendApproval authorizes DraftReply
```

HumanActor is an authorization principal, not a fifth Email business object.

A first-class Customer, Contact, Lead, Opportunity, CRM record, Calendar event, EmailThread, or FollowUp object is not required for the initial workflow.

Result:

```text
PASS — minimal model is sufficient without domain expansion.
```

---

## 6. Human Identity & Approval Model review

The completed baseline distinguishes:

```text
HumanActor
≠ Hermes Profile
≠ provider mailbox/service credential
```

HumanActor is resolved from a trusted employee identity surface and is the human principal used for authorization, approval, and audit.

Formal approval:

```text
approve_reply_draft
→ SendApproval
```

Approval is deterministic evidence bound to the exact DraftReply revision/hash. Natural-language inference by the LLM cannot manufacture approval.

Self-approval is allowed by the baseline when the same trusted HumanActor has the required Mailbox-scoped permissions. Second-person approval is deferred until a real policy requires it.

Result:

```text
PASS
```

---

## 7. Mailbox / Permission Model review

Mailbox is the human-authorization resource.

Baseline operation permissions are:

```text
email.read
email.draft
email.approve
email.send
```

They are independent and scoped to Mailbox.

Effective authorization is the intersection of:

```text
trusted HumanActor
+
Mailbox-scoped human permission
+
Hermes Profile capability
+
object/relation visibility on the actual data path
+
operation-specific policy / preconditions
+
provider credential scope
+
valid approval when required
```

No explicit effective grant means deny. Permissions are re-evaluated at governed operation execution time.

Result:

```text
PASS
```

---

## 8. Draft / Approval / Send lifecycle review

The employee-visible happy path is:

```text
DRAFT
→ PRESENTED_FOR_REVIEW
→ APPROVED
→ SEND_PENDING
→ SENT
```

Internally, DraftReply, SendApproval, and send execution maintain separate lifecycle semantics.

Key invariants:

```text
material edit → new Draft revision/hash
old approval cannot authorize new revision
one SendApproval → one logical send operation
approval is claimed before external side effect
ambiguous provider result → RECONCILIATION_REQUIRED
no blind retry
```

Send outcomes are:

```text
SENT
FAILED_NOT_SENT
RECONCILIATION_REQUIRED
```

Result:

```text
PASS
```

---

## 9. Employee UX review

Open WebUI remains the primary v2 employee interface.

Natural language is used for low-risk workflow intent such as:

```text
find mail
select context
draft
edit
request a reminder
```

Formal approval requires deterministic interaction with the exact outbound material visible to the employee:

```text
sender
To
Cc when present
subject
body
```

The baseline may expose a simple:

```text
[Edit]
[Approve & Send]
```

interaction while internally preserving distinct `approve_reply_draft` and `send_approved_reply` operations.

Result:

```text
PASS — governance complexity stays behind a simple employee workflow.
```

---

## 10. Audit & Governance review

EAO records governance evidence rather than duplicating the mailbox.

The system can determine:

```text
who requested
who approved
who executed
which Profile participated
which Mailbox/source message was involved
which exact Draft revision/hash was approved
which approval authorized send
which governance contract version applied
what decision occurred
what provider result/reference was observed
how reconciliation resolved when needed
```

Governance evidence is append-oriented.

Secrets, unnecessary full email bodies, and unnecessary attachments are not governance-audit payloads.

Provider-side mail records remain provider evidence and are referenced rather than copied wholesale.

Result:

```text
PASS
```

---

## 11. Follow-up and messaging review

Open WebUI remains the primary employee surface.

One messaging platform may later act only as an optional entry/delivery surface and must not own email authorization, approval policy, provider credentials, or independent workflow state.

Follow-up authority remains:

```text
simple reminder / summary → Hermes Cron
persistent multi-step Agent work → Hermes Kanban when justified
```

No Cron/Kanban worker may bypass the human-approved send path.

Result:

```text
PASS
```

---

## 12. Failure / reconciliation review

The design does not assume exactly-once email delivery.

For ambiguous provider outcome:

```text
no blind retry
→ reconciliation required
→ inspect provider evidence
→ resolve to SENT or FAILED_NOT_SENT
```

A controlled retry may occur only after trustworthy evidence confirms that the previous provider attempt did not send, and it remains bound to the same exact DraftReply revision/hash and logical send operation.

Result:

```text
PASS
```

---

## 13. Known non-blocking cleanup / deferred items

The following do not block System Design completion:

```text
exact JWT/OIDC/trusted actor propagation mechanism
exact provider API/MCP/SMTP implementation
exact secret store
exact audit persistence backend
exact approval TTL
second-person approval policy
retry backoff mechanics
provider-specific delivery status mapping
attachments / Bcc / scheduled send
manager approval hierarchy
ABAC / dynamic risk policies
SIEM / compliance analytics
```

Any older design-support fixture naming such as `employee_id` may be normalized to generic `actor_id` during later contract/fixture maintenance. This is terminology cleanup, not an architecture blocker.

---

## 14. Installation / deployment boundary

Provider research, read-only prototypes, fixtures, tests, and early implementation-plan artifacts do not define project phase and do not authorize runtime work.

System Design completion means the blueprint now sufficiently defines **what v2 is**.

It does not answer every concrete installation question and does not activate any real company deployment.

Until an explicit lifecycle transition and, separately, an explicit real deployment task occur:

```text
no real mailbox credential required
no real mailbox connection required
no real IMAP read required
no SMTP/send required
no real employee/Profile binding required
no messaging credentials required
no production Cron/Kanban change required
```

Result:

```text
PASS
```

---

## 15. Final review result

```text
ENTERPRISE AI OFFICE v2

SYSTEM DESIGN FINAL REVIEW: PASS

CORE ARCHITECTURE: PASS
HUMAN IDENTITY & APPROVAL: PASS
DRAFT / APPROVAL / SEND LIFECYCLE: PASS
EMPLOYEE UX: PASS
AUDIT & GOVERNANCE: PASS
MAILBOX / PERMISSION: PASS
FAILURE / RECONCILIATION: PASS
FOLLOW-UP BOUNDARY: PASS
SCOPE CONTROL: PASS

SYSTEM DESIGN: BASELINE COMPLETE
V2 DESIGN STATUS: FROZEN
RUNTIME STATUS: NOT AUTHORIZED
REAL DEPLOYMENT TASK: INACTIVE
```

No structural blocker remains that justifies keeping v2 in an open-ended System Design optimization loop.

The next blueprint phase is `installation_design`, but the repository must not transition to it implicitly. The lifecycle transition still requires explicit human direction under `state/PROJECT-PHASE.yaml`.
