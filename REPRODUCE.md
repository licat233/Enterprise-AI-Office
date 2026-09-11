# Reproduce Enterprise AI Office

> Fresh-agent reconstruction contract for Enterprise AI Office (EAO).
>
> Audience: a capable AI engineering agent that has **no prior chat history** and must understand, install, validate, and operate EAO from repository evidence plus explicitly supplied private deployment inputs.

## 1. Success criterion

A reconstruction is successful only when a fresh agent can answer and execute all of the following from this repository:

1. What EAO is and which component owns each responsibility.
2. Which capabilities are frozen, optional, deferred, or prohibited.
3. Which upstream projects and validated versions are used.
4. Which public configuration is required and which private values must be supplied out-of-band.
5. How to install the stack in dependency order.
6. How Open WebUI users/groups map to employee-facing Assistants and Hermes Profiles.
7. How Hermes reaches WeKnora and other approved MCP/tool capabilities.
8. How company knowledge, durable business authority, Agent memory, and operational state differ.
9. How to validate security, RBAC, knowledge retrieval, Skills, web research, email governance, backup, restore, and restart persistence.
10. How to detect when the runtime differs from the repository contract.

Do not declare success because containers start or one chat response works. EAO is a governed system; successful reproduction includes authority boundaries and acceptance evidence.

## 2. Read this repository in this order

A fresh agent MUST read these files before changing architecture or deploying:

1. `AGENTS.md` — repository-local agent operating contract.
2. `state/PROJECT-PHASE.yaml` — lifecycle and real-deployment gate.
3. `config/eao-manifest.yaml` — machine-readable project map and reconstruction sequence.
4. `config/validated-stack.yaml` — validated upstream versions.
5. `config/capabilities.yaml` — capability registry and closure.
6. `DEPLOY.md` — Golden Path installation contract.
7. `docs/ARCHITECTURE.md` — component responsibilities and boundaries.
8. `docs/SECURITY.md` — security model and least-privilege rules.
9. `docs/CLIENT-RBAC.md` and `docs/EAO-RBAC-BASELINE.md` — employee/client permission model.
10. `docs/KNOWLEDGE.md` — WeKnora authority and retrieval model.
11. `docs/PROFILE-STANDARD.md` — Hermes Profile conventions.
12. `docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md` — frozen Operations capability baseline.
13. `docs/ENTERPRISE-WEB-RESEARCH-V1.md` — approved research capability.
14. `docs/ENTERPRISE-EMAIL-OPERATIONS-V1.md` — email Operations boundary.
15. `docs/BACKUP-RESTORE.md` and `docs/OPERATIONS.md` — runbook and recovery.
16. `docs/ACCEPTANCE-TESTS.md` — final acceptance contract.
17. `state/DEPLOYMENT-STATE.md` — sanitized current reference-deployment state when operating the reference installation.
18. `state/CHANGELOG.md` — deployment change history.

Historical migration and design documents are evidence, not the first installation instructions. Prefer the current normative files above.

## 3. Frozen responsibility map

| Responsibility | EAO authority / component |
| --- | --- |
| Employee web client and human login | Open WebUI |
| Human-facing Assistant visibility / resource ACL | Open WebUI |
| Agent runtime, Profiles, Skills, Cron, Kanban, Gateway | Hermes Agent |
| Shared company knowledge | WeKnora |
| Knowledge retrieval boundary | WeKnora MCP/API through approved Hermes configuration |
| Durable ARMOR business rules / working authority | ARMOR Vault Router contracts where explicitly enabled |
| Employee long-term Agent memory | Disabled in the frozen employee baseline |
| Web research | Enterprise Web Research capability through approved Hermes Operations path |
| Email read / draft / approval / send governance | EAO email governance + narrow provider adapters |
| Media transcription | Host-native validated media-transcription capability |
| Backup / restore | Repository scripts and documented component-specific procedures |
| Remote administrative access | Existing approved network access layer; do not invent another remote-access stack |

Never silently substitute a second RAG system, workflow engine, scheduler, portal, IAM system, vector database, Agent framework, or observability stack for responsibilities already owned above.

## 4. Capability Reuse Pass — mandatory before adding anything

Before proposing or installing a new component, Skill, MCP server, scheduler, database, browser, workflow engine, memory layer, or external service, perform the Capability Reuse Pass in `docs/CAPABILITY-REUSE-PASS.md`.

Minimum search order:

