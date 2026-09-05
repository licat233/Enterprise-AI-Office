# Company Configuration

This directory defines the public, reusable configuration boundary for an Enterprise AI Office deployment.

For deployment execution, follow root [`DEPLOY.md`](../DEPLOY.md).

## `company.example.yaml`

`company.example.yaml` describes deployment **intent**:

- company identity/language/timezone;
- Knowledge Base structure;
- Hermes Profiles;
- employee groups;
- role capabilities;
- messaging intent;
- backup/update policy;
- model roles.

It is deliberately free of production secrets.

### Configuration baseline

The example starts from a small reusable baseline:

- Hermes `default` / admin belongs to the control plane;
- `general` is the baseline employee-facing Profile;
- `all-employees` is the baseline employee group;
- `ai-admins` is the administrative group;
- a shared `Company Knowledge` Knowledge Base provides the initial employee knowledge boundary.

Extend Profiles, groups, Knowledge Bases, Skills, integrations, automation, and privileged capabilities only when the adopting company's actual requirements justify them. Repository examples and templates are reusable options rather than a deployment checklist.

## `validated-stack.yaml`

`validated-stack.yaml` is the machine-readable reproducibility baseline for the first successfully validated reference stack.

It records:

- supported reference host/runtime;
- exact tested component versions/commits;
- baseline Profile/group posture;
- baseline employee-memory and Open WebUI permission posture;
- which capabilities are optional unless company configuration enables them.

It is not a permanent version policy and does not contain company secrets.

For an ordinary Golden Path deployment, prefer this tested stack unless the task explicitly includes upgrade qualification. Upgrade work follows `docs/UPGRADE.md`.

## Important: schema vs installer

The current company YAML is a declarative configuration schema for humans and AI agents. It is not a generic one-command installer input.

An implementation agent should combine:

```text
DEPLOY.md execution contract
+
company configuration intent
+
validated-stack.yaml tested baseline
+
infrastructure adapters/templates
+
protected deployment secrets
```

to reach the target state.

Do not invent a parser/installer that the repository does not contain, and do not stop merely because no monolithic installer exists.

## Private company overlay

A production adopter should keep real company-specific deployment configuration in a private repository or protected deployment location.

Do not commit to this public repository:

- real employee lists;
- private network details that create risk;
- API keys;
- bot secrets;
- database passwords;
- private documents;
- customer data.

## `config/.env.example`

This is a non-secret input inventory/template for deployment adaptation.

Copy/adapt it only in a protected deployment-specific location. Add specialist credentials only for Profiles/integrations actually enabled.

## Configuration precedence

Conceptually:

```text
Generic architecture / Golden Path
        ↓
Validated stack baseline
        ↓
Company configuration
        ↓
Environment-specific deployment configuration
        ↓
Protected secrets
        ↓
Actual runtime state
```

Runtime reality must be recorded in `state/DEPLOYMENT-STATE.md`.

## Company values do not fork the architecture

Differences in specialist roles, Knowledge Bases, groups, and optional integrations belong in company configuration rather than separate generic architectures.

Generic architecture should change only when the reusable system model changes.
