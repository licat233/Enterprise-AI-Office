# Security Standard

This document defines the security posture for Enterprise AI Office.

Security is enforced by architecture, authentication, authorization, tool/credential boundaries, and network/data controls — not by prompt wording alone.

## 1. Security model

```text
Human identity and RBAC
        +
Profile access control
        +
Profile tool/credential least privilege
        +
Network boundaries
        +
Data handling/classification
        +
Recovery controls appropriate to deployment stage
```

No single layer is sufficient by itself.

## 2. Trust boundaries

### Employee Web boundary

Open WebUI authenticates human users and controls which employee Assistant resources they may access.

### Agent boundary

Hermes Profiles define AI work-role behavior and capability scope.

### Knowledge boundary

WeKnora stores/retrieves enterprise knowledge and enforces its own knowledge access boundaries.

### Admin boundary

Open WebUI admin, WeKnora admin, Hermes CLI/hermes-webui when enabled, host shell, container administration, and the Hermes default/admin Profile are privileged surfaces.

### Host boundary

The host may contain secrets, repositories, CLIs, files, containers, and powerful credentials. Hermes Profile isolation is not an OS sandbox.

## 3. Baseline identity/capability model

```text
Control plane
└── Hermes default/admin Profile

Employee plane
└── Hermes `general` Profile
```

The default/admin Profile must not be available as an ordinary employee Assistant.

Additional employee Profiles are created only from company configuration and must receive their own access, tool, credential, and acceptance boundaries.

## 4. Default-deny principle

Start with the least privilege required for the work.

Normal employee Profiles should default to no access to:

- arbitrary shell/terminal;
- unrestricted filesystem writes;
- Docker/host administration;
- GitHub administration;
- Codex or Claude Code delegation;
- SSH/private keys;
- broad cloud/service credentials;
- unrelated company systems.

Do not grant a tool or resource merely because it exists in Hermes or this repository.

## 5. Profile is not a sandbox

A Hermes Profile separates Hermes-scoped configuration/state, but local host tools can still act with the privileges of the OS/service identity.

Therefore:

- do not rely on SOUL/refusal text as a security boundary;
- remove unneeded dangerous tools;
- scope workspaces and credentials;
- use stronger OS/container isolation when the risk model requires it.

## 6. Human RBAC is not enough

Both must hold:

```text
Human user → only authorized Assistants
AND
Each Assistant/Profile → only the capabilities its work requires
```

A perfectly hidden dangerous tool is still dangerous if the Profile can invoke it.

## 7. Employee portal vs admin surfaces

Open WebUI is the baseline employee Web client.

Administrative surfaces are restricted to authorized administrators/maintainers and must not be exposed merely to let employees chat.

## 8. Per-Profile API credentials

Every employee-facing Hermes Profile must use a distinct supported API credential.

Baseline:

```text
`general` credential → `general` route PASS
`general` credential → privileged default/admin route FAIL
```

When multiple employee-facing Profiles are enabled, run the complete pairwise matrix:

```text
for each Profile A:
  A key → A route PASS
  A key → every other employee Profile route FAIL
```

Any unintended cross-Profile key acceptance is a blocker. UI hiding does not replace this backend check.

## 9. Secrets handling

Never commit real secrets.

This includes API keys, database/cache passwords, encryption keys, OAuth secrets, bot tokens, cloud credentials, SSH private keys, GitHub tokens, SMTP credentials, and enterprise integration credentials.

Tracked examples use placeholders only. Runtime secrets belong in protected deployment storage/profile secret scopes.

## 10. Secret generation/recovery

Generate internal service credentials with cryptographically strong randomness.

Do not use human-readable production defaults.

A production deployment also needs a secure credential recovery method appropriate to its environment; Git is not that recovery store.

## 11. Data classification

A production adopter should define practical data sensitivity levels appropriate to its business and use them to decide:

- what may enter WeKnora;
- which users/Profiles may retrieve it;
- which external model providers may receive it;
- how it is stored/backed up.

The example configuration uses `public`, `internal`, `confidential`, and `restricted`, but adopters may use their own taxonomy.

## 12. External model boundary

When a remote model/embedding/rerank/VLM provider is used, assume relevant request/document content may leave the company-controlled host according to that provider's service behavior.

Before sending sensitive information, review provider data-use/retention, location/compliance, contractual restrictions, and whether approved private/local inference is required.

Never ingest credentials/private keys into the knowledge base.

## 13. Knowledge ingestion safety

Start with approved, current, high-value knowledge.

