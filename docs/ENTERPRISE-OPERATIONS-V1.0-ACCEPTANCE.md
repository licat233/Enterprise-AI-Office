# Enterprise Operations Capability Baseline v1.0

## Final Acceptance and Freeze

Date: 2026-09-10
Starting baseline: `d7ec20d8516ee65502daccb9d63739616d5041fa`
Branch: `codex/media-transcription`
Final baseline SHA: see final task handoff

## Scope and decision

This record is the final acceptance boundary for the Hermes Skills Migration
v1.0 project. It freezes the deployed ARMOR Operations capability baseline; it
does not migrate another Skill, reactivate a Legacy Profile, add an MCP,
install an image runtime, add browser automation, add delegation, add
scheduling, or perform a business-system action.

```text
Enterprise Operations Capability Baseline v1.0: FROZEN
Hermes Skills Migration v1.0: CLOSED
```

The repository remains a system blueprint and installation blueprint. This
acceptance record closes the ARMOR Skills migration project; it does not
silently change the separate blueprint lifecycle or activate a real company
deployment task.

## Frozen capability scope

```text
Website
├── Website Article Production
└── Website Product Materials

Marketing
├── Social Media Production
└── ARMOR Product Visual Preparation

Product
└── MIC Product Optimization

Shared
├── Company Knowledge / WeKnora
├── Scoped ARMOR Vault Router
├── ai-writing-audit v0.3.1
├── Media Transcription
└── ToolScout
```

Explicitly outside v1.0:

```text
Agent Delegate / Multi-Agent Orchestration
Codex automatic executor delegation
Claude Code automatic executor delegation
generic shell
generic terminal
generic browser
generic filesystem
generic code execution
automatic publishing
Legacy Hermes Memory
```

## Architecture

```text
Open WebUI
→ human identity / UI / RBAC

Hermes
→ agent runtime / Profiles / Skills / Tools

WeKnora
→ shared company-knowledge retrieval

ARMOR Vault
→ canonical durable ARMOR business rules, standards, and work products

Scoped ARMOR Vault Router
→ deterministic, closed persistence for approved package contracts
```

The active Enterprise Profile model is:

```text
Open WebUI User
→ Assistant / Group
→ Hermes Profile
```

The current department capability model is `general` plus the protected
`operations` surface, with existing administrative/control-plane surfaces
remaining separate. Operations is one shared least-privilege capability
bundle; it is not a set of copied Legacy `web-ops`, `social-ops`, `mic-ops`,
or `design-ops` Profiles.

## Definitive capability matrix

