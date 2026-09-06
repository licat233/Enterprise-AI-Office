# Enterprise AI Office v2 — Governance Runtime Installation Contract

Status: governance runtime contract frozen / real deployment not authorized
Version: 1.0
Date: 2026-09-06

This document closes `ID-5 — Draft / Approval governance runtime` for the Enterprise AI Office v2 `installation_design` phase.

It defines the minimum deterministic runtime owned by `eao-email-governance` for DraftReply revisions, trusted human approval evidence, single-logical-send claiming, and append-oriented governance audit.

It does **not** authorize a real company installation, mailbox credential, provider send, or customer-facing side effect. Provider send transport and ambiguous-outcome reconciliation are completed under ID-6.

Use with:

- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-INSTALLATION-ARCHITECTURE.md`
- `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`
- `docs/V2-STAGE-CONTRACTS.md`
- `docs/V2-CONFIG-PROTECTED-INPUTS.md`
- `ontology/examples/email-communication.yaml`
- `infrastructure/email/governance/schema.sql`

---

## 1. Runtime scope

The reference runtime remains one thin local service:

```text
eao-email-governance
```

It owns only deterministic EAO email-governance state and policy enforcement.

It does not own:

```text
LLM inference
employee authentication
Open WebUI groups
company knowledge
provider mailbox truth
Cron/Kanban
CRM/customer state
mailbox mirroring
generic workflow execution
```

Reference persistence:

```text
SQLite
<runtime_root>/runtime/email-governance/state.sqlite3
```

No PostgreSQL, Redis, queue, event bus, or separate Approval/Audit service is required for the single-host baseline.

---

## 2. Runtime-owned records

The minimum persistent record classes are:

```text
DraftReply revisions
SendApproval evidence
ApprovalClaim evidence
governance audit events
```

`ApprovalClaim` is runtime execution evidence, not a fifth Email Ontology business object. It exists only to enforce:

```text
one SendApproval
→ at most one logical send operation
```

Provider send result/reconciliation tables are deliberately not frozen here; ID-6 extends the runtime without changing these Stage 2/3 contracts.

---

## 3. Draft identity and immutable revisions

The runtime representation is:

```text
logical draft identity: draft_id
immutable revision identity: (draft_id, revision)
```

This makes the System Design rule executable:

```text
material edit
→ new revision
→ old revision remains historical evidence
```

A DraftReply revision is never updated in place after creation.

The current revision is derived as the greatest committed `revision` for one `draft_id`.

The runtime does not require a mutable `draft_head` table for the baseline.

---

## 4. Draft material fields

Each immutable revision persists at least:

```text
draft_id
revision
source_message_id
sender_mailbox_id
to_addresses
cc_addresses
subject
body
content_hash
created_by_actor_id
created_at
```

Attachments and Bcc remain outside the initial v2 milestone.

Inbound provider message bodies are not copied into this database merely to support DraftReply state.

---

## 5. Canonical content hash

`content_hash` binds approval to the exact material outbound state.

Reference algorithm:

```text
SHA-256 over UTF-8 canonical JSON
```

Canonical object keys:

```text
schema
draft_id
revision
source_message_id
sender_mailbox_id
to_addresses
cc_addresses
subject
body
```

Reference schema marker:

```text
eao.draft-reply.v1
```

Serialization contract:

```text
JSON object keys sorted lexicographically
UTF-8
no insignificant whitespace
Unicode emitted as stored
array order preserved
null and [] are not interchangeable
```

Reference output format:

```text
sha256:<lowercase hex digest>
```

The service hashes the final stored outbound values. The LLM/client does not provide a trusted hash.

The service must return the persisted `draft_id`, `revision`, and computed `content_hash` with the reviewable DraftReply.

---

## 6. Draft creation / revision transaction

`prepare_reply_draft` is a governed business operation, not an installer replay primitive.

Within one SQLite write transaction:

```text
1. authenticate trusted Open WebUI forwarder
2. resolve HumanActor + current groups
3. enforce email.read + email.draft on sender mailbox/source context
4. validate final outbound fields
5. acquire write transaction
6. determine next revision for draft_id
7. compute content_hash from exact revision payload
8. INSERT immutable draft revision
9. INSERT audit event
10. COMMIT
```

If any step before commit fails:

```text
ROLLBACK
→ no partial DraftReply/audit success
```

Reference SQLite write mode for mutation operations:

```text
BEGIN IMMEDIATE
```

This avoids two concurrent writers allocating the same next revision without requiring a distributed lock.

For a brand-new DraftReply, the service may allocate a new opaque UUID/ULID-style `draft_id` server-side.

For an explicit edit, the caller references the existing `draft_id`; the service creates `revision + 1`.

---

## 7. Draft request deduplication

Do not use `source_message_id + actor_id` as a permanent uniqueness constraint because the same employee may intentionally prepare multiple candidate replies.

The baseline therefore distinguishes:

```text
transport/request replay
≠
intentional new draft/revision request
```

A trusted client may send an opaque request idempotency key for accidental HTTP/tool replay.

If implemented, store/resolve it only for the operation result and do not make it the business identity of DraftReply.

Absent an explicit idempotency key, a new valid `prepare_reply_draft` invocation is allowed to create a new draft/revision.

---

## 8. SendApproval evidence

A SendApproval is immutable approval evidence bound to:

```text
approval_id
draft_id
draft_revision
draft_content_hash
approved_by_actor_id
approved_at
optional valid_until
```

The baseline does not require a universal Approval TTL. `valid_until` is nullable and becomes active only if company policy later configures expiration.

Approval creation requires the exact currently reviewable Draft revision/hash and current `email.approve` authorization for the sender mailbox.

Natural-language inference does not call this operation.

---

## 9. Approval state is derived

Avoid one mutable mega-status column.

Approval validity is derived from immutable evidence plus disposition facts.

Reference evaluation order:

```text
if revoked_at exists
→ REVOKED

