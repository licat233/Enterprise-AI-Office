# Enterprise AI Office v2 — Installation Design Blueprint

Status: installation design active / real deployment not authorized
Version: 2.0
Date: 2026-09-06

This document is the primary working blueprint for the Enterprise AI Office v2 `installation_design` phase.

It translates the frozen v2 System Design into an agent-readable and eventually agent-executable installation/acceptance contract.

It does **not** authorize a real company installation, real mailbox credentials, real employee binding, SMTP/API sending, or mutation of any ARMOR host.

Authoritative design inputs:

- `state/PROJECT-PHASE.yaml`
- `docs/V2-SCOPE.md`
- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-COMMUNICATION-FOLLOWUP-DESIGN.md`
- `docs/V2-DESIGN-REVIEW.md`
- `docs/ONTOLOGY.md`
- `ontology/examples/email-communication.yaml`
- `config/company.example.yaml`
- `config/capabilities.yaml`

---

## 1. Installation Design objective

Installation Design must make it possible for a fresh capable AI Engineering Agent to answer and execute, on an explicitly authorized future target:

```text
what must already exist
what must be installed
what must be configured
which company-private values are required
which values are secrets
where those values enter the system
which upstream component or thin adapter owns each function
what order installation must follow
what can be retried safely
what requires reconciliation
how each stage is accepted
how each stage is removed or rolled back
how readiness is recorded
```

The design must remain reusable across adopting companies. Public repository examples use synthetic identifiers only.

---

## 2. Frozen runtime boundary

Installation Design may choose implementation mechanisms, but it must preserve the frozen System Design responsibilities:

```text
Company/Product/SOP knowledge          → WeKnora
Employee Web identity/access           → Open WebUI / trusted identity layer
Agent role/capability                  → Hermes Profile
Mailbox/messages/provider send result  → Email Provider
DraftReply / SendApproval governance   → EAO governance implementation
Simple scheduled reminder state        → Hermes Cron
Persistent multi-step Agent work       → Hermes Kanban only when justified
```

Do not create a mailbox mirror, CRM, second scheduler, new graph runtime, or broad generic email automation layer.

---

## 3. Installation Design work packages

The phase is complete only when the following installation contracts are closed.

### ID-1 — Installation architecture and v1 preservation boundary

Define:

```text
host/runtime topology
existing v1 components that must remain unchanged
new v2 runtime boundaries
network/process boundaries
persistent-state locations/classes
component startup/recovery ownership
```

Exit evidence:

```text
INSTALLATION ARCHITECTURE FROZEN
```

### ID-2 — Company configuration and protected-input contract

Define:

```text
public reusable configuration schema
company-private non-secret overlay
secret classes and injection points
required vs optional values
validation/fail-closed behavior
synthetic examples
```

Real secret values never belong in the public repository.

Exit evidence:

```text
CONFIG / SECRET INPUT CONTRACT FROZEN
```

### ID-3 — Capability sequencing and closure

Turn the Stage 0–6 rollout below into explicit per-stage:

```text
preconditions
provisioning steps
configuration inputs
idempotency expectations
acceptance tests
evidence records
rollback/removal path
```

Exit evidence:

```text
STAGE CONTRACTS FROZEN
```

### ID-4 — Trusted identity and mailbox authorization propagation

Define how an installed system carries trusted HumanActor identity and mailbox-scoped permissions from the employee surface to governed reads/actions without confusing them with Hermes Profile or provider credentials.

The exact upstream mechanism must be selected using the pinned/current supported Open WebUI/Hermes capabilities at implementation time.

Exit evidence:

```text
IDENTITY / AUTHORIZATION INSTALLATION CONTRACT FROZEN
```

### ID-5 — Draft / Approval governance persistence and action gate

Define the smallest runtime mechanism that can deterministically persist and enforce:

```text
DraftReply revision/hash
SendApproval exact binding
approval lifecycle
single logical send claim
current permission re-check
append-oriented governance evidence
```

Prefer an existing supported component or thin module over a new standalone platform.

Exit evidence:

```text
GOVERNANCE RUNTIME CONTRACT FROZEN
```

### ID-6 — Provider send binding and reconciliation

Define:

```text
provider transport binding
sender-mailbox restriction
fully resolved approved payload contract
idempotency/logical-send identity
provider-result mapping
ambiguous-outcome reconciliation
controlled retry rules
```

No generic send-anything primitive may be exposed to ordinary Agent tools.

Exit evidence:

```text
GOVERNED SEND / RECONCILIATION CONTRACT FROZEN
```

### ID-7 — Rollback, recovery, clean-host installation, acceptance

Define:

```text
stage disable/removal
credential revocation/removal
persistent-state backup/restore where required
startup/recovery behavior
clean-host installation sequence
acceptance evidence
capability closure
readiness reporting
```

Exit evidence:

```text
INSTALLATION ACCEPTANCE CONTRACT FROZEN
```

---

## 4. Stage 0 — Preserve the v1 baseline

Before adding email capability, a future installer must verify that the existing v1 employee path is healthy.

Required evidence:

```text
Open WebUI employee access works
Hermes general/Profile boundary remains healthy
WeKnora grounded retrieval works
existing RBAC remains fail-closed
current deployment state/backup is known
```

No v2 stage should silently redesign unrelated v1 components.

Exit condition:

```text
V1 BASELINE VERIFIED
```

---

## 5. Stage 1 — Read-only email capability

Objective:

> Let an authorized HumanActor search/read bounded email context without changing provider state.

Required operation surface:

```text
search_email
get_email
```

Must not expose:

```text
send
move
delete
flag mutation
folder mutation
arbitrary protocol command
```

Installation contract must resolve:

```text
selected provider/mailbox configuration
mailbox-specific protected credential class
trusted HumanActor propagation
mailbox-scoped read authorization
Hermes Profile capability binding
allowed folder scope
safe result/body limits
attachment policy
adapter/tool registration
```

Acceptance emphasis:

```text
authorized read succeeds
unauthorized human fails
unauthorized Profile fails
out-of-scope mailbox/folder fails closed
read does not mutate Seen/flags where verifiable
credentials stay outside prompts/logs/Git
```

Exit condition:

```text
READ-ONLY EMAIL PASS
```

---

## 6. Stage 2 — Draft preparation

Objective:

> Use authorized EmailMessage context plus WeKnora evidence to prepare a reviewable DraftReply with no provider-side send effect.

Installation contract must define:

```text
prepare_reply_draft binding
DraftReply persistence
revision generation
stable content_hash calculation
creator HumanActor reference
source message/mailbox reference
human-readable outbound preview path
backup/recovery requirement for draft governance state
```

Exit condition:

```text
DRAFT PREPARATION PASS
```

---

## 7. Stage 3 — Trusted human approval evidence

Objective:

> Deterministically record that an authorized HumanActor approved one exact DraftReply revision/hash.

Installation contract must define:

```text
approve_reply_draft binding
trusted identity propagation
email.approve mailbox scope evaluation
SendApproval persistence
stale/revoked/consumed semantics
exact approval-subject binding
append-oriented evidence
```

Natural-language inference is never approval evidence.

Exit condition:

```text
APPROVAL GATE PASS
```

No customer-facing send capability may be enabled before this stage passes.

---

## 8. Stage 4 — Governed send action

Objective:

> Execute only the exact approved reply through one narrow provider binding.

Installation contract must define:

```text
send_approved_reply action gate
current HumanActor permission re-check
Hermes Profile capability re-check
sender mailbox authorization
approval claim / logical send identity
provider transport binding
provider result/reference capture
audit decision record
ambiguous-outcome reconciliation
```

The provider adapter receives a fully resolved approved payload. It does not reason about whether sending is allowed.

Send outcomes normalize to:

```text
SENT
FAILED_NOT_SENT
RECONCILIATION_REQUIRED
```

Exit condition:

```text
GOVERNED EMAIL LOOP PASS
```

Stages 0–4 form the v2 core.

---

## 9. Stage 5 — Simple follow-up assistance

Optional controlled extension.

Default upstream authority:

```text
Hermes Cron
```

Installation design may enable examples such as:

```text
internal follow-up reminder
morning communication review summary
weekly pending-communication summary
```

Cron state must not become email/CRM state and must not bypass `send_approved_reply`.

Exit condition when enabled:

```text
SIMPLE FOLLOW-UP PASS
```

---

## 10. Stage 6 — Optional messaging surface

Optional controlled extension.

Enable at most one company-selected Hermes-supported messaging surface.

It may provide:

```text
employee entry signal
trusted identity signal when proven
Profile routing
notification/reminder delivery
```

It must not own email authorization, approval policy, provider credentials, or duplicate workflow state.

If channel identity cannot support trusted approval, approval routes back to the trusted employee surface.

Exit condition when enabled:

```text
ONE MESSAGING SURFACE PASS
```

---

## 11. Kanban activation gate

Kanban is not a default installation stage.

Enable only when a real configured workflow requires durable multi-step Agent coordination that Cron or an interactive session cannot satisfy.

If the requirement is only a reminder:

```text
KANBAN: NOT NOW
```

---

## 12. Existing reusable installation assets

Installation Design starts from existing repository capabilities rather than a blank implementation:

```text
v1 provisioning:
  infrastructure/weknora/
  infrastructure/hermes/
  infrastructure/open-webui/

