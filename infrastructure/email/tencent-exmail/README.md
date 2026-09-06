# Tencent Enterprise Mail Integration

Status: v2 installation-design provider playbook / governance-wrapped provider adapter

This playbook defines the smallest approved Enterprise AI Office integration path for Tencent Enterprise Mail (`腾讯企业邮箱`) under the frozen v2 System Design and active Installation Design phase.

Use with:

- `docs/V2-SCOPE.md`
- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-DESIGN-REVIEW.md`
- `docs/V2-IMPLEMENTATION-PLAN.md`
- `docs/V2-INSTALLATION-ARCHITECTURE.md`
- `docs/V2-STAGE-CONTRACTS.md`
- `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`
- `infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md`
- `docs/ONTOLOGY.md`
- `ontology/examples/email-communication.yaml`
- `docs/acceptance/TENCENT-EXMAIL.md`

This document does not authorize any mailbox credential, mailbox access, or outbound message.

## 1. Provider capabilities relevant to v2

Tencent Enterprise Mail exposes mailbox protocols and enterprise Open API surfaces that must not be confused.

### Mailbox protocols

Current documented encrypted mail-client endpoints used by the reference candidate are:

```text
IMAP over SSL:  imap.exmail.qq.com:993
SMTP over SSL:  smtp.exmail.qq.com:465
```

Tencent also documents overseas endpoint variants. Do not select them merely because they exist; use the endpoint appropriate to the authorized deployment network and re-verify provider documentation at deployment time.

If mailbox security login is enabled, use the provider-supported client-specific password/credential rather than treating the interactive Web-login flow as an automation credential.

### Enterprise Mail Open API

Tencent Enterprise Mail Open API may later be useful for concrete requirements such as notification or provider-log correlation, but it is not required for the initial bounded mailbox read/send path.

Do not grant a company-wide Open API credential merely to read one mailbox.

## 2. Frozen provider boundary

```text
message body/context read  → provider-supported mailbox read surface (initial candidate: IMAP)
outbound send              → governed provider binding (initial candidate: SMTP)
optional event metadata    → Tencent Open API only if a concrete requirement later justifies it
```

The protocol candidate does not override the governed business-operation contract.

Do not introduce a generic mail automation platform, n8n, second workflow engine, or custom mail database merely to bridge Tencent Enterprise Mail.

## 3. Stage 1 operation surface

Approved employee/model-facing operation surface:

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

Stage 1 must not create customer-facing side effects.

## 4. Current read adapter candidate

Repository candidate:

```text
imap_readonly_mcp.py
```

It remains useful as a narrow provider-adapter prototype and deterministic safety-test asset:

```text
configured mailbox only
allowlisted folders only
read-only mailbox selection
UID SEARCH / FETCH
BODY.PEEK-style reads
bounded result/body sizes
attachment filenames only
no attachment download
no SMTP
no arbitrary IMAP command
```

For the reference runtime, this provider logic sits **behind `eao-email-governance`** rather than being registered directly into Hermes.

The governance service is responsible for trusted HumanActor authorization before provider access.

The file name retains `_mcp` because it originated as the Stage 1 design-support prototype; its existence does not make direct Hermes MCP registration the reference installation path.

## 5. Credential boundary

Reference posture:

```text
selected mailbox
→ mailbox-specific provider/client credential
→ protected runtime secret storage
→ eao-email-governance/provider adapter boundary only
```

Never commit or log:

```text
primary mailbox password
client-specific password
CorpSecret
access token
SMTP/IMAP credential
```

The mailbox credential proves provider access only. It does not identify or authorize a HumanActor.

## 6. Trusted HumanActor path

The reference path is:

```text
Employee
→ authenticated Open WebUI session
→ Communication Assistant
→ Hermes communication Profile for reasoning
→ Open WebUI server-side Email Governance tool execution
→ eao-email-governance
→ Tencent provider adapter
```

Open WebUI supplies current HumanActor/group context through the protected trusted-forwarder contract defined in:

```text
docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md
```

Do not accept employee identity from:

```text
prompt text
LLM-generated tool arguments
mailbox username
Hermes Profile key
provider credential
```

## 7. Read behavior

Normal reads must not mutate mailbox state as a side effect.

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

Initial folder scope should remain narrow until private company configuration expands it explicitly.

Email is operational context, not authoritative company knowledge. Do not bulk-ingest the mailbox into WeKnora by default.

## 8. Offline deterministic tests first

Before any real mailbox credential is used by an authorized future target, run:

```sh
uv run infrastructure/email/tencent-exmail/test_imap_readonly.py
```

The tests require no real mailbox and verify the provider-adapter safety properties:

```text
folder allowlist fails closed
mailbox selection is read-only
search uses UID SEARCH/FETCH-only behavior
message body fetch uses BODY.PEEK
no write-capable email function exists in the adapter surface
```

A passing offline test does not prove provider authentication, HumanActor authorization, or live provider non-mutation.

Future Stage 1 progression is:

```text
offline adapter tests PASS
→ governance identity/authorization path installed
→ protected provider credential available on authorized target
→ bounded runtime read acceptance
→ Stage 1 PASS
```

## 9. Runtime registration path

The previous direct Hermes MCP registration template is no longer the reference path and has been removed.

Reference runtime registration is:

```text
Open WebUI admin-managed Email Governance external-tool connection
→ eao-email-governance private MCP/OpenAPI endpoint
→ provider adapter
```

Use:

```text
infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md
```

The Communication Assistant is still backed by the isolated Hermes communication Profile for reasoning, but Hermes does not carry trusted HumanActor identity into the provider adapter.

## 10. Frozen Ontology boundary

The initial v2 email model remains:

```text
Mailbox       → source-backed by email provider
EmailMessage  → source-backed by email provider
DraftReply    → Enterprise AI Office owned
SendApproval  → Enterprise AI Office owned
```

Do not expand this into a shadow CRM.

Provider result/reference belongs in action/audit evidence. Simple scheduled follow-up belongs to Hermes Cron; durable multi-step Agent work belongs to Kanban only when justified.

## 11. Draft and approval boundary

Stage 2/3 implement:

```text
prepare_reply_draft
approve_reply_draft
```

Approval binds to the exact material outbound subject, including sender mailbox, recipients, subject, body, source/reply identity and Draft revision/hash.

A material edit invalidates the previous approval for the new Draft revision.

Formal approval comes from the trusted server-side human Action path, never free-form model inference.

## 12. Governed send boundary

Stage 4 introduces exactly one initial external Named Action:

```text
send_approved_reply
```

Do not expose generic SMTP/send-anything to ordinary Agents.

The governance service must revalidate current HumanActor/mailbox permission, exact Draft revision/hash and valid SendApproval before invoking the provider send adapter.

## 13. Failure and retry rule

Email send is an external side effect.

```text
confirmed SENT
→ no retry

