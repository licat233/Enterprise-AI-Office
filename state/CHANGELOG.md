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

### 2026-09-05 — Enterprise AI Office architecture repository initialized

Component: Project architecture / governance
Environment: Public reference repository

#### After

- Selected v1 architecture documented.
- WeKnora established as enterprise knowledge layer.
- Hermes Agent established as primary Agent runtime.
- Open WebUI established as employee Web client.
- hermes-webui established as administrative Hermes surface.
- Codex and Claude Code established as specialist coding workers.
- Apache-2.0 project license added.
- Agent operating contract, architecture, deployment, security, Profile, RBAC, knowledge, operations, backup, upgrade, and acceptance standards added.

#### Reason

Turn the initial ARMOR design into a reusable, AI-agent-readable Enterprise AI Office project.

#### Validation

Repository documents cross-reference the same responsibility boundaries and do not treat the public repository as an already deployed production system.

#### Rollback

Git history can restore earlier repository content. No production infrastructure is affected by this documentation bootstrap.
