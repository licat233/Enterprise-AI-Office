# Validate Enterprise AI Office

> Fresh-Agent Validation entrypoint for Enterprise AI Office (EAO).
>
> This document defines how to test whether a capable AI engineering agent can understand and reproduce EAO from repository evidence alone, plus explicitly supplied private inputs when a real validation target is authorized.

## Lifecycle note

The lifecycle is currently:

```text
blueprint_lifecycle.current_phase = release_ready
blueprint_validation.status = opened
release_ready.status = opened
```

Blueprint Validation and Release Ready were explicitly opened by human direction. An opened phase is not the same as a PASS result or a final `RELEASE READY` declaration, and it does not authorize any new deployment target.

## What this validates

The validation problem has four separate layers:

1. **Repository integrity** — required contracts, adapters, scripts, and references exist.
2. **Agent comprehension** — a fresh Agent correctly identifies architecture, authorities, security boundaries, and capability state.
3. **Agent planning** — the Agent can produce an unambiguous reconstruction plan without inventing infrastructure or asking for inputs already defined by the repository.
4. **Runtime reproduction** — only on an explicitly authorized validation target, the Agent can install/configure the requested target state and produce acceptance evidence.

A PASS at one layer does not imply PASS at the next layer.

## Fresh-Agent rule

A valid Fresh-Agent test must not provide hidden project history.

The Agent receives only:

- the GitHub repository/ref;
- `validation/FRESH-AGENT-TASK.md`;
- the identity of the approved validation target, if runtime reproduction is authorized;
- genuine private inputs that the repository explicitly classifies as required for that authorized target.

Do not provide:

- previous ChatGPT/Codex conversation history;
- undocumented architecture explanations;
- private production state from ARMOR unless that exact state is part of the authorized test;
- hints that answer the comprehension questions.

## Required validation order

### Gate 0 — Public repository integrity

Run:

```sh
EAO_REPOSITORY_ONLY=1 sh scripts/repository-readiness-check.sh
python3 scripts/validate-fresh-agent-kit.py
sh scripts/check-yaml-syntax.sh
python3 scripts/check-repository-links.py
python3 scripts/check-declarative-paths.py
python3 scripts/check-capability-acceptance.py
python3 scripts/check-capability-selectors.py
python3 scripts/check-validated-stack-consistency.py
python3 scripts/check-public-repository-hygiene.py
python3 scripts/check-frozen-baselines.py
sh scripts/run-public-offline-tests.sh
```

Expected:

```text
PASS
```

Failure here is a **REPOSITORY_DEFECT**. Do not compensate by explaining missing information to the Agent.

### Gate 1 — Cold-start comprehension

Give the Agent only `validation/FRESH-AGENT-TASK.md` and the repository.

The Agent must answer the comprehension section before proposing installation steps.

Score using `validation/scorecard.yaml`.

Critical failures include:

- treating Open WebUI as the company knowledge authority;
- treating a Hermes Profile as an employee identity;
- treating provider credentials as human approval;
- enabling employee long-term Memory by default;
- introducing a second RAG/vector database, scheduler, workflow engine, IAM system, or employee portal without a proven gap;
- assuming historical migration documents are current runtime authority;
- claiming that `real_deployment_task.active: false` means no ARMOR reference deployment exists;
- assuming Open WebUI native Knowledge must contain Company Knowledge;
- exposing generic shell/browser/SMTP capabilities to ordinary employee Profiles.

Any critical failure means Gate 1 FAIL.

### Gate 2 — Reconstruction dry run

Without mutating a host, the Agent must produce:

- exact reading order and authority map;
- target readiness interpretation;
- required public inputs;
- required private inputs, by class only;
- component/version plan;
- WeKnora → Hermes → Open WebUI dependency order;
- Profile/Assistant/group mapping plan;
- capability closure table;
- security boundary plan;
- acceptance plan;
- restart plan, plus backup/restore plan only when backup is explicitly enabled;
- explicit blockers, if any.

The dry run must distinguish:

```text
REPOSITORY_DEFECT
MISSING_PRIVATE_INPUT
TARGET_ENVIRONMENT_BLOCKER
RUNTIME_FAILURE
POLICY_OR_AUTHORITY_BLOCKER
```

Do not accept vague statements such as "need more information" when the repository already defines the answer.

### Gate 3 — Authorized isolated reproduction

Blueprint Validation is already open. Run runtime reproduction only after an explicit validation target is identified and authorized.

The target should be isolated, synthetic, disposable, or otherwise explicitly designated for validation.

The Agent must follow `DEPLOY.md` and `docs/ACCEPTANCE-TESTS.md`.

At minimum, prove the Core path:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes general
→ WeKnora
→ grounded answer + source
```

If the validation configuration enables Operations, also prove:

```text
Operations Employee
→ Operations Assistant
→ Hermes /p/operations
→ operations-weknora
→ Company Knowledge
```

For every enabled optional capability, run its referenced acceptance contract.

### Gate 4 — Recovery and convergence

For the requested readiness level, verify applicable:

- controlled restart;
- host/runtime recovery boundary;
- observed recovery exercise appropriate to the requested readiness level; do not infer recovery PASS from restart configuration alone;
- any required operator/GUI-login boundary and whether unattended boot-to-service recovery was actually observed;
- configuration persistence;
- employee-visible behavior after restart;
- when backup is explicitly enabled: backup generation and isolated restore;
- when the selected backup policy requires off-primary independence: approved off-primary copy, post-transfer integrity/freshness evidence, and final isolated restore sourced from that independent copy;
- second-run/idempotent reconciliation;
- no privilege expansion after recovery.

### Gate 5 — Independent report

Produce a report using `validation/REPORT.template.md`.

A validation report must name:

- repository commit;
- validation target class;
- Agent/model identity when available;
- whether the Agent had prior project context;
- all requested private-input classes;
- achieved gates;
- failures and their taxonomy;
- repository defects discovered;
- manual hints given after the test began;
- final conclusion.

If material hints were required after Gate 1 began, record them. A test that succeeds only after undocumented human explanation is evidence of a repository gap.

## Pass criteria

The validation target is **Fresh-Agent Reproducible** only if:

- Gate 0 PASS;
- Gate 1 PASS with zero critical failures;
- Gate 2 PASS without undocumented architecture hints;
- Gate 3 PASS for the explicitly selected target scope;
- all enabled capabilities close through their acceptance paths;
- Gate 4 PASS for the requested readiness level;
- the final report contains enough evidence for another Agent to understand what was reproduced and from which commit.

## Release Ready rule

Do not mark EAO `release_ready` merely because this kit exists.

A Release Ready decision should require at least one completed Fresh-Agent Validation run against an explicitly approved target, followed by correction of material repository defects discovered during that run.

The Release Ready phase is already open. A final `RELEASE READY` declaration remains an evidence-based human decision governed by `state/PROJECT-PHASE.yaml`.
