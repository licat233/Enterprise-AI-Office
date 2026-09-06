# Enterprise AI Office v2 — Installation Architecture

Status: installation architecture frozen / ID-4 identity-path refinement applied / real deployment not authorized
Version: 1.1
Date: 2026-09-06

This document closes `ID-1 — Installation architecture and v1 preservation boundary` for the Enterprise AI Office v2 `installation_design` phase and incorporates the identity-safe tool-routing refinement discovered during ID-4.

It defines the minimum runtime topology that a future authorized installer should reproduce. It does **not** authorize installation on any real company host, use of real employee identities, mailbox credentials, or customer-facing sends.

Use with:

- `state/PROJECT-PHASE.yaml`
- `docs/ARCHITECTURE.md`
- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-IMPLEMENTATION-PLAN.md`
- `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`
- `config/company.example.yaml`
- `config/capabilities.yaml`

---

## 1. Architecture objective

v2 must add governed email capability without destabilizing or redesigning the validated v1 employee path.

The reference architecture follows two rules:

```text
preserve the v1 General Assistant path unchanged
+
add the smallest isolated runtime boundary that can deterministically govern email state/actions
```

The design must not introduce a CRM, generic workflow platform, mailbox mirror, graph runtime, second scheduler, or broad mail-automation platform.

---

## 2. v1 preservation boundary

The validated v1 path remains:

```text
Employee
↓
Open WebUI
↓
General Assistant
↓
Hermes `general` Profile
↓
WeKnora
↓
grounded answer + source
```

The following remain unchanged:

```text
Open WebUI employee identity / ordinary chat UX
General Assistant resource
Hermes `general` Profile
`general` Profile WeKnora retrieval boundary
WeKnora knowledge authority
v1 knowledge ingestion/retrieval paths
existing employee conversation history
existing v1 production backup/recovery responsibilities
```

The v2 reference path must not add Email provider/governance startup dependencies to the validated `general` Profile.

If the entire v2 email capability is disabled or unhealthy, the v1 General Assistant path must remain independently usable.

---

## 3. Reference v2 topology

ID-4 upstream verification refined the original ID-1 assumption that Hermes should transitively carry HumanActor identity into the Email MCP boundary.

The reference topology now uses Open WebUI's server-side external-tool execution for the identity-sensitive Email Governance path:

```text
                           ┌──────────────────────┐
Employee ─────────────────►│      Open WebUI      │
                           └──────────┬───────────┘
                                      │
                    ┌─────────────────┴────────────────────────┐
                    │                                          │
                    ▼                                          ▼
          General Assistant                         Communication Assistant
                    │                                          │
                    ▼                                          ▼
          Hermes `general`                         Hermes communication Profile
                    │                                          │
                    ▼                                          ▼
                WeKnora                                   WeKnora / reasoning
                                                               │
                           Open WebUI server-side tool loop ◄───┘
                                      │
                                      │ trusted HumanActor context
                                      ▼
                           EAO Email Governance Service
                                      │
                                      ▼
                                Email Provider

Open WebUI trusted approval Action ───► EAO Email Governance Service
```

The Communication Assistant remains backed by the isolated Hermes communication Profile, but Open WebUI executes the Email Governance MCP/OpenAPI tools server-side and supplies trusted current-user context directly to governance.

This preserves the frozen System Design responsibilities while avoiding a Hermes fork or unproven transitive header propagation.

---

## 4. New runtime responsibility — EAO Email Governance Service

v2 introduces exactly one new EAO-owned runtime responsibility:

```text
EAO Email Governance Service
```

Reference service identifier:

```text
eao-email-governance
```

This is a narrow local service, not a new enterprise platform.

It owns only:

```text
Mailbox-scoped authorization enforcement
provider read adapter boundary
DraftReply persistence
Draft revision/content-hash generation or validation
SendApproval persistence and lifecycle enforcement
single-logical-send claim/enforcement
provider send adapter boundary when Stage 4 is enabled
provider-result normalization/reference capture
reconciliation state
append-oriented governance evidence
```

It does not own:

```text
LLM/model inference
company knowledge authority
employee authentication
Open WebUI group administration
Hermes Profile configuration
Cron scheduling
Kanban task management
mailbox mirroring
CRM/customer records
bulk/campaign sending
attachment archive
generic IMAP/SMTP/API proxy
```

---

## 5. Why a separate governance service is justified

DraftReply and SendApproval are EAO-owned authoritative state shared across model-assisted draft/read operations, trusted human approval, provider send and reconciliation.

Keeping this state only in chat, Hermes session, SOUL/Skill, or Open WebUI message text would not provide deterministic authorization or restart-safe governance.

Writing directly into Open WebUI or Hermes internal databases would create unsupported coupling and incorrectly turn those components into the authority for email governance state.

Therefore one thin service is the minimum clean boundary.

Do not split it into separate Draft, Approval, Audit, Retry, or Workflow services.

---

## 6. Reference process placement

For the first validated macOS/arm64 reference posture:

```text
Host-native
├── existing Hermes runtime
├── Hermes communication Profile API/Gateway process
└── eao-email-governance

