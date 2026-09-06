# ARMOR Reference Implementation

ARMOR is the first real company used to validate Enterprise AI Office.

This directory separates reusable Enterprise AI Office architecture from ARMOR-specific organization, roles, paths, products, credentials, and operating decisions.

## Authority boundary

The generic deployment contract is defined by:

```text
AGENTS.md
DEPLOY.md
docs/COMPLETENESS.md
config/capabilities.yaml
current generic standards/adapters
```

ARMOR reference material is non-normative. It must not override the generic contract for another company or the active private configuration of an ARMOR deployment.

The older ARMOR v1 design document remains at the repository root for reference/backward-compatible linking:

- [`ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范.md`](../../ARMOR%20Enterprise%20AI%20Office%20v1%20%E2%80%94%20%E6%80%BB%E4%BD%93%E6%9E%B6%E6%9E%84%E3%80%81%E9%83%A8%E7%BD%B2%E8%93%9D%E5%9B%BE%E4%B8%8E%E9%95%BF%E6%9C%9F%E8%BF%90%E7%BB%B4%E8%A7%84%E8%8C%83.md)

Use it as historical/reference design material, not as the current deployment execution contract.

## ARMOR reference technology choices

The ARMOR reference architecture uses the same current core responsibilities as the generic v1 design:

```text
Knowledge: WeKnora
Agent runtime: Hermes Agent
Employee Web client: Open WebUI
Optional Hermes admin client: hermes-webui
Optional coding workers: Codex + Claude Code
Host target: company-managed machine
```

Which optional capabilities and specialist Profiles ARMOR actually enables must come from its current private deployment configuration and real operating needs.

## Profiles

ARMOR does not derive Profiles from a generic department checklist.

The ARMOR deployment starts from the same core Profile model:

```text
default/admin
general
```

Additional specialist Profiles are created only for real ARMOR work/capability boundaries selected in the active deployment configuration.

## What belongs in this reference implementation

Sanitized ARMOR-specific examples may include:

- Profile role definitions actually used by ARMOR;
- example SOUL/Skill patterns;
- Knowledge Base organization;
- RBAC mappings;
- deployment lessons;
- acceptance findings;
- operational problems discovered during real use.

## What must not be committed publicly

Do not commit:

- real API keys/passwords;
- bot/OAuth secrets;
- employee personal data;
- customer secrets;
- private contracts;
- unrestricted internal documents;
- sensitive production network details;
- production `.env` files.

## Feedback loop

```text
Generic architecture
→ ARMOR deployment
→ real employee usage
→ concrete problem
→ smallest justified refinement
→ reusable lesson back into generic project
```

Do not promote an ARMOR-specific workaround or organization choice into the generic architecture unless the underlying requirement is broadly reusable.
