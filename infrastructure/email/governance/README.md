# EAO Email Governance Runtime

Status: Installation Design reference asset / no real deployment authorized

Normative contract:

```text
docs/V2-GOVERNANCE-RUNTIME.md
```

Reference persistence schema:

```text
schema.sql
```

Offline deterministic contract check:

```sh
python3 infrastructure/email/governance/test_schema.py
```

This runtime is the single thin EAO-owned service introduced by v2. It must remain independent of the validated v1 `general` employee path.

## Reference install shape

```text
<runtime_root>/runtime/email-governance/state.sqlite3
<runtime_root>/logs/email-governance/
```

The service is host-native in the first macOS/arm64 reference topology unless later validation proves another placement materially simpler.

## Startup order

```text
load validated company/private config
→ resolve protected trusted-forwarder secret
→ open local SQLite database
→ enable foreign keys / WAL / synchronous policy / busy timeout
→ verify or migrate schema
→ load mailbox authorization policy from ID-4 inputs
→ bind only Stage-enabled operation surfaces
→ become ready
```

Unknown/newer schema version, failed migration, missing trusted-forwarder authentication, or invalid mailbox policy means fail-closed readiness.

## Stage surface

```text
Stage 1
  search_email
  get_email

Stage 2
  prepare_reply_draft

Stage 3
  trusted server-side approve_reply_draft action
  optional revoke_reply_approval

Stage 4
  claim_approval_for_send
  governed provider send binding added by ID-6
```

Formal approval is never a free-choice LLM tool.

## Database ownership

Only the governance service writes the governance SQLite database.

Do not give Open WebUI, Hermes, an employee browser, or a provider adapter direct SQLite access.

Do not turn this database into a mailbox cache or CRM.

## Offline schema contract

`test_schema.py` intentionally uses only Python stdlib and in-memory SQLite. It validates the repository-level contract without provider credentials or a real target:

```text
canonical Draft hash is deterministic
immutable revisions coexist
exact duplicate approval is constrained
one Approval cannot be claimed twice
append-oriented audit table accepts governance evidence
foreign keys are enabled in the test connection
```

Passing this test is blueprint/implementation evidence only. It does not prove a live runtime, HumanActor propagation, mailbox authorization, or provider behavior.

## ID-6 boundary

Do not add SMTP/provider retries or reconciliation semantics to the Stage 2/3 implementation merely because the schema has an approval claim primitive.

ID-6 owns:

```text
logical send execution/provider attempts
provider result normalization
confirmed-not-sent retry
ambiguous outcome handling
reconciliation
```

The ID-5 invariant that ID-6 must preserve is:

```text
one SendApproval
→ one logical send claim
→ provider side effect only after claim
```
