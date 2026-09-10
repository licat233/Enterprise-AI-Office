---
name: armor-product-visual
description: >
  Prepare source-grounded ARMOR product visual briefs, prompt/edit handoffs,
  provenance records, anti-moiré constraints, and manual QA packages for
  website, social, MIC, and future approved visual production; no image
  generation, binary upload, editing runtime, or publication.
license: MIT
metadata:
  hermes:
    tags:
      - armor
      - product
      - visual
      - anti-moire
      - provenance
      - qa
    pipeline_version: "1.0"
---

# ARMOR Product Visual

This is the Enterprise execution adapter for the single canonical Vault
Standard:

`$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Products/Product-Visual/ARMOR-Product-Visual-Standard-v1.0.md`

Load that Standard before doing Product Visual work. If it is unavailable,
stop with `BLOCKED_SOURCE`; do not fall back to a detailed SOP embedded here.

## Use this Skill for

- source-grounded visual source maps and product-identity checks;
- visual briefs for ARMOR products and approved channel/use contexts;
- prompt or edit-instruction handoffs with immutable product constraints;
- `REAL_SOURCE_ASSET`, `EDITED_REAL_ASSET`, `GENERATED_ASSET`,
  `COMPOSITE_ASSET`, and `REFERENCE_ONLY` provenance classification;
- ARMOR anti-moiré constraints and manual visual QA preparation;
- a reviewed, non-publishing handoff consumed later by Website Product
  Materials, Social, MIC, or another separately approved production workflow.

The one active ARMOR Product Visual entrypoint is this Skill. Do not create a
second visual workflow, copy the Legacy `design-image-prompt-engineer` SOP, or
use the generic design roles as a substitute for the ARMOR product-truth and
provenance boundary.

## Input and authority boundary

Require a stable product identity, scoped authoritative product sources,
available real assets and their source locators, target use/channel, and the
requested visual objective. Resolve product facts from the Standard's
authority model. Product facts and approved Brand rules outrank creative
direction. Observable media supports only directly visible facts. Keep
unknowns and conflicts explicit; use `BLOCKED_PRODUCT_IDENTITY`,
`BLOCKED_SOURCE`, or `VISUAL_AUTHORITY_REVIEW_REQUIRED` when the boundary
cannot be resolved safely.

`REASONABLE_INFERENCE` may organize a brief or improve wording only. It may
not create numeric or hidden technical facts, certifications, logos, labels,
commercial facts, performance claims, or product structures.

## Execution stages

1. Load the canonical Vault Standard and resolve the deterministic
   `products/product-visual` Router destination.
2. Identify the product and reconcile scoped product/Brand sources; preserve
   authority conflicts and unknowns.
3. Inventory supplied real images and classify provenance without overwriting
   or relabeling source history.
4. Define the visual objective, channel/use, dimensions/aspect when supplied,
   and a source-grounded visual brief.
5. Produce a prompt/edit handoff with immutable product facts, scene and
   composition direction, controlled text policy, negative constraints, and
   anti-moiré constraints kept separate.
6. Produce a manual or available-image QA checklist/audit covering product
   identity, unsupported features, fake certification/logo/text, geometry,
   high-frequency artifacts, brand alignment, provenance, and approval state.
7. Stop at `READY_FOR_GENERATION` when an external image generator would be a
   separate, explicitly approved next action. Image generation is not part of
   this v1.0 workflow.
8. After explicit approval, call only `save_product_visual_package` with the
   exact closed four-file UTF-8 text contract, then verify Router path,
   package identity, atomic read-back, and SHA256 results.

## Runtime and publication boundary

This Skill does not generate, edit, retouch, render, upscale, upload, publish,
deploy, or write binary assets. It does not invoke ComfyUI, Stable Diffusion,
an external image account, a browser, file/terminal/code execution, Agent
Delegate, Codex delegation, Claude Code delegation, Legacy Hermes Memory, or a
new daemon/runtime. It does not invoke Agent Delegate runtime. The Product
Visual handoff is text/metadata only and does
not alter Website Product Materials, Social, MIC, or publication contracts.

The scoped Router save accepts exactly:

- `visual-source-map.yaml`
- `visual-brief.md`
- `visual-prompt.md`
- `visual-audit.md`

It accepts no arbitrary destination, absolute path, traversal, symlink escape,
Published destination, extra file, or binary upload. Saving a handoff is not
generation approval and never performs publication.
