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

These describe how EAO is intended to work now.

| Document | Purpose |
| --- | --- |
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
| `REPOSITORY-GOVERNANCE.md` | Branch, PR, CI, frozen-history, and repository authority rules |

These should normally be read before specialized or historical files.

## Tier 2 — Frozen/current capability baselines

These record accepted capability boundaries and evidence.

| Document | Meaning |
| --- | --- |
| `ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md` | Frozen Enterprise Operations v1.0 baseline |
| `ENTERPRISE-WEB-RESEARCH-V1.md` | Frozen Enterprise Web Research v1 capability |
| `ENTERPRISE-EMAIL-OPERATIONS-V1.md` | Governed Email Operations boundary |
| `EAO-RBAC-BASELINE.md` | Employee RBAC baseline |
| `OPERATIONS-EMPLOYEE-RBAC-AUDIT.md` | Operations RBAC audit evidence |
| `MCP-CONTROL-PLANE.md` | MCP inventory/control-plane contract |
| `OPEN-WEBUI-BRANDING.md` | Open WebUI branding implementation notes and boundary |

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

Material deployment history is recorded in:

```text
state/CHANGELOG.md
```

Protected real runtime state remains outside public Git when it contains private company information.

## Reference material

The `reference/` directory and the root ARMOR v1 architecture document are reference evidence.

They may provide company context or historical rationale, but they are non-normative unless a current contract explicitly incorporates them.

## Finding the right document for a task

Use this shortcut:

| Task | Start here |
| --- | --- |
| Understand EAO | `README.md` → `AGENTS.md` → `REPRODUCE.md` |
| Rebuild EAO | `REPRODUCE.md` → `DEPLOY.md` |
| Validate a fresh Agent | `VALIDATE.md` |
| Add a capability | `CAPABILITY-REUSE-PASS.md` → `config/capabilities.yaml` |
| Change architecture | `AGENTS.md` → `ARCHITECTURE.md` → `SECURITY.md` |
| Maintain repository / GitHub workflow | `REPOSITORY-GOVERNANCE.md` |
| Work with knowledge | `KNOWLEDGE.md` |
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
