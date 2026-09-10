# Enterprise AI Office — Phase 5E

## ARMOR Product Visual / Anti-Moiré Capability Migration

Date: 2026-09-10
Repository baseline: `ad86c21a1cff6106f45f8d403dd3768798066093`
Repository branch: `codex/media-transcription`

## Decision

Phase 5E migrates one ARMOR-specific business workflow: source-grounded
Product Visual preparation and anti-moiré QA handoff. It does not migrate
generic design tooling, image-generation infrastructure, visual runtime
accounts, publication, or Agent Delegate/Multi-Agent Orchestration.

Phase 5E: PASS

The migration is clean-room. Legacy sources were inspected read-only as
evidence; no Legacy Skill, Profile, script, template, runtime, image account,
or memory content was copied into Enterprise.

## Legacy Product Visual inventory

```text
Legacy Skill(s): design-image-prompt-engineer
ARMOR-specific reference: armor-anti-moire-guide.md
Related reference: ai-cleaner-pitfalls.md
Profile inspected: design-ops
Related generic Skills inspected: design-brand-guardian, design-ux-researcher, product-marketing
Historical work products reviewed: ARMOR Real Product Visual Asset Strategy, AI image artifact avoidance guidance, Visual Exploration material, ESL V26.4 Datasheet and existing SLIM-213BWRY image evidence
Whole design-ops migration: NO
Legacy Memory/session/history/private remembered facts/correction memory: NOT ACCESSED
```

The Legacy prompt Skill is generic prompt-engineering infrastructure. The
business-specific migration evidence is the ARMOR anti-moiré reference and
the product-identity/provenance constraints in ARMOR's existing asset
governance and real product materials. No ComfyUI, Stable Diffusion, local
GPU, image daemon, browser utility, retouching runtime, or external image
account was present as a capability to migrate.

| Legacy module or capability | Decision | Enterprise result | Reason |
|---|---|---|---|
| `design-image-prompt-engineer` generic prompt skeleton | `GENERIC_INFRASTRUCTURE` / not migrated | Thin Product Visual adapter only | Generic prompt mechanics are not an ARMOR business capability |
| `armor-anti-moire-guide.md` | `MIGRATED` | Canonical Product Visual Standard | Verified ARMOR LED/ESL visual rules were re-expressed in the Standard |
| `ai-cleaner-pitfalls.md` | `MIGRATED` | Product Visual post-processing and QA guardrails | Real cleanup pitfalls are retained without enabling a cleaner runtime |
| ARMOR visual asset strategy and real product evidence | `MERGE` | Product identity, provenance, and no-invention boundary | Existing canonical/working ARMOR evidence establishes product truth and asset status |
| Generic Brand/design roles | `KEEP` | Existing generic capabilities | No duplicate ARMOR visual brand system was created |
| Image generation/editing runtime | `EXPERIMENTAL_HOLD` / `NOT_MIGRATED` | No Enterprise runtime or permission | Phase 5E ends at `READY_FOR_GENERATION` |
| Agent Delegate / Codex / Claude Code lanes | `EXPERIMENTAL_HOLD` / `NOT_MIGRATED` | No Operations exposure | Runtime/Profile architecture remains disabled |

## Authority and ownership

```text
Vault Standard: $ARMOR_VAULT_ROOT/02-Projects/Workspaces/Products/Product-Visual/ARMOR-Product-Visual-Standard-v1.0.md
Previous authority: Legacy ARMOR anti-moiré reference, current ARMOR Brand/Product rules, official asset-governance guidance, and real historical/source work products
Current authority: canonical active Product Visual Standard v1.0
Execution owner: skills/shared/department/armor-product-visual/SKILL.md
Workflow owner: the canonical Vault Standard, not the Skill or an Operations Profile
Router destination: 02-Projects/Workspaces/Products/Product-Visual/
```

The Skill is a thin execution adapter. It loads the Standard, performs the
source-grounded intake/brief/prompt/QA workflow, and binds only the scoped
four-file save. It does not duplicate the anti-moiré SOP, product-facts
database, Brand rules, or channel publication contracts.

The Product Visual Standard is lifecycle-neutral and cross-channel. Website
Product Materials, Social, MIC, and future approved visual production may
consume a reviewed handoff, but Product Visual does not publish or alter those
work products.

## Product truth and provenance

For exact product facts, the Standard uses this hierarchy:

```text
1. authoritative original Datasheet / Manual / test or certification document
2. canonical or explicitly verified Product Knowledge derived from an authoritative source
3. read-only WeKnora retrieval used to locate or retrieve that knowledge/source
4. current website or MIC listing as existing-state evidence
```

