# Enterprise AI Office v2 — Stage & Capability Closure Contracts

Status: stage contracts frozen / real deployment not authorized
Version: 1.0
Date: 2026-09-06

This document closes `ID-3 — Capability sequencing and closure` for the Enterprise AI Office v2 `installation_design` phase.

It converts the Stage 0–6 rollout into deterministic installation/acceptance gates for a future capable AI Engineering Agent.

It does **not** authorize execution against a real company host, mailbox, employee identity, or recipient. Runtime execution requires an explicitly authorized validation/deployment target and the applicable protected inputs.

Use with:

- `state/PROJECT-PHASE.yaml`
- `docs/V2-IMPLEMENTATION-PLAN.md`
- `docs/V2-INSTALLATION-ARCHITECTURE.md`
- `docs/V2-CONFIG-PROTECTED-INPUTS.md`
- `config/company.example.yaml`
- `config/company.private.example.yaml`
- `config/capabilities.yaml`
- `docs/ACCEPTANCE-TESTS.md`
- `docs/acceptance/TENCENT-EXMAIL.md`

---

## 1. Stage model

A Stage is an **installation/capability closure gate**, not a runtime workflow object and not a workflow engine.

Each Stage has exactly these contract classes:

```text
preconditions
required inputs
provisioning / activation
idempotency boundary
acceptance
required evidence
rollback / removal
result
```

The runtime system does not persist `Stage` business objects merely because this installation blueprint uses stages.

---

## 2. Sequence and dependency rules

Core sequence:

```text
Stage 0  V1 BASELINE VERIFIED
   ↓
Stage 1  READ-ONLY EMAIL PASS
   ↓
Stage 2  DRAFT PREPARATION PASS
   ↓
Stage 3  APPROVAL GATE PASS
   ↓
Stage 4  GOVERNED EMAIL LOOP PASS
```

Stages 0–4 form the mandatory v2 Communication & Follow-up core when the email capability is enabled.

Optional extensions:

```text
Stage 5  SIMPLE FOLLOW-UP PASS
Stage 6  ONE MESSAGING SURFACE PASS
```

Stage 5 and Stage 6 are evaluated only when the active company configuration explicitly enables the corresponding capability.

Rules:

```text
A later mandatory Stage must not PASS while an earlier mandatory Stage is not PASS.
A blocked Stage blocks later dependent Stages.
A failed Stage blocks later dependent Stages until corrected and re-accepted.
An optional disabled Stage is NOT REQUESTED, not FAIL and not deployment debt.
Stage completion is evidence about one target; it does not mutate blueprint lifecycle state.
```

---

## 3. Common result vocabulary

Every applicable Stage closes with exactly one of:

```text
PASS — <stage milestone>
BLOCKED — REQUIRED INPUT: <specific input or authority>
FAIL — <specific implementation/security/acceptance boundary>
```

Optional disabled stages close as:

```text
NOT REQUESTED — capability disabled by company configuration
```

Do not convert a required capability to disabled merely to get a green result.

A missing real credential is not a blueprint-development blocker. It becomes `BLOCKED — REQUIRED INPUT` only when an explicitly authorized validation/deployment target is actually executing a Stage that requires that credential.

---

## 4. Common provisioning discipline

Provisioning/activation work should be convergent and repeatable where practical:

```text
inspect actual state
→ compare with desired state
→ create/update only what is required
→ preserve stable identifiers/state where applicable
→ run acceptance
→ record observed evidence
```

Ordinary installation retry must not duplicate runtime resources merely because a previous run partially succeeded.

Business side effects are different:

```text
creating a draft
creating an approval
sending email
```

These operations follow their own governance/idempotency contracts and must never be blindly replayed as generic installer steps.

---

# Stage 0 — Preserve / verify v1 baseline

## Objective

Prove that the existing v1 employee knowledge path is healthy before v2 email dependencies are activated.

### Preconditions

```text
explicit authorized target exists when Stage 0 is actually executed
active target/company configuration is known
requested readiness is known
host/runtime actual state has been inspected
```

