# Enterprise AI Office v2 — Implementation Blueprint

Status: approved plan / implementation not authorized
Version: 1.0
Date: 2026-09-06

This document translates the frozen v2 design into a staged future implementation plan.

It is a **plan only**. It does not authorize credentials, mailbox access, runtime changes, Profile binding, messaging deployment, Cron/Kanban changes, or customer-facing sends.

Authoritative design inputs:

- `docs/V2-SCOPE.md`
- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-COMMUNICATION-FOLLOWUP-DESIGN.md`
- `docs/V2-DESIGN-REVIEW.md`
- `docs/ONTOLOGY.md`
- `ontology/examples/email-communication.yaml`

---

## 1. Implementation philosophy

v2 should be implemented as a sequence of independently useful, independently testable increments.

Do not begin all stages at once.

```text
complete one stage
→ validate
→ preserve evidence
→ decide whether the next stage is still justified
```

A later stage may be deferred without invalidating an earlier successful stage unless the active company configuration explicitly requires the full v2 milestone.

---

## 2. Stage 0 — Preserve the v1 baseline

Before adding email capability, verify that the current v1 employee path remains healthy.

Required evidence:

```text
Open WebUI employee access works
Hermes general/Profile boundary remains healthy
WeKnora grounded retrieval works
existing RBAC remains fail-closed
current deployment state/backup is known
```

No v2 work should silently repair or redesign unrelated v1 components unless a real blocker is discovered.

Exit condition:

```text
V1 BASELINE VERIFIED
```

---

## 3. Stage 1 — Read-only email capability

Objective:

> Let one authorized employee/role search and read bounded email context without changing provider state.

Implementation-time decisions to resolve:

```text
selected provider account/mailbox authorization
credential mechanism
trusted human identity path
Hermes Profile / employee RBAC mapping
provider read interface
allowed mailbox/folder scope
safe result-size/body-size limits
attachment behavior
```

Required operation surface:

```text
search_email
get_email
```

Must not expose:

```text
send
move
delete
flag mutation
folder mutation
arbitrary protocol command
```

Acceptance emphasis:

```text
authorized read succeeds
unauthorized human/Profile fails
out-of-scope mailbox/folder fails
read does not mutate Seen/flags where provider behavior allows verification
credentials remain outside prompts/logs/Git
```

Exit condition:

```text
READ-ONLY EMAIL PASS
```

Stop here if real employee usage shows that email retrieval itself is not valuable enough to justify send capability.

---

## 4. Stage 2 — Draft preparation

Objective:

> Use authorized email context plus WeKnora evidence to prepare a reviewable reply with no external side effect.

Implement:

```text
prepare_reply_draft
DraftReply persistence/evidence
stable draft revision/content hash or equivalent immutable approval subject
human-readable final outbound preview
```

The draft store must remain small and purpose-specific. Do not turn it into a general document-management system.

Acceptance emphasis:

```text
draft uses authorized source context
company facts are grounded where required
draft creation sends nothing
material outbound fields are inspectable
draft revision/evidence is stable enough for later approval binding
```

Exit condition:

```text
DRAFT PREPARATION PASS
```

---

## 5. Stage 3 — Trusted human approval evidence

Objective:

> Record deterministic evidence that a real authorized human approved one exact outbound draft revision.

Implement:

```text
approve_reply_draft
trusted human actor propagation or equivalent deterministic identity binding
SendApproval persistence
approval binding to exact material outbound content
stale-approval rejection
```

Do not solve this with a prompt convention such as:

```text
"if the user says yes, assume approved"
```

The approval mechanism must be trustworthy enough for the risk of customer-facing email.

Acceptance emphasis:

```text
real human actor identified
approval references exact draft revision/hash
edited draft invalidates prior approval
another employee cannot reuse/forge approval
missing/unresolved actor fails closed
```

Exit condition:

```text
APPROVAL GATE PASS
```

Do not implement customer-facing send until this stage passes.

---

## 6. Stage 4 — Governed send action

Objective:

> Execute only the exact approved customer-facing reply through one narrow provider binding.

Implement:

```text
send_approved_reply
provider transport/tool binding
sender-mailbox restriction
approval revalidation immediately before side effect
provider result/reference capture
audit decision record
ambiguous-outcome reconciliation path
```

Do not expose a generic transport primitive to ordinary Agent tools.

The send adapter must receive a fully resolved approved payload; it should not be responsible for LLM reasoning about whether the message ought to be sent.

Acceptance emphasis:

```text
unapproved send fails
stale approval fails
sender/recipient/content mismatch fails
approved controlled test send succeeds
provider result is captured
ambiguous result does not blindly retry
no bulk/campaign sending appears
```

Exit condition:

```text
GOVERNED EMAIL LOOP PASS
```

At this point the core v2 business outcome exists even if messaging and follow-up automation are still disabled.

---

## 7. Stage 5 — Simple follow-up assistance

Objective:

> Add internal reminders or summaries without creating a CRM or autonomous sender.

Default implementation:

```text
Hermes Cron
```

Initial use cases should be limited to examples such as:

```text
internal follow-up reminder
morning communication review summary
weekly pending-communication summary
```

A scheduled job may read only the email scope already authorized to its execution Profile.

It may not execute `send_approved_reply` without the same valid human approval evidence required by interactive use.

Exit condition:

```text
SIMPLE FOLLOW-UP PASS
```

---

## 8. Stage 6 — Optional messaging surface

This stage is optional.

Enable only when ARMOR selects one real messaging platform and the convenience value justifies the additional identity/routing boundary.

Objective:

```text
approved employee message
→ deterministic identity / Profile routing
→ same v2 operations
```

Do not duplicate email logic in a bot-specific workflow.

If channel identity cannot support trusted approval, use the channel only for read requests/notifications and route approval back to a trusted surface.

Exit condition:

```text
ONE MESSAGING SURFACE PASS
```

This stage must not block v2 completion if the selected v2 definition/configuration does not require messaging.

---

## 9. Kanban activation gate

Kanban is not a numbered default stage.

Enable only after a demonstrated workflow requires persistent multi-step coordination, for example:

```text
customer technical question
→ research
→ engineering input
→ draft
→ review
→ response
```

A simple reminder is not sufficient justification.

Before enabling, answer:

```text
Why Cron or a single interactive session is insufficient?
What durable work state must survive?
Who owns/reviews the task?
What workspace/data scope is required?
```

If the answers are weak:

```text
KANBAN: NOT NOW
```

---

## 10. Runtime artifacts expected when implementation begins

Create or finalize only the artifacts required by the active stage.

Potential artifacts include:

```text
protected company deployment overlay
provider secret references
Hermes Profile/MCP configuration
read adapter/tool binding
DraftReply / SendApproval persistence implementation
send Action Gate
provider send adapter
runtime audit/reconciliation storage
acceptance evidence
DEPLOYMENT-STATE updates
CHANGELOG entry for material activation
```

Do not create every potential artifact at Stage 1.

---

## 11. Prototype policy

Existing provider/read prototypes are implementation candidates only.

At implementation time:

```text
re-check current Tencent Enterprise Mail behavior
re-check current Hermes/MCP upstream capabilities
prefer mature supported upstream integration if it now satisfies the frozen design
reuse prototype only if it remains the smallest correct implementation
```

Do not preserve prototype code merely because it was written first.

---

## 12. Rollback/removal principle

Each implementation stage should be removable without corrupting the v1 knowledge/employee path.

At minimum:

```text
email capability can be disabled
mail credentials can be revoked/removed
email tools disappear from affected Profile(s)
Cron reminder jobs can be removed
messaging route can be disabled
v1 Open WebUI → Hermes → WeKnora path remains functional
```

Externally sent email cannot be rolled back; this is why send approval and duplicate prevention are pre-send controls.

---

## 13. Scope escalation rule

During implementation, move a request out of v2 when it requires a new major domain such as:

```text
CRM master data
opportunity/pipeline state
calendar scheduling
employee long-term memory
multi-channel customer profile
ERP/order synchronization
new workflow platform
new graph/runtime platform
```

Do not absorb the feature by extending the email objects until they resemble a hidden CRM.

Record it as a post-v2 candidate instead.

---

## 14. Future implementation completion

The core v2 milestone is operationally proven when Stages 0–4 pass for the selected company configuration.

Stages 5–6 are controlled extensions when selected.

Conceptually:

```text
V2 CORE
= v1 healthy
+ authorized email read
+ useful draft
+ trusted human approval
+ governed send
+ audit/reconciliation evidence

OPTIONAL V2 EXTENSIONS
= internal follow-up automation
+ one messaging surface
+ Kanban only if justified
```

This split prevents optional convenience features from making the v2 release difficult to finish.
