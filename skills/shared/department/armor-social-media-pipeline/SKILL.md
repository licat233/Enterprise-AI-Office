---
name: armor-social-media-pipeline
description: The single Hermes runtime entrypoint for producing ARMOR overseas social-media content for LinkedIn, Facebook, Instagram, TikTok, and YouTube. Use when selecting topics, building social Topic Briefs, drafting platform-specific copy, producing video packages, auditing social content, routing approved social-copy deliverables, or reviewing published performance. The canonical workflow and templates live in the ARMOR Vault Social Media Production Pipeline folder.
---

# ARMOR Social Media Production Pipeline

This is the single runtime entrypoint for ARMOR overseas social-media
production. It is an adapter: the canonical stages, artifacts, gates, and save
boundaries live in independent Markdown standards in the Vault pipeline folder.
Do not duplicate the full workflow in this skill.

Canonical folder:

`${ARMOR_VAULT_ROOT}/02-Projects/Workspaces/Content/ARMOR-Content-Operations/ARMOR-Social-Media-Production-Pipeline-v2.0/`

`ARMOR_VAULT_ROOT` is supplied by the Enterprise runtime. Do not replace it
with a host-specific absolute path.

Read the matching Markdown standard for the current stage. The main stage map
and contracts live in `armor-social-media-pipeline.md`; detailed stage
standards are `intake-standard.md`, `topic-selection-standard.md`,
`topic-brief-standard.md`, `social-writing-standard.md`,
`platform-adaptation-standard.md`, `social-audit-standard.md`,
`approval-standard.md`, `save-standard.md`, and
`performance-standard.md`.

## Stable flow

```text
Intake / topic confirmation
→ topic signals and deduplication
→ evidence pack and Topic Brief
→ core draft
→ humanization (ai-writing-audit detect → fix → re-detect)
→ humanization and platform adaptation
→ social audit
→ focused correction when required
→ write every artifact directly into the Router destination (quality_status: DRAFT)
→ user approval of the Vault file (Obsidian)
→ status update and read-back in the same file
→ post-publication performance review
```

## Draft location and review

Write every pipeline artifact — Topic Brief, Core Draft, platform variants,
and the audit report — directly into the Router destination directory
(`route.sh --object work-product --domain marketing --artifact social-copy --json`
→ `03-Records/Published/Social-Media/`) as soon as it exists, with
`quality_status: DRAFT` in the frontmatter.

- Do not write working drafts to `/tmp`, the home directory, or anywhere
  outside the ARMOR Vault.
- The user reviews the Vault file itself (e.g. in Obsidian). There is no
  "temporary draft for review, then move to the Vault" step: the reviewed file
  is the Vault file.
- After explicit user approval, update the status in that same file
  (`quality_status: APPROVED_FOR_SAVE`), read it back, and verify. Do not copy
  or move the file to a second location.
- Draft is a status, not a destination. Writing to the Router destination with
  `quality_status: DRAFT` is not publishing and not a final save.

## AI-style detection and humanization

Humanization is not a free-form rewrite. Run the `ai-writing-audit`
CLI on the core draft and on every platform variant before handoff:

```bash
python3 <ai-writing-audit>/scripts/audit.py DRAFT.md --mode detect \
  --language auto --profile armor --format json
```

Resolve `<ai-writing-audit>` to the directory containing the installed
`ai-writing-audit` `SKILL.md` (this profile's `ai-writing-audit` skill;
do not assume the current working directory).

- The `armor` profile enables both generic AI-style rules and the
  `ARMOR-FACT-*` domain checks (ESL≠LCD, power-track connection needs
  evidence, magnetic lights need ferromagnetic surfaces, no unsupported
  zero-install-cost/ROI claims, verify voltage/connection).
- Treat every finding as a required fix for the affected section unless
  the finding is a style choice that the buyer problem justifies. A
  `facts`-category finding (or any `high`/`critical` finding) blocks
  progression until resolved or explicitly overridden by the user.
- After rewriting, re-run the same command on the fixed text and require
  the re-audit to show the fixing findings resolved or risk reduced
  before moving to platform adaptation.
- Keep the audit report (JSON or Markdown) with the working artifacts so
  the independent audit stage can reference it.

## Non-negotiable boundaries

- Use `armor-memory` for scoped ARMOR retrieval and Router-based saving.
- Use only confirmed company, product, certification, customer, case, market,
  and performance facts. Unknown material facts remain `[TO CONFIRM]` and may
  block progression.
- Keep all external-facing social copy, hashtags, subtitles, and overlays in
  English unless the user explicitly changes the language strategy.
- Include `https://www.armorlighting.com` in every platform variant. Deliver one
  copy-ready `Post Content` block for LinkedIn Posts, Facebook, Instagram, and
  TikTok; keep the CTA, website URL, and hashtags inside that block. For YouTube,
  keep `Title`, `Description`, and `Tags` as separate real fields and place the
  CTA, website URL, and hashtags inside `Description`. Use a verified,
  topic-matched page on the same domain when one is available; otherwise use the
  homepage. Do not replace the website with an email-only, DM-only, or "link in
  bio" CTA. Email and DM may remain secondary contact options.
- Default platforms are LinkedIn, Facebook, Instagram, TikTok, and YouTube.
  ARMOR does not use Twitter/X by default.
- LinkedIn and Facebook require both ARMOR corporate and Lisa personal
  variants. Lisa personal copy uses first person and must not be a mechanical
  rewrite of corporate copy.
- Facebook Company Reels require a separate `Reels Title` of no more than 60
  characters, one copy-ready `Post Content` block, and a separate `Tags` field.
  Tags use plain keyword phrases without `#`, separated by commas or semicolons.
  The one-block rule does not remove these real publishing fields.
- For a local video with existing narration, use an existing non-empty
  transcript first; otherwise extract and transcribe audio only. Do not
  extract frames, screenshots, or thumbnails, and do not run OCR or visual
  analysis by default. Visual inspection requires an explicit user request,
  a task that explicitly needs shot-by-shot visual judgment, or user approval
  after narration proves insufficient. "Do not infer footage" is not
  authorization to inspect the video visually.
- Do not infer video footage. Use only confirmed footage descriptions,
  screenshots, transcripts, or approved shot lists.
- Do not publish, send, change accounts, make commercial commitments, or alter
  canonical knowledge without explicit authority.
- Do not save an approved social deliverable by hand. Use the Router command
  configured in `social-pipeline-config.yaml` and read back the result.

## Pipeline gates

The writer does not self-approve the final audit. A formal social-copy save
requires:

1. a complete Topic Brief and evidence pack;
2. a platform-complete draft with required account variants;
3. an independent audit result of `PASS`;
4. explicit user approval of the Vault file; and
5. status update to `APPROVED_FOR_SAVE` in the same Router-destination file,
   followed by read-back verification.

Publishing or sending the saved content is outside this pipeline and requires
separate approval.

## Compatibility skills

`armor-social-media-workflow` remains available as a subordinate compatibility
skill for legacy platform fields, historical corrections, and the existing
Vault template. It is not the production workflow authority. When it conflicts
with this pipeline, the canonical pipeline files win.

Load `armor-memory` for Vault retrieval/save, `ai-writing-audit` for
AI-style detection during humanization, and
`armor-video-content-rules` when video is in scope. Do not load unrelated
marketing, generic social, design, development, or legacy workflow skills into
the pipeline context.