For an existing deployment, inspect before mutation.

For a clean host, provision the validated v1 core through the existing Golden Path before claiming Stage 0 PASS.

### Required inputs

```text
host/runtime target
active company configuration
selected/pinned core stack or approved upgrade choice
core model/provider inputs required by v1
core protected secrets required by v1
```

### Provisioning / activation

Stage 0 adds no v2 email capability.

Required behavior:

```text
verify/provision WeKnora baseline
verify/provision Hermes `general`
verify/provision Open WebUI employee path
verify employee RBAC
verify WeKnora grounded retrieval
capture current backup/deployment-state boundary where applicable
```

### Idempotency

Safe to rerun.

Re-running Stage 0 must inspect and verify the same v1 desired state rather than creating duplicate Profiles, Assistants, groups, Knowledge Bases, or credentials without cause.

### Acceptance

Use `docs/ACCEPTANCE-TESTS.md` Part A — Core Ready.

Minimum v2-preservation assertions:

```text
General Assistant works
Hermes `general` is healthy and least-privileged
WeKnora grounding/source path works
Open WebUI employee authentication/RBAC works
unapproved tools remain absent/fail closed
v2 email dependencies are not required for `general` startup
```

### Required evidence

```text
core component versions/commits
core health result
General Assistant employee-client result
WeKnora grounding result
RBAC/dangerous-tool boundary result
known backup/deployment-state baseline where applicable
Stage 0 result
```

### Rollback / removal

Stage 0 is a verification/core-provisioning gate, not a disposable v2 layer.

If a Stage 0 verification-only run changes nothing, no rollback is required.

If a clean-host core was provisioned, use the existing v1 deployment/recovery contracts rather than v2 email rollback logic.

### Result

```text
PASS — V1 BASELINE VERIFIED
```

---

# Stage 1 — Bounded read-only email

## Objective

Let an authorized HumanActor search/read configured mailbox context without provider-side mailbox mutation.

### Preconditions

```text
Stage 0 PASS
email capability enabled in active company configuration
provider selected
communication Profile defined
at least one mailbox defined
mailbox grants include at least one email.read grant
allowed read folder scope defined
provider credential symbolic reference defined
```

When actually executed on an authorized target, the referenced provider credential must be resolvable before provider acceptance can run.

### Required inputs

From ID-2 company/private/protected input contracts:

```text
communication Profile ID + employee group mapping
mailbox logical ID/address/business purpose
provider read endpoint mode
allowed folders/read limits
attachment policy
mailbox grants
mailbox credential reference
resolved mailbox credential at runtime
private governance service bind/state/log settings or accepted defaults
```

### Provisioning / activation

```text
provision/enable `eao-email-governance` in read-only mode
initialize governance service runtime directories/state store if required
bind provider read adapter for configured mailbox(es)
provision/enable isolated Hermes communication Profile
expose only `search_email` and `get_email` email operations to that Profile
bind the intended Open WebUI Communication Assistant/resource to authorized users/groups
keep provider send binding disabled
keep approval/send action disabled
```

The validated v1 `general` Profile remains unchanged.

### Idempotency

Provisioning is convergent and repeatable.

Re-running Stage 1 must not:

```text
create duplicate Communication Assistants/Profiles
duplicate mailbox policy grants
mutate mailbox flags/folders/messages
replace stable governance state without migration/backup reason
```

Read operations themselves are repeatable but must remain non-mutating where the provider supports it.

### Acceptance

Use applicable sections of `docs/acceptance/TENCENT-EXMAIL.md` or the selected provider-equivalent acceptance:

```text
provider/mailbox scope
credential boundary
non-mutating read path
knowledge/source boundary
employee-client read authorization
```

Required security behavior:

```text
authorized read succeeds
unauthorized human fails
unauthorized Profile fails
out-of-scope mailbox/folder fails closed
read does not mark Seen or mutate provider state where verifiable
credentials do not appear in prompts/logs/Git/audit
```

### Required evidence

