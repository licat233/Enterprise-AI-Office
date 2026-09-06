# Tencent Enterprise Mail Integration Acceptance

Status: conditional capability acceptance

Run this acceptance only when the active company configuration enables the Tencent Enterprise Mail integration.

Use with:

- `docs/V2-SCOPE.md`
- `docs/V2-STAGE-CONTRACTS.md`
- `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`
- `docs/V2-GOVERNANCE-RUNTIME.md`
- `docs/ONTOLOGY.md`
- `infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md`
- `infrastructure/open-webui/V2-APPROVAL-ACTION.md`
- `infrastructure/email/governance/README.md`
- `infrastructure/email/tencent-exmail/README.md`
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

## 8. Send path

Use controlled test recipients before real customer use.

```text
[ ] Only the approved mailbox identity can be used as sender
[ ] Current email.send permission is re-checked immediately before send
[ ] Approval is atomically claimed for one logical send before provider side effect
[ ] Narrow send action succeeds for an approved test message
[ ] Provider result/message evidence recorded without secrets
[ ] Unapproved send attempt fails closed
[ ] Stale/revoked/previously-claimed approval send fails closed
[ ] Generic SMTP/send-anything primitive is not exposed to ordinary employee Agent surface
[ ] Bulk/campaign sending unavailable in initial v2 scope
[ ] Attachments unavailable unless separately enabled and accepted
```

## 9. Ambiguous failure / duplicate-send safety

Create or simulate a harmless uncertain-result condition where practical.

```text
[ ] Implementation does not blindly retry an ambiguous SMTP outcome
[ ] Retry/idempotency policy documented
[ ] Uncertain outcome becomes reconciliation-required rather than duplicate-send-by-default
[ ] Human/operator can determine or reconcile final send state
```

If the provider/integration cannot guarantee exactly-once delivery, documentation and behavior must state that limitation rather than pretending transactionality exists.

## 10. Audit

Audit/evidence should be sufficient to answer:

```text
who requested the send
which HumanActor approved it
which Assistant/Profile context was involved
which mailbox was used
which source message was targeted
which recipient set and content hash/version were approved
which Ontology/operation contract version applied
what provider result was observed
whether reconciliation is pending
```

Acceptance:

```text
[ ] Draft/approval/claim governance events are append-oriented
[ ] Applied send recorded
[ ] Denied/blocked send recorded when policy requires it
[ ] Approval reference recorded
[ ] Provider result/reference recorded
[ ] No mailbox/forwarder secret or unnecessary full message content stored in audit
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
[ ] Unauthorized employee cannot access another mailbox by prompting
[ ] General Assistant remains usable without Email tools
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

A blocked or failed Email capability must not be silently disabled if the active company configuration requires it for `CONFIGURED READY`.