| Capability | Business purpose | Canonical Skill | Canonical Vault Standard | Operations exposure | Read/write boundary | External action boundary | Current runtime status |
|---|---|---|---|---|---|---|---|
| Website Article Production | Research, brief, SEO/GEO blueprint, governed article draft, final editorial pass | `armor-website-article-pipeline` | `$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Content/ARMOR-Content-Operations/ARMOR-Article-Production-Pipeline-v1.3/` | Enabled as one canonical entrypoint | Four-file Article package through `save_article_package` | No website publishing or indexing | PASS |
| Website Product Materials | Source reconciliation, product-page content, SEO structure, and media plan | `armor-website-product-materials` | `$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Website/Product-Materials/ARMOR-Website-Product-Materials-Standard-v1.0.md` | Enabled as one canonical entrypoint | Five-file Product Materials package through `save_website_product_materials_package` | Website repository read-only; no deployment/publication | PASS |
| Social Media Production | Evidence-grounded social drafts, platform adaptation, audit, approval handoff | `armor-social-media-pipeline` | `$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Content/ARMOR-Content-Operations/ARMOR-Social-Media-Production-Pipeline-v2.0/` | Enabled; one primary Social entrypoint | Closed Social package through `save_social_package`; optional video artifacts remain contract-bound | No social account posting or messaging | PASS |
| ARMOR Video Content Rules | Transcript-first and platform-specific video rules supporting Social | `armor-video-content-rules` | Social `video-package-standard.md` and related pipeline standards | Enabled as Social support Skill | No independent persistence surface; Social package only | No video upload or publication | PASS |
| MIC Product Optimization | Source-grounded MIC product naming, attributes, copy, audit, and review package | `armor-mic-product-optimization` | `$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Products/MIC-Products/ARMOR-MIC-Product-Optimization-Standard-v1.0.md` | Enabled as one canonical entrypoint | Closed MIC package through `save_mic_product_package` | No live MIC edit, upload, or publication | PASS |
| ARMOR Product Visual Preparation | Source-grounded visual brief, prompt, provenance, anti-moiré constraints, and QA handoff | `armor-product-visual` | `$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Products/Product-Visual/ARMOR-Product-Visual-Standard-v1.0.md` | Enabled as one canonical entrypoint | Four-file text package through `save_product_visual_package` | Image generation/editing and publication OFF | PASS |
| Company Knowledge / WeKnora | Shared company/product retrieval with source evidence | None; upstream/core MCP contract | WeKnora provisioning and Knowledge governance documents | Read-only retrieval exposed | Retrieval only; no Operations Knowledge write | No external mutation | PASS; live WeKnora containers and API healthy |
| ToolScout | Shared tool-selection and commodity-infrastructure control plane | `skills/shared/toolscout/SKILL.md` | None; shared infrastructure contract | Exposed through established exact shared allowlist | Tool advice/registry/memory infrastructure only; not business-package authority | No business publication or account mutation | PASS; healthy |
| Media Transcription | Explicit local audio/video to reviewable timestamped Markdown transcript | None; `scripts/transcribe` and `infrastructure/media-transcription/` | Media transcription README and existing acceptance section | Conditional CLI capability; no direct Operations upload tool | Local transcript under configured runtime root; no automatic WeKnora write | Human review required before optional Knowledge ingestion | PASS; contract/CLI smoke and unchanged boundary |
| ai-writing-audit v0.3.1 | Diagnostic AI-style and domain-boundary audit for Article/Social/MIC work | `ai-writing-audit` | None; audit Skill contract | Enabled as shared dependency | Reads supplied text and returns audit evidence; no business persistence | No publication or authorship claim | PASS; required version present |
| Scoped ARMOR Vault Router | Deterministic routing and narrow persistence of approved work packages | `armor-memory` Router/MCP adapter | Individual workflow Standards own package semantics | Exposed only as the six closed Router tools | Closed Article, Social, MIC, Website Product Materials, and Product Visual packages plus route | No generic file write, publication, or external account action | PASS; route, atomic write, read-back, and SHA-256 checks pass |

`WeKnora`, `ToolScout`, `Firecrawl`, `Anysearch`, `Obscura`, and `PaddleOCR`
are separately recorded in the MCP/runtime status below. WeKnora and Media
Transcription are core/conditional capabilities rather than entries in the
MCP server registry; their actual status is recorded without inventing a
duplicate registry definition.

## Profile architecture verification

```text
Current Enterprise Profiles: general, operations
Operations department bundle: shared capability surface
Legacy web-ops Profile migrated: NO
Legacy social-ops Profile migrated: NO
Legacy mic-ops Profile migrated: NO
Legacy design-ops Profile migrated: NO
Delegate worker Profile exposed: NO
Independent auditor Profile exposed: NO
Broken active Profile Skill symlinks: none observed
```

The deployed Operations Skill directory exposes the canonical Article,
Product Materials, Social, Video, MIC, Product Visual, audit, and shared
support Skills. The Legacy Profile identity is not used as evidence of v1.0
coverage; mature business semantics are represented by the canonical
Enterprise Skills and Vault standards.

## Operations permission matrix

