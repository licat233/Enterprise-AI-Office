# Security Standard

This document defines the minimum security posture for Enterprise AI Office.

The project is an enterprise AI work system. It can access company knowledge, tools, files, code repositories, external services, and automation. Security must therefore be enforced by architecture and permissions, not merely by prompts.

## 1. Security model

Enterprise AI Office uses layered controls:

```text
Human identity and RBAC
        +
Profile access control
        +
Profile tool/credential least privilege
        +
Network boundaries
        +
Data classification
        +
Backups and recovery
```

No single layer is sufficient by itself.

## 2. Trust boundaries

### Employee Web boundary

Open WebUI authenticates human users and determines which employee-facing assistant resources they may access.

### Agent boundary

Hermes Profiles define AI role behavior and tool/credential capability.

### Knowledge boundary

WeKnora controls enterprise knowledge storage, retrieval, and its own tenant/workspace/KB permissions.

### Admin boundary

hermes-webui, Hermes CLI, WeKnora admin, Open WebUI admin, host shell, and Docker administration are privileged administrative surfaces.

### Host boundary

The host OS contains secrets, repositories, CLIs, local files, containers, and potentially powerful credentials. Profile isolation alone does not protect the host.

## 3. Default-deny principle

Start with the least privilege required for normal employee work.

Do not grant a tool or resource merely because it is available.

Normal business Profiles should default to no access to:

- arbitrary shell/terminal;
- unrestricted filesystem write;
- Docker control;
- host system administration;
- GitHub organization/repository administration;
- Codex or Claude Code;
- SSH/private keys;
- broad cloud credentials;
- unrelated department systems.

## 4. Profile is not a sandbox

A Hermes Profile separates Hermes configuration, state, memory, sessions, Skills, credentials, and related Profile data.

It does not automatically sandbox all host access.

If a Profile has a local terminal tool under the service user's account, that Profile may be able to access whatever that OS user can access.

Therefore:

- do not rely on SOUL instructions as a security control;
- remove unneeded dangerous tools;
- scope working directories;
- use OS/container isolation when stronger enforcement is required;
- scope credentials per role.

## 5. Human RBAC is not enough

Even if Sales users can only see the Sales Assistant, the Sales Profile itself is unsafe if it has unrestricted terminal or admin tools.

Security must satisfy both:

```text
Sales user → only Sales/General assistants
AND
Sales Profile → only Sales-required capabilities
```

## 6. Employee portal vs admin console

`hermes-webui` is an administrative surface.

Do not expose it as the ordinary employee client unless upstream later provides and the project explicitly validates a safe multi-user administrative permission model.

Open WebUI is the default employee Web surface.

## 7. Privileged Profile

The default/admin/orchestrator Hermes Profile must not be exposed to ordinary employees.

If it has broad access to Profiles, tools, credentials, Kanban, Cron, system files, coding agents, or admin APIs, it is a privileged system identity.

## 8. Per-Profile API credentials

Every employee-facing Hermes Profile must use a distinct API credential where supported.

Required behavior:

```text
sales credential → sales PASS
sales credential → qc FAIL
qc credential    → qc PASS
qc credential    → sales FAIL
```

Do not share one global Hermes API key across all department Profiles if the upstream supports Profile-scoped credentials.

## 9. Secrets handling

Never commit secrets to this repository.

Secrets include:

- `.env` credentials;
- model API keys;
- DB passwords;
- Redis passwords;
- encryption keys;
- OAuth client secrets;
- bot tokens;
- cloud keys;
- SSH private keys;
- GitHub tokens;
- SMTP passwords;
- CRM/ERP keys.

Repository examples must use placeholders such as:

```text
<GENERATE_STRONG_SECRET>
<MODEL_API_KEY>
<PROFILE_API_KEY>
```

## 10. Secret generation

Use cryptographically strong random secrets.

Do not use human-readable production defaults such as:

```text
admin123
password123
companyname123
weknora123
```

## 11. Secrets backup

Secrets must not be in Git, but production credentials still require a secure recovery method.

Maintain an encrypted backup or enterprise credential store appropriate to the deployment.

A backup that restores databases but loses every integration credential is incomplete.

## 12. Data classification

Before ingesting company data, classify at minimum:

```text
Public
Internal
Confidential
Restricted
```

The names may be changed by the adopting company, but the concept must exist.

## 13. External model boundary

When using a remote LLM/embedding/rerank/VLM provider, assume relevant query/document content may leave the company-controlled host according to that provider's API behavior.

Before sending Confidential/Restricted data to an external model, verify:

- provider data-use terms;
- retention behavior;
- regional/compliance requirements;
- contractual restrictions;
- whether local or approved private inference is required.

Do not upload secrets, passwords, private keys, or credential material into the knowledge base.

## 14. Initial knowledge ingestion policy