OrbStack / Docker
├── existing WeKnora stack
└── existing Open WebUI
```

The governance service should remain host-native unless later implementation evidence proves a container materially simpler.

Open WebUI reaches it through an explicitly approved private host bridge/private endpoint.

A non-macOS deployment may use the platform-native equivalent while preserving the same trust/process boundaries.

---

## 7. Hermes isolation boundary

The reference v2 capability uses a separate Hermes employee Profile rather than extending `general`.

```text
general
→ WeKnora
→ existing v1 employee path
→ no Email Governance tools by default

communication
→ WeKnora / communication reasoning
→ exposed to employee through restricted Communication Assistant
```

The Communication Assistant has stage-enabled Email Governance tools attached at the Open WebUI model/tool layer. Open WebUI executes those tools server-side; Hermes does not authenticate the employee to governance.

The communication Profile still uses its own API credential and isolated employee Assistant/resource grant.

Where the selected Hermes release supports a separate Profile API process/port, prefer it so a malformed/unavailable email integration cannot become a startup dependency of v1 `general`.

---

## 8. Open WebUI boundary

Open WebUI remains:

```text
employee Web surface
human authentication/identity source
Assistant/resource RBAC surface
server-side external-tool execution boundary for v2 Email
trusted human approval Action surface
```

The reference v2 installation adds only:

```text
one restricted Communication Assistant/Model resource
one admin-managed Email Governance external-tool connection
one server-side trusted approval Action/Function or equivalent native extension
```

Open WebUI must not become the Source of Truth for DraftReply, SendApproval, logical send state, or provider result.

Do not write v2 governance records directly into Open WebUI's internal application tables.

Trusted identity propagation is defined in `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`.

---

## 9. Email Governance operation surface

Stage-gated surface:

```text
Stage 1
  search_email
  get_email

Stage 2
  prepare_reply_draft

Stage 3
  no model-inferred approval primitive

Stage 4
  send_approved_reply behind governed action gate
```

The Communication Assistant/model may decide to invoke read/draft tools, but Open WebUI performs the server-side tool request to governance with current HumanActor context.

Formal `approve_reply_draft` originates only from a deterministic trusted-human path.

`send_approved_reply` does not need to be a free-choice ordinary LLM tool when the trusted `Approve & Send` action can invoke it directly after approval.

No generic provider mutation primitive is exposed.

---

## 10. Provider boundary

The governance service owns the narrow provider binding for configured mailboxes.

```text
Governance Service
├── read adapter → provider-supported mailbox read surface
└── send adapter → provider-supported outbound surface, Stage 4 only
```

Current Tencent Enterprise Mail reference candidate:

```text
read candidate → IMAP over TLS
send candidate → SMTP over TLS
```

Provider credentials remain inside the governance/provider runtime secret boundary and never enter Open WebUI user state, model prompts, WeKnora, or ordinary tool arguments.

The provider remains authoritative for source messages and actual delivery state.

---

## 11. Persistent state boundary

The single-host reference uses one local SQLite database owned only by governance:

```text
<runtime_root>/runtime/email-governance/state.sqlite3
```

It stores only EAO-owned governance state:

```text
DraftReply
SendApproval
logical send execution/claim state
governance audit events
reconciliation state/provider references
```

It must not become a mailbox cache or customer database.

DraftReply bodies are persisted because the exact outbound artifact being approved is EAO-owned state; normal inbound message bodies remain provider-backed context.

---

## 12. Logs and secrets

```text
technical logs
→ <runtime_root>/logs/email-governance/ or platform service logs

governance state
→ governance SQLite database

