# Third-Party Skill Admission Standard

> Normative decision standard for evaluating, integrating, and operating third-party AI Agent Skills in Enterprise AI Office.

## 1. Purpose

Enterprise AI Office uses Hermes Agent as the primary Agent runtime and governance boundary, while optional specialist execution backends such as Codex and Claude Code may be enabled for explicitly authorized technical work.

The external Skill ecosystem is larger than any one Agent runtime. A useful Skill may be described as "for Claude Code", "for Codex", or "for another Agent" even when most of its workflow is portable.

EAO therefore does **not** use vendor labels as the compatibility decision.

The admission question is:

```text
What does this Skill actually require at runtime?
```

The goal is to safely reuse high-quality upstream Skills without:

- unnecessarily rewriting portable Skills;
- creating permanent forks for small compatibility differences;
- using Codex/Claude Code delegation as a privilege-escalation path;
- duplicating existing EAO capabilities;
- turning EAO into a custom Skill-conversion framework.

This standard extends `CAPABILITY-REUSE-PASS.md`. It does not reopen the historical ARMOR Skill migration phases.

## 2. Core rule

For every third-party Skill, use this decision order:

```text
DIRECT
→ ADAPT
→ DELEGATE
→ REJECT
```

Meaning:

1. **DIRECT** — use the upstream Skill unchanged when its runtime requirements are compatible with Hermes and the target Profile's already-approved capabilities.
2. **ADAPT** — add the smallest thin compatibility layer when the workflow is portable but contains limited Agent-specific assumptions.
3. **DELEGATE** — keep the Skill in its native Codex/Claude Code execution environment when its value materially depends on that runtime and delegation is already authorized for the calling role.
4. **REJECT** — do not admit the Skill when it duplicates existing capability, requires unjustified privilege, has unacceptable supply-chain/licensing risk, or its maintenance/security cost exceeds its business value.

Do not jump directly from "Hermes cannot run this unchanged" to "install it in Codex/Claude Code".

## 3. Admission starts with Capability Reuse Pass

Before evaluating compatibility, determine whether the Skill is needed at all.

Required order:

```text
existing EAO capability
→ Hermes native capability
→ already approved/frozen Skill
→ selected upstream integration
→ third-party Skill admission
```

A popular or high-quality external Skill is not automatically useful to EAO.

The preferred outcome may be:

```text
NO NEW SKILL REQUIRED
```

## 4. Compatibility classes

### Class A — Portable Skill

Typical characteristics:

- workflow/instructions primarily live in `SKILL.md` or equivalent declarative material;
- references, templates, prompts, and scripts are self-contained;
- required operations map to capabilities Hermes already exposes to the target Profile;
- no hard dependency on a vendor-specific session model, hook system, subagent runtime, slash-command implementation, or proprietary orchestration primitive.

Default treatment:

```text
DIRECT
```

A README saying "Claude Code Skill" or "Codex Skill" does not by itself disqualify it.

### Class B — Semi-portable Skill

Typical characteristics:

- core workflow is portable;
- small portions assume vendor-specific tool names, file locations, instruction filenames, command names, environment variables, or output conventions;
- those assumptions can be mapped without reproducing another Agent runtime.

Default treatment:

```text
ADAPT
```

The adapter should contain only compatibility logic, for example:

- tool-name mapping;
- path/context mapping;
- supported command replacement;
- metadata normalization;
- explicit unsupported-step handling.

Do not copy and rewrite the whole upstream Skill merely to change a few runtime assumptions.

### Class C — Agent-native Skill

Typical characteristics:

- materially depends on Codex or Claude Code runtime behavior;
- requires native hooks, plugins, subagents, session/process semantics, vendor-specific commands, coding sandbox behavior, worktree orchestration, or other runtime primitives whose semantics are part of the Skill itself;
- removing those dependencies would amount to reimplementing the original Agent runtime.

Default treatment:

```text
DELEGATE
```

Keep the Skill with its native backend and use EAO's existing coding-agent delegation boundary when that boundary is explicitly enabled and authorized.

### Class D — Non-admissible Skill

Typical characteristics:

- duplicates an existing EAO/Hermes capability without material benefit;
- requests unrestricted terminal/filesystem/network/credential access not justified by the business requirement;
- attempts to bypass EAO approval or side-effect governance;
- contains unreviewed executable bootstrap/install behavior with unacceptable supply-chain risk;
- has incompatible licensing or unclear redistribution/use terms;
- depends on abandoned/unpinned infrastructure whose operational burden exceeds its value;
- cannot be meaningfully tested or rolled back.

Default treatment:

```text
REJECT
```

## 5. Compatibility is not permission

This is a hard security invariant:

```text
Skill procedure
≠ runtime authority
```

A Skill never grants tools, credentials, filesystem access, external write authority, coding-agent delegation, or provider permissions.

If a Skill requires a capability the target Profile does not already have, the result is not "enable the Skill and inherit the capability".

Instead:

```text
required capability absent
→ evaluate role/business need
→ explicit Profile/capability review
→ otherwise BLOCK / REJECT
```

Prompt text is not a security boundary.

## 6. Delegation is not a privilege-escalation tunnel

Codex/Claude Code delegation is governed by `../infrastructure/coding-agents/README.md`.

Installing a Skill into Codex or Claude Code does **not** make that Skill available to ordinary business Profiles through indirect execution.

Forbidden pattern:

```text
normal business Profile
→ Hermes lacks terminal/write privilege
→ ask Codex/Claude Code to perform the privileged operation instead
```

That is permission bypass, not Skill compatibility.

Delegated Skills may run only when all of the following are already true:

- coding delegation is enabled by company configuration;
- the calling Hermes Profile is explicitly authorized;
- the backend is explicitly enabled;
- workspace/repository scope is explicit;
- required credentials are scoped to that technical Profile/backend context;
- repository-local instructions are read;
- the requested action itself is within the role's authority;
- completion evidence is inspectable and testable.

Delegation changes the execution backend. It does not widen human or Profile authority.

## 7. Direct-use rules

A third-party Skill may be used directly from Hermes only when:

- its source and version/commit are identifiable;
- required files are available through an approved external Skill directory or other supported Hermes mechanism;
- its runtime dependencies are present and approved;
- every required tool is already permitted to the target Profile;
- it does not redefine company knowledge authority;
- it does not introduce hidden external side effects;
- its license/use terms are acceptable;
- a harmless acceptance test passes.

Prefer shared external Skill directories over copying the same Skill into multiple Profile homes.

Do not duplicate authoritative company facts into third-party Skill prose. Company facts remain in WeKnora or another explicitly approved source of truth.

## 8. Thin-adapter rules

Use an adapter only when the workflow is meaningfully portable and the compatibility gap is small.

A valid adapter should:

- preserve the upstream Skill as the primary source;
- document the exact incompatibility being bridged;
- map only the necessary runtime assumptions;
- fail explicitly when no safe equivalent exists;
- avoid granting new authority;
- be easy to remove when upstream compatibility improves;
- retain upstream provenance/version information.

An adapter should not become a silent fork.

If the adapter begins to reproduce another Agent's orchestration/session/plugin system, reclassify the Skill as Agent-native and use DELEGATE or REJECT.

## 9. Delegated-Skill rules

For Class C Skills:

```text
Hermes
→ authorized technical Profile
→ approved Codex/Claude Code backend
→ backend-native Skill
→ bounded workspace
→ inspectable result
```

The backend-native Skill remains subject to:

- EAO Profile/RBAC policy;
- coding-agent workspace policy;
- repository-local `AGENTS.md`, `CLAUDE.md`, contribution, and security rules;
- provider/account permissions;
- existing approval rules for external side effects;
- completion/verification requirements.

A backend exit code of zero is not sufficient acceptance.

## 10. Admission granularity and mixed-runtime Skills

Admission is performed at the **smallest meaningful executable/procedural unit**, normally an individual Skill or tightly coupled workflow.

Do not treat repository/plugin reputation as blanket approval:

```text
trusted repository
≠ every Skill approved
```

A single plugin bundle may legitimately contain:

- one Skill that is DIRECT;
- another that requires ADAPT;
- another that is backend-native and must DELEGATE;
- a global/process Skill that EAO should REJECT.

Repository/plugin provenance and license may be shared evidence, but the operational admission decision remains Skill/workflow-specific.

A mostly portable Skill may also contain an optional backend-native subflow. It may remain ADAPT rather than being forced into DELEGATE when a thin adapter can safely express:

```text
portable subflow → run through approved Hermes capability
backend-only subflow → explicit BLOCK or authorized delegation
```

The adapter must fail closed when the backend-only path is unavailable. It must not silently invoke a more privileged backend.

The first real classification evidence is recorded in [`THIRD-PARTY-SKILL-ADMISSION-PILOT.md`](THIRD-PARTY-SKILL-ADMISSION-PILOT.md). That report is evidence/example material; this document remains the normative policy.

## 11. Source, update, and supply-chain policy

For every admitted third-party Skill, record enough provenance to reproduce the decision:

- source repository;
- upstream owner;
- Skill path/name;
- reviewed version, tag, or commit where practical;
- license;
- selected compatibility class;
- admission decision;
- required runtime/backend;
- required tools/credentials/workspace;
- adapter location if any;
- acceptance evidence;
- reviewer/date.

Prefer pinned or reviewable upstream states for production use.

Do not silently auto-update a production Skill across major behavioral changes. Re-run admission review when an update changes:

- requested tools;
- external side effects;
- install/bootstrap scripts;
- credentials;
- network behavior;
- delegation behavior;
- write scope;
- licensing;
- core workflow semantics.

## 12. Minimal decision record

A material admission should record at least:

