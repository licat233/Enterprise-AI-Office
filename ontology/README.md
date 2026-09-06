# Enterprise Ontology Schema Experiments

Status: design-time experiments / non-runtime

This directory contains small machine-readable examples used to test the architecture contract in `docs/ONTOLOGY.md`.

These files are **not** production runtime configuration. They do not authorize a new Ontology service, graph database, CRM/ERP integration, write capability, or Agent tool.

## Purpose

The experiments answer a narrow question:

> Can the Enterprise Ontology Contract express a real business workflow clearly enough before Enterprise AI Office selects or builds any runtime?

The first experiment is deliberately small:

```text
Customer
   ↓ submits
Inquiry
   ↓ relates_to
Product
   ↓
Follow-up Action
```

See:

- `examples/sales-inquiry.yaml`

## Rules for experiments

1. Model only concepts required by the selected workflow.
2. Declare stable identity for every Object Type.
3. Declare Authority for every mutable operational property or relation.
4. Distinguish `source-backed`, `ontology-owned`, and `derived` state.
5. Prefer Named Actions over generic mutation primitives.
6. Represent deterministic preconditions with machine-readable reason codes.
7. Keep actor, approval, tool binding, expected effects, and audit expectations explicit.
8. Treat unresolved real-system bindings as unresolved; do not invent runtime IDs, credentials, APIs, or tools.
9. Keep authorization fail-closed.
10. Do not treat an example as an active company policy.

## Schema status

There is intentionally no frozen schema language yet.

YAML is being used because it is reviewable, Git-friendly, and sufficient for the first design experiment. Fields may change while the contract is being validated.

A formal schema, validator, code generator, database, or runtime should be introduced only if repeated real examples demonstrate that one is justified.

## Runtime boundary

Every current example must remain non-executable unless a later approved implementation decision defines:

```text
trusted actor identity propagation
real system/tool binding
authorization enforcement
Action Gate behavior
audit persistence
write-back/reconciliation
acceptance tests
capability closure
```

Until then, examples are design fixtures only.
