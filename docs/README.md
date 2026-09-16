# Enterprise AI Office Documentation Map

> Navigation and authority map for humans and AI engineering agents.
>
> This file does not replace the root operating contracts. Its purpose is to stop current normative guidance, frozen capability evidence, historical migration records, and reference material from being treated as equivalent.

## Start at the repository root

A fresh Agent should begin with:

1. `README.md` — project orientation.
2. `AGENTS.md` — highest-priority repository-local Agent operating contract.
3. `REPRODUCE.md` — end-to-end reconstruction contract.
4. `VALIDATE.md` — Fresh-Agent validation contract.
5. `config/eao-manifest.yaml` — machine-readable project map.
6. `state/PROJECT-PHASE.yaml` — blueprint lifecycle and real-deployment gate.
7. `DEPLOY.md` — deployment Golden Path when deployment or installation design is in scope.

Do not begin with a `PHASE*` migration document merely because it looks operational.

GitHub Wiki pages, Project cards, Issues, PR descriptions/comments, and similar
collaboration surfaces are not part of the normative documentation hierarchy.
If they produce a durable decision, that decision must be promoted into the
version-controlled authority chain below.


## Authority order

When documents appear to overlap, use this precedence:

```text
AGENTS.md
+ state/PROJECT-PHASE.yaml
+ config/eao-manifest.yaml
        ↓
DEPLOY.md / current normative docs / config registries
        ↓
frozen capability baselines and acceptance evidence
        ↓
specialized design contracts
        ↓
historical migration / closure evidence
        ↓
reference examples
```

A historical file may explain why the current design exists. It must not silently override the current contract.

## Tier 1 — Current normative system contracts

For an administrator-discovered resource, start with
[Administrator Resource Intake](ADMIN-RESOURCE-INTAKE.md). It routes knowledge,
Tools/MCPs/services, and third-party Skills into the existing authoritative
procedures. For durable knowledge, continue to [Knowledge Intake v1](KNOWLEDGE-INTAKE.md)
and the broader [Enterprise Knowledge Standard](KNOWLEDGE.md). For organization
changes, use [Administrator Department Provisioning](ADMIN-DEPARTMENT-PROVISIONING.md)
so Open WebUI Groups are not confused with Hermes Profiles.

These describe how EAO is intended to work now.

| Document | Purpose |
| --- | --- |
| `ADMIN-RESOURCE-INTAKE.md` | Administrator routing entry point for Knowledge, Tool/MCP/service, and third-party Skill intake |
| `ADMIN-DEPARTMENT-PROVISIONING.md` | Administrator workflow for department Groups, Profile reuse/creation, Assistant ACLs, and acceptance |
| `ARCHITECTURE.md` | Component responsibilities and architecture boundaries |
| `SECURITY.md` | Security model and least-privilege rules |
| `KNOWLEDGE.md` | WeKnora authority, knowledge boundaries, embedding/retrieval model |
| `PROFILE-STANDARD.md` | Hermes Profile conventions and boundaries |
| `CLIENT-RBAC.md` | Employee client/RBAC model |
| `COMPLETENESS.md` | CORE / CONFIGURED / PRODUCTION readiness semantics |
| `DEPLOYMENT.md` | Detailed deployment implementation guidance |
| `DEPLOYMENT-PRACTICES.md` | Reusable lessons validated during real installations |
| `ACCEPTANCE-TESTS.md` | Observable acceptance requirements |
| `BACKUP-RESTORE.md` | Backup/recovery contract |
| `OPERATIONS.md` | Operating procedures |
| `UPGRADE.md` | Version-change and upgrade rules |
| `CAPABILITY-REUSE-PASS.md` | Mandatory reuse-before-build decision gate |
| `SKILL-ADMISSION.md` | Third-party Skill compatibility, authority, adaptation, and delegation standard |
| `SELF-EVOLUTION.md` | Work-embedded employee experience → organizational intelligence design; repository-side Operations Skill mutation boundary at `../infrastructure/hermes/plugins/skill-mutation-guard/`; human-workload constraint, trust/promotion model, and runtime-audit gate |
| `REPOSITORY-GOVERNANCE.md` | Branch, PR, CI, frozen-history, and repository authority rules |

