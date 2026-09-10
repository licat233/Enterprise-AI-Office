# Enterprise AI Office — Phase 5C

## Remaining ARMOR Skills Gap Audit & Migration Wave Plan

Date: 2026-09-10
Repository baseline: `59d3a9c371f233adb10ee2b3eb6bf4d978a74038`
Repository branch: `codex/media-transcription`
Audit repository HEAD: `197f65a8a3dae3826b3132c73bb1cd135fda58dc`
Phase 5C audit starting point after Phase 5B.2: `197f65a8a3dae3826b3132c73bb1cd135fda58dc`

The historical project baseline above remains unchanged; the audit HEAD is
the clean post-Phase-5B.2 repository state from which the Phase 5C findings
were made.

## Decision

Phase 5C is complete as an audit and planning phase. No Legacy Skill was
copied, reactivated, enabled, or rewritten. No Legacy Profile was copied and
no Legacy Hermes Memory, session history, conversation history, or private
remembered data was inspected.

The three highest-priority production workflows remain the current Enterprise
Article, Social, and MIC entrypoints. The meaningful remaining ARMOR business
gaps are two P1 candidates:

1. a website product-materials / product-page source-and-media package; and
2. an ARMOR product-visual production workflow carrying the verified LED/ESL
   anti-moiré guidance into an approved, governed asset-generation boundary.

The Legacy Agent Delegate / Multi-Agent Orchestration implementation is not a
business Skill migration candidate. It remains an explicit experimental hold:

```text
Multi-Agent Orchestration: EXPERIMENTAL_HOLD
Agent Delegate migrated: NO
Operations delegation: OFF
Default enabled: NO
```

The distinction between workflow semantics and runtime implementation is
preserved. Article and Social retain selected fallback and independent-audit
semantics where their current standards require them; that does not absorb or
enable the Legacy Worker/Auditor Profiles or the Delegate runtime.

## Method and evidence boundary

The read-only Legacy scan used `/Users/licat/.hermes/skills/` and the six
specified Profile roots under `/Users/licat/.hermes/profiles/`. Active counts
followed links and counted `SKILL.md` leaves while excluding `.archive`,
`.curator_backups`, hidden directories, backups, and inactive roots. Each
resolved Skill directory was identified by real path, source kind, and a
SHA-256 identity of its `SKILL.md`; a matching name was not treated as a
matching implementation.

The scan used only Skill files, their references/scripts/templates, Profile
configuration and generated role metadata, current Enterprise files, current
Vault standards, and the repository history needed to establish lineage. The
Legacy archive was recorded but not counted as active exposure. The archive
contains 29 `SKILL.md` files, including the old Social stage bundle; those
files are not migration evidence for active Profile exposure.

No Legacy Memory was opened. In particular, this audit did not read Hermes
Memory databases, `.hermes_history`, session or conversation records, logs,
private remembered facts, or old correction patches.

## Inventory totals

The required machine-readable inventory is
`docs/inventory/legacy-operations-skills-triage.csv`. It is deduplicated by
resolved implementation identity, while `exposure_count` and the comma-
separated `legacy_profile` field preserve every audited Profile exposure.

| Scope | Count |
|---|---:|
| Active global Legacy `SKILL.md` leaves, nested links followed | 384 |
| Active global Legacy `SKILL.md` leaves, direct non-following comparison | 380 |
| Active global unique Skill names | 293 |
| Archived `SKILL.md` leaves, excluded from active count | 29 |
| Six-Profile raw active exposures | 460 |
| Six-Profile resolved Skill implementations after de-duplication | 432 |
| Cross-Profile duplicate exposure slots | 28 |
| CSV rows including one global-only Delegate guide | 433 |

### Profile exposure accounting

| Legacy Profile | Raw exposures | Resolved implementations | Resulting treatment |
|---|---:|---:|---|
| `web-ops` | 110 | 110 | Article capability migrated; product-materials gap is P1 |
| `social-ops` | 92 | 92 | Social/video capability migrated; remaining items are absorbed, generic, or held |
| `mic-ops` | 153 | 153 | MIC capability migrated; historical source/fill/audit modules absorbed |
| `design-ops` | 97 | 97 | Partially migrated; ARMOR visual-production gap is P1 |
| `armor-fallback-content-worker` | 4 | 4 | `EXPERIMENTAL_HOLD`, role `DELEGATE_WORKER` |
| `armor-independent-auditor` | 4 | 4 | `EXPERIMENTAL_HOLD`, role `DELEGATE_AUDITOR` |
| **Total** | **460** | **432** | Profile runtime is not migrated or exposed |

