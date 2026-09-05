# Operations and Maintenance Manual

This document defines normal operating procedures for a deployed Enterprise AI Office.

The goal is not maximum operational ceremony. The goal is reliable service, recoverability, and enough state documentation that another human or AI agent can safely take over.

## 1. Operational priorities

Use this order:

1. preserve company data;
2. preserve recoverability;
3. preserve security boundaries;
4. understand current deployment state;
5. restore service with the smallest justified change;
6. document material changes.

## 2. Authoritative operational state

Before maintenance, compare:

```text
state/DEPLOYMENT-STATE.md
+
actual host/runtime state
```

If they differ, actual runtime is evidence of what is running, but the discrepancy must be reconciled and documented.

## 3. Routine cadence

### Automated daily

- backups;
- optional lightweight health check/report;
- existing approved business Cron jobs.

### Weekly operator review

Check:

- host disk usage;
- Docker/container health;
- WeKnora health;
- Open WebUI health;
- Hermes Gateway health;
- Profile health;
- WeKnora MCP/API access;
- backup freshness;
- repeated Cron/Kanban failures.

### Monthly maintenance review

Check:

- upstream stable releases/security notices;
- restore-test status;
- disk growth;
- stale test Profiles/jobs;
- unused credentials/integrations;
- access/group drift;
- knowledge ingestion quality issues.

Monthly review does not imply monthly upgrade.

## 4. Health status format

Prefer simple output:

```text
PASS / WARN / FAIL
```

Example:

```text
Host disk              PASS
Docker                 PASS
WeKnora                PASS
Open WebUI             PASS
Hermes Gateway         PASS
WeKnora MCP            PASS
Backup freshness       WARN
```

Do not deploy a large monitoring platform merely to produce a small-system health report.

## 5. Disk-space policy

Disk growth can come from:

- Docker images/volumes;
- databases;
- document uploads;
- indexes;
- logs;
- Hermes sessions/memory;
- Kanban attachments/workspaces;
- backups staged locally;
- coding repositories/worktrees.

Suggested general thresholds:

```text
< 70% used     normal
70–85% used    warning / investigate growth
> 85% used     action required
```

Adapt to real storage size and workload.

## 6. Service restart principle

Restart only the affected component when practical.

Do not reboot the entire host as the first troubleshooting step for every failure.

However, planned reboot testing is part of deployment acceptance.

## 7. Troubleshooting order

Use:

```text
symptom
→ health/status
→ logs
→ affected component
→ recent changes
→ root cause
→ minimal repair
→ verification
```

Do not reinstall the entire stack merely because one service is unhealthy.

## 8. Common fault domains

### Employee portal unavailable

Check:

- Open WebUI container/service;
- network/listener;
- storage/database state;
- authentication config.

### Employee can log in but assistant unavailable

Check:

- group/resource ACL;
- Hermes Profile connection;
- Profile API key;
- Hermes Gateway/Profile health;
- resource visibility.

### Hermes responds but company knowledge is missing

Check:

- WeKnora health;
- MCP/API bridge;
- KB visibility;
- document parsing/index readiness;
- retrieval results;
- Profile knowledge instructions.

### Knowledge answer is wrong

Check source quality first:

```text
source document
→ parsing
→ chunk/retrieval
→ rerank
→ reasoning
```

Do not automatically change the LLM because a source document is obsolete.

### Coding delegation fails

Check:

- Codex/Claude Code availability;
- authentication;
- PATH/environment under the Hermes service context;
- repository path;
- repository instructions;
- Profile tool permissions.

### Cron fails repeatedly

Check:

- job owner Profile;
- provider/model credentials;
- Skill prerequisites;
- workdir;
- delivery target;
- execution history.

Pause a repeatedly failing expensive job while repairing it.

### Kanban worker does not run

Check:

- Gateway/dispatcher health;
- assignee Profile exists;
- task status/dependencies;
- workspace path;
- worker/tool permissions;
- failure/block reason.

## 9. Profile operations

For Profile changes:

- inspect current config;
- avoid editing multiple Profiles unnecessarily;
- use a fresh session to validate SOUL/tool changes;
- test unauthorized capabilities;
- update Profile documentation when the contract changes.

## 10. User operations

New employee:

- create/activate user;
- assign minimum groups;
- verify one allowed assistant;
- verify one denied assistant.

Role change:

- remove old group access;
- add required new group access;
- verify effective resources.

Departure:

- disable/remove human access;
- revoke personal tokens if any;
- do not delete department Profiles or shared company knowledge.

## 11. Knowledge operations

Knowledge maintainers should:

- ingest current high-value documents;
- maintain metadata/status;
- mark old versions superseded;
- investigate conflicting retrieval sources;
- periodically remove obvious duplicate/noise entries only after confirming value/history requirements.

Do not let ordinary troubleshooting agents delete knowledge merely because an answer is confusing.

## 12. Secret rotation

Rotate credentials when:

- compromise is suspected;
- an administrator leaves;
- provider policy requires it;
- a credential was accidentally exposed;
- a major environment migration warrants new keys.

