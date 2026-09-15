# Upgrade and Rollback Standard

Production priority is:

```text
Validated Current > Unvalidated Latest
```

Hermes Agent is a **rolling-validated dependency**. EAO does not permanently pin
Hermes to one version. New Hermes capabilities should remain available to EAO,
but each production change must resolve one exact candidate commit, hold that
candidate stable for the transaction, validate it, record the resulting runtime
identity, and preserve a rollback point.

"Rolling" does not mean unattended auto-update. New upstream changes are
reviewed and validated before they replace the current production runtime.

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

Do not upgrade a stateful core component solely because a release exists.

For Hermes Agent, frequent upstream evolution is itself a legitimate reason to
periodically evaluate a newer candidate because EAO follows an upstream-first /
Capability Reuse Pass strategy. Evaluation still does not imply automatic
production promotion.

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
- protected operational deployment-state/handoff record;
- protected secret recovery path.

Record the current component versions and the protected operational-state
location before mutation.

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
- re-verify the provisioning API surface against the selected commit's
  `internal/router/router.go`, `routes_auth_tenant.go`,
  `routes_knowledge.go`, and `routes_infra.go`;
- re-check tenant API-key capability semantics and Knowledge Base allow-list
  enforcement used by the employee retrieval boundary;
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

## 11. Hermes rolling-validated upgrades

Hermes is intentionally different from fixed-image Core components:

```text
permanent Hermes version pin: NO
exact identity for every running deployment: YES
transaction-scoped candidate commit: YES
unattended production auto-update: NO
post-change acceptance: YES
rollback point: YES
```

At the start of a Hermes install/upgrade transaction:

1. record the current production version and commit;
2. preserve that accepted commit as the rollback / last-known-good point;
3. resolve the configured upstream tracking ref (normally `main`) once;
4. record that exact commit as `HERMES_CANDIDATE_COMMIT`;
5. use that same commit for source review, installer acquisition, installation,
   and acceptance during the whole transaction.

Do not re-resolve upstream halfway through a transaction.

Before promoting the candidate:

- inspect Profile/multiplex/Gateway changes;
- re-verify the provisioning behavior against the candidate commit's
  `hermes_cli/subcommands/profile.py`, `hermes_cli/profiles.py`,
  `gateway/config.py`, and `gateway/platforms/api_server.py`;
- confirm current bundled-Skill opt-out / Skill discovery semantics;
- confirm `/p/<profile>/` routing, Profile-scoped `API_SERVER_KEY`
  resolution/fail-closed behavior, and Profile model-ID advertisement;
- inspect API server changes;
- inspect Skills / Background Review / Curator behavior when those capabilities
  are relevant;
- inspect Cron/Kanban changes;
- inspect memory/session behavior;
- inspect tool/terminal security changes;
- inspect Codex/Claude Code integration changes;
- run the applicable Profile, RBAC, knowledge, tool-boundary, and capability
  acceptance tests.

After upgrade verify every production Profile, not only the default Profile.

If the candidate fails acceptance, do not normalize the failure as expected
drift. Restore the last-known-good Hermes commit/configuration and record the
failed candidate.

A successful candidate becomes the new observed/accepted runtime. Updating the
repository's Hermes reference identity records that accepted evidence; it does
not create a permanent product version lock.

## 12. Open WebUI upgrades

Before upgrading Open WebUI:

- inspect database/schema changes;
- inspect authentication/RBAC changes;
- inspect OpenAI connection configuration changes;
- re-verify the provisioning routes and first-admin bootstrap behavior against
  the selected commit's `backend/open_webui/main.py`,
  `backend/open_webui/utils/auth.py`, plus `routers/auths.py`, `groups.py`,
  `openai.py`, and `models.py`;
- confirm `WEBUI_ADMIN_*` still creates an administrator only when the user DB
  is empty, skips creation on an existing deployment, and keeps signup disabled
  after successful first-admin creation;
- inspect request/response schema changes for the exact admin/group/model
  reconciliation calls used by `infrastructure/open-webui/PROVISIONING.md`;
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
2. Read the protected operational state created from state/DEPLOYMENT-STATE.template.md
3. Inspect actual runtime/status
4. Record the current component runtime identity and last-known-good point
5. For Hermes, resolve one exact upstream candidate commit for this transaction
6. Read target release/source changes
7. Identify breaking/migration changes
8. Create the required pre-upgrade recovery point
9. Verify the recovery point exists
10. Apply the selected candidate
11. Run component health and exact runtime-identity checks
12. Run integration smoke tests
13. Run security/RBAC tests
14. Run relevant Golden Questions
15. Verify Cron/Kanban and other affected capabilities
16. Update the protected operational deployment state
17. Record the exact version/commit transition and evidence in state/CHANGELOG.md when it affects the reusable/reference baseline
18. For Hermes, update the reference identity only after acceptance; never reinterpret it as a permanent version pin
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

After a successful upgrade or rollback:

- update the **protected operational** deployment state created from
  `state/DEPLOYMENT-STATE.template.md`;
- update `state/CHANGELOG.md` when the change affects the reusable/reference
  baseline or materially changes deployment behavior;
- for fixed Core components, update `config/validated-stack.yaml` only after
  explicit qualification of a new reference baseline;
- for Hermes, update its reference/last-known-good identity after acceptance
  while preserving `version_policy: rolling-validated`;
- update relevant docs if upstream integration syntax changed.

Do not rewrite the historical public `state/DEPLOYMENT-STATE.md` as the live
runtime state store.

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
- forgetting to update protected operational deployment state;
- treating the Hermes reference identity as a permanent version lock;
- changing a Hermes production commit without an explicit acceptance/changelog evidence trail;
- treating a historical deployment-state observation as the current version authority.