These should normally be read before specialized or historical files.

Machine-oriented Core provisioning contracts live with their component adapters:

- `../infrastructure/weknora/PROVISIONING.md` — WeKnora model/KB/credential reconciliation.
- `../infrastructure/hermes/PROVISIONING.md` — Hermes default/general Profile and shared-Gateway reconciliation.
- `../infrastructure/open-webui/PROVISIONING.md` — Open WebUI groups/connections/model ACL reconciliation.

## Tier 2 — Frozen/current capability baselines

These record accepted capability boundaries and evidence.

| Document | Meaning |
| --- | --- |
| `ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md` | Frozen Enterprise Operations v1.0 baseline |
| `ENTERPRISE-WEB-RESEARCH-V1.md` | Frozen Enterprise Web Research v1 capability |
| `ENTERPRISE-EMAIL-OPERATIONS-V1.md` | Governed Email Operations boundary |
| EAO-ADMIN-CONSOLE-V1A.md | Conditional governed EAO administrator capability |
| `EAO-RBAC-BASELINE.md` | Employee RBAC baseline |
| `OPERATIONS-EMPLOYEE-RBAC-AUDIT.md` | Operations RBAC audit evidence |
| `MCP-CONTROL-PLANE.md` | MCP inventory/control-plane contract |
| `THIRD-PARTY-SKILL-RUNTIME-ACCEPTANCE.md` | Runtime evidence for admitted direct-use third-party Skills |
| `OPEN-WEBUI-BRANDING.md` | Open WebUI branding implementation notes and boundary |
| `THIRD-PARTY-SKILL-ADMISSION-PILOT.md` | Non-normative evidence from the first real DIRECT / ADAPT / DELEGATE / REJECT admission pilot |
| `THIRD-PARTY-SKILL-ADAPT-RUNTIME-ACCEPTANCE.md` | Runtime evidence for the plugin-eval ADAPT compatibility pilot |
| `THIRD-PARTY-SKILL-PRODUCTION-ACCEPTANCE.md` | Production admission and Operations-only runtime evidence for `competitive-intel` |

Use these when reproducing or changing the corresponding capability.

## Tier 3 — Specialized v2 design and installation contracts

The `V2-*` documents preserve the detailed design/install contracts for the governed Communication & Email milestone.

Important examples include:

- `V2-SCOPE.md`
- `V2-EMAIL-DESIGN.md`
- `V2-INSTALLATION-ARCHITECTURE.md`
- `V2-CONFIG-PROTECTED-INPUTS.md`
- `V2-STAGE-CONTRACTS.md`
- `V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`
- `V2-GOVERNANCE-RUNTIME.md`
- `V2-SEND-RECONCILIATION.md`
- `V2-RECOVERY-CLEAN-HOST.md`
- `V2-INSTALLATION-DESIGN-REVIEW.md`

They are still useful contracts, but a fresh Agent should reach them through `config/capabilities.yaml`, `DEPLOY.md`, or the relevant capability document rather than treating the entire V2 set as the universal first-read path.

## Tier 4 — Historical migration and closure evidence

Files beginning with `PHASE4*` or `PHASE5*` record how ARMOR Operations Skills and related capabilities were migrated, deduplicated, audited, and closed.

Examples:

- `PHASE4A-ARMOR-MIGRATION.md`
- `PHASE4B-ARMOR-RUNTIME-CLOSURE.md`
- `PHASE4C-ARMOR-RUNTIME-CLOSURE.md`
- `PHASE5A-ARMOR-SOCIAL-MEDIA-MIGRATION.md`
- `PHASE5B-ARMOR-MIC-PRODUCT-OPTIMIZATION-MIGRATION.md`
- `PHASE5C-REMAINING-OPERATIONS-SKILLS-TRIAGE.md`
- `PHASE5D-WEBSITE-PRODUCT-MATERIALS-MIGRATION.md`
- `PHASE5E-ARMOR-PRODUCT-VISUAL-MIGRATION.md`

