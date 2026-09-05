# Hermes Profile Templates

This directory contains reusable starting points for department/specialist Hermes Profiles.

These are templates, not immutable production prompts.

A company should adapt them to its actual organization while preserving the security and source-of-truth rules in:

- `docs/PROFILE-STANDARD.md`
- `docs/SECURITY.md`
- `docs/KNOWLEDGE.md`
- `docs/CLIENT-RBAC.md`

## Included templates

```text
profiles/
├── general/SOUL.md
├── sales/SOUL.md
├── qc/SOUL.md
├── marketing/SOUL.md
└── engineering/SOUL.md
```

## Template rules

1. A Profile represents an AI role, not an employee account.
2. Do not insert secrets into SOUL files.
3. Do not turn SOUL into a copy of the company knowledge base.
4. Company-specific facts should be retrieved from WeKnora.
5. Tool permissions must be enforced in Hermes configuration, not only described in SOUL.
6. Replace `<COMPANY_NAME>` and other placeholders before production.
7. Remove a Profile entirely if the adopting company does not need that role.
8. Add new Profiles only when a real distinct role/capability/permission boundary exists.

## Applying a template

An implementation agent should:

1. copy/adapt the relevant SOUL template into the actual Hermes Profile home;
2. configure the Profile's model/provider;
3. configure Skills and external Skill directories;
4. configure WeKnora MCP/API access;
5. configure least-privilege tools;
6. configure unique API credentials;
7. start a fresh session;
8. run the relevant acceptance tests.

Do not assume copying `SOUL.md` alone creates a safe Profile.