| Surface | Final state | Evidence |
|---|---|---|
| Hermes Memory | OFF | `memory.memory_enabled: false`; Phase 5A–5E and final runtime checks |
| Profile Memory | OFF | Operations profile has no enabled Profile memory; `memory` toolset disabled |
| Session search | OFF | `session_search` is in disabled toolsets |
| Delegation | OFF | `delegation` is in disabled toolsets and no Delegate runtime is exposed |
| Generic shell | OFF | `terminal` is disabled; no Operations shell binding |
| Generic terminal | OFF | `terminal` is disabled |
| Generic file | OFF | `file` is disabled; Router is the only governed persistence path |
| Generic browser | OFF | `browser` and `web` are disabled for Operations |
| Computer-use | OFF | `computer_use` is disabled |
| Code execution | OFF | `code_execution` is disabled |
| Image generation / vision | OFF | `image_gen` and `vision` are disabled |
| SSH | Not an Operations tool | No SSH tool binding in Operations |
| sudo/root | Not granted | Hermes status reports sudo disabled; no Operations root grant |
| External Skill directories | Empty | `skills.external_dirs: []` |
| Project discovery | Disabled | `skills.project_discovery: false` |

## Agent Delegate final freeze

The complete Legacy Agent Delegate implementation remains outside v1.0. The
Phase 5C audit records its components as one experimental runtime capability:

```text
Hermes orchestrator Profile/config
delegate_task / Kanban dispatch and task-state integration
armor-fallback-content-worker
armor-independent-auditor
delegation Skills and worker selection rules
Codex executor binding
Claude Code executor binding
fallback and executor-selection rules
audit / Required Fixes / re-audit return flow
```

Some fallback and independent-audit semantics are intentionally absorbed by
current Article/Social workflows. That semantic reuse does not absorb the
runtime/Profile implementation.

```text
Multi-Agent Orchestration: EXPERIMENTAL_HOLD
Agent Delegate migrated: NO
Operations exposure: NO
Default enabled: NO
Operations delegation: OFF
Codex auto-executor: NO
Claude Code auto-executor: NO
```

## Final canonical business capabilities

### Website Article

`armor-website-article-pipeline` is the one canonical entrypoint. Article v1.3
rules own the Research/Brief, SEO/GEO Blueprint, Blueprint Gate, writing, one
Codex Final Editorial Pass, audit, and scoped four-file save. The Article
workflow does not automatically publish to a website.

### Social Media

`armor-social-media-pipeline` is the one primary Social entrypoint and
`armor-video-content-rules` is its video-specific support Skill. Social v2
owns topic signals, platform adaptation, independent Social audit semantics,
approval, and scoped save. No social account publication is enabled.

### MIC Product Optimization

`armor-mic-product-optimization` is a thin execution adapter. The canonical
MIC Vault Standard owns detailed field, fact, source-authority, blocker,
approval, and package semantics. Original technical documents outrank
WeKnora, and MIC editing/upload/publication remains OFF.

### Website Product Materials

`armor-website-product-materials` is one canonical source-reconciliation and
product-materials entrypoint. The Standard owns product facts, page content,
SEO package, media plan, source review, and five-file save. The official
website repository remains read-only evidence; no deployment or publication is
performed.

### ARMOR Product Visual

`armor-product-visual` is one canonical entrypoint. The Product Visual
Standard owns anti-moiré guidance, product identity preservation,
real/generated/composite/reference-only provenance, visual brief/prompt/QA
handoff, and the closed four-file text package. Image generation and
publication remain OFF; `READY_FOR_GENERATION` is only a separately approved
future handoff state.

## Authority separation and product fact consistency

```text
ARMOR Vault
= canonical durable business rules, standards, knowledge, and work products

WeKnora
= derived retrieval/index layer

Skill
= execution adapter / procedure

Scoped Router
= controlled persistence

SOUL
= behavior / policy

Operations Memory
= OFF
```

Across MIC, Website Product Materials, and Product Visual, exact technical
facts use the same hierarchy:

