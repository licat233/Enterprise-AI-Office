# Contributing to Enterprise AI Office

Enterprise AI Office is intended to be a reusable, AI-agent-readable and AI-agent-executable enterprise AI deployment/operating standard.

Contributions are welcome when they improve real deployability, safety, maintainability, or reuse.

## Read first

Before a material change, read:

1. `README.md`
2. `AGENTS.md`
3. `DEPLOY.md`
4. `docs/COMPLETENESS.md`
5. `config/capabilities.yaml` when the change affects a deployable capability
6. `docs/ARCHITECTURE.md`
7. the standards/adapters for the area being changed.

## Preserve capability closure

A capability is not complete because documentation mentions it.

If a contribution adds or materially changes a deployable capability, keep this chain closed:

```text
company configuration selector
→ config/capabilities.yaml
→ implementation adapter/playbook
→ required protected inputs/security boundary
→ acceptance test
→ deployment-state fields
```

Do not add a capability selector that has no implementation/acceptance path.

Do not remove or rename an implementation artifact without updating the registry and dependent documentation.

Run the static check after relevant changes:

```sh
sh scripts/repository-readiness-check.sh
```

A static PASS does not replace runtime acceptance.

## Good contributions

Examples:

- fixes to outdated upstream integration details;
- tested deployment adapters for pinned releases;
- clearer capability playbooks that reduce deployment-agent guessing;
- reusable Profile/SOUL/Skill patterns validated in real work;
- safer RBAC/memory/tool isolation;
- health/backup/restore improvements;
- acceptance-test automation;
- minimal fixes derived from real failure modes;
- portability improvements preserving architecture boundaries.

## Changes needing stronger justification

Major new components such as another agent framework, workflow engine, vector database, model gateway, auth proxy, or synchronization service must pass the architecture-change criteria in `AGENTS.md`.

A feature being popular is not enough.

Before adding another service, first verify that WeKnora, Hermes, Open WebUI, or their supported extension/configuration mechanisms cannot solve the actual requirement.

## No feature collection

Repository templates/playbooks form a capability library; they do not imply every deployment should instantiate them.

Generic company defaults should remain small. New optional examples must not silently become default Profiles, groups, Knowledge Bases, integrations, or services.

## No secrets/private company data

Never include:

- API keys/passwords/tokens;
- private keys;
- employee personal data;
- customer secrets;
- private contracts;
- production `.env` files;
- sensitive network details.

Use placeholders and sanitized examples.

## Generic vs company-specific

Reusable improvements belong in generic standards/adapters.

Company-specific organization, roles, values, and operational evidence belong under sanitized `reference/` material or the company's private deployment configuration/state.

Reference material is non-normative and must not override the generic execution contract.

## Upstream first

Before custom implementation, check the exact selected upstream release.

Preferred order:

```text
upstream capability
→ official integration/extension
→ configuration
→ thin adapter/playbook
→ custom infrastructure only when necessary
```

Avoid permanent forks of upstream projects for configuration-level needs.

## Clean-state documentation

Normative documentation should describe the intended current design cleanly.

Do not turn each past correction into a permanent list of special prohibitions or historical commentary. Preserve history in Git/deployment changelogs when history is operationally useful.

## Documentation synchronization

If a code/config change affects architecture, readiness semantics, capability closure, security, deployment, backup, RBAC, Profile behavior, network exposure, or upgrade procedures, update the corresponding docs/registry in the same contribution.

## Testing and evidence

Document what was actually tested.

Use `docs/ACCEPTANCE-TESTS.md` according to the capability/readiness level affected.

Do not claim:

- runtime acceptance from a static config review;
- Configured Ready while an enabled capability remains untested;
- Production Ready without applicable recovery/security/operations evidence.

## Licensing

By contributing original material, you agree it may be distributed under this repository's Apache License 2.0 unless clearly stated otherwise for independently licensed third-party material.

Do not copy third-party code/content without checking its license/attribution requirements. See `THIRD_PARTY_NOTICES.md`.