### Classification totals

The following counts are rows in the deduplicated CSV, not raw Profile
exposure slots. They include 432 Profile-resolved rows and one global-only
orchestrator guide.

| Classification | Rows | Meaning in this audit |
|---|---:|---|
| `MIGRATED` | 17 | Current Enterprise capability is the governed operational entrypoint |
| `ABSORBED` | 6 | Meaningful semantics are already owned by a current workflow/standard; no direct copy needed |
| `KEEP_MIGRATE` | 2 | A real ARMOR business gap remains; planned migration only |
| `REFERENCE_ONLY` | 21 | Useful context or generic method, but not an ARMOR runtime capability |
| `EXPERIMENTAL_HOLD` | 16 | Agent Delegate/runtime or related executor lane; do not migrate or expose |
| `DO_NOT_MIGRATE` | 370 | Commodity, machine-specific, administrative, risky, or superseded implementation |
| `DUPLICATE` | 1 | Superseded implementation with an explicit current equivalent |
| **Total** | **433** | **All seven required classes represented** |

## Current Enterprise coverage

### Article

`armor-website-article-pipeline` is the current canonical Enterprise entrypoint
and is active in the deployed Operations Profile. The current Article Vault
standards already absorb the useful historical topic-selection, deduplication,
scoring, SEO/GEO blueprint, fact-boundary, writing, audit, frontmatter, and
fallback semantics. The current lifecycle is Research/Brief → SEO/GEO
Blueprint → Blueprint Gate → Draft → one Codex Final Editorial Pass → scoped
Router save. The old multi-stage `armor-content-pipeline` runtime is not
reactivated; its direct orchestration, old paths, and old write behavior are
superseded.

### Social and video

`armor-social-media-pipeline` and `armor-video-content-rules` are current
Enterprise entrypoints and are active in Operations. The historical
`armor-social-media-workflow` is subordinate compatibility material and is
classified `ABSORBED`. Social v2 owns topic signals/deduplication, evidence,
drafting, humanization, platform adaptation, independent Social audit,
approval, and scoped Router save. The archived Social stage bundle is not
counted as active exposure.

### MIC

`armor-mic-product-optimization` and the active `mic-optimization-guide` are
current Enterprise capability entrypoints. The canonical Vault standard owns
the detailed MIC source hierarchy, field rules, fact classes, blockers,
approval, and artifact semantics. `mic-product-fill`, `mic-product-audit`,
`mic-product-detail-page`, and `mic-upload-data-sources` are useful historical
modules whose safe semantics are absorbed by the canonical MIC adapter and
standard; their live browser/fill side effects are intentionally not migrated.

### Shared control plane and knowledge boundary

The deployed Operations Profile has scoped WeKnora retrieval, ToolScout,
Firecrawl MCP, and the Scoped ARMOR Vault Router. `armor-memory` is not
enabled in Operations; the scoped Router is the only governed save boundary.
The current Article, Social, and MIC packages preserve review and read-back
gates. `ai-writing-audit v0.3.1` is an editorial audit aid and does not outrank
source authority.

## Explicit historical capability resolution

These names were specifically requested for resolution, whether or not an
active Skill with that exact name remains in the audited Profiles.

| Historical capability | Resolution | Evidence-based current status |
|---|---|---|
| `armor-topic-recommendation` | `ABSORBED` | Article topic-selection standard covers explicit-topic handling, recent deduplication, funnel/social gaps, campaign alignment, product mapping, candidate scoring, and recommendation output. |
| `armor-topic-radar` | `ABSORBED` | Article topic-selection and Social topic-signal standards preserve scan, deduplication, and scoring semantics; no standalone legacy radar runtime is required. |
| `armor-content-writing` | `ABSORBED` | Article/Social writing and humanization standards plus source/fact boundaries cover the useful method. |
| `agent-seo-research` | `ABSORBED` | Article Research/Brief and SEO/GEO Blueprint stages own the governed research-to-blueprint path. |
| `agent-content-writer` | `ABSORBED` | Current Article and Social writers are the governed workflow stages. |
| `agent-content-auditor` | `ABSORBED` | Article final editorial checks and Social independent audit/reaudit own the required review semantics. |
| `agent-geo-entity` | `ABSORBED` | The Enterprise repository contains the same implementation identity as the Legacy copy, but it is disabled as a standalone Operations Skill; its valid semantics are in the Article SEO/GEO Blueprint. |
| `agent-knowledge-growth` | `ABSORBED` | Safe persistence is provided by the scoped Router and governed Article/Social/MIC package flows; the old Obsidian graph writer is not migrated. |
| `armor-business` | `ABSORBED` | Current Brand, Product, and Vault knowledge boundaries replace the historical bundle; no active standalone runtime is required. |
| `armor-brand-guidelines` | `ABSORBED` | Canonical ARMOR Brand knowledge and current brand-content rules are the source of truth. |
| `armor-article-frontmatter` | `ABSORBED` | Article frontmatter is owned by the current Article package/standard. |
| `armor-content-pipeline` | `DO_NOT_MIGRATE` | The seven-stage legacy orchestrator is a superseded runtime with historical paths, direct delegation, and unsafe write assumptions; its useful stage semantics are distributed across current governed workflows. |
| `armor-daily-browser-setup` | `DO_NOT_MIGRATE` | Machine/session/account setup for WP and MIC inboxes; administrative and account-bound, not an Enterprise business Skill. |

