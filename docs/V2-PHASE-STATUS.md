# Enterprise AI Office v2 — Blueprint Status

Status: installation design active / ID-1 through ID-4 complete / real deployment task inactive
Version: 3.3.0
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
ID-3 STAGE / CAPABILITY CLOSURE: COMPLETE
ID-4 TRUSTED IDENTITY / MAILBOX AUTHORIZATION: COMPLETE
NEXT WORK PACKAGE: ID-5 GOVERNANCE RUNTIME
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

Core email model:

```text
Mailbox
EmailMessage
DraftReply
SendApproval
```

Installation Design must implement this contract without reopening scope merely for implementation convenience.

---

## 3. Installation Design progress

```text
ID-1  Installation architecture + v1 preservation     COMPLETE
ID-2  Company configuration + protected inputs        COMPLETE
ID-3  Stage sequencing + capability closure           COMPLETE
ID-4  Trusted identity + mailbox authorization        COMPLETE
ID-5  Draft / Approval governance runtime             NEXT
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

ID-3 → docs/V2-STAGE-CONTRACTS.md
       STAGE CONTRACTS FROZEN

ID-4 → docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md
       infrastructure/open-webui/V2-COMMUNICATION-PROVISIONING.md
       IDENTITY / AUTHORIZATION INSTALLATION CONTRACT FROZEN
```

---

## 4. Identity / authorization path frozen by ID-4

The reference installation no longer relies on Hermes to relay HumanActor identity into downstream MCP calls.

Reference path:

```text
Employee browser
→ authenticated Open WebUI session
→ Communication Assistant
→ Hermes communication Profile for reasoning
→ Open WebUI server-side Email Governance tool execution
→ eao-email-governance
→ mailbox-scoped authorization
→ Email Provider
```

Open WebUI is the trusted HumanActor source and server-side tool forwarder.

Canonical HumanActor:

```text
open-webui:<Open WebUI user id>
```

The dedicated Open WebUI → Governance connection uses protected service authentication and server-side current-user/group context. Browser/model-supplied actor or group values are never trusted authorization inputs.

Company logical groups are deterministically mapped to runtime Open WebUI group IDs; governance evaluates direct + current group mailbox grants additively, and no matching grant means deny.

The old direct Hermes Email MCP registration template was removed because it would require unproven transitive identity propagation. Hermes remains the isolated AI role/reasoning boundary; Open WebUI's native server-side tool mechanism carries the HumanActor context.

---

## 5. Stage / capability closure

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

## 6. Next work package — ID-5

ID-5 now closes the smallest deterministic governance runtime behind the trusted identity path.

It must freeze:

```text
SQLite schema / migrations
DraftReply persistence
canonical revision + content_hash
SendApproval persistence
stale / revoke / consume behavior
trusted approval Action binding
single logical-send claim boundary
append-oriented governance evidence
governance service API/MCP surface
restart/concurrency/transaction behavior
```

It must not create a generic workflow platform or duplicate provider mailbox state.

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

A real deployment remains a separate consumer activity requiring an explicit deployment request and explicit target.

---

## 8. Scope discipline

Prefer:

```text
existing EAO capability
→ upstream-supported capability
→ thin adapter
→ minimum new component only if unavoidable
```

Do not introduce a new IAM platform, workflow engine, CRM, graph runtime, scheduler, audit platform, or provider abstraction merely for implementation elegance.

---

## 9. Completion language

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
