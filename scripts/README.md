# Operations Scripts

This directory contains small, reviewable helpers for Enterprise AI Office.

Scripts support the deployment contract; they do not replace understanding the selected upstream versions or the AI agent execution flow in `DEPLOY.md`.

## Principles

- Prefer read-only inspection/checks where possible.
- Fail clearly rather than guess service names, paths, capabilities, or secrets.
- Production secrets never belong in scripts.
- Version-specific commands belong here only after validation against the selected runtime.
- Restore actions must target an isolated/new location unless an explicitly reviewed recovery procedure says otherwise.

## `repository-readiness-check.sh`

Static, non-installing repository self-check.

For a public clone, Fresh-Agent check, CI job, or another company's blueprint work, run:

```sh
EAO_REPOSITORY_ONLY=1 sh scripts/repository-readiness-check.sh
```

This is the portable repository check.

The script also retains a runtime-inclusive/reference mode for the existing ARMOR validation lineage. That mode may inspect protected `private/department-profile/*` material and ARMOR-specific closure evidence, so it is **not** the command a fresh public clone should run.

Do not treat missing ARMOR private Profile files as a repository defect when validating a fresh clone. Use repository-only mode for that purpose.

It verifies that the repository still contains the execution contracts, machine-readable configuration, core adapters, conditional capability playbooks, acceptance gates, state template, and production-control helpers needed to resolve a deployment.

It also checks a few critical cross-references such as:

```text
DEPLOY.md → config/capabilities.yaml
AGENTS.md → CONFIGURED READY
ACCEPTANCE-TESTS → Configured Ready gate
company config → target_readiness
```

A PASS means the **repository execution paths are structurally present**. It does not prove that a real host deployment or an external integration works; runtime acceptance remains required.

## `check-frozen-baselines.py`

Frozen local evidence-history check.

Run from a checkout with full Git history:

```sh
python3 scripts/check-frozen-baselines.py
```

It reads every `frozen_commit` declared in `config/eao-manifest.yaml`, verifies the commit object is present, and requires that commit to remain an ancestor of the checked HEAD. It validates EAO repository evidence SHAs only; upstream component commits are outside its scope.

GitHub Repository Readiness uses a full-history checkout specifically so this gate is meaningful.

## `check-yaml-syntax.sh`

Public YAML syntax gate for repository configuration/contracts.

Run:

```sh
sh scripts/check-yaml-syntax.sh
```

It uses Ruby/Psych's parser to parse YAML ASTs under the public configuration,
infrastructure, reference, state, validation, workflow, Profile, and Skill
trees. It does not deserialize application objects and does not claim schema or
business-policy correctness.

The gate exists to catch malformed YAML before higher-level text/path checks can
produce a false PASS.

## `check-capability-acceptance.py`

Dependency-free structural validation for capability acceptance references.

Run:

```sh
python3 scripts/check-capability-acceptance.py
```

It reads the `acceptance.document` plus `section` / `sections` references
declared in `config/capabilities.yaml` and requires each referenced Markdown
heading to exist. It catches renamed/misspelled acceptance anchors but does not
decide whether an older stage is semantically sufficient; final-stage selection
still requires architecture/capability review.

## `check-capability-selectors.py`

Dependency-free integrity check for conditional capability selection and
deployment-record metadata.

Run:

```sh
python3 scripts/check-capability-selectors.py
```

It requires every `kind: conditional` capability to declare both:

- selection metadata;
- `records` metadata describing the non-secret operational evidence/state that
  must be preserved after deployment.

Generic selectors must use `source: company_configuration`, and every declared
selector path must exist in `config/company.example.yaml`.
ARMOR-reference-specific workflows remain explicit selection exceptions and are
not forced into the generic company schema; they still must declare records.

## `check-validated-stack-consistency.py`

Dependency-free cross-file check for derived Core runtime pins.

Run:

```sh
python3 scripts/check-validated-stack-consistency.py
```

It reads the authoritative versions, upstream provenance, acquisition metadata,
and runtime-identity expectations from `config/validated-stack.yaml`. It
verifies the derived Open WebUI image tag, WeKnora/Hermes reference markers,
and the deterministic Core acquisition + post-acquisition identity assertions
in `DEPLOY.md` remain synchronized. Historical RBAC snapshots are excluded
because they are immutable evidence rather than current deployment pins.

## `check-public-repository-hygiene.py`

High-confidence public Git hygiene check.

Run:

```sh
python3 scripts/check-public-repository-hygiene.py
```

It rejects tracked protected/local directories, production `.env`/credential/private-key file classes, private-key blocks, a small set of high-confidence token signatures, and sensitive uppercase environment assignments whose values are not obvious placeholders/test fixtures.

This is intentionally narrower than a full secret-scanning product. It avoids treating sanitized historical host paths, public company names, or arbitrary prose as secret leakage.

## `check-declarative-paths.py`

Machine-readable contract path integrity check for `config/eao-manifest.yaml`, `config/capabilities.yaml`, and the sanitized ARMOR `reference/armor/reference-index.yaml`.

