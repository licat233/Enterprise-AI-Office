# Enterprise AI Office v2 — Governed Send & Reconciliation Installation Contract

Status: send / reconciliation installation contract frozen / real deployment not authorized
Version: 1.0
Date: 2026-09-07

This document closes `ID-6 — Governed send + reconciliation` for the Enterprise AI Office v2 `installation_design` phase.

It defines how one already-approved and already-claimed logical email send is rendered, submitted to Tencent Enterprise Mail through the narrow SMTP provider adapter, classified as `SENT`, `CONFIRMED_NOT_SENT`, or `OUTCOME_UNKNOWN`, and reconciled without blind duplicate sending.

It does **not** authorize a real mailbox credential, real SMTP connection, customer-visible send, or real company deployment.

Use with:

- `docs/V2-GOVERNANCE-RUNTIME.md`
- `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`
- `docs/V2-STAGE-CONTRACTS.md`
- `docs/V2-CONFIG-PROTECTED-INPUTS.md`
- `infrastructure/email/governance/schema.sql`
- `infrastructure/email/tencent-exmail/README.md`
- `infrastructure/email/tencent-exmail/smtp_send_adapter.py`
- `docs/acceptance/TENCENT-EXMAIL.md`

---

## 1. Scope

ID-6 does not reopen DraftReply or SendApproval design.

The input to ID-6 is already:

```text
trusted HumanActor
+
current email.send authorization
+
exact current DraftReply revision/hash
+
ACTIVE SendApproval
+
committed ApprovalClaim
+
logical_send_id
```

ID-6 adds only deterministic outbound transport execution evidence.

It does not add a fifth Email Ontology business object. `LogicalSend`, `SendAttempt`, and reconciliation rows are governance/runtime execution evidence.

---

## 2. Reference send path

```text
Open WebUI trusted Action/path
→ eao-email-governance
→ revalidate current HumanActor/email.send + exact Draft/Approval
→ atomically claim Approval + initialize logical send
→ COMMIT
→ create durable send attempt record
→ Tencent SMTP provider adapter
→ persist observed result
→ audit
```

The provider adapter is internal to the Governance boundary.

Ordinary employees/LLMs never receive:

```text
generic SMTP
raw socket access
arbitrary From override
arbitrary provider credential
send-anything primitive
```

---

## 3. One Approval → one logical send

The ID-5 invariant remains authoritative:

```text
one SendApproval
→ at most one logical_send_id
```

ID-6 requires the logical send record to match the committed ApprovalClaim.

Creating a second logical send from the same Approval is forbidden even if the first provider attempt failed.

Provider retries, where permitted, are **new attempts inside the same logical_send_id**, not new logical sends.

---

## 4. Logical send initialization transaction

Before any provider network side effect, one `BEGIN IMMEDIATE` transaction must:

```text
1. authenticate trusted caller/HumanActor context
2. reload current Draft revision/hash
3. reload exact SendApproval
4. derive Approval state and require ACTIVE
5. re-check current email.send on sender mailbox
6. validate configured sender mailbox/provider credential binding exists
7. validate recipient policy / controlled-test scope when applicable
8. allocate opaque logical_send_id
9. allocate stable RFC Message-ID
10. allocate stable Date header
11. render exact outbound transport bytes
12. calculate transport_payload_hash
13. INSERT approval_claim
14. INSERT logical_send evidence
15. INSERT governance audit event
16. COMMIT
```

If the transaction fails:

```text
ROLLBACK
→ no provider send attempt
```

The provider must never be called before the ApprovalClaim/logical-send transaction commits.

---

## 5. Stable RFC Message-ID

Every logical send receives one stable RFC `Message-ID` before the first provider attempt.

Reference form:

```text
<eao.<opaque-logical-send-id>@<sender-domain>>
```

Example using synthetic data:

```text
<eao.018f0000-0000-7000-8000-000000000001@example.invalid>
```

Requirements:

```text
opaque/random logical_send_id only
sender domain derived from configured sender mailbox
same logical send → same Message-ID on every controlled retry
new logical send → new Message-ID
```

Do not add an internal `X-EAO-*` recipient-visible header merely for correlation.

The standard Message-ID is a correlation aid, not proof of provider acceptance by itself.

---

## 6. Exact transport payload

The provider adapter receives only a fully resolved immutable payload constructed from the approved Draft and stored send metadata.

Baseline material:

```text
From      = configured sender mailbox
To        = exact approved Draft To
Cc        = exact approved Draft Cc
Subject   = exact approved Draft subject
Body      = exact approved Draft body
Date      = stable logical-send Date header
Message-ID = stable logical-send Message-ID
```

