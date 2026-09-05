# Company Skills Architecture

This directory contains reusable company-owned Hermes Skill templates.

The project should prefer upstream/bundled Hermes Skills when they already solve a task. Company Skills should encode company-specific workflows, policies, integrations, or reusable operating procedures that are not already provided upstream.

## Design model

```text
company Skills
├── shared/
│   ├── company-knowledge/
│   └── enterprise-security/
├── sales/
├── qc/
├── marketing/
└── engineering/
```

The folders may evolve as real workflows appear.

## Shared Skills

Shared Skills are capabilities useful across multiple Profiles.

Examples:

- how to retrieve company knowledge safely;
- company document/output standards;
- enterprise security/authorization reminders;
- common office workflow conventions.

## Role Skills

Role-specific Skills should represent real repeatable work, for example:

```text
sales/customer-reply
sales/product-recommendation
qc/inspection-report
marketing/social-copy
marketing/content-audit
```

Do not pre-create dozens of placeholder Skills merely to fill a catalog.

## Skill rules

1. Prefer existing Hermes/upstream Skills first.
2. A Skill should solve a repeatable workflow, not merely contain a vague persona.
3. Keep authoritative company facts in WeKnora, not copied into Skills unless the fact is part of the workflow contract itself.
4. Do not store secrets inside `SKILL.md`.
5. Declare prerequisites clearly.
6. Document verification steps.
7. Review scripts/network/filesystem behavior before production.
8. Use external Skill directories so shared company Skills do not need to be copied into every Profile.
9. Version-control company-owned Skills.
10. Avoid shadowing an upstream Skill name unless intentional and reviewed.

## Installation pattern

A company-private deployment may clone this repository or a dedicated company Skills repository to a stable local directory, then configure Profiles to scan the required external directories.

Conceptually:

```text
general → shared
sales → shared + sales
qc → shared + qc
marketing → shared + marketing
engineering → shared + engineering
```

Exact Hermes configuration keys must match the installed upstream version.

## Security

A Skill can influence tool use and may ship scripts. Treat third-party Skills as software dependencies.

Before installing/using an external Skill:

- verify source;
- review license;
- inspect `SKILL.md`;
- inspect scripts/templates/references;
- inspect required environment variables;
- inspect external network calls;
- inspect filesystem/terminal requirements;
- confirm it fits the Profile's least-privilege boundary.

## What not to build here

Do not recreate:

- Codex itself;
- Claude Code itself;
- WeKnora retrieval engine;
- Hermes built-in Kanban/Cron;
- existing mature upstream Skills without a company-specific reason.
