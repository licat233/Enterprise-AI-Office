---
name: armor-mic-product-optimization
description: >
  Enterprise Hermes execution adapter for ARMOR Made-in-China.com product
  information optimization. It loads the canonical MIC Vault Standard,
  orchestrates the reviewed workflow, and binds the scoped save operation.
license: MIT
metadata:
  hermes:
    tags: [armor, mic, product, bulkfill, listing, audit, detail-page]
    pipeline_version: "1.0"
---

# ARMOR MIC Product Information Optimization

This Skill applies when preparing, auditing, or saving ARMOR MIC product
information. It is an Enterprise Hermes execution adapter, not a second copy
of the MIC business SOP. The detailed rules, field standards, authority
hierarchy, artifact semantics, and blockers live in the canonical Vault
Standard below.

## Canonical Vault Standard

Resolve and read the exact current standard through the runtime Vault root:

```text
$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Products/MIC-Products/
ARMOR-MIC-Product-Optimization-Standard-v1.0.md
```

The Vault Standard is the sole detailed MIC workflow authority. Use
`armor-memory` for scoped retrieval and never use WeKnora's indexed copy as a
replacement for the Vault document. If the standard is missing, unreadable,
or cannot be resolved through `$ARMOR_VAULT_ROOT`, return `BLOCKED_SOURCE`.
Never silently fall back to an embedded duplicate rule set.

## Minimum input

Collect only what the requested task needs: product identity and model/SKU,
target MIC category, source references, current edit-page extraction
(`mic-product-edit-context/v1`) when an existing listing is being optimized,
and any current user/company decisions.
Pass the sources and requested scope to the Vault Standard's field and fact
rules before drafting.

## Execution adapter stages

1. Resolve the canonical Vault Standard and the Router-returned MIC workspace.
2. Collect only scoped Vault, original product, user/company, current MIC, and
   supplied-media evidence permitted by that Standard.
3. Apply the Standard's authority review, field plan, optimization, detail-page
   and audit stages; preserve its blockers and approval gate.
4. After explicit user approval, call only `save_mic_product_package` through
   the scoped Router and verify the read-back result.

Use `armor-memory` for Vault routing/retrieval, WeKnora only as a product or
company knowledge retrieval surface, and `ai-writing-audit v0.3.1` only when
editorial style adds value. Do not load legacy MIC workflow Skills as
competing authorities.

## Fail-closed invariants

- Do not fabricate technical, commercial, certification, packaging, or
  performance facts.
- Exact technical values must ultimately resolve to an authoritative original
  source under the Vault Standard's authority rules; conflicts remain visible
  and use `MIC_AUTHORITY_REVIEW_REQUIRED` or the appropriate blocker.
- `UNKNOWN` remains unknown and is not converted into a complete-looking
  numeric or commercial value.
- Do not perform live MIC editing or edit a live MIC listing, upload,
  publication, price/category mutation, messaging, or account actions.
  Automatic MIC editing is also forbidden.
- Persistence uses only `save_mic_product_package`; no arbitrary file write or
  destination is allowed.

## Runtime boundary

This adapter is compatible with the existing Operations Profile boundary:
generic shell, terminal, file, browser, computer-use, delegation, and Legacy
Memory remain unavailable. Firecrawl/Anysearch credential blockers and the
unexposed Obscura/PaddleOCR surfaces do not change the Vault-grounded core
workflow.
