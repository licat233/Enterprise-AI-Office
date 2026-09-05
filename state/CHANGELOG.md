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
- Repository changes are ordinary Git changes and have not been committed or pushed.

### Notes

- This is a local synthetic demo, not a production deployment. Hermes binds `0.0.0.0:8642` so OrbStack can reach the host process; keep it trusted-local-only.
- Employee MCP server names are intentionally unique per Profile because Hermes v0.21.0 multiplex registration is name-sensitive.

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
