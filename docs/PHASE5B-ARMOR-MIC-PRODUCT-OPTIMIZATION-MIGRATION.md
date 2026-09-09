# Enterprise AI Office — Phase 5B

## ARMOR MIC Product Information Optimization Capability Migration

Date: 2026-09-09
Repository baseline: `f67671ecf93bb5fadc0754cb281a65f1826cfb50`
Target: Operations Hermes on MacStudio
Scope: MIC product-information preparation and reviewed Vault package save only

## Legacy MIC Inventory

The scoped Legacy review covered the active global Skill root and the local
`mic-ops` profile without opening Legacy Hermes Memory, session history, or
private Memory data.

Selected MIC capabilities:

- `mic-product-fill`: the legacy BulkFill field contract and paste-ready
  output rules. The profile copy is a link to the global ARMOR copy; no second
  implementation was found.
- `mic-product-audit`: a separate pre-delivery checklist with known MIC
  pitfalls, including ASCII, single-select voltage, package data, pricing
  modes, FAQ specificity, and current edit-page extraction.
- `mic-product-detail-page`: a separate module-based rich-text/detail-page
  workflow with image planning and no-HTML/no-external-contact rules.
- `mic-upload-data-sources`: source priority, defuddle-first public-page
  extraction, edit-page extraction JSON, and quotation/package guidance.
- `mic-optimization-guide`: related platform standards and historical category
  references; its copied/profile form was treated as a cache, not authority.

The Legacy profile contained approximately 114 exposed Skills. No bulk copy
was performed. The selected Skills were inspected with their references and
agent metadata. Relevant references covered category attributes, current
BulkFill field mappings, product-type mappings, member-center extraction,
Defuddle scraping, quotation structure, detail-page modules, and IP language.
No selected Skill required a runtime script or a new dependency.

Representative real Vault artifacts reviewed before design included multiple
`MIC-BulkFill-Input` and `PASTE-READY` files, `MIC-Optimization-Report` and
`MIC-Optimization-Summary` files, `MIC-Product-Description`, and
`MIC-Detail-Page` files across the 2026-05-19 through 2026-07-03 product
batches. The review found duplicate versions, legacy section headings,
unresolved price/package fields, and historical output claims that must remain
evidence rather than rules.

## MIC Authority

The current authority is:

`${ARMOR_VAULT_ROOT}/02-Projects/Workspaces/Products/MIC-Products/ARMOR-MIC-Product-Optimization-Standard-v1.0.md`

It is explicitly marked `authority: canonical` and records the source
hierarchy, current edit-page extraction precedence, fact classes, conflict
handling, BulkFill rules, detail-page boundary, and save/publication gate.
Historical files remain working evidence and were not promoted automatically.

The canonical runtime entrypoint is
`skills/shared/department/armor-mic-product-optimization/SKILL.md`. The
historical `mic-product-fill` shared entrypoint was removed; audit and detail
logic are subordinate stages of the single MIC workflow.

## MIC Workflow

Input is intentionally small: product identity, model/SKU, target MIC
category, source references, and the current edit-page extraction when an
existing listing is being optimized. Commercial and packaging fields are
optional but must be source-backed.

The stages are intake/route, scoped source collection, authority review, field
plan and fact audit, MIC optimization, optional materially separate detail-page
writing, deterministic audit, explicit user review/approval, scoped save, and
read-back verification.

Fact classes are `USER_CONFIRMED`, `AUTHORITATIVE_DOCUMENT`,
`CANONICAL_KNOWLEDGE`, `MIC_EXISTING_SOURCE`, `OBSERVABLE_MEDIA`,
`REASONABLE_INFERENCE`, and `UNKNOWN`. Inference may improve wording but may
not create technical or commercial values. Missing values become
`BLOCKED_FACTS`, `BLOCKED_SOURCE`, or `BLOCKED_CATEGORY`; conflicts become
`MIC_AUTHORITY_REVIEW_REQUIRED`. The workflow never fabricates dimensions,
power, voltage, CCT, CRI, materials, certifications, MOQ, price, lead time,
capacity, warranty, customer/case/market claims, packaging, logistics, or
ranking claims.

The audit checks current category fields, exact BulkFill names, title and
keyword consistency, highlights, specs, one FOB mode, ASCII/length limits,
custom-property deduplication, package evidence, unknowns, and contradictions.
`ai-writing-audit v0.3.1` is reused for editorial style where useful; facts
and source coverage outrank its score.

