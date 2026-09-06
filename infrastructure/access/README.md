# Access and Enterprise Identity Playbook

This playbook covers two optional boundaries:

- remote/private browser access;
- employee SSO / enterprise identity.

Neither is required for a local/LAN Core Ready deployment. Enable only when selected by company configuration.

## 1. Remote/private browser access

When `capabilities.remote_access.enabled: true`, the company configuration must select one access method rather than asking the deployment agent to stack several products.

Typical supported patterns include:

```text
private LAN only
VPN / Tailscale-style private network
identity-aware reverse proxy / access gateway
company-approved equivalent
```

The repository does not prescribe one vendor for every company.

### Surface classification

Treat surfaces differently:

```text
Employee surface
  Open WebUI

Administrative surfaces
  hermes-webui (when enabled)
  WeKnora admin UI
  Open WebUI admin
  host/Docker/Hermes CLI

Internal-only services
  PostgreSQL
  Redis
  DocReader/parser/internal workers
  raw privileged Hermes routes
```

Remote employee access does not imply remote exposure of every administrative or internal service.

### Deployment contract

For the selected access method:

1. keep the application service bound as narrowly as practical;
2. place the approved private/identity-aware access layer in front when required;
3. configure TLS/identity policy appropriate to that layer;
4. expose only the surfaces declared by company configuration;
5. keep databases/cache/internal services private;
6. verify an authorized and unauthorized access attempt;
7. record the actual public/private endpoint boundary without recording secrets.

Do not use an unauthenticated public tunnel as the production employee access design.

## 2. SSO / enterprise identity

When `capabilities.sso.enabled: true`, the company configuration must provide or name the real identity provider and the intended claim/group policy.

Open WebUI versions may support OAuth/OIDC and other identity integrations. Use the selected pinned Open WebUI release's native supported mechanism before adding a custom authentication proxy or fork.

The deployment agent must inspect the exact release documentation/configuration before writing identity settings; provider-specific endpoints, claims, and callback URLs are not universal defaults.

### Required identity inputs

Resolve:

```text
identity provider
tenant/issuer/discovery metadata
client ID
client secret or other approved client credential
redirect/callback URL
allowed domain/user policy
group/claim mapping
initial admin / break-glass policy
```

Secrets stay outside Git.

If the company asks for SSO but does not identify the provider or authorize the required identity application, report `BLOCKED — REQUIRED INPUT` rather than inventing one.

### Group mapping

SSO authenticates a human identity; it does not replace the Enterprise AI Office authorization model.

The effective path remains:

```text
enterprise identity
→ Open WebUI user/group membership
→ authorized Assistant
→ Hermes Profile
```

Where native group/claim synchronization is supported and validated, map only the required groups. Otherwise use a controlled provisioning process. Do not automatically map every IdP group into AI permissions.

### Local fallback / break-glass

If production policy requires a local emergency administrator, document how it is protected and when it may be used. Do not leave a weak local admin password merely because SSO exists.

## 3. Administrative WebUI remote access

If hermes-webui is enabled remotely:

- require its supported password/authentication control;
- keep it behind a stricter private access boundary than the employee portal;
- do not reuse employee-facing credentials as administrative credentials.

## 4. Acceptance

### Remote access

```text
[ ] intended employee endpoint reachable through approved access layer
[ ] unauthorized/untrusted access is rejected
[ ] admin surfaces are restricted according to policy
[ ] database/cache/internal service ports remain unreachable externally
[ ] TLS/identity boundary is documented
```

### SSO

```text
[ ] authorized enterprise user can sign in
[ ] unauthorized user/domain cannot sign in
[ ] intended groups/Assistant access are correct after login
[ ] privilege does not follow arbitrary user-controlled claims/text
[ ] admin/break-glass access policy works as designed
[ ] logout/session behavior is acceptable
```

Record the access method, identity provider, group-mapping policy, and acceptance result in `state/DEPLOYMENT-STATE.md`.