provider/model/Profile/forwarder secrets
→ protected secret storage defined by ID-2
```

No credentials, bearer/session tokens, mailbox passwords, or unnecessary full email bodies may be written to normal logs.

---

## 13. Network / trust paths

Required logical paths:

```text
Employee browser
→ Open WebUI

Open WebUI
→ Hermes employee Profile API

Hermes communication Profile
→ WeKnora supported retrieval interface

Open WebUI server-side Email tool connection
→ EAO Email Governance private endpoint

Open WebUI server-side approval Action
→ EAO Email Governance trusted action endpoint

EAO Email Governance
→ Email Provider over approved encrypted transport
```

Not allowed:

```text
Employee browser → governance service directly
Employee browser → provider credential
LLM/tool arguments → trusted actor identity
Hermes → governance SQLite directly
Open WebUI → governance SQLite directly
Governance service → Open WebUI internal DB directly
Governance service → WeKnora internal database
public Internet → governance service inbound
```

The private tool channel must authenticate Open WebUI as a trusted forwarder and fail closed when trusted HumanActor context is absent.

---

## 14. Startup and failure containment

Required behavior:

```text
communication Profile unavailable
→ v2 communication reasoning unavailable
→ v1 General Assistant remains available

governance service unavailable
→ Email tools/actions fail closed
→ v1 General Assistant remains available

email provider unavailable
→ email operations fail/enter applicable reconciliation state
→ v1 General Assistant remains available

Open WebUI unavailable
→ employee Web entry unavailable as in v1
```

Governance must not become a startup prerequisite for `general`.

Reference activation order:

```text
v1 core healthy
→ governance service healthy
→ communication Profile healthy
→ Open WebUI Communication Assistant + Email tool connection/action enabled
```

Disable/removal occurs in reverse dependency order.

---

## 15. Stage activation model

```text
Stage 0
  v1 only

Stage 1
  communication Profile + governance service
  Open WebUI Email read tools
  provider read binding only

Stage 2
  DraftReply persistence + prepare tool enabled

Stage 3
  trusted approval Action + SendApproval persistence enabled
  provider send remains disabled

Stage 4
  governed provider send binding enabled

Stage 5
  optional Hermes Cron reuses the same governance boundary

Stage 6
  optional messaging reuses the same approved Profile/governance operations
```

Do not create a temporary read architecture that must later be replaced for send.

---

## 16. Removal / rollback boundary

Minimum v2 removal sequence:

```text
disable employee Communication Assistant/action/tool grants
→ remove/disable Open WebUI Email Governance tool connection
→ stop/disable communication Profile service
→ stop/disable governance service
→ revoke/remove email provider and forwarder credentials
→ preserve/archive governance state according to policy
→ verify General Assistant v1 path remains healthy
```

Externally sent email cannot be rolled back.

A lost/unavailable governance database must never cause the system to infer approval existed; governed send fails closed.

Detailed backup/restore mechanics are completed under ID-7.

---

## 17. Explicitly rejected alternatives

### Put all v2 Email capability into `general`

Rejected because it expands the validated v1 risk/credential boundary and weakens failure isolation.

### Make Hermes relay HumanActor identity to MCP through a custom fork

Rejected for the reference path because Open WebUI already has a supported server-side tool execution and user-context mechanism; a Hermes fork would add unnecessary coupling.

### Store approvals only in chat/history

Rejected because conversation text is not deterministic authorization evidence.

### Store governance state in Open WebUI/Hermes internal databases

Rejected because those systems are not the authority for EAO Email governance state and direct internal DB coupling is unsupported.

### Add PostgreSQL/Redis, n8n, workflow engine or event bus

Rejected because the single-host v2 baseline does not require them.

---

## 18. ID-1 acceptance contract

Installation Architecture remains frozen when the blueprint establishes:

```text
[✓] validated v1 General Assistant path remains unchanged
[✓] v2 communication reasoning has an isolated Hermes Profile boundary
[✓] one thin EAO Email Governance Service owns deterministic email governance state
[✓] Open WebUI supplies trusted HumanActor context directly on server-side governance tool/action calls
[✓] no Hermes fork/transitive identity relay is required
[✓] no new broad platform/database/workflow system is introduced
[✓] provider remains source of mailbox/delivery truth
[✓] governance SQLite stores only EAO-owned state
[✓] v2 failure/removal does not require v1 redesign
[✓] stage activation reuses one stable topology
[✓] real deployment remains independently gated
```

Result:

```text
ID-1: PASS
INSTALLATION ARCHITECTURE FROZEN
```
