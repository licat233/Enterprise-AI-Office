# Third-Party Skill Admission Pilot

> Evidence report for the first real application of `SKILL-ADMISSION.md`.
>
> Scope: static source/provenance/admission analysis only. No Mac Studio runtime
> installation or production Profile exposure was performed in this pilot.

## 1. Purpose

This pilot tests whether the EAO decision model:

```text
DIRECT → ADAPT → DELEGATE → REJECT
```

can classify real, high-quality GitHub Skills without forcing a pre-selected
answer.

The pilot intentionally uses current official/curated Agent ecosystems and
includes one source that is technically Hermes-aware but still unsuitable as
an EAO-wide control-plane Skill.

## 2. Reviewed upstream snapshots

| Source | Reviewed repository ref | Notes |
| --- | --- | --- |
| `openai/plugins` | `1dc195897af4161d039b80d8471ec0a10c9bbc89` | Current OpenAI Plugins snapshot used for Superpowers + Plugin Eval evidence |
| `anthropics/claude-plugins-official` | `022b3c274938ddfb9fd928fc582eb9b9ed0f537f` | Current Anthropic official plugin snapshot used for Claude Security evidence |

The decision is tied to the reviewed source state. A future upstream update
that materially changes tools, permissions, runtime dependencies, licensing, or
workflow semantics requires re-review.

## 3. Results at a glance

| Pilot | Skill | Source | Decision | Key reason |
| --- | --- | --- | --- | --- |
| A | `verification-before-completion` | OpenAI Plugins / Superpowers 6.3.0 | **DIRECT** | Pure procedural Skill; no hard Codex/Claude-only runtime primitive |
| B | `plugin-eval` | OpenAI Plugins / Plugin Eval 0.1.2 | **ADAPT** | Core local CLI is reusable, but Skill lookup and live benchmark assumptions are Codex-specific |
| C | `claude-security` | Anthropic official / 0.11.0 | **DELEGATE (conditional)** | Deep Claude Code-native Workflow/Agent/tool semantics + license restricts use to Anthropic products |
| D | `using-superpowers` | OpenAI Plugins / Superpowers 6.3.0 | **REJECT as EAO global entrypoint** | Technically Hermes-aware, but attempts to become the global process/Skill-selection control plane |

The pilot therefore produced all four intended outcomes without changing the
classification criteria after the fact.

## 4. Pilot A — DIRECT

### Candidate

```text
openai/plugins
plugins/superpowers/skills/verification-before-completion/SKILL.md
Skill blob SHA: 7d45333cc4a49c57a80df6c1fe2fa777a207afbc
Plugin version: 6.3.0
License: MIT (plugin manifest)
```

### What it actually requires

The Skill defines a verification discipline:

```text
identify proof command
→ run it
→ read output/exit status
→ compare evidence to claim
→ only then report success
```

It does not hard-code Codex-only subagent/session primitives, Claude Code
hooks/plugins, vendor-specific Skill directories, vendor-specific environment
variables, or a proprietary tool API.

Its required action is simply to run the appropriate verification command when
the target role already has authority to do so.

### Admission decision

```text
Class A — Portable
Decision: DIRECT
```

No translation of the Skill body is required.

### Authority boundary

DIRECT does **not** mean every EAO Profile receives terminal access.

Examples:

- an authorized Engineering/technical Profile may run build/test commands;
- a read-only business Profile may still use the evidence principle but cannot
  execute a command it lacks permission to run;
- installing the Skill must not add terminal, Git, filesystem write, or
  delegation authority.

### Runtime acceptance still required

Before production exposure to a terminal-capable technical Profile:

1. load the Skill through the supported Hermes Skill mechanism;
2. use a harmless disposable repository;
3. create a known failing test/build state;
4. verify the Agent does not claim success without fresh evidence;
5. verify the Agent reports failure accurately;
6. restore a passing state and verify the success claim cites fresh evidence.

Status in this pilot:

```text
STATIC ADMISSION: PASS — DIRECT
RUNTIME ACCEPTANCE: NOT EXECUTED
```

## 5. Pilot B — ADAPT

### Candidate

```text
openai/plugins
plugins/plugin-eval/skills/plugin-eval/SKILL.md
Skill blob SHA: 3d58206a936c83ae15cc274a623604f64925f17d
Plugin version: 0.1.2
License: MIT (plugin manifest)
Runtime dependency: Node.js >=20
```

### What is portable

