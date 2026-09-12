# Backup and Restore Standard

Backups are a production requirement from v1, not a future enhancement.

This document defines what must be backed up, where it should be stored, and how recovery is verified.

When the conditional media_transcription capability is enabled, reviewed
Markdown transcripts under the derived runtime
media-transcription/transcripts/ directory are deployment data and must be
included in the encrypted backup generation. The job work/ directory is
ephemeral and should be empty after successful transcription; it is not a
separate recovery dependency. Transcription never auto-publishes to Company
Knowledge, so a restored transcript remains a reviewable local artifact until
an authorized operator chooses the documented WeKnora ingestion path.

## 1. Backup objective

A successful recovery must be able to restore:

```text
knowledge
+
users/access state
+
Hermes Profiles and automation
+
configuration
+
required secrets
```

to a usable state after host loss or major corruption.

## 2. Backup scope

### WeKnora

Back up:

- PostgreSQL data via a supported logical/native backup method;
- uploaded/original documents and persistent file/object storage;
- important application configuration;
- model/provider configuration metadata as applicable.

Do not assume Docker volume names remain constant forever. Discover actual persistent volumes/paths from the deployed version.

### Open WebUI

Back up:

- persistent database/data volume;
- server configuration needed to reconstruct authentication/groups/resources;
- any local persistent content required by the selected version.

### Hermes

Back up the active Hermes home(s), including production-relevant:

- Profiles;
- `config.yaml`;
- `SOUL.md`;
- Skills owned by the deployment;
- memory/state;
- sessions where business retention is desired;
- Cron jobs/history as appropriate;
- Kanban databases/attachments/workspaces that must persist;
- MCP/config metadata;
- logs only to the extent operationally useful.

Use Hermes upstream backup/export facilities where they correctly cover the required data, but verify their exclusions against this deployment.

### Company-owned Skills / configuration

Version-controlled non-secret Skills/config belong in the company's ops repository or equivalent source control.

Back up runtime-only local data as well.

### Protected operational deployment state

Back up the deployment's protected operational copy created from
`state/DEPLOYMENT-STATE.template.md`.

This state is small but operationally important because it carries the
non-secret identity handoffs needed to reconcile restored resources without
guessing, including:

- WeKnora logical Knowledge Base ID → runtime UUID mappings;
- retrieval-key record/reference metadata without plaintext tokens;
- model-role source/auth path plus symbolic provider-credential ref/native-binding metadata, never credential values;
- Hermes served Profile set, Profile routes, advertised model IDs, and
  non-secret credential reference names;
- Open WebUI logical group ID → display name → runtime UUID mappings;
- Open WebUI Profile connection exact URL plus observed/re-discoverable connection index/runtime handle;
- Profile/model/group ACL mappings;
- acceptance/recovery evidence.

The public historical `state/DEPLOYMENT-STATE.md` and sanitized public status
are **not** substitutes for this protected operational state.

The reference scripts use
`EAIO_DEPLOYMENT_STATE_FILE` when explicitly set, otherwise
`${EAIO_RUNTIME_DIR}/state/deployment-state.md`.

### Secrets

Back up production secrets using an encrypted/secure method and preserve a
documented recovery source.

Do not assume the optional `secrets/runtime-credentials.tar.gz` artifact is the
only secret-bearing backup file. The current backup helper can also capture
credentials inside:

```text
weknora/runtime-config.tar.gz   # protected runtime .env/config when present
hermes/runtime.tar.gz           # .env, Profile .env, auth.json/OAuth/provider state when present
open-webui/.env                 # protected runtime environment when present
secrets/runtime-credentials.tar.gz  # optional separate credential inventory
```

Therefore the **entire backup generation** is confidential/secret-bearing and
must receive the protection appropriate for production secrets. Do not put any
of these artifacts in this public repository.

### 2.1 Backup source runtime identity

A backup is only useful evidence when the source runtime is identified
unambiguously. On hosts that contain production plus test/restore Compose
projects, Docker service labels or container-name regexes can legitimately match
more than one running container. Stale/migrated layouts can likewise leave both
supported runtime-directory name variants present.

The repository helper therefore follows this rule:

```text
explicit EAIO_WEKNORA_RUNTIME_DIR / EAIO_OPENWEBUI_RUNTIME_DIR
→ use that runtime configuration directory

otherwise exactly one supported runtime-directory candidate
→ adopt it

explicit WEKNORA_POSTGRES_CONTAINER / WEKNORA_APP_CONTAINER / OPENWEBUI_CONTAINER
→ use that named running container, then validate the expected mounts/runtime

otherwise exactly one discovered container candidate for the required role
→ adopt it

more than one directory or container candidate
→ FAIL — ambiguous backup source; require an explicit existing override

zero candidates
→ existing missing-directory/container failure
```

Do not choose the first filesystem or Docker result. Do not assume the path
or container with the shortest/newest/reference-looking name is production.

`HERMES_HOME` defaults to the invoking user's `~/.hermes`; a deployment that
uses a different Hermes home must supply the observed active path explicitly.
Record that active Hermes runtime home in protected operational state.

Each backup manifest records the selected WeKnora/Open WebUI runtime paths,
Hermes home, actual PostgreSQL/WeKnora/Open WebUI source container names, and
discovered persistent volumes. Record the source-runtime identity/selection
result in protected operational state for Production Ready evidence.

The same fail-closed rule applies to the legacy restore compatibility path that
tries to recover a missing PostgreSQL image from a running container: a live
container may be used only when explicitly named or uniquely discoverable.

## 3. What is not enough

The following are not complete backup strategies:

- copying one Docker Compose YAML file;
- relying only on Git;
- copying files while omitting PostgreSQL;
- database backup without uploaded source files;
- keeping the only backup on the same internal SSD;
- relying on a running Docker volume with no export/recovery plan.

## 4. Backup destination

Maintain at least one backup copy on storage independent from the primary host disk.

Examples:

- NAS;
- external SSD rotated appropriately;
- backup server;
- approved encrypted remote/object storage.

The exact target depends on company policy.

For `PRODUCTION READY`, evidence must distinguish a local/primary-disk
validation generation from the approved independent production copy. Record at
least:

```text
backup generation ID/timestamp
approved off-primary destination/boundary
off-primary copy completion timestamp
integrity/checksum verification after transfer
freshness/retention result
restore source generation/location
final isolated restore result
```

A backup generated on the primary disk and an isolated restore from that same
primary-disk generation are useful recovery-path validation, but they do **not**
prove independence from host/disk loss.

## 5. Frequency

Default small-company starting policy:

```text
Daily backup
14 daily generations
4 weekly generations
```

Adjust for:

- document/change volume;
- recovery-point objective;
- available storage;
- compliance requirements.

### Blueprint revision provenance

Backup provenance contains two different repository identities and they must not
be conflated:

```text
Backup helper repository commit
= EAO checkout that executed scripts/backup.sh

Deployment blueprint commit
= EAO commit recorded in protected operational deployment state
  that actually governs the backed-up runtime
```

Those commits may legitimately differ. For example, `main` may advance after a
production deployment while the runtime intentionally remains on its previously
accepted blueprint revision.

New backup manifests therefore record both values. When protected operational
state contains a valid 40-character blueprint commit, the backup copies that
value into `MANIFEST.txt`.

During isolated restore, a new-format backup must have the restored protected
state's `EAO blueprint commit` match the manifest's `Deployment blueprint
commit`. A mismatch is a restore-integrity failure.

Older backups that predate this field remain readable, but absence of the
deployment blueprint commit is an evidence limitation. Verify/reconstruct the
governing revision before treating such a restored target as production-ready.

The backup helper checkout commit is tool provenance only. It must never be
silently substituted for the deployment blueprint authority.

## 6. Backup consistency

For major upgrades or migrations, create an explicit pre-change backup set that represents a recoverable point in time.

Record:

- component versions;
- database backup file/generation;
- file-storage backup generation;
- Hermes backup generation;
- Open WebUI backup generation;
- configuration version/commit;
- timestamp.

## 7. Database backup

Use the supported PostgreSQL backup approach for the installed WeKnora version.

Prefer a logical backup such as `pg_dump` for portability unless a documented deployment-specific method is better.

Do not copy raw live database files casually and assume consistency.

## 8. File storage backup

Back up WeKnora's real persistent document storage.

