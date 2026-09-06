# Hermes Optional Feature Playbook

This playbook covers optional capabilities that are native to Hermes Agent and therefore should be enabled through Hermes itself rather than by adding new orchestration services.

Covered capabilities:

- Kanban;
- Cron;
- enterprise messaging through Hermes Gateway.

Enable only the sections selected by the company configuration.

## 1. Kanban

Hermes Kanban is the durable multi-Agent work queue. It is appropriate when work must survive context boundaries, service restarts, handoffs, review, or human intervention.

Do not enable Kanban merely to run a short synchronous subtask; use normal delegation for that.

### Deployment

On the validated Hermes 0.21.0 reference, Kanban is built into Hermes. The default dispatcher runs inside the Gateway. No external Kanban server should be added.

Minimal activation/verification flow:

```bash
hermes kanban init
hermes gateway start
hermes kanban boards list
```

Create additional boards only when company configuration defines a real project/domain boundary.

For orchestrator Profiles that need to create/route tasks directly, enable the Hermes `kanban` toolset explicitly. Do not add Kanban administration to ordinary employee Profiles by default.

### Required configuration decisions

Resolve:

- owning/orchestrator Profiles;
- board(s), if more than the default board is required;
- workspace policy (`scratch`, explicit directory, or Git worktree);
- any tenant/project isolation requirement;
- worker Profile tool/credential boundaries.

### Acceptance

Use a harmless temporary task:

```text
[ ] task created
[ ] intended Profile assigned
[ ] dispatcher starts worker
[ ] worker reads/updates task through Kanban tools
[ ] comment/review/completion lifecycle works
[ ] completed state persists across the relevant service restart
[ ] temporary test task/workspace is cleaned or retained according to policy
```

## 2. Cron

Hermes Cron owns scheduled Agent work. Do not add an external workflow engine for simple Hermes schedules unless a real requirement exceeds the built-in capability.

### Deployment

Cron is native to the selected Hermes runtime. Create only jobs declared by company configuration or explicitly authorized operations.

For repeatable unattended jobs, pin the intended model/provider policy so a later interactive model switch does not silently change cost or behavior.

Example operator flow on the validated Hermes reference:

```bash
hermes cron create "every 1d at 09:00" "<harmless-test-prompt>"
hermes cron list
```

Use an explicit absolute `--workdir` for repository/project automation. Attach only Skills required by that job.

### Required configuration decisions

Resolve:

- owning Profile;
- schedule/timezone;
- prompt/workflow;
- model/provider/cost policy;
- Skills;
- workdir when relevant;
- delivery target;
- failure/alert behavior.

### Acceptance

Create a harmless temporary scheduled job and verify:

```text
[ ] schedule accepted
[ ] job fires
[ ] expected output is produced/delivered
[ ] run history/status is recorded
[ ] pause/resume works
[ ] state survives the relevant service restart
[ ] temporary test job removed
```

Do not call Cron configured merely because `hermes cron list` works; at least one harmless execution must complete.

## 3. Enterprise messaging

Messaging is an alternate employee access/delivery surface, not a separate Agent architecture.

The company configuration must select an actual platform before deployment. Do not enable multiple messaging platforms for completeness.

Supported Hermes Gateway platforms evolve by release. For the selected pinned Hermes version, inspect and use that release's official setup documentation/CLI for the chosen platform.

Typical Enterprise AI Office choices may include Feishu/Lark, WeCom, or Weixin when the company actually uses them.

### Deployment contract

1. resolve selected platform from company configuration;
2. resolve required enterprise/bot credentials without committing or printing them;
3. use Hermes' supported Gateway setup/configuration for that platform;
4. restrict invocation with enterprise identity, pairing, or an explicit allowlist;
5. configure deterministic Profile routing;
6. start/restart the managed Gateway;
7. test an authorized and unauthorized identity;
8. test delivery for any enabled Cron/Kanban workflow that uses messaging.

Never set allow-all merely to get the integration working during production deployment.

### Multiplexed Profiles

When Hermes Profile multiplexing is enabled, keep routing explicit. A message must resolve to a Profile from authenticated platform context/configuration; arbitrary user prompt text must not be treated as authorization to switch to a privileged Profile.

### Required configuration decisions

Resolve:

```text
platform
credentials/application identity
authorized users/chats or enterprise identity rule
Profile routing
allowed message/file types
delivery targets
```

If these values are absent, the correct result is `BLOCKED — REQUIRED INPUT`, not an invented messaging policy.

### Acceptance

```text
[ ] authorized employee can invoke the intended Profile
[ ] unauthorized identity fails closed
[ ] routing reaches the intended Profile deterministically
[ ] privileged/default admin Profile is not reachable through ordinary employee messaging
[ ] file/media behavior works if enabled
[ ] outbound delivery works for configured automation
[ ] credentials remain outside Git/log output
```

## 4. State recording

For every enabled native Hermes feature, record actual configuration in `state/DEPLOYMENT-STATE.md`, including ownership, enabled objects, routing, model policy where applicable, and acceptance result.

Native availability is not the same as enabled capability. An unused built-in feature should remain recorded as disabled/not configured rather than being instantiated for completeness.
