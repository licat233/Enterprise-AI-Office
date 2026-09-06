# Enterprise AI Office v2 — Installation Architecture

Status: installation architecture frozen / real deployment not authorized
Version: 1.0
Date: 2026-09-06

This document closes `ID-1 — Installation architecture and v1 preservation boundary` for the Enterprise AI Office v2 `installation_design` phase.

It defines the minimum runtime topology that a future authorized installer should reproduce. It does **not** authorize installation on any real company host, use of real employee identities, mailbox credentials, or customer-facing sends.

Use with:

- `state/PROJECT-PHASE.yaml`
- `docs/ARCHITECTURE.md`
- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-IMPLEMENTATION-PLAN.md`
- `config/company.example.yaml`
- `config/capabilities.yaml`

---

## 1. Architecture objective

v2 must add governed email capability without destabilizing or redesigning the validated v1 employee path.

The reference architecture therefore follows two rules:

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

For the v2 reference topology, the following v1 responsibilities remain unchanged:

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

The v2 reference path must not add Email MCP/provider dependencies to the validated `general` Profile.

If the entire v2 email capability is disabled or unhealthy, the v1 General Assistant path must remain independently usable.

---

## 3. Reference v2 topology

The minimum v2 reference topology is:

```text
                           ┌──────────────────────┐
Employee ─────────────────►│      Open WebUI      │
                           └──────────┬───────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
          General Assistant                  Communication Assistant
                    │                                   │
                    ▼                                   ▼
          Hermes `general`                  Hermes communication Profile
                    │                            │                 │
                    ▼                            │                 │
                WeKnora                         │                 ▼
                                                 │      EAO Email Governance Service
                                                 │                 │
                                                 ▼                 ▼
                                              WeKnora        Email Provider

Open WebUI trusted approval Action ───────────────► EAO Email Governance Service
```

The exact communication Profile identifier is company-configurable. Public examples may use the synthetic identifier:

```text
communication
```

The reference blueprint uses a separate employee-facing communication Profile because email introduces a materially different tool/credential/risk boundary.

A company may choose a different specialist Profile name or an equivalent isolated Profile mapping, but the v1 `general` path must remain independently recoverable and testable.

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

It owns only the deterministic v2 email governance responsibilities that do not belong safely in prompts, Open WebUI internals, Hermes Profile state, WeKnora, or the email provider.

### Responsibilities

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

### Explicit non-responsibilities

```text
LLM/model inference
company knowledge retrieval authority
employee authentication
Open WebUI group administration
Hermes Profile configuration authority
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

DraftReply and SendApproval are EAO-owned authoritative state.

They must be shared across:

```text
Hermes-driven draft/read operations
+
trusted Open WebUI human approval interaction
+
provider send/reconciliation execution
```

Keeping this state only in an LLM conversation, Hermes session, SOUL/Skill, or Open WebUI message text would not provide deterministic authorization or restart-safe governance.

Writing directly into Open WebUI or Hermes internal databases would also create unsupported coupling and incorrectly turn those components into the authority for email governance state.

Therefore a single thin service is the minimum clean boundary.

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

The governance service should remain host-native for the reference blueprint unless later implementation evidence proves a container is materially simpler.

Reasons:

```text
current narrow provider adapter is Python/uv-oriented
no new container image/build lifecycle is required
Hermes can reach the service locally
Open WebUI can reach the service through an explicitly approved private host bridge
local SQLite persistence is sufficient for the single-host baseline
```

A non-macOS deployment may use the platform-native equivalent while preserving the same process/trust boundaries.

---

## 7. Hermes isolation boundary

The reference v2 email capability uses a separate Hermes employee Profile rather than extending the validated `general` Profile.

Conceptually:

```text
general
→ WeKnora only
→ existing v1 employee path

communication
→ WeKnora
→ EAO Email Governance MCP/tool surface
→ separate Profile credential/risk boundary
```

The communication Profile should use its own API credential and employee Assistant/resource grant.