Attachments and Bcc remain outside v2 baseline.

Envelope recipients are:

```text
To + Cc
```

after exact address validation/deduplication rules defined by the implementation.

The runtime serializes RFC 5322/MIME bytes once from these immutable inputs and records:

```text
transport_payload_hash = sha256:<digest>
```

A retry must re-render and verify the same transport hash before SMTP submission.

If software/library drift renders different bytes:

```text
FAIL — TRANSPORT PAYLOAD HASH MISMATCH
→ do not send
```

Do not silently create a semantically-similar but byte-different retry under the same logical send.

---

## 7. Sender boundary

The adapter must enforce:

```text
envelope MAIL FROM
=
configured sender mailbox address
=
DraftReply.sender_mailbox_id resolved provider address
=
visible From header mailbox identity
```

No caller-supplied arbitrary From value may override this relationship.

If they differ:

```text
DENY — SENDER_MAILBOX_MISMATCH
```

---

## 8. Multi-recipient all-before-DATA rule

Partial-recipient submission is intentionally avoided in v2 baseline.

SMTP sequence:

```text
MAIL FROM
→ RCPT TO recipient 1
→ RCPT TO recipient 2
→ ...
→ only if every intended envelope recipient is accepted
→ DATA
```

If any intended recipient is rejected before DATA:

```text
best-effort RSET/close transaction
→ do not issue DATA
→ CONFIRMED_NOT_SENT
```

This deliberately favors an all-intended-recipients submission boundary over accepting a partial recipient set.

A later requirement for partial-recipient delivery must reopen this narrow policy explicitly; do not infer it from generic SMTP behavior.

---

## 9. Provider outcome semantics

The normalized attempt outcomes are exactly:

```text
SENT
CONFIRMED_NOT_SENT
OUTCOME_UNKNOWN
```

### SENT

`SENT` means:

> the SMTP server returned an explicit successful final response after the complete DATA payload was submitted.

It means the provider accepted responsibility for the message at the SMTP boundary.

It does **not** mean:

```text
recipient read it
recipient inbox accepted it permanently
no later bounce can occur
```

Later delivery/bounce tracking is outside the initial v2 milestone.

### CONFIRMED_NOT_SENT

Use only when there is positive evidence that this attempt did not reach provider acceptance, including examples such as:

```text
local payload validation/render failure before network side effect
connect/TLS/authentication failure
MAIL FROM rejection
recipient rejection before DATA (baseline aborts whole transaction)
explicit DATA-command rejection before message transfer
explicit negative final SMTP response after DATA
```

A controlled retry may be considered for the same logical send only after the logical send derives `CONFIRMED_NOT_SENT` and all retry preconditions still hold.

### OUTCOME_UNKNOWN

Use whenever the runtime cannot prove whether provider acceptance occurred.

Conservative rule:

```text
once message DATA transfer has begun,
transport timeout/disconnect/I/O exception before a trustworthy final SMTP response
→ OUTCOME_UNKNOWN
```

Also:

```text
attempt row exists
+
no durable terminal attempt result after process restart
→ OUTCOME_UNKNOWN
```

Unknown is not failure. Unknown means the side effect may already have happened.

---

## 10. Attempt durability before network I/O

Before each provider attempt, persist a new immutable attempt row in a transaction:

```text
attempt_id
logical_send_id
attempt_no
provider
endpoint
transport_payload_hash
started_at
```

Commit this attempt row **before** opening/submitting the SMTP transaction.

After observing a terminal provider outcome, append one terminal result row:

```text
attempt_id
observed_at
outcome
smtp_stage
smtp_code when available
provider_reference when available
diagnostic_code
sanitized diagnostic summary
```

If the process dies after attempt creation but before result persistence, restart derives:

```text
OUTCOME_UNKNOWN
```

and blocks retry.

This intentionally converts crash uncertainty into reconciliation rather than duplicate-send risk.

---

## 11. Logical send state derivation

Do not maintain a mutable mega-status if facts can determine the state.

Reference derivation:

```text
if any trusted reconciliation concludes SENT
→ SENT

else if any attempt has terminal SENT
→ SENT

else if any attempt exists without terminal result
→ RECONCILIATION_REQUIRED

else if latest observed attempt outcome == OUTCOME_UNKNOWN
→ RECONCILIATION_REQUIRED

else if latest trusted reconciliation concludes REMAINS_UNKNOWN
→ RECONCILIATION_REQUIRED

else if no attempts exist
→ READY_TO_ATTEMPT

else if latest terminal attempt/reconciliation == CONFIRMED_NOT_SENT
→ CONFIRMED_NOT_SENT
```

