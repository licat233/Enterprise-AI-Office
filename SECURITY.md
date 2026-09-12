# Security Policy

Enterprise AI Office is designed around least privilege, explicit authority boundaries, and reproducible deployment evidence.

For the system security model, read [docs/SECURITY.md](docs/SECURITY.md).

## Do not publish secrets

Never commit or include in public issues or pull requests:

- API keys, OAuth tokens, passwords, session cookies, or bearer tokens;
- mailbox credentials;
- real employee credentials or personal identifiers;
- private company configuration;
- private network/device identity material;
- protected deployment snapshots containing secrets.

Use the symbolic/private-input contracts in `config/` instead.

## Security-sensitive changes

Changes that expand employee permissions, external side effects, network exposure, credential scope, or a source-of-truth boundary must:

1. run the [Capability Reuse Pass](docs/CAPABILITY-REUSE-PASS.md);
2. document the authority/security impact;
3. preserve a rollback path;
4. add observable acceptance evidence;
5. avoid silently broadening a frozen baseline.

## Supported project state

Enterprise AI Office has not declared `RELEASE READY`. Security fixes and
security-contract corrections therefore target the current canonical `main`
branch and the validated baseline referenced by the repository authority files.

Historical frozen commits, migration reports, and sanitized deployment snapshots
are evidence. Do not rewrite them in place merely to make old evidence look
current; fix the active contracts and clearly record any superseding guidance.

## Reporting

Do not publish exploit details, credentials, private runtime identifiers, or
proof-of-concept material in a public GitHub issue or pull request.

Preferred path:

1. Open the repository's **Security** tab.
2. If **Report a vulnerability** is available, use that private GitHub reporting
   flow.
3. If that option is not available, contact the repository maintainer through an
   already-established private channel and request a private security thread.
4. If no private channel is available, a minimal public issue may request
   security contact **without** vulnerability details, secrets, affected private
   identifiers, or exploit reproduction steps.

A public issue is not an acceptable place for the vulnerability payload itself.

When reporting, include privately when applicable:

- affected repository commit/version;
- affected capability/component;
- security boundary that failed;
- minimal reproduction;
- observed versus expected behavior;
- whether any credential or private data may have been exposed;
- suggested containment/rollback if known.

The public repository intentionally contains sanitized architecture and
deployment evidence only.