If storage later moves to S3/MinIO/another backend, update this document and deployment state to reflect the new recovery mechanism.

## 9. Open WebUI backup

Identify the actual persistent data path/database used by the installed release.

Back it up on the same schedule as other production state.

A restored Open WebUI should recover users/groups/resource configuration according to the capabilities of that release.

## 10. Hermes backup

Before a Hermes major upgrade or Profile-destructive change, create a fresh Hermes backup/export and verify its contents.

If Hermes upstream backup intentionally excludes large runtime/model caches, that is normally acceptable. Do not waste backup space on reproducible model/cache artifacts unless there is a reason.

## 11. Kanban backup

Kanban databases and durable attachments can contain business work state.

Ensure they are included when Kanban is in production use.

Disposable scratch workspaces do not necessarily need long-term backup unless they contain unpromoted business artifacts.

## 12. Cron backup

Cron definitions and relevant execution/audit state should be recoverable when scheduled automation is business-critical.

After restore, verify jobs are not accidentally duplicated by running both old and recovered schedulers simultaneously.

## 13. Secrets recovery

Maintain a secure inventory of required credentials, such as:

- model providers;
- WeKnora secrets;
- Profile API keys;
- messaging bots/apps;
- OAuth clients;
- GitHub/engineering access;
- remote storage credentials.

Recovery documentation should explain where secrets come from, without embedding them in public docs.

## 14. Restore-test schedule

Run a restore verification at least monthly for an active production deployment, or at an interval justified by company risk.

Also run one before production launch and after material backup-architecture changes.

## 15. Restore test environment

Restore into an isolated temporary environment when practical.

Avoid overwriting the live production system just to test backups.

### 15.1 Validated MacBook/OrbStack demo procedure

The local reference demo was validated on 2026-09-05 with the following
deployment-specific procedure:

1. `scripts/backup.sh` discovered the running WeKnora PostgreSQL, WeKnora
   `/data/files`, and Open WebUI `/app/backend/data` volumes.
2. WeKnora PostgreSQL was exported as a custom-format `pg_dump`; the archive
   was independently inspected with `pg_restore --list` and contained 657 TOC
   entries. The live PostgreSQL volume was not copied as a raw live database.
3. The WeKnora data-files volume was archived even though this synthetic demo's
   current document records use PostgreSQL-backed metadata/content and the
   volume was empty. A future upload that uses `/data/files` will therefore be
   covered by the same artifact.
4. Open WebUI data, WeKnora runtime configuration, Hermes Profiles/state/
   Skills/MCP configuration, repository Profile/Skill templates, the Hermes
   LaunchAgent definition, and a restricted runtime-credentials archive were
   captured. Secrets were not written to the repository or manifest.
5. `MANIFEST.txt` and `SHA256SUMS` were created. The successful backup is stored
   under `$EAIO_RUNTIME_DIR/backups/<timestamp>` on the demo host; it still
   needs an encrypted copy on independent storage before production use.

The backup was restored into a separate temporary Compose project and separate
Docker volumes. The restored WeKnora app/API became healthy, both demo Knowledge
Bases and their document records were present, and a Sales Profile query through
the restored MCP bridge returned the expected workflow plus the
`Demo Products & Technical` source title. A temporary Open WebUI instance
accepted all three restored demo accounts and retained the expected model ACLs.
The full Profile key matrix, unauthorized Open WebUI model probes, terminal
denial probes, and disabled employee-memory settings also passed against the
restored material. The temporary target used loopback-only ports and was
discarded after verification.

After this manual restore procedure succeeded, `scripts/restore.sh` was added.
It is a guarded restore-materialization helper: it requires a new target and
`--confirm-isolated`, verifies checksums, restores PostgreSQL and both data
archives into newly named temporary Docker resources, and never stops or
overwrites the live demo. Run the isolated service bring-up and acceptance
checks before relying on a newly restored target.

## 16. Restore verification

A restore is successful only when at least these checks pass:

For final `PRODUCTION READY` acceptance, the isolated restore must be sourced
from the approved off-primary backup copy (or an equivalent independently
stored generation), not merely from a generation that still resides on the
primary host disk. Verify the copied generation's checksums/integrity before
restore.

