# Hermes runtime dispatch — verified 2026-08-17 (pipeline v1.3.4, one full C-store article run)

Operational recipes for driving the ARMOR article pipeline engines from Hermes.
These are Hermes-side execution notes, NOT stage rules — stage rules stay in the
canonical Vault folder.

## 1. Engine invocation (verified working)

- claude (the Enterprise runtime's `claude` executable resolved from `PATH`), non-interactive:
  `claude -p "<prompt>" --allowedTools "Read,Write,Grep,Glob,Bash,WebSearch,WebFetch" --output-format json --dangerously-skip-permissions`
  - Startup noise `(eval):1: can't change option: zle` / `gitstatus failed to initialize` is harmless zsh chaff; ignore it.
  - API error `402 Insufficient Balance` mid-run: no partial artifact is written. User tops up → retry SAME engine in a NEW session (pipeline policy: QUOTA-class failures retry once). This session: first research run died at 48 turns/402; retry succeeded in ~7 min.
- codex (codex-cli 0.146.0), non-interactive:
  `codex exec "<prompt>" --skip-git-repo-check`
  - Longest stage; first final editorial pass ~14–15 min, bounded re-run ~7 min.

## 2. Execution pattern from Hermes

- Work package: `cd /tmp/armor-article/<YYYY-MM-DD_slug>/` first; run each engine with terminal `background=true` + `notify_on_complete=true`.
- `process wait` clamps to 180 s per call — repeat the wait, or poll file timestamps in the work package to gauge progress (Codex writes ai-audit/draft-check JSON early, audit-report.md last).
- Engines write artifacts into the work package; Hermes verifies files itself — never trust CLI exit code alone.

## 3. Stage wall-clock budget (one article, real run)

| Stage | Engine | Time |
|---|---|---|
| 1 Research & Brief | claude | ~5–7 min |
| 2 SEO/GEO Blueprint | claude | ~5 min |
| 3 Blueprint Gate | codex | ~3–7 min per run |
| 4 Draft Article | claude | ~8 min |
| 5 Codex Final Editorial Pass | codex | ~7–15 min |

Full pipeline ≈ 40–70 min wall-clock. SET USER EXPECTATIONS before dispatching;
Licat gets impatient with long autonomous multi-engine runs and may interrupt
mid-wait. Offer a gate-skip / lightweight option when he is present and wants
speed (note the independence trade-off).

## 4. Gate repair loops (verified)

### Blueprint Gate DETAIL_FAIL → PASS
Codex writes `gate-result.json` with precise paths (editorial_thesis,
outline[i].required_points[j], fact_gaps). Producer applies ONLY those bounded
fixes, then re-runs the Gate. Recurring findings seen in practice:
- Overbroad installation claims ("install cost (no electrician)") that contradict
  the blueprint's own power-feed boundary → rewrite conditionally.
- Unsupported superlatives ("the densest margin real estate") → replace with a
  qualified buyer-prioritization judgment.
- Causation without evidence ("display is the margin story") → label as editorial
  inference with limits.
- Unused `[TO CONFIRM]` entries left in blueprint `fact_gaps` → DELETE them;
  the Gate blocks on any live `[TO CONFIRM]`, even unused ones.
- Claims asserted as verified without a mapped source (e.g. IP64 rating) → attach
  the exact source; the ARMOR Product KB CSV `IP_Rating` column confirmed
  HM-PB34BY / HM-PB34BY-5W-M/C = IP64. Grep the CSV before asserting specs.

### Codex Final Pass BLUEPRINT_FAILED from title length (costly, avoidable)
Symptom: deterministic gate BLOCKED on SEO-01 only ("seo_title is 61 characters;
maximum is 60"). Root cause: the blueprint's locked `seo_title` exceeded 60 chars.
SEO-03 requires the article frontmatter title to be CONSISTENT with the blueprint,
and SEO-01 requires ≤60 — both must hold simultaneously.
Fix (bounded, ~7 min re-run, NO article rewrite): patch the SAME ≤60-char title
into BOTH `seo-blueprint.json` and the article frontmatter, then re-run the Codex
final pass with a bounded prompt ("only change was the SEO title") — it re-runs
both checks, recomputes sha256, and updates audit-report.md to PASS.
AVOID UPFRONT: instruct the blueprint producer to keep `seo_title` ≤60 chars
(exact limit lives in the deterministic checker, not in the blueprint standard).

## 5. Router save conventions (verified)

- Router: `cd "$ARMOR_VAULT_ROOT" && bash <profile>/skills/armor-memory/scripts/route.sh --object work-product --domain website --artifact article --json` → returns the configured destination (never hand-construct a path).
- Folder: `2026-08-17_armorlighting_industry_cstore-shelf-lighting` (date_site_type_slug).
- Files: `article.md`, `index.md` (copy of article.md — Vault presentation convention), `article-brief.json`, `seo-blueprint.json`, `audit-report.md`, `draft-check-codex-final.json`, `ai-audit-codex-final.json`.
- Thumbnail image is NOT part of the save (thumbnail_prompt is the executable brief; the image file is a separate asset requirement to flag to the user).
- Read-back: sha256 of saved article.md must equal the Codex-recorded sha; audit-report.md must have all 9 sections with `Final Status: PASS`; zero `[TO CONFIRM]` in body; exactly one H1.
