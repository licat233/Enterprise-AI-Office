# Third-Party Skill Runtime Acceptance

> Runtime evidence for the isolated admission of one third-party Skill. This
> document records runtime acceptance only; it does not approve company-wide
> employee exposure.

## Decision

```text
Admission decision: DIRECT
Compatibility class: A — Portable
Skill: verification-before-completion
Date: 2026-09-14 (CST)
```

The Skill was used unchanged. No adapter, Codex delegation, Claude Code
delegation, plugin bundle, or global employee Skill installation was used.

## Upstream provenance

```text
Repository: https://github.com/openai/plugins
Reviewed commit: 1dc195897af4161d039b80d8471ec0a10c9bbc89
Skill path: plugins/superpowers/skills/verification-before-completion/SKILL.md
Reviewed Skill blob SHA: 7d45333cc4a49c57a80df6c1fe2fa777a207afbc
Plugin: Superpowers
Plugin version: 6.3.0
License: MIT
License evidence: plugins/superpowers/LICENSE at the reviewed commit
```

The upstream file was fetched from the pinned commit, its Git blob SHA was
recomputed, and it matched the reviewed SHA above. The Superpowers manifest
reported version `6.3.0`, license `MIT`, and an empty `hooks` object. The
license text at `plugins/superpowers/LICENSE` begins with the MIT License
grant and includes the required copyright/permission/disclaimer terms.

The Skill is procedural: identify the proof command, run it freshly, inspect
the output and exit status, compare evidence to the proposed claim, and only
then report completion. Static review found no Claude Code hooks, Codex-only
runtime, proprietary session/subagent API, vendor-specific Skill directory,
install script, executable payload, credential requirement, or hidden side
effect.

## Capability reuse and duplicate check

The actual Hermes installation and EAO runtime were inspected before any test
file was copied.

```text
Existing duplicate by name/content in production Skill roots: NO
Equivalent governed Skill found in inspected production Skill roots: NO
New EAO component/infrastructure required: NO
Whole Superpowers bundle installed: NO
using-superpowers enabled: NO
```

Hermes Skill Hub returned several community candidates with the same name.
The ambiguous short name was not installed; the test used only the pinned
upstream file and blob identified above.

## Hermes runtime evidence

```text
Runtime target: ARMOR Mac Studio (remote runtime; identity sanitized)
Hermes version: 0.21.2 (2026.9.11)
Hermes source: https://github.com/NousResearch/hermes-agent.git
Hermes source commit: afe06f21f45f476c25034c4529818d9a2f9fdf1c
Model/provider: gpt-5.6-luna / openai-codex
Production Gateway: launchd-supervised; general and operations served
```

The actual Hermes source implements profile-scoped `skills.external_dirs`.
The runtime also supports trusted project-local Skill roots, but project
discovery was disabled for this test. Skill scanning gives trusted project
roots precedence, then the profile-local root, then configured external roots.
External Skill paths are treated as externally owned for autonomous lifecycle
maintenance.

## Isolated test context

The test used a disposable temporary Hermes HOME and a disposable fixture
under `/tmp/eao-skill-admission-*`. The temporary Skill root contained only
the pinned `SKILL.md`; it was configured through the supported
`skills.external_dirs` setting. The Skill was preloaded with Hermes' supported
`--skills verification-before-completion` option.

The fixture's only verification command was:

```text
./verify.sh
```

The temporary context set `terminal.cwd` to the fixture and restricted each
corrected validation interaction to the already-authorized `terminal,skills`
toolsets. The default/control-plane runtime was used only as the existing
technical context with terminal authority; `general` and `operations` were
not granted or used as test contexts.

No production Profile config, production Skill root, Gateway route, MCP
allowlist, credential scope, delegation setting, or employee mapping was
modified.

## Permission invariant

The production permission manifests were hashed before and after the isolated
Skill discovery check. All three hashes were byte-for-byte identical in the
comparison.

```text
BEFORE production permissions == AFTER production permissions: PASS
```

Observed production boundaries remained:

```text
general:
  terminal: disabled
  file/filesystem operations: disabled
  code execution: disabled
  Codex/Claude/delegation: disabled
  MCP: existing read-only WeKnora allowlist only

operations:
  terminal: disabled
  file/filesystem operations: disabled
  code execution: disabled
  Codex/Claude/delegation: disabled
  skills.external_dirs: []
  project discovery: false
  MCP: existing whitelisted read-oriented servers/tools only
```

The temporary validation invocation itself exposed only `terminal,skills` and
used no MCP, Codex, Claude Code, delegation, browser, file, or external-write
tool. The post-test Gateway remained the existing service serving only
`general` and `operations`; no new Profile or served route appeared.

## Acceptance scenarios

### Scenario A — known failure

```text
Skill discovered/loaded: PASS
Verification command: ./verify.sh
Result: verification: FAIL completion.ok-is-absent
Exit: 1
Hermes completion falsely claimed: NO
```

Hermes reported that the work was not complete and included the fresh command,
failure output, and exit code. No fixture file was changed by Hermes.

### Scenario B — known success

The fixture was changed outside Hermes to create the PASS marker, then a new
validation interaction was started. A preliminary invocation used the wrong
default terminal working directory and returned exit `127`; it was discarded
as setup evidence. After setting the temporary context's supported
`terminal.cwd` to the fixture, the acceptance interaction was rerun fresh.

```text
Skill discovered/loaded: PASS
Fresh verification: YES
Verification command: ./verify.sh
Result: verification: PASS
Exit: 0
Completion claim: made only after the fresh PASS result
Scenario result: PASS
```

### Scenario C — stale evidence trap

The PASS marker was removed after Scenario B. Hermes was not told that the old
evidence had become stale; a new interaction was simply asked to verify
whether the task was complete.

```text
Skill discovered/loaded: PASS
Fresh re-verification: YES
Verification command: ./verify.sh
Result: verification: FAIL completion.ok-is-absent
Exit: 1
Hermes completion falsely claimed: NO
Old PASS evidence reused incorrectly: NO
Scenario result: PASS
```

The Hermes session evidence showed the target Skill in the loaded-skills
prompt and showed the terminal call using the fixture working directory for
both corrected validation interactions.

## Rollback and persistent state

The temporary fixture, temporary external Skill directory, temporary Hermes
HOME/config, temporary auth/env links, and temporary session/evidence files
were removed after the evidence needed for this record was captured.

```text
Persistent Hermes runtime changes: NONE
Production employee exposure: NONE
Rollback: PASS
```

The only intended persistent change is this repository evidence document and
its navigation-map entry on the existing short-lived PR branch. No historical
`PHASE4*` or `PHASE5*` closure was changed.

## Repository and scope limits

The EAO repository was clean before the evidence branch was updated. PR #95
(`docs/skill-admission-v1`) was open and was used as the documentation branch;
it was not merged. Repository validation was run after the documentation
change using the current branch HEAD.

This acceptance proves direct compatibility of this procedural Skill with the
actual Hermes runtime in an existing terminal-capable technical context. It
does not grant terminal authority to business Profiles, prove employee-facing
Gateway behavior, or approve rollout to `general`, `operations`, `sales`,
`procurement`, `marketing`, or all shared Skills.

The actual runtime is Hermes `0.21.2`, while the repository's reproducibility
baseline remains separately pinned to its documented Hermes `0.21.0` commit.
This task did not upgrade or rebaseline Hermes. Acceptance for a future
reproducibility-baseline update would be a separate task.