```text
provider + mailbox identifiers, never credentials
communication Profile identifier
mailbox grant summary
allowed folder/read scope
provider endpoint mode
credential symbolic reference/storage-class description, never value
read adapter/unit test result
runtime authorized-read result
runtime unauthorized-read result
non-mutating read result
Stage 1 result
```

### Rollback / removal

```text
disable/remove Communication Assistant access
remove read tools from/stop communication Profile as applicable
stop/disable governance service if no later v2 capability depends on it
revoke/remove mailbox credential from runtime
preserve/remove governance state according to retention/recovery policy
verify v1 General Assistant still passes
```

Rollback must not mutate mailbox contents.

### Result

```text
PASS — READ-ONLY EMAIL PASS
```

---

# Stage 2 — DraftReply preparation

## Objective

Create a reviewable EAO-owned DraftReply from authorized EmailMessage context plus approved company knowledge, with no provider send side effect.

### Preconditions

```text
Stage 1 PASS
governance persistence available
communication Profile can access WeKnora as configured
HumanActor read/draft authorization contract is resolvable
```

### Required inputs

```text
governance SQLite state location
DraftReply retention/backup policy or accepted company default
communication Profile policy/tool mapping
human-readable outbound preview surface
```

No SMTP/send credential is required merely to close Draft preparation.

### Provisioning / activation

```text
initialize/upgrade governance schema for DraftReply state
enable `prepare_reply_draft`
bind source EmailMessage + mailbox references
persist exact outbound DraftReply artifact
create deterministic revision number/version
calculate canonical content_hash
record creator HumanActor reference
present sender/To/Cc/subject/body/source context for review
keep provider send disabled
```

### Idempotency

Installer/schema provisioning is repeatable and migration-aware.

`prepare_reply_draft` is a business operation, not an installer retry primitive. Replaying a failed installer must not create a new business DraftReply.

An intentional human/Agent request for a materially edited draft creates a new revision rather than silently overwriting an approved/reviewed revision.

### Acceptance

```text
authorized source message can produce a DraftReply
unauthorized mailbox/message cannot produce a DraftReply
draft creation causes no provider send side effect
sender/recipients/subject/body/source are human-inspectable
material edit creates a new revision/hash
DraftReply survives governance service restart according to persistence contract
company/product claims use WeKnora evidence when required
```

Use `docs/acceptance/TENCENT-EXMAIL.md` Draft behavior and knowledge/source sections where applicable.

### Required evidence

```text
draft_id
source mailbox/message references
draft revision
content_hash
creator HumanActor reference
persistence/restart test result
no-send-side-effect result
human preview result
Stage 2 result
```

Do not copy credentials into evidence.

### Rollback / removal

```text
disable `prepare_reply_draft`
remove Draft tool exposure from communication Profile
preserve/archive/delete governance Draft state only according to configured retention policy
leave provider mailbox untouched
verify Stage 1 read path and v1 path as intended
```

### Result

```text
PASS — DRAFT PREPARATION PASS
```

---

# Stage 3 — Trusted human approval gate

## Objective

Deterministically record that an authorized HumanActor approved one exact DraftReply revision/hash before any customer-visible send is enabled.

### Preconditions

```text
Stage 2 PASS
trusted HumanActor path selected for the employee surface
mailbox-scoped email.approve grant model available
trusted server-side approval interaction available or implementation path closed
SendApproval persistence available
```

The detailed identity assertion/runtime mechanism is frozen under ID-4; governance persistence mechanics are frozen under ID-5. Stage 3 cannot be runtime-accepted before those contracts are implemented on the target.

### Required inputs

```text
trusted identity source configuration
group/principal mapping inputs
mailbox grants including email.approve
approval UI/action binding
approval policy/version identifiers
```

### Provisioning / activation

```text
enable trusted Open WebUI approval Action/Function or approved equivalent
bind trusted HumanActor identity to governance service call
enable `approve_reply_draft` only through deterministic trusted-human path
persist SendApproval bound to exact draft_id + revision + content_hash
record approved_by_actor_id and approved_at
implement stale/revoked/consumed evaluation contract
keep provider send disabled until Stage 3 acceptance passes
```

