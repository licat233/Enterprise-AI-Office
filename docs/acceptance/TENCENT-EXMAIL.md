# Tencent Enterprise Mail Integration Acceptance

Status: conditional capability acceptance

Run this acceptance only when the active company configuration enables the Tencent Enterprise Mail integration.

Use with:

- `docs/V2-SCOPE.md`
- `docs/V2-STAGE-CONTRACTS.md`
- `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`
- `docs/V2-GOVERNANCE-RUNTIME.md`
- `docs/V2-SEND-RECONCILIATION.md`
- `docs/ONTOLOGY.md`
- `infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md`
- `infrastructure/open-webui/V2-APPROVAL-ACTION.md`
- `infrastructure/email/governance/README.md`
- `infrastructure/email/tencent-exmail/README.md`
- `infrastructure/email/tencent-exmail/smtp_send_adapter.py`
- `docs/SECURITY.md`
- `docs/CLIENT-RBAC.md`
- `config/capabilities.yaml`

A successful IMAP or SMTP login alone is not acceptance.

## Stage mapping

```text
Stage 0 — v1 baseline
→ docs/ACCEPTANCE-TESTS.md Part A

Stage 1 — read-only email
→ Sections 1–5 and applicable employee-client checks in Section 12

Stage 2 — DraftReply preparation
→ Sections 5–6 and applicable employee-client checks in Section 12

Stage 3 — trusted human approval
→ Sections 3, 7, 10 and 12

Stage 4 — governed send
→ Sections 3, 8–10 and 12

Stage 5 — optional simple follow-up
→ Section 11 plus docs/ACCEPTANCE-TESTS.md Cron section

Stage 6 — optional messaging surface
→ docs/ACCEPTANCE-TESTS.md Messaging section plus the same email governance boundary
```

The detailed Stage preconditions, inputs, idempotency, evidence, and rollback contracts are authoritative in `docs/V2-STAGE-CONTRACTS.md`.

## 1. Provider and mailbox scope

```text
[ ] Provider recorded as Tencent Enterprise Mail / Tencent Exmail
[ ] Exactly selected mailbox(es) recorded
[ ] Business owner/purpose recorded
[ ] Authorized HumanActor/group scope recorded
[ ] Communication Assistant/Profile scope recorded
[ ] Allowed mailbox folders/read scope recorded
[ ] Attachments disabled unless explicitly required and tested
```

The initial v2 pilot should normally use one mailbox. Adding more mailboxes is a deliberate scope expansion.

## 2. Credential boundary

```text
[ ] IMAP/SMTP uses TLS endpoints supported by the provider
[ ] Client-specific password/credential used where Tencent security-login policy requires it
[ ] Primary mailbox password is not committed to Git
[ ] Mail credential is stored only in protected runtime secret storage
[ ] Mail credential is available only to the governance/provider adapter boundary
[ ] Open WebUI → Governance forwarder credential is protected separately
[ ] No provider/forwarder credential appears in logs, prompts, audit records, or deployment state
[ ] Company-wide CorpSecret is not granted merely to read/send one mailbox
```

If Tencent Open API is separately enabled:

```text
[ ] Concrete API-backed requirement documented
[ ] CorpSecret protected
[ ] application scope reviewed
[ ] callback signature/encryption validation works if callbacks are enabled
```

## 3. Trusted HumanActor and mailbox authorization propagation

Use at least two synthetic/authorized human identities with different group/mailbox scope.

```text
[ ] Open WebUI current user ID reaches governance only through the protected server-side tool/action path
[ ] Canonical HumanActor uses stable Open WebUI user ID, not display name/email
[ ] Current Open WebUI runtime group IDs reach governance on the trusted forwarder path
[ ] logical company group → runtime Open WebUI group mapping is recorded and unambiguous
[ ] valid Open WebUI → Governance forwarder authentication is required
[ ] missing/invalid forwarder authentication fails closed
[ ] actor/group values supplied as prompt text or ordinary tool arguments cannot override trusted context
[ ] authorized group/direct mailbox grant allows only configured operations
[ ] no matching mailbox grant denies the operation
[ ] removing a user from the authorizing Open WebUI group removes the grant on the next governed request after selected identity-sync/session semantics take effect
[ ] General Assistant has no Email Governance tools attached by default
[ ] Communication Assistant exposes only stage-enabled Email tools
```

If OIDC group synchronization is enabled, exercise the selected release's required logout/login or session-refresh behavior after a group change.

## 4. Non-mutating read path

Test with harmless known messages in the configured mailbox.

