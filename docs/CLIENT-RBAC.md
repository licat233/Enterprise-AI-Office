# Employee Client and RBAC Standard

This document defines how human employees access Enterprise AI Office through the Web client and how those identities map to Hermes Profiles.

## 1. Client roles

### Open WebUI

Default multi-user employee Web portal.

Responsibilities:

- user authentication;
- groups;
- resource/model/assistant access;
- chat UX;
- conversation history.

### hermes-webui

Administrative Hermes control surface.

Responsibilities may include:

- Profiles;
- SOUL;
- Skills;
- MCP;
- models;
- memory;
- Cron;
- Kanban;
- Gateway/settings.

It is not the ordinary employee client.

### Messaging platforms

Feishu, WeCom, Weixin, or another approved Hermes Gateway platform may provide mobile/remote employee access.

They complement the Web client rather than becoming a separate agent architecture.

## 2. Identity mapping

Keep human and agent identity separate.

```text
Human employee
→ Open WebUI user
→ Group membership
→ Authorized assistant resource
→ Hermes Profile
```

Example:

```text
Alice
  groups: Sales, All-Employees
  assistants: General Assistant, Sales Assistant
```

## 3. Recommended generic groups

A company may start with:

```text
All-Employees
Sales
QC
Marketing
Engineering
Operations
Management
AI-Admins
```

Only create groups that correspond to real authorization needs.

## 4. Default permissions

Global/default employee permissions should be minimal.

Normal users should not automatically receive:

- model workspace administration;
- Knowledge administration;
- prompt/system prompt administration;
- tool administration;
- API-key management;
- public sharing;
- unrestricted assistant creation;
- admin settings.

Grant additional capabilities through specific groups when needed.

## 5. Resource visibility

Each Hermes-backed employee assistant should be private/restricted and explicitly shared with authorized groups/users.

Do not rely on hiding UI entries as the security control. Verify unauthorized direct access is rejected.

## 6. Reference assistant mapping

```text
All-Employees → General Assistant → general Profile
Sales         → Sales Assistant   → sales Profile
QC            → QC Assistant      → qc Profile
Marketing     → Marketing Assistant → marketing Profile
Engineering   → Engineering Assistant → engineering Profile
```

Management may be granted selected cross-department assistants according to company policy.

## 7. Admin separation

AI administrators may use Open WebUI admin, WeKnora admin, Hermes CLI, and hermes-webui.

Ordinary employees must not receive administrative Hermes credentials merely to use chat.

## 8. Hermes Profile connections

Open WebUI should connect server-side to Hermes employee-facing Profile API endpoints using Profile-scoped credentials where supported.

Conceptually:

```text
General connection   → /p/general/...   → general Profile key
Sales connection     → /p/sales/...     → sales Profile key
QC connection        → /p/qc/...        → qc Profile key
Marketing connection → /p/marketing/... → marketing Profile key
```

Exact URLs depend on the installed Hermes release and must be verified from current upstream behavior.

## 9. Credential handling

Hermes API keys belong in server-side connection configuration or protected secrets, not in employee browsers.

Use a unique credential per employee-facing Profile.

## 10. Long-term memory scope

Where Hermes/Open WebUI versions support it, use a stable user-scoped session-key header for long-term memory isolation.

Conceptual values:

```text
general:webui:<USER_ID>
sales:webui:<USER_ID>
qc:webui:<USER_ID>
```

Use stable non-secret user IDs rather than display names that may change or collide.

Exact dynamic-header syntax must be verified against the deployed Open WebUI release.

## 11. Transcript identity

Transcript/conversation IDs and long-term memory keys are different concerns.

If a separate Hermes transcript/session header is used, validate it independently. Do not assume a browser chat ID is automatically a valid persistent Hermes memory scope.

## 12. Cross-user memory acceptance test

Use at least two users on the same department Profile.

User A supplies a unique private marker and asks the agent to remember it.

User B then tries to retrieve that marker.

Expected: User B cannot access it.

If the test fails, disable user long-term memory and rely on Open WebUI conversation history until corrected.

## 13. Cross-Profile memory acceptance test

The same user should not accidentally leak user-scoped Sales memory into Marketing or another Profile unless an intentionally shared memory provider is designed and approved.

## 14. RBAC test matrix

At minimum test:

| User | General | Sales | QC | Marketing | Engineering | Admin |
| --- | --- | --- | --- | --- | --- | --- |
| Sales test | allow | allow | deny | deny unless justified | deny | deny |
| QC test | allow | deny | allow | deny | deny | deny |
| Marketing test | allow | deny | deny | allow | deny | deny |
| Engineering test | allow | deny by default | deny by default | deny by default | allow | deny |
| AI Admin | as configured | as configured | as configured | as configured | as configured | allow |

Adapt this matrix to the actual company.

## 15. Group permissions are additive

When the selected client uses additive group permissions, configure global defaults conservatively.

Do not give broad global permissions and expect another group to subtract them later.

## 16. New user onboarding

For each new employee:

1. create/activate user according to company auth policy;
2. assign only required groups;
3. verify effective assistant/resource access;
4. do not grant admin by convenience;
5. test one authorized and one unauthorized assistant.

## 17. Employee departure / role change

When a user leaves or changes roles:

- disable/remove user access promptly;
- update group memberships;
- review API tokens personally issued to that user, if any;
- preserve business records according to company policy;
- do not delete shared department Profiles just because one employee left.

## 18. File upload policy

Do not assume every Open WebUI file workflow is automatically compatible with Hermes API behavior.

Before enabling ad-hoc employee file upload through the Hermes connection, test the installed versions and approved file types.

Official company knowledge ingestion should continue through WeKnora knowledge-management workflows.

## 19. Remote browser access

If Open WebUI must be reachable outside the office, place it behind one approved private/identity-aware access layer.

Do not expose the portal directly without authentication/TLS/network controls.

## 20. Messaging identity

Messaging platforms must map authenticated enterprise users/chats to approved Profiles.

Do not infer privileged Profile selection from arbitrary user text.

Use supported routing configuration, separate bot credentials, or explicit route rules.

## 21. Client acceptance checklist

```text
[ ] Admin account secured
[ ] Default user permissions minimal
[ ] Department groups created
[ ] Employee assistants private/restricted
[ ] Profile API credentials unique
[ ] Sales cannot access QC
[ ] QC cannot access Sales
[ ] Normal users cannot access admin surfaces
[ ] Direct unauthorized resource request fails
[ ] Cross-user memory test passes or long-term memory disabled
[ ] Conversation history works
[ ] Logout/session behavior tested
[ ] Remote-access boundary documented if enabled
```
