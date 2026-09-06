# Enterprise AI Office v2 — Design / Prototype Status

Status: design stage / implementation not authorized / runtime not activated
Version: 0.4.0
Date: 2026-09-06

This document records the current repository-level status of the frozen v2 design and its non-runtime prototype artifacts.

It is not deployment runtime evidence and does not authorize access to any real mailbox, credential, Hermes Profile, IMAP/SMTP runtime, messaging platform, Cron/Kanban job, or customer-facing action.

## 1. Current phase boundary

Enterprise AI Office v2 is currently in the **design stage**.

The v2 design is frozen in `docs/V2-DESIGN-REVIEW.md`. `docs/V2-IMPLEMENTATION-PLAN.md` is a future implementation blueprint only and explicitly remains:

```text
implementation not authorized
```

Repository adapters, examples, tests, acceptance contracts, and provider playbooks created during design are design-support/prototype artifacts. Their presence must not be interpreted as a request to activate a real provider.

Current rule:

```text
design / research / prototype / offline validation
→ allowed

real credentials / mailbox access / Profile binding / IMAP or SMTP runtime
→ not authorized
```

## 2. v1 baseline context

`state/DEPLOYMENT-STATE.md` records that the first validated local reference deployment previously passed the core employee workflow, grounded retrieval, RBAC, Profile credential isolation, dangerous-tool denial, employee-client acceptance, and isolated backup/restore checks.

Known existing limitation:

```text
OrbStack was not automatically available at the first post-reboot probe.
```

This historical v1 reference evidence is context only. It is not evidence that any v2 capability is deployed.

## 3. v2 email design target

Selected provider for the ARMOR reference design:

```text
Tencent Enterprise Mail
```

The frozen Stage 1 conceptual read surface is:

```text
search_email
get_email
```

The design requires:

```text
configured mailbox only
allowlisted folder scope
read-only mailbox access
non-Seen body reads where supported
bounded result/body sizes
no attachment download initially
no arbitrary IMAP command
no SMTP in Stage 1
```

## 4. Design-support repository artifacts

Current repository artifacts include:

```text
docs/V2-EMAIL-DESIGN.md
docs/V2-DESIGN-REVIEW.md
docs/V2-IMPLEMENTATION-PLAN.md
docs/ONTOLOGY.md
ontology/examples/email-communication.yaml
infrastructure/email/tencent-exmail/README.md
infrastructure/email/tencent-exmail/imap_readonly_mcp.py
infrastructure/email/tencent-exmail/imap.env.example
infrastructure/email/tencent-exmail/hermes.mcp.example.yaml
infrastructure/email/tencent-exmail/test_imap_readonly.py
docs/acceptance/TENCENT-EXMAIL.md
config/capabilities.yaml
```

The read-only adapter and Hermes template are **implementation candidates**, not active runtime configuration and not normative architecture authority.

At actual implementation time, upstream behavior must be re-checked and a more mature supported integration should replace the prototype if it satisfies the frozen design with less custom code.

## 5. Offline design/prototype verification evidence

Offline verification was executed on 2026-09-06 without connecting a real mailbox.

### 5.1 Ontology structural validation

Result:

```text
PASS — email-communication Ontology structural validation
```

This is design-time structural validation only.

### 5.2 Read-only adapter logic tests

The repository test suite contains five deterministic safety tests.

The execution environment had `uv` but did not have `mcp>=2,<3` in its offline package cache. To separate dependency resolution from adapter logic, the adapter/test logic was executed with only the MCP registration/decorator layer replaced by a local no-op stub.

Result:

```text
5 tests run
5 PASS
0 FAIL
```

Covered design properties:

```text
folder scope fails closed
mailbox select requests readonly=True
search path uses UID SEARCH/FETCH only
message body fetch uses BODY.PEEK
no send/delete/move/flag/generic SMTP tool is exposed
```

Canonical command status:

```text
uv run infrastructure/email/tencent-exmail/test_imap_readonly.py
→ not executed to completion in that environment
→ missing offline mcp package cache
```

This evidence validates the prototype logic, not a deployed provider integration.

### 5.3 Repository readiness semantics

A connector-backed mirror of the current GitHub tree/contract markers produced:

```text
86 PASS
0 FAIL
```

This is a static repository-closure check only and does not imply implementation authorization.

## 6. Current design status

```text
V2 PHASE: DESIGN
DESIGN REVIEW: PASS / FROZEN
PROVIDER RESEARCH: COMPLETE FOR CURRENT DESIGN
EMAIL ONTOLOGY FIXTURE: PRESENT / DESIGN-ONLY
READ-ONLY ADAPTER: PROTOTYPE PRESENT
OFFLINE LOGIC CHECKS: PASS WITH ENVIRONMENT CAVEAT
REAL MAILBOX ACCESS: NOT AUTHORIZED
REAL PROVIDER RUNTIME: NOT STARTED
HERMES PROFILE BINDING: NOT STARTED
SMTP / CUSTOMER SEND: NOT IMPLEMENTED OR AUTHORIZED
```

## 7. What does not require mailbox authorization now

The following remain valid design-stage work and require no real mailbox credential:

```text
architecture review
Ontology/schema refinement driven by a real design defect
security/threat modeling
human-approval design
identity/authorization design
failure/reconciliation design
acceptance-test design
provider documentation research
offline prototype/unit tests
implementation-stage decomposition
scope and non-goal review
```

Do not ask the company to generate a mailbox client password merely to continue design.

## 8. Future implementation gate

Real implementation starts only when the company explicitly opens a deployment/implementation task.

Only then may the implementation process resolve protected inputs such as:

```text
pilot mailbox authorization
client credential / client-specific password
protected secret location
authorized human identity/group
authorized Hermes Profile
actual runtime host access
harmless known test message(s)
```

Until that future gate is explicitly opened, these are **deferred implementation inputs**, not current blockers.

## 9. Future staged implementation order

The future implementation blueprint remains:

```text
Stage 0  preserve/verify v1 baseline
Stage 1  bounded read-only email
Stage 2  DraftReply preparation
Stage 3  trusted human approval evidence
Stage 4  governed send_approved_reply
Stage 5  optional simple follow-up
Stage 6  optional one messaging surface
```

This sequence is a planning artifact. The project is not currently executing Stage 1 against a real provider.

## 10. Current conclusion

```text
V2 DESIGN: ACTIVE / FROZEN CORE DIRECTION
DESIGN-SUPPORT PROTOTYPES: AVAILABLE
IMPLEMENTATION: NOT AUTHORIZED
RUNTIME PROVIDER ACCESS: NOT REQUIRED NOW
```