Ordinary LLM free-text interpretation must not manufacture formal approval.

### Idempotency

Provisioning is convergent.

Approval creation is a governance business operation. Duplicate delivery of the same trusted approval request must not create multiple independently reusable approvals for the same intended approval interaction.

Material Draft edit after approval invalidates the old approval for the new revision.

### Acceptance

```text
authorized approver can approve exact presented Draft revision/hash
unauthorized actor cannot approve
approval for another mailbox scope fails closed
natural-language-only "send it" cannot create formal approval
material edit makes previous approval invalid/stale for current draft
revoked approval cannot authorize send
approval evidence survives governance service restart
no provider send capability is needed to demonstrate approval gate correctness
```

Use `docs/acceptance/TENCENT-EXMAIL.md` Human approval binding section where applicable.

### Required evidence

```text
approval_id
approved_by_actor_id
draft_id + revision + content_hash
approval timestamp
policy/contract version
stale-edit test result
unauthorized-approval test result
natural-language-not-approval test result
persistence/restart result
Stage 3 result
```

### Rollback / removal

```text
disable trusted approval Action
revoke active approvals where company removal policy requires it
remove approval operation exposure/binding
preserve governance evidence according to retention policy
leave provider send disabled
verify Stage 1/2 and v1 behavior according to desired rollback level
```

### Result

```text
PASS — APPROVAL GATE PASS
```

---

# Stage 4 — Governed send_approved_reply

## Objective

Send only the exact approved DraftReply through the configured sender mailbox after current authorization and approval are revalidated.

### Preconditions

```text
Stage 3 PASS
provider send transport selected
sender mailbox send credential binding available
mailbox grants include required email.send authorization
provider controlled test recipient scope defined
send/reconciliation implementation available
```

No customer-facing send is enabled before Stage 3 PASS.

### Required inputs

```text
sender mailbox/provider send endpoint
mailbox credential symbolic ref + protected runtime value
email.send mailbox grants
controlled test recipients for acceptance
provider result mapping
reconciliation operator/evidence path
```

### Provisioning / activation

```text
enable narrow provider send adapter inside governance service
enable governed `send_approved_reply` action gate
re-check current HumanActor + mailbox + Profile authorization at execution time
re-check exact Draft revision/hash and valid SendApproval
claim approval for one logical send operation before provider side effect
construct fully resolved approved payload inside trusted runtime
restrict From to approved mailbox identity
restrict acceptance send to controlled test recipient scope
capture normalized provider result/reference
record append-oriented governance evidence
```

Do not expose generic SMTP/send-anything primitives to the employee Agent surface.

### Idempotency

Installer provisioning is repeatable.

Email send is **not** generic retryable provisioning.

One Approval authorizes one logical send operation.

Provider attempts inside that logical operation follow ID-6 reconciliation rules:

```text
confirmed SENT
→ no retry

confirmed NOT SENT
→ controlled retry may be allowed for the same immutable logical send

outcome UNKNOWN
→ RECONCILIATION_REQUIRED
→ no blind retry
```

### Acceptance

Use controlled test recipients only until the real deployment/pilot explicitly authorizes broader use.

Use applicable provider acceptance sections:

```text
send path
ambiguous failure / duplicate-send safety
audit
employee-client acceptance
```

Required assertions:

```text
approved exact test message sends successfully
unapproved send fails closed
stale/revoked approval fails closed
actor whose email.send permission was removed cannot send even with old approval
wrong sender mailbox fails closed
provider result/reference captured without secret leakage
ambiguous outcome cannot cause blind duplicate send
v1 General Assistant remains healthy if provider/send path fails
```

### Required evidence

```text
action_execution_id/logical_send_id
requested/approved/executed actor references as applicable
Profile ID
mailbox ID
draft_id + revision + content_hash
approval_id
provider normalized result + provider reference
reconciliation state if any
controlled-recipient acceptance result
negative authorization/stale-approval tests
Stage 4 result
```

