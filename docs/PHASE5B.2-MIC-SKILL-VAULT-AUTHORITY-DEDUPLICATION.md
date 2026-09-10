# Enterprise AI Office — Phase 5B.2

## MIC Skill / Vault Authority De-duplication

Date: 2026-09-10

This is an audit record for the narrow authority de-duplication correction. It
does not define a second MIC SOP.

## Resulting ownership

| Location | Role |
|---|---|
| `${ARMOR_VAULT_ROOT}/02-Projects/Workspaces/Products/MIC-Products/ARMOR-MIC-Product-Optimization-Standard-v1.0.md` | `CANONICAL` detailed MIC business standard |
| `skills/shared/department/armor-mic-product-optimization/SKILL.md` | `EXECUTION_ADAPTER` for Hermes invocation, lookup, gates, bindings, and fail-closed boundaries |

The Vault Standard owns the detailed fact authority hierarchy, MIC field and
BulkFill rules, audit requirements, blockers, approval rules, and artifact
semantics. The Skill resolves that file through `$ARMOR_VAULT_ROOT` and does
not embed a fallback copy of the detailed SOP.

## Preserved boundaries

The corrected technical source hierarchy remains in the Vault Standard:

```text
authoritative original Datasheet / Manual / test / certification document
→ canonical or verified Product Knowledge derived from those sources
→ WeKnora as retrieval layer only
→ current MIC listing as existing-state evidence
```

`save_mic_product_package`, the MIC artifact contract, Router destination,
Operations permissions, approval gate, and no-live-edit/publication boundary
are unchanged.

## Validation

Phase 5B.1 authority tests now inspect the Vault Standard for detailed source
precedence. Phase 5B.2 tests verify the Skill's adapter role, non-identical and
smaller content, canonical Standard lookup, fail-closed missing-source
behavior, and deployed Skill symlink resolution.
