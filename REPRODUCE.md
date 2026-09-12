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
4. `VALIDATE.md` — Fresh-Agent validation contract and lifecycle-safe validation gates.
5. `config/validated-stack.yaml` — validated upstream versions.
6. `config/capabilities.yaml` — capability registry and closure.
7. `DEPLOY.md` — Golden Path installation contract.
8. `docs/ARCHITECTURE.md` — component responsibilities and boundaries.
9. `docs/SECURITY.md` — security model and least-privilege rules.
10. `docs/CLIENT-RBAC.md` and `docs/EAO-RBAC-BASELINE.md` — employee/client permission model.
11. `docs/KNOWLEDGE.md` — WeKnora authority and retrieval model.
12. `docs/PROFILE-STANDARD.md` — Hermes Profile conventions.
13. `docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md` — frozen Operations capability baseline.
14. `docs/ENTERPRISE-WEB-RESEARCH-V1.md` — approved research capability.
15. `docs/ENTERPRISE-EMAIL-OPERATIONS-V1.md` — email Operations boundary.
16. `docs/BACKUP-RESTORE.md` and `docs/OPERATIONS.md` — runbook and recovery.
17. `docs/ACCEPTANCE-TESTS.md` — final acceptance contract.
18. `state/DEPLOYMENT-STATE.template.md` — protected operational state/handoff template for a real or validation deployment.
19. `state/REAL-DEPLOYMENT-STATUS.md` — sanitized current ARMOR reference-deployment status.
20. `state/DEPLOYMENT-STATE.md` — historical local/demo validation evidence, not current ARMOR runtime truth.
21. `state/CHANGELOG.md` — deployment change history.

Historical migration and design documents are evidence, not the first installation instructions. Prefer the current normative files above.

## 2.1 Pin the repository revision

The EAO repository itself is part of the deployment contract.

Before runtime mutation:

```sh
git rev-parse HEAD
git status --porcelain --untracked-files=no
```

Require a commit-addressable revision and a clean tracked worktree. Record that
exact EAO commit in the protected operational deployment state.

Do not let a moving `main` branch silently change the blueprint midway through
the same reproduction. An explicitly authorized repository revision change is a
rebaseline and requires recording the new commit plus rerunning affected
acceptance.

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

Resolve the Core network desired state before provisioning:

```text
core_network.weknora.api_base_url_for_hermes
core_network.hermes.shared_listener.bind_host
core_network.hermes.shared_listener.port
core_network.hermes.open_webui_backend_base_url
core_network.open_webui.employee_url
core_network.open_webui.access_layer
```

Do not substitute ARMOR reference addresses when these values are unresolved.

### Stage B — WeKnora

1. Install the validated upstream WeKnora baseline through `DEPLOY.md §4.1` and prove runtime identity through §4.2.
2. Reconcile tenant/owner bootstrap, embedding model, company Knowledge Base(s), retrieval credentials, and official MCP bridge through `infrastructure/weknora/PROVISIONING.md`.
3. Record the resulting non-secret logical-ID → runtime-ID mappings and retrieval-key record metadata in the protected operational state created from `state/DEPLOYMENT-STATE.template.md`.
4. Verify direct listing/search/retrieval, source evidence, credential denial, and cross-KB scoping before connecting Hermes.
5. Do not create duplicate company knowledge in Open WebUI native Knowledge when the selected architecture routes company facts through Hermes → WeKnora.

### Stage C — Hermes Agent

1. Install the validated host-native Hermes version through `DEPLOY.md §4.1` and prove runtime identity through §4.2.
2. Reconcile the privileged/default control plane plus baseline `general` employee Profile through `infrastructure/hermes/PROVISIONING.md`.
3. On a fresh target create `general` through upstream Profile management with bundled-Skill opt-out; on an existing target reconcile it in place.
4. Configure specialist Profiles only when an explicit capability boundary requires them.
5. Install only repository-approved Skills required by the selected Profile/capability boundary.
6. Configure profile-local MCP names so shared-gateway registrations do not collide.
7. Keep employee/Profile memory disabled unless a later approved baseline explicitly changes it.
8. Enable only the narrow tools required by the Profile; generic shell/filesystem/browser/code execution must not be exposed merely for convenience.
9. Prove the shared Gateway serves exactly the intended Profile set and that Profile-scoped API credentials fail closed across routes.

### Stage D — Open WebUI

1. Deploy the validated Open WebUI container through `DEPLOY.md §4.1` and prove runtime identity through §4.2.
2. Reconcile groups, Hermes Profile connections, employee-visible Model/Assistant ACL resources, and feature permissions through `infrastructure/open-webui/PROVISIONING.md`.
3. Consume the Hermes Profile route/model handoff and company logical group mappings from the protected operational state; resolve API-key values only from protected secret storage.
4. Preserve persistent data and unrelated legitimate administrator-owned resources.
5. Grant resource READ ACLs rather than workspace management rights.
6. Preserve WeKnora as the company-knowledge authority; do not attach a duplicate EAO-managed native Open WebUI company Knowledge corpus.
7. Validate login, backend-to-Hermes connectivity, employee model visibility, chat history, file upload, reload persistence, unauthorized model denial, and unauthenticated denial.
8. Record logical group ID → display name → runtime UUID and Profile/model ACL mappings back into the protected operational state.

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