The plugin ships a normal local Node.js CLI. Its local/static workflows include
skill/plugin analysis, budget explanation, measurement planning, benchmark
configuration preparation, and JSON/Markdown reporting.

The CLI can be invoked directly from its checked-out plugin directory and is not
intrinsically dependent on the Codex chat UI.

### What is Codex-specific

The Skill currently assumes:

```text
~/.codex/skills/<skill-name>
```

when resolving named Skills.

Its live benchmark path also launches real Codex CLI sessions. The plugin README
separates deterministic local analysis from live Codex benchmarking.

### Admission decision

```text
Class B — Semi-portable
Decision: ADAPT
```

The correct EAO adaptation is intentionally narrow:

1. replace the hard-coded local Skill lookup rule with EAO/Hermes approved Skill
   source resolution;
2. keep the upstream CLI and scoring/report logic unchanged;
3. invoke the CLI from an explicit reviewed local checkout/path rather than
   cloning its implementation into EAO;
4. mark live `benchmark` execution as unavailable unless an authorized
   Codex-delegation lane is active;
5. never let "evaluate a Skill" become permission to inspect arbitrary private
   host paths.

No "Codex Skill → Hermes Skill converter" is justified.

### Important mixed-runtime rule learned by the pilot

A Skill may be mostly portable while one optional subflow is backend-native.

That does not require reclassifying the entire Skill as DELEGATE if a thin
adapter can safely:

```text
portable subflow → run locally
backend-only subflow → explicit BLOCK or authorized delegation
```

The adapter must fail explicitly rather than silently escalating permissions.

### Runtime acceptance still required

1. run local deterministic analysis on a synthetic Skill fixture;
2. confirm EAO Skill roots resolve without `~/.codex/skills`;
3. confirm no unapproved directory traversal occurs;
4. confirm static analysis works without Codex auth;
5. request live benchmark from a non-authorized Profile and verify it is denied;
6. if an authorized technical Profile exists, separately verify the Codex
   benchmark through the existing coding-agent delegation boundary.

Status in this pilot:

```text
STATIC ADMISSION: PASS — ADAPT
ADAPTER IMPLEMENTATION: NOT YET CREATED
RUNTIME ACCEPTANCE: NOT EXECUTED
```

## 6. Pilot C — DELEGATE

### Candidate

```text
anthropics/claude-plugins-official
plugins/claude-security/skills/claude-security/SKILL.md
Skill blob SHA: 504ef679d739c59bc608d769805956faa0a80ac2
Plugin version: 0.11.0
License: proprietary Anthropic license in plugins/claude-security/LICENSE
```

### Runtime evidence

The Skill declares/uses native Claude Code concepts including:

- `Workflow` and named workflow invocation;
- multiple named `Agent(...)` workers/verifiers;
- `AskUserQuestion`;
- Claude plugin variables such as `${CLAUDE_PLUGIN_ROOT}` and
  `${CLAUDE_SKILL_DIR}`;
- Claude Code permission/auto-mode guidance;
- bundled scripts coordinated by the plugin runtime.

Porting this faithfully to Hermes would mean reconstructing significant parts of
the Claude Code plugin/agent/workflow runtime.

### License evidence

The plugin LICENSE states that the Plugin is proprietary to Anthropic and grants
a limited internal-use license solely with Claude Code or other Anthropic
products/services. It also restricts use with non-Anthropic products/services.

Therefore EAO must **not** copy, adapt, or redistribute this Skill into Hermes as
if it were an ordinary open Skill.

### Admission decision

```text
Class C — Agent-native
Technical decision: DELEGATE
Production admission: CONDITIONAL on applicable Anthropic terms
```

The architecture, if approved, is:

```text
authorized technical user
→ authorized Hermes technical Profile
→ existing Claude Code delegation boundary
→ Claude Code
→ claude-security plugin
→ bounded repository/workspace
```

The plugin remains inside Claude Code.

Hermes does not reinterpret its prompts, copy its agents, or emulate its
Workflow implementation.

### Licensing caution

This document records a technical governance decision, not legal advice.

Before production use, the operator must confirm that the intended internal
Hermes → Claude Code invocation pattern is permitted by the applicable
Anthropic agreement/license. If that cannot be confirmed:

```text
REJECT / DO NOT ENABLE
```

### Runtime acceptance still required

If license/terms permit and the capability is selected:

1. install/enable the plugin only in the Claude Code identity/context used by
   the authorized technical Profile;