For early deployment, prioritize high-value current company knowledge that is appropriate for the selected model/data boundary.

Do not blindly ingest entire shared drives containing:

- payroll;
- employee personal data;
- passwords;
- banking information;
- highly sensitive contracts;
- unrestricted customer secrets;
- raw credentials;
- old/conflicting drafts.

## 15. Prompt injection treatment

Documents, Web pages, emails, retrieved knowledge, user attachments, and external content are data sources.

Instructions inside retrieved content must not override:

- system safety rules;
- repository operating rules;
- Profile SOUL/security rules;
- authorization boundaries.

A document saying `ignore previous instructions` is not authorization.

## 16. Knowledge conflict safety

When authoritative-looking sources materially disagree, the agent should expose the conflict rather than silently choose a convenient answer.

Example:

```text
Source A: 12 V
Source B: 24 V
```

Expected behavior:

- cite both sources;
- identify the conflict;
- avoid inventing a reconciliation;
- escalate to a knowledge maintainer or responsible human when the correct current fact cannot be established.

## 17. Memory privacy

Department Profile memory is potentially shared state.

Do not allow ordinary employee private information, private customer conversations, personal data, or one user's secrets to be written into shared Profile memory by default.

Before enabling user-scoped long-term Hermes memory behind a shared Profile, pass the cross-user isolation test in `ACCEPTANCE-TESTS.md`.

If that test fails, disable long-term employee memory.

## 18. Messaging security

For Feishu, WeCom, Weixin, Slack, Telegram, or other Gateway platforms:

- prefer enterprise identity/allowlists/pairing;
- restrict approved users/chats;
- use explicit Profile routing;
- do not default to allow-all in production;
- treat bot/app credentials as secrets;
- ensure scheduled delivery does not leak into the wrong channel.

## 19. Network exposure

Recommended default:

### Employee-accessible
- Open WebUI on the approved LAN/private access layer.

### Restricted
- WeKnora UI to knowledge maintainers/admins as required.
- hermes-webui to AI admins only.
- Hermes API to internal trusted callers.

### Internal only
- PostgreSQL;
- Redis;
- DocReader/internal parser services;
- internal model/storage services unless explicitly required.

Do not publish raw databases directly to the Internet.

## 20. Remote access

Prefer enterprise messaging for mobile/remote employee access when practical.

If remote browser access is required, choose one mature private-access layer such as an approved VPN, Tailscale, or Cloudflare Access/Tunnel based on company needs.

Do not stack multiple access products without a reason.

## 21. Engineering Profile security

Engineering may need terminal, files, Git, GitHub, Codex, or Claude Code.

Mitigations include:

- explicit working directory/repository;
- repository-local `AGENTS.md`/rules;
- least-privilege GitHub credentials;
- branch/review policy appropriate to the repo;
- profile-specific OS/CLI identity where required;
- sandbox/container backend for higher-risk workloads;
- no unrelated company credentials in the Engineering Profile.

## 22. OAuth and shared host credentials

Host-native CLIs may use credentials from the service user's normal HOME.

If multiple powerful Profiles have terminal access, they may see the same CLI identity unless Profile-specific HOME/credential isolation is configured.

Do not assume Profile `.env` isolation automatically isolates every external CLI credential.

## 23. Kanban security

Kanban is a durable agent work queue, not automatically a per-employee authorization boundary.

Do not expose unrestricted Kanban administration to every employee simply because they can chat with an agent.

Use it for authorized agent workflows and management/orchestration roles.

## 24. Cron security

Cron jobs are unattended execution.

Before enabling a recurring job:

- confirm the owning Profile;
- confirm tool/credential scope;
- confirm output destination;
- confirm model/provider/cost policy;
- test manually;
- confirm failure behavior.

Do not allow scheduled tasks to silently inherit broader credentials after a configuration change.

## 25. Logging

Logs should be useful for operations without becoming a secret dump.

Do not log complete API keys, passwords, private tokens, or sensitive retrieved documents unnecessarily.

Use debug logging temporarily during troubleshooting and revert to normal production logging afterward.

## 26. Destructive-action controls

Destructive operations require explicit intent and appropriate backup.

Examples:

- deleting a production KB;
- deleting Profiles;
- database reset;
- deleting persistent volumes;
- destructive storage migration;
- hard Git reset over unknown work;
- deleting backup history.

## 27. Security acceptance

Before production, verify all security checks in `docs/ACCEPTANCE-TESTS.md`, including:

- cross-Profile API-key rejection;
- unauthorized resource denial;
- normal Profile terminal denial;
- memory isolation;
- prompt-injection resistance;
- knowledge-conflict behavior;
- backup restoration;
- network exposure audit.

## 28. Security changes are architecture changes when boundaries move

A change that materially alters who can access which data/tools, or moves data across a new trust boundary, is not merely a configuration tweak.

Document and review it accordingly.