Supporting evidence under `inventory/` and `rbac/` belongs to this evidence layer unless another current contract explicitly says otherwise.

Use these files to understand provenance, migration decisions, and past acceptance. Do not automatically re-enable a legacy Skill or old runtime path because it appears in historical evidence.

## Tier 5 — Ontology research/design

`ONTOLOGY.md` and `ONTOLOGY-RESEARCH.md` document the EAO ontology/governance model.

They are architecture/design material. They do not create a separate graph database or generic Ontology runtime by themselves.

## Current reference deployment vs historical demo

Current sanitized ARMOR reference state is outside `docs/`:

```text
state/REAL-DEPLOYMENT-STATUS.md
```

Historical first local/demo validation is:

```text
state/DEPLOYMENT-STATE.md
```

Do not treat the historical demo as the current Mac Studio runtime truth.

Fresh deployments must start their real operational state record from:

```text
state/DEPLOYMENT-STATE.template.md
```

Copy that template to protected deployment storage. Do not turn the historical
demo record or sanitized public status file into the private runtime state store.

Material deployment history is recorded in:

```text
state/CHANGELOG.md
```

Protected real runtime state remains outside public Git when it contains private company information.

## Reference material

The sanitized machine-readable ARMOR reference index is:

```text
reference/armor/reference-index.yaml
```

It points to existing runtime/RBAC/capability authorities and is deliberately
non-normative and non-deployable as company configuration.

The `reference/` directory and the root ARMOR v1 architecture document are reference evidence.

They may provide company context or historical rationale, but they are non-normative unless a current contract explicitly incorporates them.

## Finding the right document for a task

Use this shortcut:

| Task | Start here |
| --- | --- |
| Understand EAO | `README.md` → `AGENTS.md` → `REPRODUCE.md` |
| Rebuild EAO | `REPRODUCE.md` → `DEPLOY.md` |
| Validate a fresh Agent | `VALIDATE.md` |
| Introduce an administrator-discovered resource | `ADMIN-RESOURCE-INTAKE.md` |
| Add durable knowledge | `ADMIN-RESOURCE-INTAKE.md` → `KNOWLEDGE-INTAKE.md` |
| Assess a new Tool / MCP / service | `ADMIN-RESOURCE-INTAKE.md` → `CAPABILITY-REUSE-PASS.md` |
| Add a capability | `CAPABILITY-REUSE-PASS.md` → `config/capabilities.yaml` |
| Assess a third-party Skill | `ADMIN-RESOURCE-INTAKE.md` → `CAPABILITY-REUSE-PASS.md` → `SKILL-ADMISSION.md` (pilot report is example evidence, not authority) |
| Change architecture | `AGENTS.md` → `ARCHITECTURE.md` → `SECURITY.md` |
| Maintain repository / GitHub workflow | `REPOSITORY-GOVERNANCE.md` |
| Work with knowledge | `KNOWLEDGE.md` |
| Design or implement employee-learning / Self-Evolution | `SELF-EVOLUTION.md` → `CAPABILITY-REUSE-PASS.md` → inspect actual Hermes runtime before enablement |
| Change Profiles | `PROFILE-STANDARD.md` |
| Change employee access | `CLIENT-RBAC.md` / `EAO-RBAC-BASELINE.md` |
| Deploy | root `DEPLOY.md` → `DEPLOYMENT.md` |
| Validate runtime | `ACCEPTANCE-TESTS.md` |
| Recover | `BACKUP-RESTORE.md` |
| Upgrade | `UPGRADE.md` |
| Inspect current ARMOR reference state | `../state/REAL-DEPLOYMENT-STATUS.md` |
| Understand an old migration decision | matching `PHASE*` file |

## Rule for new documentation

Before adding another document:

1. check whether an existing current contract should be updated instead;
2. avoid creating a second authority for the same topic;
3. classify the new file as normative, capability baseline, specialized design, historical evidence, or reference;
4. update this map only when the new file changes how a fresh reader should navigate the repository.

The goal is not more documentation. The goal is fewer ambiguous authorities.
