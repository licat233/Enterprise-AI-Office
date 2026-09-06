# Enterprise AI Office v2 — Communication & Follow-up Scope

Status: approved scope / implementation not yet complete
Version: 0.1.0
Date: 2026-09-06

This document defines the deliberately narrow scope for Enterprise AI Office v2.

v2 exists to move the system from a primarily knowledge-grounded employee assistant toward the first governed operational work loop, without turning the project into a broad enterprise-integration program.

The v1 baseline remains valid. v2 extends it; it does not replace or destabilize the validated core architecture.

---

## 1. v2 theme

v1 primarily proves:

```text
Ask AI
→ retrieve company knowledge
→ grounded answer
```

v2 should prove:

```text
Work with AI
→ retrieve context
→ prepare a real business action
→ human review/approval
→ execute through a narrow integration
→ preserve follow-up/audit state
```

The v2 theme is therefore:

> **Communication & Follow-up**

---

## 2. Primary outcome

The first v2 operational loop should support one realistic employee workflow such as:

```text
Employee
   ↓
Open WebUI or one approved enterprise messaging surface
   ↓
Hermes specialist Profile
   ↓
retrieve company knowledge from WeKnora
   ↓
read relevant communication context
   ↓
draft a response
   ↓
human reviews the final content
   ↓
explicit approval
   ↓
send through the selected email system
   ↓
record the result / follow-up state
   ↓
optional reminder through Hermes Cron
```

The system does not need a CRM to prove this loop.

---

## 3. In scope

v2 may add only the following capability classes.

### 3.1 Email integration — primary v2 capability

Email is the only new external business-system type approved for the initial v2 implementation.

The selected integration should support the minimum useful operation surface:

```text
search/read relevant messages or threads
get one thread/message
prepare a draft reply
send only through an approved Named Action
return the authoritative provider result/reference
```

The exact provider is not selected by this document.

Before implementation, the adopting company must identify the real email system and authorize the required account/application access. Do not invent Gmail, Microsoft 365, IMAP/SMTP, or another provider merely to continue implementation.

### 3.2 One enterprise messaging surface — optional v2 employee entry point

v2 may enable exactly one company-selected messaging platform through the existing Hermes Gateway capability.

Do not enable multiple messaging ecosystems in the same v2 milestone merely because Hermes supports them.

Messaging is an access/delivery surface, not a second business-system integration project.

### 3.3 Follow-up automation using existing Hermes capabilities

v2 may use existing Hermes Cron and, where justified, Kanban for narrow follow-up workflows such as:

```text
remind an authorized employee that a follow-up is due
produce a daily/weekly follow-up summary
schedule a department-owned recurring review
track a persistent multi-step work item when Kanban is genuinely useful
```

Do not introduce n8n, another workflow engine, or a second scheduler for v2.

### 3.4 Ontology governance for the real operational loop

The Enterprise Ontology Contract in `docs/ONTOLOGY.md` becomes applicable when the selected email integration exposes governed reads or writes.

Use it to model only the objects and operations required by the real v2 workflow, for example:

```text
EmailThread
EmailMessage
DraftReply
FollowUp
```

and operations such as:

```text
search_email
read_thread
draft_reply
send_reply
schedule_follow_up
```

Do not create a general-purpose Ontology Runtime merely because v2 uses the contract.

---

## 4. Explicitly out of scope for v2

The following are not part of the initial v2 milestone:

```text
CRM
ERP
PIM
Calendar integration
employee long-term memory re-enable
SSO expansion unless independently required for production access
armor-memory synchronization
n8n or another workflow platform
additional vector database
Prometheus/Grafana observability stack
local-LLM infrastructure project
custom Agent framework
graph database / generic Ontology Runtime
multiple new messaging platforms
multiple new external business systems
```

A real blocking requirement may justify a separate architecture decision, but these items must not be absorbed into v2 merely because implementation work has started.

---

## 5. Scope-control rules

v2 follows these hard scope limits.

1. **One new external business-system type:** email.
2. **At most one new employee messaging surface** in the milestone.
3. **No new workflow engine:** use Hermes Cron/Kanban where sufficient.
4. **Human-in-the-loop by default for externally visible writes.**
5. **No autonomous customer-facing send in the initial v2 milestone.**
6. **No generic write primitive exposed to ordinary Agents.**
7. **No provider assumption before the real company system is selected.**
8. **No attempt to model every department or business object.**
9. **A requirement that materially expands infrastructure or trust boundaries moves to a later milestone unless it is necessary to complete the single v2 operational loop.**

---

## 6. v2 implementation sequence

### Stage A — Select the real email system and authority boundary

Resolve:

```text
provider/system
account ownership
human vs service identity
supported official API/MCP/action surface
read scope
send scope
credential model
provider-native audit/history
```

If these are unknown, report:

```text
BLOCKED — REQUIRED INPUT: email system / authorization
```

Do not design against an imaginary provider.

### Stage B — Read-only communication path

First prove the least-risk path:

```text
Hermes authorized Profile
→ provider-supported read interface
→ search/read a bounded mailbox/thread scope
→ return communication context without mutation
```

Acceptance must verify real authorization boundaries, not only successful API calls.

### Stage C — Draft preparation

Allow the Agent to prepare a response while keeping the draft non-sent.

A draft may be represented in provider-native draft state or another explicitly approved state model. The source of truth must be clear.

### Stage D — Governed send Action

Before the first real send capability is enabled:

- define the relevant Ontology objects/reads/actions;
- define trusted actor propagation;
- define the final-content approval binding;
- define provider/tool binding;
- define idempotency/failure behavior;
- define audit evidence;
- add acceptance tests.

The minimum rule is:

> the exact final message content being sent must be known to and explicitly approved by the authorized human actor.

### Stage E — One messaging entry point

If the company has selected a Hermes-supported messaging platform, enable only that platform and validate:

```text
identity/allowlist
Profile routing
message delivery
no privilege expansion
```

This stage may proceed after the email operational boundary is understood; it must not delay the core email loop if the messaging credentials are unavailable.

### Stage F — Narrow follow-up automation

Use Hermes Cron/Kanban only after the communication loop works manually.

Automation should begin with reminders or summaries rather than autonomous external communication.

---

## 7. Security and authority model

v2 must preserve the existing layered boundary:

```text
Human identity / RBAC
+
Hermes Profile capability
+
Ontology Object/Read/Action policy where applicable
+
provider-native authorization
```

No layer should be treated as a substitute for the others.

Specifically:

- a Profile API key is not proof of end-user identity;
- natural-language instructions are not authorization;
- UI visibility is not backend enforcement;
- provider credentials must be least-privilege;
- externally visible sends require a governed action path;
- provider-native logs remain authoritative evidence of provider execution;
- Enterprise AI Office audit should link its decision to the provider result rather than duplicate the entire mailbox.

---

## 8. Capability-closure rule

Do not add a generic placeholder `operational_integration` capability.

Once the real email provider/system is selected, add or extend a concrete conditional capability in `config/capabilities.yaml` with:

```text
business purpose
selected upstream/provider integration
required protected inputs
identity/credential boundary
read/write scope
Ontology contract path where applicable
implementation playbook/adapter
acceptance tests
state/audit evidence
rollback/removal path
```

The capability remains disabled for deployments that do not select it.

Messaging, Cron, and Kanban should continue to use their existing capability entries rather than creating v2-specific duplicates.

---

## 9. v2 acceptance boundary

The v2 milestone is complete only when one real communication/follow-up loop has been demonstrated with evidence.

Minimum acceptance:

```text
[ ] v1 baseline remains healthy
[ ] real email provider/system is explicitly selected and recorded
[ ] least-privilege credentials/identity boundary is documented
[ ] authorized Profile can read only approved communication scope
[ ] unauthorized read path fails closed
[ ] Agent can prepare a useful draft using communication context + WeKnora evidence
[ ] final outbound content requires explicit human approval
[ ] send occurs through a narrow Named Action / provider binding
[ ] stale or changed content cannot reuse prior approval
[ ] duplicate/retry behavior is understood and tested
[ ] provider result/reference is captured
[ ] relevant business Action decision is auditable
[ ] no generic arbitrary-send/write primitive is exposed
[ ] optional messaging surface, if enabled, passes identity/routing tests
[ ] follow-up automation, if enabled, begins with reminders/summaries rather than autonomous customer sends
[ ] actual enabled capability state is recorded
```

A v2 deployment does not need CRM, Calendar, employee long-term memory, SSO expansion, local models, or additional infrastructure to satisfy this milestone.

---

## 10. Stop conditions

Stop adding scope and defer to a later milestone when a request requires any of the following without being essential to the single communication loop:

```text
a second external business system
company-wide workflow redesign
ERP/CRM master-data synchronization
new graph/reasoning infrastructure
new multi-system event bus
new workflow platform
new employee-memory subsystem
large observability platform
multiple messaging providers
broad autonomous external actions
```

Prefer a clean v2 completion over a theoretically complete enterprise platform.

---

## 11. Likely post-v2 candidates

After v2 is stable in real employee use, evaluate based on observed demand rather than sequence alone.

Likely candidates include:

```text
Calendar
employee long-term memory
CRM / Inquiry workflow
```

They are not commitments.

The next version should be selected from actual v2 usage evidence.

---

## 12. v2 definition in one sentence

> **Enterprise AI Office v2 adds one safe, human-approved communication and follow-up operational loop on top of the stable v1 knowledge/agent foundation, while deliberately refusing broader enterprise-system expansion.**
