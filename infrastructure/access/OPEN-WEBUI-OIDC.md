# Open WebUI OIDC Execution Path

This is the version-bound execution companion to `infrastructure/access/README.md` for the first validated Open WebUI core baseline:

```text
open-webui/open-webui v0.11.3
commit 2a960a59fe1dbbd35282f0556b3666d81102e781
```

Use this file only when `capabilities.sso.enabled: true` and the company selected OIDC/enterprise identity for Open WebUI. For another Open WebUI release, re-verify these settings against that exact release before deployment.

## 1. Required company/IdP input

Resolve from the active company configuration and protected identity-provider setup:

```text
OIDC discovery URL / issuer metadata
client ID
client secret, or the approved PKCE/client auth mode
redirect URI
allowed email domains/users
IdP group/role claim names
mapping from enterprise groups/roles to Open WebUI authorization
admin / break-glass policy
```

If the IdP application has not been authorized or any required credential/metadata is missing:

```text
BLOCKED — REQUIRED INPUT: <specific identity-provider input>
```

Do not invent an IdP, callback URL, group claim, or privilege mapping.

## 2. Native v0.11.3 OIDC variables

The pinned Open WebUI source reads the following generic OIDC settings directly:

```text
OAUTH_CLIENT_ID
OAUTH_CLIENT_SECRET
OPENID_PROVIDER_URL
OPENID_REDIRECT_URI
```

It also supports claim/policy controls including:

```text
OAUTH_EMAIL_CLAIM
OAUTH_GROUPS_CLAIM
ENABLE_OAUTH_GROUP_MANAGEMENT
ENABLE_OAUTH_GROUP_CREATION
ENABLE_OAUTH_ROLE_MANAGEMENT
OAUTH_ROLES_CLAIM
OAUTH_ALLOWED_ROLES
OAUTH_ADMIN_ROLES
OAUTH_ALLOWED_DOMAINS
```

The exact values are company/IdP-specific. Do not copy placeholder claim names into production without verifying the IdP token.

The repository's `config/.env.example` already includes the core protected OIDC variables. Add only the additional claim/mapping variables actually required by the selected identity design.

## 3. Configure the container

For the normal container deployment, inject the selected native variables through the protected Open WebUI runtime environment/Compose override rather than editing Open WebUI's database directly.

Minimum generic client configuration:

```text
OPENID_PROVIDER_URL=<OIDC_DISCOVERY_URL>
OAUTH_CLIENT_ID=<PROTECTED_CLIENT_ID>
OAUTH_CLIENT_SECRET=<PROTECTED_CLIENT_SECRET>
OPENID_REDIRECT_URI=<AUTHORIZED_CALLBACK_URL>
```

For domain restriction, never rely on the v0.11.3 default `*` in production when the company configuration declares an allow-list. Set:

```text
OAUTH_ALLOWED_DOMAINS=<COMMA_SEPARATED_APPROVED_DOMAINS>
```

Restart/recreate only the Open WebUI service through the deployment's normal Compose lifecycle and verify health before login testing.

## 4. Group and role mapping

SSO authentication does not by itself grant an Assistant.

The Enterprise AI Office authorization path remains:

```text
IdP identity
→ Open WebUI user
→ Open WebUI group
→ Model/Assistant read grant
→ Hermes Profile
```

If the company configuration explicitly maps IdP groups into Open WebUI groups, enable native group management only after confirming the actual token claim:

```text
ENABLE_OAUTH_GROUP_MANAGEMENT=true
OAUTH_GROUPS_CLAIM=<VERIFIED_IDP_GROUP_CLAIM>
```

Do not enable automatic group creation unless company policy explicitly permits IdP groups to create Open WebUI groups:

```text
ENABLE_OAUTH_GROUP_CREATION=false
```

is the safer baseline.

When role mapping is required, configure `ENABLE_OAUTH_ROLE_MANAGEMENT`, `OAUTH_ROLES_CLAIM`, `OAUTH_ALLOWED_ROLES`, and `OAUTH_ADMIN_ROLES` from an explicit company policy. Never map a broad/default IdP role to Open WebUI admin by convenience.

If native claim mapping cannot express the required company policy safely, keep authentication in OIDC and use the controlled Open WebUI provisioning path in `infrastructure/open-webui/PROVISIONING.md` for group/resource assignment. Do not add a custom auth proxy unless a real requirement remains unsatisfied.

## 5. Reconciliation

On rerun:

1. read the active company SSO configuration;
2. inspect the current protected Open WebUI environment/Compose override;
3. preserve unrelated approved Open WebUI settings;
4. update only the selected OIDC/mapping variables;
5. restart the service;
6. test with an authorized identity;
7. test with an unauthorized domain/user;
8. inspect the resulting Open WebUI group membership and Assistant visibility;
9. verify the admin/break-glass path separately.

Do not treat a successful IdP redirect as completed SSO provisioning.

## 6. Acceptance

PASS requires:

```text
[ ] exact Open WebUI version/commit recorded
[ ] configured discovery URL and callback match the authorized IdP application
[ ] authorized enterprise identity signs in
[ ] unauthorized domain/user is rejected
[ ] expected email/group/role claims were observed and mapped deliberately
[ ] intended Open WebUI group membership results
[ ] intended Assistant/model grants result
[ ] ordinary enterprise identity cannot reach admin-only resources
[ ] arbitrary user-controlled text/claims cannot select a privileged Hermes Profile
[ ] admin/break-glass policy works as documented
[ ] logout/session behavior is acceptable for the selected IdP
[ ] OIDC client secret remains outside Git and logs
```

Record provider identity, non-secret discovery/callback metadata, group/role policy, and acceptance result in deployment state.