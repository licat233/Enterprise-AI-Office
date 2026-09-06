# Enterprise AI Office v2 — Communication Entry & Follow-up Design

Status: approved design / non-runtime
Version: 0.1.0
Date: 2026-09-06

This document completes the non-email portion of the Enterprise AI Office v2 `Communication & Follow-up` design.

It is intentionally conservative. v2 does not need a new employee portal, workflow engine, CRM, scheduler, or messaging stack to prove the milestone.

Use with:

- `docs/V2-SCOPE.md`
- `docs/V2-EMAIL-DESIGN.md`
- `docs/CLIENT-RBAC.md`
- existing Hermes Cron / Kanban / Gateway capability playbooks

---

## 1. Employee entry-point decision

The primary v2 employee surface remains:

```text
Open WebUI
```

v2 does not replace the working v1 employee client merely because a communication feature is being added.

One enterprise messaging platform may later be enabled as a convenience entry/delivery surface, but it is:

```text
optional
not a v2 blocker
not a second Agent runtime
not a second identity authority
not a reason to duplicate business logic
```

The same governed email operations must apply regardless of whether the request originates from Open WebUI or an approved messaging surface.

---

## 2. Messaging boundary

If one messaging platform is selected later, its role is limited to:

```text
employee identity / access signal where trustworthy
message delivery
Profile routing
notification / reminder delivery
```

It must not own:

```text
email authorization policy
email approval policy
email business objects
provider credentials
independent workflow state
```

No business rule should exist only in the messaging prompt or bot configuration.

---

## 3. Identity rule across channels

A governed operation must make the same authorization decision regardless of channel.

Conceptually:

```text
Open WebUI user
or
approved messaging identity
        ↓
trusted human identity
        ↓
permitted Assistant / Hermes Profile
        ↓
Ontology read/action policy
        ↓
provider/tool boundary
```

If a messaging identity cannot be deterministically mapped to an authorized human actor, the channel may still be used for low-risk notifications but must not be allowed to approve or execute governed external sends.

Channel identity is evidence only when the selected platform and deployment prove it reliably.

---

## 4. Follow-up design objective

The initial follow-up requirement is deliberately small:

> Help an employee remember or review communication that may need attention.

v2 does not attempt to build lead management, pipeline management, account history, opportunity scoring, or customer lifecycle management.

Those are CRM concerns.

---

## 5. Default automation primitive — Hermes Cron

For simple reminders and summaries, use Hermes Cron because it is already the system authority for scheduled Agent work.

Suitable v2 examples:

```text
weekday morning: summarize flagged/pending communication for an authorized role
remind an employee that a manually identified follow-up is due
weekly communication review summary
```

Cron owns schedule state. The email Ontology must not create a parallel scheduler.

The scheduled job may read authorized email context and produce a reminder/summary. It must not automatically send customer-facing email in the initial v2 milestone.

---

## 6. When Kanban is justified

Do not enable Kanban merely because follow-up sounds like a task.

Use Hermes Kanban only when the work item genuinely requires persistent multi-step Agent coordination such as:

```text
research customer request
→ gather technical evidence
→ wait for engineering response
→ draft customer reply
→ human review
→ complete
```

If the need is only:

```text
remind me tomorrow
```

Cron is sufficient.

This preserves the v1/v2 rule:

```text
simplest existing authority that completely satisfies the requirement
```

---

## 7. Follow-up state boundary

Do not create a shadow CRM table for v2.

State belongs to the smallest existing authority:

```text
email content / sent state       → email provider
schedule / reminder time         → Hermes Cron
persistent Agent work lifecycle  → Hermes Kanban when enabled
company/product facts            → WeKnora
email draft / approval evidence  → EAO governance/Ontology layer
```

A reminder may carry a stable reference to an email message or draft, but it does not copy the customer's full history into another database.

---

## 8. Automation permission boundary

Scheduled work does not inherit permission merely because a human originally created the schedule.

At execution time, a scheduled operation must still operate within its configured Profile/tool/credential scope.

The initial v2 automation surface should allow:

```text
read authorized communication context
summarize
classify for employee attention
create internal reminder output
deliver internal notification
```

It should not allow:

```text
autonomous customer-facing send
silent recipient changes
automatic mailbox mutation
bulk communication
authority escalation
```

No Cron or Kanban worker may bypass `send_approved_reply` approval rules.

---

## 9. Notification design

A follow-up notification should contain only enough information for the employee to understand and continue the work.

Prefer:

```text
source/message reference
short reason follow-up is due
safe summary
recommended next step
link/route back to the authorized employee surface when available
```

Avoid copying unnecessary full customer correspondence into multiple channels, logs, or scheduler state.

---

## 10. v2 rollout order after design freeze

Implementation, when explicitly authorized later, should proceed in this order:

```text
1. read-only email context
2. draft preparation
3. explicit approval evidence
4. governed send action
5. simple internal follow-up reminder/summary
6. optional one-platform messaging entry/delivery
7. Kanban only if a real multi-step use case proves necessary
```

This order prevents Messaging or automation from delaying the first useful email loop.

---

## 11. Explicitly deferred

The following remain outside the initial v2 design:

```text
CRM pipeline / lead objects
Calendar synchronization
automatic appointment creation
employee long-term memory
multi-channel inbox
omnichannel customer profile
n8n / another workflow engine
new event bus
multiple messaging platforms
autonomous outbound follow-up
customer scoring / sales forecasting
```

---

## 12. Design acceptance

This part of v2 is design-complete when:

```text
[ ] Open WebUI remains the primary employee surface
[ ] messaging is optional and limited to one selected platform
[ ] channel identity cannot bypass human authorization
[ ] Cron is the default scheduler
[ ] Kanban has an explicit complexity trigger
[ ] follow-up state does not create a shadow CRM
[ ] scheduled jobs cannot bypass send approval
[ ] customer-facing autonomous communication remains out of scope
[ ] rollout order keeps email loop ahead of optional convenience features
```