WeKnora is a derived retrieval/index layer and cannot silently override an
original authoritative document. Conflicting authoritative claims produce
`VISUAL_AUTHORITY_REVIEW_REQUIRED`. Explicit current company/user confirmation
or approved current commercial documentation may supersede historical
commercial evidence, but cannot upgrade a technical claim. Observable media
supports only directly visible facts. `REASONABLE_INFERENCE` may improve
wording or organization but cannot create numeric/hidden specifications,
certifications, commercial facts, performance claims, labels, or structures.

The minimum fact classes are:

```text
AUTHORITATIVE_PRODUCT_FACT
OBSERVABLE_SOURCE_IMAGE
BRAND_VISUAL_RULE
CREATIVE_DIRECTION
GENERATIVE_INFERENCE
UNKNOWN
```

The asset provenance classes are:

```text
REAL_SOURCE_ASSET
EDITED_REAL_ASSET
GENERATED_ASSET
COMPOSITE_ASSET
REFERENCE_ONLY
```

Provenance is never overwritten or relabeled to make an asset appear
original. Generated or composite material is not represented as a real source
asset, and generated material is not final product truth by default.

## Product Visual workflow

```text
Input: stable product/SKU identity, scoped authoritative references, available real images and locators, target use/channel, requested visual objective, supplied dimensions/aspect, creative direction if any
Stages: intake → product identity → source/image collection → existing asset classification → product-truth constraints → visual objective/channel → visual brief → prompt/edit instruction → anti-moiré controls → Brand/product audit → human review → scoped save/readback
States: BLOCKED_PRODUCT_IDENTITY → BLOCKED_SOURCE → VISUAL_AUTHORITY_REVIEW_REQUIRED → READY_FOR_BRIEF → READY_FOR_GENERATION → READY_FOR_QA
Approval: explicit review/approval is required before the four-file scoped save; save is not generation approval or publication approval
```

The product boundary preserves geometry, connector, housing, mounting,
materials, dimensions/proportions, emitting structure, screens, ports, cables,
magnets, controls, accessories, and source-consistent labels. The workflow
must not invent LEDs, continuous diffusion, non-emissive display glow, ports,
controls, certification marks, logos, or text labels. Product truth wins over
creative direction.

## Anti-moiré rules

The migrated ARMOR guidance covers LED pixel/segment repetition, ESL/display
pixel patterns, fine grille or mesh, close-up camera/render sampling,
repetitive shelf geometry, and texture frequency. It requires:

- a close or medium-close source-grounded view with the product large in frame;
- simple backgrounds and reduced high-frequency/repetitive detail density;
- avoidance of tiny LED beads, dense grids, fine mesh, repeated holes, and
  distant repeated shelf details unless the source requires them;
- controlled sharpness, realistic clean matte materials, natural edges, and
  negative constraints for moiré, interference, aliasing, wavy/noisy grids,
  fake micro-detail, pixel noise, distorted/repeating patterns, and rainbow or
  crawling artifacts;
- conditional LED/ESL wording only when consistent with the verified product
  emitting/display structure; a diffuser must not be invented or used to hide
  a real structure;
- post-processing defaults that reduce noise, texture, or clarity only as
  needed, with stronger correction reserved for severe artifacts;
- inspection at 100%, while avoiding aggressive sharpening, JPEG
  recompression, or abusive upscaling.

These controls reduce sampling-risk detail; they do not change what the
product is or create a technical specification.

## Prompt and QA handoff

The prompt/edit handoff keeps these sections separate:

```text
immutable_product_facts
scene_and_composition
lighting_camera_and_view
materials_and_environment
target_use_or_channel
negative_constraints
anti_moire_constraints
```

If an image is later supplied, QA checks product identity, geometry,
emitting/display structure, unsupported features, fabricated text/logos or
certifications, high-frequency artifacts, brand alignment, provenance, and
approval state. If no safe image-inspection runtime is available, the result
is a manual QA handoff; lack of generation or multimodal inspection is not a
Phase 5E failure.

## Closed artifact contract

The durable Product Visual package contains exactly these UTF-8 text files:

```text
visual-source-map.yaml
visual-brief.md
visual-prompt.md
visual-audit.md
```

`save_product_visual_package` accepts only a validated package id and those
four filenames. The deterministic Router resolves
`02-Projects/Workspaces/Products/Product-Visual/`. The scoped MCP rejects
absolute paths, traversal, symlink escape, `Published` destinations, extra
files, binary uploads, arbitrary destinations, and publication. It writes
atomically and returns/read-verifies package identity and SHA256 values.

