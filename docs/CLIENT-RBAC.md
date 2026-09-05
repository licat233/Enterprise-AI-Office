# Employee Client and RBAC Standard

This document defines how human employees access Enterprise AI Office through Open WebUI and how those identities map to Hermes Profiles.

For deployment execution, follow `DEPLOY.md` first.

## 1. Client roles

### Open WebUI

Baseline multi-user employee Web portal.

Responsibilities:

- user authentication;
- groups;
- Assistant/resource access;
- chat UX;
- conversation history;
- attachments when enabled.

### Administrative surfaces

Open WebUI admin, Hermes CLI/hermes-webui when enabled, and WeKnora admin are control-plane surfaces.

They are not ordinary employee clients.

### Messaging platforms

Messaging surfaces are optional extensions. Enable only those the company actually uses.

## 2. Identity mapping

Keep human identity and AI work-role identity separate.

```text
Human employee
→ Open WebUI user
→ Group/resource authorization
→ Assistant
→ Hermes Profile
```

Baseline:

```text
ordinary employee
→ All-Employees
→ General Assistant
→ `general`
```

Additional mappings come from company configuration.

## 3. Baseline groups

The generic baseline is:

```text
All-Employees
AI-Admins
```

Create additional groups only when a real authorization boundary requires them.

A department name by itself is not sufficient reason to create a group unless different resource access is needed.

## 4. Default employee permissions

Global/default employee permissions should be minimal.

The validated baseline keeps:

```text
Normal chat              enabled
Conversation history     enabled
File upload              enabled unless company policy disables it
Chat System Prompt       disabled
Advanced Chat Parameters disabled
```

Normal employees should not automatically receive:

- model/provider administration;
- Knowledge administration;
- tool administration;
- API-key management;
- public sharing;
- unrestricted Assistant creation;
- system/admin settings.

Use Open WebUI's native permission model for the installed release rather than source edits or CSS hiding.

## 5. Resource visibility

Every Hermes-backed employee Assistant should be private/restricted and explicitly shared with intended groups/users.

Baseline:

```text
All-Employees → General Assistant → Hermes `general`
```

Do not rely on UI visibility alone as the security control. Verify unauthorized direct resource/API access is rejected.

## 6. Specialist mappings

If company configuration enables a specialist Profile:

1. create only the authorization group(s) actually needed;
2. create the matching private Assistant resource;
3. connect it server-side to that Profile;
4. grant it only to intended users/groups;
5. run the conditional specialist RBAC tests in `docs/ACCEPTANCE-TESTS.md`.

Do not infer specialist groups from the optional templates under `profiles/`.

## 7. Admin separation

AI administrators may use approved administrative surfaces.

Ordinary employees must not receive administrative Hermes credentials merely to use chat.

The Hermes default/admin Profile is never the ordinary employee General Assistant.

## 8. Hermes Profile connections

Open WebUI connects server-side to employee-facing Hermes Profile API endpoints using Profile-scoped credentials.

Baseline conceptual route:

```text
General Assistant → /p/general/... → `general` Profile key
```

Exact URLs and supported connection behavior must match the pinned Hermes/Open WebUI versions.

For every additional employee Profile, create a distinct connection using that Profile's own key.

## 9. Credential handling

Hermes API keys belong in server-side connection configuration or protected secrets, never in employee browsers or Git.

Use a unique credential per employee-facing Profile.

When multiple employee Profiles are enabled, run the complete pairwise cross-Profile credential test.

## 10. Long-term memory scope

Open WebUI conversation history is independent of Hermes long-term memory.

Employee Hermes long-term memory is disabled by baseline policy until a stable user-scoped Open WebUI → Hermes memory/session mechanism passes the cross-user isolation test for the exact deployed versions.

Do not invent or assume a mapping between browser chat IDs and persistent Hermes memory scope.

## 11. Cross-user memory gate

Only when enabling Hermes employee long-term memory:

- use two distinct employees authorized for the same Profile;
- store a unique private marker for User A;
- attempt retrieval from User B;
- verify User B cannot recover User A's private data;
- verify intended User A continuity if user-scoped memory is the design.

If isolation cannot be proven, keep Hermes employee long-term memory disabled and rely on Open WebUI conversation history.

## 12. RBAC acceptance model

For every enabled employee Assistant:

```text
intended user/group    → allow
unauthorized user/group → deny
ordinary employee      → admin/default deny
```

Test both UI visibility and direct unauthorized access.

Do not create unused Assistants merely to populate an RBAC matrix.

## 13. Group permissions are additive

When the selected Open WebUI release uses additive group permissions, configure global defaults conservatively.

Do not grant broad global permissions and expect another group to subtract them later.

## 14. New employee onboarding

For each new employee:

1. create/activate identity according to company auth policy;
2. assign only required groups/resources;
3. verify effective Assistant access;
4. do not grant admin for convenience;
5. test at least one authorized path and, when applicable, one unauthorized path.

## 15. Employee departure / role change

When a user leaves or changes roles:

- disable/remove user access promptly;
- update group memberships/resource grants;
- review personal tokens if any were issued;
- preserve business records according to company policy;
- do not delete shared Profiles merely because one employee left.

## 16. File upload policy

File upload may be enabled for temporary conversation context when the deployed Open WebUI/Hermes path supports the intended file types and company policy permits it.

Durable authoritative company knowledge should be ingested through WeKnora knowledge-management workflows rather than treated as chat attachments.

## 17. Remote browser access

If Open WebUI is reachable outside the approved local network, place it behind an approved private/identity-aware access layer with appropriate authentication and TLS/network controls.

Remote access is not part of the baseline unless company configuration enables it.

## 18. Messaging identity

When messaging is enabled, authenticated enterprise users/chats must map deterministically to approved Profiles.

Do not infer privileged Profile selection from arbitrary message text.

Use supported routing, allowlists/pairing, and platform identity controls.

## 19. Client acceptance checklist

```text
[ ] Admin account/access secured
[ ] Baseline All-Employees and AI-Admins boundaries configured
[ ] Default employee permissions minimal
[ ] General Assistant private/restricted to intended employees
[ ] Hermes default/admin not employee-exposed
[ ] Employee Profile API credentials server-side and unique
[ ] Ordinary employee login/chat/history works
[ ] Grounded answer/source path works
[ ] Direct unauthorized resource request fails closed
[ ] Specialist groups/resources exist only when configured
[ ] Long-term memory disabled or isolation proven
[ ] File upload tested if enabled
[ ] Remote-access boundary tested if enabled
```

Specific validation results from an individual deployment belong in `state/DEPLOYMENT-STATE.md` and `state/CHANGELOG.md`.