2. use a disposable test repository;
3. verify normal business Profiles cannot reach the Claude backend;
4. verify workspace scope;
5. verify findings/patches do not auto-commit/push/apply;
6. verify no broader host credential set is exposed than required;
7. record backend/plugin version and acceptance evidence.

Status in this pilot:

```text
STATIC ADMISSION: PASS — DELEGATE (CONDITIONAL)
RUNTIME ACCEPTANCE: NOT EXECUTED
```

## 7. Pilot D — REJECT

### Candidate

```text
openai/plugins
plugins/superpowers/skills/using-superpowers/SKILL.md
Skill blob SHA: 7ab2eb678f649c8befb94512359ee0b6e9a9a9a4
Plugin version: 6.3.0
License: MIT
Upstream: obra/superpowers
```

### Why this is an important rejection sample

This is not rejected because it is low quality or incompatible.

The package explicitly ships Hermes Agent tool mapping, including mappings for
file read/write/patch, terminal, web search/extraction, `delegate_task`,
todo/task tracking, `skill_view`, and `AGENTS.md` / `SOUL.md` instruction
mapping.

So a superficial compatibility test would likely say:

```text
Hermes supported → install
```

That would be the wrong EAO decision.

### Control-plane conflict

The `using-superpowers` Skill requires Skill checking/invocation before any
response or action, including clarifying questions. It also establishes process
Skills as the first-order workflow authority.

EAO already has a repository/system control plane:

```text
AGENTS.md
→ Capability Reuse Pass
→ Profile/SOUL policy
→ approved Skills/tools
→ explicit delegation policy
```

Installing another global methodology entrypoint that attempts to govern every
conversation would create a second behavioral authority and increase cognitive
and upgrade coupling.

Its Hermes mapping also maps subagent dispatch to `delegate_task`. EAO's normal
business Profiles must not reactivate Agent Delegate / multi-agent
orchestration merely because a third-party methodology knows how to call it.

### Admission decision

```text
Class D — Non-admissible as an EAO-wide/global Skill
Decision: REJECT
```

This is a **scope-specific rejection**, not a judgment that Superpowers is a bad
project.

Individual Superpowers Skills can still be admitted independently. Pilot A is
the concrete proof: `verification-before-completion` is DIRECT even though the
global `using-superpowers` entrypoint is REJECT.

### Key lesson

```text
repository/plugin reputation
≠ blanket admission for every Skill inside it
```

Admission is performed at the smallest meaningful executable/procedural unit.

Status in this pilot:

```text
STATIC ADMISSION: PASS — REJECT
RUNTIME ACCEPTANCE: NOT APPLICABLE
```

## 8. Pilot conclusions

### 8.1 The four-way model works

The pilot found natural examples of DIRECT, ADAPT, DELEGATE, and REJECT without
changing the decision criteria to force those outcomes.

### 8.2 Agent labels are weak evidence

The useful decision inputs were actual SKILL.md content, runtime primitives,
bundled scripts/resources, tool/credential needs, plugin/runtime packaging,
license, and EAO authority fit.

"Supports Claude Code", "supports Codex", or even "supports Hermes" was not
enough to determine the admission decision.

### 8.3 Compatibility and authority remain separate

A technically compatible Skill can still be unavailable to a Profile that lacks
the required tools.

A delegated backend must not become a privilege proxy.

### 8.4 License can determine architecture

Claude Security demonstrates that a license may make "port to Hermes" an invalid
option even before engineering cost is considered.

License review belongs before copying/adapting third-party Skill content.

### 8.5 Admission must be granular

A repository/plugin is a source/provenance unit, not necessarily the admission
unit.

Different Skills from the same package may receive different decisions.

### 8.6 No universal converter is justified

Nothing in this pilot requires a generalized Skill conversion service.

The observed needs are covered by:

```text
direct source reuse
+
one thin path/runtime adapter case
+
existing backend delegation
+
rejection when a second control plane is not justified
```

## 9. Next implementation recommendation

Do **not** install all four samples.

The smallest useful next implementation is:

1. runtime-test one low-risk DIRECT Skill in an explicitly authorized technical
   test context;
2. only after DIRECT acceptance, implement a tiny adapter prototype for
   `plugin-eval` static/local analysis;
3. keep Claude Security uninstalled until license/terms and technical-profile
   delegation authorization are confirmed;
4. keep `using-superpowers` rejected as a global EAO entrypoint.

This preserves the upstream-first / smallest-change rule and gives EAO real
runtime evidence before broadening Skill ingestion.
