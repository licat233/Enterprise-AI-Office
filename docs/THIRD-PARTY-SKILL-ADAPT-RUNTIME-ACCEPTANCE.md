# Third-Party Skill ADAPT Runtime Acceptance

> Runtime evidence for the isolated `plugin-eval` ADAPT pilot. This document
> does not authorize company-wide employee exposure or live Codex benchmarking.

## Decision

```text
Admission decision: ADAPT
Compatibility class: B — Semi-portable
Candidate: plugin-eval
Date: 2026-09-14 (CST)
Runtime target: armor@MacStudio.local
```

The upstream local/static evaluator was reused through one thin EAO/Hermes
adapter. The adapter was tested in a disposable Hermes context and is not
configured in `general`, `operations`, or any employee route.

## Upstream provenance

```text
Repository: https://github.com/openai/plugins
Reviewed commit: 1dc195897af4161d039b80d8471ec0a10c9bbc89
Skill path: plugins/plugin-eval/skills/plugin-eval/SKILL.md
Reviewed Skill blob SHA: 3d58206a936c83ae15cc274a623604f64925f17d
Plugin manifest version: 0.1.2
Plugin manifest license: MIT
Node requirement: >=20.0.0
```

The reviewed `.codex-plugin/plugin.json` reports version `0.1.2`, license
`MIT`, and the stated repository. The private Node package's `package.json`
reports version `0.1.0`; this is an upstream package/manifest metadata split,
not a second runtime release. The plugin README identifies the package as
private and the manifest is the plugin-version authority used for this record.
The split remains a maintenance caveat and requires re-review if upstream
release metadata or packaging semantics change. No upstream source was edited.

## Capability Reuse Pass

```text
Existing plugin-eval installation in production Skill roots: NO
Existing equivalent EAO Skill evaluator: NO
Existing EAO repository evaluator: NO
New adapter required for the tested named-Skill workflow: YES
Whole plugin marketplace installed: NO
Codex/Claude delegation enabled by this pilot: NO
```

EAO repository readiness, capability-acceptance, migration, and ontology
validators were inspected. They do not provide the same deterministic
Skill/plugin quality, budget, and measurement analysis. Historical references
to unrelated LLM-evaluation Skills are not active equivalent coverage.

## What is portable

- `analyze <explicit-path>`: deterministic local structural and budget analysis.
- `explain-budget <explicit-path>`: deterministic local budget explanation.
- `measurement-plan <explicit-path>`: deterministic local measurement guidance.
- Local `report`, `compare`, and benchmark preparation/reporting logic where
  the operation does not launch a live Codex session.
- JSON and Markdown rendering from the upstream CLI.

## Codex-specific assumptions

- The upstream Skill resolves a named Skill through `~/.codex/skills/<name>`.
- The upstream budget baseline reads Codex-specific home/cache roots.
- The plugin bundle uses a Codex `.codex-plugin` manifest and Codex chat
  entrypoint conventions.
- `benchmark` launches real `codex exec` sessions with Codex-specific
  workspace, approval, and telemetry assumptions.

The upstream CLI accepts an explicit absolute target path and has no external
runtime dependency beyond Node for the tested local/static commands. This is
the compatibility seam; the live benchmark path remains outside this pilot.

## Adapter

```text
Path: infrastructure/hermes/skill-adapters/plugin-eval.js
Size: 76 lines
Responsibility:
  - accept only analyze, explain-budget, and measurement-plan;
  - resolve lowercase hyphen-case names only inside absolute approved roots;
  - pass the resolved absolute Skill path to the pinned upstream CLI;
  - return NOT FOUND for unknown names;
  - BLOCK path-like/escaping names before upstream invocation;
  - BLOCK benchmark/live Codex execution in this context;
  - pass only minimal PATH/HOME environment variables to the child process.
Upstream source modified: NO
New authority, database, daemon, MCP server, scheduler, or credential store: NO
```

The adapter does not search the host, inspect arbitrary employee homes, copy
the upstream scoring engine, or convert Skills between Agent runtimes. Its
inputs are explicit environment configuration for the approved roots and the
pinned upstream checkout; missing or relative roots fail closed.

## Approved roots

```text
Runtime variable: PLUGIN_EVAL_APPROVED_SKILL_ROOTS
Pilot root: /tmp/eao-skill-adapt-FYrQys/fixtures
Upstream variable: PLUGIN_EVAL_UPSTREAM_ROOT
Pilot checkout: /tmp/eao-skill-adapt-FYrQys/plugins/plugin-eval
```

The paths above were disposable pilot paths. No production Hermes Skill root
or employee home was added. The adapter accepts only simple names such as
`sample-good`; `/etc`, `~/.ssh`, `../../`, and equivalent path-like input is
rejected before the upstream CLI is started.

## Runtime context

```text
Hermes: 0.21.2 (2026.9.11)
Hermes source commit: afe06f21f45f476c25034c4529818d9a2f9fdf1c
Hermes source: https://github.com/NousResearch/hermes-agent.git
Node: v26.8.1
```

The test used a disposable `HERMES_HOME`, a temporary external Skill root
containing the pinned upstream `plugin-eval` Skill, synthetic fixtures, and an
existing technical/control-plane context. Corrected Hermes interactions used
only `terminal,skills`; no MCP, browser, file, code-execution, Codex,
Claude Code, delegation, or external-write tool was exposed.

## Acceptance scenarios

### Scenario A — direct upstream CLI baseline

```text
Command: node <plugin-eval>/scripts/plugin-eval.js analyze <sample-good> --format json
Result: PASS
Exit: 0
Score/grade: 100/A
Fixture files changed: NO
```

The same direct checkout also passed `explain-budget` and
`measurement-plan`. Upstream `npm test` passed 28/28 tests with the remote
Node path made explicit.

