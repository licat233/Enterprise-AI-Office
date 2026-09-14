# Coding-Agent Delegation Playbook

Codex and Claude Code are optional specialist execution backends. They are not ordinary employee tools and must not be exposed merely because their CLIs exist on the host.

Enable this playbook only when `capabilities.coding_delegation.enabled: true` and company configuration names the authorized Hermes Profile(s) and workspace/repository boundaries.

## 1. Security model

```text
Authorized employee
→ restricted technical Assistant
→ privileged Hermes technical Profile
→ approved repository/workspace
→ Codex and/or Claude Code
```

Do not give `general` or normal business Profiles terminal/coding-agent access by default.

A Hermes Profile is not an OS sandbox. Terminal access is a real privileged host capability even when `terminal.cwd` points at one repository.

## 2. Technical Profile configuration

Use [`technical-profile.config.example.yaml`](technical-profile.config.example.yaml) as the configuration starting point for an authorized coding Profile rather than extending the knowledge-only specialist template by guesswork.

It explicitly enables the Hermes API toolsets required for coding delegation:

```text
terminal/process
file
skills
read-only WeKnora MCP
```

and uses an explicit approved workspace plus Profile-scoped HOME for deliberate CLI credential isolation.

The local terminal backend is still not a filesystem sandbox. If the configured risk boundary requires stronger enforcement, use a supported Docker/sandbox/OS isolation design and validate the coding CLIs inside it.

## 3. Upstream-first coding integration

The validated Hermes reference commit ships bundled `codex` and `claude-code` orchestration Skills. Use those supported upstream capabilities rather than creating another coding-agent wrapper.

Inspect the bundled Skills for the exact selected Hermes version because CLI flags/auth behavior can evolve.

### Codex

Validated-reference prerequisites:

```bash
npm install -g @openai/codex
codex --version
```

Authenticate the Codex CLI under the HOME/service context actually used by the technical Profile. Standalone Codex CLI OAuth and Hermes' own `openai-codex` model-provider authentication are separate concerns.

For ordinary one-shot work, prefer the bundled Skill's `codex exec` workflow inside an explicit Git repository/workdir, then inspect the diff and run relevant tests.

Hermes 0.21.0 also has an optional Codex app-server runtime. Enable it only when company configuration deliberately selects that runtime and its tool trade-offs are acceptable. It is not required merely to delegate coding tasks to the Codex CLI.

### Claude Code

Validated-reference prerequisites:

```bash
npm install -g @anthropic-ai/claude-code
claude --version
claude auth status
```

Authenticate Claude Code under the technical Profile's actual CLI HOME/context.

For unattended one-shot work, prefer `claude -p` with an explicit workdir, bounded tools, and bounded turns rather than an uncontrolled interactive session.

Do not use `--dangerously-skip-permissions` as a default Enterprise AI Office integration policy.

## 4. Backend-native third-party Skills

Some third-party Skills are genuinely Codex-native or Claude-Code-native. Evaluate them under [`../../docs/SKILL-ADMISSION.md`](../../docs/SKILL-ADMISSION.md).

Installing a backend-native Skill does not expand who may use coding delegation.

The execution boundary remains:

```text
authorized employee
→ authorized technical Assistant/Profile
→ approved coding backend
→ approved backend-native Skill
→ explicit workspace
```

Do not use Codex or Claude Code as a privilege proxy for `general`, Operations, Sales, Marketing, Procurement, or another normal business Profile that lacks coding-agent authority.

A delegated Skill must remain inside the same backend, workspace, credential, repository-instruction, side-effect, and verification rules defined by this playbook. If the Skill requires broader authority, treat that as a separate Profile/capability change requiring explicit review rather than silently inheriting the backend's host privileges.

Prefer the backend-native Skill when its value depends materially on native session, sandbox, hook, plugin, subagent, review, or worktree semantics. Prefer direct Hermes use or a thin adapter when those semantics are not actually required.

## 5. Repository-local instructions

Before a coding backend modifies a repository, Hermes/the coding agent must read repository-local instructions such as:

```text
AGENTS.md
CLAUDE.md
.cursorrules
project README / contribution rules
```

The target repository's own rules outrank generic coding assumptions.

## 6. Workspace policy

Company configuration declares allowed workspaces, for example:

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

Do not infer broad home-directory access from an empty workspace list. A missing required workspace is `BLOCKED — REQUIRED INPUT`.

For higher-risk work, use worktrees/disposable clones or another approved isolation boundary.

## 7. Authentication and credentials

Validate separately:

```text
Hermes model/provider auth
Codex CLI auth
Claude Code auth
Git/GitHub auth
other repository-specific credentials
```

Do not copy all host credentials into a Profile `.env`.

With `terminal.home_mode: profile`, initialize only the required CLI identities/configuration inside that Profile-scoped HOME.

## 8. Delegation completion contract

A coding task is not successful merely because the coding CLI exits zero.

Required evidence:

```text
correct repository/workdir
→ requested change
→ inspectable diff
→ relevant tests/checks
→ accurate result summary
```

Do not silently commit, push, merge, release, or deploy unless company/repository policy explicitly authorizes those actions.

## 9. Acceptance

Use a disposable or harmless test repository before real work.

For each enabled backend:

```text
[ ] CLI installed and version recorded
[ ] auth works in the technical Profile/service-user context
[ ] only authorized technical Profile/users can invoke it
[ ] effective Hermes toolsets match the privileged role design
[ ] explicit allowed repository/workdir used
[ ] repository-local instructions read
[ ] small change is inspectable
[ ] tests/verification run
[ ] unrelated host resources are not intentionally granted
[ ] Hermes reports result accurately
```

Record enabled backend(s), version, auth boundary, Profile, workspace scope, and acceptance result in deployment state.