After rotation:

- update protected runtime secret locations;
- restart only necessary services;
- verify integrations;
- never commit the new secret.

## 13. Backup operations

Follow `BACKUP-RESTORE.md`.

A backup incident is operationally significant if:

- scheduled backup stops;
- off-device copy fails repeatedly;
- restore verification is overdue;
- storage retention unexpectedly collapses.

### 13.1 Validated local demo commands

The current MacBook demo uses the deployment-specific helpers below. Inspect
`state/DEPLOYMENT-STATE.md` and confirm the live container names before running
them; do not point them at an inferred or broad path.

```sh
./scripts/backup.sh \
  "$EAIO_RUNTIME_DIR/backups/$(date -u +%Y%m%dT%H%M%SZ)"
```

The backup must finish with `PASS backup complete`, and both the manifest and
checksums must be retained. Move the completed directory to encrypted storage
independent of the Mac. Do not add the generated archive to Git.

For a restore rehearsal, use a new target and explicit confirmation:

```sh
./scripts/restore.sh \
  "$EAIO_RUNTIME_DIR/backups/<timestamp>" \
  "$EAIO_RUNTIME_DIR/restore-tests/<new-target>" \
  --confirm-isolated
```

This creates new named Docker volumes and a temporary PostgreSQL container. It
does not stop the live `weknora`, `open-webui`, or Hermes services. Bring up a
separate Compose project with unused loopback ports, point the restored Hermes
Profile MCP URLs at the restored WeKnora API, and run the restore and security
checks before deleting only the exact temporary resources listed by the helper.

The 2026-09-05 rehearsal used a separate WeKnora API/frontend, Open WebUI,
and Hermes gateway port and verified Knowledge Bases, grounded retrieval,
Profile-key isolation, Open WebUI group/model ACL, terminal denial, and disabled
employee memory. This is evidence for the local demo only, not a production
off-device backup or reboot test.

## 14. Version review

When an upstream release appears:

- do not automatically upgrade;
- read release notes;
- identify security fixes relevant to the deployment;
- determine whether the current version has a real issue;
- plan/testing according to `UPGRADE.md`.

## 15. Production change recording

Record material changes in `state/CHANGELOG.md`.

Examples:

- component upgrade;
- model change;
- Profile permission change;
- new external integration;
- network exposure change;
- backup destination change;
- major Knowledge Base structure change.

Do not log every harmless UI click.

## 16. Host reboot recovery rehearsal

A real host reboot is an acceptance test, not something to infer from a healthy
pre-reboot process. On the current MacBook demo, prepare the exact post-reboot
continuation below and record the result in `state/DEPLOYMENT-STATE.md`:

```sh
OPEN_WEBUI_HEALTH_URL=http://127.0.0.1:3000 \
WEKNORA_HEALTH_URL=http://127.0.0.1:18080/health \
HERMES_HEALTH_URL=http://127.0.0.1:8642/health \
./scripts/health-check.sh
docker compose ls
docker ps
launchctl print "gui/$(id -u)/ai.hermes.gateway"
```

Then verify the two WeKnora services and Hermes health endpoints, employee
sign-in, the Profile key matrix, Open WebUI RBAC, a grounded query, and the
Sales/QC terminal-denial probe. Until a post-reboot check has completed, record
`REBOOT RECOVERY NOT YET EXECUTED`; a configured `restart: unless-stopped` or
LaunchAgent `KeepAlive` is only startup configuration evidence.

## 17. Incident notes

For a meaningful incident, record:

```text
Date/time
Impact
Symptoms
Root cause
Fix
Data/security impact
Verification
Preventive action if justified
```

Avoid long speculative narratives. Preserve actionable facts.

## 18. No silent architecture drift

Maintenance convenience must not gradually change architecture.

Examples of silent drift to avoid:

- exposing hermes-webui to employees because it is easier;
- giving Sales terminal because one task once needed a shell command;
- writing company facts into Profile memory instead of fixing knowledge ingestion;
- adding another vector DB before measuring retrieval need;
- sharing one API key across all Profiles for convenience.

## 19. Degraded-mode decisions

Prefer graceful temporary degradation over unsafe emergency expansion.

Examples:

- disable employee long-term memory if isolation fails;
- disable a broken external integration while core chat/knowledge remains healthy;
- pause a failing Cron job;
- keep messaging disabled while Web access works.

## 20. Handover to another AI agent

Before ending a maintenance session after material work:

- ensure repository changes are committed;
- update deployment state if reality changed;
- update changelog if material;
- leave no unexplained temporary debug configuration;
- report remaining known issues explicitly.

## 21. Operational anti-patterns

Avoid:

- using production as an experiment without rollback;
- blind `latest` upgrades;
- deleting volumes to fix application errors;
- leaving debug logging indefinitely;
- using a privileged Profile for ordinary employees;
- accumulating abandoned test Profiles and scheduled jobs;
- treating successful backup creation as proof of restore capability;
- relying on one internal SSD as the only backup location.
