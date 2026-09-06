# Enterprise AI Office v2 — Blueprint Status

Status: system design active / installation design not yet opened / real deployment task inactive
Version: 2.0.0
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

## 2. Current blueprint phase

```text
RELEASE TRACK: v2
BLUEPRINT PHASE: SYSTEM DESIGN
INSTALLATION DESIGN: NOT YET OPENED
BLUEPRINT VALIDATION: NOT YET OPENED
REAL DEPLOYMENT TASK: INACTIVE
```

Current work should continue designing **what v2 should be**.

This includes product behavior, architecture, capability boundaries, security, human approval, identity, Ontology, provider choices, failure semantics, and acceptance criteria.

Provider research, sanitized examples, offline prototypes, and offline tests may support design decisions. Their presence does not mean installation design has started and does not mean a real company system is being deployed.

## 3. Blueprint lifecycle

The intended repository-development sequence is:

```text
System Design
→ Installation Design
→ Blueprint Validation
→ Release Ready
```

### System Design

Define the system itself:

```text
product/capability scope
architecture
user and Agent workflows
authority/RBAC
security boundaries
Ontology/action semantics
provider/upstream choices
failure/reconciliation behavior
acceptance criteria
non-goals
```

### Installation Design

After the system design is sufficiently approved, turn it into an installation blueprint that a capable AI engineering agent can execute:

```text
deployment architecture
installation sequence
config schemas/templates
provision/install scripts
secret-input contracts
idempotency/reconciliation
rollback/recovery
clean-host setup
machine-readable capability closure
installation-time acceptance
```

**Installation Design is still repository design. It does not mean installing onto ARMOR's real infrastructure.**

### Blueprint Validation

Use an explicitly approved clean/isolated validation target to prove that a fresh capable AI agent can:

```text
read the repository
understand the intended Enterprise AI Office
resolve required non-secret/company-private inputs
install the designed system
run acceptance
report readiness correctly
```

A validation target is not automatically a production deployment.

### Release Ready

The blueprint is ready when the repository sufficiently explains both the system and the installation/acceptance path for adoption.

## 4. Real deployment is a separate activity

A real company deployment is a consumer of the blueprint, not the automatic next repository phase.

It requires a separate explicit request with an explicit target, for example a designated Mac Studio.

Without such a task, repository work must not request or use real credentials, connect real provider accounts, bind real employee identities, or mutate a live environment merely to continue blueprint development.

## 5. Current v2 system-design direction

The controlled v2 milestone remains:

```text
Communication & Follow-up
```

The current email design direction includes:

```text
provider reference: Tencent Enterprise Mail
read operations: search_email, get_email
governed DraftReply
trusted human approval bound to exact draft state
governed send_approved_reply
optional simple follow-up later
optional one messaging surface later
```

Current design-support artifacts may include provider research, read-only adapter prototypes, synthetic fixtures, Ontology examples, tests, and acceptance drafts.

They validate or explore design properties only.

## 6. Recorded offline design evidence

Without connecting a real mailbox, previous design-support checks recorded:

```text
email Ontology structural validation: PASS
read-only adapter safety logic: 5/5 PASS with dependency-environment caveat
repository static closure mirror: 86 PASS / 0 FAIL at the recorded check
```

These results do not mean a Tencent Enterprise Mail capability has been deployed.

## 7. Installation-plan artifact status

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

While the blueprint phase is still `system_design`, this document is an input for identifying future installation requirements, not an executable instruction to move into provider runtime work.

When the human explicitly advances the blueprint lifecycle to `installation_design`, this sequence can be audited, revised, and converted into the actual agent-readable installation contract.

## 8. Current work that remains valid

Examples:

```text
Human Approval & Identity Model
email action semantics
failure/reconciliation design
follow-up behavior
messaging-entry design
security/threat review
scope review
Ontology refinement driven by design needs
upstream/provider research
acceptance criteria
sanitized prototypes or synthetic tests that answer design questions
```

## 9. Current boundary

```text
SYSTEM DESIGN: ACTIVE
INSTALLATION DESIGN: NOT YET OPENED
REAL COMPANY DEPLOYMENT: NOT ACTIVE
REAL PROVIDER CREDENTIALS: NOT REQUIRED
REAL MAILBOX ACCESS: NOT REQUIRED
```

Continuation wording such as `继续`, `开始吧`, `下一步`, `continue`, or `next` means continue the current **system-design** work unless the human explicitly directs a blueprint-phase change.

## 10. Completion language

Keep repository maturity distinct from deployment readiness.

Repository/blueprint milestones:

```text
SYSTEM DESIGN COMPLETE
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
