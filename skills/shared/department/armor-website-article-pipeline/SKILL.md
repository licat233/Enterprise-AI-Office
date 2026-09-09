---
name: armor-website-article-pipeline
description: >
  The single Hermes runtime entrypoint for producing ARMOR website articles
  for armorlighting.com and armordigitalscreen.com. Dispatches topic selection,
  research, Article Brief, SEO/GEO Blueprint, Blueprint Gate, writing, Codex final
  editorial pass, and Router save according to the canonical ARMOR Vault
  Article Production Pipeline runtime enforcement v1.3.4. Do not use legacy article, SEO, or copy
  quality skills as workflow authorities.
license: MIT
metadata:
  hermes:
    tags: [armor, website, article, pipeline, seo, geo, research, audit]
    pipeline_version: "1.3.4"
---

# ARMOR Website Article Production Pipeline

This is the only runtime skill entrypoint for ARMOR website article
production. It is an adapter, not a second copy of the workflow. The canonical
rules and templates live in:

`${ARMOR_VAULT_ROOT}/02-Projects/Workspaces/Content/ARMOR-Content-Operations/ARMOR-Article-Production-Pipeline-v1.3/`

`ARMOR_VAULT_ROOT` is supplied by the Enterprise runtime. Do not replace it
with a host-specific absolute path.

Read the relevant Vault standard for the current stage. Do not invent or
duplicate stage rules in this skill.

## Canonical stage map

| Stage | Read from the canonical Vault folder |
|---|---|
| Task confirmation / dispatch | `armor-article-pipeline.md`, `article-pipeline-config.yaml` |
| Topic selection, only when no topic is supplied | `topic-selection-standard.md` |
| Research and Article Brief | `article-brief-standard.md` |
| SEO/GEO Blueprint | `seo-geo-blueprint-standard.md` |
| Blueprint Gate | `blueprint-gate-standard.md` |
| Writing | `article-writing-standard.md`, `article-frontmatter-standard.md` |
| Codex final editorial pass | `article-audit-standard.md`, `article-pipeline-config.yaml` |
| Executor fallback | `executor-fallback-standard.md` |
| Router save and verification | `armor-article-pipeline.md`, `article-pipeline-config.yaml` |

Use the matching template in the same folder. The four core article artifacts
are only `article-brief.json`, `seo-blueprint.json`, `article.md`, and
`audit-report.md`. Kanban carries state; do not create `task-state.json`.

## Non-negotiable boundaries

- The stable default flow is: intake → research/deduplication → Brief → Blueprint →
  Blueprint Gate → writing → one Codex final editorial pass → Router save.
- The Vault pipeline is authoritative for stages, inputs, outputs, gates,
  states, facts, and save boundaries. Executor or Skill names are configuration,
  not workflow rules.
- Use ARMOR Vault retrieval and the current `armor-memory` Router rules. Never
  guess company facts, product specifications, certifications, customers,
  project results, market coverage, historical data, or quotations. Unconfirmed
  facts remain `[TO CONFIRM]` and may block progression.
- Codex owns the final AI-style, factual-boundary, and deterministic checks in
  the same work round. Do not dispatch a Hermes correction loop or require a
  separate independent auditor. The editor may make bounded repairs without
  changing the confirmed reader decision, factual boundary, or required
  evidence. Heading wording and order remain editorial choices under the v1.3
  structure policy.
- Treat AI-writing scores as diagnostic evidence, never as an authorship claim
  or automatic pass gate. A systemic template failure is `STRUCTURE_FAILED` and
  requires a full rewrite or a return to Blueprint; do not chase a lower score
  with local synonym replacement.
- A deterministic `PASS` is not delivery approval. Before delivery, the Draft
  Gate must independently reject: an introduction that substantially repeats
  the first headed section; unsupported buyer or shopper behavior claims;
  article-roadmap or list-count announcements; and four or more mirrored H3
  spec-tour sections. These are blocking human-editorial gates even when the
  scanner reports no findings.
- Brief and Blueprint must carry the canonical `title_value_contract`. H1 and
  SEO Title must promise a buyer answer, comparison, choice, cost/ROI insight,
  risk diagnosis, practical method, or decision outcome. Questions are
  preferred when they fit search intent but are not mandatory. Keyword-correct
  trend slogans and self-celebratory titles without buyer value fail TITLE-01.
- Every Blueprint must include an executable `thumbnail/hero` image plan, and
  every article must contain a real `thumbnail_prompt`. `NOT_REQUIRED` is
  invalid for thumbnails; the brief must work for AI generation, design,
  image selection, or photography. Additional in-article images remain optional.
- Codex runs `ai-writing-audit` v0.3.1 and the deterministic checker on the
  final article, records the current SHA-256 and result, and repairs bounded
  issues directly. Formal save requires Blueprint Gate PASS, the Codex final
  pass, and no unresolved critical `[TO CONFIRM]`. Save only through the
  configured Router and read back the result. Website publishing is outside
  this workflow and always requires separate user approval.
- Do not load retired cross-channel quality layers, legacy article
  writer/auditor/SEO skills, or generic cross-channel content workflows as
  authorities for this pipeline. If compatibility skills appear in the
  environment, they are subordinate and must not add gates, artifacts, stages,
  or conflicting instructions.

## Loading discipline

Load only the current stage standard and the sources named by that standard.
The Writer does not load the full pipeline, audit rules, Topic Radar, or
unrelated historical articles. The Auditor does not rewrite the article or
silently add facts. Hermes dispatches stages and verifies evidence; it does not
perform the research, writing, or independent audit in one long context.

For detailed examples and implementation records, use the canonical Vault
folder. This skill intentionally contains no duplicate copies of those rules.
