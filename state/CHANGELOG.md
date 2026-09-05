# Enterprise AI Office Deployment Changelog

This file is a template for material deployment changes.

Do not record secrets. Do not turn it into a transcript of every terminal command.

## Entry format

```markdown
## YYYY-MM-DD — Short change title

Component:
Environment:

### Before

<previous state>

### After

<new state>

### Reason

<why this change was needed>

### Validation

<tests / checks performed>

### Rollback

<how to return to previous state, if applicable>

### Notes

<known limitations / follow-up>
```

---

## 2026-09-05 — First end-to-end Enterprise AI Office demo validated

Component: WeKnora, Hermes Agent, Open WebUI, deployment adapters
Environment: Local Apple Silicon Mac with OrbStack; synthetic demo data

### Before

- Repository contained architecture and deployment templates, but no validated local runtime record.
- The local host had an existing Hermes installation that required inspection before reuse.

### After

- Pinned and started WeKnora `v0.8.0` and Open WebUI `v0.11.3` with loopback-only container ports.
- Kept Hermes `0.21.0` host-native and enabled the `general`, `sales`, and `qc` Profile gateway routes with distinct API keys.
- Added read-only WeKnora MCP access, synthetic Company & Brand and Products & Technical KBs, and completed document ingestion using the protected Qwen/DashScope fallback after the initial OpenAI quota failure.
- Configured Open WebUI groups, employee model ACLs, and three server-side Hermes connections. The privileged default/admin Profile is not employee-exposed.
- Validated the end-to-end path: Open WebUI → authorized Hermes Profile → WeKnora MCP → grounded knowledge answer with source title.
- Disabled employee long-term Profile memory because a validated per-user Hermes session-header mapping is not available in this connection path.
- Added the tested Open WebUI Compose manifest and minimal WeKnora demo override. Marked the operational helper scripts executable.
- Created a protected pre-change Hermes default Profile archive before modifying the existing installation.
- Captured the reusable demo findings in commit `cabbef0f226b45e497c71e4003aed38c20f07c0f` and pushed them to `origin/main`.

### Reason

Build the requested macOS/OrbStack Enterprise AI Office demonstration while preserving the repository's source-of-truth, RBAC, least-privilege, and production-boundary requirements.

### Validation

- Container health, Open WebUI sign-in, group/model visibility, direct Profile key isolation, and grounded Open WebUI chats passed.
- General, Sales, and QC grounded Profile answers returned source titles from WeKnora.
- Sales and QC terminal escape probes returned `NO_TERMINAL_TOOL`.
- Employee memory remained deliberately disabled; backup restore and host reboot recovery were not run.

### Rollback

- Stop the demo Compose services from the configured EAIO runtime directory and remove the three demo Profile configs if reverting the local setup.
- Restore the protected pre-change Hermes default Profile archive only after confirming the exact target and preserving current user changes.
- Repository documentation/adapters can be rolled back with normal Git history; prefer `git revert` of the relevant committed change instead of rewriting published `main` history.

### Notes

- This is a local synthetic demo, not a production deployment. Hermes binds `0.0.0.0:8642` so OrbStack can reach the host process; keep it trusted-local-only.
- Employee MCP server names are intentionally unique per Profile because Hermes v0.21.0 multiplex registration is name-sensitive.

## 2026-09-05 — Validate local backup and isolated restore

Component: WeKnora, Hermes Agent, Open WebUI, backup/restore helpers
Environment: Local Apple Silicon Mac with OrbStack; synthetic demo data

### Before

- The end-to-end demo was healthy, but no complete backup/restore rehearsal had
  been recorded.
- The host reboot recovery test had not been executed.

### After

- Added `scripts/backup.sh` for the inspected runtime: WeKnora PostgreSQL
  logical backup, WeKnora file storage, Open WebUI data, runtime configuration,
  Hermes Profiles/state/Skills/MCP, repository templates, protected credentials,
  a non-secret manifest, and checksums.
- Added guarded `scripts/restore.sh`, requiring a new target and
  `--confirm-isolated`; it restores into new temporary Docker resources and
  never stops or overwrites the live demo.