### Stage F — resolve enabled conditional capabilities

Before adding any specialist Profile, Skill bundle, MCP runtime, scheduler, messaging
surface, browser/research backend, transcription engine, Email integration, or remote
access layer, resolve the active target against `config/capabilities.yaml`.

The rule is:

```text
active company configuration
+ capability registry
→ only explicitly enabled conditional capabilities
```

If a capability is not enabled for the target, do not install it merely because the
ARMOR reference implementation contains it.

For every enabled conditional capability, treat its `records` list in
`config/capabilities.yaml` as a mandatory completion-evidence checklist. Write
those non-secret records into the protected operational copy created from
`state/DEPLOYMENT-STATE.template.md`; do not scatter them across ad hoc notes.

#### Stage F.1 — ARMOR Operations reference bundle, when selected

The ARMOR Operations bundle is a validated reference capability, not universal EAO
Core. Reproduce it only when the target explicitly selects the corresponding
specialist workflow boundary.

Install only the accepted/frozen Skills and preserve their authority boundaries. The
current ARMOR Operations capability baseline includes canonical entry points for:

- website article production;
- website product materials;
- social-media content, including video rules;
- MIC product optimization;
- product-visual preparation;
- AI-writing audit and supporting approved department Skills.

Use `docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md` as the current frozen
capability authority. Use `docs/PHASE4*` and `docs/PHASE5*` only as migration
provenance/evidence. Do not re-enable triaged legacy Skills merely because files
exist in historical inventories.

#### Stage F.2 — Enterprise Web Research, when enabled

Use the already-approved Enterprise Web Research capability before adding another
browser/search stack. Validate the adapter and selected upstream runtime path using
`docs/ENTERPRISE-WEB-RESEARCH-V1.md`, `config/mcp-registry.yaml`, and the
repository checks.

Do not install Firecrawl, Obscura, CloakBrowser, or another browser backend for a
target that has not enabled this capability.

#### Stage F.3 — Media transcription, when enabled

Use `infrastructure/media-transcription/` and `scripts/transcribe` for the
validated host-native transcription capability. Do not introduce a separate
transcription service unless the approved capability is proven insufficient.

A target that does not enable media transcription does not need Whisper, SenseVoice,
or ffmpeg for EAO Core.

#### Stage F.4 — Governed Email Operations, when enabled

Email is a governed side-effect capability and must remain narrower than generic
IMAP/SMTP access.

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

Use the governance SQLite schema/runtime and provider adapters under
`infrastructure/email/`. Do not expose unrestricted send credentials to
employee-facing Agents.

#### Stage F.5 — all other conditional capabilities

For Hermes WebUI, coding delegation, Kanban, Cron, messaging, SSO, remote access,
employee long-term Memory, or later registered capabilities, follow the exact
`implementation`, required-input, security-boundary, and `acceptance` entries in
`config/capabilities.yaml`.

Do not infer enablement from repository file presence. Employee long-term Memory
remains OFF unless its exact isolation gate is explicitly enabled and passes.

### Stage G — network and access boundary

Expose only the surfaces selected by the target configuration.

Core requires an employee-reachable Open WebUI surface, but it does not require a
specific remote-access product. LAN-only access, an already-approved private network
layer, or an explicitly enabled `remote_access` capability are separate deployment
choices.

Do not create a new VPN, reverse proxy, SSO system, or public ingress architecture
without a demonstrated requirement and Capability Reuse Pass.

### Stage H — acceptance and freeze

Run the Core checks for every deployment:

- repository integrity/readiness;
- selected component health;
- direct and employee-path knowledge tests;
- Open WebUI RBAC tests;
- restart persistence;
- unauthenticated-access denial;
- the recovery checks required by the requested readiness level.

Then run acceptance only for capabilities actually enabled on that target, for example:

- Operations Skill/runtime checks;
- Enterprise Web Research checks;
- Email governance/provider checks;
- media-transcription smoke tests;
- Cron/Kanban/messaging/SSO/remote-access checks where selected.

For `production-ready`, also close the production controls in
`config/capabilities.yaml`, including backup/restore, startup recovery,
security/access review, and operations health.

Create/update the deployment's protected operational state from
`state/DEPLOYMENT-STATE.template.md`, including the Core runtime handoff mappings
and exact baseline commit. Do not overwrite the repository's historical
`state/DEPLOYMENT-STATE.md`.

Publish a sanitized public summary only when that reference-deployment activity
is explicitly authorized. A deployment is not frozen until its protected
acceptance/state record can be traced to repository evidence without exposing
company-private runtime state.

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