else if approval claim exists
→ CONSUMED

else if valid_until exists and now > valid_until
→ EXPIRED

else if approval draft revision/hash != current draft revision/hash
→ STALE

else
→ ACTIVE
```

`STALE` therefore does not require rewriting historical Approval evidence.

A later Draft revision automatically makes an older unconsumed Approval stale for the current Draft.

---

## 10. Approval creation transaction

Within one SQLite write transaction:

```text
1. authenticate trusted Open WebUI approval path
2. resolve HumanActor + current groups
3. load exact Draft revision referenced by the trusted review subject
4. confirm referenced revision/hash match persisted state
5. confirm referenced revision is still current for that draft
6. enforce current email.approve mailbox grant
7. reject revoked/invalid review subject
8. INSERT SendApproval or return the existing equivalent approval for replay
9. INSERT audit event
10. COMMIT
```

Duplicate delivery of the **same trusted approval interaction** must not create multiple independently reusable approvals.

Reference uniqueness for replay-safe approval creation:

```text
(draft_id, draft_revision, draft_content_hash, approved_by_actor_id)
```

Returning the existing approval is acceptable for exact replay.

A different authorized human may separately approve the same exact Draft when a future policy requires it; the schema must not globally forbid that.

---

## 11. Trusted review subject

The approval path must know which exact Draft revision/hash the human is approving without trusting LLM-generated authority.

Baseline contract:

```text
Governance service creates/returns exact Draft review data
→ Open WebUI presents sender/To/Cc/subject/body
→ trusted server-side Action submits exact draft_id/revision/content_hash
→ Governance service reloads persisted Draft state and revalidates it
```

The human identity comes from `__user__` / trusted forwarder per ID-4, never from these Draft identifiers.

The Draft identifiers are **subject selectors**, not authority tokens.

A tampered selector can at most request approval of another object; governance must still enforce:

```text
actor can see the Draft
+
actor has email.approve on its mailbox
+
exact persisted revision/hash match
+
current revision match
```

For the baseline, this is sufficient without introducing a second signed presentation-token service.

If later UI implementation cannot prove that the exact Draft fields were presented before the Action, Installation Design must fail closed and add the smallest presentation-binding mechanism then; do not infer approval from chat text.

---

## 12. Revoke approval

A minimal deterministic revocation operation may exist for an ACTIVE approval before it is claimed.

Reference facts persisted on the approval row:

```text
revoked_at
revoked_by_actor_id
revoke_reason_code
```

Revocation does not delete historical approval evidence.

Once an Approval has been claimed for a logical send, ordinary revoke must not pretend the external side effect can be undone.

ID-6 defines behavior after claim/provider execution begins.

---

## 13. Single logical send claim

Before any provider send side effect, Stage 4 must atomically claim one valid Approval for one logical send operation.

ID-5 freezes only the claim primitive:

```text
claim_approval_for_send(
  approval_id,
  logical_send_id,
  current_actor,
  expected_draft_id,
  expected_revision,
  expected_content_hash
)
```

Inside one SQLite transaction it must:

```text
1. re-authenticate trusted caller/HumanActor context
2. re-evaluate current email.send authorization
3. reload Draft revision/hash
4. derive Approval state
5. require ACTIVE
6. require exact Draft/Approval binding
7. INSERT approval_claim with UNIQUE approval_id
8. INSERT audit event
9. COMMIT
```

The unique constraint guarantees:

```text
same approval
→ cannot authorize two logical_send_id values
```

The claim happens **before** provider side effect.

ID-6 defines provider attempts, confirmed-not-sent retry, ambiguous outcomes, and reconciliation around the claimed logical send.

---

## 14. Governance audit

Governance audit is append-oriented evidence, not a mutable operational log.

Minimum event fields:

```text
audit_event_id
occurred_at
human_actor_id
human_group_ids_at_decision
assistant_id/profile_context when available
operation
target_type
target_id
mailbox_id
decision
reason_code
correlation_id
contract_version
policy_version
metadata_json
```

`metadata_json` is sanitized structured evidence only.

Do not store in audit:

```text
mailbox passwords
provider tokens
Open WebUI session/bearer tokens
trusted-forwarder token
full inbound message bodies
full DraftReply body when draft_id/revision/hash is sufficient
```

DraftReply body already belongs in the DraftReply table because it is the exact EAO-owned outbound artifact.

---

## 15. Audit append discipline

Normal governance operations append new events.

Examples:

```text
DRAFT_REVISION_CREATED
APPROVAL_CREATED
APPROVAL_REVOKED
APPROVAL_CLAIMED
AUTHORIZATION_DENIED
```

Do not rewrite old events when later facts change.

Examples:

```text
Approval later stale
→ old APPROVAL_CREATED remains true