- Updated the backup/restore, operations, acceptance, and deployment-state
  documentation with the tested procedure and reboot continuation checklist.

### Reason

Verify that the current MacBook/OrbStack demo has a recoverable state without
adding components or changing the approved architecture.

### Validation

- Backup generation completed with PostgreSQL `pg_restore --list`, volume
  archive, manifest, and SHA-256 checks passing; secret values were not printed
  or committed.
- An isolated temporary Compose restore recovered both Knowledge Bases and
  document records; a restored Hermes Sales query returned the expected
  workflow and source title through the restored MCP configuration.
- Restored Open WebUI users signed in with Sales/QC model ACLs; unauthorized
  direct model probes returned HTTP 400 `Model not found`.
- Restored Hermes Profile key matrix returned only same-Profile HTTP 200s and
  cross-Profile HTTP 401s. Sales/QC terminal probes returned
  `NO_TERMINAL_TOOL`; employee memory remained disabled.
- `scripts/restore.sh` self-test also materialized a fresh temporary PostgreSQL
  container and both data volumes successfully.
- Host reboot recovery was intentionally not run because the active Codex
  session cannot safely resume and prove post-reboot state.

### Rollback

- The new helpers are ordinary repository files and can be reverted through
  Git. The live demo was not modified by the isolated restore.
- Remove only the exact temporary containers/volumes/targets listed by the
  restore helper after inspection; retain the successful backup generation.

### Notes

- The backup is still on the primary Mac and has no configured retention or
  encrypted off-device copy; this is not production disaster-recovery sign-off.
- Current final status is `PARTIAL — reboot recovery not yet executed`.

## Repository bootstrap history

### 2026-09-05 — Enterprise AI Office executable repository baseline created

Component: Project architecture / governance / implementation bootstrap
Environment: Public reference repository

#### After

- Selected v1 architecture documented.
- WeKnora established as enterprise knowledge layer.
- Hermes Agent established as primary Agent runtime.
- Open WebUI established as employee Web client.
- hermes-webui established as administrative Hermes surface.
- Codex and Claude Code established as specialist coding workers.
- Apache-2.0 project license added.
- Third-party license boundaries documented.
- `AGENTS.md` added as the highest-priority AI agent operating contract.
- Generic architecture, deployment, security, Profile, RBAC, knowledge, operations, backup, upgrade, and acceptance standards added.
- Generic `config/company.example.yaml` and non-secret environment template added.
- Reusable General, Sales, QC, Marketing, and Engineering SOUL templates added.
- Initial shared `company-knowledge` and `enterprise-security` Hermes Skill templates added.
- Infrastructure adapter guidance added for WeKnora, Open WebUI, and Hermes.
- Read-only `preflight.sh` and `health-check.sh` operational helpers added.
- Deployment-state template added.
- ARMOR separated as the first reference implementation rather than the universal project identity.
- Contribution guidance and runtime/secret `.gitignore` rules added.

#### Reason

Turn the initial ARMOR-specific design into a reusable, AI-agent-readable and increasingly executable Enterprise AI Office project that another company or AI engineering agent can understand without reconstructing the architecture from conversation history.

#### Validation

- Repository root and target directories were re-read after creation.
- README documentation map and repository tree were synchronized to actual files.
- Generic documents preserve the same component/source-of-truth boundaries.
- Public templates contain placeholders rather than production secrets.
- The repository explicitly distinguishes tested architecture/standards from runtime-specific deployment manifests that still require validation on the first real ARMOR deployment.

#### Rollback

Git history can restore earlier repository content. No production infrastructure is affected by this repository bootstrap.

#### Next validation milestone

The next major milestone is the first ARMOR Mac Studio deployment. That deployment should validate exact upstream versions, real service/volume names, Open WebUI ↔ Hermes Profile/RBAC/memory behavior, Codex/Claude Code delegation under the long-running service account, backup/restore commands, Kanban, Cron, and the selected enterprise messaging platform. Reusable validated runtime artifacts can then be promoted into `infrastructure/` and `scripts/`.