1. Existing EAO capability and scripts.
2. Hermes native capability.
3. Installed/frozen Hermes Skills.
4. Existing Open WebUI capability.
5. Existing WeKnora capability.
6. Existing email/governance capability.
7. Official upstream capability or supported integration.
8. Thin adapter only if the above cannot satisfy the requirement.
9. New infrastructure only with an explicit gap, benefit, risk, maintenance, and rollback justification.

A statement such as “EAO cannot do X” is invalid until this pass has been completed with repository/runtime evidence.

## 5. Reference stack

The reproducibility baseline is pinned in `config/validated-stack.yaml`. At the current frozen baseline the core stack is:

- macOS arm64 reference host;
- OrbStack/Docker-compatible container runtime;
- WeKnora `v0.8.0`;
- Hermes Agent `0.21.0`, host-native;
- Open WebUI `v0.11.3`;
- MCP as the preferred narrow integration boundary.

Do not silently upgrade while reproducing the baseline. Upgrade qualification is a separate task governed by `docs/UPGRADE.md`.

## 6. Public vs private inputs

This repository MUST remain sufficient to explain structure and installation without containing secrets.

Public repository inputs include:

- component versions and deployment shapes;
- example environment/configuration schemas;
- capability registry;
- profile conventions;
- RBAC contracts;
- Skill source and migration records;
- install/validation scripts;
- sanitized reference-deployment evidence.

Private deployment inputs include, as applicable:

- model/API credentials;
- WeKnora service credentials;
- real company knowledge content;
- employee identities;
- mailbox credentials;
- Tailscale/device identity material;
- provider tokens and other protected secrets.

Use `config/.env.example`, `config/company.example.yaml`, and `config/company.private.example.yaml` as shape contracts. Never replace secret references in Git with real values.

## 7. Reconstruction sequence

### Stage A — repository and host preflight

1. Clone the repository at the approved branch/tag/commit.
2. Read the mandatory files in section 2.
3. Confirm target OS/architecture and available container/runtime prerequisites.
4. Confirm that no real deployment is inferred unless the human explicitly names the target and authorizes it.
5. Resolve public company configuration and required private inputs.
6. Run repository readiness checks before installation.

### Stage B — WeKnora

1. Install the validated upstream WeKnora baseline using the repository deployment contract.
2. Create/configure the approved company Knowledge Base(s).
3. Provision the least-privilege retrieval credential used by Hermes.
4. Verify listing/search/retrieval before connecting employee Assistants.
5. Keep Open WebUI native Knowledge empty when the selected architecture routes company knowledge through Hermes → WeKnora. `Open WebUI Knowledge records = 0` can be intentional.

### Stage C — Hermes Agent

1. Install the validated host-native Hermes version.
2. Create/control the privileged/default profile.
3. Configure the `general` employee profile.
4. Configure specialist profiles only when an explicit capability boundary requires them.
5. Install repository-approved shared department Skills.
6. Configure profile-local MCP names so shared-gateway registrations do not collide.
7. Keep employee/Profile memory disabled unless a later approved baseline explicitly changes it.
8. Enable only the narrow tools required by the profile; generic shell/filesystem/browser/code execution must not be exposed merely for convenience.

### Stage D — Open WebUI

1. Deploy the validated Open WebUI container configuration.
2. Preserve persistent data volumes.
3. Create employee groups and Assistant/model resources.
4. Apply default employee permission restrictions.
5. Grant resource READ ACLs rather than workspace management rights.
6. Route each Assistant to the correct Hermes profile/API path.
7. Validate login, chat history, file upload, reload persistence, and unauthenticated denial.

Frozen reference pattern:

```text
All Employees
  -> General Assistant READ

Operations Employees
  -> Operations Assistant READ
```

Employee groups do not receive Open WebUI workspace-management grants.

### Stage E — company knowledge path

Validate the entire path, not only direct WeKnora access:

```text
Employee
-> Open WebUI Assistant
-> Hermes profile
-> profile-local WeKnora MCP namespace
-> Company Knowledge
-> grounded answer with source evidence
```

For Operations on the reference baseline:

```text
Operations Assistant
-> Hermes /p/operations
-> Operations profile
-> operations-weknora
-> Company Knowledge
```

### Stage F — Operations Skills

Install only the accepted/frozen Skills and preserve their authority boundaries. The current ARMOR Operations capability baseline includes canonical entry points for:

