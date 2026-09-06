# Coding-Agent Delegation Playbook

Codex and Claude Code are optional specialist execution backends. They are not ordinary employee tools and must not be exposed merely because their CLIs exist on the host.

Enable this playbook only when `capabilities.coding_delegation.enabled: true` and the company configuration names the authorized Hermes Profile(s) and workspace/repository boundaries.

## 1. Security model

The intended path is:

```text
Authorized employee
→ restricted technical Assistant
→ Hermes technical Profile
→ approved repository/workspace
→ Codex and/or Claude Code
```

Do not give `general` or other normal business Profiles terminal/coding-agent access by default.

A Hermes Profile is not an OS sandbox. The service user's CLI credentials and filesystem access are real capabilities. Define the working directory, repository policy, and credential scope before enabling coding delegation.

## 2. Upstream-first implementation

The validated Hermes reference commit already ships bundled `codex` and `claude-code` orchestration Skills. Use those supported upstream capabilities rather than inventing a second coding-agent wrapper.

For the selected Hermes version, inspect the bundled Skills before deployment because CLI flags and authentication behavior can change.

### Codex

At the validated Hermes reference commit, the bundled Codex Skill expects:

```bash
npm install -g @openai/codex
codex --version
```

Authenticate the Codex CLI for the OS/service user that Hermes will actually run as. Codex CLI OAuth state and Hermes' own `openai-codex` model-provider authentication are separate concerns; validate the CLI itself before delegation.

For ordinary one-shot coding delegation, prefer the bundled Skill's supported `codex exec` workflow inside an explicit Git repository/workdir, then inspect the diff and run tests.

Hermes 0.21.0 also provides an optional Codex app-server runtime. Use that only when the company configuration deliberately selects it and its tool/runtime trade-offs are acceptable; it is not required merely to use Codex as a specialist coding worker.

### Claude Code

At the validated Hermes reference commit, the bundled Claude Code Skill expects:

```bash
npm install -g @anthropic-ai/claude-code
claude --version
claude auth status
```

Authenticate Claude Code for the actual OS/service user. For unattended one-shot work, prefer Claude Code print mode (`claude -p`) with an explicit workdir and bounded allowed tools/max turns rather than an uncontrolled interactive session.

Do not use `--dangerously-skip-permissions` as a default Enterprise AI Office integration policy.

## 3. Repository-local instructions

Before a coding backend modifies a repository, Hermes/the coding agent must read repository-local instructions such as:

```text
AGENTS.md
CLAUDE.md
.cursorrules
project README / contribution rules
```

The repository's own rules outrank generic assumptions about how that codebase should be changed.

## 4. Workspace policy

Company configuration should declare allowed workspaces, for example:

```yaml
capabilities:
  coding_delegation:
    enabled: true
    allowed_profiles:
      - engineering
    backends:
      codex: true
      claude_code: true
    workspaces:
      - /absolute/path/to/approved/repository
```

Do not infer broad home-directory access from an empty workspace list. Treat a missing required workspace as `BLOCKED — REQUIRED INPUT`.

For higher-risk work, use worktrees/disposable clones or another approved sandbox boundary.

## 5. Authentication and credentials

Validate separately:

```text
Hermes model/provider auth
Codex CLI auth
Claude Code auth
Git/GitHub auth
other repository-specific credentials
```

Do not copy all host credentials into a Profile `.env`. Use the minimum credential set required by the authorized workspace and workflow.

If Profile-specific CLI identity is required, use Hermes' supported Profile HOME/terminal isolation mechanism and initialize the CLI credentials inside that boundary.

## 6. Delegation completion contract

A coding task is not successful merely because the coding CLI exits zero.

The technical Profile must return enough evidence to establish:

```text
correct repository/workdir
→ requested change
→ inspectable diff
→ relevant tests/checks
→ accurate result summary
```

Do not silently commit, push, merge, release, or deploy unless the company/repository policy explicitly authorizes those actions.

## 7. Acceptance

Use a disposable or harmless test repository before enabling real work.

For each enabled backend:

```text
[ ] CLI is installed and version recorded
[ ] authentication works in the Hermes service-user context
[ ] only an authorized technical Profile can invoke the capability
[ ] explicit allowed repository/workdir is used
[ ] repository-local instructions are read
[ ] backend makes a small inspectable change
[ ] tests/verification run
[ ] unrelated host resources are not intentionally granted
[ ] Hermes reports the result accurately
```

Record the enabled backend(s), version, auth boundary, Profile, and workspace scope in `state/DEPLOYMENT-STATE.md`.
