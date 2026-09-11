---
name: armor-video-content-rules
title: ARMOR Video Content Production Rules
category: brand
author: Licat
description: Platform-specific rules, pitfalls, and workflows for ARMOR social video content. Covers voiceover decisions, text overlay design, SRT generation, YouTube publishing rules, and multi-platform completeness checks. Supplements armor-social-media-pipeline for video-specific work.
version: 1.0.0
---

# ARMOR Video Content Production Rules

Session-hardened rules for short-form video production across TikTok, Reels, Shorts, and YouTube.

Use the current ARMOR Vault facts before writing video scripts, titles, captions,
or overlays. This skill owns video-specific formats, limits, and acceptance.

## Existing Narrated Video: Source Priority

When the user supplies a finished local video that already contains narration,
use this order by default:

1. Read an existing non-empty transcript in the expected same-stem location.
2. If none exists, extract and transcribe the audio track only.
3. Use the exact filename stem and the user's footage description as supporting
   context.

Do not extract video frames, create screenshots or thumbnails, run OCR, or use
visual analysis by default. Those actions are permitted only when the user
explicitly asks for visual verification, when the requested deliverable
explicitly requires shot-by-shot visual judgment, or when narration is
insufficient and the user approves visual inspection. A requirement to avoid
inventing footage is not permission to inspect frames.

## Voiceover vs Text Overlay Decision

**Always ask the user first.** Don't assume either way.

| Approach | Best for | Example |
|----------|----------|---------|
| Voiceover | Complex products, B2B explanation, storytelling | ESL market trend video with data narration |
| Text overlay only | Simple visual demos, product-first showcases, global audience | Hand-held product showcase with installation demo |
| Hybrid | Key numbers reinforced on screen while narrating | Voiceover + "$2B → $7B" data overlay |

### When User Chooses No Voiceover

Design a **text overlay sequence** instead:

1. Each card maps to one specific video moment
2. One idea per card — max 8 words
3. Opening card: hook (benefit or curiosity)
4. Middle cards: features tied to what's on screen
5. Closing card: memorable 3-word summary or brand name
6. Font: sans-serif bold, white with shadow/outline
7. Animation: fade-in/fade-out only — no bouncing or sliding
8. Timing: 2-3 seconds per card, synced to visual transitions

### When User Wants Voiceover

Provide:
1. Full voiceover as a **standalone copy-paste block** (for recording or AI TTS)
2. Script breakdown table: timestamp → visual → text overlay → voiceover
3. SRT subtitle file
4. Editing notes (pacing, music level, visual moments)

## Music Guidelines

- **With voiceover**: music at -15 to -20dB, instrumental only, no lyrics
- **Without voiceover**: music at moderate volume — becomes the pacing driver
- Style: "minimal tech," "modern corporate," or "cinematic ambient" for B2B
- Source: CapCut built-in library (search "modern," "tech," "minimal")

## YouTube Publishing Rules

### No Square Brackets

YouTube descriptions and captions **reject square brackets `[ ]`** as invalid characters. Any `[placeholder]` text causes upload failure or text stripping. Use plain text or "link in bio" style CTAs.

**This is YouTube-specific** — other platforms accept brackets.

### YouTube Shorts Title Format

`Primary Keyword + Pain Point/Value Hook + Brand Name`

- 60 characters or less when possible
- Primary keyword near the beginning
- End with brand name for recall
- Provide 2-3 alt title options for A/B testing

### YouTube Description

- First 100 characters appear before "more" fold — lead with value proposition
- Include full spec list (YouTube is a search engine — descriptions rank)
- 3-5 hashtags at the end
- No brackets anywhere

## SRT Subtitle Rules

1. One `.srt` file per video, saved in the same folder as the `.md`
2. Filename: `YYYY-MM-DD_Topic_Subtitles.srt`
3. First 0-3 seconds: no subtitle entry (silent hook / visual-only intro)
4. Each entry: max 2 lines, max ~42 characters per line
5. Sync to voiceover timestamps, not text overlay timestamps
6. Standard SRT format: sequence number → `HH:MM:SS,mmm --> HH:MM:SS,mmm` → text → blank line

## Platform Completeness Check

**Before delivering multi-platform content, verify all specified channels are covered.**

Common mistake: listing YouTube Shorts in frontmatter but forgetting to write the YouTube-specific section (title, description, SEO notes). YouTube requires more structure than TikTok/Reels — it's not just a caption.

Checklist for each deliverable:
- [ ] TikTok caption
- [ ] Reels caption (may differ from TikTok)
- [ ] Shorts caption
- [ ] YouTube title + description + SEO notes
- [ ] LinkedIn post (with summary blockquote for ARMOR)
- [ ] Instagram caption
- [ ] Facebook caption

If frontmatter lists a channel, there must be a section for it.

## Pitfalls

### VP1: Don't assume video footage contents

**Trigger:** Writing a video script breakdown with timestamps.
**Fix:** Before writing shot-by-shot directions, confirm with the user what the video actually contains. Don't assume close-ups, side-by-side comparisons, or specific angles exist.

### VP2: Don't push product CTAs on trend/insight posts

**Trigger:** Writing an industry insight or market trend post.
**Fix:** Use engagement questions as CTAs, not "DM us" or "link in bio." The post should read like industry commentary, not a sales pitch.

### VP3: English text for English-speaking platforms

**Trigger:** Adding text overlays or on-screen text to video for international platforms.
**Fix:** All text overlays on TikTok, Reels, Shorts, YouTube must be in English. Chinese text on English-narrated/English-audience video creates a language mismatch that confuses viewers.

## Changelog

- 2026-08-11: Added narration-first source priority and prohibited default
  frame extraction, screenshots, OCR, and visual analysis.
