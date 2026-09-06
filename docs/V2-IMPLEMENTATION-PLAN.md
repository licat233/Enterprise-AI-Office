# Enterprise AI Office v2 — Installation Design Blueprint

Status: **installation design complete / final review PASS / real deployment not authorized**
Version: 3.0
Date: 2026-09-07

This document is the completed index and staged execution map for the Enterprise AI Office v2 `installation_design` milestone.

It translates the frozen v2 System Design into an agent-readable installation, recovery, and acceptance blueprint. The detailed normative contracts live in the ID-1 through ID-7 documents referenced below.

It does **not** authorize a real company installation, real mailbox credentials, real employee binding, SMTP/API sending, or mutation of an ARMOR production host.

Authoritative lifecycle state:

```text
state/PROJECT-PHASE.yaml
```

Current milestone state:

```text
SYSTEM DESIGN: COMPLETE
INSTALLATION DESIGN: COMPLETE
INSTALLATION DESIGN FINAL REVIEW: PASS
BLUEPRINT VALIDATION: NOT YET OPENED
REAL DEPLOYMENT TASK: INACTIVE
```

`current_phase` intentionally remains `installation_design` until a human explicitly opens `blueprint_validation`.

---

## 1. Frozen responsibilities

```text
Company/Product/SOP knowledge          → WeKnora
Employee Web identity/access           → Open WebUI / trusted identity layer
Agent role/capability                  → Hermes Profile
Mailbox/messages/provider send result  → Email Provider
DraftReply / SendApproval governance   → eao-email-governance
Governance persistence                 → local SQLite
Simple scheduled reminder state        → Hermes Cron when requested
Persistent multi-step Agent work       → Hermes Kanban only when justified
```

Do not create a mailbox mirror, CRM, second scheduler, graph runtime, generic send platform, or broad workflow engine.

---

## 2. Completed Installation Design work packages

| Work package | Result | Normative contract / evidence |
| --- | --- | --- |
| ID-1 Installation architecture + v1 preservation | COMPLETE | `docs/V2-INSTALLATION-ARCHITECTURE.md` — `INSTALLATION ARCHITECTURE FROZEN` |
| ID-2 Company config + protected inputs | COMPLETE | `docs/V2-CONFIG-PROTECTED-INPUTS.md` — `CONFIG / SECRET INPUT CONTRACT FROZEN` |
| ID-3 Stage / capability closure | COMPLETE | `docs/V2-STAGE-CONTRACTS.md` — `STAGE CONTRACTS FROZEN` |
| ID-4 Trusted identity + mailbox authorization | COMPLETE | `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md` — `IDENTITY / AUTHORIZATION INSTALLATION CONTRACT FROZEN` |
| ID-5 Draft / Approval governance runtime | COMPLETE | `docs/V2-GOVERNANCE-RUNTIME.md` — `GOVERNANCE RUNTIME CONTRACT FROZEN` |
| ID-6 Governed send + reconciliation | COMPLETE | `docs/V2-SEND-RECONCILIATION.md` — `SEND / RECONCILIATION INSTALLATION CONTRACT FROZEN` |
| ID-7 Recovery / rollback / clean-host acceptance | COMPLETE | `docs/V2-RECOVERY-CLEAN-HOST.md` — `RECOVERY / CLEAN-HOST INSTALLATION CONTRACT FROZEN` |

Final review:

```text
docs/V2-INSTALLATION-DESIGN-REVIEW.md
INSTALLATION DESIGN FINAL REVIEW: PASS
```

---

## 3. Reference runtime topology

```text
Employee
↓
Open WebUI
├─ General Assistant
│  ↓
│  Hermes general
│  ↓
│  WeKnora
│
└─ Communication Assistant
   ├─ Hermes communication Profile for reasoning
   └─ Open WebUI server-side governed Email tools/actions
      ↓
      eao-email-governance
      ├─ Governance SQLite
      └─ narrow provider adapters
         └─ Tencent Enterprise Mail (reference provider)
```

The v1 path must remain independent:

```text
Open WebUI → General Assistant → Hermes general → WeKnora
```

A Governance/Email failure must not break that path.

---

## 4. Configuration / protected-input model

The installer resolves four classes of state:

```text
A. Public reusable blueprint/schema
   → repository

B. Company-private non-secret desired state
   → private/company.yaml or equivalent protected overlay

C. Secrets / credentials
   → protected secret storage and native runtime bindings

D. Observed runtime state
   → actual runtime + deployment state record
```

Missing required input:

```text
BLOCKED — REQUIRED INPUT: <specific input>
```

Configuration conflict:

```text
BLOCKED — CONFIG CONFLICT: <specific conflict>
```

Security-contract violation:

```text
FAIL — SECURITY CONTRACT VIOLATION: <invariant>
```

Real credentials are never required merely to continue blueprint development.

---

## 5. Stage closure sequence

### Stage 0 — Preserve v1 baseline

Required outcome:

```text
V1 BASELINE VERIFIED
```

Verify Open WebUI employee access, Hermes general boundary, WeKnora grounded retrieval, fail-closed RBAC, and recoverability before enabling Email.

### Stage 1 — Read-only Email

Surface:

```text
search_email
get_email
```

Must remain mailbox/folder scoped and must not expose generic IMAP mutation.

Exit:

```text
READ-ONLY EMAIL PASS
```

### Stage 2 — Draft preparation

```text
authorized EmailMessage + WeKnora evidence
→ prepare_reply_draft
→ immutable DraftReply revision + server-computed content_hash
```

No provider-side send effect.

Exit:

```text
DRAFT PREPARATION PASS
```

### Stage 3 — Deterministic human approval

Open WebUI server-side Action resolves the exact persisted review binding, displays the exact persisted outbound content, and creates `SendApproval` only after explicit confirmation and current authorization/revision/hash revalidation.

Natural-language inference is never formal approval.

Exit:

```text
APPROVAL GATE PASS
```

### Stage 4 — Governed send + reconciliation

```text
ACTIVE SendApproval
→ one ApprovalClaim
→ one logical_send_id
→ durable SendAttempt
→ narrow provider adapter
```

Normalized provider-attempt outcomes are exactly:

```text
SENT
CONFIRMED_NOT_SENT
OUTCOME_UNKNOWN
```

Derived behavior:

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

Every retry must preserve the same immutable logical-send identity, including approved Draft revision/hash, sender/recipients, RFC Message-ID, Date, and transport payload hash.

Exit:

```text
GOVERNED EMAIL LOOP PASS
```

Stages 0–4 form the mandatory v2 Email core when Email is enabled.

### Stage 5 — Optional simple follow-up

Use Hermes Cron only when company configuration requests a simple reminder/review workflow.

Cron may remind, summarize, or prompt a new Draft; it may not bypass the human approval/send gate.

When not requested:

```text
NOT REQUESTED
```

### Stage 6 — Optional messaging surface

Enable at most one company-selected messaging surface when explicitly requested. It may provide employee entry, routing, or notification but must not own Email approval/provider authority.

When not requested:

```text
NOT REQUESTED
```

---

## 6. Trusted HumanActor / mailbox authorization path

Reference installation path:

```text
Open WebUI authenticated session
→ server-side current user + current groups
→ protected Open WebUI → Governance forwarder
→ canonical HumanActor
→ direct/group mailbox grants
→ operation-specific authorization
```

Canonical actor form:

```text
open-webui:<runtime-user-id>
```

Baseline mailbox permissions:

```text
email.read
email.draft
email.approve
email.send
```

Permissions are independent and mailbox-scoped. No explicit effective grant means deny.

Hermes Profile capability, HumanActor authorization, and provider credential are separate boundaries.

---

## 7. Governance persistence

Reference persistence:

```text
<runtime_root>/runtime/email-governance/state.sqlite3
```

Owned state includes:

```text
immutable DraftReply revisions
review bindings
SendApproval evidence
ApprovalClaim
governance audit
logical sends
send attempts / results
reconciliation evidence
```