Where the selected Hermes release supports a separate Profile API server process/port, the reference installation should prefer that isolated process for the communication Profile instead of making the v1 General Assistant startup depend on the email MCP/governance service.

If a deployment intentionally uses a shared/multiplexed Hermes listener, acceptance must prove that an unavailable or malformed email governance integration does not prevent the v1 `general` Profile from serving employee requests.

---

## 8. Open WebUI boundary

Open WebUI remains the employee Web surface and human identity source.

The reference v2 installation adds only:

```text
one restricted Communication Assistant/Model resource
one server-side trusted approval Action/Function or equivalent native extension
```

The approval UI adapter may receive authenticated Open WebUI user context and call the governance service through a protected server-side channel.

It must not become the Source of Truth for:

```text
DraftReply
SendApproval
logical send state
provider result
```

Do not write v2 governance records directly into Open WebUI's internal application tables.

The exact Action/Function code and trusted identity assertion mechanism are closed later under ID-4 and ID-5.

---

## 9. Hermes-facing operation surface

Hermes reaches the governance boundary through a narrow supported MCP/API surface rather than direct SQLite/provider access.

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
  send_approved_reply exists as a governed Named Action
```

Formal `approve_reply_draft` must originate from a deterministic trusted-human path, not from an ordinary model tool call inferred from chat text.

`send_approved_reply` is a governed runtime operation. It does not have to be exposed as an ordinary free-choice LLM tool when the trusted Open WebUI `Approve & Send` server-side action can invoke it directly after approval.

No generic provider mutation primitive is exposed.

---

## 10. Provider boundary

The governance service owns the narrow email-provider binding for configured pilot mailboxes.

Conceptually:

```text
Governance Service
├── read adapter  → provider-supported mailbox read surface
└── send adapter  → provider-supported outbound surface, Stage 4 only
```

For the current Tencent Enterprise Mail reference candidate:

```text
read candidate → IMAP over TLS
send candidate → SMTP over TLS
```

Protocol credentials remain inside the governance/provider runtime secret boundary and are never passed into Open WebUI, model prompts, WeKnora, or ordinary Hermes tool arguments.

The provider remains authoritative for source messages and actual delivery state.

---

## 11. Persistent state boundary

The single-host reference uses one small local SQLite database owned only by the governance service.

Reference persistent-state class:

```text
<runtime_root>/runtime/email-governance/state.sqlite3
```

The exact path may be overridden by company-private deployment configuration, but it must be outside the public repository and included in the applicable backup/restore contract.

The database stores only EAO-owned governance state such as:

```text
DraftReply
SendApproval
logical send execution/claim state
governance audit events
reconciliation state/provider references
```

It must not become a mailbox cache or customer database.

Normal inbound message bodies remain provider-backed operational context and are not bulk-persisted into the governance database.

DraftReply bodies are persisted because the exact outbound artifact being approved is EAO-owned state.

---

## 12. Logs and secrets

Technical logs and governance evidence remain distinct.

Reference classes:

```text
technical logs
→ <runtime_root>/logs/email-governance/ or platform service logs

governance state
→ governance SQLite database

provider/model/API secrets
→ protected secret storage defined by ID-2
```

No credentials, bearer tokens, mailbox passwords, or full unnecessary email bodies may be written to normal logs.

---

## 13. Network / trust paths

Required logical paths are:

```text
Employee browser
→ Open WebUI

Open WebUI
→ Hermes employee Profile API

Hermes communication Profile
→ WeKnora supported retrieval interface

Hermes communication Profile
→ EAO Email Governance private MCP/API endpoint

Open WebUI server-side approval Action
→ EAO Email Governance trusted action endpoint

