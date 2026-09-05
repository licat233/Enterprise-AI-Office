# Hermes Profile Standard

This document defines how Enterprise AI Office should design and maintain Hermes Profiles.

A Profile is an AI role or specialist. It is not a human user account and it is not, by itself, a security sandbox.

## 1. When to create a Profile

Create a Profile when at least one of the following is true:

- a distinct business role exists;
- a distinct SOUL / behavioral contract is required;
- a distinct tool or credential boundary is required;
- a distinct persistent specialist memory is useful;
- a distinct model/provider policy is useful;
- a distinct Cron or automation owner is required;
- a distinct Kanban worker identity is required.

Do not create a Profile merely because another employee exists.

## 2. Reference Profile set

A common starting set may be:

```text
default      # privileged admin / orchestrator
general      # broad employee assistant
sales        # sales specialist
qc           # quality specialist
marketing    # marketing specialist
engineering  # restricted technical specialist
```

These names are examples. Adopting companies should model real roles.

## 3. Profile contract

Every production Profile must document:

- canonical name;
- display name;
- business purpose;
- intended human groups;
- SOUL file;
- model/provider;
- allowed Skills;
- allowed toolsets/tools;
- MCP servers;
- credentials it may use;
- Knowledge Bases it may query;
- terminal/workspace policy;
- memory policy;
- Cron policy;
- Kanban role;
- escalation rules;
- prohibited actions.

## 4. SOUL standard

Every `SOUL.md` should contain these sections or equivalent content:

```text
Role
Purpose
Primary Responsibilities
Operating Principles
Knowledge Policy
Tool Policy
Decision Boundary
Escalation Rules
Confidentiality
Memory Policy
Output Standards
Forbidden Actions
```

The SOUL should describe how the agent works, not serve as a product/specification database.

## 5. Knowledge policy

For company-specific facts, Profiles should prefer WeKnora or another approved authoritative company knowledge source.

A SOUL should instruct the agent to:

- use company sources for company facts;
- preserve exact model names, units, dimensions, dates, certifications, and other technical values;
- avoid inventing unsupported company facts;
- expose source conflict;
- say when evidence is insufficient.

Do not duplicate a large set of company facts into SOUL.

## 6. Shared Skills vs role Skills

Use shared external Skill directories for common company workflows.

Example:

```text
company-skills/
├── shared/
│   ├── company-knowledge/
│   ├── document-quality/
│   └── company-security/
├── sales/
├── qc/
├── marketing/
└── engineering/
```

A Profile should load:

```text
shared Skills
+
role-specific Skills
```

Avoid copying the same Skill into many Profile homes, which causes drift and duplicate maintenance.

## 7. Skill ownership

Company-owned reusable Skills should be version-controlled outside runtime Profile memory/state where practical.

External Skill directories are preferred for shared company Skills because they make ownership explicit and reduce accidental autonomous modification.

## 8. Tool policy

Tool access must follow least privilege.

### General

Typical capabilities:

- company knowledge;
- approved Web/search if needed;
- basic document reasoning.

Typical denials:

- terminal;
- unrestricted filesystem;
- Docker;
- coding agents;
- system configuration.

### Sales

Typical capabilities:

- company/product knowledge;
- sales Skills;
- approved Web search;
- approved CRM/email tools when later integrated.

Typical denials:

- terminal;
- code execution;
- Codex/Claude Code;
- host administration;
- unrelated finance/QC credentials.

### QC

Typical capabilities:

- product specifications;
- standards/certificates;
- document/spreadsheet analysis;
- approved quality-system tools.

Typical denials:

- social publishing;
- coding agents;
- infrastructure admin;
- unrelated sales credentials.

### Marketing

Typical capabilities:

- company knowledge;
- market research;
- writing/content Skills;
- approved browser/search/social tooling.

Typical denials:

- infrastructure admin;
- unrestricted terminal;
- engineering credentials.

### Engineering

May include:

