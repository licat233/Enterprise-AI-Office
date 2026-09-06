# Tencent Enterprise Mail Integration Acceptance

Status: conditional capability acceptance

Run this acceptance only when the active company configuration enables the Tencent Enterprise Mail integration.

Use with:

- `docs/V2-SCOPE.md`
- `docs/V2-STAGE-CONTRACTS.md`
- `docs/ONTOLOGY.md`
- `infrastructure/email/tencent-exmail/README.md`
- `docs/SECURITY.md`
- `docs/CLIENT-RBAC.md`
- `config/capabilities.yaml`

A successful IMAP or SMTP login alone is not acceptance.

## Stage mapping

This provider acceptance is reused by the v2 installation Stage contracts rather than duplicated into separate provider test suites.

```text
Stage 0 — v1 baseline
→ docs/ACCEPTANCE-TESTS.md Part A

Stage 1 — read-only email
→ Sections 1–4 and applicable employee-client checks in Section 11

Stage 2 — DraftReply preparation
→ Sections 4–5 and applicable employee-client checks in Section 11

Stage 3 — trusted human approval
→ Section 6 and applicable audit/employee-client checks in Sections 9 and 11

Stage 4 — governed send
→ Sections 7–9 and 11

Stage 5 — optional simple follow-up
→ Section 10 plus docs/ACCEPTANCE-TESTS.md Cron section

Stage 6 — optional messaging surface
→ docs/ACCEPTANCE-TESTS.md Messaging section plus the same email governance boundary
```

The detailed Stage preconditions, inputs, idempotency, evidence, and rollback contracts are authoritative in `docs/V2-STAGE-CONTRACTS.md`.

## 1. Provider and mailbox scope

```text
[ ] Provider recorded as Tencent Enterprise Mail / Tencent Exmail
[ ] Exactly selected pilot mailbox(es) recorded
[ ] Business owner/purpose recorded
[ ] Authorized human users/groups recorded
[ ] Authorized Hermes Profile(s) recorded
[ ] Allowed mailbox folders/read scope recorded
[ ] Attachments disabled unless explicitly required and tested
```

The initial v2 pilot should normally use one mailbox. Adding more mailboxes is a deliberate scope expansion, not an incidental configuration change.

## 2. Credential boundary

```text
[ ] IMAP/SMTP uses TLS endpoints supported by the provider
[ ] Client-specific password/credential used where Tencent security-login policy requires it
[ ] Primary mailbox password is not committed to Git
[ ] Mail credential is stored only in protected runtime secret storage
[ ] Credential is available only to the intended integration process/Profile boundary
[ ] No mailbox credential appears in logs, prompts, audit records, or deployment state
[ ] Company-wide CorpSecret is not granted merely to read/send one mailbox
```

If Tencent Open API is separately enabled:

```text
[ ] Concrete API-backed requirement documented
[ ] CorpSecret protected
[ ] application scope reviewed
[ ] callback signature/encryption validation works if callbacks are enabled
```

## 3. Non-mutating read path

Test with harmless known messages in the configured pilot mailbox.

```text
[ ] Authorized operation can search configured mailbox/folder scope
[ ] Authorized operation can retrieve expected message/thread content
[ ] Read operation does not mark an unread test message as Seen
[ ] Read operation does not move/delete messages
[ ] Read operation does not create folders or change flags/rules
[ ] Unauthorized Profile/user cannot retrieve mailbox content
[ ] Out-of-scope mailbox/folder access fails closed
```

Where implementation uses IMAP directly, verify behavior equivalent to read-only mailbox selection and non-mutating body fetch (`EXAMINE` / `BODY.PEEK` semantics where supported).

## 4. Knowledge/source boundary

```text
[ ] Email content is treated as operational communication context, not automatically as authoritative company knowledge
[ ] Company/product facts in a drafted reply are grounded through approved WeKnora knowledge when required
[ ] Mailbox contents are not bulk-ingested into WeKnora merely to simplify retrieval
[ ] Conflicting email context vs authoritative company source is surfaced rather than silently overwriting company truth
```

## 5. Draft behavior

```text
[ ] Agent can prepare a reply without sending it
[ ] Draft generation alone causes no SMTP side effect
[ ] Final outbound fields are inspectable by the human approver
[ ] Draft clearly identifies target mailbox/thread/recipients before approval
```

## 6. Human approval binding

For the initial v2 send path, approval must bind to the exact outbound subject:

```text
From mailbox
To
Cc/Bcc if enabled
Subject
Body
Thread/reply identity
Attachments if later enabled
```

Acceptance:

```text
[ ] Explicit trusted human approval required before send
[ ] Approval evidence binds to exact final outbound content/state
[ ] Changing recipient, subject, body, thread target, or attachment after approval invalidates approval
[ ] Stale approval produces a structured deny/block result
[ ] Natural-language Agent inference cannot manufacture approval
```

## 7. Send path

Use controlled test recipients before real customer use.

```text
[ ] Only the approved mailbox identity can be used as sender
[ ] Narrow send action succeeds for an approved test message
[ ] Provider result/message evidence recorded without secrets
[ ] Unapproved send attempt fails closed
[ ] Generic SMTP/send-anything primitive is not exposed to ordinary employee Agent surface
[ ] Bulk/campaign sending unavailable in initial v2 scope
[ ] Attachments unavailable unless separately enabled and accepted
```

## 8. Ambiguous failure / duplicate-send safety

Create or simulate a harmless uncertain-result condition where practical.

```text
[ ] Implementation does not blindly retry an ambiguous SMTP outcome
[ ] Retry/idempotency policy documented
[ ] Uncertain outcome becomes reconciliation-required rather than duplicate-send-by-default
[ ] Human/operator can determine or reconcile final send state
```

If the provider/integration cannot guarantee exactly-once delivery, documentation and behavior must state that limitation rather than pretending transactionality exists.

## 9. Audit

Audit/evidence should be sufficient to answer:

```text
who requested the send
which human approved it
which Profile executed it
which mailbox was used
which thread/message was targeted
which recipient set and content hash/version were approved
which Ontology/operation contract version applied
what provider result was observed
whether reconciliation is pending
```

Acceptance:

```text
[ ] Applied send recorded
[ ] Denied/blocked send recorded when policy requires it
[ ] Approval reference recorded
[ ] Provider result/reference recorded
[ ] No mailbox secret or unnecessary full message content stored in audit
```

## 10. Follow-up integration

If Hermes Cron or Kanban is enabled for this email workflow:

```text
[ ] Follow-up state belongs to the configured Hermes capability, not a shadow CRM
[ ] Reminder/action references the correct email thread/customer context
[ ] Scheduled task cannot bypass send approval
[ ] Removing/disabling the email capability leaves no orphaned autonomous sender
```

## 11. Employee-client acceptance

From the actual employee client used in production/pilot:

```text
[ ] Authorized employee can ask for relevant email context
[ ] Employee can request a draft
[ ] Employee sees final outbound content before approval
[ ] Approval/send result is understandable
[ ] Unauthorized employee cannot access another mailbox/thread by prompting
[ ] No infrastructure credentials/config are exposed to the employee
```

## 12. Capability result

The Tencent Enterprise Mail capability is accepted only when all applicable sections pass.

Record either:

```text
PASS — TENCENT EXMAIL EMAIL INTEGRATION
BLOCKED — REQUIRED INPUT: <specific mailbox/credential/authorization>
FAIL — <specific security/integration boundary>
```

A blocked or failed email capability must not be silently disabled if the active company configuration requires it for `CONFIGURED READY`.