Existing Article, Social, MIC, and Website Product Materials save contracts
were not changed; the aggregate scoped Router allowlist adds only the new
semantically distinct Product Visual save tool.

## Acceptance fixture

The offline E2E fixture uses the real ARMOR ESL product `SLIM-213BWRY`:

```text
Original source: ESL - Product Specification V26.4.pdf, including the verified product page/technical drawing
Derived support: canonical ESL Product Knowledge V27.0
Existing source image: SLIM-213BWRY.jpg, classified as REAL_SOURCE_ASSET / source evidence
Visual job: source-grounded close-up ESL product visual brief with anti-moiré constraints; no generation required
```

The fixture resolves authoritative original facts ahead of derived knowledge,
WeKnora retrieval, current listing evidence, and creative direction. It keeps
unknowns/conflicts explicit, classifies provenance, produces the four handoff
files, exercises the anti-moiré and QA checklist, simulates approval, and
performs scoped save/readback/SHA256 in an isolated Vault root. No image was
generated, uploaded, published, or substituted for the real source asset.

## Operations and runtime boundary

```text
Product Visual Skill: enabled by canonical symlink only
Product Visual scoped save: enabled
Image generation/editing/retouch/render/upscale: OFF
ComfyUI / Stable Diffusion / local GPU / image daemon: NOT INSTALLED OR BOUND
Generic browser / computer-use / shell / terminal / file / code execution: OFF
External image account or credentials: OFF
Website/social/MIC publication: NOT PERFORMED
Agent Delegate / Codex / Claude Code delegation: OFF
Legacy Hermes Memory: OFF and not accessed
```

The two Legacy Delegate Profiles remain distinct runtime implementations and
are not classified as absorbed Product Visual workflow. Multi-Agent
Orchestration remains `EXPERIMENTAL_HOLD`; fallback and independent-audit
semantics may be preserved separately by current workflows, but no Delegate
worker, auditor, orchestrator, binding, selection rule, fallback runtime, or
audit-return implementation is migrated or exposed here.

## Regressions and acceptance commands

Phase 5E acceptance and the Phase 4A–5D regression suite cover:

- one canonical Product Visual entrypoint and one canonical Vault Standard;
- Router destination, closed package identity, traversal/symlink rejection,
  atomic readback, and SHA256;
- product facts outranking creative direction and inference leaving unknown
  numeric specifications unknown;
- real/generated/composite/reference-only provenance distinctions;
- anti-moiré preservation, immutable prompt constraints, no image runtime,
  no browser/file/code/publication path, and Agent Delegate OFF;
- unchanged Article, Social, MIC, and Website Product Materials contracts;
- repository readiness and `git diff --check`.

Commands executed locally before deployment:

```text
python3 -m py_compile <changed Router/MCP/checker/test scripts>: PASS
python3 scripts/test_phase5e_product_visual.py: PASS (8 tests)
python3 scripts/phase5e_product_visual_check.py: PASS (0 failures)
Phase 4A migration checker: PASS
Phase 4B runtime checker/tests: PASS
Phase 4C runtime checker/tests: PASS
Phase 5A runtime checker/tests: PASS
Phase 5B runtime checker/tests: PASS
Phase 5B.1 authority tests: PASS
Phase 5B.2 authority de-duplication tests: PASS (1 expected skip)
Phase 5D runtime checker/tests: PASS
```

## Final status block

```text
Phase 5E: PASS
Product Visual authority: CANONICAL
Canonical Product Visual Skill: PASS
Duplicate visual workflow removed: PASS
Product Visual runtime exposure: PASS
Product Visual scoped Router Save: PASS
Product Visual workflow E2E: PASS

Anti-moiré rules preserved: PASS
Product identity boundary: PASS
Real/generated asset distinction: PASS

New image generation infrastructure installed: NO
Operations image generation enabled: NO
Generic browser enabled: NO
Website/social/MIC publication performed: NO

Article regression: PASS
Social regression: PASS
MIC regression: PASS
Website Product Materials regression: PASS
ToolScout regression: PASS

Multi-Agent Orchestration: EXPERIMENTAL_HOLD
Agent Delegate migrated: NO
Operations delegation: OFF

Operations Hermes Memory: OFF
Legacy Memory accessed: NO
Secrets committed: NO

Repository readiness: 309 PASS / 0 FAIL
Commit: recorded in final task handoff
Push: PASS after final commit
```
