# Hermes Profile Templates

This directory contains reusable starting points for Hermes Profiles.

These are templates, not immutable production prompts.

A company should adapt them to its actual organization while preserving the security and source-of-truth rules in:

- `docs/PROFILE-STANDARD.md`
- `docs/SECURITY.md`
- `docs/KNOWLEDGE.md`
- `docs/CLIENT-RBAC.md`

## Baseline employee template

```text
profiles/
└── general/SOUL.md
```

`general` is the baseline employee-facing Profile for company-wide assistance.
The privileged Hermes `default` / admin Profile belongs to the control plane and is not an employee template.

## Optional specialist templates

```text
profiles/
├── sales/SOUL.md
├── qc/SOUL.md
├── marketing/SOUL.md
└── engineering/SOUL.md
```

Specialist templates are a library. A deployment should instantiate only the Profiles justified by its real roles, workflows, knowledge boundaries, tool permissions, credentials, automation ownership, or risk boundaries.

## Template rules

1. A Profile represents an AI role, not an employee account.
2. Do not insert secrets into SOUL files.
3. Do not turn SOUL into a copy of the company knowledge base.
4. Company-specific facts should be retrieved from WeKnora.
5. Tool permissions must be enforced in Hermes configuration, not only described in SOUL.
6. Replace `<COMPANY_NAME>` and other placeholders before production.
7. Add specialist Profiles only when a real distinct role/capability/permission boundary exists.

## Applying a template

An implementation agent should:

1. select only the templates required by the company configuration;
2. copy/adapt the relevant SOUL template into the actual Hermes Profile home;
3. configure the Profile's model/provider;
4. configure Skills and external Skill directories;
5. configure WeKnora MCP/API access;
6. configure least-privilege tools;
7. configure unique API credentials;
8. start a fresh session;
9. run the relevant acceptance tests.

Do not assume copying `SOUL.md` alone creates a safe Profile.
