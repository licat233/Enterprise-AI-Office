# Enterprise AI Office v2 — Blueprint Status

Status: system design complete / awaiting explicit lifecycle transition / real deployment task inactive
Version: 2.1.0
Date: 2026-09-06

The authoritative machine-readable repository state is:

```text
state/PROJECT-PHASE.yaml
```

This document explains that state for humans. If this prose conflicts with `state/PROJECT-PHASE.yaml`, the machine-readable file wins until an explicit human-directed blueprint transition updates both.

## 1. What this repository is building

Enterprise AI Office is not the deployment record of one ARMOR machine.

It is a reusable blueprint that must eventually explain:

```text
what the Enterprise AI Office is
+
how a capable AI engineering agent installs it
+
how that agent verifies that the installed system is correct
```

Therefore repository development has a blueprint lifecycle separate from any real company deployment.

## 2. Current blueprint phase and milestone

```text
RELEASE TRACK: v2
BLUEPRINT PHASE: SYSTEM DESIGN
SYSTEM DESIGN MILESTONE: COMPLETE
NEXT BLUEPRINT PHASE: INSTALLATION DESIGN (NOT YET OPENED)
BLUEPRINT VALIDATION: NOT YET OPENED
REAL DEPLOYMENT TASK: INACTIVE
```

The repository remains in the `system_design` lifecycle phase because phase transitions require explicit human direction. The System Design milestone itself is complete and should not remain open merely for optional optimization or hardening.

No further v2 System Design scope should be added unless a real structural defect or contradiction is discovered.

---

## 3. Blueprint lifecycle

The repository-development sequence remains:

```text
System Design
→ Installation Design
→ Blueprint Validation
→ Release Ready
```

### System Design — COMPLETE

The v2 baseline now defines:

```text
product/capability scope
architecture
user and Agent workflow
HumanActor identity boundary
Mailbox-scoped authorization
human approval semantics
Draft / Approval / Send lifecycle
employee UX
Source-of-Truth boundaries
Ontology/action semantics
failure/reconciliation behavior
audit/governance evidence
follow-up boundary
acceptance/non-goal boundary
```

The final result is recorded in:

```text
docs/V2-DESIGN-REVIEW.md
```

### Installation Design — NOT YET OPENED

After an explicit human lifecycle transition, convert the approved system design into an agent-readable and agent-executable installation blueprint:

```text
deployment architecture
installation sequence
config schemas/templates
provision/install scripts
secret-input contracts
identity propagation implementation
provider/tool bindings
approval persistence/enforcement
idempotency/reconciliation implementation
rollback/recovery
clean-host setup
machine-readable capability closure
installation-time acceptance
```

**Installation Design is still repository design. It does not mean installing onto ARMOR's real infrastructure.**

### Blueprint Validation — NOT YET OPENED

Use an explicitly approved clean/isolated validation target to prove that a fresh capable AI agent can understand and reproduce the blueprint.

A validation target is not automatically a production deployment.

### Release Ready

The blueprint is ready when the repository sufficiently explains both the approved system and the installation/acceptance path for adoption.

---

## 4. Real deployment is a separate activity

A real company deployment is a consumer of the blueprint, not the automatic next repository phase.

It requires a separate explicit request with an explicit target, for example a designated Mac Studio.

Without such a task, repository work must not request or use real credentials, connect real provider accounts, bind real employee identities, or mutate a live environment merely to continue blueprint development.

---

## 5. Completed v2 system-design baseline

The controlled v2 milestone remains:

```text
Communication & Follow-up
```

Completed baseline operational loop:

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

The completed baseline includes:

```text
provider reference: Tencent Enterprise Mail
minimal Email objects: Mailbox, EmailMessage, DraftReply, SendApproval
read operations: search_email, get_email
human permissions: email.read, email.draft, email.approve, email.send
trusted HumanActor distinct from Hermes Profile and provider credential
exact Draft revision/hash approval binding
single-logical-send approval semantics
send outcomes: SENT / FAILED_NOT_SENT / RECONCILIATION_REQUIRED
Open WebUI employee UX baseline
append-oriented governance evidence
Hermes Cron for simple reminders/summaries
optional one messaging surface later
```

Current design-support artifacts may include provider research, read-only adapter prototypes, synthetic fixtures, Ontology examples, tests, and acceptance drafts. They remain design-support artifacts only.

---

## 6. Recorded offline design evidence

Without connecting a real mailbox, previous design-support checks recorded:

```text
email Ontology structural validation: PASS
read-only adapter safety logic: 5/5 PASS with dependency-environment caveat
repository static closure mirror: 86 PASS / 0 FAIL at the recorded check
```

These results do not mean a Tencent Enterprise Mail capability has been deployed.

---

## 7. Existing implementation-plan artifact

`docs/V2-IMPLEMENTATION-PLAN.md` currently captures an early staged installation/deployment idea:

```text
Stage 0  preserve/verify v1 baseline
Stage 1  bounded read-only email
Stage 2  DraftReply preparation
Stage 3  trusted human approval evidence
Stage 4  governed send_approved_reply
Stage 5  optional simple follow-up
Stage 6  optional one messaging surface
```

Because Installation Design has not yet been explicitly opened, this remains an input for the next lifecycle phase rather than an executable instruction to begin real provider work.

When the human explicitly advances the blueprint lifecycle to `installation_design`, this sequence should be audited against the completed System Design and converted into the actual agent-readable installation contract.

---

## 8. Deferred non-blocking decisions

The following do not reopen System Design:

```text
exact JWT/OIDC/trusted actor propagation mechanism
exact provider API/MCP/SMTP implementation
exact secret store
exact audit persistence backend
exact approval TTL
second-person approval policy
retry backoff mechanics
provider-specific delivery states
attachments / Bcc / scheduled send
manager approval hierarchy
ABAC / dynamic risk policies
SIEM / compliance analytics
```

They belong to later Installation Design, hardening, or future-version work when required.

---

## 9. Current boundary

```text
SYSTEM DESIGN: COMPLETE
BLUEPRINT PHASE: SYSTEM DESIGN
INSTALLATION DESIGN: NOT YET OPENED
REAL COMPANY DEPLOYMENT: NOT ACTIVE
REAL DEPLOYMENT TASK: INACTIVE
REAL PROVIDER CREDENTIALS: NOT REQUIRED
REAL MAILBOX ACCESS: NOT REQUIRED
```

Continuation wording such as `继续`, `开始吧`, `下一步`, `continue`, or `next` still does not change the blueprint phase.

Because the current System Design milestone is complete, an explicit human direction is required to advance to `installation_design`.

---

## 10. Completion language

Keep repository maturity distinct from deployment readiness.

Repository/blueprint milestones:

```text
SYSTEM DESIGN COMPLETE        ← achieved for v2 baseline
INSTALLATION DESIGN COMPLETE
BLUEPRINT VALIDATED
RELEASE READY
```

Deployment-target readiness:

```text
CORE READY
CONFIGURED READY
PRODUCTION READY
```

A blueprint can reach `INSTALLATION DESIGN COMPLETE` without touching ARMOR production. A real ARMOR deployment can later consume that blueprint and separately reach `PRODUCTION READY`.