## Additional ARMOR-specific findings

| Capability | Classification | Priority | Gap decision |
|---|---|---:|---|
| `website-product-materials` | `KEEP_MIGRATE` | P1 | Product source-folder reconciliation, product-page copy package, SEO structure, source review, and media planning are not the same contract as an Article package or MIC package. |
| `design-image-prompt-engineer` with `references/armor-anti-moire-guide.md` | `KEEP_MIGRATE` | P1 | The ARMOR-specific LED/ESL/retail anti-moiré guidance is meaningful, but the Enterprise copy is not Operations-enabled and there is no governed ARMOR product-visual production wrapper. |
| `armor-article-pipeline-runtime` | `DUPLICATE` | — | Legacy Article runtime companion is superseded by `armor-website-article-pipeline`; it is not directly activated. |
| `armor-social-media-workflow` | `ABSORBED` | — | Historical compatibility rules remain subordinate to the current Social pipeline. |
| `mic-product-fill`, `mic-product-audit`, `mic-product-detail-page`, `mic-upload-data-sources` | `ABSORBED` | — | Their safe data-preparation and audit semantics are in the canonical MIC adapter/standard; live-edit behavior remains disabled. |

Generic research, marketing, SEO, competitor, product-trend, coding, browser,
office, PDF, image utility, and agent-runtime Skills were included in the
full exposure accounting but were not promoted to ARMOR migration backlog
items. They are marked `REFERENCE_ONLY`, `DO_NOT_MIGRATE`, or
`EXPERIMENTAL_HOLD` in the CSV according to their actual source and risk.

## Design Ops review

`design-ops` exposes 97 active resolved implementations. The cluster is mostly
generic design roles, public prompt/image/HTML utilities, UI/UX helpers,
prototype workflows, and machine-specific diffusion or browser tooling. The
only clearly ARMOR-specific production knowledge found in the audited active
cluster is `armor-anti-moire-guide.md`, covering LED/ESL/retail product prompt
guidance, moiré negative prompts, close-up/clean-background presentation, and
post-processing considerations. The referenced texture-cleaning script was
not present as a governed Enterprise runtime dependency.

Two generic Enterprise design roles are already enabled in Operations:
`design-brand-guardian` and `design-ux-researcher`. That makes Design Ops
partially migrated, not fully migrated. A future visual-production workflow
must first define approved image/media tools, Product/Brand source and claim
gates, output/QA rules, and publication boundaries. It must not be created by
bulk-copying the public Legacy design bundle or by installing ComfyUI/GPU
dependencies as part of this phase.

## Legacy Agent Delegate / Multi-Agent Orchestration audit

The two named Profiles are core runtime components, not historical content
helpers. Their Profile status is therefore kept separate from any absorbed
Article/Social workflow semantics.

### Reconstructed implementation

```text
Hermes Profile with built-in orchestrator
  delegation.orchestrator_enabled: true
  kanban.dispatch_in_gateway: true
  kanban.auto_decompose: true
  kanban.orchestrator_profile: ""
        ↓
delegate_task / Kanban task card
  parent/dependency state + assignee/worker selection
        ↓
armor-fallback-content-worker Profile
  role: DELEGATE_WORKER
        ↓
Codex or Claude Code executor lane
  coding-agent-delegation + codex.md / claude-code.md
  kanban-codex-lane isolates execution; Hermes reconciles/tests/accepts
        ↓
armor-independent-auditor Profile
  role: DELEGATE_AUDITOR
        ↓
audit / Required Fixes / re-audit
  Kanban worker handoff and kanban_complete result metadata return to Hermes
```

