# hermes-webui Deployment Playbook

`hermes-webui` is an optional administrative Web surface for Hermes Agent. It is not the ordinary employee portal; Open WebUI remains the employee-facing multi-user client.

Enable this playbook only when `capabilities.hermes_webui.enabled: true` in the company configuration.

## Upstream

Repository:

```text
nesquena/hermes-webui
```

The upstream project is independently licensed under MIT. Do not vendor or fork it into Enterprise AI Office by default.

Because hermes-webui was not part of the first validated Core Ready deployment, its exact commit is deployment-specific until a compatible version is validated and recorded. Resolve an upstream version/commit deliberately, pin it, and write it to `state/DEPLOYMENT-STATE.md`. Do not deploy floating `master` as a production version.

## Deployment shape

For the validated macOS-style architecture, prefer host-native hermes-webui beside the host-native Hermes installation so it can use the same intended `HERMES_HOME` without copying Hermes state into another authority.

Upstream's supported bootstrap path is:

```bash
git clone https://github.com/nesquena/hermes-webui.git <runtime-dir>/hermes-webui
cd <runtime-dir>/hermes-webui
git checkout <PINNED_COMMIT>
python3 bootstrap.py --no-browser
```

For an always-on installation, upstream also provides `ctl.sh` lifecycle management:

```bash
./ctl.sh start
./ctl.sh status
./ctl.sh logs --lines 100
./ctl.sh restart
./ctl.sh stop
```

Use the exact commands supported by the selected pinned commit; inspect its README/onboarding checklist before execution.

## Access boundary

Safe default:

```text
HERMES_WEBUI_HOST=127.0.0.1
HERMES_WEBUI_PORT=8787
```

Keep it loopback-only unless the company configuration explicitly enables remote administrative access.

If it binds beyond loopback, configure a strong `HERMES_WEBUI_PASSWORD` and place access behind the approved private/identity-aware layer described by `infrastructure/access/README.md`.

Do not expose hermes-webui as the employee chat client. It provides powerful controls over Hermes sessions, Profiles, workspace files, tools, and configuration.

## State and authority

hermes-webui should use the intended Hermes installation/state rather than creating a parallel source of truth.

Record:

- `HERMES_HOME` used;
- WebUI state directory if customized;
- bind host/port;
- authentication/access method;
- pinned upstream commit/version.

Include its state in production backup only when the selected deployment actually relies on that state for operations.

## Required inputs

Before enabling beyond loopback, resolve:

- admin access method;
- password or identity-aware access policy;
- intended network exposure;
- exact upstream commit/version.

These are genuine configuration/security inputs. The deployment agent must not invent a public exposure policy.

## Acceptance

When enabled, do not mark the capability complete until all applicable checks pass:

```text
[ ] selected upstream commit/version is pinned and recorded
[ ] service starts and health/status succeeds
[ ] intended Hermes installation/Profile state is visible
[ ] ordinary employees have no access to the admin surface
[ ] loopback/private-access boundary matches company configuration
[ ] authentication is enforced whenever the surface is reachable outside loopback
[ ] restart procedure is documented or managed by the selected service mechanism
```

Record the result in `state/DEPLOYMENT-STATE.md`.