- website article production;
- website product materials;
- social-media content, including video rules;
- MIC product optimization;
- product-visual preparation;
- AI-writing audit and supporting approved department Skills.

Use the acceptance/migration documents under `docs/PHASE4*`, `docs/PHASE5*`, and `docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md` for exact disposition and evidence. Do not re-enable triaged legacy Skills merely because files exist in historical inventories.

### Stage G — Enterprise Web Research

Use the already-approved Enterprise Web Research capability before adding another browser/search stack. Validate the adapter and its accepted runtime path using `docs/ENTERPRISE-WEB-RESEARCH-V1.md` and repository checks.

### Stage H — Media transcription

Use `infrastructure/media-transcription/` and `scripts/transcribe` for the validated host-native transcription capability. Do not introduce a separate transcription service unless the approved capability is proven insufficient.

### Stage I — Email Operations

Email is a governed side-effect capability and must remain narrower than generic IMAP/SMTP access.

Reproduce the repository-defined flow:

```text
read/search
-> draft
-> exact human review
-> deterministic approval
-> governed send
-> provider result
-> reconciliation if ambiguous
```

Use the governance SQLite schema/runtime and provider adapters under `infrastructure/email/`. Do not expose unrestricted send credentials to employee-facing Agents.

### Stage J — network access

The employee web surface may be published to the approved LAN interface and/or accessed through the already-approved private network layer. Do not create a new VPN/reverse-proxy architecture without a demonstrated need.

### Stage K — acceptance and freeze

Run:

- repository readiness checks;
- component health checks;
- direct and employee-path knowledge tests;
- Open WebUI RBAC tests;
- Hermes Skill/runtime checks;
- Enterprise Web Research checks;
- email-governance tests when enabled;
- media-transcription smoke tests when enabled;
- restart persistence tests;
- backup + isolated restore tests;
- unauthenticated-access denial checks.

Record the resulting sanitized state and exact baseline commit. A deployment is not frozen until its acceptance record can be traced to repository evidence.

## 8. Reference implementation facts that matter to reproduction

The ARMOR reference deployment proved several non-obvious requirements:

- Open WebUI is an employee client, not the company-knowledge authority.
- Company Knowledge can intentionally be reached only through Hermes → WeKnora.
- A shared Hermes gateway may host multiple profiles; a secondary profile must not bind a conflicting API port.
- Profile-local MCP naming may need to differ (`operations-weknora`) to avoid same-process registration collisions while still addressing the same WeKnora service.
- Open WebUI resource ACLs and feature permissions are separate concerns; employee groups can have empty workspace permission objects while receiving explicit model READ ACLs.
- Tailscale/private-network access can coexist with LAN publication; it is not a reason to expose internal admin services publicly.
- Runtime acceptance must verify employee-visible behavior after restart, not just configuration files before restart.

These are architecture lessons, not hard-coded hostnames, IP addresses, credentials, or company secrets.

## 9. Anti-patterns that invalidate a reproduction

A fresh agent must stop and correct the design if it does any of the following without explicit approval:

- invents a replacement architecture instead of using WeKnora + Hermes + Open WebUI;
- stores real secrets in Git;
- duplicates company knowledge in Agent memory;
- attaches company knowledge to an unintended Open WebUI native Knowledge workspace merely because the UI supports it;
- gives employees Workspace/Admin permissions to make setup easier;
- exposes generic shell, filesystem, browser, code execution, or SMTP tools to ordinary employee profiles;
- introduces n8n or another scheduler when Hermes Cron/Kanban already covers the use case;
- creates one Hermes Profile per employee by default;
- uses a provider credential as proof of human approval;
- automatically retries an email whose external send outcome is unknown;
- treats historical migration files as current runtime authority;
- claims a deployment is reproduced without running the acceptance contract.

## 10. Definition of “another AI Agent can rebuild EAO”

The repository satisfies the goal only when a fresh agent can, without hidden chat context:

- discover the current architecture and component versions;
- distinguish normative contracts from history/evidence;
- obtain only the missing private inputs from a human;
- install each component in dependency order;
- create the correct profiles/groups/ACLs;
- install approved Skills and MCP routes;
- connect WeKnora without duplicating authority;
- reproduce optional approved capabilities;
- run acceptance tests and identify failures;
- recover/restore the system;
- explain exactly which repository commit the deployed state implements.

When in doubt, prefer repository evidence over remembered conversations and prefer the existing EAO/Hermes/upstream capability over new infrastructure.
