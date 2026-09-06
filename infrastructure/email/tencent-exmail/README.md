# Tencent Enterprise Mail Integration

Status: v2 implementation playbook / not enabled by documentation alone

This playbook defines the smallest approved Enterprise AI Office integration path for Tencent Enterprise Mail (`腾讯企业邮箱`) under `docs/V2-SCOPE.md`.

It is provider-specific because the real provider is now known. It does not authorize any mailbox credential, mailbox access, or outbound message by itself.

## 1. Provider capabilities relevant to v2

Current Tencent Enterprise Mail documentation exposes two different integration surfaces that must not be confused.

### Mailbox protocols

For actual mailbox content access and ordinary sending, Tencent Enterprise Mail documents encrypted mail-client protocols:

```text
IMAP over SSL:  imap.exmail.qq.com:993
SMTP over SSL:  smtp.exmail.qq.com:465
```

Tencent also documents overseas endpoints:

```text
IMAP over SSL:  hwimap.exmail.qq.com:993
SMTP over SSL:  hwsmtp.exmail.qq.com:465
```

Do not select overseas endpoints merely because they exist. Use the endpoint appropriate to the real deployment network and verify it during acceptance.

If mailbox security login is enabled, mail clients use a client-specific password rather than treating the interactive Web-login flow as an automation credential.

### Enterprise Mail Open API

Tencent Enterprise Mail also exposes an enterprise Open API based on `CorpID` / application `CorpSecret` / short-lived access token.

The currently documented API categories are primarily:

```text
address-book management
new-mail notification / unread count
single sign-on
system/mail logs
feature settings
```

The documented `log/mail` query returns mail-log metadata such as subject, sender, receiver, timestamp, and status. New-mail callback payloads expose metadata such as MailID, sender, title, time, and unread count.

These interfaces are useful for optional event notification, administration, or audit correlation, but they are not a substitute for IMAP when Enterprise AI Office needs authorized access to message bodies, nor are they the primary v2 sending mechanism.

## 2. v2 integration decision

For the initial v2 operational loop:

```text
mail body / thread read  → IMAP
outbound send            → SMTP
optional event metadata  → Tencent Enterprise Mail Open API callback/log API only if justified later
```

Do not introduce a generic mail automation platform, n8n, a second workflow engine, or a custom mail database merely to bridge Tencent Enterprise Mail.

## 3. Credential boundary

The first pilot must use exactly one explicitly selected mailbox.

Preferred credential posture:

```text
one pilot mailbox
→ mailbox-specific client credential / client-specific password when available
→ protected runtime secret storage
→ only the authorized Hermes Profile/integration process receives it
```

Never commit or log:

```text
primary mailbox password
client-specific password
CorpSecret
access token
SMTP/IMAP credential
```

Do not grant a company-wide `CorpSecret` merely because v2 needs one mailbox's message body.

A company-wide Open API credential may be introduced only if a specific API-backed requirement such as new-mail callback or mail-log correlation justifies it and its scope is separately reviewed.

## 4. Read path — read-only first

The first runtime milestone is read-only mailbox access.

The adapter/tool must be designed so normal Agent reads do not mutate mailbox state as a side effect.

Prefer protocol behavior equivalent to:

```text
select mailbox read-only (`EXAMINE` where supported)
fetch message content without setting Seen (`BODY.PEEK` semantics)
no delete
no move
no flag mutation
no folder creation
no mailbox rule changes
```

Initial read operations should be narrow, for example:

```text
search_mail
get_thread
get_message
```

They must be constrained by configured mailbox/folder scope and Profile/human authorization.

Email is operational communication data, not authoritative company knowledge. Do not bulk-ingest the mailbox into WeKnora by default.

## 5. Draft path

Draft generation does not itself require SMTP.

The Agent may combine:

```text
authorized email/thread context
+
WeKnora company/product evidence
+
Profile/Sales Skill behavior
```

to prepare a proposed reply.

A proposed reply is not permission to send it.

## 6. Send path — human approval required