```text
authoritative original Datasheet / Manual / test / certification
→ canonical or explicitly verified Product Knowledge derived from that source
→ WeKnora retrieval/discovery used to locate the knowledge/source
→ current website or MIC listing as existing-state evidence
```

WeKnora never silently overrides an original document. Unknown technical facts
remain unknown. `REASONABLE_INFERENCE` cannot create numeric, technical,
certification, commercial, performance, or hidden-structure facts. Material
authoritative conflicts fail closed with the workflow-specific authority
review state.

The three business Skills are semantic adapters, not byte-copy competitors to
their Standards:

```text
MIC Skill ≠ duplicate MIC Standard
Product Materials Skill ≠ duplicate Product Materials Standard
Product Visual Skill ≠ duplicate Product Visual Standard
```

Each Skill loads its canonical Standard, names the required stage interface,
and binds only its scoped save operation.

## Scoped Router final contract

Allowed Operations tools are exactly:

```text
route_work_product
save_article_package
save_social_package
save_mic_product_package
save_website_product_materials_package
save_product_visual_package
```

The Router and scoped MCP enforce:

```text
generic filesystem write: rejected
arbitrary destination: rejected
absolute model path: rejected
path traversal: rejected
symlink escape: rejected
editable Published destination: rejected
binary upload: rejected by Product Visual contract
atomic writes: required
read-back: required
SHA-256 verification: returned and verified
```

Current destination map, verified from Router output:

```text
Website Article
→ 02-Projects/Workspaces/Website/Articles/

Social
→ 02-Projects/Workspaces/Marketing/Social-Media/

MIC
→ 02-Projects/Workspaces/Products/MIC-Products/

Website Product Materials
→ 02-Projects/Workspaces/Website/Product-Materials/

Product Visual
→ 02-Projects/Workspaces/Products/Product-Visual/
```

## MCP and runtime status

| Runtime | Installed/configured | Health | Operations exposure | Final status |
|---|---|---|---|---|
| WeKnora | Existing core runtime; configured read-only MCP | WeKnora app, docreader, PostgreSQL, Redis, and frontend containers running; app health HTTP 200 on current runtime port `18081` | Read-only retrieval | PASS |
| ToolScout | Installed and configured | HEALTHY | Exposed through established exact shared allowlist | PASS |
| Firecrawl | Installed and configured; Enterprise Web Research adapter uses the read API lane | `HEALTHY`; live Search, Fetch, and URL-security acceptance passed | Operations exposes only `web_search` and `web_fetch`; raw/action-capable lanes denied | PASS |
| Anysearch | Registered; remote runtime known; configured | `BLOCKED_CREDENTIAL` because `ANYSEARCH_API_KEY` is not bound | Not exposed | ACCEPTABLE DEGRADED |
| Obscura | Installed and configured | HEALTHY in registry probes | Not exposed; reserved for future approved browser-session worker | PASS / not exposed |
| PaddleOCR | Installed and configured | HEALTHY in registry probes | Not exposed; reserved for future approved media worker | PASS / not exposed |
| Scoped ARMOR Router | Installed and configured | HEALTHY; initialize/tools/route/save/read-back tests pass | Six closed Router tools | PASS |
| Media Transcription | Existing conditional host-native CLI contract | CLI/contract smoke passes; no daemon or automatic publication | No direct Operations upload/tool binding | PASS / conditional |

No credential was copied from Legacy. The approved Firecrawl credential is
held outside Git by the protected Enterprise runtime environment; raw
Firecrawl MCP tools remain unbound to Operations.

## Product Visual image boundary

```text
Product Visual preparation: ENABLED
Product Visual scoped save: ENABLED
image generation: OFF
image editing runtime: OFF
ComfyUI: not added
Stable Diffusion: not added
generic image daemon: not added
external generator credential: not added
binary arbitrary asset upload: OFF
```

## Backup, restore, and gateway health

