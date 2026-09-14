# EAO Production Business Skill Admission — `competitive-intel`

Status: `ADMITTED RUNTIME VALIDATED EMPLOYEE-EXPOSED: OPERATIONS`

Date: 2026-09-14 (Asia/Shanghai)

This is production evidence for one governed third-party business Skill. It
does not change the closed PHASE4/PHASE5 migration records and does not expose
the Skill to General or to future Profiles.

## Admission decision

- Classification: Class A Portable / DIRECT.
- Candidate: `competitive-intel` from `alirezarezvani/claude-skills`.
- Pinned upstream commit: `19392f7a08264ed00486a251f5b2098321771f94`.
- Pinned `SKILL.md` blob: `4903607353bfc30cd5fedc9c3ac6c18ce4fcfb9d`.
- License: MIT, upstream repository `LICENSE`.
- Installed source: exactly `SKILL.md`, `references/ci-playbook.md`, and
  `templates/battlecard-template.md`; no other upstream Skill or repository
  content was installed.
- Existing equivalent: no complete Operations Skill with this competitor
  identification, current-evidence, positioning, threat, and sales-battlecard
  procedure. Existing research, product-marketing, and legacy competitor-news
  records were capability-reuse inputs, not substitutes.
- New component required: none. The admission reuses the existing Skills
  loader, read-only WeKnora, Enterprise Web Research, and normal reasoning.

The upstream files contain generic suggestions for Notion, Confluence, and
Salesforce distribution. EAO policy overrides those suggestions: Company
Knowledge through WeKnora is authoritative; those integrations are neither
installed nor used; competitive output is a report/battlecard only; no
automatic WeKnora write is performed.

## Runtime exposure

Runtime target and evidence host: `armor@MacStudio.local` only.

- Hermes profile: `operations`, existing employee route `/p/operations`.
- Hermes runtime: `v0.21.2`, upstream `afe06f21`, local build `939e45c9`.
- Profile-scoped source root:
  `/Users/armor/Enterprise-AI-Office/infrastructure/hermes/third-party-skills`.
- Operations `skills.external_dirs` changed from `[]` to that single root;
  auto-update and project discovery remain off.
- `hermes skills list` reports `competitive-intel` as local/enabled. The source
  tree contains only the three pinned files and the committed blob IDs above.
- General config and the shared Hermes config were not changed.
- No new Profile, route, MCP server, credential, plugin, database, Cron job,
  dashboard, Open WebUI setting, terminal, file, code, browser, or delegation
  authority was added.

Hermes 0.21.2 currently fails the default bare-name `skill_view` JSON response
for this upstream file because its unquoted YAML date is parsed as a Python
`date`. The existing Skills tool successfully serves the exact file and linked
files using relative `file_path` values. Production evidence therefore uses:

- `skill_view(competitive-intel, SKILL.md)`
- `skill_view(competitive-intel, references/ci-playbook.md)`
- `skill_view(competitive-intel, templates/battlecard-template.md)`

This is a serving-path workaround only; no source content, hash, permission,
or adapter code was changed. Bare-name loading remains a Hermes runtime gap.

## Runtime business acceptance

Final Operations session: `20260914_155431_374c36`, titled
`Produce ARMOR retail lighting brief`.

Actual call evidence from the redacted session export:

- `skill_view`: 3 successful calls for the exact Skill and two references.
- `mcp__operations_weknora__list_knowledge_bases`: 1 call; found Company
  Knowledge.
- `mcp__operations_weknora__hybrid_search`: 10 calls; retrieved ARMOR
  product/brand records, including shelf, cabinet, freezer, magnetic-track,
  wireless-track, and display-fixture evidence.
- `mcp__enterprise_web_research__web_search`: 15 calls.
- `mcp__enterprise_web_research__web_fetch`: 9 calls.
- Forbidden-call scan: no terminal, browser, file, code execution,
  delegation, Codex, Claude, Cron, save, route, Vault, CRM, Notion,
  Confluence, or Salesforce tool call.

Selected competitor: Signify, including Philips InteGrade and Signify
Interact, because WeKnora evidence showed direct ARMOR overlap in retail
shelf/display lighting and the public research found matching retail-display
products, connected-retail capability, and public M&S/Hoogvliet evidence.

The brief used `armor-employee-product-knowledge-phase1a.csv` and
`armor-brand-employee-knowledge.md` as internal sources, and current public
Signify sources including:

- https://www.signify.com/global/applications/large-retail
- https://www.signify.com/oem/en-eg/products/retail-display-lighting
- https://www.signify.com/oem/en-gb/products/retail-display-lighting/retail-display-lighting-modules/philips-integrade-gen-4/929002150206_EU/product
- https://www.signify.com/global/case-studies/hoogvliet
- https://www.signify.com/global/our-company/news/press-releases/2026/20260309-next-generation-signify-interact-solutions-provide-smarter-safer-more-efficient-lighting-for-intelligent-buildings-and-cities

The output separated `VERIFIED`, `COMPETITOR CLAIM`, `INFERENCE`, and
`UNKNOWN`. It explicitly did not claim ARMOR price, win rate, customer proof,
better lifetime, faster installation, superior quality, stronger software, or
any other unsupported advantage. The battlecard identifies where Signify is
stronger, where ARMOR may fit based on retrieved product evidence, where not
to attack, buyer-winning/losing scenarios, objections, safe responses,
discovery questions, and claims requiring verification. It is not a generic
SWOT.

## Permission invariant and rollback

Pre-change backup:
`/Users/armor/.hermes/profiles/operations/config.yaml.pre-competitive-intel-20260914-154700.bak`

The final diff against that backup is only the two functional
`skills.external_dirs` lines. The global config hash remains
`3c55210f2b9b2db756942498c7d3905acef1e078dfeb2e0c0d7a22592b30f4b8` and the
General config hash remains
`fa4e51f90e20bb506e1ccd2c376b7161fcaaf944f23ddbb37102d0d8d3c5536d`.
Operations config validation passes with version 42. Existing disabled
toolsets and MCP allowlists remain in force; the only persistent runtime
change is Skill discovery/exposure itself.

Rollback is bounded and reversible: restore the backup (or remove the single
`external_dirs` entry), remove the committed third-party source directory,
and revert the admission PR. No employee migration or data deletion is
required. No Cron or update monitor was created.

## Repository evidence

- Branch: `codex/competitive-intel-production-admission`, from latest
  `origin/main` (`bad1e98300f9863d97dd2a5361c7cbaa672b471f`), not the old
  `docs/skill-admission-v1` branch.
- Source commit: `7de8f0e` (`feat: vendor pinned competitive-intel skill source`).
- The final evidence document and documentation-map entry are to be included
  in the same short-lived PR; merge is intentionally not performed here.

## Final scope

- General exposure: `NONE`.
- Operations exposure: `ENABLED`.
- New runtime permission: only profile-scoped discovery/loading of this pinned
  portable Skill through existing approved capabilities.
- External write authority added: `NONE`.
- Terminal granted: `NO`.
- Codex/Claude delegation granted: `NO`.
- Persistent runtime change: Operations `skills.external_dirs` contains one
  governed EAO source root; no other profile or permission changed.
- Remaining gaps: Hermes bare-name `skill_view` date serialization, no
  independent ARMOR customer/price/win-loss evidence in Company Knowledge,
  and no future automatic upstream updates until a separately reviewed
  admission update.
