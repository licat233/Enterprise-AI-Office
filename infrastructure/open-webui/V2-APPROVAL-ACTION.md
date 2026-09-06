# Open WebUI v2 Deterministic Approval Action

Status: Installation Design reference / no real deployment authorized

Reference implementation:

```text
infrastructure/open-webui/v2_approve_draft_action.py
```

Normative runtime contract:

```text
docs/V2-GOVERNANCE-RUNTIME.md
```

This Action is version-bound to the first validated Open WebUI reference line:

```text
Open WebUI v0.11.3
```

The selected release must be re-verified before a future target imports the Action.

## Why this Action exists

Formal email approval must be a deterministic human action, not a model tool call or interpretation of chat text.

The pinned Open WebUI Action runtime supplies the authenticated current user as `__user__`; its Action route also carries the current chat and assistant-message identifiers. Open WebUI's server-side group model can resolve the current user's group membership.

The reference Action therefore uses:

```text
current __user__.id
current Open WebUI group IDs
current chat_id
current assistant message id
```

and never accepts human authority from model-generated arguments.

## Review binding

When `prepare_reply_draft` creates the exact Draft revision, governance records:

```text
HumanActor
+ chat_id
+ assistant message_id
→ draft_id + revision + content_hash
```

in `draft_review_bindings`.

That binding selects the exact server-owned review subject for the Action. It is not approval authority.

The Action never parses `draft_id`, revision, or hash from assistant text.

## What happens when the employee clicks Approve

```text
1. Open WebUI authenticates the employee and executes the server-side Action.
2. Action resolves current Open WebUI groups.
3. Action calls governance /v1/actions/resolve-current-review using the protected forwarder channel.
4. Governance resolves the exact review binding and returns the persisted Draft fields.
5. Action shows an Open WebUI native confirmation dialog containing exact From/To/Cc/Subject/Body.
6. Employee confirms or cancels.
7. On confirm, Action calls /v1/actions/approve-current-review with the same chat/message context plus the exact revision/hash it just displayed.
8. Governance reloads current state, re-checks HumanActor/mailbox authorization, revision/hash/currentness, and creates or replay-resolves SendApproval.
9. Stage 3 performs no provider send.
```

The confirmation dialog is important: the employee approves governance-owned persisted content, not a possibly paraphrased model rendering.

## Required Open WebUI runtime bindings

Inject server-side only:

```text
EAIO_GOVERNANCE_URL
EAIO_TRUSTED_FORWARDER_TOKEN
```

The token must not be exposed in browser state, model context, Action output, or logs.

## Required Action access

Provision the Action only on the restricted Communication Assistant/Model.

Do not attach it to:

```text
General Assistant
public/wildcard models
ordinary unrelated Assistants
```

The Open WebUI Action route's own model/resource checks are one gate; governance mailbox authorization remains authoritative for the email operation.

## Governance endpoint contract used by the template

### Resolve current review

```text
POST /v1/actions/resolve-current-review
```

Trusted identity comes from headers defined in ID-4.

Body:

```json
{
  "chat_id": "<current chat>",
  "message_id": "<current assistant message>"
}
```

Response contains at least:

```text
draft_id
revision
content_hash
sender_mailbox_id
sender_mailbox_address when available
to_addresses
cc_addresses
subject
body
```

Governance returns only a review binding owned/visible to the current trusted HumanActor.

### Approve current review

```text
POST /v1/actions/approve-current-review
```

Body:

```json
{
  "chat_id": "<current chat>",
  "message_id": "<current assistant message>",
  "expected_draft_id": "<server-resolved draft>",
  "expected_revision": 1,
  "expected_content_hash": "sha256:<digest>"
}
```

The expected values are an optimistic concurrency guard, not identity/authority.

Governance must deny if the binding/current Draft changed between confirmation display and approval commit.

## Failure behavior

```text
missing __user__.id
→ ACTOR_UNRESOLVED

missing chat/message context
→ REVIEW_CONTEXT_UNRESOLVED

missing/invalid forwarder token
→ TRUSTED_FORWARDER_INVALID

no matching review binding for actor/chat/message
→ REVIEW_CONTEXT_NOT_FOUND

Draft revision/hash changed before approval commit
→ DRAFT_STALE / DRAFT_REVISION_MISMATCH / DRAFT_HASH_MISMATCH

current email.approve grant missing
→ MAILBOX_OPERATION_NOT_AUTHORIZED

user cancels confirmation
→ no SendApproval created
```

No failure path falls back to natural-language approval.

## Stage 4 evolution

ID-5 freezes a Stage 3 approval-only Action.

ID-6 may provide an `Approve & Send` variant that reuses the exact same:

```text
trusted HumanActor
review binding
confirmation preview
approval transaction
```

and then enters the separately governed logical-send/provider transaction.

Do not bypass Stage 3 semantics merely to reduce one UI click.

## Acceptance

A future authorized target must prove:

```text
[ ] Action is visible only where intended
[ ] Action receives the currently authenticated Open WebUI user
[ ] current group membership is resolved server-side
[ ] Action selects review subject by actor/chat/message binding, not chat text
[ ] confirmation dialog displays exact persisted Draft fields
[ ] cancel creates no SendApproval
[ ] confirm creates exact SendApproval
[ ] edit/new revision between display and commit causes stale/deny
[ ] forged draft id/hash in model text has no effect
[ ] removed email.approve permission blocks approval
[ ] no provider email is sent by Stage 3 Action
[ ] forwarder credential does not leak
```

Result when applicable runtime acceptance passes:

```text
PASS — DETERMINISTIC HUMAN APPROVAL ACTION
```