| Component | Legacy evidence inspected | Finding | Final status |
|---|---|---|---|
| Orchestrator Profile/config | `profiles/{web-ops,social-ops,mic-ops,design-ops}/config.yaml` | No separate named orchestrator Profile was configured. Each relevant Profile has built-in orchestrator settings, with `orchestrator_profile: ""`, gateway dispatch, auto-decomposition, bounded concurrency, and one spawn depth. | `EXPERIMENTAL_HOLD` |
| Delegate worker Profile | `profiles/armor-fallback-content-worker/{profile.yaml,config.yaml,SOUL.md}` | ARMOR fallback worker for research, Blueprint, writing, and Required Fixes; uses a separate Profile boundary and Codex provider configuration. | `EXPERIMENTAL_HOLD`; role `DELEGATE_WORKER`; Enterprise migration `NO`; Operations exposure `NO` |
| Independent auditor Profile | `profiles/armor-independent-auditor/{profile.yaml,config.yaml,SOUL.md}` | Separate auditor for Blueprint Gate, Draft Audit, and Final Reaudit; explicitly kept separate from Writer context. | `EXPERIMENTAL_HOLD`; role `DELEGATE_AUDITOR`; Enterprise migration `NO`; Operations exposure `NO` |
| Delegation Skills | `autonomous-ai-agents/coding-agent-delegation`, `kanban-system`, `kanban-orchestrator`, `kanban-worker`, `kanban-codex-lane` | Documents the delegation, worker lifecycle, isolated executor lane, acceptance, retry, and handoff semantics. | `EXPERIMENTAL_HOLD` |
| Codex binding | `coding-agent-delegation/references/codex.md`, active `codex`, `kanban-codex-lane` | Codex CLI/worktree execution is a selectable subordinate lane; Hermes retains board ownership and acceptance. | `EXPERIMENTAL_HOLD` |
| Claude Code binding | `coding-agent-delegation/references/claude-code.md`, active `claude-code` | Claude Code is a separate subordinate technical lane; nested dispatch is constrained by the role instructions. | `EXPERIMENTAL_HOLD` |
| Worker/executor selection | delegation config, Kanban references, `default_assignee: ""` | Selection follows task/assignee and executor-lane rules; no Enterprise Operations selection rule is enabled. | `EXPERIMENTAL_HOLD` |
| Fallback | worker/auditor `fallback_model`, `executor-fallback-standard`, old pipeline fallback rules | Same-engine retry, verified fallback switch, and fail-closed blocked-executor behavior are documented. The semantic portion is selectively absorbed by current Article rules; the Profile/runtime implementation is not. | Runtime `EXPERIMENTAL_HOLD` |
| Audit return flow | `kanban-system` worker/orchestrator references and Article audit stages | Audit/Required Fixes/re-audit returns through worker handoff and `kanban_complete` summary/metadata. No separate explicit return script was found. | `EXPERIMENTAL_HOLD` |
| Kanban/task state | `kanban-system`, `kanban-codex-lane`, `config.yaml` Kanban blocks | Gateway dispatch, parent/dependency graph, ready/todo/blocked lifecycle, retry/recovery, and Hermes acceptance are part of the runtime substrate. | `EXPERIMENTAL_HOLD` |
| Global orchestrator guide | `agency-agents-armor/06-specialized/agents-orchestrator/SKILL.md` | Generic orchestration planning guide exists in the global pool but is not exposed by the six audited Profiles. | `EXPERIMENTAL_HOLD`; global-only |

The Legacy implementation is therefore a runtime/configuration capability, not
a stable Enterprise business workflow. It is not migrated, not enabled, not
exposed to Operations, and not a default trigger. Operations currently
disables the `delegation` toolset and has no fallback/auditor/orchestrator
Profile, Codex/Claude binding, or Kanban Skill exposure.

## Migration wave plan — KEEP_MIGRATE only

No P0 item was found. The following are planning items only; this phase does
not implement them.

### P1 — ARMOR website product-materials / product-page package

- **Legacy source:** `web-ops` `website-product-materials` Skill and its
  references.
- **Business capability:** reconcile product source folders; prepare a
  product-page copy/SEO structure, source review, and media plan.
- **Why it remains a gap:** the Article contract produces an article package;
  the MIC contract produces MIC optimization data and optional detail-page
  content. Neither is a website product-page/materials package.
- **Destination:** a future ARMOR-specific website product-materials workflow
  under the current Enterprise department skills and the existing scoped
  Router, with an explicitly defined artifact contract.
- **Tools/dependencies:** approved Vault retrieval, current Product/Brand
  knowledge, Firecrawl or another approved retrieval path where appropriate,
  document/OCR tooling when source files require it, and the existing scoped
  Router only after review. No new credential is implied.
