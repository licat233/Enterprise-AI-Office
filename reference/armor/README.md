# ARMOR Reference Implementation

ARMOR is the first real company used to validate Enterprise AI Office.

This directory exists to separate:

```text
Reusable Enterprise AI Office architecture
```

from:

```text
ARMOR-specific organization, roles, paths, products, credentials, and operating decisions
```

## Current reference design

The original ARMOR v1 design document currently remains at the repository root for backward-compatible linking:

- [`ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范.md`](../../ARMOR%20Enterprise%20AI%20Office%20v1%20%E2%80%94%20%E6%80%BB%E4%BD%93%E6%9E%B6%E6%9E%84%E3%80%81%E9%83%A8%E7%BD%B2%E8%93%9D%E5%9B%BE%E4%B8%8E%E9%95%BF%E6%9C%9F%E8%BF%90%E7%BB%B4%E8%A7%84%E8%8C%83.md)

It is a concrete reference implementation, not the generic contract for every adopter.

## ARMOR reference technology choices

The first ARMOR implementation is expected to use:

```text
Knowledge: WeKnora
Agent runtime: Hermes Agent
Employee Web client: Open WebUI
Hermes admin client: hermes-webui
Coding workers: Codex + Claude Code
Host target: company Mac Studio
```

These choices also define the current generic v1 reference architecture, but company-specific configuration must remain separate.

## Example ARMOR Profiles

ARMOR's initial Profile model includes concepts such as:

```text
general
sales
qc
marketing
engineering
```

These reflect ARMOR's organizational needs. Another company may use different roles such as Support, Legal, Finance, Research, Procurement, or Operations.

## What belongs in this reference implementation

Sanitized ARMOR-specific examples may include:

- Profile role definitions;
- example SOUL patterns;
- example department Skill layouts;
- Knowledge Base organization;
- RBAC mapping examples;
- deployment lessons;
- acceptance-test findings;
- operational problems discovered during real use.

## What must not be committed publicly

Do not commit:

- real API keys;
- production passwords;
- bot tokens;
- employee personal data;
- customer secrets;
- private contracts;
- unrestricted internal documents;
- private IP/network details that create security risk;
- production `.env` files.

## Feedback loop

ARMOR exists as the first validation environment so that real operational findings can improve the generic project.

The intended loop is:

```text
Generic architecture
→ ARMOR deployment
→ real employee usage
→ concrete problem
→ fix / refinement
→ feed reusable lesson back into generic docs/templates
```

Do not push an ARMOR-specific workaround into the generic architecture unless the underlying problem is broadly applicable.