```text
[ ] WeKnora database starts
[ ] Knowledge Bases/documents are present
[ ] Representative retrieval works
[ ] Uploaded source files are available
[ ] Open WebUI state is recoverable as intended
[ ] Hermes Profiles are present
[ ] SOUL/Skills/config are present
[ ] Required MCP integrations can be reconnected
[ ] Kanban data is present if required
[ ] Cron definitions are present if required
[ ] Secrets can be restored/re-entered securely
```

For this MacBook demo, a host reboot was not executed because the active Codex
session cannot safely resume and prove post-reboot state. The exact continuation
check is:

```sh
OPEN_WEBUI_HEALTH_URL=http://127.0.0.1:3000 \
WEKNORA_HEALTH_URL=http://127.0.0.1:18080/health \
HERMES_HEALTH_URL=http://127.0.0.1:8642/health \
./scripts/health-check.sh
docker compose ls
docker ps
launchctl print "gui/$(id -u)/ai.hermes.gateway"
curl -fsS http://127.0.0.1:18080/health
curl -fsS http://127.0.0.1:8642/health
```

Then repeat the employee sign-in, Profile key matrix, RBAC, MCP grounding, and
terminal-denial checks from `docs/ACCEPTANCE-TESTS.md`. Until those commands are
run after a real Mac/OrbStack reboot, reboot recovery remains unexecuted.

## 17. Full disaster recovery order

A typical full-host recovery sequence:

```text
1. Provision supported OS/runtime
2. Restore ops repository/config baseline
3. Install pinned core component versions
4. Restore WeKnora database
5. Restore WeKnora file storage
6. Restore Open WebUI persistent state
7. Restore Hermes state/Profiles
8. Restore protected operational deployment-state/handoff record
9. Restore protected secrets
10. Start internal services
11. Verify knowledge retrieval
12. Verify Hermes Profile APIs/MCP
13. Verify employee RBAC and runtime ID mappings
14. Verify Cron/Kanban
15. Re-enable messaging/remote access
16. Run acceptance smoke tests and update recovery evidence
```

Do not expose employee access before core restore validation.

## 18. Upgrade rollback backup

Before a high-risk upgrade, record a rollback bundle/reference containing:

```text
previous component version
previous config commit
pre-upgrade DB backup
pre-upgrade files backup
pre-upgrade Hermes/Open WebUI state backup
```

Downgrading only an application image may be insufficient after a database migration.

## 19. Backup monitoring

A daily backup process should record:

- start/end time;
- success/failure;
- destination;
- artifact/generation identifier;
- high-level size if useful.

Alert/flag repeated failure.

Do not print secrets into backup logs.

## 20. Retention deletion safety

Retention cleanup should delete only generations outside policy.

Do not use broad destructive cleanup commands against paths/volumes that have not been positively identified as backup generations.

## 21. Encryption

Treat the whole EAO backup generation as confidential/secret-bearing, not only
the optional `secrets/` archive. Encrypt/protect it according to company
security policy before it is accepted as an off-primary production copy.

For `PRODUCTION READY`, the protected operational state must identify the
approved encrypted off-primary destination/boundary and record the
whole-generation confidentiality/encryption result without recording keys or
secret values.

Treat removable media as potentially losable.

## 22. Recovery objectives

A production company should eventually define:

- RPO: maximum acceptable data loss window;
- RTO: maximum acceptable recovery time.

The default daily policy is a starting point, not a universal compliance answer.

## 23. Backup acceptance checklist

```text
[ ] Database backup automated
[ ] File storage backup automated
[ ] Open WebUI state backed up
[ ] Hermes production state backed up
[ ] Protected operational deployment-state/handoff record backed up
[ ] Secrets have a secure recovery path
[ ] Entire backup generation is treated as confidential/secret-bearing and protected/encrypted accordingly
[ ] At least one approved copy is off the primary disk
[ ] Off-primary copy integrity/checksum verified after transfer
[ ] Retention and freshness against the off-primary destination verified
[ ] Backup failures visible
[ ] Isolated restore tested from the approved off-primary copy for Production Ready
[ ] Restored deployment-state/handoff mappings validated against restored resources
[ ] Last restore-test date recorded in protected deployment state
```
