# Real Deployment Status — Sanitized Public Summary

> This file is a **sanitized public progress summary** for the explicitly authorized real company deployment. It is not the protected runtime state record and must never contain credentials, real employee identifiers, private network details, mailbox data, or secret values.

Last updated: 2026-09-08

## Deployment authorization

```text
Real deployment task: ACTIVE
Target: designated company Mac Studio (publicly sanitized)
Blueprint lifecycle: installation_design (unchanged)
Blueprint Validation: not opened
```

The real deployment is an independently authorized consumer activity. Its activation does **not** advance the repository blueprint lifecycle.

## Operator topology

```text
Operator Mac
  ↓
Codex macOS App
  ↓ SSH
Designated company Mac Studio
  ↓
Enterprise AI Office runtime
```

Deployment commands execute on the remote Mac Studio unless a task explicitly says otherwise. A local Codex/ChatGPT login on the Mac Studio is not required for the deployment path.

## Current deployment stage

Current focus:

```text
Core baseline installation / acceptance
```

Target core employee path:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes `general`
→ WeKnora
→ grounded company answer + source
```

Current public status:

| Area | Status |
| --- | --- |
| Remote host preflight | ✅ Complete |
| OrbStack / Docker | ✅ Running |
| WeKnora v0.8.0 | ✅ Running |
| Hermes v0.21.0 | ✅ Running |
| Hermes `general` | ✅ Configured |
| Hermes reasoning model | ✅ `gpt-5.6-luna` |
| Open WebUI v0.11.3 | ✅ Running |
| Open WebUI admin bootstrap | ✅ Complete |
| Signup | ✅ Disabled |
| Employee groups / baseline ACL | ✅ Reconciled |
| General Assistant | ✅ Configured |
| Synthetic acceptance employee | ✅ Created in protected runtime state |
| Employee model isolation | ✅ Baseline checks passed |
| WeKnora Owner/Admin bootstrap | ✅ Complete |
| Local Embedding qualification | ✅ `bge-m3` / 1024 dimensions passed |
| Formal `Company Knowledge` production indexing | ⏳ Waiting for final binding/provisioning |
| Grounded employee answer + source acceptance | ⏳ Pending final WeKnora provisioning |
| Core Ready | ⏳ Not yet declared |

Do not infer a higher readiness level from individual green components. Readiness remains evidence-based under [`docs/COMPLETENESS.md`](../docs/COMPLETENESS.md).

## Current model direction

Reasoning / answer generation:

```text
Hermes
→ gpt-5.6-luna
```

Validated local embedding for the current Mac Studio deployment:

```text
WeKnora v0.8.0
→ Ollama 0.30.8
→ bge-m3
→ 1024 dimensions
```

Small qualification result on 2026-09-08:

- 6 sanitized representative documents parsed successfully;
- 8 mixed Chinese / English / cross-language retrieval questions returned relevant source evidence;
- observed Ollama RSS was approximately 1.75 GB;
- available-memory ratio remained approximately 68–71% on the deployment host;
- WeKnora and Open WebUI health checks remained HTTP 200;
- no obvious system slowdown was observed;
- `qwen3-embedding:0.6b` was not tested because `bge-m3` already passed the intended minimal qualification.

The qualification used a temporary test Knowledge Base only. The formal `Company Knowledge` Knowledge Base has not yet been reindexed/bound to this model in the public status recorded here.

DashScope is not required for the selected local embedding path. Rerank remains disabled unless a real retrieval-quality need later justifies it.

## Capabilities intentionally disabled during Core deployment

The current Core baseline does not enable optional capabilities merely because repository playbooks exist.

Examples currently outside the active Core deployment scope include:

- Email / governed send;
- Messaging;
- Hermes Cron;
- Hermes Kanban;
- Coding delegation for employees;
- hermes-webui employee exposure;
- Remote access;
- SSO expansion;
- Employee Hermes long-term memory.

They may be enabled later only through explicit company configuration and their applicable acceptance contracts.

## Secrets and deployment truth

The public repository must not contain:

- passwords;
- API keys;
- OAuth tokens;
- bearer tokens;
- employee credentials;
- real employee identifiers;
- private host/network identifiers beyond intentionally sanitized descriptions;
- protected company configuration.

Actual deployment truth is:

```text
active private company configuration
+
protected deployment/runtime state
+
observed runtime behavior
```

This public file is only a sanitized progress summary.

## Reference demo vs current deployment

[`DEPLOYMENT-STATE.md`](./DEPLOYMENT-STATE.md) records the earlier **sanitized local reference/demo validation** performed before this company deployment. It is valuable reproducibility evidence, but it is **not** the current Mac Studio runtime state.

That reference record contains historical choices such as:

- MacBook demo host characteristics;
- `gpt-5.5`;
- DashScope embedding/chat models;
- `sales` / `qc` demo Profiles.

Do not copy those values into the current deployment unless the active company configuration explicitly selects them.

Fresh deployments should start from [`DEPLOYMENT-STATE.template.md`](./DEPLOYMENT-STATE.template.md) and keep the real operational copy in protected deployment storage when it contains company-private information.

## Next public milestone

The next meaningful deployment milestone is:

```text
CORE READY — PASS
```

It may be declared only after the employee-facing Open WebUI → Hermes `general` → WeKnora path returns a grounded answer with source evidence and the applicable Core acceptance checks pass.
