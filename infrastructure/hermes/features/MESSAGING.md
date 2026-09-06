# Hermes Messaging Execution Path

This is the version-bound execution companion to `infrastructure/hermes/features/README.md` for the first validated Hermes baseline:

```text
NousResearch/hermes-agent 0.21.0
commit f1ccf436a27522c1bb5d36383a6f13b950676338
```

Use it only when `capabilities.messaging.enabled: true`. The company configuration selects one real platform; do not enable every supported platform for completeness.

## 1. Native execution path

Hermes 0.21.0 provides the native messaging setup wizard:

```bash
hermes gateway setup
```

Use that supported path before hand-editing a platform configuration from memory. It can create/collect credentials for supported platforms and guide access control.

Start/restart the Gateway through the deployment's normal managed Hermes lifecycle after configuration. For direct foreground verification, the pinned platform guides use:

```bash
hermes gateway
```

Do not add a second messaging gateway/service when Hermes' native adapter satisfies the company requirement.

## 2. Protected inputs and authorization

Resolve before enabling a platform:

```text
selected platform
real enterprise/bot/account authorization
platform credentials or QR authorization
allowed users/chats or pairing/enterprise identity policy
Profile routing
delivery/home-channel policy when required
```

Credentials belong in the intended Hermes protected environment/state, not Git.

Production baseline:

```text
explicit allowlist / pairing / enterprise identity
not allow-all
```

Hermes uses platform-specific `*_ALLOWED_USERS` and `*_ALLOW_ALL_USERS` authorization controls. Do not enable an `*_ALLOW_ALL_USERS=true` shortcut merely to pass setup.

## 3. Feishu / Lark — validated 0.21.0 path

Preferred transport on a workstation/private server is the upstream WebSocket/long-connection path, so no public webhook is required.

Run:

```bash
hermes gateway setup
```

Select **Feishu / Lark**. The pinned upstream supports QR-assisted app creation or manual App ID/App Secret entry.

Native environment variables include:

```text
FEISHU_APP_ID=<protected>
FEISHU_APP_SECRET=<protected>
FEISHU_DOMAIN=feishu|lark
FEISHU_CONNECTION_MODE=websocket
FEISHU_ALLOWED_USERS=<comma-separated approved Open IDs>
FEISHU_HOME_CHANNEL=<optional chat ID>
```

If webhook mode is deliberately selected, also follow the pinned upstream webhook security controls (`FEISHU_ENCRYPT_KEY`, `FEISHU_VERIFICATION_TOKEN`, host/port/path) and the company-approved remote access boundary. Do not choose webhook mode merely because it exists.

For production, keep Feishu DM/group access constrained to the configured identities. The company must authorize the actual Feishu/Lark app and permissions; the deployment agent must not invent that enterprise authority.

## 4. WeCom — validated 0.21.0 path

Hermes 0.21.0 supports the WeCom AI Bot WebSocket gateway and does not require a public webhook for this path.

Run:

```bash
hermes gateway setup
```

Select **WeCom**. The wizard supports QR-assisted bot creation or manual credentials.

Native environment variables include:

```text
WECOM_BOT_ID=<protected>
WECOM_SECRET=<protected>
WECOM_ALLOWED_USERS=<comma-separated approved user IDs>
WECOM_HOME_CHANNEL=<optional chat ID>
WECOM_DM_POLICY=allowlist
WECOM_GROUP_POLICY=allowlist|disabled
```

Use `allowlist`/`disabled` according to company configuration. Do not keep the upstream-open DM/group behavior as an accidental production authorization policy.

If group messaging is enabled, configure the approved group IDs and, where required, per-group sender allowlists using the pinned Hermes configuration model.

## 5. Weixin / personal WeChat — validated 0.21.0 path

This adapter uses Tencent's iLink bot identity. It is not the WeCom enterprise adapter.

Run:

```bash
hermes gateway setup
```

Select **Weixin** and complete the QR authorization. Hermes stores the iLink account material under its supported state path (`~/.hermes/weixin/accounts/` in the standard upstream home convention).

Native configuration includes:

```text
WEIXIN_ACCOUNT_ID=<authorized iLink bot account ID>
WEIXIN_TOKEN=<protected; normally saved by setup>
WEIXIN_DM_POLICY=allowlist
WEIXIN_ALLOWED_USERS=<comma-separated approved sender IDs>
WEIXIN_HOME_CHANNEL=<optional chat ID>
```

For the validated upstream, `WEIXIN_GROUP_POLICY=disabled` is the safe/default baseline and ordinary WeChat group delivery may not be available for iLink bot identities. Do not promise group-message support when the platform does not deliver those events.

## 6. Another Hermes-supported platform

If company configuration selects another platform supported by the pinned Hermes release:

1. run `hermes gateway setup` under the actual Hermes service/Profile context;
2. select only that configured platform;
3. use the wizard's native credential/config path;
4. keep platform authorization on allowlist/pairing/enterprise identity rather than allow-all;
5. inspect the resulting supported Hermes configuration/state rather than inventing variable names;
6. record the exact platform settings used (excluding secrets);
7. run the same authorized/unauthorized acceptance below.

If the selected platform is not supported by the pinned release, report:

```text
BLOCKED — SELECTED HERMES RELEASE DOES NOT SUPPORT CONFIGURED MESSAGING PLATFORM
```

Do not silently install a second messaging framework or upgrade Hermes as part of ordinary provisioning.

## 7. Profile routing

Messaging is an employee access/delivery surface, not authorization to switch Profiles.

Required path:

```text
authenticated/allowed platform identity
→ configured messaging route
→ intended Hermes employee Profile
```

Keep default/admin unreachable through ordinary employee messaging. When multiple Profiles exist, routing must come from trusted configuration/authenticated platform context, not arbitrary message text.

## 8. Idempotent reconciliation

On rerun:

```text
read selected platform from company config
→ inspect current Hermes gateway configuration/state
→ preserve unrelated approved platform state
→ update only configured platform credentials/policy/routing
→ restart managed Gateway when required
→ test authorized identity
→ test unauthorized identity
→ test configured delivery/home channel when used
→ record result
```

Do not run setup for disabled platforms and do not reset a working platform credential unless the protected input explicitly requests rotation.

## 9. Acceptance

PASS requires:

```text
[ ] exact Hermes version/commit recorded
[ ] only company-configured messaging platform enabled for this capability
[ ] native Hermes setup/configuration path used
[ ] real platform credential/account authorization succeeds
[ ] explicit allowlist/pairing/enterprise identity policy configured
[ ] no production allow-all shortcut enabled
[ ] authorized identity reaches the intended Profile
[ ] unauthorized identity fails closed
[ ] default/admin Profile cannot be selected by ordinary messaging
[ ] deterministic Profile routing verified
[ ] configured file/media behavior works when enabled
[ ] configured automation/home-channel delivery works when enabled
[ ] credentials remain outside Git/log output
[ ] actual platform/routing/acceptance state recorded
```

This acceptance supplements the `Messaging` section in `docs/ACCEPTANCE-TESTS.md`.