### Rollback / removal

```text
disable employee approval/send Action first
disable `send_approved_reply`
remove/revoke send credential binding
keep or downgrade read/draft/approval capability according to desired state
preserve governance evidence according to retention policy
verify no autonomous sender remains
verify v1 General Assistant remains healthy
```

Externally sent email cannot be rolled back.

### Result

```text
PASS — GOVERNED EMAIL LOOP PASS
```

---

# Stage 5 — Optional simple follow-up

## Objective

Add internal reminder/review assistance using Hermes Cron without creating a shadow CRM or bypassing governed send.

### Applicability

Run only when:

```text
capabilities.cron.enabled == true
+
company configuration defines an email/communication follow-up job or policy
```

Otherwise:

```text
NOT REQUESTED — capability disabled by company configuration
```

### Preconditions

```text
Stage 4 PASS for workflows that follow sent email
Hermes Cron capability enabled and accepted
owner Profile and timezone defined
follow-up job behavior defined
```

A reminder-only use case does not justify Kanban.

### Required inputs

```text
Cron owner Profile
schedule/timezone
internal delivery target
business purpose
email/thread reference policy
```

### Provisioning / activation

```text
create only configured reminder/review Cron jobs
reference existing email context/logical identifiers without copying mailbox state into Cron
keep all customer-visible send paths behind normal Draft → Approval → send_approved_reply
```

### Idempotency

Provisioning must converge on the configured Cron job identity rather than duplicate jobs on rerun.

Reminder execution may repeat only according to the configured schedule; it must not duplicate customer-visible sends.

### Acceptance

Use `docs/ACCEPTANCE-TESTS.md` Cron section plus applicable email follow-up checks:

```text
job executes at intended schedule/timezone
expected internal reminder/summary delivered
run state/history available
pause/resume works
restart persistence works
scheduled task cannot bypass approval/send gate
disabling email capability leaves no autonomous customer sender
```

### Required evidence

```text
Cron job ID/name
owner Profile
schedule/timezone
delivery target
acceptance result
email-governance boundary result
Stage 5 result
```

### Rollback / removal

```text
pause/delete configured communication Cron jobs
verify no customer-facing send path remains
leave Stage 0–4 state untouched unless separately requested
```

### Result

```text
PASS — SIMPLE FOLLOW-UP PASS
```

---

# Stage 6 — Optional one messaging surface

## Objective

Expose at most one selected employee messaging entry/notification surface without moving email governance authority into the messaging platform.

### Applicability

Run only when:

```text
capabilities.messaging.enabled == true
```

Otherwise:

```text
NOT REQUESTED — capability disabled by company configuration
```

### Preconditions

```text
selected Hermes-supported messaging platform defined
messaging credentials available on authorized target
authorized user/chat or trusted identity policy defined
Profile routing defined
Stage 0 PASS
```

If messaging participates in the email workflow, Stage 1–4 must already be accepted to the level required by that route.

### Required inputs

```text
selected platform
platform credential symbolic refs + protected values
authorized users/chats or enterprise identity mapping
Profile route
notification policy
trusted approval capability decision for that channel
```

### Provisioning / activation

```text
enable one selected Hermes Gateway messaging route
route only to intended Profile(s)
keep default/admin unavailable to ordinary messaging users
use messaging only for entry/notification/approved employee interaction
route formal approval back to trusted Open WebUI surface unless channel identity + deterministic approval mechanism has separately passed the same ID-4/ID-5 trust contract
```

### Idempotency

Gateway/channel provisioning must converge on configured routes and must not create duplicate bots/routes/jobs on rerun.

### Acceptance

Use `docs/ACCEPTANCE-TESTS.md` Messaging section:

```text
authorized user/chat can invoke intended Profile
unauthorized identity fails closed
routing is deterministic
default/admin unavailable
credentials absent from Git/logs
configured notification works
messaging does not become Source of Truth for Draft/Approval/send state
channel cannot bypass governed send
```

### Required evidence