### Scenario B — Hermes through thin adapter

```text
Result: PASS
Hermes session: 20260914_152222_7aee82
Loaded Skill: plugin-eval
Adapter resolution: sample-good -> approved fixture root
Upstream CLI actually executed: YES
Upstream result: score 100/A, exit 0
```

The exported session contains a terminal call invoking the adapter and a tool
result containing both the adapter's resolved path and the upstream
`# Plugin Eval Report` output. Hermes summarized the actual upstream result.

### Scenario C — bad Skill detection

```text
Result: PASS
Hermes session: 20260914_152301_11e907
Fixture: sample-bad
Upstream result: score 58/D, exit 0
Findings: 3 failures
```

Upstream findings were `name-not-hyphen-case`, `description-missing`, and
`broken-relative-links`; the missing coverage artifact was informational.
Hermes reported the findings separately and did not invent PASS.

### Scenario D — unknown Skill

```text
Result: PASS
Hermes session: 20260914_152324_7dcb57
Result: NOT FOUND: approved Skill "does-not-exist"
Adapter exit: 2
Host-wide search occurred: NO
Upstream plugin-eval invoked: NO
```

### Scenario E — path escape

```text
Result: PASS
Hermes session: 20260914_152341_684ccd
Input: ../../
Result: BLOCKED before upstream invocation
Adapter exit: 2
Upstream plugin-eval invoked: NO
```

Equivalent `/etc` and `~/.ssh` inputs were also rejected by the same
simple-name guard.

### Scenario F — live benchmark boundary

```text
Result: PASS
Hermes session: 20260914_152359_5d7bb2
Input: benchmark sample-good
Result: BLOCKED: live Codex benchmark is unsupported in this adapter context
Adapter exit: 2
Codex silently invoked: NO
Claude Code invoked: NO
```

The adapter blocks the backend-only subflow before path resolution or CLI
launch. This pilot did not run `plugin-eval benchmark` or any `codex exec`
session.

## Permission invariant

Production Hermes permission manifests were hashed before and after the
isolated test and remained byte-for-byte identical:

```text
/Users/armor/.hermes/config.yaml:                 3c55210f2b9b2db756942498c7d3905acef1e078dfeb2e0c0d7a22592b30f4b8
/Users/armor/.hermes/profiles/general/config.yaml: fa4e51f90e20bb506e1ccd2c376b7161fcaaf944f23ddbb37102d0d8d3c5536d
/Users/armor/.hermes/profiles/operations/config.yaml: 01fea211cbb675dc09001cf332df638f55361ea54b9d05c2ec7926721b5c4c5c
BEFORE == AFTER: PASS
```

```text
General permissions changed: NO
Operations permissions changed: NO
Codex delegation changed: NO
Claude Code delegation changed: NO
MCP exposure changed: NO
Credentials changed: NO
Employee Skill exposure changed: NO
```

Observed production boundaries remained: `general` has terminal, file,
code-execution, and delegation disabled with only its existing read-only
WeKnora MCP allowlist; `operations` has those privileged toolsets disabled,
`skills.external_dirs: []`, `project_discovery: false`, and only its existing
read-oriented MCP allowlists. No production Profile, route, or Gateway
allowlist was changed.

## Production exposure and Gateway observation

```text
Production employee exposure: NONE
general: NOT USED / NOT MODIFIED
operations: NOT USED / NOT MODIFIED
Company-wide exposure: NONE
```

The procedure issued no Gateway control command. A Gateway restart was
observed in the existing production log during the broader test window; the
post-check remained healthy, launchd-supervised, and served only `general` and
`operations`. This was recorded as an operational observation, not treated as
an adapter permission change and not expanded into root-cause investigation.

## Rollback and persistent state

```text
Persistent Hermes runtime config/Profile permission changes: NONE
Persistent employee exposure: NONE
Disposable fixtures/Hermes HOME/upstream checkout/session exports: removed after evidence capture
Rollback: PASS
```

The adapter is separable from the upstream checkout and can be removed with
one repository revert; no runtime restart or employee migration is required.
The repository evidence document and navigation-map entry are the intended
persistent changes.

## Maintenance assessment

```text
Upstream remains source of truth: YES
Adapter complexity: LOW
New operational authority/state: NONE
Maintenance assessment: LOW
Recommendation: KEEP ADAPTER
```

Keep the adapter only for deterministic local/static analysis. Re-run the
admission review when upstream changes path resolution, requested tools,
network/credential behavior, benchmark semantics, licensing, or manifest
packaging. Do not expose it to employee Profiles without a separate Profile
capability and acceptance decision.

## Final classification

```text
ADAPT RUNTIME PILOT: PASS
Final classification: ADAPT
Final production status: ADMITTED + ADAPTER VALIDATED + NOT EMPLOYEE-EXPOSED
```

This pilot proves that `plugin-eval` local analysis works through a thin
Hermes compatibility layer. The adapter resolves approved EAO/Hermes Skill
paths and invokes the upstream local CLI; it does not enable Codex delegation,
Claude Code delegation, live benchmarking, or a universal Skill-conversion
layer.

## Remaining gaps

- No employee-facing Profile exposure was attempted or approved.
- Live Codex benchmarking remains unsupported in this adapter context and was
  intentionally not executed.
- The plugin manifest/package version split (`0.1.2` vs private package
  `0.1.0`) is an upstream metadata caveat and should be reconciled or reviewed
  before a future release-based packaging decision.
- The actual Hermes runtime is `0.21.2`, ahead of EAO's separately pinned
  reproducibility baseline `0.21.0`; this pilot did not upgrade or rebaseline
  Hermes.
- Gateway continuity was observed as healthy after the test, but Gateway
  restart behavior is outside this pilot's acceptance scope.