Runtime Draft revision identity:

```text
(draft_id, revision)
```

Approval binding:

```text
draft_id + revision + content_hash
```

One Approval may authorize at most one logical send.

---

## 8. Provider binding

Reference provider:

```text
Tencent Enterprise Mail
```

Reference assets:

```text
infrastructure/email/tencent-exmail/imap_readonly_mcp.py
infrastructure/email/tencent-exmail/imap.env.example
infrastructure/email/tencent-exmail/test_imap_readonly.py
infrastructure/email/tencent-exmail/smtp_send_adapter.py
infrastructure/email/tencent-exmail/smtp.env.example
infrastructure/email/tencent-exmail/test_smtp_send_adapter.py
```

The obsolete direct Hermes Email MCP registration template has been removed. HumanActor-bound Email operations use the Open WebUI server-side governed tool/action path through `eao-email-governance`.

The provider adapter is narrow and internal. Ordinary employees/LLMs never receive a generic SMTP/send-anything primitive.

---

## 9. Backup / recovery / rollback

Reference recovery contract:

```text
docs/V2-RECOVERY-CLEAN-HOST.md
```

Governance helpers:

```text
infrastructure/email/governance/backup_state.py
infrastructure/email/governance/restore_state.py
infrastructure/email/governance/test_recovery.py
```

The existing full-stack helpers conditionally include v2 Governance state:

```text
scripts/backup.sh
scripts/restore.sh
```

Recovery rule:

```text
attempt exists without terminal result
or latest outcome is OUTCOME_UNKNOWN
→ RECONCILIATION_REQUIRED
→ restart/restore must not resend
```

Rollback is capability-oriented:

```text
Level 1  disable send only
Level 2  downgrade Email to read-only
Level 3  disable the whole v2 Email capability
```

Externally sent email is never “rolled back”.

All rollback levels preserve the v1 General path.

---

## 10. Installer idempotency

The installer may safely reconcile installation resources such as:

```text
directories
service definitions
Open WebUI groups/resources
Communication Assistant
Hermes communication Profile
Governance service config/schema
provider adapter binding
stage-enabled tool surfaces
```

Installer re-run must never create business side effects:

```text
no DraftReply
no SendApproval
no ApprovalClaim
no LogicalSend
no SendAttempt
no customer-visible send
no fabricated reconciliation conclusion
```

---

## 11. Acceptance and evidence

Provider-specific acceptance:

```text
docs/acceptance/TENCENT-EXMAIL.md
```

Repository static closure:

```sh
sh scripts/repository-readiness-check.sh
```

Offline design/implementation assets include:

```sh
python3 infrastructure/email/governance/test_schema.py
python3 infrastructure/email/governance/test_send_reconciliation.py
python3 infrastructure/email/governance/test_recovery.py
python3 infrastructure/email/tencent-exmail/test_imap_readonly.py
python3 infrastructure/email/tencent-exmail/test_smtp_send_adapter.py
```

Offline tests and static readiness evidence do not equal live provider acceptance.

---

## 12. Clean-host validation path

The next empirical phase, after explicit human transition, is:

```text
blueprint_validation
```

A fresh capable AI Engineering Agent must be able to use only repository + authorized target inputs to:

```text
inspect target
→ resolve configuration/capability closure
→ reproduce validated v1 path
→ install v2 Communication/Governance capability
→ close Stage 0–4
→ exercise backup/isolated restore/failure recovery
→ re-run installer and prove convergence
→ roll back v2 and re-prove v1
→ record evidence
```

The validation target must be explicitly authorized. Real production deployment remains a separate task.

---

## 13. Completion result

ID-1 through ID-7 are complete with no unresolved structural contradiction.

```text
INSTALLATION DESIGN FINAL REVIEW: PASS
INSTALLATION DESIGN: COMPLETE
```

Source:

```text
docs/V2-INSTALLATION-DESIGN-REVIEW.md
state/PROJECT-PHASE.yaml
```

The next phase is **Blueprint Validation**, but it is **not yet opened** and requires explicit human direction.