EAO Email Governance
→ Email Provider over approved encrypted provider transport
```

Not allowed:

```text
Employee browser → governance service directly
Employee browser → provider credential
Hermes → governance SQLite directly
Open WebUI → governance SQLite directly
Governance service → WeKnora internal database
public Internet → governance service inbound
```

The exact host bind address, port, service authentication, and container-to-host route are installation details to close under ID-4/ID-5. Whatever mechanism is selected must remain on an approved private boundary and fail closed.

---

## 14. Startup and failure containment

The v1 path and v2 path must have independent failure containment.

Required behavior:

```text
WeKnora unavailable
→ v1/v2 grounded knowledge capability degraded according to existing behavior

communication Profile unavailable
→ v2 communication unavailable
→ v1 General Assistant remains available

governance service unavailable
→ email tools/actions fail closed
→ v1 General Assistant remains available

email provider unavailable
→ email operations fail/enter applicable reconciliation state
→ v1 General Assistant remains available

Open WebUI unavailable
→ employee Web entry unavailable as in v1
```

The governance service must not become a startup prerequisite for the validated `general` Profile.

Reference service ordering for v2 capability activation:

```text
v1 core healthy
→ governance service healthy
→ communication Profile healthy
→ Open WebUI Communication Assistant/action enabled
```

Disable/removal occurs in the reverse dependency order.

---

## 15. Stage activation model

The same topology is progressively activated rather than replaced between stages.

```text
Stage 0
  v1 only

Stage 1
  communication Profile + governance service
  provider read binding only

Stage 2
  DraftReply persistence enabled

Stage 3
  trusted approval Action + SendApproval persistence enabled
  provider send remains disabled

Stage 4
  governed provider send binding enabled

Stage 5
  optional Hermes Cron uses the same authorization/governance boundary

Stage 6
  optional messaging reuses the same Profile/governance operations
```

Do not create a temporary read architecture that must later be replaced by a different send architecture.

---

## 16. Removal / rollback boundary

The v2 capability must be removable without corrupting v1.

Minimum removal sequence:

```text
disable employee Communication Assistant/action
→ stop/disable communication Profile service
→ stop/disable governance service
→ revoke/remove email provider credentials
→ preserve or archive governance state according to company retention policy
→ verify General Assistant v1 path remains healthy
```

Externally sent email cannot be rolled back.

A lost or unavailable governance database must never cause the system to infer that approval existed; governed send fails closed.

Detailed backup/restore and recovery mechanics are completed under ID-7.

---

## 17. Explicitly rejected ID-1 alternatives

### Put all v2 email tools into `general`

Rejected for the reference baseline because it expands the validated v1 risk/credential/MCP boundary and weakens failure isolation.

### Store approvals only in chat/history

Rejected because conversation text is not deterministic authorization evidence.

### Store governance state directly in Open WebUI database

Rejected because Open WebUI is the employee client/identity surface, not the authority for EAO email governance state; direct internal DB coupling is also unsupported.

### Store governance state directly in Hermes internal/profile state database

Rejected because the state must be shared with a trusted human approval surface and must not depend on LLM/session semantics or Hermes internal schema.

### Add PostgreSQL/Redis for v2 governance

Rejected for the single-host baseline because the required state is small and transactional SQLite is sufficient. Revisit only if proven concurrency/HA requirements exceed it.

### Add n8n / workflow engine / event bus

Rejected because the frozen v2 workflow does not require them.

---

## 18. ID-1 acceptance contract

Installation Architecture is frozen when the blueprint establishes all of the following:

```text
[✓] validated v1 General Assistant path remains unchanged
[✓] v2 email capability has an isolated Hermes Profile boundary
[✓] one thin EAO Email Governance Service owns deterministic email governance state
[✓] no new broad platform/database/workflow system is introduced
[✓] Open WebUI remains employee identity/UX surface, not governance state authority
[✓] provider remains source of mailbox/delivery truth
[✓] governance SQLite stores only EAO-owned state
[✓] v2 capability failure/removal does not require v1 redesign
[✓] stage activation reuses one stable topology
[✓] real deployment remains independently gated
```

Result:

```text
ID-1: PASS
INSTALLATION ARCHITECTURE FROZEN
```
