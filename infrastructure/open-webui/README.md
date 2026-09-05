# Open WebUI Deployment Adapter

Open WebUI is the default employee-facing multi-user Web client for Enterprise AI Office.

This directory is reserved for tested Enterprise AI Office configuration layered on top of a pinned Open WebUI release.

## Responsibilities

Open WebUI owns:

- human user accounts/authentication;
- groups;
- employee-facing chat UX;
- authorized assistant/resource visibility;
- conversation history.

It does **not** own Hermes Profile definitions or WeKnora company knowledge.

## Deployment posture

Deploy Open WebUI independently from WeKnora so either project can be upgraded or rolled back without unnecessarily coupling their release cycles.

Use a pinned tested release rather than a floating production tag.

## RBAC posture

Global/default user permissions should be minimal.

Create private/restricted assistant resources mapped to approved groups.

Reference mapping:

```text
All-Employees → General Assistant → Hermes general Profile
Sales         → Sales Assistant   → Hermes sales Profile
QC            → QC Assistant      → Hermes qc Profile
Marketing     → Marketing Assistant → Hermes marketing Profile
Engineering   → Engineering Assistant → Hermes engineering Profile
```

## Hermes connections

Create server-side OpenAI-compatible connections/resources for employee-facing Hermes Profiles using the supported API route for the deployed Hermes release.

Use unique Profile API credentials and keep them server-side.

Do not create an ordinary employee connection to the privileged Hermes default/admin Profile.

## Memory scoping

Where the installed Open WebUI/Hermes versions support it, configure a stable user-derived Hermes session key using dynamic headers.

Do not enable employee long-term memory until the cross-user isolation test passes.

## File handling

Do not assume all Open WebUI file upload features map cleanly to Hermes API input formats.

Test supported file/image workflows explicitly before enabling them for employees.

Official company knowledge ingestion belongs in WeKnora.

## License note

Open WebUI currently uses its own upstream license rather than this repository's Apache-2.0 license.

Review `THIRD_PARTY_NOTICES.md` and the exact upstream license for the deployed version, especially before rebranding or large deployments.

## Validation

Run all authentication, group/resource ACL, direct unauthorized-access, and cross-user memory tests in `docs/ACCEPTANCE-TESTS.md`.
