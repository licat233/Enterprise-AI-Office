# Enterprise AI Office v2 — Blueprint Status

Status: installation design active / ID-1 and ID-2 complete / real deployment task inactive
Version: 3.1.0
Date: 2026-09-06

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
NEXT WORK PACKAGE: ID-3 STAGE / CAPABILITY CLOSURE
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

The core email model remains:

```text
Mailbox
EmailMessage
DraftReply
SendApproval
```

Installation Design must implement this contract without reopening scope merely for implementation convenience.

---

## 3. Installation Design mission

Installation Design must turn the frozen system design into a blueprint a fresh capable AI Engineering Agent can follow.

It must answer at least:

```text
What host/runtime topology is expected?
What existing v1 baseline must be preserved?
What company-private inputs are required?
Which inputs are secrets and where are they supplied?
What configuration schemas/templates are authoritative?
In what order are capabilities provisioned?
Which upstream components/adapters are used?
How is trusted HumanActor identity propagated?
How are mailbox-scoped permissions enforced?
Where do DraftReply / SendApproval / audit state persist?
How is send_approved_reply bound to the provider safely?
How are idempotency and ambiguous outcomes reconciled?
How is each stage removed or rolled back?
How does a clean-host installer prove readiness?
What evidence closes each capability and the whole installation?
```

---

## 4. Installation Design working order and progress

```text
ID-1  Installation architecture + v1 preservation     COMPLETE
ID-2  Company configuration + protected inputs        COMPLETE
ID-3  Stage sequencing + capability closure           NEXT
ID-4  Trusted identity + mailbox authorization        NOT STARTED
ID-5  Draft / Approval governance runtime             NOT STARTED
ID-6  Governed send + reconciliation                  NOT STARTED
ID-7  Rollback / recovery / clean-host acceptance     NOT STARTED
```

Completed contracts:

```text
ID-1 → docs/V2-INSTALLATION-ARCHITECTURE.md
       INSTALLATION ARCHITECTURE FROZEN

ID-2 → docs/V2-CONFIG-PROTECTED-INPUTS.md
       config/company.private.example.yaml
       CONFIG / SECRET INPUT CONTRACT FROZEN
```

Do not parallelize optional capabilities merely to make the blueprint appear comprehensive.

---

## 5. Configuration model now frozen by ID-2

Installation inputs are separated into:

```text
Public reusable blueprint
→ repository contracts/templates

Company-private non-secret desired state
→ protected private overlay such as private/company.yaml

Protected secrets
→ external/native protected secret mechanism

Observed runtime state
→ actual runtime + deployment state record
```

Environment files are runtime binding templates, not a second desired-state authority.

For v2 Email, the private desired-state model now uses:

```text
communication_profile
mailboxes
mailbox_grants
controlled_test_recipients
email_governance state/log paths
symbolic secret_refs
```

No matching mailbox grant means deny, and `send_requires_human_approval: true` is a frozen v2 security invariant rather than a company override.

---

## 6. Existing staged plan

`docs/V2-IMPLEMENTATION-PLAN.md` remains the active Installation Design working blueprint.

Its Stage 0–6 sequence remains:

```text
Stage 0  preserve/verify v1 baseline
Stage 1  bounded read-only email
Stage 2  DraftReply preparation
Stage 3  trusted human approval evidence
Stage 4  governed send_approved_reply
Stage 5  optional simple follow-up
Stage 6  optional one messaging surface
```

ID-3 now needs to turn these stages into explicit installation capability contracts covering:

```text
preconditions
required inputs
provisioning/reconciliation steps
idempotency expectations
acceptance evidence
state records
rollback/removal path
stage gate to the next capability
```

---

## 7. Explicit boundary: not a real deployment

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

Allowed work includes sanitized templates, scripts, adapters, synthetic fixtures, isolated rehearsals, acceptance contracts, and secret-input schemas **without real secret values**.

A real deployment remains a separate consumer activity and requires both:

```text
explicit human deployment request
+
explicit target
```

---

## 8. Scope discipline

Installation friction does not automatically justify changing System Design.

Prefer, in order:

```text
existing ARMOR/EAO capability
→ upstream-supported capability
→ thin adapter
→ minimum new component only if unavoidable
```

Do not introduce a new identity platform, workflow engine, CRM, graph runtime, scheduler, audit platform, or provider abstraction merely because it would make implementation theoretically cleaner.

If an actual structural contradiction in System Design is discovered, record it explicitly and reopen only the affected design contract.

---

## 9. Completion language

Repository/blueprint milestones:

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
