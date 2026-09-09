---
name: skills-to-vault-sync
title: Skills-to-Vault Synchronization Pattern
category: brand
author: hermes
description: "Pattern for syncing rich operational knowledge from Hermes skills into Obsidian vault so all agents (Hermes, Codex, Claude Code) share the same knowledge. Use when vault stubs are thinner than skill content, when setting up multi-agent vault access, or during vault hygiene audits."
version: 1.0.0
---

# Skills-to-Vault Synchronization Pattern

> When Hermes skills hold richer operational content than Obsidian vault files, other agents sharing the vault cannot access Hermes skills. This creates a knowledge asymmetry: Hermes works well, other agents work with stubs.

## When to Use This Skill

- Setting up multi-agent Obsidian vault (Hermes + Codex + Claude Code)
- Vault audit reveals thin/stub files in `02-Rules/` or other layers
- User says "other agents should know this too" or "put this in the vault"
- Content production quality differs between agents
- After a migration that created minimal stub files

## The Problem

During V7.1 migration (2026-06-06), profile files like `Profile-web-ops.md` and `Profile-social-ops.md` were migrated into `02-Rules/Content-Standards/`. The migration created **minimal stubs** (35-50 lines each). Meanwhile, Hermes skills retained **full operational detail** (500+ lines) from iterative refinement.

**Result:** Skills = rich operational knowledge. Vault stubs = skeleton outlines. Other agents see only skeletons.

## Detection

Compare vault `02-Rules/Content-Standards/` files against corresponding skills:

| Vault File | Lines | Corresponding Skill | Lines | Gap |
|---|---|---|---|---|
| `Content-Rules.md` | 51 | `armor-content-writing` | 500+ | Missing: 10-step workflow, SEO audit (14 items), link verification, anti-fabrication, product writing patterns |
| `Social-Media-Video.md` | 49 | `armor-social-media-workflow` + `armor-video-content-rules` | 300+ | Missing: SRT rules, voiceover reqs, full script template |
| `Social-Media-LinkedIn.md` | 42 | `armor-social-media-workflow` | ~60 | Missing: hashtag strategy, CTA matching, carousel format |
| `Social-Media-YouTube.md` | 35 | `armor-social-media-workflow` | ~50 | Missing: Shorts rules, SEO description rules |
| ❌ Facebook/Instagram/TikTok/Platform-Rules | 0 | `armor-social-media-workflow` | ~190 | **Files don't exist** |

## What to Sync (Priority)

**High priority** (operational workflows other agents need):
- Complete step-by-step workflows (e.g., 10-step article pipeline)
- Audit checklists (e.g., 14-point SEO audit)
- Mandatory gates (e.g., link verification, humanizer pass)
- Platform-specific rules (character limits, hashtag counts, CTA patterns)
- Anti-fabrication rules
- Product writing patterns

**Medium priority** (reference detail):
- Image prompt templates
- Frontmatter format examples
- Pitfall collections