The approval boundary is explicit user review of the prepared Vault work
product. The save is not live MIC editing or publication. Automatic MIC
editing, upload, price/category/media changes, account mutation, messaging,
and publishing remain disabled.

## Artifact Contract

Router vocabulary was extended with the smallest semantically correct enum:
`products/mic-product`. It resolves to the existing lifecycle-neutral
workspace:

`02-Projects/Workspaces/Products/MIC-Products/`

The scoped `save_mic_product_package` accepts only `package_id` and a closed
file map:

- required `mic-product-data.yaml` — structured optimized data, category and
  edit-page mapping, fact classes, sources, unknowns, blockers, and approval;
- required `mic-bulkfill.txt` — raw recognized section/field lines only;
- required `mic-audit.md` — fact, contradiction, field, character, quality,
  approval, and publication-boundary audit;
- optional `mic-detail-page.md` — manual MIC rich-text/module reference when
  materially separate.

The save rejects unknown filenames, absolute/traversal input, symlink escape,
Published destinations, unexpected existing files, manual-only Product Detail
or Product Display sections inside BulkFill, and empty/oversized files. Writes
are atomic and read back with SHA-256 evidence. Article and Social package
contracts remain unchanged apart from the shared tool-list containing the new
MIC operation.

## Runtime Statuses

| Capability | Runtime status | Operations exposure |
|---|---|---|
| WeKnora | Read-only configured/healthy | Enabled, retrieval tools only |
| ToolScout | Healthy shared infrastructure | Enabled, exact eight-tool allowlist |
| `ai-writing-audit v0.3.1` | Installed canonical offline audit | Enabled Skill dependency |
| Obscura | Installed and healthy where probed | Not exposed |
| PaddleOCR | Installed and healthy where probed | Not exposed; not required for core MIC work |
| Firecrawl | Read-oriented native filter; blocked without credential | Filtered Operations MCP |
| Anysearch | Credential-blocked | Not exposed |

Firecrawl/Anysearch credential blockers do not block a source-grounded MIC
package when Vault, WeKnora, user documents, or a supplied current MIC source
is sufficient.

## Acceptance Fixture

The fixture uses the real ARMOR product `HM-MSL-S10-24V-65K80-S-V1`, the
10x10mm magnetic LED shelf-light product represented in the existing MIC Vault
batch and product Knowledge entities. Sources are referenced by relative Vault
paths, including the existing `MIC-BulkFill-Paste-Ready.md`, the product
entity, and the magnetic mounting entity.

The acceptance exercises source collection, authority/fact classification,
field planning, title, center words, keywords, attributes, specifications,
selling points, description reference, raw paste-ready output, unknown-field
retention, scoped save, and read-back. Packaging evidence remains an explicit
unknown in the fixture and is not emitted into BulkFill. No live MIC page,
account, price, category, media, or external publication is modified.

## Operations Permissions

- Generic shell, terminal, file, code execution, browser, computer-use, and
  delegation: disabled.
- MIC listing editing, upload, account mutation, publication, and messaging:
  disabled.
- SSH: used only by the deployment operator for bounded repository/config
  synchronization and health checks; not an Operations Profile tool.
- `sudo`: not granted to the Operations Profile.
- Hermes Memory, user Profile Memory, and session search: OFF.
- The only MIC write surface is the scoped closed-package Vault save; it does
  not accept an arbitrary destination.

## Validation and Delivery

The migration runs the Phase 4A/4B/4C checks, Article and Social regression
tests, new Phase 5B MIC tests, deployed Hermes checks, repository readiness,
configuration validation, and gateway health. The live configuration is
backed up before modification. No secrets are copied into the repository or
the migration record.

Phase 5B: PASS

MIC authority: CANONICAL
Canonical MIC Skill: PASS
Duplicate MIC workflow removed: PASS
MIC runtime exposure: PASS
MIC scoped Router Save: PASS
MIC E2E: PASS

Article regression: PASS
Social regression: PASS
ToolScout regression: PASS
MCP permission regression: PASS

Operations Hermes Memory: OFF
Generic browser enabled: NO
Automatic MIC editing enabled: NO
Legacy Memory migration: NOT PERFORMED
Secrets committed: NO

Repository readiness: 265 PASS / 0 FAIL
Commit: recorded in final delivery after verification
Push: recorded in final delivery after verification
