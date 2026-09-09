# ARCHITECTURE.md as Entry Point

> For AI Agent Memory Architecture onboarding, start with `ARCHITECTURE.md` (481 lines), not the full spec files.

## The Entry Document

**URL:** https://github.com/licat233/AI-Agent-Memory-Architecture/blob/main/ARCHITECTURE.md

**What it covers in 481 lines:**
1. What the project is (and isn't)
2. Why it exists
3. Two architecture branches (ARMOR Enterprise V7.2 / PAMA Personal V5.3)
4. Universal principles (7 core principles)
5. Shared governance pattern (layer types across ARMOR and PAMA)
6. ARMOR Enterprise at a glance (vault structure, permission classes, core documents)
7. PAMA Personal at a glance (vault structure, governance priority, write discipline)
8. Runtime model (allowed/forbidden operations)
9. Default retrieval rules (ARMOR and PAMA)
10. Write routing (Remember / Fix / Discussion flows)
11. Promotion pipeline
12. Multi-agent shared vault rules
13. Installation mental model
14. Update mental model
15. Common retired active files
16. Which file should an agent read next (routing table)
17. Final operating summary

## When to Read What

| Need | Read | Lines |
|---|---|---|
| Quick orientation / "understand the architecture" | `ARCHITECTURE.md` | 481 |
| Enterprise vault details (folder structure, permission model, retrieval, lifecycle, schemas, templates, dashboards, automation) | `enterprise/V7_2_Stable.md` | 4183 |
| Enterprise governance quality gates (confidence, fact creation, frontmatter) | `enterprise/V7_1_5_Governance_Patch.md` | 508 |
| Enterprise router protocols (prompt intake, memory write, root-cause fix, runtime memory) | `enterprise/Prompt_Intake_Router.md` etc. | ~900 total |
| Enterprise multi-agent governance | `enterprise/multi_agent_shared_vault_governance.md` | 347 |
| Enterprise runtime adaptation guide | `enterprise/agent_runtime_adaptation_guide.md` | 319 |
| Personal vault details | `personal/PAMA V5.3 Stable.md` | ~900 |
| Installation procedure | `AGENT_INSTALL.md` | — |
| Update procedure | `AGENT_UPDATE.md` | — |

## Lesson (2026-06-12)

Hermes read `V7_2_Stable.md` (4183 lines) + `V7_1_5_Governance_Patch.md` (508 lines) + 4 router/protocol files (~900 lines) + `agent_runtime_adaptation_guide.md` (319 lines) + `multi_agent_shared_vault_governance.md` (347 lines) = ~6,257 lines total.

User correction: "只需读取 ARCHITECTURE.md 这个文档就能理解这个记忆架构了" — only 481 lines, covering the same conceptual ground.

**Token cost ratio:** ~13:1 (6,257 vs 481 lines for the same orientation-level understanding).

**Rule:** Start with `ARCHITECTURE.md`. Only deep-dive into spec files when the entry document doesn't answer the specific question.

## Vault Summary

After reading all the spec files, a comprehensive Chinese-language summary may
be saved under `${ARMOR_VAULT_ROOT}/03-Insights/ARMOR/` in the protected Vault.

This summary covers all 54 sections of V7.2 Stable + V7.1.5 Governance Patch + all 4 routers/protocols + runtime adaptation + multi-agent governance in ~800 lines. Use this for restoring context in future sessions without re-reading source specs.
