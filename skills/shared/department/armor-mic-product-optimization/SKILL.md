---
name: armor-mic-product-optimization
description: >
  The single Hermes runtime entrypoint for ARMOR Made-in-China.com product
  information optimization. It turns verified product inputs into a closed
  MIC data package, paste-ready BulkFill text, an evidence-bound audit, and a
  manual detail-page reference when the MIC editor requires it.
license: MIT
metadata:
  hermes:
    tags: [armor, mic, product, bulkfill, listing, audit, detail-page]
    pipeline_version: "1.0"
---

# ARMOR MIC Product Information Optimization

This is the only MIC product-information workflow exposed to the Enterprise
Operations Profile. It is a workflow adapter: detailed MIC field standards,
category choices, and product facts live in the ARMOR Vault and the shared
`mic-optimization-guide`. Do not revive `mic-product-fill`,
`mic-product-audit`, or `mic-product-detail-page` as separate runtime
entrypoints.

The canonical work-product route is:

```text
route.sh --object work-product --domain products --artifact mic-product --json
→ 02-Projects/Workspaces/Products/MIC-Products/
```

`ARMOR_VAULT_ROOT` is supplied by the Enterprise runtime. Never replace it
with a host-specific path. Retrieve exact Vault files through the current
ARMOR Memory workflow or the read-only WeKnora surface; never begin with a
full-Vault search and never inspect or migrate Legacy Hermes Memory.

## Smallest input contract

Require only what is needed for the requested listing:

- product identity: name, model or SKU, product family, and target MIC
  category;
- source references: Vault paths, user-provided documents/data, an
  authoritative datasheet, an existing MIC listing, or observable supplied
  media;
- current MIC edit-page extraction (`mic-product-edit-context/v1`) when an
  existing listing is being optimized; its actual standard properties and
  `bulkFillFieldName` values override historical templates;
- commercial and packaging fields only when the source explicitly provides
  them; package dimensions are never silently estimated.

If the category is absent, return `BLOCKED_CATEGORY`. If the source set cannot
support a requested field, return `BLOCKED_SOURCE` or `BLOCKED_FACTS` with the
exact missing fields. Do not fill a form merely to make it look complete.

## Fact boundary

Every factual value in `mic-product-data.yaml` carries one of these classes,
and records the source type and locator needed to apply the rules below:

`USER_CONFIRMED`, `AUTHORITATIVE_DOCUMENT`, `CANONICAL_KNOWLEDGE`,
`MIC_EXISTING_SOURCE`, `OBSERVABLE_MEDIA`, `REASONABLE_INFERENCE`, or
`UNKNOWN`.

The class alone is not final authority; the source type must also be checked.

## Type-aware authority rules

### Workflow governance

Use current canonical ARMOR Vault Rules and Standards as the governing
workflow authority for stages, fields, gates, artifacts, and boundaries. This
workflow authority does not let a derived retrieval result override an
authoritative product document.

### Exact product technical facts

For exact product technical facts — including model, dimensions, power,
voltage, CCT, CRI, materials, IP rating, certifications, test standards,
electrical characteristics, and formally documented packaging dimensions —
apply this priority:

1. authoritative original Datasheet, Manual, test, or certification document;
2. canonical or verified Product Knowledge derived from those authoritative
   sources;
3. read-only WeKnora retrieval, used to locate or retrieve the Knowledge or
   source above, never as final technical authority;
4. the current MIC listing or edit page as existing-state evidence.

WeKnora must never silently override a conflicting original authoritative
document. If authoritative sources conflict, keep the conflict visible and
return `MIC_AUTHORITY_REVIEW_REQUIRED` or the existing appropriate blocker.
Historical MIC output cannot override a current authoritative specification.

### Mutable commercial/business fields

For mutable commercial/business fields — including MOQ, price, lead time, payment terms, sample policy, and packaging/commercial configuration — current explicit company or user confirmation, or current approved commercial documentation, may supersede historical MIC listing data. Historical MIC
output remains evidence only, and stale retrieval or historical output must
not be used to backfill a current commercial decision.

### Observable media and inference