```text
[ ] Authorized operation can search configured mailbox/folder scope
[ ] Authorized operation can retrieve expected message content
[ ] Read operation does not mark an unread test message as Seen
[ ] Read operation does not move/delete messages
[ ] Read operation does not create folders or change flags/rules
[ ] Unauthorized HumanActor cannot retrieve mailbox content
[ ] Out-of-scope mailbox/folder access fails closed
```

Where implementation uses IMAP directly, verify behavior equivalent to read-only mailbox selection and non-mutating body fetch (`EXAMINE` / `BODY.PEEK` semantics where supported).

## 5. Knowledge/source boundary

```text
[ ] Email content is operational communication context, not automatically authoritative company knowledge
[ ] Company/product facts in a drafted reply are grounded through approved WeKnora knowledge when required
[ ] Mailbox contents are not bulk-ingested into WeKnora merely to simplify retrieval
[ ] Conflicting email context vs authoritative company source is surfaced rather than silently overwriting company truth
```

## 6. Draft behavior / governance persistence

Before runtime tests, run the offline governance contract check:

```sh
python3 infrastructure/email/governance/test_schema.py
```

Then verify on the authorized target:

```text
[ ] Offline governance SQLite/hash/review-binding test PASS
[ ] Authorized HumanActor can prepare a reply without sending it
[ ] Unauthorized mailbox/message cannot produce a DraftReply
[ ] Draft generation alone causes no SMTP side effect
[ ] New Draft begins at revision 1
[ ] Material edit creates a new immutable revision/hash and preserves the prior revision
[ ] content_hash is service-computed from the exact persisted outbound fields
[ ] Re-hashing the same persisted revision after restart produces the same digest
[ ] Draft identifies target mailbox/source/recipients before approval
[ ] Draft governance state survives the required service restart/recovery test
[ ] Draft creation + audit event do not partially commit when the transaction fails
[ ] HumanActor/chat/assistant-message review binding points to the exact persisted Draft revision/hash
```

## 7. Human approval binding

Approval must bind to the exact outbound subject:

```text
From mailbox
To
Cc/Bcc if enabled
Subject
Body
source/reply identity
Attachments if later enabled
Draft revision/content hash
```

Acceptance:

```text
[ ] Explicit trusted human approval required before send
[ ] Version-bound Open WebUI approval Action is attached only to the intended Communication Assistant
[ ] Approval Action derives current HumanActor server-side
[ ] Approval Action resolves current authorization/group context server-side
[ ] Action resolves the review subject from governance HumanActor/chat/message binding, not model-generated draft identifiers
[ ] Native confirmation dialog displays the exact governance-persisted From/To/Cc/Subject/Body before approval commit
[ ] Cancelling the confirmation creates no SendApproval
[ ] Approval evidence binds to exact final outbound content/state
[ ] Changing recipient, subject, body, source target, or attachment after approval invalidates approval
[ ] Changing the Draft after confirmation display but before approval commit fails closed as stale/mismatch
[ ] Duplicate delivery of the same trusted approval interaction does not create independently reusable duplicate authority
[ ] Stale approval produces structured deny/block result
[ ] Revoked approval cannot be claimed for send
[ ] One Approval cannot be claimed for two logical send IDs
[ ] Current email.approve permission is re-checked at approval time
[ ] Natural-language Agent inference cannot manufacture approval
[ ] Stage 3 approval Action performs no provider send
```

## 8. Governed send path

Before any real/authorized provider submission, run the offline ID-6 checks:

```sh
python3 infrastructure/email/governance/test_send_reconciliation.py
python3 infrastructure/email/tencent-exmail/test_smtp_send_adapter.py
```

Then verify with controlled test recipients only:

```text
[ ] Offline send/reconciliation SQLite contract PASS
[ ] Offline fake-SMTP outcome classification PASS
[ ] Only the configured approved mailbox identity can be envelope MAIL FROM and visible From
[ ] Current email.send permission is re-checked immediately before logical-send initialization
[ ] Exact Draft revision/hash and ACTIVE SendApproval are re-checked before claim
[ ] ApprovalClaim + logical-send initialization commit before provider network side effect
[ ] Logical send records one stable RFC Message-ID
[ ] Logical send records one stable Date header
[ ] Logical send records transport_payload_hash for exact rendered message bytes
[ ] Out-of-scope controlled-test recipient is denied before provider submission
[ ] Every intended envelope recipient must be SMTP-accepted before DATA is issued
[ ] Any RCPT rejection aborts the whole baseline transaction before DATA
[ ] Successful final SMTP DATA response maps to SENT
[ ] Explicit pre-DATA/auth/envelope rejection maps to CONFIRMED_NOT_SENT
[ ] Explicit negative final SMTP response maps to CONFIRMED_NOT_SENT
[ ] Unapproved/stale/revoked/previously-claimed approval send fails closed
[ ] Generic SMTP/send-anything primitive is not exposed to ordinary employee Agent surface
[ ] Bulk/campaign sending unavailable in initial v2 scope
[ ] Attachments unavailable unless separately enabled and accepted
```