Once `SENT`, the logical send never returns to retryable state because a later delivery bounce is not equivalent to SMTP non-acceptance.

---

## 12. Controlled retry contract

A provider retry is allowed only when all are true:

```text
same logical_send_id
same claimed approval
same draft_id/revision/content_hash
same sender mailbox
same envelope recipient set
same Date header
same Message-ID
same transport_payload_hash
current HumanActor still has email.send
provider credential/binding still valid
current logical-send state == CONFIRMED_NOT_SENT
```

Then:

```text
attempt_no = previous + 1
```

The retry remains inside the same logical send.

Retry is forbidden when state is:

```text
SENT
RECONCILIATION_REQUIRED
```

No exponential-backoff subsystem or job queue is required by the baseline. A retry may be explicit/manual or narrowly orchestrated only after the confirmed-not-sent gate passes.

---

## 13. Reconciliation trigger

Reconciliation is required when:

```text
OUTCOME_UNKNOWN
or
attempt record exists without durable result
```

User-facing/operator result:

```text
RECONCILIATION_REQUIRED
Do not resend yet.
```

The ordinary employee/model tool surface does not contain a `force_retry_unknown` operation.

---

## 14. Reconciliation evidence

Reconciliation seeks trustworthy external evidence associated with the exact logical send / Message-ID.

Possible evidence classes, only when validated for the selected provider/runtime, include:

```text
provider/admin mail logs
provider API/log correlation
provider-maintained Sent mailbox evidence
controlled recipient evidence during acceptance
other operator-verified provider evidence
```

Do **not** assume SMTP automatically saves a copy to a Sent folder. That behavior must be proven for the selected deployment before Sent-folder evidence is treated as authoritative.

Do not enable Tencent company-wide Open API solely to make reconciliation theoretically easier. Add it only when a concrete validated requirement justifies the authority expansion.

Each reconciliation event records:

```text
reconciliation_id
logical_send_id
attempt_id when applicable
performed_by_actor_id or protected operator identity
performed_at
evidence_type
evidence_reference
conclusion
sanitized note
```

Allowed conclusions:

```text
SENT
CONFIRMED_NOT_SENT
REMAINS_UNKNOWN
```

Previous attempt observations are not overwritten.

---

## 15. Who may reconcile

Baseline reconciliation is a protected operator/governance control-plane action.

It is **not**:

```text
an ordinary LLM tool
an employee natural-language instruction
an automatic timeout retry
```

The baseline does not add a fifth employee mailbox permission such as `email.reconcile` merely for architectural symmetry.

The future authorized deployment records which protected operator/admin path can inspect and record reconciliation evidence.

If delegated reconciliation later becomes a real business requirement, add it as a specific policy extension rather than silently treating `email.send` as reconciliation authority.

---

## 16. Irreducibly unknown outcome

If trustworthy evidence cannot determine whether the provider accepted the message:

```text
REMAINS_UNKNOWN
→ logical send remains RECONCILIATION_REQUIRED
→ no retry
```

The baseline does not include a generic "send again despite unknown" override.

If a company later requires that risk-taking workflow, it must be designed explicitly with a fresh human decision/approval boundary; do not hide it inside retry behavior.

---

## 17. SMTP adapter classification boundary

The Tencent reference adapter may use Python stdlib `smtplib` with TLS/SSL on the selected provider endpoint.

The adapter must expose a narrow internal operation equivalent to:

```text
submit_prepared_message(
  configured sender,
  exact envelope recipients,
  exact pre-rendered message bytes
)
→ normalized AttemptResult
```

It must not expose generic SMTP commands to the Agent surface.

Reference classification:

```text
connection/auth/envelope exception before DATA begins
→ CONFIRMED_NOT_SENT

explicit recipient rejection before DATA
→ CONFIRMED_NOT_SENT

explicit DATA rejection / explicit final negative response
→ CONFIRMED_NOT_SENT

successful final DATA response
→ SENT

transport exception after DATA transfer begins without trustworthy final response
→ OUTCOME_UNKNOWN
```

The adapter returns only sanitized provider evidence. Secrets are never included in diagnostics.

---

## 18. SMTP endpoint / credential input

The selected Tencent endpoint remains deployment-time provider configuration.

Reference candidate currently documented by the repository:

```text
smtp.exmail.qq.com:465 over SSL
```

Deployment/validation must re-check Tencent's current official administration/client documentation before real activation.

Required protected inputs for a real authorized target include:

```text
selected sender mailbox
selected SMTP host/port/TLS mode
mailbox-specific provider/client credential
controlled test recipient scope for acceptance
```

