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
