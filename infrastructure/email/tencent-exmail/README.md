# Tencent Enterprise Mail Integration

Status: v2 installation-design provider playbook / Stage 1 read-only candidate

This playbook defines the smallest approved Enterprise AI Office integration path for Tencent Enterprise Mail (`腾讯企业邮箱`) under the frozen v2 System Design and active Installation Design phase.

Use with:

- `docs/V2-SCOPE.md`
- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-DESIGN-REVIEW.md`
- `docs/V2-IMPLEMENTATION-PLAN.md`
- `docs/ONTOLOGY.md`
- `ontology/examples/email-communication.yaml`
- `docs/acceptance/TENCENT-EXMAIL.md`

This document does not authorize any mailbox credential, mailbox access, or outbound message.

## 1. Provider capabilities relevant to v2

Tencent Enterprise Mail exposes two integration surfaces that must not be confused.

### Mailbox protocols

For actual mailbox-content access and ordinary sending, Tencent Enterprise Mail documents encrypted mail-client protocols:

```text
IMAP over SSL:  imap.exmail.qq.com:993
SMTP over SSL:  smtp.exmail.qq.com:465
```

Tencent also documents overseas endpoints:

```text
IMAP over SSL:  hwimap.exmail.qq.com:993
SMTP over SSL:  hwsmtp.exmail.qq.com:465
```

Do not select the overseas endpoints merely because they exist. Use the endpoint appropriate to the real deployment network and verify it during runtime acceptance.

If mailbox security login is enabled, use the provider-supported client-specific password/credential rather than treating the interactive Web-login flow as an automation credential.

### Enterprise Mail Open API

Tencent Enterprise Mail also exposes enterprise Open API capabilities around areas such as:

```text
address book
new-mail notification / unread count
single sign-on
system/mail logs
feature settings
```

These interfaces may later be useful for event notification or audit correlation, but they are not the primary Stage 1 mechanism for reading message bodies and are not required for the initial read-only pilot.

Do not grant a company-wide Open API credential merely to read one mailbox.

## 2. Frozen v2 provider decision

For the frozen v2 design:

```text
message body/context read  → provider-supported mailbox read surface (initial candidate: IMAP)
outbound send              → later governed provider binding (initial candidate: SMTP)
optional event metadata    → Tencent Open API only if a concrete later requirement justifies it
```

The protocol candidate does not override the business-operation contract.

Do not introduce a generic mail automation platform, n8n, a second workflow engine, or a custom mail database merely to bridge Tencent Enterprise Mail.

## 3. Stage 1 candidate scope

The first installation-stage candidate is:

> Read-only bounded email context.

Approved Agent-facing operation surface:

```text
search_email
get_email
```

Intentionally absent from Stage 1:

```text
send_approved_reply
send_email
generic_smtp_send
generic_imap_command
mailbox_delete
mailbox_move
mailbox_flag_write
mailbox_folder_write
bulk_send
campaign_send
```

Stage 1 must not create any customer-facing side effect.

## 4. Current read-only adapter candidate

Repository candidate:

```text
imap_readonly_mcp.py
```

It is deliberately narrow:

```text
configured mailbox only
allowlisted folders only
read-only mailbox selection
UID SEARCH / FETCH
BODY.PEEK-style message reads
bounded result/body sizes
attachment filenames only
no attachment download
no SMTP
no arbitrary IMAP command
```

Email content is untrusted operational data and must not override system, Profile, security, tool, or approval policy.

Installation Design must re-check whether a mature upstream integration can enforce the same frozen operation/security contract with less maintenance before this custom candidate is frozen as the final path.

## 5. Credential boundary

The first pilot design assumes exactly one explicitly selected mailbox.

Preferred posture:

```text
one pilot mailbox
→ mailbox-specific client credential / client-specific password when available
→ protected runtime secret storage
→ only the authorized integration/Profile boundary receives it
```

Never commit or log:

```text
primary mailbox password
client-specific password
CorpSecret
access token
SMTP/IMAP credential
```

The mailbox credential proves provider access. It does not prove which employee requested or approved an operation.

## 6. Read behavior

Normal Agent reads must not mutate mailbox state as a side effect.

The current candidate implements behavior equivalent to:

```text
select mailbox read-only
fetch content without setting Seen (`BODY.PEEK` semantics)
no delete
no move
no flag mutation
no folder creation
no mailbox-rule change
```

Initial folder scope should remain narrow (normally `INBOX`) until company configuration explicitly expands it.

Email is operational communication context, not authoritative company knowledge. Do not bulk-ingest the mailbox into WeKnora by default.

## 7. Offline deterministic tests first

Before any real mailbox credential is ever used by a future deployment, run the repository-local deterministic tests:

```sh
uv run infrastructure/email/tencent-exmail/test_imap_readonly.py
```

These tests require no real mailbox. They verify the local Stage 1 safety contract:

```text
folder allowlist fails closed
mailbox selection is read-only
search uses UID SEARCH/FETCH-only behavior
message body fetch uses BODY.PEEK
no write-capable email function exists in the adapter surface
```

A passing offline test does **not** prove provider authentication, employee authorization, or real non-mutating behavior against Tencent Enterprise Mail. It is only the first installation-design candidate gate.

Future deployment progression:

```text
offline deterministic tests PASS
→ protected real provider authorization available
→ bounded runtime read-only acceptance
→ Stage 1 PASS
```

Do not skip directly from source-code presence to real mailbox access.

## 8. Hermes registration candidate

Use:

```text
hermes.mcp.example.yaml
```

only as a registration template for an authorized Profile during a future real installation.

The template must expose only:

```text
search_email
get_email
```

Do not add a generic mail protocol toolset.

## 9. Frozen Ontology boundary

The frozen initial v2 email model contains only:

```text
Mailbox       → source-backed by email provider
EmailMessage  → source-backed by email provider
DraftReply    → Enterprise AI Office owned
SendApproval  → Enterprise AI Office owned
```

Policy-relevant relations:

```text
Mailbox contains EmailMessage
DraftReply replies_to EmailMessage
SendApproval authorizes DraftReply
```

The initial design deliberately does **not** create first-class:

```text
EmailThread
Customer
Contact
Lead
Opportunity
CRM record
Calendar event
SendResult object
FollowUp object
```

Provider result/reference belongs in action/audit evidence. Simple scheduled follow-up state belongs to Hermes Cron; persistent multi-step Agent work belongs to Kanban only when later justified.

Do not expand the email Ontology into a shadow CRM.

## 10. Draft and approval boundary

Stage 2/3 introduce the installation contracts for:

```text
prepare_reply_draft
approve_reply_draft
```

A proposed draft is not permission to send.

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

If a material field changes after approval, the previous approval becomes stale.

## 11. Governed send boundary

Stage 4 introduces exactly one initial external Named Action:

```text
send_approved_reply
```

Do not expose generic SMTP/send-anything to ordinary Agents.

Before Stage 4 can be frozen as installable, Installation Design must close:

```text
trusted human actor identity propagation
mailbox-scoped send authorization
exact approval-subject binding
DraftReply / SendApproval persistence
provider send binding
approval revalidation immediately before send
single logical send claim/idempotency
provider result/reference capture
ambiguous-result reconciliation
audit evidence persistence
```

No autonomous customer-facing send is allowed in the initial v2 milestone.

## 12. Failure and retry rule

Email sending is an external side effect.

Do not assume exactly-once delivery and do not blindly retry an ambiguous provider outcome.

Frozen behavior:

```text
ambiguous send result
→ no blind retry
→ reconciliation required
→ inspect provider evidence
→ human/deterministic decision before another send attempt
```

Duplicate avoidance is more important than automatic retry speed.

## 13. Attachment policy

Attachments are outside the initial v2 send milestone.

Stage 1 reports attachment filenames only; it does not download attachment content.

If attachments are later enabled, they require a separate data-exfiltration/security review and must become part of the exact approval subject.

## 14. Optional Tencent Open API use

Do not require Tencent Enterprise Mail Open API for Stage 1.

Evaluate it later only for a concrete need such as:

```text
new-mail event trigger
unread-count signal
mail-log delivery/status correlation
provider protocol-setting inspection
```

If enabled later, protect `CorpSecret`, review application scope, validate callback authenticity/encryption where applicable, and record the additional authority boundary.

## 15. Protected inputs required by a future real Stage 1 activation

A real mailbox connection would require protected company inputs/authority including:

```text
selected pilot mailbox authorization
mailbox owner/business purpose
authorized human user/group scope
authorized Hermes Profile
allowed mailbox folders/read scope
approved client-credential mechanism
protected secret location
actual runtime host access
harmless known test message(s)
```

These are input **classes** during Installation Design, not requests for real values.

A future installer missing them must report:

```text
BLOCKED — REQUIRED INPUT: Stage 1 provider/runtime authorization
```

Do not substitute a broader company credential.

## 16. Acceptance

Use:

```text
docs/acceptance/TENCENT-EXMAIL.md
```

Stage 1 is not accepted merely because IMAP authentication succeeds.

Acceptance must demonstrate applicable boundaries including:

```text
authorized read succeeds
unauthorized human/Profile read fails
out-of-scope folder/mailbox access fails closed
read-only behavior is preserved
credentials remain protected
real employee-client behavior is correct when the capability is exposed
```

Do not report `READ-ONLY EMAIL PASS` until both repository-level deterministic tests and applicable real runtime checks have passed in an explicitly authorized deployment or validation task.

## 17. Provider references

Provider documentation must be re-checked before the provider binding is frozen for real installation because authentication, endpoint, administration, and Open API behavior may change.
