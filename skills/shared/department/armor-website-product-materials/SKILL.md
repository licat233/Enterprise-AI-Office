---
name: armor-website-product-materials
description: >
  Prepare source-grounded ARMOR product-page materials for armorltg.com as a
  reviewed Vault package. Use for product-page source reconciliation, copy,
  SEO, and media planning; not for Article, MIC, website code, publishing, or
  visual generation.
license: MIT
metadata:
  hermes:
    tags:
      - armor
      - website
      - product
      - product-materials
      - seo
      - media
      - source-reconciliation
    pipeline_version: "1.0"
---

# ARMOR Website Product Materials

This is the Enterprise execution adapter for the canonical Vault Standard:

`$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Website/Product-Materials/ARMOR-Website-Product-Materials-Standard-v1.0.md`

Load that Standard before doing product-materials work. If it is unavailable,
stop with `BLOCKED_SOURCE`; do not fall back to a detailed SOP embedded here.

## Use this Skill for

- a reusable ARMOR product-page preparation package;
- source inventory and reconciliation across product sources;
- fact-bound product-page copy, SEO metadata, information architecture, FAQ,
  applications/installation notes, and a media plan;
- a reviewed handoff for later implementation in the official website repo.

The one active Enterprise entrypoint is this Skill. It is separate from
`armor-website-article-pipeline` and
`armor-mic-product-optimization`. Do not use Article or MIC artifacts as an
authority substitute, and do not create a second product-materials workflow.

## Input and source boundary

Require a stable product identity/package id, the scoped source references,
the current website-repo snapshot or URL evidence when available, and any
explicit current company decisions. Collect only the named product scope:
canonical Brand and Product Knowledge, authoritative original Datasheet/
Manual/test/certification documents, supplied media, approved website evidence,
and relevant historical records as evidence only. WeKnora may locate or
retrieve source-backed knowledge; it is not final technical authority.

Technical facts follow the Standard's hierarchy: authoritative original
documents, then canonical/verified Product Knowledge, then WeKnora retrieval,
then current website evidence. A conflict fails closed as
`PRODUCT_AUTHORITY_REVIEW_REQUIRED`; an unknown stays unknown. Observable media
can support only directly visible facts. `REASONABLE_INFERENCE` may improve
wording or organization, never numeric, certification, commercial,
performance, or other hidden technical facts.

Marketing choices must come from current canonical Brand/Product rules,
approved website strategy, or explicit current company decisions. Historical
website/MIC copy is evidence, not current authority.

## Execution stages

1. Resolve the Standard and deterministic `website/product-materials` Router
   destination.
2. Build a scoped source inventory and reconciliation map with source locators,
   authority class, identity relation, extracted facts, unknowns, and conflicts.
3. Normalize only source-supported facts; preserve blockers and unresolved
   identity instead of guessing.
4. Draft page content mapped to the current website Product schema
   (`title`, `sourceId`, `system`, `family`, optional `subfamily`, `excerpt`,
   `image`, `gallery`, `pdf`, `video`, `videos`, `specifications`, and
   `metadata`) plus body structure, applications/installation, FAQ, and related
   content where supported.
5. Draft natural title, slug/permalink proposal, meta description, keywords,
   and search/entity coverage without invented search-volume claims.
6. Inventory supplied media, identify missing assets, propose a shot list and
   alt text, and retain source citations. Do not generate, retouch, diffuse,
   or otherwise modify visuals; do not invoke ComfyUI or image tools.
7. Produce the audit and request the required user/company review before save.
8. After approval, call only
   `save_website_product_materials_package` with the exact closed five-file
   contract. Verify Router path, package identity, atomic read-back, and SHA256
   results.

## Runtime and publication boundary

This Skill prepares materials; it does not edit the website repository, deploy,
publish, submit indexing, mutate accounts, or create a Published record. The
website repository is read-only evidence. The scoped Router may persist only
the closed package under its deterministic Vault workspace; it accepts no
arbitrary destination, absolute path, traversal, symlink escape, or extra file.

The package is:

- `product-source-map.yaml`
- `product-page-content.md`
- `product-seo.md`
- `product-media-plan.md`
- `product-audit.md`

The audit must state approval status, source/identity conflicts, unknowns,
unsupported claims removed, schema mapping, media gaps, and the no-publication
result. A package may be saved for review while carrying
`PRODUCT_AUTHORITY_REVIEW_REQUIRED`; it must not turn a blocker into a public
claim.

Keep generic execution, browser/file/terminal access, Legacy Hermes Memory,
and Agent Delegate/Multi-Agent Orchestration outside this workflow. Use only
the approved read/retrieval tools and the scoped save tool exposed by the
Operations Profile.
