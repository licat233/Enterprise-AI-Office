# Enterprise Ontology Schema Experiments

Status: design-time experiments / research phase closed / non-runtime

This directory contains small machine-readable examples used to test the architecture contract in `docs/ONTOLOGY.md`.

These files are **not** production runtime configuration. They do not authorize a new Ontology service, graph database, CRM/ERP/CMS integration, write capability, or Agent tool.

## Current phase status

The initial Ontology research/model-validation phase is complete.

Current retained outputs are:

```text
docs/ONTOLOGY-RESEARCH.md          research findings
docs/ONTOLOGY.md                   Enterprise Ontology Contract v0.3.0
ontology/examples/sales-inquiry.yaml
ontology/examples/content-publication.yaml
scripts/validate-ontology.py       structural validator
```

The two experiments already demonstrated two concrete contract corrections:

1. read/traversal authorization must close over the full data path, not only the entry-point object;
2. approval for a mutable subject must bind to the exact version/state it authorizes and must be revalidated before the governed side effect executes.

The experiments also produced repeated mechanical schema-drift defects, which justified the lightweight structural validator.

There is currently no demonstrated requirement for:

```text
an Ontology Runtime
a graph database
a reasoning engine
a third speculative domain example
a generic CRM/ERP/CMS adapter
a new Agent platform
```

Do not continue expanding Ontology merely for conceptual completeness.

## Reactivation trigger

Resume Ontology implementation work only when a real Enterprise AI Office capability creates an operational requirement that the current stack cannot safely express or enforce by itself.

The primary trigger is a real integration that allows an Agent to change external business state, for example through:

```text
CRM
ERP
PIM
CMS
email / customer communication
social publishing
another operational business system
```

A read-only integration does not automatically require an Ontology Runtime. It may still justify contract work when cross-system Object visibility, traversal authorization, or business semantics cannot be safely preserved by the upstream system plus existing Enterprise AI Office RBAC/Profile boundaries.

When a trigger exists, do not start by selecting a graph database or building a runtime. First close the integration through the existing repository architecture process:

```text
real business requirement
→ inspect the exact upstream system and supported API/MCP/action model
→ declare company deployment intent
→ register/extend the capability in config/capabilities.yaml
→ identify Objects / Relations / Authority / Visibility / Reads / Actions actually required
→ define trusted actor/credential/tool boundaries
→ define acceptance tests and deployment-state evidence
→ decide whether upstream enforcement is sufficient
→ use a thin deterministic gate only if needed
→ introduce a larger Ontology/runtime component only if the prior options are insufficient
```

Do not create a generic placeholder `operational_integration` capability just to reserve architecture for the future. Add a capability only when a concrete integration is actually selected.

## Purpose

The experiments answer a narrow question:

> Can the Enterprise Ontology Contract express real business workflows clearly enough before Enterprise AI Office selects or builds any runtime?

Current experiments:

### Sales Inquiry

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

Main finding:

> read/traversal authorization must close over the full data path, not only the entry-point object.

### Content Publication

```text
ContentItem
   ↓ has_review
ReviewDecision
   ↓ authorizes exact revision/hash
Publish Action
   ↓
PublicationRecord
```

See:

- `examples/content-publication.yaml`

Main finding:

> approval for a mutable subject must bind to the exact version/state it authorizes and must be revalidated before the governed side effect executes.

The second experiment also exposed a dangling reference in an idempotency expression during manual review. Combined with the authorization-closure mistake found in the first experiment, this provided concrete evidence for a lightweight structural validator.

## Rules for experiments

1. Model only concepts required by the selected workflow.
2. Declare stable identity for every Object Type.
3. Declare Authority for every mutable operational property or relation.
4. Distinguish `source-backed`, `ontology-owned`, and `derived` state.
5. Keep operational Object visibility fail-closed unless a broader policy is explicitly justified.
6. Model named Read Operations when query semantics or cross-object authorization matter.
7. Close authorization over every Object, Relation, and Property actually read or traversed.
8. Prefer Named Actions over generic mutation primitives.
9. Represent deterministic preconditions with machine-readable reason codes.
10. Keep actor, approval, tool binding, expected effects, and audit expectations explicit.
11. Bind approval to exact subject evidence when a mutable subject can change after review.
12. Treat unresolved real-system bindings as unresolved; do not invent runtime IDs, credentials, APIs, or tools.
13. Keep authorization fail-closed.
14. Do not treat an example as an active company policy.

## Structural validator

The repository includes:

```text
scripts/validate-ontology.py
```

Run from the repository root:

```sh
uv run scripts/validate-ontology.py
```

The validator exists because repeated design experiments produced mechanical consistency defects that were otherwise found only during manual review.

Its scope is deliberately narrow:

```text
duplicate YAML keys
unknown Object/Property/Relation/system references
invalid Authority references
fail-open Object visibility in design examples
Read Operation authorization-closure defects
Action precondition references
approval binding references
unknown tool-binding system namespaces
idempotency expressions using undeclared action parameters
operation-surface references
```

A validator PASS means only that the YAML is structurally self-consistent according to the implemented checks.

It does **not** mean:

```text
the business policy is correct
the integration exists
the actor is really authorized
the Action is executable
the deployment is Production Ready
```

Business policy correctness remains a domain/human review responsibility.

## Schema status

There is intentionally no fully frozen schema language yet.

YAML is being used because it is reviewable, Git-friendly, and sufficient for the current design experiments. The validator is intentionally tolerant of optional fields and should grow only when another real example exposes a recurring mechanical defect.

Do not turn the validator into an Ontology Runtime, policy engine, database, code generator, or speculative schema framework.

## Runtime boundary

Every current example must remain non-executable unless a later approved implementation decision defines:

```text
trusted actor identity propagation
real system/tool binding
authorization enforcement
Action Gate behavior
approval evidence/validation behavior
audit persistence
write-back/reconciliation
acceptance tests
capability closure
```

Until then, examples are design fixtures only.
