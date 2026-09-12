# Repository Governance

This document defines the GitHub/repository workflow required to preserve Enterprise AI Office as an agent-readable, reproducible system blueprint.

It governs repository maintenance. It does not replace runtime RBAC, deployment authorization, or company-private operational controls.

## 1. Main branch role

`main` is the canonical public blueprint state.

A fresh AI Agent must be able to clone `main` and obtain the current:

- architecture and authority model;
- validated stack;
- capability registry;
- deployment and validation contracts;
- reusable implementation assets;
- sanitized reference-deployment evidence.

Do not use a long-lived feature branch as the only home of a frozen capability or current operational lesson.

## 2. Change path

Material changes should use:

```text
branch
→ Capability Reuse Pass
→ implementation/docs/tests
→ Repository Readiness CI
→ pull request
→ review of authority/security/runtime impact
→ merge to main
```

Direct commits to `main` should be treated as an exception rather than the normal Agent workflow.

## 3. Required checks

The public repository check is:

```sh
EAO_REPOSITORY_ONLY=1 sh scripts/repository-readiness-check.sh
python3 scripts/validate-fresh-agent-kit.py
```

GitHub Actions additionally checks shell syntax and Python compilation.

These checks validate repository closure. They do not replace deployment-host acceptance.

## 4. GitHub main-branch protection target

The repository should protect `main` with the following policy where GitHub repository settings permit it:

- require a pull request before merge;
- require the **Repository Readiness / Agent reproducibility contract** check to pass;
- block force pushes to `main`;
- block branch deletion;
- do not allow a failing/stale required check to be bypassed for routine Agent work.

This is a GitHub repository setting, not something a Markdown file can enforce by itself.

If branch protection is temporarily unavailable or disabled, Agents must still follow the PR + CI workflow above and record the gap rather than treating direct-push capability as permission.

## 5. Merge history

Frozen baseline commits referenced by SHA are part of the evidence model.

When a PR contains commits that are already named by SHA in frozen baseline documentation, prefer a merge strategy that preserves those commits in reachable history rather than rewriting them away without updating the evidence.

Do not change a frozen SHA reference casually.

## 6. Authority-changing pull requests

A PR requires explicit architecture/security review when it changes any of:

- source-of-truth ownership;
- employee permissions;
- Profile tool exposure;
- knowledge authority;
- memory policy;
- external side effects;
- credential scope;
- network exposure;
- backup/recovery boundaries;
- validated component versions;
- lifecycle/readiness semantics.

The PR template and `docs/CAPABILITY-REUSE-PASS.md` are the minimum decision record.

## 7. Historical material

Historical/reference documents must be visibly labeled as non-normative.

They must not claim to be the current execution contract if they have been superseded.

Current authority entrypoints are:

```text
README.md
AGENTS.md
REPRODUCE.md
config/eao-manifest.yaml
state/PROJECT-PHASE.yaml
VALIDATE.md
DEPLOY.md
current normative docs/
```

## 7.1 GitHub collaboration surfaces are non-normative

GitHub-hosted collaboration surfaces may be useful, but they are not architecture
or deployment authority.

The following are **non-normative unless their content is merged into the
repository authority chain above**:

- GitHub Wiki pages;
- GitHub Project boards/cards;
- Issues and issue comments;
- Pull Request descriptions/comments/reviews;
- Discussions or other collaboration surfaces if enabled later.

Use them for intake, planning, review, and coordination. Do not place the only
copy of a current architecture decision, capability contract, runtime mapping,
deployment procedure, or frozen acceptance result there.

When collaboration produces a durable decision, promote it into the appropriate
version-controlled repository contract/evidence through a reviewed pull request.

A Fresh Agent must not override merged repository authority merely because a
Wiki page, Project card, Issue, or PR comment appears newer.

## 8. Releases

Do not publish a GitHub release that implies `release_ready` while `state/PROJECT-PHASE.yaml` says Release Ready has not been opened/passed.

Tags/releases must reflect the repository lifecycle truth, not marketing convenience.

## 9. Private state

Never solve CI or reproducibility failures by committing protected runtime state.

Private Profile configuration, real credentials, employee identities, mailbox data, protected company configuration, and private network/device identity material remain outside the public repository.

Public CI must validate public reproducibility contracts only.

## 10. Definition of repository maturity

Repository maturity means a fresh capable Agent can determine:

1. what the system is;
2. what is authoritative;
3. what is historical;
4. how to reproduce it;
5. how to validate it;
6. how to change it safely;
7. which information must remain private.

More GitHub features do not automatically make the repository more mature. Add repository machinery only when it strengthens one of these properties.


## 11. CI supply-chain posture

Repository validation workflows should remain reproducible and least-privilege:

- grant only the GitHub token permissions the job actually needs;
- prefer read-only permissions for validation jobs;
- pin third-party GitHub Actions to an exact reviewed commit SHA, retaining a comment for the human-readable release family;
- disable checkout credential persistence when the job does not push;
- pin the runner image family instead of relying on a floating `latest` label when the checked workflow does not require that drift;
- do not use `pull_request_target` to execute untrusted pull-request code;
- do not expose repository or deployment secrets to public validation jobs.

The Repository Readiness workflow is expected to be a clean-checkout, read-only validation path. Deployment credentials and company-private runtime state do not belong in this workflow.
