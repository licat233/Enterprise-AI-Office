---
name: Capability / architecture change request
about: Propose a new capability or a material architecture/integration change
title: "[Capability] "
---

> Start with reuse. Do not propose a new service, database, scheduler, agent framework, browser stack, memory layer, MCP server, or external integration until the Capability Reuse Pass below is complete.

## Business requirement

What real user/company need is not satisfied today?

## Capability Reuse Pass

For each layer, record what you checked and why it is insufficient:

- [ ] existing Enterprise AI Office capability
- [ ] Hermes native capability
- [ ] installed/frozen Skills
- [ ] Open WebUI native capability
- [ ] WeKnora native capability
- [ ] existing Email/governance/integration module where relevant
- [ ] official upstream integration
- [ ] thin adapter possibility

Reference `docs/CAPABILITY-REUSE-PASS.md`.

## Exact gap

State the smallest verified gap after the reuse pass. "Easier", "popular", "we may need it later", or "the host has enough resources" is not a gap.

## Smallest proposed change

Describe the minimal addition. Prefer configuration/reconciliation around existing authority rather than a new source of truth.

## New authority or durable state

Will this change create or duplicate any durable authority/state?

Examples:

- knowledge store
- employee identity/RBAC
- Agent memory
- scheduler/work queue
- message/email state
- deployment/runtime state
- secret store

If yes, explain ownership and why the existing authority cannot be reused.

## Security / side effects

Describe:

- credentials required;
- employee/admin exposure;
- network exposure;
- external side effects;
- least-privilege boundary;
- fail-closed behavior.

Do not include secret values.

## Maintenance cost

What new upgrades, backups, monitoring, migrations, or operator knowledge will this introduce?

## Rollback / degradation path

How can the capability be disabled or rolled back without breaking Core?

## Acceptance evidence

What deterministic tests prove the capability is complete?

Include runtime path, negative tests, restart/recovery behavior, and user-facing acceptance where applicable.

## Generic EAO or reference-specific?

- [ ] reusable generic capability
- [ ] ARMOR/reference-specific capability
- [ ] not yet determined

If reference-specific, do not add a generic company-schema field unless another deployment explicitly adopts it.
