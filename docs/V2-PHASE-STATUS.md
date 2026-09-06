# Enterprise AI Office v2 — Blueprint Status

Status: installation design active / ID-1 through ID-6 complete / real deployment task inactive
Version: 3.5.0
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
INSTALLATION DESIGN: ACTIVE
ID-1 INSTALLATION ARCHITECTURE: COMPLETE
ID-2 CONFIG / PROTECTED INPUTS: COMPLETE
ID-3 STAGE / CAPABILITY CLOSURE: COMPLETE
ID-4 TRUSTED IDENTITY / MAILBOX AUTHORIZATION: COMPLETE
ID-5 DRAFT / APPROVAL GOVERNANCE RUNTIME: COMPLETE
ID-6 GOVERNED SEND / RECONCILIATION: COMPLETE
NEXT WORK PACKAGE: ID-7 RECOVERY / CLEAN-HOST ACCEPTANCE
BLUEPRINT VALIDATION: NOT YET OPENED
REAL DEPLOYMENT TASK: INACTIVE
```

The human explicitly advanced the blueprint lifecycle to `installation_design` on 2026-09-06.

This does **not** authorize a real company installation. Installation Design is repository design work: it defines how a capable AI Engineering Agent should install, configure, reconcile, validate, recover, and report the approved Enterprise AI Office v2 design on a future explicitly authorized target.

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

Core email model remains:

```text
Mailbox
EmailMessage
DraftReply
SendApproval
```

Runtime execution evidence introduced under ID-5/ID-6 does not add new Email Ontology business objects.

---

## 3. Installation Design progress

```text
ID-1  Installation architecture + v1 preservation     COMPLETE
ID-2  Company configuration + protected inputs        COMPLETE
ID-3  Stage sequencing + capability closure           COMPLETE
ID-4  Trusted identity + mailbox authorization        COMPLETE
ID-5  Draft / Approval governance runtime             COMPLETE
ID-6  Governed send + reconciliation                  COMPLETE
ID-7  Rollback / recovery / clean-host acceptance     NEXT
```

Completed contracts:

```text
ID-1 → docs/V2-INSTALLATION-ARCHITECTURE.md
       INSTALLATION ARCHITECTURE FROZEN

ID-2 → docs/V2-CONFIG-PROTECTED-INPUTS.md
       config/company.private.example.yaml
       CONFIG / SECRET INPUT CONTRACT FROZEN

ID-3 → docs/V2-STAGE-CONTRACTS.md
       STAGE CONTRACTS FROZEN

ID-4 → docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md
       infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md
       IDENTITY / AUTHORIZATION INSTALLATION CONTRACT FROZEN

ID-5 → docs/V2-GOVERNANCE-RUNTIME.md
       infrastructure/email/governance/schema.sql
       infrastructure/email/governance/test_schema.py
       infrastructure/open-webui/V2-APPROVAL-ACTION.md
       infrastructure/open-webui/v2_approve_draft_action.py
       GOVERNANCE RUNTIME CONTRACT FROZEN

ID-6 → docs/V2-SEND-RECONCILIATION.md
       infrastructure/email/governance/migrations/002_send_reconciliation.sql
       infrastructure/email/governance/test_send_reconciliation.py
       infrastructure/email/tencent-exmail/smtp_send_adapter.py
       infrastructure/email/tencent-exmail/smtp.env.example
       infrastructure/email/tencent-exmail/test_smtp_send_adapter.py
       SEND / RECONCILIATION INSTALLATION CONTRACT FROZEN
