# Enterprise AI Office — Phase 5D

## Website Product Materials Capability Migration

Date: 2026-09-10
Repository baseline: `6020a601bdd181dbd762f9debbc8a0a914429a60`
Repository branch: `codex/media-transcription`

## Decision

Phase 5D migrates one ARMOR-specific business capability: preparation of a
source-grounded website Product Materials package. The capability is exposed
through one canonical Enterprise Skill and one narrow scoped Vault save tool.
It does not migrate Product Visual/anti-moiré production, website code
generation, publication, account mutation, or Agent Delegate/Multi-Agent
Orchestration.

Website Product Materials: PASS

The migration is clean-room. No Legacy Skill, Profile, script, template, or
configuration was copied into the Enterprise repository. The Legacy workflow
was used only as evidence for source inventory, reconciliation, product-page
brief/copy, SEO, media planning, review, and readback semantics.

## Evidence and scope boundary

The exact Legacy implementation inspected was:

- `/Users/licat/.hermes/profiles/web-ops/skills/web/website-product-materials/SKILL.md`
- `/Users/licat/.hermes/profiles/web-ops/skills/web/website-product-materials/references/source-reconciliation-checklist.md`

That resolved implementation contains no scripts, templates, examples, or
additional configuration. The Skill describes a larger five-file handoff shape;
the Enterprise package uses a smaller self-describing five-file closed set and
puts the handoff/readiness details in `product-audit.md` rather than creating a
second handoff artifact.

No Legacy Hermes Memory, session history, conversation history, private
remembered facts, logs, or correction-patch history was inspected.

The official `ARMOR-Lighting/armorltgcom` repository was inspected read-only at
commit `a825cda6d7cd88134ed091dd626be7d893e013b8`. The current Product schema
and detail component establish these implementation fields: `title`,
`sourceId`, `permalink`, `excerpt`, `image`, `gallery`, `pdf`, `video`,
`videos`, `specifications`, `system`, `family`, optional `subfamily`, and
`metadata`. No website repository file was modified, deployed, published, or
indexed. The repository's existing site configuration contains a different
URL; that mismatch is recorded as an implementation-owner review item rather
than silently changed.

## Legacy Product Materials Inventory

```text
Legacy Skill(s): website-product-materials
Resolved source: /Users/licat/.hermes/profiles/web-ops/skills/web/website-product-materials/
Same-name copies: none found in the searched global/profile roots; the resolved implementation is a physical directory, not a symlink
References/scripts/templates reviewed: SKILL.md and references/source-reconciliation-checklist.md; no scripts/templates/examples/configuration were present in the resolved implementation
Historical artifacts reviewed: Vault Product Knowledge/entities, MIC historical product records, website product sources and schema, and the read-only official website repository snapshot
```

Relevant capability decisions:

| Capability | Decision | Enterprise role | Reason |
|---|---|---|---|
| Legacy `website-product-materials` Skill | `MERGE` | Source workflow evidence for the new adapter and Standard | Useful source inventory, reconciliation, copy, SEO, media, review, and readback semantics were re-expressed clean-room |
| `source-reconciliation-checklist.md` | `MERGE` | Canonical Standard input | Its checks are incorporated without copying a second reference authority |
| Referenced five-file handoff shape | `REPLACE` | Closed Enterprise five-file package | The audit absorbs handoff/readiness details; no duplicate `handoff` artifact is needed |
| Absent Legacy scripts/templates/examples/config | `REFERENCE_ONLY` | None | No absent implementation was invented or migrated |
| Article and MIC workflows | `KEEP` | Existing canonical Article/MIC entrypoints | Separate contracts and publication contexts remain intact |
| Product Visual / anti-moiré workflow | `DO_NOT_MIGRATE` | Future P1 only | No visual generation, retouching, diffusion, or image-tool activation in Phase 5D |
| Agent Delegate / Multi-Agent Orchestration runtime | `DO_NOT_MIGRATE` | `EXPERIMENTAL_HOLD` | Runtime/Profile implementation remains unexposed and disabled |

## Enterprise ownership

| Layer | Enterprise owner | Result |
|---|---|---|
| Durable business rules | `$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Website/Product-Materials/ARMOR-Website-Product-Materials-Standard-v1.0.md` | Canonical, active, review-required |
| Execution adapter | `skills/shared/department/armor-website-product-materials/SKILL.md` | One canonical entrypoint |
| Deterministic Router | `website/product-materials` | `02-Projects/Workspaces/Website/Product-Materials/` |
| Persistence | `save_website_product_materials_package` | Exact five UTF-8 text files, atomic/read-back/SHA256 |
| Website implementation | Official website repository | Read-only evidence in this phase |
| Operations exposure | Existing `operations` Profile | Skill symlink and one scoped MCP tool; no new Profile |

The package contract is:

```text
product-source-map.yaml
product-page-content.md
product-seo.md
product-media-plan.md
product-audit.md
```

The Router rejects arbitrary destinations, absolute paths, path traversal,
symlink escape, Published destinations, extra files, and website-repository
paths. The scoped MCP never exposes a generic filesystem write.

## Authority

```text
Vault Standard: $ARMOR_VAULT_ROOT/02-Projects/Workspaces/Website/Product-Materials/ARMOR-Website-Product-Materials-Standard-v1.0.md
Previous authority: no canonical Product Materials Standard existed; Legacy Skill/reference and current architecture were evidence only
Current authority: the new canonical, active, review-required Vault Standard
Canonicalization: created at the deterministic Website Product Materials Router destination; Skill is a thin execution adapter
Material unresolved decisions: authoritative product-document readback for the acceptance product, existing website URL/domain mismatch, and any current company decisions needed for mutable positioning/commercial wording
```

### Authority result

The canonical Standard defines this technical hierarchy:

```text
authoritative original Datasheet / Manual / test / certification document
→ canonical or explicitly verified Product Knowledge
→ WeKnora retrieval used to locate that knowledge/source
→ current website or MIC listing as existing-state evidence
```

Conflicting authoritative claims produce
`PRODUCT_AUTHORITY_REVIEW_REQUIRED`. WeKnora cannot silently override an
original document. Current explicit company/user confirmation or approved
current commercial documentation may supersede historical MOQ, price, lead
time, payment, sample, and packaging data. Media supports visible facts only.
`REASONABLE_INFERENCE` cannot create numeric, certification, commercial,
performance, or technical facts.

The Standard is the only detailed Product Materials business authority. The
Skill is an execution adapter and does not contain a duplicate product-facts
database or detailed alternate SOP.

## Product Materials Workflow

```text
Input contract: stable product identity/package id; scoped source references; current website snapshot/evidence; supplied media; current Brand/Product rules; explicit current company decisions; review context
Stages: Intake → identity resolution → scoped source inventory → source reconciliation → authority/conflict review → normalized facts → page brief/copy → SEO → media inventory/gap plan → audit → review/approval → scoped save → read-back/SHA256
Fact/source hierarchy: authoritative original Datasheet/Manual/test/certification → canonical/verified Product Knowledge → WeKnora retrieval/discovery → current website or MIC listing as evidence
Approval gate: READY_FOR_REVIEW → explicit user/company approval → scoped Vault save; save is not publication approval
Website implementation boundary: map to the existing Product schema/component vocabulary; website repository is read-only evidence and is not edited by this capability
Publication boundary: no website edit, deploy, publish, indexing, account mutation, or Published-record write
```

## Acceptance fixture

The actual workflow was exercised in a temporary Vault root with the real ARMOR
product `HM-SX64F010W24-2835` / `High Efficient LED Flexible Strip Light`:

- authoritative-source evidence: the official website repository's linked
  `hm_sx64f010w24_2835_datasheet_armor.pdf`;
- current website evidence: Product source `wp-365` at the read-only website
  commit above;
- historical MIC/website material: evidence only, never final technical
  authority.

The original PDF is present as a six-page encrypted binary and therefore its
technical values were not guessed or silently extracted. The generated review
fixture records `PRODUCT_AUTHORITY_REVIEW_REQUIRED` until the original
document is readable and reconciled; exact technical values remain unknown in
the public draft. The fixture verified product identity handling, source map,
copy, SEO, media plan, audit, package identity, closed files, readback, and
SHA256 without publication.

## Legacy module treatment

| Legacy module/evidence | Treatment | Enterprise result |
|---|---|---|
| `website-product-materials/SKILL.md` | `MERGE` | Safe workflow semantics re-expressed in the canonical Standard and thin adapter |
| `source-reconciliation-checklist.md` | `MERGE` | Source inventory/reconciliation checks incorporated into the Standard; no duplicate reference copied |
| Five prescribed product-page handoff outputs | `REPLACE` | Replaced by the closed five-file Enterprise package; audit is self-describing |
| Referenced scripts/templates/examples/config/input-output not present in resolved implementation | `REFERENCE_ONLY` | No absent implementation was invented or copied |
| `armor-website-article-pipeline` | `KEEP` | Existing Article workflow remains separate and unchanged |
| `armor-mic-product-optimization` | `KEEP` | Existing MIC workflow remains separate and unchanged |
| Legacy Product Visual / anti-moiré path | `DO_NOT_MIGRATE` | Future P1; no visual generation or image tooling enabled |
| Agent Delegate orchestrator, workers, auditor, Codex/Claude lanes, Kanban runtime | `DO_NOT_MIGRATE` | `EXPERIMENTAL_HOLD`; no Operations exposure or default enablement |

There is one active Product Materials entrypoint and no new Profile.

