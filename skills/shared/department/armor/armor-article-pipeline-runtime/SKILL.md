---
name: armor-article-pipeline-runtime
description: >
  Use when dispatching ARMOR article pipeline engines.
license: MIT
metadata:
  hermes:
    tags: [armor, website, article, pipeline, runtime, claude, codex, router]
    pipeline_version: "1.3.4"
---

# ARMOR Article Pipeline — Hermes Runtime Execution

Companion runtime skill for the canonical ARMOR Article Production Pipeline
v1.3.4 (Vault: `02-Projects/Workspaces/Content/ARMOR-Content-Operations/ARMOR-Article-Production-Pipeline-v1.3/`).
The canonical Vault standards own stages, artifacts, gates, and facts. This
skill owns how Hermes drives the engines, repairs gate failures, and saves.

## Core recipes (full detail in `references/runtime-dispatch.md`)

- **claude (Claude Code)**: `claude -p "<prompt>" --allowedTools "Read,Write,Grep,Glob,Bash,WebSearch,WebFetch" --output-format json --dangerously-skip-permissions`
  - `(eval):1: can't change option: zle` / gitstatus noise at start = harmless.
  - API `402 Insufficient Balance` mid-run = no partial artifact; retry SAME engine, NEW session after user tops up.
- **codex**: `codex exec "<prompt>" --skip-git-repo-check`
- **Pattern**: run each engine with terminal `background=true` + `notify_on_complete=true` from `/tmp/armor-article/<date_slug>/`; `process wait` clamps to 180 s (repeat); verify artifact files yourself, never trust exit codes.

## Time budget — SET USER EXPECTATIONS FIRST

Full run ≈ 40–70 min wall-clock: research ~5–7, blueprint ~5, blueprint gate ~3–7 per run, draft ~8, Codex final pass ~7–15. Licat gets impatient with long autonomous multi-engine runs and may interrupt. Before dispatching, tell him the time budget and offer a gate-skip/lightweight option when he is present (note the independence trade-off).

## Pitfalls that cost re-run cycles (verified 2026-08-17)

1. **SEO Title must be ≤60 chars in the blueprint from the start.** The cap lives in the deterministic checker (SEO-01), not the blueprint standard. A 61-char locked `seo_title` → Codex final pass BLUEPRINT_FAILED (SEO-03 also forces article frontmatter to match the blueprint). Fix = patch the SAME ≤60-char title into BOTH `seo-blueprint.json` and article frontmatter, re-run the final pass with a bounded prompt. No article rewrite needed, but it costs ~7 min. Instruct every blueprint dispatch: `seo_title` ≤ 60 chars.
2. **Delete unused `[TO CONFIRM]` entries from blueprint `fact_gaps` before the Blueprint Gate** — the Gate blocks on any live `[TO CONFIRM]`, even ones the outline never uses.
3. **Asserted-verified spec claims need a mapped source** (e.g. IP64): grep the ARMOR Product KB CSV (`IP_Rating` column) before asserting; HM-PB34BY / HM-PB34BY-5W-M/C verified IP64.
4. **Blueprint Gate DETAIL_FAIL repair loop**: codex writes `gate-result.json` with exact paths (`editorial_thesis`, `outline[i].required_points[j]`, `fact_gaps`); producer applies ONLY those bounded fixes, then re-gates. Recurring findings: overbroad "no electrician" claims, unsupported superlatives ("densest margin real estate"), causation without evidence ("X is the margin story" — relabel as inference).

## Router save conventions

`cd "$ARMOR_VAULT_ROOT" && bash <profile>/skills/armor-memory/scripts/route.sh --object work-product --domain website --artifact article --json` → the Router-selected destination. Folder and artifact rules come from the current Vault pipeline. Do not hand-construct a host-specific Vault path. Read back the saved artifact and verify the recorded hash, audit result, and unresolved `[TO CONFIRM]` status.