Approval revoked
→ append APPROVAL_REVOKED

claim created
→ append APPROVAL_CLAIMED
```

`STALE` may be derived at query/decision time and does not require noisy `APPROVAL_BECAME_STALE` events for every draft edit unless future audit policy explicitly requires it.

---

## 16. SQLite constraints and pragmas

Reference service startup enables at least:

```text
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
PRAGMA busy_timeout = <bounded milliseconds>;
```

The installer must verify the selected SQLite library/build supports the chosen journal mode on the deployment filesystem.

Do not place the database on an unsafe network filesystem merely to simulate HA.

Single-host local persistent storage is the reference posture.

---

## 17. Schema migration contract

The service owns explicit forward-only schema migrations.

Minimum rules:

```text
schema version recorded in SQLite
migration runs before service becomes ready
migration executes transactionally where SQLite permits
backup/restore boundary checked before destructive migration
unknown newer schema version → service refuses write startup
failed migration → service not ready / fail closed
```

Do not let application startup silently drop/recreate the governance database.

ID-7 closes backup/restore and clean-host migration acceptance.

---

## 18. Service endpoint classes

The reference governance service exposes two private logical endpoint classes.

### Employee tool endpoints

Called only through the authenticated Open WebUI trusted-forwarder path:

```text
search_email
get_email
prepare_reply_draft
```

Stage gating controls which are enabled.

### Trusted human action endpoints

Called only through deterministic Open WebUI server-side Actions:

```text
approve_reply_draft
revoke_reply_approval (when enabled)
```

Later Stage 4 may use an internal/trusted action path for:

```text
claim_approval_for_send
send_approved_reply
```

Do not expose formal approval as a free-choice LLM tool.

Exact HTTP/MCP wire shape may be implemented as one small private API/tool server; do not create separate services per endpoint class.

---

## 19. Service health / readiness

Reference health semantics:

```text
liveness
→ process event loop/server responds

