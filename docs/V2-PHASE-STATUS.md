# Enterprise AI Office v2 — Phase Status

Status: design stage / implementation not authorized / runtime not activated
Version: 1.0.0
Date: 2026-09-06

The authoritative machine-readable phase state is:

```text
state/PROJECT-PHASE.yaml
```

This document explains that state for humans. If this prose ever conflicts with `state/PROJECT-PHASE.yaml`, the phase file wins until an explicit human-authorized phase transition updates both.

## 1. Current phase

```text
V2 PHASE: DESIGN
IMPLEMENTATION: NOT AUTHORIZED
DEPLOYMENT: NOT AUTHORIZED
REAL PROVIDER ACCESS: NOT AUTHORIZED
```

The frozen v2 design may include documentation, provider research, Ontology fixtures, sanitized examples, offline prototypes, unit tests, structural validators, acceptance-test designs, and future implementation plans.

Their presence does **not** mean the system is being implemented or deployed.

## 2. Phase interpretation rule

Agents must not infer a phase transition from:

```text
prototype code existing
adapter code existing
tests passing
implementation plan existing
acceptance document existing
previous assistant momentum
phrases such as “continue”, “start”, “next”, “继续”, “开始吧”, or “下一步”
```

Those phrases mean **continue work inside the current phase** unless the human explicitly authorizes a new phase.

Examples of phase-changing intent are recorded in `state/PROJECT-PHASE.yaml`.

## 3. Work allowed now

Current design-stage work includes:

```text
architecture and product design
scope/non-goal decisions
security and threat modeling
human approval / identity design
Ontology/schema refinement
provider/upstream research
sanitized examples
synthetic fixtures
offline prototypes
offline tests/static validation
future implementation decomposition
acceptance-test design
```

## 4. Work not allowed now

During the current design phase, do not:

```text
request or use real credentials merely to continue design
connect a real mailbox or external business system
bind real employees/accounts/Profiles/provider identities
perform real IMAP/SMTP runtime work
mutate the production/live Enterprise AI Office deployment
perform customer-facing sends
mark a prototype as a deployed capability
advance into a future implementation stage because its plan exists
```

Missing runtime credentials are therefore **not blockers** in the design phase; they are deferred implementation inputs.

## 5. v1 baseline context

The existing v1 deployment and its acceptance evidence remain historical/reference context. They do not authorize v2 runtime mutation.

## 6. v2 email design target

Selected reference provider:

```text
Tencent Enterprise Mail
```

Frozen Stage 1 conceptual read surface:

```text
search_email
get_email
```

Design properties:

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

The repository's read-only adapter, Hermes registration example, environment template, deterministic tests, provider playbook, and acceptance contract are design-support prototypes/artifacts only.

## 7. Offline prototype evidence

Offline design/prototype validation was performed without connecting a real mailbox.

Recorded results:

```text
email Ontology structural validation: PASS
read-only adapter safety logic: 5/5 PASS with dependency-environment caveat
repository static closure mirror: 86 PASS / 0 FAIL at the recorded check
```

These results validate design/prototype properties only. They are not provider runtime evidence and do not authorize implementation.

## 8. Future implementation plan

`docs/V2-IMPLEMENTATION-PLAN.md` is a future blueprint only.

Its sequence remains:

```text
Stage 0  preserve/verify v1 baseline
Stage 1  bounded read-only email
Stage 2  DraftReply preparation
Stage 3  trusted human approval evidence
Stage 4  governed send_approved_reply
Stage 5  optional simple follow-up
Stage 6  optional one messaging surface
```

The sequence becomes executable only after the human explicitly changes the project phase to implementation/deployment.

## 9. Transition authority

Only an explicit human instruction may change the phase.

When that happens:

1. update `state/PROJECT-PHASE.yaml` first;
2. update this document to match;
3. then apply the implementation/deployment contracts relevant to the newly authorized phase.

Until then:

```text
DESIGN CONTINUES
IMPLEMENTATION DOES NOT START
REAL RUNTIME ACCESS IS OUT OF SCOPE
```