```text
platform
route/Profile mapping
authorization method
credential storage-class description, never value
notification result
negative authorization result
approval-boundary decision/result
Stage 6 result
```

### Rollback / removal

```text
disable/remove messaging route
revoke/remove platform credentials
remove temporary acceptance objects
leave Open WebUI + v1/v2 core paths intact
```

### Result

```text
PASS — ONE MESSAGING SURFACE PASS
```

---

## 11. Kanban remains outside Stage 0–6 by default

Kanban is enabled only when the active company configuration contains a real durable multi-step Agent workflow that cannot be handled by an interactive session or Cron.

```text
reminder only
→ Cron
→ KANBAN: NOT NOW
```

A future Kanban-enabled communication workflow must receive its own capability closure; the existence of v2 email does not imply it.

---

## 12. Capability closure table

For an enabled v2 email deployment, the installer records at least:

| Stage | Capability | Required? | Exit milestone |
| --- | --- | --- | --- |
| 0 | v1 core employee path | yes | `V1 BASELINE VERIFIED` |
| 1 | bounded email read | yes | `READ-ONLY EMAIL PASS` |
| 2 | DraftReply preparation | yes | `DRAFT PREPARATION PASS` |
| 3 | trusted human approval | yes | `APPROVAL GATE PASS` |
| 4 | governed send | yes | `GOVERNED EMAIL LOOP PASS` |
| 5 | simple follow-up / Cron | config-dependent | `SIMPLE FOLLOW-UP PASS` or `NOT REQUESTED` |
| 6 | messaging surface | config-dependent | `ONE MESSAGING SURFACE PASS` or `NOT REQUESTED` |

`CONFIGURED READY` may be recorded only when:

```text
Stage 0–4 PASS for enabled v2 email
+
every other company-enabled conditional capability PASS
+
Stage 5/6 PASS when those capabilities are enabled
+
actual state/evidence recorded
```

A Stage result does not override the broader readiness rules in `docs/COMPLETENESS.md` / `docs/ACCEPTANCE-TESTS.md`.

---

## 13. Stage rollback dependency rule

Removal proceeds in reverse dependency order.

Full v2 email removal:

```text
Stage 6 messaging route, if enabled
→ Stage 5 communication Cron jobs, if enabled
→ Stage 4 governed send binding
→ Stage 3 approval Action/binding
→ Stage 2 Draft operation exposure
→ Stage 1 read integration / communication Profile
→ verify Stage 0 v1 baseline remains healthy
```

Partial downgrade is allowed when desired state explicitly requests it, for example:

```text
Stage 4 removed
→ keep Stage 1–3 read/draft/approval capability if desired
```

Do not destroy governance evidence merely because a capability is disabled; retention/removal behavior follows ID-7.

---

## 14. Stage execution record boundary

The public blueprint records **what evidence is required**, not target-specific PASS claims.

When a real/validation target is explicitly authorized, observed Stage results belong in that target's deployment/validation state record.

Recommended stage evidence shape:

```text
stage_id
requested
preconditions_result
implementation/version or adapter reference
configuration fingerprint/reference (no secrets)
acceptance_result
evidence references
final_result
timestamp
```

Do not place secrets, real mailbox passwords, bearer tokens, or unnecessary full message bodies in stage evidence.

---

## 15. ID-3 acceptance contract

ID-3 is complete when the blueprint establishes:

```text
[✓] Stage 0–4 mandatory dependency order
[✓] Stage 5/6 config-dependent activation
[✓] one common PASS/BLOCKED/FAIL vocabulary
[✓] preconditions for every Stage
[✓] required input classes for every Stage
[✓] provisioning/activation boundary for every Stage
[✓] idempotency/retry boundary for every Stage
[✓] acceptance mapping for every Stage
[✓] evidence requirements for every Stage
[✓] rollback/removal path for every Stage
[✓] Configured Ready closure relationship
[✓] no Stage requires a workflow-engine runtime object
[✓] no real deployment is implied by the blueprint
```

Result:

```text
ID-3: PASS
STAGE CONTRACTS FROZEN
```
