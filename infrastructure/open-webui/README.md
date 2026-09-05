# Open WebUI Deployment Adapter

Open WebUI is the default employee-facing Web client for Enterprise AI Office.

For deployment execution, follow `DEPLOY.md` first. This adapter describes the validated integration pattern and the baseline employee permission model.

## Responsibilities

Open WebUI owns:

- human user accounts/authentication;
- groups;
- employee-facing chat UX;
- authorized assistant/resource visibility;
- conversation history.

It does not own Hermes Profile definitions or WeKnora company knowledge.

## Baseline employee model

Build employee groups and Assistant connections from company configuration.

The baseline is:

```text
All-Employees → General Assistant → Hermes `general` Profile
AI-Admins     → administrative access according to company policy
```

The Hermes default/admin Profile is not an employee Assistant.

Specialist groups and Assistant resources are added only when the adopting company enables the matching specialist Profile.

## Validated local deployment pattern

The tested manifest is [`docker-compose.yml`](docker-compose.yml).

The first validated local demo used:

- Open WebUI `v0.11.3`;
- persistent named volume `open-webui-data`;
- loopback-only host publication;
- Docker host alias `host.docker.internal` so the container could reach host-native Hermes;
- server-side Hermes Profile connections, keeping Profile API keys out of the browser.

The exact demo runtime evidence, users, specialist Profiles, URLs, and ACL results are recorded in `state/DEPLOYMENT-STATE.md` rather than treated as generic provisioning defaults.

## Authentication posture

For the baseline:

1. provision the first administrator;
2. create ordinary employee identities according to company policy;
3. disable open self-signup after provisioning unless the company explicitly wants it;
4. keep provider/API credentials server-side;
5. restrict administration to authorized administrators.

## Ordinary employee permissions

The validated Open WebUI baseline uses native permissions rather than source changes, CSS hiding, or a proxy.

```text
Normal chat              enabled
Conversation history     enabled
File upload              enabled unless company policy disables it
Chat System Prompt       disabled
Advanced Chat Parameters disabled
```

Use the current upstream-supported administrator permission controls for the installed version.

## Hermes connections

Create one server-side OpenAI-compatible resource/connection for each employee-facing Hermes Profile that is actually enabled.

Baseline:

```text
General Assistant → Hermes `general` Profile
```

Requirements:

- use the supported Profile API route for the installed Hermes version;
- keep API credentials server-side;
- do not create an employee connection to the privileged default/admin Profile;
- apply resource ACLs so only intended groups can use each Assistant;
- test direct unauthorized access, not only UI visibility.

If specialist Profiles are enabled, each gets its own connection and group mapping from company configuration.

## Memory scoping

Open WebUI conversation history is separate from Hermes long-term memory.

Employee Hermes long-term memory is disabled by default until a stable user-derived Open WebUI → Hermes session/memory isolation mechanism passes the cross-user test in `docs/ACCEPTANCE-TESTS.md`.

Do not enable shared employee Profile memory based only on prompt instructions.

## File handling

File upload may be enabled for employee conversation context when supported and allowed by company policy.

Do not assume every Open WebUI attachment mode maps identically to Hermes. Test the file types the company actually intends to use.

Official durable company knowledge ingestion belongs in WeKnora.

## Employee-client validation

Core Ready requires testing from the real employee UI:

- ordinary employee login;
- permitted Assistant visibility;
- normal chat;
- grounded WeKnora answer;
- readable source evidence;
- follow-up context;
- history after refresh/re-login;
- file upload when enabled;
- default/admin non-exposure;
- absence of employee admin/provider/API-key controls;
- unauthorized direct access fails closed.

Backend health alone is not sufficient.

## License note

Open WebUI uses its own upstream license rather than this repository's Apache-2.0 license. Review `THIRD_PARTY_NOTICES.md` and the exact upstream license for the deployed version, especially before rebranding or larger deployments.
