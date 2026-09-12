---
name: Bug / reproduction failure
about: Report a broken contract, deployment failure, regression, or Fresh-Agent reproducibility problem
title: "[Bug] "
---

> Do not put passwords, API keys, bearer tokens, private mailbox data, real employee identifiers, private host/network identity, or exploit payloads here. Security vulnerabilities must follow SECURITY.md instead of a public issue.

## What failed

Describe the observable failure. Prefer exact error text and the smallest reproducible path.

## Affected contract / path

Examples:

- DEPLOY.md phase/section
- REPRODUCE.md stage
- config/capabilities.yaml capability
- infrastructure/<component>/PROVISIONING.md
- scripts/<check>.*
- Open WebUI → Hermes → WeKnora employee path

## Repository baseline

- EAO commit:
- validated-stack baseline:
- host/runtime family, if relevant:
- requested readiness level:

Do not report only a moving branch name such as `main`; include the exact commit used for the reproduction.

## Steps to reproduce

1.
2.
3.

## Expected result

What should have happened according to the repository contract?

## Actual result / evidence

Include non-secret logs, command output, failing CI run/job, screenshots, or acceptance evidence.

## Existing deployment or fresh reproduction?

- [ ] Fresh/isolated target
- [ ] Existing deployment

If existing, state what was inspected before mutation and whether rollback material exists.

## Authority / privacy boundary

Confirm whether this issue touches any of the following:

- [ ] company knowledge authority
- [ ] employee RBAC/Profile boundary
- [ ] secrets/credentials
- [ ] network exposure
- [ ] external side effects such as Email
- [ ] backup/restore or deployment state
- [ ] none of the above

## Regression check

If you know the last passing commit/version, record it here.
