# Operations Scripts

This directory contains small, reviewable helper scripts for Enterprise AI Office.

The scripts are not a replacement for understanding the deployed upstream versions.

## Principles

- Read-only health/preflight checks are preferred where possible.
- Restore actions require an explicit new target and confirmation; they do not stop,
  overwrite, or clean the live demo.
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

### `backup.sh`

Backup helper for the validated MacBook/OrbStack demo. It discovers the running
WeKnora PostgreSQL, WeKnora file, and Open WebUI Docker volumes, then creates:

- a custom-format WeKnora PostgreSQL dump and `pg_restore --list` validation;
- WeKnora document storage and Open WebUI data-volume archives;
- WeKnora/Open WebUI runtime configuration;
- Hermes Profiles, state, Skills/MCP configuration, and LaunchAgent definition;
- a restricted runtime-credentials archive;
- a non-secret `MANIFEST.txt` and `SHA256SUMS`.

Run it only against the inspected deployment:

```sh
./scripts/backup.sh "$EAIO_RUNTIME_DIR/backups/$(date -u +%Y%m%dT%H%M%SZ)"
```

The destination must not already exist. The generated archive is protected by
`umask 077`; move it to encrypted storage independent of the primary Mac before
treating it as a production backup.

### `restore.sh`

Guarded restore-materialization helper for a tested backup. It requires a new
target and an explicit `--confirm-isolated` flag:

```sh
./scripts/restore.sh \
  "$EAIO_RUNTIME_DIR/backups/<timestamp>" \
  "$EAIO_RUNTIME_DIR/restore-tests/<new-target>" \
  --confirm-isolated
```

It verifies checksums, extracts the protected runtime material, restores the
WeKnora PostgreSQL dump into a new temporary PostgreSQL container, and restores
the WeKnora/Open WebUI data archives into new Docker volumes. It intentionally
leaves those exact temporary resources for service-level inspection; it never
touches the live Compose projects or live Hermes installation. Complete the
isolated service bring-up and acceptance checks documented in
`docs/BACKUP-RESTORE.md`.

## Scope boundary

These scripts are tied to the current tested runtime and must be reviewed after
an upstream upgrade, storage migration, container rename, or Hermes layout
change. They are not a generic disaster-recovery product and must never create
false confidence about off-device retention, encryption, or host-reboot recovery.
