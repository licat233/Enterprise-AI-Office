# E-commerce Product Image Production — Preparation Record

Status: PREPARATION ONLY / NOT INSTALLED / NOT EXPOSED

Date: 2026-09-13

Repository branch: `task/ecommerce-product-image-prep`

## 1. Purpose

Prepare Enterprise AI Office for a future reusable Skill that performs real e-commerce product image production.

Target canonical path after approval:

```text
skills/shared/department/ecommerce-product-image-production/
```

This preparation record does **not** create or activate the Skill. No Hermes Profile exposure changes are made in this phase.

## 2. Capability Reuse Pass

### Business requirement

EAO needs a governed workflow that can take approved product facts, real source assets, target marketplace/channel requirements, and a product-visual brief, then produce or edit e-commerce product images and perform post-generation QA.

### Existing EAO check

The current repository already contains:

- `skills/shared/department/armor-product-visual/`
- generic design-related Skills under `skills/shared/department/`
- Product Marketing / cross-border e-commerce Skills
- ToolScout
- MCP Control Plane
- WeKnora company knowledge
- ARMOR scoped Vault Router

### Existing Skill check

`armor-product-visual` is the closest current ARMOR capability.

Its current contract ends at:

```text
READY_FOR_GENERATION
```

It covers source grounding, product identity, provenance, visual brief, prompt/edit handoff, anti-moiré constraints, and manual QA preparation.

It explicitly does **not** provide:

- image generation runtime;
- image editing runtime;
- binary image upload;
- publishing.

Therefore the missing business capability is real image production/editing after the governed Product Visual handoff.

### Hermes native check

Hermes provides the Agent/Skill/Profile runtime, but no existing repository evidence establishes a production-approved image-generation/editing backend for this ARMOR deployment.

No second workflow engine is justified.

### Open WebUI check

Open WebUI may be used as a human-facing invocation surface, but it is not the authority for the business workflow and does not remove the need for a governed image-production backend.

### WeKnora check

WeKnora remains the authority for approved company/product knowledge retrieval. It is not an image-generation runtime.

### ToolScout check

ToolScout should be used before adding incidental image-processing utilities. Commodity operations such as resize, format conversion, metadata inspection, compression, or batch transformation should reuse mature installed tools where possible instead of being reimplemented inside the Skill.

### Gap

The precise gap is:

```text
approved Product Visual handoff
→ actual image generation/editing
→ source/product consistency QA
→ approved final e-commerce image artifacts
```

### Smallest proposed addition

Add one reusable Skill:

```text
ecommerce-product-image-production
```

that consumes the existing Product Visual handoff and calls only an explicitly approved image-generation/editing capability.

Do not duplicate the Product Visual source-of-truth/provenance workflow.

## 3. Proposed responsibility split

```text
Authoritative product/company facts
→ WeKnora / approved source documents

Product identity, provenance, visual brief, anti-moiré, pre-generation QA
→ armor-product-visual

Real e-commerce image generation/editing
→ ecommerce-product-image-production

Commodity file/image transformations
→ ToolScout-selected mature tools

Profile/tool authorization
→ Hermes Profile config + MCP Control Plane

Employee/admin chat surface
→ Open WebUI and/or approved Hermes Messaging
```

## 4. Proposed Skill boundary

The future Skill may own:

- e-commerce image-set planning from an approved brief;
- generation/edit execution through an approved backend;
- channel-specific composition instructions;
- asset-by-asset production state;
- product-consistency checks after generation/editing;
- text/logo/certification hallucination checks;
- output naming and handoff metadata;
- final human-review package.

It must not silently own or overwrite:

- authoritative product specifications;
- company knowledge;
- Brand source of truth;
- marketplace account credentials;
- generic filesystem write access;
- publication authority;
- arbitrary browser automation;
- unrestricted shell access;
- image-generation provider credentials outside the approved protected binding.

