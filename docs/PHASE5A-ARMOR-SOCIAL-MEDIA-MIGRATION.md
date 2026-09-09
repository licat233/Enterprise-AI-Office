---
type: "project-record"
status: "active"
created: "2026-09-09"
updated: "2026-09-09"
---

# Phase 5A — ARMOR Social Media Capability Migration

## Social authority

```text
Vault source reviewed: ARMOR-Social-Media-Production-Pipeline-v2.0 and every referenced stage standard/template
Previous authority: WORKING
Current authority: CANONICAL
Canonicalization: safe after mechanical normalization
Material unresolved decisions: none
```

The Social workflow is internally consistent. Phase 5A promoted the stable
stage-map document after normalizing the lifecycle-neutral Router destination
and removing machine-specific runtime assumptions from the Enterprise Skill.
The material business rules preserved are: the five-platform core contract;
Topic Brief and evidence gates; transcript-first video handling; independent
Social audit; Codex final humanization; explicit user approval before formal
save; and a separate no-publishing boundary.

## Skill migration decisions

| Legacy capability | Decision | Enterprise result |
|---|---|---|
| `armor-social-media-pipeline` | MERGE | One canonical shared Department entrypoint; runtime exposed to Operations |
| `armor-social-media-workflow` | MERGE / REFERENCE_ONLY | Platform fields and corrections are represented by the canonical Vault standards and primary Skill; no competing runtime copy or Profile exposure |
| `armor-video-content-rules` | KEEP | Canonical shared subordinate Skill; reusable for video work without becoming a second Social workflow |

The same-name Legacy global and `social-ops` Profile copies were compared and
were identical for all three inspected capabilities. Legacy Memory, session
history, and private correction state were not inspected or migrated.

## Canonical Social workflow

```text
Intake
→ Topic / Dedup
→ Evidence Pack / Topic Brief
→ Core Draft
→ Humanization + Platform Adaptation
→ Independent Social Audit
→ Required Fixes / Reaudit
→ User Approval
→ Router Save / Read-back
→ Post-publication Performance
```

The core platform contract remains LinkedIn, Facebook, Instagram, TikTok, and
YouTube. LinkedIn and Facebook retain both ARMOR Company and Lisa personal
variants. Social approval is distinct from audit and save; publication or
account actions require separate authorization.

The durable Social package is the smallest contract already required by the
Vault configuration:

```text
required: topic-brief.yaml, core-draft.md, social-copy.md, audit-report.md
optional: video-package.md, subtitles.srt
```

The scoped `save_social_package` operation accepts only those names, resolves
the destination through `work-product + marketing + social-copy`, rejects
Published as editable source, and performs atomic writes plus read-back
verification. The Article four-file contract is unchanged.

## Runtime and permission boundary

Operations receives the canonical Social Skill, canonical video rules, the
existing read-only WeKnora surface, ToolScout, the Firecrawl native read lane,
and the scoped ARMOR Vault MCP. The scoped MCP exposes only:

```text
route_work_product
save_article_package
save_social_package
```

PaddleOCR and Obscura remain installed and healthy but are not exposed because
Social production does not require raw OCR file access or a browser session.
Media Transcription remains the transcript-first path for actual narrated
video input. No publisher, sender, account mutation, or automatic external
publication tool was added.

## Controlled acceptance

The acceptance fixture uses the scoped Product Knowledge facts for the ARMOR
10x10mm Slim Magnetic LED Shelf Light and its magnetic mounting system. It
keeps the factual boundary explicit: magnetic mounting is conditional on a
ferromagnetic shelf surface, and the fixture makes no shelf-manufacturing,
ROI, labor-savings, customer, certification, or performance claim beyond the
source material.

The executed sequence was:

```text
Intake → Topic/Dedup → Evidence Pack / Brief → Core Draft
→ Text-Overlay video package check → Platform Adaptation
→ ai-writing-audit v0.3.1 (armor profile)
→ independent Social quality audit
→ simulated approval boundary (not a real user approval)
→ scoped save_social_package → read-back
```

The fixture checked platform-specific output differences, both account
variants, official website CTA placement, Facebook Reels Title and Tags,
YouTube title and placeholder limits, first-person Lisa copy, buyer-search
hashtags, factual caveats, and absence of publication. It saved under a
temporary Vault root; no production Vault file and no external account were
changed.

## Security and rollback

No secret values were copied or committed. Live Operations configuration and
curated profile manifests were backed up before the Phase 5A change. The
rollback is the recoverable backup under the Hermes backups directory for this
phase plus removal of the Social symlink and the added scoped tool binding.