The existing `scripts/backup.sh`, `scripts/restore.sh`,
`docs/BACKUP-RESTORE.md`, and `docs/OPERATIONS.md` remain the backup/restore
authority. Phase 6 performed safe shell-syntax and restore-guard validation
without touching live state or performing a destructive restore. The existing
documented isolated restore rehearsal from 2026-09-05 remains the recovery
evidence; no second backup system was created.

MacStudio runtime validation recorded:

```text
Hermes config check: PASS
Hermes doctor: no active security advisories; required runtime/config checks PASS
Hermes gateway status: RUNNING and supervised by launchd, PID 82446
Hermes health endpoint: HTTP 200
Open WebUI: HTTP 200; container healthy
WeKnora app/docreader/PostgreSQL: running and healthy
WeKnora frontend: HTTP 200
Operations scheduled jobs: 0
Operations active sessions: 0
```

Hermes reports a non-blocking stale LaunchAgent definition warning relative to
the current installed Hermes build. The service is running under the expected
`ai.hermes.gateway` label and remains healthy; Phase 6 does not rewrite the
launchd architecture for this warning. A direct `launchctl print` query from
the non-Aqua SSH context did not resolve the label, while `launchctl list` and
Hermes gateway status confirmed the supervised running service.

Other doctor warnings are optional integrations or disabled/unconfigured
surfaces (for example optional messaging packages, browser dependencies, and
unbound provider credentials). They do not expand Operations permissions and
do not block this v1.0 baseline.

## End-to-end acceptance

Each representative workflow used its existing authoritative offline fixture
or runtime checker, with source resolution, authority handling, artifact
generation, approval boundary, scoped save, read-back, and no publication:

| Workflow | Evidence | Result |
|---|---|---|
| Article | Phase 4A/4B/4C runtime and package tests; four-file Article contract | PASS |
| Social | Phase 5A runtime and package tests; Social/video approval boundary | PASS |
| MIC | Phase 5B, 5B.1, 5B.2 authority/de-duplication tests; closed MIC package | PASS |
| Website Product Materials | Phase 5D runtime and package tests; five-file source/materials contract | PASS |
| Product Visual | `SLIM-213BWRY` source fixture, ESL Datasheet/source image, authority/provenance/anti-moiré/QA handoff, four-file save/read-back | PASS |

Product Visual ends at `READY_FOR_GENERATION`; actual image generation is not
required and was not performed.

## Fail-closed evidence

The accepted suite demonstrates:

```text
unknown fact remains unknown: PASS
authority conflict blocks affected output: PASS
missing canonical Standard blocks execution: PASS
Router rejects path traversal: PASS
Router rejects symlink escape: PASS
publication is not performed: PASS
delegation remains disabled: PASS
```

## Legacy migration status

The Phase 5C ledger is now finalized in
`docs/inventory/legacy-operations-skills-triage.csv`:

```text
MIGRATED: 19
ABSORBED: 6
REFERENCE_ONLY: 21
EXPERIMENTAL_HOLD: 16
DO_NOT_MIGRATE: 370
DUPLICATE: 1
KEEP_MIGRATE: 0
Total rows: 433
```

The two Phase 5C P1 candidates are finalized as `MIGRATED`: website product
materials and ARMOR Product Visual/anti-moiré. The historical Phase 5C report
still records that they were open planning items at that earlier point; that
historical truth is not rewritten.

| Legacy Profile | Final business-capability result |
|---|---|
| `web-ops` | Mature Article and Website Product Materials coverage migrated/absorbed; the Profile itself was not migrated |
| `social-ops` | Mature Social/video coverage migrated/absorbed; the Profile itself was not migrated |
| `mic-ops` | Mature MIC coverage migrated/absorbed; the Profile itself was not migrated |
| `design-ops` | ARMOR-specific Product Visual/anti-moiré capability migrated; generic design bundle intentionally not migrated |
| `armor-fallback-content-worker` | `EXPERIMENTAL_HOLD`; role `DELEGATE_WORKER`; migration NO; Operations exposure NO |
| `armor-independent-auditor` | `EXPERIMENTAL_HOLD`; role `DELEGATE_AUDITOR`; migration NO; Operations exposure NO |
| Legacy Hermes Memory | Not accessed; not a v1.0 migration obligation |