Missing credential/authority is:

```text
BLOCKED — REQUIRED INPUT: Stage 4 SMTP/provider authorization
```

not a reason to weaken the blueprint.

---

## 19. Audit linkage

Governance audit must link:

```text
logical_send_id
approval_id
draft_id/revision/content_hash
requested/executing HumanActor
sender mailbox
stable Message-ID
transport_payload_hash
attempt_id / attempt_no
normalized outcome
provider reference when available
reconciliation_id/conclusion when applicable
contract/policy version
```

Do not copy SMTP credentials, trusted-forwarder secrets, or unnecessary full MIME payload into audit.

The DraftReply already owns the human-reviewed outbound content.

---

## 20. Restart behavior

On governance-service startup:

```text
load schema
inspect logical sends/attempts
find attempts with no terminal result
classify them operationally as RECONCILIATION_REQUIRED
never auto-retry them
```

A restart may safely begin the first attempt for a committed logical send that has **no attempt row at all**, because no provider attempt was durably recorded as having started.

A restart must not infer that an incomplete attempt failed just because the process died.

---

## 21. Provider credential rotation

Credential rotation does not create a new logical send.

If an attempt was `CONFIRMED_NOT_SENT` because authentication failed, an operator may fix/rotate the protected credential and then retry the **same logical send** if all retry invariants still hold.

If the prior attempt is `OUTCOME_UNKNOWN`, credential rotation does not make it safe to retry.

---

## 22. Controlled test-recipient gate

During target acceptance/pilot, the send adapter must enforce the configured controlled recipient scope before SMTP submission.

An out-of-scope recipient causes:

```text
DENY — RECIPIENT_OUT_OF_ACCEPTANCE_SCOPE
```

before ApprovalClaim/send initialization where practical, or at latest before provider attempt.

Moving from controlled recipients to broader production recipients is an explicit deployment-policy change, not an automatic consequence of Stage 4 code existing.

---

## 23. Stage 4 acceptance

A future explicitly authorized validation/deployment target must prove at least:

```text
[ ] exact ACTIVE Approval is claimed once before network side effect
[ ] logical send stores stable Message-ID and transport payload hash
[ ] wrong sender mailbox fails closed
[ ] out-of-scope acceptance recipient fails closed
[ ] all intended recipients must pass RCPT before DATA
[ ] successful final SMTP response maps to SENT
[ ] pre-DATA/auth/envelope rejection maps to CONFIRMED_NOT_SENT
[ ] simulated transport loss after DATA begins maps to OUTCOME_UNKNOWN
[ ] OUTCOME_UNKNOWN blocks another attempt
[ ] process crash with attempt/no-result becomes RECONCILIATION_REQUIRED after restart
[ ] CONFIRMED_NOT_SENT can retry only same immutable logical send
[ ] retry reuses Message-ID / Date / payload hash
[ ] SENT cannot retry
[ ] reconciliation appends evidence instead of rewriting old attempt observation
[ ] REMAINS_UNKNOWN stays blocked
[ ] no generic SMTP/send-anything tool reaches ordinary Agent surface
[ ] no provider/forwarder credential appears in audit/log/prompt/browser
[ ] v1 General Assistant remains healthy while send provider is unavailable
```

Result:

```text
PASS — GOVERNED EMAIL LOOP PASS
```

---

## 24. Explicitly rejected ID-6 alternatives

### Blind retry on timeout

Rejected: provider may already have accepted the message.

### Treat socket exception as NOT SENT

Rejected after DATA begins: it cannot prove provider-side non-acceptance.

### New logical send for every retry

Rejected: it defeats one Approval → one logical send and creates duplicate-send risk.

### Use a generic SMTP MCP tool

Rejected: it bypasses exact approval and sender/recipient policy boundaries.

### Require Redis/queue just for retry

Rejected: SQLite attempt evidence and explicit retry gates are sufficient for the single-host baseline.

### Assume Sent folder proves SMTP delivery

Rejected unless the selected provider/runtime is explicitly validated to save and correlate that message.

---

## 25. ID-6 completion gate

ID-6 is complete when the repository contains and consistently references:

```text
this send/reconciliation contract
SQLite logical-send/attempt/reconciliation schema
narrow SMTP provider adapter candidate
offline deterministic provider-attempt tests
Stage 4 acceptance mapping
capability/readiness references
```

Installation Design completion does not require a real mailbox or real SMTP credential.

Result:

```text
ID-6: PASS
SEND / RECONCILIATION INSTALLATION CONTRACT FROZEN
```