The initial v2 send operation must remain human-in-the-loop.

A governed send must bind approval to the exact final outbound subject:

```text
from mailbox
To
Cc/Bcc if enabled
subject
body
attachments if later enabled
reply/thread identity
```

If any material outbound field changes after approval, the approval becomes stale and the send must require a new approval under `docs/ONTOLOGY.md`.

Initial scope should exclude bulk sending and autonomous campaign delivery.

Prefer one narrow Named Action such as:

```text
send_approved_reply
```

rather than exposing a generic SMTP send primitive directly to the Agent.

## 7. Tool surface

The preferred future Agent-facing surface is narrow:

```text
search_mail
get_thread
get_message
send_approved_reply
```

Intentionally absent from the ordinary employee Profile surface:

```text
generic_imap_command
generic_smtp_send
mailbox_delete
mailbox_move
mailbox_flag_write
mail_admin
bulk_send
```

The actual implementation may use an existing supported MCP/mail component if one can enforce these boundaries. Otherwise use the smallest reviewable adapter needed for this provider.

## 8. Ontology boundary

This real writable integration reactivates Ontology work only for the objects/actions required by the email loop.

Likely minimal concepts include:

```text
Mailbox
EmailThread
EmailMessage
DraftReply
SendApproval / approval evidence
SendResult
FollowUp
```

Do not expand this into CRM objects unless the real email workflow later requires CRM integration.

Critical rules include:

```text
mailbox visibility
thread/message read authorization
exact approval-subject binding
trusted human actor identity
Named Action for send
idempotency / uncertain-send handling
audit linkage to provider result
```

## 9. Failure and retry rules

SMTP delivery attempts are external side effects.

The implementation must not blindly retry after an ambiguous transport failure if doing so could send the same customer message twice.

Before production use define:

```text
idempotency strategy where technically possible
provider message/result evidence
ambiguous-outcome handling
manual reconciliation path
```

If delivery outcome cannot be established safely:

```text
BLOCKED / RECONCILIATION REQUIRED
```

is preferable to a duplicate customer email.

## 10. Initial attachment policy

Attachments are outside the first send milestone unless a real pilot workflow requires them.

If later enabled, attachment filename/type/size/content reference must become part of the approval subject and acceptance testing.

Do not silently expand from text reply to arbitrary file exfiltration.

## 11. Optional Tencent Open API use

Do not require the enterprise Open API for the initial IMAP/SMTP pilot.

Evaluate it later only for a concrete need such as:

```text
new-mail event trigger
unread-count signal
mail-log delivery/status correlation
mailbox protocol-setting inspection
```

If enabled, protect `CorpSecret`, validate callback signatures/encryption according to Tencent's callback contract, and record the additional authority/data boundary.

## 12. Required company inputs before activation

Before enabling this capability, the adopting company must supply or approve:

```text
selected pilot mailbox
mailbox owner/business purpose
authorized Hermes Profile(s)
authorized human user/group scope
allowed mailbox folders/read scope
whether security login is enabled
approved client-credential mechanism
outbound-send approval policy
initial recipient/test scope
whether attachments are disabled (default) or explicitly required
```

Missing credentials/authority must produce `BLOCKED — REQUIRED INPUT`; do not substitute a broader company credential.

## 13. Acceptance

Use the `Tencent Enterprise Mail email integration` section in `docs/ACCEPTANCE-TESTS.md`.

A successful IMAP login or SMTP test alone is not acceptance. The employee authorization, non-mutating read behavior, approval binding, outbound result, credential isolation, and fail-closed behavior must all be demonstrated.

## 14. Provider references

Provider documentation reviewed for this playbook includes:

- Tencent Enterprise Mail client settings/help for IMAP/SMTP SSL endpoints and client-specific password behavior;
- Tencent Enterprise Mail Open API index and access-token contract;
- Tencent Enterprise Mail mail-log query contract;
- Tencent Enterprise Mail new-mail callback/unread metadata contract.

Re-check current provider documentation at implementation time because authentication and administration controls may change.