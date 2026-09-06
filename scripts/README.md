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

Run:

```sh
sh scripts/repository-readiness-check.sh
```

It verifies that the repository still contains the execution contracts, machine-readable configuration, core adapters, conditional capability playbooks, acceptance gates, state template, and production-control helpers needed to resolve a deployment.

It also checks a few critical cross-references such as:

```text
DEPLOY.md → config/capabilities.yaml
AGENTS.md → CONFIGURED READY
ACCEPTANCE-TESTS → Configured Ready gate
company config → target_readiness
```

A PASS means the **repository execution paths are structurally present**. It does not prove that a real host deployment or an external integration works; runtime acceptance remains required.

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

Read-only host inventory before installation/change. It inspects OS/architecture, resources, common tools, Docker availability, existing Hermes state/runtime directories, and repository status.

Warnings are expected for optional components and should be interpreted against active company configuration.

## `health-check.sh`

Read-only high-level deployed-system health check for:

- disk usage;
- Docker availability;
- configured HTTP health endpoints;
- Hermes CLI/status when available;
- optional backup freshness marker.

Configure URLs/thresholds through the protected deployment environment; see `config/.env.example` for placeholders.

## `backup.sh`

Backup helper derived from the validated MacBook/OrbStack reference runtime. It discovers the inspected WeKnora/Open WebUI/Hermes state and creates the tested classes of backup material, including PostgreSQL dump, persistent-data archives, runtime configuration, Hermes state, protected credential recovery material, manifest, and checksums.

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
