# Open WebUI Deployment Adapter

Open WebUI is the default employee-facing multi-user Web client for Enterprise AI Office. The validated local demo uses the pinned image `ghcr.io/open-webui/open-webui:v0.11.3` and publishes it only on `127.0.0.1:3000`.

## Responsibilities

Open WebUI owns:

- human user accounts and authentication;
- groups;
- employee-facing chat UX;
- authorized assistant/resource visibility;
- conversation history.

It does **not** own Hermes Profile definitions or WeKnora company knowledge.

## Local demo deployment

The tested manifest is [docker-compose.yml](docker-compose.yml). It is a reference/demo adapter, not a permanently fixed upstream deployment. In the validated setup it was copied to `$EAIO_RUNTIME_DIR/open-webui/docker-compose.yml` and started as an independent Compose project, separate from WeKnora. It uses the persistent named volume `open-webui-data` and the Docker host alias `host.docker.internal` so the container can reach the host-native Hermes Gateway.

```text
Open WebUI: http://127.0.0.1:3000
Hermes employee API: http://host.docker.internal:8642/p/<profile>/v1
```

The admin account and demo-user credentials are stored in protected files under `$EAIO_RUNTIME_DIR/credentials/`; values must not be committed or printed.
Self-signup is disabled after provisioning; the login form remains enabled for the known demo accounts.

## RBAC posture

Global/default user permissions are minimal. The validated demo contains these groups and model ACLs:

```text
All-Employees → General Assistant → Hermes general Profile
Sales         → Sales Assistant   → Hermes sales Profile
QC            → QC Assistant      → Hermes qc Profile
```

`sales-test-a` and `sales-test-b` belong to `All-Employees` and `Sales`. `qc-test` belongs to `All-Employees` and `QC`. The employee `/api/v1/models` route was verified to expose `general,sales` to Sales users and `general,qc` to the QC user. The Hermes default/admin Profile has no Open WebUI employee connection.

## Hermes connections

Create server-side OpenAI-compatible connections/resources for employee-facing Hermes Profiles using the supported profile routes. Use a distinct Profile API key for each connection:

```text
General Assistant → http://host.docker.internal:8642/p/general/v1
Sales Assistant   → http://host.docker.internal:8642/p/sales/v1
QC Assistant      → http://host.docker.internal:8642/p/qc/v1
```

The local demo restricts each employee Profile to seven read-only WeKnora retrieval tools. The unique per-Profile MCP names are intentional for Hermes v0.21.0 multiplex registration. Do not create an ordinary employee connection to the privileged Hermes default/admin Profile.

## Memory scoping

Employee long-term memory is disabled in the validated demo (`memory: false` and `user_profile: false` in each employee Profile). The current Open WebUI connection path does not provide a validated user-derived Hermes session-header mapping, so enabling shared Profile memory would not meet the isolation requirement. Conversation history remains user-scoped in Open WebUI.

Do not enable employee long-term memory until the cross-user isolation test in `docs/ACCEPTANCE-TESTS.md` passes with the exact deployed versions and connection behavior.

## File handling

Do not assume all Open WebUI file upload features map cleanly to Hermes API input formats. Test supported file/image workflows explicitly before enabling them for employees. Official company knowledge ingestion belongs in WeKnora.

## Validation

The local demo passed sign-in, group/model ACL, direct unauthorized chat probes (`400 Model not found`), direct Profile API-key isolation, least-privilege terminal probes, and grounded chat through Open WebUI. Run all authentication, group/resource ACL, direct unauthorized-access, and cross-user memory tests in `docs/ACCEPTANCE-TESTS.md` before employee rollout.

## Employee-client validation

Observed on 2026-09-06 from the pinned Open WebUI employee UI:

- `sales-test-a` and `sales-test-b` authenticated and exposed only `General Assistant` and `Sales Assistant`; `qc-test` exposed only `General Assistant` and `Quality Control Assistant`.
- General, Sales, and QC conversations completed grounded WeKnora queries. The UI showed source titles and knowledge-base names inline; attachment responses also exposed a human-readable `View source` entry.
- Sales responses were customer-oriented and refused unsupported shelf-lighting and delivery claims. QC responses separated available demo workflow guidance from missing approved specifications and placed the inspection checklist on hold pending evidence.
- A five-turn Sales conversation survived refresh and logout/login. Employee long-term memory and user profiles remained disabled.
- A small temporary text attachment was read in the current conversation and explicitly treated as attachment context rather than durable company knowledge. Official knowledge remains a WeKnora ingestion concern.
- Open WebUI direct unauthorized model requests returned HTTP 400 `Model not found` for cross-department and default/admin model names. The employee settings page exposes user-level system-prompt and advanced-parameter controls; it does not expose provider credentials or administration.
- Sales/QC terminal requests returned a human-readable unavailable-capability response and no tool call, but the exact `NO_TERMINAL_TOOL` marker was not observed in this run. Keep the backend least-privilege checks and treat the marker mismatch as a validation limitation, not as evidence of terminal access.
- One grounded Sales answer surfaced local demo endpoint details because those details are present in the synthetic Products & Technical document. Do not use that corpus as production employee knowledge without sanitizing or replacing the demo material.

## License note

Open WebUI uses its own upstream license rather than this repository's Apache-2.0 license. Review `THIRD_PARTY_NOTICES.md` and the exact upstream license for the deployed version, especially before rebranding or large deployments.