readiness
→ configuration loaded
→ SQLite opened
→ required schema version accepted
→ trusted-forwarder auth configured
→ mailbox authorization policy loaded
```

Stage-specific readiness may additionally require provider read/send bindings.

The v1 General Assistant must not depend on this readiness check.

---

## 20. Stage 2 acceptance

Draft runtime acceptance must prove:

```text
[ ] new Draft creates revision 1
[ ] material edit creates revision 2, does not overwrite revision 1
[ ] content_hash is server-computed and deterministic
[ ] same stored revision re-hashes identically after restart
[ ] unauthorized actor cannot create/read Draft for another mailbox
[ ] Draft persists across governance service restart
[ ] Draft creation has no provider send side effect
[ ] failed transaction leaves no partial Draft/audit success
```

Result:

```text
PASS — DRAFT PREPARATION PASS
```

---

## 21. Stage 3 acceptance

Approval runtime acceptance must prove:

```text
[ ] trusted authorized human creates exact approval
[ ] duplicate delivery of same approval interaction returns same/equivalent approval rather than reusable duplicates
[ ] wrong revision fails
[ ] wrong content_hash fails
[ ] older approval becomes STALE after a new Draft revision
[ ] revoked approval derives REVOKED and cannot be claimed
[ ] natural-language-only instruction cannot create SendApproval
[ ] Approval persists across restart
[ ] service re-checks current email.approve permission
[ ] approval contains stable HumanActor id, not email/display-name authority
```

Result:

```text
PASS — APPROVAL GATE PASS
```

---

## 22. Claim acceptance before ID-6

The local claim primitive must prove offline/synthetically:

```text
[ ] ACTIVE exact approval can be claimed once
[ ] second logical_send_id cannot claim the same approval
[ ] stale approval cannot be claimed
[ ] revoked approval cannot be claimed
[ ] expired approval cannot be claimed when expiration policy is configured
[ ] current email.send permission is re-checked
[ ] claim and audit event are committed atomically
[ ] no provider network send is required for this test
```

Provider transport acceptance remains ID-6.

---

## 23. Explicitly rejected ID-5 alternatives

### Persist Draft/Approval only in Open WebUI chat

Rejected: conversation text is not deterministic governance state.

### Persist Draft/Approval in Hermes memory/session

Rejected: Profile/session state is not the trusted human approval authority and must not control external side effects.

### One mutable workflow-status row

Rejected: it mixes Draft, Approval, send execution, and provider outcome into ambiguous state.

### New workflow engine / event bus

Rejected: Stage 2/3 need a few transactional records, not a workflow platform.

### New database server

Rejected for the single-host baseline; SQLite provides the required local transactional constraints with far lower operational cost.

---

## 24. ID-5 completion gate

ID-5 is closed when the Installation Blueprint establishes:

```text
[✓] one thin governance service remains the only new EAO runtime
[✓] SQLite is the single-host governance persistence baseline
[✓] immutable Draft revisions use (draft_id, revision)
[✓] exact deterministic content_hash contract exists
[✓] SendApproval binds exact draft/revision/hash
[✓] ACTIVE/STALE/REVOKED/CONSUMED are deterministic/derived
[✓] approval replay does not create reusable duplicate authority
[✓] one Approval can be claimed by only one logical send
[✓] claim is transactional and precedes provider side effect
[✓] audit evidence is append-oriented
[✓] secrets/full unnecessary mailbox content are excluded from audit
[✓] trusted approval remains server-side HumanActor action
[✓] schema/migration/readiness fail closed
[✓] provider send/reconciliation remains isolated to ID-6
```

Result:

```text
ID-5: PASS
GOVERNANCE RUNTIME CONTRACT FROZEN
```