Observable media supports directly visible facts only; it cannot create exact
hidden technical parameters. `REASONABLE_INFERENCE` may improve wording or
organization but cannot create numeric facts, certifications, commercial
facts, performance claims, or technical specifications. `UNKNOWN` stays
explicit in the structured data and audit, or is omitted from paste-ready
output. Never fabricate or silently normalize any technical, commercial,
customer, case, market, packaging, logistics, ranking, or performance claim.

## Canonical stages and gates

1. Intake and route: confirm product identity, category, scope, and the
   Router-returned workspace.
2. Source collection: read only the scoped Vault entities/documents and the
   supplied/current MIC source. Record every source used.
3. Authority review: apply explicit `authority: canonical` or
   `authority: verified` only when present. A material conflict returns
   `MIC_AUTHORITY_REVIEW_REQUIRED`; status alone is not authority.
4. Field plan and fact audit: map title, center words, keywords, highlights,
   category properties, custom properties, specs, price, unit, package,
   delivery, sample, payment, FAQ, and detail-page needs. Mark unknowns and
   blockers before writing.
5. MIC optimization: write buyer-useful English copy using the current edit
   page's actual fields. Use one FOB mode only, keep single-select voltage
   single-valued, dedupe custom properties against standard properties, and
   keep the raw BulkFill file to the plugin's recognized section/field lines.
6. Detail-page stage: when the MIC rich-text/module editor is materially in
   scope, write a module plan and copy reference with image placeholders based
   only on supplied/observable media. MIC details are not HTML and contain no
   external URLs or contact identifiers.
7. Audit and approval: run deterministic field/order/ASCII/length/price-mode
   checks and use `ai-writing-audit v0.3.1` when editorial style adds value.
   Facts and source coverage outrank an audit score. Save requires explicit
   user approval represented in the audit/package metadata.
8. Scoped save and read-back: call only `save_mic_product_package` after the
   approval gate, then verify the returned path, exact file set, and hashes.

The workflow may end as `READY_FOR_REVIEW`, `BLOCKED_FACTS`,
`BLOCKED_SOURCE`, `BLOCKED_CATEGORY`, `MIC_AUTHORITY_REVIEW_REQUIRED`,
`READY_FOR_SAVE`, `SAVED_READ_BACK`, or `DEGRADED`. A blocked field is never
replaced with a guess.

## Durable artifact contract

The scoped MIC package uses these normalized filenames under the Router
destination:

- `mic-product-data.yaml` — structured product data, category/edit-page
  mapping, fact classes, source references, unknowns, blockers, and approval
  metadata;
- `mic-bulkfill.txt` — raw Chrome BulkFill text only. It contains recognized
  `# section` headers and `field:value` lines, omits `# 产品详情` and
  `# 产品展示`, and uses no standalone comments or explanations;
- `mic-audit.md` — fact audit, contradiction report, MIC quality checks,
  source list, tool result, approval status, and publication boundary;
- `mic-detail-page.md` — optional manual rich-text/module reference when a
  separate MIC detail-page stage is materially required.

Legacy names are normalized as follows: `MIC-BulkFill-Input*` and
`PASTE-READY*` → `mic-bulkfill.txt`; `MIC-Optimization-Report*` →
`mic-audit.md`; `Product-Description*` and `MIC-Detail-Page*` →
`mic-detail-page.md`. Do not keep duplicate versions in a new package. Never
create `task-state.json` or use a lifecycle folder such as Draft/Review/
Approved/Published for this work product.

The save operation accepts only `package_id` plus the closed `files` object.
It routes to the deterministic MIC workspace, rejects absolute paths,
traversal, symlink escapes, Published destinations, unexpected existing files,
and unknown filenames, and performs atomic write plus read-back verification.

## External-action boundary

This capability prepares and saves a reviewed Vault work product only. It does
 not perform automatic MIC editing or edit a live MIC listing, upload images, select a category, change price,
send messages, publish, or mutate an account. Generic shell, terminal, file,
browser, computer-use, delegation, and Legacy Memory surfaces remain outside
the Operations Profile. Obscura and PaddleOCR are not required for the core
workflow and remain unexposed. Firecrawl and Anysearch are optional read-side
dependencies; credential blockers do not block work grounded in Vault,
WeKnora, user documents, or a supplied current listing.