## 5. Dependency on `armor-product-visual`

Preferred flow:

```text
product sources + real photos
        ↓
armor-product-visual
        ↓
READY_FOR_GENERATION
        ↓
ecommerce-product-image-production
        ↓
generated / edited image set
        ↓
post-generation QA
        ↓
human approval
        ↓
approved output handoff
```

The new Skill should consume the existing handoff rather than re-encode Product Visual truth/provenance rules.

## 6. Source-of-truth and runtime location

Canonical repository authority:

```text
Enterprise-AI-Office/
└── skills/
    └── shared/
        └── department/
            └── ecommerce-product-image-production/
```

The runtime Hermes Profile should load the approved Skill from the company Skill source/external Skill directory according to the installed Hermes version.

Do not create independent drifting copies in multiple Profile homes.

## 7. Initial Profile exposure target

Preparation recommendation only:

| Profile | Proposed exposure |
| --- | --- |
| Operations | Candidate |
| Marketing | Candidate when/if instantiated and approved |
| General | No |
| Sales | No |
| Procurement | No |
| default/admin | Control-plane only; not a normal employee invocation surface |
| future EAO maintainer/admin Profile | Review/admin use only, subject to its own contract |

Actual exposure remains disabled until runtime acceptance is complete.

## 8. Image-generation/editing backend gate

A Skill alone cannot create images unless a real backend is available.

Before activation, resolve exactly one approved execution path and record:

- provider/runtime identity;
- supported generation vs editing operations;
- authentication method;
- data sent externally;
- product-image input handling;
- output/download handling;
- image size/format limits;
- cost/rate limits;
- safety/content constraints;
- file-storage boundary;
- rollback/remove procedure.

Do not add multiple image backends for completeness.

If no approved backend exists, the future Skill must stop at:

```text
BLOCKED — IMAGE PRODUCTION BACKEND NOT APPROVED
```

## 9. Security review required before activation

Review at minimum:

- `SKILL.md`;
- all scripts;
- references/templates;
- required environment variables;
- external network calls;
- filesystem read/write scope;
- binary file handling;
- image provider/API credentials;
- license/provenance;
- whether prompts or uploaded product images leave the Mac Studio;
- whether the backend can perform unrelated actions;
- whether final outputs can be written only to an approved destination.

No plaintext secrets may enter Git.

## 10. Acceptance plan

The capability is not considered installed merely because its directory exists.

Activation PASS should prove:

```text
[ ] real Skill source reviewed
[ ] no duplicate of armor-product-visual
[ ] approved image backend resolved
[ ] protected credential binding works
[ ] intended Profile can invoke the Skill
[ ] unapproved Profile cannot invoke it
[ ] input product facts come from approved sources/handoff
[ ] real source image provenance is preserved
[ ] one controlled generation/edit test completes
[ ] output does not invent unsupported product geometry/features
[ ] fake text/logo/certification behavior is checked
[ ] anti-moiré/product-visual constraints survive execution
[ ] output lands only in approved location
[ ] no unintended publication occurs
[ ] restart/new-session behavior remains correct
[ ] rollback disables the capability without damaging Core/Operations
```

## 11. Installation gate

Do not create the final Skill directory or expose it to a Hermes Profile until at least one of the following is supplied:

1. the real third-party/company Skill source (repository, folder, or `SKILL.md` package); or
2. an explicit requirement to author a new company-owned Skill from scratch.

At that point:

```text
source review
→ duplicate/overlap check
→ adapt minimally if required
→ place in canonical skills directory
→ configure runtime loading
→ configure backend/tool boundary
→ acceptance
→ repository readiness
→ PR review
→ merge to main
→ delete task branch
```

## 12. Current decision

```text
Preparation: PASS
Skill installed: NO
Hermes exposure: NO
Image backend approved: NO
Runtime mutation: NO
Existing Product Visual capability preserved: YES
New infrastructure added: NO
```
