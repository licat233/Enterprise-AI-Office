# Deployment Completeness Contract

This document defines what it means for an AI engineering agent to finish an Enterprise AI Office deployment.

The word "complete" is configuration-relative. A deployment is not complete because every feature in the repository was installed, and it is not complete because the core chat path happens to work. It is complete when the baseline works and every capability explicitly enabled by the adopting company's configuration has been deployed, secured, validated, and recorded.

## 1. Completion levels

### CORE READY

The baseline employee workflow works:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes `general` Profile
→ WeKnora
→ grounded answer + source
```

Core Ready is a functional milestone. It does not prove that every company-configured capability is present and does not imply production readiness.

### CONFIGURED READY

`CONFIGURED READY` requires:

1. `CORE READY` is still PASS;
2. every capability enabled by the company configuration has a closed implementation path;
3. every enabled capability passes its applicable acceptance test;
4. no enabled capability is left as `TODO`, `not configured`, or an undocumented manual follow-up;
5. the actual enabled/disabled capability set is recorded in `state/DEPLOYMENT-STATE.md`.

An optional capability that is disabled does not block Configured Ready.

An enabled capability whose required credential, external approval, provider choice, or security decision is genuinely unavailable produces `BLOCKED — REQUIRED INPUT`; the agent must not silently disable it merely to reach a green status.

### PRODUCTION READY

`PRODUCTION READY` requires:

1. `CONFIGURED READY` is PASS;
2. production backup/recovery requirements are implemented and tested;
3. production secrets, access, and network exposure are reviewed;
4. startup/recovery behavior is known and supported;
5. production operational ownership/health procedures are in place;
6. representative production knowledge and security tests pass.

Production Ready is therefore a superset of Configured Ready, not a synonym for "services are running".

## 2. Target readiness is an input

The company deployment configuration must declare the intended target:

```yaml
deployment:
  target_readiness: configured-ready
```

Allowed values:

```text
core-ready
configured-ready
production-ready
```

An AI deployment agent must continue until the requested target is reached, blocked on genuine required input, or fails at a specific boundary.

It must not stop at `CORE READY` when the requested target is `configured-ready` or `production-ready`.

## 3. Capability closure

Before mutation, read `config/capabilities.yaml` and the adopting company's configuration.

Build a capability closure table:

| Capability | Requested | Implementation path | Required input resolved | Acceptance | Final state |
| --- | --- | --- | --- | --- | --- |
| core employee path | yes | core adapters | yes/no | pass/fail | enabled |
| specialist Profiles | config-derived | Profile standard/templates | yes/no | pass/fail/N/A | ... |
| hermes-webui | true/false | capability registry path | yes/no | pass/fail/N/A | ... |
| coding delegation | true/false | capability registry path | yes/no | pass/fail/N/A | ... |
| Kanban | true/false | capability registry path | yes/no | pass/fail/N/A | ... |
| Cron | true/false | capability registry path | yes/no | pass/fail/N/A | ... |
| messaging | true/false | capability registry path | yes/no | pass/fail/N/A | ... |
| remote access | true/false | capability registry path | yes/no | pass/fail/N/A | ... |
| SSO | true/false | capability registry path | yes/no | pass/fail/N/A | ... |
| employee long-term memory | true/false | capability registry path | yes/no | pass/fail/N/A | ... |

The exact rows come from `config/capabilities.yaml`; do not invent company requirements from this example table.

## 4. No silent downgrade

If the company configuration says a capability is enabled, the deployment agent may not silently:

- omit it;
- replace it with an unrelated feature;
- mark it "later";
- disable it to simplify deployment;
- declare completion while its acceptance remains unresolved.

If the capability cannot safely be implemented with the selected versions or required external data is missing, report the specific blocker.

## 5. No feature collection

The inverse rule is equally important: do not enable a capability merely because a template or playbook exists.

The repository provides a capability library. The company configuration selects from it.

```text
repository capability library
        +
company configuration
        ↓
actual deployment target
```

## 6. Implementation-path requirement

A capability is deployable from this repository only when the capability registry points to all of the following that apply:

- upstream/component responsibility;
- deployment/configuration playbook or adapter;
- required protected inputs;
- security boundary;
- acceptance test;
- state fields that must be recorded.

If an enabled capability lacks that closure, the repository itself has a deployability defect. The agent should report the gap rather than improvising a new architecture.

## 7. Version-specific behavior

The validated stack in `config/validated-stack.yaml` is the reproducibility baseline for the core path.

Optional capabilities that were not part of the first validated deployment must be checked against the exact selected upstream version before activation. Use official upstream capability first, pin the resolved version/commit where practical, and record it in deployment state.

Do not claim an unvalidated optional component is part of the validated core stack merely because this repository contains a playbook for it.

## 8. Evidence over intention

Completion is based on observed behavior, not configuration files alone.

Examples:

- a configured Open WebUI group is not enough; an employee account must see the correct assistants;
- an MCP stanza is not enough; Hermes must retrieve a real source;
- a Cron entry is not enough; the harmless acceptance job must actually run;
- a Kanban board is not enough; a worker lifecycle must execute;
- a coding-agent binary is not enough; delegation must modify/verify a disposable repository;
- backup files are not enough; an isolated restore must work for Production Ready.

## 9. Final statuses

A deployment agent should report one of:

```text
CORE READY
CONFIGURED READY
PRODUCTION READY
BLOCKED — REQUIRED INPUT: <specific missing authority/input>
FAIL — <specific failed boundary>
```

Never use the vague word `complete` without also naming the achieved readiness level.