confirmed NOT SENT
→ controlled retry may be allowed for the same immutable logical send

ambiguous outcome
→ RECONCILIATION_REQUIRED
→ no blind retry
```

Duplicate avoidance is more important than automatic retry speed.

## 14. Attachment policy

Attachments remain outside the initial v2 send milestone.

Stage 1 may report attachment filenames only. If attachments are later enabled, they require separate data/security review and become part of the exact approval subject.

## 15. Optional Tencent Open API use

Do not require Tencent Enterprise Mail Open API for Stage 1.

Evaluate it later only for a concrete requirement such as new-mail signals or provider-log correlation.

If enabled, protect `CorpSecret`, review scope, validate callback authenticity/encryption where applicable, and record the additional authority boundary.

## 16. Protected input classes for a future authorized target

A real provider activation may require:

```text
selected mailbox authorization
mailbox business purpose
Communication employee group scope
mailbox grants
resolved Open WebUI group IDs
Open WebUI → Governance forwarder credential
mailbox provider/client credential
allowed folders
controlled test recipient scope
actual runtime target authority
harmless known test messages
```

These are input classes during Installation Design, not requests for real values.

Missing runtime authority/input during an authorized execution must be reported specifically as:

```text
BLOCKED — REQUIRED INPUT: <specific input>
```

Do not substitute broader company credentials.

## 17. Acceptance

Use:

```text
docs/acceptance/TENCENT-EXMAIL.md
```

Stage 1 is not accepted because IMAP login succeeds.

Acceptance must demonstrate applicable provider, HumanActor, mailbox-scope, non-mutating-read, credential-protection and employee-client boundaries.

Do not report `READ-ONLY EMAIL PASS` until repository-level deterministic tests and applicable target runtime checks pass on an explicitly authorized validation/deployment target.

## 18. Provider references

Provider documentation must be re-checked before real installation because authentication, endpoint, administration and Open API behavior may change.
