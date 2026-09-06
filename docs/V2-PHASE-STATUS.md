# Enterprise AI Office v2 — Blueprint Status

Status: installation design complete / transition-ready / real deployment task inactive
Version: 4.0.0
Date: 2026-09-07

The authoritative machine-readable repository state is:

```text
state/PROJECT-PHASE.yaml
```

If this document conflicts with `state/PROJECT-PHASE.yaml`, the machine-readable file wins until an explicit human-directed lifecycle update changes both.

## 1. Current blueprint state

```text
RELEASE TRACK: v2
BLUEPRINT PHASE: INSTALLATION DESIGN
SYSTEM DESIGN: COMPLETE
INSTALLATION DESIGN: COMPLETE
INSTALLATION DESIGN FINAL REVIEW: PASS
ID-1 INSTALLATION ARCHITECTURE: COMPLETE
ID-2 CONFIG / PROTECTED INPUTS: COMPLETE
ID-3 STAGE / CAPABILITY CLOSURE: COMPLETE
ID-4 TRUSTED IDENTITY / MAILBOX AUTHORIZATION: COMPLETE
ID-5 DRAFT / APPROVAL GOVERNANCE RUNTIME: COMPLETE
ID-6 GOVERNED SEND / RECONCILIATION: COMPLETE
ID-7 RECOVERY / CLEAN-HOST ACCEPTANCE: COMPLETE
NEXT LIFECYCLE PHASE: BLUEPRINT VALIDATION — NOT YET OPENED
REAL DEPLOYMENT TASK: INACTIVE
```

The human explicitly advanced the blueprint lifecycle to `installation_design` on 2026-09-06. Installation Design completed on 2026-09-07.

`current_phase` intentionally remains `installation_design`. Opening `blueprint_validation` requires a separate explicit human direction; Installation Design completion itself does not change phase and does not authorize any real company deployment.

---

## 2. Frozen System Design input

The v2 System Design baseline remains frozen and authoritative.

Core operational loop:

```text
Trusted HumanActor
↓
Open WebUI
↓
Hermes Profile
↓
authorized Email context + WeKnora knowledge
↓
DraftReply
↓
exact human review
↓
SendApproval
↓
send_approved_reply
↓
provider result / reconciliation
↓
governance audit
↓
optional internal follow-up
```

Core Email Ontology remains:

```text
Mailbox
EmailMessage
DraftReply
SendApproval
```

Governance/runtime execution evidence does not add new Email business objects.

---

## 3. Installation Design completion

```text
ID-1  Installation architecture + v1 preservation     COMPLETE
ID-2  Company configuration + protected inputs        COMPLETE
ID-3  Stage sequencing + capability closure           COMPLETE
ID-4  Trusted identity + mailbox authorization        COMPLETE
ID-5  Draft / Approval governance runtime             COMPLETE
ID-6  Governed send + reconciliation                  COMPLETE
ID-7  Rollback / recovery / clean-host acceptance     COMPLETE
```

Frozen contracts:

```text
ID-1 → docs/V2-INSTALLATION-ARCHITECTURE.md
       INSTALLATION ARCHITECTURE FROZEN

ID-2 → docs/V2-CONFIG-PROTECTED-INPUTS.md
       CONFIG / SECRET INPUT CONTRACT FROZEN

ID-3 → docs/V2-STAGE-CONTRACTS.md
       STAGE CONTRACTS FROZEN

ID-4 → docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md
       infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md
       IDENTITY / AUTHORIZATION INSTALLATION CONTRACT FROZEN

ID-5 → docs/V2-GOVERNANCE-RUNTIME.md
       infrastructure/email/governance/schema.sql
       infrastructure/open-webui/V2-APPROVAL-ACTION.md
       infrastructure/open-webui/v2_approve_draft_action.py
       GOVERNANCE RUNTIME CONTRACT FROZEN

ID-6 → docs/V2-SEND-RECONCILIATION.md
       infrastructure/email/governance/migrations/002_send_reconciliation.sql
       infrastructure/email/tencent-exmail/smtp_send_adapter.py
       SEND / RECONCILIATION INSTALLATION CONTRACT FROZEN

ID-7 → docs/V2-RECOVERY-CLEAN-HOST.md
       infrastructure/email/governance/backup_state.py
       infrastructure/email/governance/restore_state.py
       infrastructure/email/governance/test_recovery.py
       scripts/backup.sh
       scripts/restore.sh
       RECOVERY / CLEAN-HOST INSTALLATION CONTRACT FROZEN
```

Final review:

```text
docs/V2-INSTALLATION-DESIGN-REVIEW.md
INSTALLATION DESIGN FINAL REVIEW: PASS
```

---

## 4. Reference v2 runtime topology

The validated v1 General path remains independent:

```text
Employee
→ Open WebUI General Assistant
→ Hermes general Profile
→ WeKnora
```

The v2 Communication path is isolated:

```text
Employee
→ authenticated Open WebUI session
→ Communication Assistant
├─ Hermes communication Profile for reasoning
└─ Open WebUI server-side governed Email tool/action path
   → eao-email-governance
   → Tencent provider adapter
```

The v2 reference introduces only one thin EAO-owned runtime:

```text
eao-email-governance
```

Reference persistence:

```text
SQLite
<runtime_root>/runtime/email-governance/state.sqlite3
```

No CRM, workflow engine, queue, new IAM platform, or database server is introduced for the baseline.

---

## 5. Deterministic authority path

A governed send requires the intersection of:

```text
trusted HumanActor
current mailbox-scoped email.send permission
Communication capability context
exact DraftReply revision/hash
explicit SendApproval
committed single-use ApprovalClaim
fully frozen logical-send payload
```

The following do not constitute send authority:

```text
LLM natural-language inference
Hermes Profile capability alone
provider credential alone
mailbox address
browser/model-supplied actor/group fields
Message-ID alone
retry after timeout
```

Formal approval is performed through the deterministic server-side Open WebUI Action path and exact persisted Draft review binding.

---

## 6. Governed send / reconciliation

Every logical send freezes:

```text
logical_send_id
Approval/Draft revision/hash
sender + recipient set
stable RFC Message-ID
stable Date header
transport_payload_hash
```

Normalized provider outcomes are exactly:

```text
SENT
CONFIRMED_NOT_SENT
OUTCOME_UNKNOWN
```

Safety behavior:

```text
SENT
→ no retry

CONFIRMED_NOT_SENT
→ controlled retry may occur only inside the same logical_send_id after revalidation

OUTCOME_UNKNOWN
or durable SendAttempt without terminal result
→ RECONCILIATION_REQUIRED
→ no blind retry
```

All intended SMTP recipients must be accepted before DATA in the baseline; partial-recipient delivery is intentionally avoided.

---

## 7. Recovery / rollback / clean-host closure

ID-7 freezes:

```text
SQLite-native Governance backup
isolated restore into a new target
schema/integrity/foreign-key validation
unknown-newer-schema fail closed
unresolved-send preservation after restore
startup recovery without automatic resend
pre-migration backup + restore-based rollback boundary
Stage 4 → Stage 1 capability degradation/removal
v1 preservation after v2 failure/rollback
installer second-run convergence without business side effects
clean-host install sequence
failure-injection matrix
deployment-state evidence requirements
```

The full-stack backup/restore helpers now include Governance state only when v2 Email is actually enabled. A v1-only deployment remains valid when Governance state is absent.

Restoring a database can never manufacture `CONFIRMED_NOT_SENT` or an automatic retry from uncertainty.

---

## 8. Stage / capability closure

Core dependency chain remains:

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

Stage 5/6 remain conditional on configured Cron/follow-up and Messaging respectively.

A Stage is an installation/capability closure gate, not a runtime workflow engine.

---

## 9. Validation truth

Installation Design is complete because the repository now defines how a future capable AI Engineering Agent should install, reconcile, recover, roll back, and accept the design.

It does **not** mean the clean-host validation has run.

Repository-defined deterministic test assets include:

```text
Governance schema/hash/review-binding
send/reconciliation schema
Governance backup/restore/recovery
read-only IMAP adapter
SMTP outcome classifier
repository readiness
```

Actual execution evidence belongs to `blueprint_validation` or an explicitly authorized deployment target.

---

## 10. Explicit boundary: not a real deployment

```text
REAL COMPANY DEPLOYMENT: NOT ACTIVE
REAL DEPLOYMENT TASK: INACTIVE
REAL PROVIDER CREDENTIALS: NOT REQUIRED
REAL MAILBOX ACCESS: NOT REQUIRED
REAL EMPLOYEE IDENTITIES: NOT REQUIRED
REAL SMTP/API SEND: NOT AUTHORIZED
REAL MAC STUDIO MUTATION: NOT AUTHORIZED
```

A real deployment remains a separate consumer activity requiring an explicit deployment request and explicit target.

---

## 11. Next lifecycle phase

The repository is now transition-ready for:

```text
BLUEPRINT VALIDATION
```

That phase should prove on an explicitly approved clean/synthetic target that a fresh capable AI agent can reproduce the designed system from repository artifacts alone.

It is **not yet opened**.

---

## 12. Completion language

```text
SYSTEM DESIGN COMPLETE        ← achieved
INSTALLATION DESIGN COMPLETE  ← achieved
BLUEPRINT VALIDATED           ← not yet opened
RELEASE READY                 ← not yet opened
```

Deployment-target readiness remains separate:

```text
CORE READY
CONFIGURED READY
PRODUCTION READY
```
