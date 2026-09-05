# Operations Scripts

This directory contains small, reviewable, non-destructive helper scripts for Enterprise AI Office.

The scripts are not a replacement for understanding the deployed upstream versions.

## Principles

- Read-only health/preflight checks are preferred where possible.
- Destructive actions do not belong in convenience scripts without explicit safeguards.
- Production secrets must not be embedded in scripts.
- Version-specific commands should be introduced only after validation against the pinned upstream release.
- A generic script should fail clearly rather than guess service names/paths.

## Current scripts

### `health-check.sh`

Read-only high-level health check for:

- disk usage;
- Docker availability;
- configured HTTP health endpoints;
- Hermes CLI/status when available;
- optional backup freshness marker.

Configure URLs/thresholds through environment variables; see `config/.env.example`.

## Planned after reference deployment validation

The project may later add:

- deployment preflight checks;
- WeKnora backup wrappers for the exact tested deployment;
- Open WebUI backup wrappers;
- Hermes backup wrappers;
- restore verification helpers;
- automated acceptance-test helpers.

Do not add a generic `backup.sh` that guesses database container/service names. Backup tooling must match the tested runtime and must never create false confidence.
