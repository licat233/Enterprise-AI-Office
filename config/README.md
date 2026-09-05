# Company Configuration

This directory defines the public, reusable configuration boundary for an Enterprise AI Office deployment.

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

Extend Profiles, groups, Knowledge Bases, Skills, integrations, automation, and privileged capabilities only when the adopting company's actual organization and operating requirements justify them. Repository examples and templates are reusable options rather than a deployment checklist.

## Important: schema vs installer

The current YAML is a reference configuration schema for humans and AI agents. It is not yet guaranteed to be consumed directly by an installer.

An implementation agent must not pretend that a parser/installer exists when it does not.

As the project matures, validated automation may consume this schema. Until then it is the canonical declarative description of what a company wants built.

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

This is a non-secret environment-variable template for local scripts and deployment adaptation.

Copy it to an untracked/protected `.env` only when needed.

## Configuration precedence

Conceptually:

```text
Generic project defaults / standards
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

## Do not fork generic architecture for company values

Differences in specialist roles belong in company configuration rather than separate architecture variants.

Generic architecture should change only when the underlying reusable system model changes.
