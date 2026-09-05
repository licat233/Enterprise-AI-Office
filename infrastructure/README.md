# Infrastructure

This directory contains reusable deployment adapters, examples, and implementation notes for the selected Enterprise AI Office components.

The repository intentionally does **not** vendor entire upstream projects.

## Component directories

```text
infrastructure/
├── weknora/
├── open-webui/
└── hermes/
```

## Upstream-version rule

Infrastructure files must be written against a known tested upstream release.

Do not copy configuration from an old blog post and assume it still matches current WeKnora/Hermes/Open WebUI.

Before creating or updating deployment manifests:

1. identify the target upstream version;
2. read its official deployment documentation;
3. inspect the official example configuration/Compose files;
4. use the smallest override necessary for Enterprise AI Office;
5. record the tested version in `state/DEPLOYMENT-STATE.md`.

## Why not vendor upstream Compose files permanently?

WeKnora and Open WebUI evolve independently. Copying their full upstream deployment definitions into this repository too early creates a stale fork that future AI agents may mistakenly treat as authoritative.

Preferred pattern:

```text
pinned upstream release
+
Enterprise AI Office configuration/override
+
recorded deployment state
```

## Secrets

Infrastructure examples must use placeholders only.

Never commit production `.env` files or credentials.

## Port/network rules

Do not publish internal databases/queues merely because an upstream Compose example exposes them for development.

Production exposure must follow `docs/SECURITY.md`.

## Future files

As the ARMOR reference deployment is implemented and validated, this directory may gain:

- tested Compose overrides;
- environment templates;
- service startup examples;
- reverse-proxy/private-access examples when justified;
- version-specific compatibility notes.

Only promote an implementation artifact into the generic project after it has been validated and is reasonably reusable.
