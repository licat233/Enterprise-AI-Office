## Purpose

Describe the concrete Enterprise AI Office requirement this change addresses.

## Capability Reuse Pass

- [ ] I checked existing EAO capabilities and scripts.
- [ ] I checked relevant Hermes native capabilities.
- [ ] I checked installed/frozen Skills.
- [ ] I checked relevant Open WebUI / WeKnora / Email governance capabilities.
- [ ] I used official upstream capability or a thin adapter before adding new infrastructure.
- [ ] If this introduces a new component/state authority, the gap, maintenance burden, rollback, and acceptance evidence are documented.

## Architecture / authority impact

- [ ] No source-of-truth boundary changes.
- [ ] No source-of-truth boundary changes are claimed; OR the change is explicitly documented and approved.
- [ ] Employee least-privilege boundaries are preserved.
- [ ] No real credentials, employee secrets, or private network identifiers are committed.

## Validation

- [ ] `scripts/repository-readiness-check.sh` passes.
- [ ] Relevant capability tests pass.
- [ ] Runtime behavior was tested when this changes a deployed capability.
- [ ] Restart / persistence / rollback implications are documented where applicable.

## Frozen baseline impact

List any frozen baseline changed by this PR. If none, write `none`.

## Deployment impact

State one:

- blueprint/docs only
- reusable implementation only
- requires explicit real deployment
- updates sanitized reference-deployment evidence

## Notes for a fresh AI Agent

Explain anything a new Agent would need to know to reproduce or safely operate this change without chat history.