- terminal;
- files;
- Git;
- GitHub;
- Codex;
- Claude Code;
- project MCPs.

Engineering remains restricted and must operate inside an explicit workspace/repository policy.

## 9. Credentials

Credentials should be scoped to the Profile's responsibilities.

Do not copy all enterprise credentials into every Profile.

Examples:

```text
sales → sales/CRM credentials
marketing → approved marketing integrations
engineering → GitHub/engineering credentials
```

Be aware that host-native CLI credentials may come from the OS user's HOME and may therefore be shared across terminal-capable Profiles unless stronger isolation is configured.

## 10. Memory policy

Classify Profile memory as one of:

### Shared role memory

Safe department-level operating experience intentionally shared by users of the Profile.

### User-scoped memory

Private/personal continuity for one human user, allowed only when technical isolation is proven.

### Prohibited shared-memory content

Do not intentionally store in shared Profile memory:

- private employee data;
- one employee's confidential notes;
- private customer correspondence not meant for the department;
- secrets/passwords/tokens;
- authoritative company facts that belong in WeKnora.

## 11. Long-term memory rollout

Do not enable employee long-term memory merely because Hermes supports memory.

First run the two-user isolation test.

If isolation fails, disable user-scoped long-term memory and retain only safe shared role memory plus client conversation history.

## 12. Terminal policy

A Profile with terminal access must define:

- backend;
- starting working directory;
- allowed workspace/repository;
- credential expectations;
- whether Profile-specific HOME isolation is required;
- whether Docker/sandbox backend is more appropriate.

Do not treat `terminal.cwd` alone as a complete sandbox.

## 13. Profile lifecycle

### Create

Create fresh where practical. Avoid cloning historical memory into a new business role unless explicitly intended.

### Modify

After changing SOUL, tools, MCP, model, or Skills:

- start a fresh session for behavior validation;
- run role-specific acceptance tests;
- update documentation if the role contract changed.

### Rename

Treat Profile names as technical identifiers referenced by API routes, routing rules, Cron/Kanban, and clients. Renaming can be a breaking change.

### Delete

Profile deletion is destructive. Back up and confirm no active client/routing/Cron/Kanban dependencies remain.

## 14. Default/admin Profile

The default/admin Profile may be privileged and should be treated as part of the control plane.

Do not expose it in the employee Web portal.

If a company wants a general employee assistant, create a separate `general` Profile instead of reusing the privileged default Profile.

## 15. Profile routing

A client or messaging route should resolve deterministically to a Profile.

Do not rely on the model to infer its own privilege level or switch identities from natural-language instructions.

## 16. Profile API isolation

Every employee-facing Profile should use its own supported API credential.

Cross-Profile credential tests are mandatory before production.

## 17. Cron ownership

Cron jobs belong to a Profile and should be treated as role/system automation.

Normal employees should not automatically be able to mutate all department routines.

## 18. Kanban worker descriptions

When Profiles participate as Kanban workers, give them clear role descriptions so orchestration can route tasks appropriately.

Example:

```text
researcher: gathers external sources and writes evidence-backed findings
engineering: implements and tests repository changes
reviewer: audits results and requests changes
```

## 19. Profile review checklist

Before exposing a new Profile to employees:

```text
[ ] Role is necessary and distinct
[ ] SOUL exists
[ ] Knowledge policy defined
[ ] Tool list reviewed
[ ] Dangerous tools denied by default
[ ] Credentials scoped
[ ] MCP list reviewed
[ ] Memory policy defined
[ ] API credential unique
[ ] Client group mapping configured
[ ] Unauthorized access test passes
[ ] Role-specific functional tests pass
```

## 20. Anti-patterns

Avoid:

- one Profile per employee without a real role reason;
- every Profile receiving every Skill;
- every Profile receiving all tools;
- product specifications duplicated into memory/SOUL;
- shared admin credentials in business Profiles;
- exposing default/admin as the company general assistant;
- using prompt wording as the only security boundary;
- cloning memory blindly between department Profiles.