configuration/capability intent:
  config/company.example.yaml
  config/capabilities.yaml

email Stage 1 candidate:
  infrastructure/email/tencent-exmail/imap_readonly_mcp.py
  infrastructure/email/tencent-exmail/imap.env.example
  infrastructure/email/tencent-exmail/hermes.mcp.example.yaml
  infrastructure/email/tencent-exmail/test_imap_readonly.py
  docs/acceptance/TENCENT-EXMAIL.md

existing production controls:
  scripts/preflight.sh
  scripts/health-check.sh
  scripts/backup.sh
  scripts/restore.sh
```

These are candidates and reusable assets, not proof that Installation Design is complete.

Upstream-supported alternatives must be re-evaluated before freezing a custom adapter as the final installation path.

---

## 13. Configuration authority model

The future installer should consume three distinct classes of input:

```text
Public blueprint defaults/templates
→ repository

Company-private non-secret desired state
→ private company configuration overlay

Secrets / credentials
→ protected external secret input at install/runtime
```

Do not merge these classes into one `.env` or one committed company file.

The public blueprint may define secret **names/classes**, never real values.

---

## 14. Idempotency and reconciliation principle

Installation/provisioning operations should be repeatable where practical:

```text
inspect actual state
compare desired state
create/update only what is required
preserve stable identifiers where needed
report drift explicitly
```

External email send is different: it is a business side effect and must not be treated as a generic retryable provisioning operation.

Ambiguous send outcome:

```text
no blind retry
→ RECONCILIATION_REQUIRED
→ inspect provider evidence
→ resolve actual result
```

---

## 15. Rollback/removal principle

Each v2 stage must be removable without corrupting the v1 employee/knowledge path.

At minimum:

```text
email capability can be disabled
mail credentials can be revoked/removed
email tools disappear from affected Profile(s)
EAO governance state can be preserved/exported according to retention policy
Cron jobs can be removed
messaging route can be disabled
v1 Open WebUI → Hermes → WeKnora remains functional
```

Externally sent email cannot be rolled back.

---

## 16. Installation Design evidence and status

Installation Design work produces repository artifacts, tests, fixtures, and contracts.

It must not write target-specific success into the public blueprint as though a company deployment occurred.

Blueprint phase authority:

```text
state/PROJECT-PHASE.yaml
```

Deployment-specific readiness, when a real deployment task later exists, belongs to deployment-state records rather than this document.

---

## 17. Installation Design completion gate

Do not declare `INSTALLATION DESIGN COMPLETE` until a fresh AI Engineering Agent can determine from the repository:

```text
[ ] v1 preservation prerequisites
[ ] installation topology/runtime ownership
[ ] company-private configuration schema
[ ] protected secret-input classes
[ ] Stage 0–4 mandatory sequence
[ ] optional Stage 5–6 activation rules
[ ] exact provisioning/adapters or upstream bindings for each mandatory stage
[ ] trusted identity propagation contract
[ ] mailbox authorization enforcement contract
[ ] DraftReply / SendApproval persistence contract
[ ] deterministic approval gate
[ ] governed send binding
[ ] idempotency / reconciliation behavior
[ ] audit evidence storage/reference contract
[ ] rollback/removal/recovery path
[ ] clean-host setup path
[ ] installation-time acceptance and capability-closure evidence
[ ] no real deployment is implied by the blueprint itself
```

After this gate passes, the next lifecycle phase is `blueprint_validation`, and that transition again requires explicit human direction.