Remaining raw Legacy Skills are not a v1.0 migration obligation. The ledger
preserves `REFERENCE_ONLY`, `DO_NOT_MIGRATE`, `DUPLICATE`, and
`EXPERIMENTAL_HOLD` outcomes without implying that every generic/public Skill
was migrated.

## Known non-blocking limitations

- Firecrawl and Anysearch remain credential-blocked by design; they are not
  required by the core v1.0 workflows.
- Product Visual is text/metadata-only in v1.0; future image generation needs
  a separately approved tool, credential, binary, QA, and publication boundary.
- Hermes reports a stale LaunchAgent definition warning even though the
  current gateway is supervised and healthy.
- Media Transcription remains a conditional host-native CLI capability and
  does not auto-publish transcripts to WeKnora.
- The repository's separate blueprint lifecycle remains governed by
  `state/PROJECT-PHASE.yaml`; this migration closure is not a real-company
  deployment declaration.

## Post-v1.0 backlog

The only deferred items are recorded in
[`docs/POST-V1.0-BACKLOG.md`](POST-V1.0-BACKLOG.md):

```text
Agent Delegate / Multi-Agent Orchestration → EXPERIMENTAL_HOLD
Product Visual actual image-generation integration → future optional capability
credential-dependent external research enhancements → future optional capability
```

No further migration phase is proposed.

## Tests and final evidence

Phase 6 ran the existing relevant acceptance suite and the final static/runtime
checks:

```text
Phase 5C finalized triage checker: PASS; no KEEP_MIGRATE rows
Phase 4A migration checker: PASS
Phase 4B runtime checker/tests: PASS
Phase 4C runtime checker/tests: PASS
Phase 5A runtime checker/tests: PASS
Phase 5B runtime checker/tests: PASS
Phase 5B.1 authority tests: PASS
Phase 5B.2 authority de-duplication tests: PASS; one expected skip
Phase 5D runtime checker/tests: PASS
Phase 5E runtime checker/tests: PASS
Media Transcription compile/help smoke: PASS
Backup/restore shell syntax and isolated-target guard: PASS
Hermes config check/doctor/gateway status: PASS with recorded non-blocking warnings
scripts/repository-readiness-check.sh: PASS
git diff --check: PASS
```

## Files changed in Phase 6

```text
README.md
README.zh-CN.md
docs/OPERATIONS.md
docs/POST-V1.0-BACKLOG.md
docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md
docs/inventory/legacy-operations-skills-triage.csv
scripts/phase5c_operations_skills_triage_check.py
scripts/repository-readiness-check.sh
```

No Legacy Memory data, credential, temporary fixture, or generated binary was
added to the repository. No production business action was performed.

## Final status

```text
Phase 6: PASS

Enterprise Operations Capability Baseline v1.0: FROZEN
Hermes Skills Migration v1.0: CLOSED

Website Article: PASS
Website Product Materials: PASS
Social Media: PASS
MIC Product Optimization: PASS
Product Visual: PASS

Operations Hermes Memory: OFF
Operations delegation: OFF
Generic shell: OFF
Generic browser: OFF
Generic filesystem: OFF

Multi-Agent Orchestration: EXPERIMENTAL_HOLD
Agent Delegate migrated: NO
Codex auto-executor: NO
Claude Code auto-executor: NO

Image generation infrastructure added: NO
Automatic publication enabled: NO
Legacy Memory accessed: NO
Secrets committed: NO

Repository readiness: 320 PASS / 0 FAIL
Final baseline commit: see final task handoff
Push: see final task handoff
Worktree: clean after final commit
```