## Website Integration Boundary

```text
Website repo inspected: ARMOR-Lighting/armorltgcom, read-only commit a825cda6d7cd88134ed091dd626be7d893e013b8
Website repo modified: NO
Website deployed: NO
Product page published: NO
Search indexing changed: NO
```

## Runtime and safety result

The deployed Operations runtime now exposes the canonical Skill by symlink and
the exact scoped Router allowlist:

```text
route_work_product
save_article_package
save_social_package
save_mic_product_package
save_website_product_materials_package
```

The existing Article, Social, and MIC package file contracts remain unchanged;
the aggregate MCP tool list grew only by the new semantically distinct save
tool. Operations still has Memory OFF, external Skill directories empty,
project discovery disabled, generic terminal/file/browser/code execution
disabled, delegation disabled, and image generation disabled. The two Legacy
Delegate Profiles remain unexposed.

## Tests

New Phase 5D tests cover:

- original Datasheet outranking conflicting WeKnora-derived and historical MIC
  values;
- WeKnora remaining retrieval-layer input rather than final authority;
- current explicit commercial confirmation superseding historical commercial
  data;
- inference-only input leaving an unknown numeric specification as `UNKNOWN`;
- authoritative-source conflict producing `PRODUCT_AUTHORITY_REVIEW_REQUIRED`;
- one canonical entrypoint and no duplicate active Product Materials workflow;
- Router destination, exact five-file contract, identity validation, traversal
  rejection, symlink-escape rejection, atomic readback, and SHA256;
- no website-repository write path, no publication, no personal runtime path,
  and Delegate/Memory-off boundaries.

The Phase 4A–5C regression suite, repository readiness, runtime checks, and
`git diff --check` are run as part of final acceptance.

## Regressions

```text
Article: PASS
Social: PASS
MIC: PASS
MIC authority/de-duplication: PASS
Scoped Router: PASS
ToolScout: PASS
WeKnora: PASS
Operations Memory OFF: PASS
Agent Delegate hold: PASS — EXPERIMENTAL_HOLD; not migrated or exposed
```

## Operations Permissions

```text
Generic shell: OFF
Generic terminal: OFF
Generic file: OFF
Generic browser: OFF
Code execution: OFF
Delegation: OFF
SSH: not an Operations tool
sudo/root: OFF
Hermes Memory: OFF
```

## Files Changed

Tracked Enterprise files:

- `skills/shared/department/armor-website-product-materials/SKILL.md`
- `skills/shared/department/armor-website-product-materials/agents/openai.yaml`
- `skills/shared/department/armor-memory/scripts/armor-route.py`
- `skills/shared/department/armor-memory/scripts/armor-vault-mcp.py`
- `skills/shared/department/armor-memory/SKILL.md` (routing vocabulary only)
- `config/mcp-registry.yaml`
- Phase 4C/5A/5B aggregate MCP regression expectations
- `scripts/test_phase5d_product_materials.py`
- `scripts/phase5d_product_materials_check.py`
- `scripts/repository-readiness-check.sh`
- `docs/PHASE5C-REMAINING-OPERATIONS-SKILLS-TRIAGE.md` (timeline wording only)
- `docs/PHASE5D-WEBSITE-PRODUCT-MATERIALS-MIGRATION.md`

Durable Vault file:

- `$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Website/Product-Materials/ARMOR-Website-Product-Materials-Standard-v1.0.md`

Deployed ignored runtime binding (not a secret and not a new Profile): the
Operations Skill symlink, private Skill/tool manifests, and scoped Router
allowlist were updated on the MacStudio and are covered by runtime checks.

## Commit / Push

```text
Suggested commit: feat: migrate ARMOR website product materials capability
Commit: recorded in final task handoff
Push: PASS after final commit
```

## Final status block

```text
Phase 5D status: PASS
Website Product Materials: PASS
Website Product Materials authority: CANONICAL
Canonical Product Materials Skill: PASS
Duplicate Product Materials workflow removed: PASS
Product Materials runtime exposure: PASS
Product Materials scoped Router Save: PASS
Product Materials E2E: PASS
Vault Standard: PASS
Scoped Router destination: PASS
Closed five-file package: PASS
Technical authority hierarchy: PASS
Current commercial-decision rule: PASS
Website repository modified: NO
Website publication performed: NO
Article regression: PASS
Social regression: PASS
MIC regression: PASS
ToolScout regression: PASS
Multi-Agent Orchestration: EXPERIMENTAL_HOLD
Agent Delegate migrated: NO
Operations delegation: OFF
Operations Hermes Memory: OFF
Generic browser enabled: NO
Article/Social/MIC contracts changed: NO
Legacy Memory accessed: NO
Secrets committed: NO
Repository readiness: 291 PASS / 0 FAIL
Commit: recorded in final task handoff
Push: PASS
```
