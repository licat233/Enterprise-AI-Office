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

## Reporting

Do not put exploitable secret material into a public GitHub issue. Repository maintainers should use an appropriate private disclosure channel for sensitive reports.

The public repository intentionally contains sanitized architecture and deployment evidence only.