```

---

## 4. Identity / authorization path frozen by ID-4

Reference path:

```text
Employee browser
→ authenticated Open WebUI session
→ Communication Assistant
→ Hermes communication Profile for reasoning
→ Open WebUI server-side Email Governance tool/action execution
→ eao-email-governance
→ mailbox-scoped authorization
→ Email Provider
```

Open WebUI is the trusted HumanActor source. Browser/model-supplied actor or group values are not trusted authorization inputs.

Canonical HumanActor:

```text
open-webui:<Open WebUI user id>
```

---

## 5. Governance runtime frozen by ID-5

The v2 reference introduces one thin EAO runtime:

```text
eao-email-governance
```

Reference persistence:

```text
SQLite
<runtime_root>/runtime/email-governance/state.sqlite3
```

ID-5 freezes:

```text
immutable DraftReply revisions
review bindings
SendApproval evidence
single-logical-send ApprovalClaim
append-oriented governance audit
```

Draft revision identity:

```text
(draft_id, revision)
```

Approval binding:

```text
draft_id + revision + content_hash
```

One Approval may be claimed by only one logical send.

---

## 6. Governed send / reconciliation frozen by ID-6

ID-6 extends the same Governance runtime with execution evidence rather than adding a new service/platform.

Reference runtime facts:

```text
logical_sends
send_attempts
send_attempt_results
send_reconciliations
```

For every logical send:

```text
stable RFC Message-ID
stable Date header
transport_payload_hash
exact approved Draft/Approval binding
```

Provider-attempt outcomes are normalized to exactly:

```text
SENT
CONFIRMED_NOT_SENT
OUTCOME_UNKNOWN
```

Safety rule:

```text
SENT
→ no retry

CONFIRMED_NOT_SENT
→ controlled retry may occur only inside the same logical_send_id

OUTCOME_UNKNOWN
or durable attempt without terminal result
→ RECONCILIATION_REQUIRED
→ no blind retry
```

A controlled retry must reuse:

```text
same logical_send_id
same Approval/Draft revision/hash
same sender and recipient set
same Message-ID
same Date
same transport_payload_hash
```

Tencent SMTP is wrapped by a narrow internal adapter. All intended RCPT recipients must be accepted before DATA; one rejected recipient aborts the whole baseline transaction before DATA.

Once DATA transfer begins, transport loss without a trustworthy final SMTP response is conservatively `OUTCOME_UNKNOWN`.

Reconciliation is a protected governance/operator control path, not an employee/LLM tool. `REMAINS_UNKNOWN` remains blocked from retry.

---

## 7. Deterministic approval UI remains frozen

The Stage 3 Open WebUI Action resolves the exact persisted Draft through HumanActor/chat/message review binding, displays persisted From/To/Cc/Subject/Body in native confirmation UI, and only then commits SendApproval after authorization/revision/hash revalidation.

It does not parse formal approval or Draft authority out of model text.

Stage 4 provider submission remains downstream of that approval and of the committed ApprovalClaim/logical-send boundary.

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

## 9. Next work package — ID-7

ID-7 is the final Installation Design work package.

It must close:

```text
rollback/removal order for Stage 4 → 1
SQLite backup/restore including schema v2
migration/restart recovery
unresolved-send startup behavior
credential rotation/removal recovery
clean-host install path
idempotent re-run/reconcile behavior
failure injection / recovery checks
v1 preservation after v2 rollback/failure
machine-readable installation evidence
whole-blueprint installation acceptance
Installation Design final review
```

ID-7 must not perform a real deployment. It may define and add deterministic scripts, synthetic fixtures, isolated rehearsal instructions, and clean-host validation contracts.

---

## 10. Explicit boundary: not a real deployment

During Installation Design:

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

## 11. Scope discipline

Prefer:

```text
existing EAO capability
→ upstream-supported capability
→ thin adapter
→ minimum new component only if unavoidable
```

Do not introduce a new IAM platform, workflow engine, CRM, graph runtime, scheduler, queue, audit platform, or provider abstraction merely for implementation elegance.

---

## 12. Completion language

```text
SYSTEM DESIGN COMPLETE        ← achieved
INSTALLATION DESIGN COMPLETE  ← current target
BLUEPRINT VALIDATED
RELEASE READY
```

Deployment-target readiness remains separate:

```text
CORE READY
CONFIGURED READY
PRODUCTION READY
```

`INSTALLATION DESIGN COMPLETE` may be reached with zero access to ARMOR production or any real mailbox.
