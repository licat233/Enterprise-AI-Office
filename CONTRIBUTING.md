# Contributing to Enterprise AI Office

Enterprise AI Office is intended to become a reusable, AI-agent-readable enterprise AI deployment and operating standard.

Contributions are welcome when they improve real deployability, safety, maintainability, or reuse.

## Read first

Before proposing a material change, read:

1. `README.md`
2. `AGENTS.md`
3. `docs/ARCHITECTURE.md`
4. the documentation for the area you want to change.

## Good contributions

Examples:

- fixes to outdated upstream integration details;
- tested deployment adapters for a pinned release;
- reusable Profile/SOUL/Skill patterns validated in a real organization;
- safer RBAC/memory/tool isolation patterns;
- health/backup/restore improvements;
- acceptance-test automation;
- documented real-world failure modes and their minimal fixes;
- portability improvements that preserve the architecture boundaries.

## Contributions that need stronger justification

Major new components such as another agent framework, workflow engine, vector database, model gateway, auth proxy, or synchronization service must pass the Architecture Change Gate in `AGENTS.md`.

A feature being popular is not enough.

## Do not submit secrets or private company data

Never include:

- API keys;
- passwords;
- tokens;
- private keys;
- employee personal data;
- customer secrets;
- private contracts;
- production `.env` files;
- sensitive network details.

Use placeholders and sanitized examples.

## Generic vs company-specific

A reusable improvement belongs in generic docs/templates.

A company-specific implementation belongs under a sanitized `reference/` example or the company's own private deployment repository.

Do not make ARMOR-specific values universal defaults unless the underlying lesson is genuinely reusable.

## Upstream-first

Before adding custom code, check whether the relevant upstream project already provides the capability.

Preferred order:

```text
upstream capability
→ official extension/integration
→ configuration
→ thin adapter
→ custom infrastructure
```

## Documentation changes

If a code/config change affects architecture, security, deployment, backup, RBAC, Profile behavior, or upgrade procedures, update the corresponding docs in the same contribution.

## Testing

For implementation changes, document what was actually tested.

Use `docs/ACCEPTANCE-TESTS.md` as the baseline for production-impacting changes.

Do not claim a test passed if it was not run.

## Licensing

By contributing original material to this repository, you agree that your contribution may be distributed under the repository's Apache License 2.0 unless clearly stated otherwise for an independently licensed third-party artifact.

Do not copy third-party code/content into the repository without checking its license and attribution requirements.

See `THIRD_PARTY_NOTICES.md`.