| Field | Required answer |
| --- | --- |
| Business requirement | What concrete work does this Skill improve? |
| Existing capability check | Why is current EAO/Hermes/approved Skill coverage insufficient? |
| Upstream source | Repository + Skill path + reviewed ref |
| Compatibility class | A / B / C / D |
| Decision | DIRECT / ADAPT / DELEGATE / REJECT |
| Agent-specific primitives | What, if any, are required? |
| Required EAO capabilities | Tools, MCP, workspace, credentials, backend |
| Authority change | Does admission require new Profile/human permissions? |
| Security/supply-chain impact | Executables, install scripts, network, secrets, side effects |
| Maintenance impact | Update/fork/adapter burden |
| License | Acceptable? attribution required? |
| Acceptance | Harmless observable test |
| Rollback | How to remove/disable safely |

If the compatibility class or required authority cannot be stated clearly, do not admit the Skill yet.

## 13. Acceptance expectations

### DIRECT

Verify at minimum:

- Skill is discovered/loaded through the supported Hermes mechanism;
- representative workflow completes;
- only already-approved target Profile tools are used;
- no unexpected external writes/network side effects occur;
- output is materially correct for the intended business use.

### ADAPT

Verify DIRECT requirements plus:

- each mapped primitive behaves as intended;
- unsupported upstream behavior fails explicitly;
- upstream Skill remains separable from the adapter;
- adapter removal/rollback is understood.

### DELEGATE

Verify at minimum:

- only the authorized technical Profile can invoke the backend;
- correct backend-native Skill is used;
- explicit workspace/repository is enforced operationally;
- repository-local instructions are honored;
- output/diff is inspectable;
- relevant tests/checks pass;
- no unauthorized host resource is intentionally granted;
- delegation does not provide a path from a normal business Profile to privileged execution.

## 14. Installation/ownership model

EAO should manage approved Skill sources, not create a Hermes-specific copy of every useful Skill.

Preferred conceptual layout:

```text
approved skill sources
├── portable        # usable directly where Profile capability permits
├── adapters        # EAO-owned thin compatibility layers
└── delegated       # provenance/policy for backend-native Skills
```

This is a logical ownership model, not a requirement to create a new service or database.

Use existing Hermes supported external Skill directories and existing Codex/Claude Code Skill mechanisms where applicable.

## 15. Rejected approaches

Do not adopt these as default architecture:

### Universal Skill converter

A converter can make syntax appear compatible while leaving runtime/security semantics incompatible.

```text
syntax converted
≠ runtime compatible
≠ permission compatible
```

Do not build a general Claude/Codex-to-Hermes conversion service without a demonstrated repeated requirement that thin adapters cannot solve.

### Fork every external Skill

Permanent forks create update drift and maintenance burden. Prefer upstream source + thin adapter.

### Delegate everything Hermes cannot run

This collapses Hermes into a routing shell and can bypass Profile privilege boundaries. Delegate only Agent-native workflows through the existing authorized coding-agent boundary.

### Install every useful-looking Skill

EAO is not a Skill collection. Admission follows concrete business value and least privilege.

## 16. Examples

### Research/writing Skill

If a Skill mainly defines research, evidence, outline, writing, and audit steps using ordinary retrieval/document capabilities, classify based on actual primitives rather than its README label.

Likely result:

```text
Class A
→ DIRECT
```

### Mostly portable Skill with Claude-specific tool wording

If the workflow is generic but says "use Claude Read tool" and "read CLAUDE.md", while Hermes has approved equivalents:

```text
Class B
→ ADAPT
```

Map the narrow assumptions; do not fork the whole Skill.

### Repository implementation Skill using Codex-native review/sandbox semantics

If the workflow materially depends on `codex exec`, `codex review`, sandbox/worktree behavior, or similar native primitives:

```text
Class C
→ DELEGATE
```

Only through an authorized technical Profile and approved workspace.

### Skill requesting unrestricted shell from Operations

If a normal business Profile has no terminal/coding delegation authority, a third-party Skill requiring unrestricted shell does not receive that authority by installation.

Likely result:

```text
BLOCK / REJECT for that Profile
```

A separate role/capability decision is required before any privileged execution path exists.

## 17. Relationship to historical ARMOR Skill migration

The `PHASE4*` and `PHASE5*` documents are historical migration/closure evidence.

This standard:

- does not reopen Legacy Hermes Skill migration;
- does not reactivate old Delegate Worker/Auditor Profiles;
- does not change the frozen status of previously closed migration work;
- governs **new third-party Skill intake from now on**.

Historical migration decisions remain evidence, not the default process for future external Skills.

## 18. Final principle

EAO's objective is not:

```text
Hermes must internally own every Skill.
```

The objective is:

```text
EAO can safely use the best available Skill
through the smallest compatible execution path
without weakening authority, reproducibility, or maintainability.
```

Hermes remains the primary Agent runtime and governance boundary. Portable work stays portable. Small gaps get thin adapters. Truly backend-native work stays with its native specialist backend. Skills that do not justify their risk or complexity are not admitted.