Run:

```sh
python3 scripts/check-declarative-paths.py
```

It verifies repository-relative implementation, acceptance, evidence, contract, and entrypoint paths that are declared in those YAML files. It intentionally uses no YAML package and only recognizes unambiguous repository path prefixes/root contract filenames.

## `check-repository-links.py`

Repository-wide, network-free Markdown link integrity check.

Run:

```sh
python3 scripts/check-repository-links.py
```

It scans Git-tracked Markdown files, validates repository-local file/directory links, rejects paths that escape the repository, and ignores external URLs, document-local anchors, and site-root application routes.

## `run-public-offline-tests.sh`

Portable zero-production-access regression suite for a fresh clone.

Run:

```sh
sh scripts/run-public-offline-tests.sh
```

The suite currently covers:

- Email Governance schema/hash/review binding;
- send/reconciliation state;
- backup/restore recovery behavior;
- Phase 1 governed email runtime with fake provider data;
- SMTP send-outcome safety with fake sessions;
- Enterprise Web Research normalization/security/path behavior.

The suite uses synthetic fixtures, in-memory or temporary local state, and fake providers. It must not contact a real mailbox, production service, or protected runtime.

Tests that require ARMOR private Vault/Profile state are intentionally excluded from this public suite and remain deployment/reference acceptance tests.

## `validate-ontology.py`

Lightweight structural validation for design-time examples under `ontology/examples/`.

Run:

```sh
uv run scripts/validate-ontology.py
```

The script uses PEP 723 inline metadata so its small YAML dependency is resolved for that script without creating a project-level Python environment.

It deliberately checks only mechanical consistency, including examples such as:

```text
duplicate YAML keys
unknown Object/Property/Relation/system references
invalid Authority references
fail-open Object visibility in design examples
Read Operation traversal/filter/projection authorization closure
Action precondition references
approval binding references
unknown tool-binding system namespaces
idempotency expressions using undeclared action parameters
operation-surface references
```

It does **not** execute business rules, connect to external systems, validate real employee authorization, generate MCP tools, or make an Ontology design example operational.

A validator PASS means the current YAML is structurally self-consistent according to the implemented checks. It does not mean the business policy is correct or Production Ready.

## `preflight.sh`

Read-only host inventory before installation/change. It inspects OS/architecture,
resources, Core prerequisites, optional/operator tools, Docker availability,
existing Hermes state/runtime directories, and repository status.

Core prerequisites are Git, Docker CLI + reachable daemon, Docker Compose,
Python 3, curl, and bash. Missing Core prerequisites produce FAIL. Optional or
pre-existing tools such as Node/npm, Hermes, OrbStack CLI, Codex, Claude Code,
and GitHub CLI produce WARN when absent because they are not universal Core
requirements.

A non-macOS-arm64 host is also a compatibility WARN rather than an automatic
architecture rejection; it must not inherit the exact reference-host
qualification without revalidation.

## `health-check.sh`

Read-only high-level deployed-system health check for:

- disk usage;
- Docker availability;
- configured HTTP health endpoints;
- Hermes CLI/status when available;
- optional backup freshness marker.

Configure URLs/thresholds through the protected deployment environment; see `config/.env.example` for placeholders.

## `backup.sh`

Backup helper derived from the validated MacBook/OrbStack reference runtime. It discovers the inspected WeKnora/Open WebUI/Hermes state and creates the tested classes of backup material, including PostgreSQL dump, persistent-data archives, runtime configuration, Hermes state, the protected operational deployment-state/handoff record when present, protected credential recovery material, manifest, and checksums.

The deployment-state source defaults to
`${EAIO_RUNTIME_DIR}/state/deployment-state.md`. Set
`EAIO_DEPLOYMENT_STATE_FILE` when the protected operational copy lives
elsewhere. The script never uses the repository's historical
`state/DEPLOYMENT-STATE.md` as the real runtime state source.

Use only after reconciling it with the actual selected component/storage layout:

```sh
./scripts/backup.sh "$EAIO_RUNTIME_DIR/backups/$(date -u +%Y%m%dT%H%M%SZ)"
```

The generated local archive is not automatically an off-device production backup. Move/protect it according to the active production backup policy.

## `restore.sh`

Guarded isolated restore-materialization helper:

```sh
./scripts/restore.sh \
  "$EAIO_RUNTIME_DIR/backups/<timestamp>" \
  "$EAIO_RUNTIME_DIR/restore-tests/<new-target>" \
  --confirm-isolated
```

It verifies backup checksums and restores material into new temporary resources rather than overwriting the live deployment. Complete service-level bring-up and acceptance according to `docs/BACKUP-RESTORE.md`.

## Scope boundary

Backup/restore helpers are tied to the validated runtime family and must be reviewed after upstream upgrades, storage migrations, container/volume naming changes, or Hermes layout changes.

They are not a generic disaster-recovery product and must not create false confidence about encryption, off-primary retention, startup recovery, or external service credentials.