- **Risk and controls:** draft-only until user review; no direct website
  publication, CMS mutation, or external messaging. Exact product facts remain
  source-backed and unresolved values remain blocked.
- **Knowledge dependency:** canonical ARMOR Product and Brand Vault content.
- **Acceptance gates:** artifact schema, source traceability, product/media
  completeness, claim/fact audit, human approval, scoped save, and read-back.

### P1 — ARMOR product-visual production wrapper

- **Legacy source:** `design-image-prompt-engineer` and
  `references/armor-anti-moire-guide.md`, exposed through `design-ops` and
  `mic-ops`.
- **Business capability:** produce governed ARMOR LED/ESL/retail product
  visual prompts/assets with anti-moiré and presentation-quality rules.
- **Why it remains a gap:** the Enterprise repository contains the guide and a
  disabled copy, but Operations has no approved image-generation/vision
  binding and no complete ARMOR visual asset contract or QA workflow.
- **Destination:** a future ARMOR product-visual workflow, not a direct copy
  of the generic Legacy design bundle.
- **Tools/dependencies:** an explicitly approved image/media tool and current
  Product/Brand source gates; optional machine-specific diffusion/GPU tooling
  would require separate approval and is not part of this phase. No install or
  credential change is authorized here.
- **Risk and controls:** visual generation must not invent hidden technical
  parameters, certifications, performance claims, or product geometry; no
  automatic publication. Product identity, source facts, brand rules, asset
  QA, and human approval must be explicit.
- **Knowledge dependency:** canonical ARMOR Brand and Product Vault content,
  plus the anti-moiré reference.
- **Acceptance gates:** approved tool boundary, prompt/asset artifact schema,
  visible-vs-inferred fact rules, anti-moiré QA, source traceability, review,
  and publication boundary.

These two items are the only `KEEP_MIGRATE` rows in the inventory. Their
future design should not enable Agent Delegate or broaden Operations
permissions.

## Profile and runtime disposition

| Capability/Profile | Enterprise migration | Operations exposure | Default |
|---|---|---|---|
| `web-ops` Article semantics | YES, through current Article | Current Article entrypoint only | governed |
| `social-ops` Social/video semantics | YES, through current Social/video | Current Social/video entrypoints only | governed |
| `mic-ops` MIC semantics | YES, through current MIC | Current MIC entrypoint only | governed |
| `design-ops` generic brand/UX subset | Partial | Current approved generic roles only | governed |
| `armor-fallback-content-worker` | NO | NO | disabled |
| `armor-independent-auditor` | NO | NO | disabled |
| Legacy Agent Delegate / Multi-Agent Orchestration | NO | OFF | NO |

The deployed Operations config records `memory_enabled: false`, an empty
external Skill directory list, disabled `delegation`, disabled host-side
execution surfaces, and a closed current tool allowlist. No permissions,
Profile architecture, Router contract, or publication boundary was changed by
Phase 5C.

## Regression and acceptance checks

The following checks are required after the inventory/report files are placed
in the repository:

```text
python3 scripts/phase5c_operations_skills_triage_check.py \
  --runtime-config /Users/armor/.hermes/profiles/operations/config.yaml \
  --operations-skills-root /Users/armor/.hermes/profiles/operations/skills
python3 scripts/phase4a_migration_check.py
python3 scripts/phase4b_runtime_check.py
python3 scripts/phase4c_runtime_check.py
python3 scripts/phase5a_social_runtime_check.py
python3 scripts/phase5b_mic_runtime_check.py
python3 scripts/test_phase5b1_mic_authority.py
python3 scripts/test_phase5b2_mic_authority_dedup.py
scripts/repository-readiness-check.sh
git diff --check
```

The Phase 5C checker is intentionally small and stdlib-only. It verifies the
CSV schema and seven-class vocabulary, all 460 active Profile exposure slots,
the expected per-Profile counts, valid KEEP priorities, explicit Delegate
hold rows, the report decisions, and the deployed Operations delegation and
Memory-off boundaries. It does not inspect Legacy Memory.

## Scope result

```text
Phase 5C: PASS
Meaningful ARMOR business gaps: 2 P1 planning items
Bulk Skill migration: NO
Legacy Profile copy: NO
Legacy Memory accessed: NO
Agent Delegate migrated: NO
Operations delegation: OFF
Default enabled: NO
MIC artifact contract changed: NO
MIC Router contract changed: NO
Operations permissions changed: NO
```

Commit and push status are recorded in the final task handoff after the
regression suite and repository readiness check complete.