**Low priority** (Hermes-specific, don't sync):
- Skill tool references (skill_view, skill_manage)
- Hermes memory tool usage
- Internal routing between skills

## What NOT to Sync

- Skill meta-structure (YAML frontmatter, category, related_skills)
- References to other skills (replace with inline content)
- Hermes-specific tool commands

## Fix Workflow

### Standard Sync (enrich existing vault files)

1. **Load the skill** — `skill_view(name='armor-content-writing')` (or relevant skill)
2. **Read the existing vault file** — understand what's already there
3. **Identify gaps** — compare sections in skill vs sections in vault file
4. **Enrich the vault file** — add missing operational detail from skill, preserving existing vault frontmatter and changelog
5. **Create missing vault files** — for platforms/topics with no vault file, create with full V7.1 frontmatter
6. **Update frontmatter** — bump `revision`, set `updated` date, update `source` to include the skill name

### Gap Analysis Workflow (audit all skills vs vault)

When the user asks "what else could go in the vault" or during a vault hygiene audit:

1. **Scan all armor-* skills** — `skills_list` + `skill_view` for each
2. **Scan vault 01-Facts/ and 02-Rules/** — `search_files` to get current coverage
3. **Compare** — for each skill, check if its knowledge already exists in vault:
   - Brand/Company/Product facts → `01-Facts/`
   - Content standards, platform rules → `02-Rules/Content-Standards/`
   - Agent behavior rules → `02-Rules/Agent-Rules/`
   - Tool discipline → `02-Rules/Architectural-Discipline/`
4. **Classify gaps**:
   - **High priority**: Operational workflows other agents need daily (writing rules, platform standards)
   - **Medium priority**: Reference detail (templates, pitfall collections)
   - **Low priority**: Hermes-specific internals (skill routing, memory tool usage)
5. **Present table to user** with priority ratings — don't self-authorize batch writes
6. **Execute approved writes** — one file at a time via `write_file`, preserve frontmatter

### Non-ARMOR Knowledge Sync

The vault isn't only for ARMOR business knowledge. Machine infrastructure, tool patterns, and agent coordination knowledge also belong in the vault:

| Knowledge Type | Vault Location | Example |
|---|---|---|
| Machine shell environment | `02-Rules/Agent-Rules/Shell-Environment-Architecture.md` | PATH layers, fnm init, Hermes bash bridge |
| Tool usage patterns | `02-Rules/Agent-Rules/` or `02-Rules/Architectural-Discipline/` | Web scraping fallback chain, defuddle for anti-bot |
| Agent coordination | `02-Rules/Agent-Rules/` | Profile responsibilities, port assignments, notification channels |
| Platform integration | `02-Rules/Platform-Standards/` | MIC standards, Feishu message format |

When syncing non-ARMOR knowledge, follow the same V7.2 frontmatter and write_policy rules.

## Vault Routing for Synced Content

Synced operational knowledge goes to `02-Rules/` (Class B or A depending on content):
- Writing standards → `02-Rules/Content-Standards/`
- Platform-specific social rules → `02-Rules/Content-Standards/Social-Media-{Platform}.md`
- Cross-platform rules → `02-Rules/Content-Standards/Social-Media-Platform-Rules.md`
- Product writing patterns → `02-Rules/Content-Standards/` or `03-Insights/Products/`

## Related Skills

- `obsidian-ai-memory-architecture` — Full vault management, routing, migration
- `armor-content-writing` — Source of article/SEO operational knowledge
- `armor-social-media-workflow` — Source of social media operational knowledge

## Pitfalls

- **Don't blindly copy-paste skill content into vault.** Skills reference other skills (e.g., "load humanizer skill"). In the vault, replace these with inline content or vault file paths.
- **Don't overwrite vault frontmatter.** Preserve the existing governance frontmatter (type, memory_layer, status, write_policy). Only enrich the body content.
- **Skills evolve faster than vault.** After syncing, note the skill version in the vault file's `source` field. During quarterly audits, re-check for new content added to skills.
- **Batch size matters when delegating.** When syncing 5+ files, `delegate_task` with large context payloads can hit stream timeouts. Write files directly via `write_file` one at a time instead of delegating a mega-task. Each file should be under ~10K tokens.
- **Memory limit when scanning skills.** Scanning all skills + vault in one turn can flood context. Use `skills_list` first for a lightweight inventory, then `skill_view` only for skills that likely have vault-relevant content. Skip skills that are clearly agent-internal (e.g., `hermes-agent`, `skill-authoring`).
- **Don't write without user approval.** After gap analysis, present the findings as a prioritized table and let the user choose which items to sync. "怎么做" = wants plan/options, not execution.
- **Update the gap analysis table after sync.** The detection table above is a point-in-time snapshot. After completing a sync, update the vault file line counts and mark gaps as resolved so the next audit starts clean.