`SENT` means provider SMTP acceptance, not recipient read/permanent delivery.

## 9. Ambiguous failure / duplicate-send safety

Create or simulate a harmless uncertain-result condition where practical.

```text
[ ] Send-attempt row is committed before provider network submission
[ ] Transport timeout/disconnect after DATA begins and before trustworthy final response maps to OUTCOME_UNKNOWN
[ ] Process crash/restart with attempt row but no result derives RECONCILIATION_REQUIRED
[ ] OUTCOME_UNKNOWN cannot create another attempt
[ ] RECONCILIATION_REQUIRED cannot create another attempt
[ ] SENT cannot create another attempt
[ ] CONFIRMED_NOT_SENT may retry only inside the same logical_send_id
[ ] Controlled retry reuses exact Draft/Approval binding
[ ] Controlled retry reuses same sender/envelope recipients
[ ] Controlled retry reuses same RFC Message-ID and Date header
[ ] Controlled retry re-renders and verifies the same transport_payload_hash
[ ] Payload-hash mismatch fails closed rather than silently retrying
[ ] Reconciliation appends evidence; original attempt observation remains unchanged
[ ] Reconciliation conclusion is only SENT / CONFIRMED_NOT_SENT / REMAINS_UNKNOWN
[ ] REMAINS_UNKNOWN remains blocked from retry
[ ] No generic "force retry unknown" employee/LLM operation exists
```

Do not claim exactly-once delivery. The safety property is:

> ambiguous provider outcome never causes blind duplicate submission.

If Sent-folder/provider-log evidence is used for reconciliation, acceptance must first prove that evidence source can reliably correlate the exact stable Message-ID for the selected Tencent deployment. Do not assume SMTP automatically saves a Sent copy.

## 10. Governance / audit evidence

Audit/evidence should be sufficient to answer:

```text
who requested/executed the send
which HumanActor approved it
which Assistant/Profile context was involved
which mailbox was used
which source message was targeted
which recipient set and Draft content hash/version were approved
which approval_id / logical_send_id applied
which stable RFC Message-ID and transport payload hash applied
which attempt_id / attempt number ran
which normalized provider result was observed
which provider reference/evidence exists
whether reconciliation is pending
which reconciliation conclusion was recorded
```

Acceptance:

```text
[ ] Draft/approval/claim governance events are append-oriented
[ ] ApprovalClaim/logical send recorded before SMTP side effect
[ ] Send attempt recorded before network submission
[ ] Terminal provider observation recorded when available
[ ] Denied/blocked send recorded when policy requires it
[ ] Reconciliation evidence is append-oriented
[ ] No mailbox/forwarder secret or unnecessary full MIME payload stored in audit
```

## 11. Follow-up integration

If Hermes Cron or Kanban is enabled for this email workflow:

```text
[ ] Follow-up state belongs to the configured Hermes capability, not a shadow CRM
[ ] Reminder/action references the correct email context
[ ] Scheduled task cannot bypass send approval
[ ] Removing/disabling Email leaves no orphaned autonomous sender
```

## 12. Employee-client acceptance

From the actual employee client used in the target:

```text
[ ] Authorized employee can use Communication Assistant for relevant email context
[ ] Employee can request a draft
[ ] Employee sees the exact persisted outbound content in the approval confirmation
[ ] Approval/send result is understandable
[ ] Ambiguous send result clearly says not to resend yet
[ ] Unauthorized employee cannot access another mailbox by prompting
[ ] General Assistant remains usable without Email tools and while provider/send path is unavailable
[ ] No infrastructure credentials/config are exposed to the employee
```

## 13. Capability result

The Tencent Enterprise Mail capability is accepted only when all applicable sections pass.

Record either:

```text
PASS — TENCENT EXMAIL EMAIL INTEGRATION
BLOCKED — REQUIRED INPUT: <specific mailbox/credential/authorization>
FAIL — <specific security/integration boundary>
```

Stage 4 closes only when the governed send/reconciliation assertions pass with controlled recipients on an explicitly authorized validation/deployment target.

A blocked or failed Email capability must not be silently disabled if the active company configuration requires it for `CONFIGURED READY`.
