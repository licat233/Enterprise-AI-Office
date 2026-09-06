# Enterprise AI Office v2 — Blueprint Status

Status: installation design active / ID-1 through ID-5 complete / real deployment task inactive
Version: 3.4.0
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
ID-5 DRAFT / APPROVAL GOVERNANCE RUNTIME: COMPLETE
NEXT WORK PACKAGE: ID-6 GOVERNED SEND / RECONCILIATION
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
ID-5  Draft / Approval governance runtime             COMPLETE
ID-6  Governed send + reconciliation                  NEXT
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

ID-5 → docs/V2-GOVERNANCE-RUNTIME.md
       infrastructure/email/governance/schema.sql
       infrastructure/email/governance/test_schema.py
       infrastructure/open-webui/V2-APPROVAL-ACTION.md
       infrastructure/open-webui/v2_approve_draft_action.py
       GOVERNANCE RUNTIME CONTRACT FROZEN
```

---

## 4. Identity / authorization path frozen by ID-4

The reference installation does not rely on Hermes to relay HumanActor identity into downstream MCP calls.

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

Open WebUI is the trusted HumanActor source and server-side tool/action forwarder.

Canonical HumanActor:

```text
open-webui:<Open WebUI user id>
```

The dedicated Open WebUI → Governance connection uses protected service authentication and server-side current-user/group context. Browser/model-supplied actor or group values are never trusted authorization inputs.

---

## 5. Governance runtime frozen by ID-5

The v2 reference introduces only one thin EAO runtime:

```text
eao-email-governance
```

Reference persistence:

```text
SQLite
<runtime_root>/runtime/email-governance/state.sqlite3
```

Minimum persistent classes:

```text
immutable DraftReply revisions
review bindings
SendApproval evidence
single-logical-send approval claims
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

Approval state is derived from persisted facts:

```text
ACTIVE
STALE
REVOKED
CONSUMED
EXPIRED when optional expiry policy is configured
```

One Approval may be claimed by only one logical send.

The claim is committed before any provider side effect; provider attempts and reconciliation are completed under ID-6.

---

## 6. Deterministic approval UI frozen by ID-5

The pinned Open WebUI reference line supports server-side Actions with authenticated `__user__`, current chat/message context, group lookup, and native confirmation callbacks.

The reference Stage 3 Action therefore:

```text
uses HumanActor + chat + assistant-message review binding
→ resolves exact persisted Draft from Governance
→ displays exact From/To/Cc/Subject/Body in native confirmation UI
→ employee explicitly confirms/cancels
→ Governance re-checks current authorization + exact revision/hash
→ creates SendApproval
```

It does not parse approval authority or Draft identity out of model-generated text.

Stage 3 Action performs no provider send.

---

## 7. Stage / capability closure

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

## 8. Next work package — ID-6

ID-6 must now freeze the provider-side half of the already claimed logical send:

```text
provider SMTP/send binding
fully resolved immutable outbound payload
logical send execution / provider-attempt records
sender-mailbox restriction
provider result normalization
SENT / CONFIRMED_NOT_SENT / OUTCOME_UNKNOWN mapping
controlled retry after confirmed-not-sent
RECONCILIATION_REQUIRED after ambiguous outcome
provider evidence lookup/correlation
no blind duplicate send
Stage 4 Approve & Send UX evolution
```

ID-6 must preserve ID-5's invariant:

```text
one SendApproval
→ one logical send claim
→ provider side effect only after claim
```

---

## 9. Explicit boundary: not a real deployment

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

## 10. Scope discipline

Prefer:

```text
existing EAO capability
→ upstream-supported capability
→ thin adapter
→ minimum new component only if unavoidable
```

Do not introduce a new IAM platform, workflow engine, CRM, graph runtime, scheduler, audit platform, or provider abstraction merely for implementation elegance.

---

## 11. Completion language

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
