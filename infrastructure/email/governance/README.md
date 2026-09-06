# EAO Email Governance Runtime

Status: Installation Design reference asset / no real deployment authorized

Normative contracts:

```text
docs/V2-GOVERNANCE-RUNTIME.md
docs/V2-SEND-RECONCILIATION.md
```

Reference persistence artifacts:

```text
schema.sql
migrations/002_send_reconciliation.sql
```

Offline deterministic contract checks:

```sh
python3 infrastructure/email/governance/test_schema.py
python3 infrastructure/email/governance/test_send_reconciliation.py
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
→ inspect unresolved send attempts
→ become ready
```

Unknown/newer schema version, failed migration, missing trusted-forwarder authentication, or invalid mailbox policy means fail-closed readiness.

Any durable send attempt without a terminal result is treated as reconciliation-required; startup must never auto-retry it.

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
  initialize logical send
  create durable provider attempt
  submit through narrow provider adapter
  persist SENT / CONFIRMED_NOT_SENT / OUTCOME_UNKNOWN
  protected reconciliation control path
```

Formal approval and reconciliation are never free-choice LLM tools.

## Database ownership

Only the governance service writes the governance SQLite database.

Do not give Open WebUI, Hermes, an employee browser, or a provider adapter direct SQLite access.

Do not turn this database into a mailbox cache or CRM.

## ID-5 offline schema contract

`test_schema.py` intentionally uses only Python stdlib and in-memory SQLite. It validates the repository-level Draft/Approval contract without provider credentials or a real target:

```text
canonical Draft hash is deterministic
immutable revisions coexist
review binding references exact Draft revision/hash
exact duplicate approval is constrained
one Approval cannot be claimed twice
append-oriented audit table accepts governance evidence
foreign keys are enabled in the test connection
```

## ID-6 offline schema contract

`test_send_reconciliation.py` applies the initial schema plus migration 002 and validates:

```text
schema advances to version 2
logical send must match the committed ApprovalClaim
stable Message-ID / transport hash evidence can persist
attempt numbers are unique per logical send
attempt-without-result is detectable as unresolved
OUTCOME_UNKNOWN observation remains intact after reconciliation
reconciliation evidence appends rather than rewrites provider observation
```

Provider outcome classification is separately checked by:

```sh
python3 infrastructure/email/tencent-exmail/test_smtp_send_adapter.py
```

Passing these offline checks is blueprint/implementation evidence only. It does not prove live HumanActor propagation, mailbox authorization, provider acceptance, or real delivery.

## ID-6 invariant

The Stage 4 implementation must preserve:

```text
one SendApproval
→ one logical send claim
→ stable Message-ID / Date / transport payload hash
→ one or more provider attempts only when state permits
```

Outcome rules:

```text
SENT
→ no retry

CONFIRMED_NOT_SENT
→ same logical send may perform a controlled retry if all invariants still hold

OUTCOME_UNKNOWN / unresolved attempt
→ RECONCILIATION_REQUIRED
→ no blind retry
```

Provider side effect happens only after durable ApprovalClaim/logical-send initialization and durable attempt creation.

## Reconciliation boundary

Reconciliation is a protected operator/governance control-plane action. It is not an ordinary employee tool and not model authority.

Possible evidence sources are provider/runtime specific and must be validated before being trusted. Do not assume SMTP automatically saves a copy in Sent.

Allowed recorded reconciliation conclusions are:

```text
SENT
CONFIRMED_NOT_SENT
REMAINS_UNKNOWN
```

`REMAINS_UNKNOWN` stays blocked from retry.
