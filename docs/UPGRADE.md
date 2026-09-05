# Upgrade and Rollback Standard

Production priority is:

```text
Stable > Newest
```

New upstream releases are reviewed, not automatically installed.

## 1. Components covered

This policy applies to core components including:

- WeKnora;
- Hermes Agent;
- Open WebUI;
- hermes-webui;
- database/storage components when version-managed separately;
- important model/provider changes;
- MCP bridges/integrations;
- company-owned Skills that materially change behavior.

## 2. No automatic core upgrades

Do not use unattended production mechanisms that blindly track:

- `main`;
- `latest`;
- unreviewed Docker tags;
- automatic `git pull`;
- automatic Hermes core update;
- generic auto-updaters for critical containers.

## 3. Upgrade trigger

Upgrade when at least one meaningful reason exists:

- security fix;
- required bug fix;
- compatibility requirement;
- valuable feature tied to a real business need;
- end-of-support/dependency pressure;
- planned maintenance consolidation with acceptable risk.

Do not upgrade solely because a release exists.

## 4. Pre-upgrade questions

Before every material upgrade answer:

```text
Current version?
Target version?
Why upgrade?
Relevant changes?
Breaking changes?
Database migrations?
Config changes?
Known regressions?
Backup status?
Rollback method?
Validation plan?
```

## 5. Read upstream information

Use current official release notes/docs/source for the target version.

Pay special attention to:

- configuration key changes;
- API path changes;
- authentication changes;
- database migrations;
- storage changes;
- Profile/Skills behavior changes;
- RBAC changes;
- deprecations;
- security advisories.

## 6. Create a pre-upgrade recovery point

For high-risk upgrades create and verify:

- WeKnora database backup;
- WeKnora file-storage backup;
- Open WebUI persistent-state backup;
- Hermes backup/state snapshot as appropriate;
- configuration/ops-repo commit reference;
- protected secret recovery path.

Record the current component versions.

## 7. Upgrade one core component at a time

Do not simultaneously major-upgrade WeKnora, Hermes, and Open WebUI unless a compatibility dependency makes that unavoidable and the combined migration has been explicitly planned.

Preferred:

```text
upgrade component A
→ verify
→ stabilize
→ upgrade component B later
```

This preserves root-cause visibility.

## 8. Test/staging strategy

When practical, test the target release using:

- a temporary environment;
- backup-restored test data;
- a non-production Profile/client;
- a small representative corpus.

For smaller installations where full staging is unreasonable, compensate with strong pre-upgrade backup and immediate post-upgrade acceptance tests.

## 9. WeKnora upgrades

Before upgrading WeKnora:

- inspect database migration notes;
- inspect storage changes;
- inspect model/retrieval compatibility;
- back up DB and uploaded files;
- verify parser/DocReader compatibility;
- rerun representative knowledge queries after upgrade.

A rollback may require restoring the pre-upgrade database, not only downgrading the container image.

## 10. Embedding-model changes are migrations

Changing the embedding model is not a casual model switch.

Before changing:

- record old/new model;
- record dimensions;
- understand index/re-embedding requirements;
- back up;
- benchmark on representative company queries;
- plan rollback/reindex.

Do not combine an embedding migration with unrelated large infrastructure changes if avoidable.

## 11. Hermes upgrades

Before upgrading Hermes:

- inspect Profile/multiplex/Gateway changes;
- inspect API server changes;
- inspect Skills sync behavior;
- inspect Cron/Kanban changes;
- inspect memory/session behavior;
- inspect tool/terminal security changes;
- inspect Codex/Claude Code integration changes.

After upgrade verify every production Profile, not only the default Profile.

## 12. Open WebUI upgrades

Before upgrading Open WebUI:

- inspect database/schema changes;
- inspect authentication/RBAC changes;
- inspect OpenAI connection configuration changes;
- inspect dynamic-header support used for Hermes session scoping;
- back up persistent state.

After upgrade verify group/resource ACLs and cross-user behavior.

## 13. hermes-webui upgrades

Because hermes-webui is an admin client, validate that it still connects to the deployed Hermes version and that administrative capabilities have not expanded to employee-facing access unexpectedly.

## 14. Model-provider changes

A chat/reasoning-model change normally requires functional benchmark/behavior validation.

A provider credential/endpoint change also requires:

- data-boundary review;
- cost/rate-limit review;
- Cron unattended-work review;
- fallback behavior review.

## 15. Company Skill changes

A Skill change that alters operational behavior should be version-controlled and tested against affected Profiles.

Security-sensitive Skills require review of:

- external commands;
- network calls;
- required environment variables;
- filesystem writes;
- tool prerequisites.

## 16. Standard upgrade sequence

```text
1. Read AGENTS.md and relevant docs
2. Read DEPLOYMENT-STATE
3. Inspect actual runtime/status
4. Confirm current version
5. Read target release notes
6. Identify breaking/migration changes
7. Create pre-upgrade backup
8. Verify backup exists
9. Record previous version/config
10. Apply upgrade
11. Run component health checks
12. Run integration smoke tests
13. Run security/RBAC tests
14. Run relevant Golden Questions
15. Verify Cron/Kanban if affected
16. Update DEPLOYMENT-STATE
17. Update CHANGELOG
```

## 17. Rollback decision

Rollback when:

- data integrity is at risk;
- employee access is broadly broken;
- security isolation fails;
- critical retrieval/agent behavior regresses and cannot be corrected safely with a small config fix;
- persistent migration error leaves the system unstable.

Do not remain on a broken target version merely to avoid admitting an upgrade failed.

## 18. Rollback method

A true rollback may include:

```text
previous application version
+
previous configuration
+
pre-upgrade database restore
+
matching file-storage restore
+
previous Hermes/Open WebUI state where required
```

Do not assume image downgrade reverses database migrations.

## 19. Post-rollback verification

Run the same smoke/security checks used after an upgrade.

Confirm:

- employees can access authorized assistants;
- unauthorized access still fails;
- knowledge retrieval works;
- Profiles work;
- Cron/Kanban state is sane;
- backup process remains healthy.

## 20. Documentation

After a successful upgrade or rollback, update:

- `state/DEPLOYMENT-STATE.md`;
- `state/CHANGELOG.md`;
- relevant docs if upstream integration syntax changed.

## 21. Security emergency exception

A critical actively exploited security issue may justify accelerated upgrade timing.

Even then:

- take a backup if doing so does not worsen the incident;
- document the emergency reason;
- preserve least privilege;
- run focused post-upgrade security validation.

## 22. Upgrade anti-patterns

Avoid:

- upgrading everything at once;
- relying on `latest` as version documentation;
- skipping DB backup before migrations;
- ignoring RBAC tests after client/auth upgrades;
- changing embedding and retrieval stack simultaneously without benchmark;
- accepting major behavioral drift because the containers are healthy;
- forgetting to update deployment state.