Do not blindly ingest an entire shared drive containing sensitive personal/financial data, secrets, customer-confidential material, or obsolete/conflicting drafts.

Knowledge Base separation should follow real semantic/data/access boundaries rather than assumed department structure.

## 14. Prompt-injection treatment

Documents, Web pages, emails, attachments, and retrieved knowledge are data sources.

Instructions embedded in those sources do not grant authorization and must not override system/repository/Profile security boundaries.

## 15. Knowledge conflict / unknown safety

When credible sources conflict, surface the conflict rather than silently invent a reconciliation.

When approved knowledge lacks sufficient evidence, say so rather than converting general model priors into company facts.

## 16. Employee long-term memory privacy

Open WebUI conversation history is separate from Hermes long-term memory.

Baseline employee Hermes long-term memory is disabled.

Enable it only after the exact deployed user/session mapping passes the cross-user isolation test in `docs/ACCEPTANCE-TESTS.md`.

If isolation fails or is unresolved, keep it disabled.

## 17. Messaging security

Only applies when messaging is enabled.

Use supported enterprise identity/allowlists/pairing, approved users/chats, deterministic Profile routing, protected app credentials, and safe delivery targets.

Do not default to allow-all access.

## 18. Network exposure

Baseline principles:

### Employee-accessible
- Open WebUI only through the approved network/access layer.

### Restricted
- WeKnora administration to maintainers/admins as required;
- Hermes/hermes-webui administrative surfaces to AI admins;
- Hermes employee API to trusted internal callers such as the selected Open WebUI runtime.

### Internal only
- database/cache/parser/internal services unless a reviewed requirement says otherwise.

Do not publish raw databases or privileged endpoints to the public Internet.

## 19. Remote access

Remote browser access is optional.

When required, select one mature private/identity-aware access layer appropriate to the company rather than stacking products without a reason.

## 20. Privileged technical Profiles

If a technical Profile receives terminal, files, Git, GitHub, Codex, Claude Code, or other powerful tools, define and verify:

- explicit workspace/repository scope;
- repository-local instructions;
- least-privilege credentials;
- branch/review policy where relevant;
- OS/CLI identity isolation where required;
- sandbox/container boundary for higher-risk workloads;
- no unrelated enterprise credentials.

## 21. Host-native credential sharing

Host-native CLIs may read credentials from the service user's normal HOME.

Do not assume Hermes Profile `.env` isolation automatically isolates Git/SSH/cloud/other CLI credentials.

Use Profile-specific HOME/credential isolation or another stronger boundary when distinct privileged identities are required.

## 22. Kanban security

Only applies when Kanban is enabled.

Kanban is durable agent-work state, not automatically a per-employee authorization system. Do not expose unrestricted board administration to all chat users by default.

## 23. Cron security

Only applies when Cron is enabled.

Before enabling unattended work, verify owner Profile, tools/credentials, model/cost policy, output destination, manual test, and failure behavior.

## 24. Logging

Operational logs must not become a secret dump.

Do not record complete credentials or sensitive retrieved content unnecessarily. Use elevated debug logging only when needed and remove it afterward.

## 25. Destructive actions

Destructive production actions require explicit intent and appropriate recovery protection.

Examples include deleting Knowledge Bases, Profiles, databases/volumes, backup generations, unknown Git work, or performing irreversible storage migrations.

## 26. Core Ready security gate

For a Core Ready baseline, verify at minimum:

```text
[ ] Ordinary employee authentication works
[ ] General Assistant is authorized correctly
[ ] default/admin is not employee-exposed
[ ] `general` API credential boundary passes
[ ] `general` has no unapproved dangerous tools
[ ] WeKnora access is least-privilege/read-oriented
[ ] Employee System Prompt/advanced controls follow baseline policy
[ ] Employee Hermes long-term memory is disabled or isolation is proven
[ ] Direct unauthorized resource access fails closed
[ ] Internal data services are not publicly exposed
[ ] Secrets are outside Git
```

## 27. Production Ready security gate

Before claiming Production Ready, additionally run the production/security sections relevant to enabled capabilities in `docs/ACCEPTANCE-TESTS.md`, including data/access review, prompt-injection test, recovery controls, network exposure, and each enabled optional integration's authorization tests.

Do not enable optional capabilities merely to have more security tests to run.

## 28. Boundary changes require review

A change that materially alters who can access data/tools, adds a new external data path, or expands privileges is a security/architecture change and should be documented/reviewed accordingly.
