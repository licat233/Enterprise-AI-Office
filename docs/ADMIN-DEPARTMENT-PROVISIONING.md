# Administrator Department Provisioning

This document defines how an Enterprise AI Office administrator adds or changes a
company department without confusing human organization structure with Hermes
AI work-role state.

For runtime execution, reuse the existing contracts:

- infrastructure/hermes/PROVISIONING.md
- infrastructure/open-webui/PROVISIONING.md
- docs/CLIENT-RBAC.md
- docs/PROFILE-STANDARD.md
- docs/ACCEPTANCE-TESTS.md

No separate department-sync daemon is required.

## 1. Core rule

An Open WebUI Group and a Hermes Profile are different objects:

~~~text
Open WebUI Group
= human identity / membership / RBAC principal

Hermes Profile
= AI work role / SOUL / Skills / tools / credentials / automation boundary
~~~

Creating a department Group MUST NOT automatically create a same-named Hermes
Profile.

The supported employee path remains:

~~~text
Human employee
→ Open WebUI user
→ Group/resource authorization
→ Assistant
→ Hermes Profile
~~~

A department may use the shared general Profile, an already-approved specialist
Profile, or a new specialist Profile. One department does not imply one Profile,
and one Profile may legitimately serve more than one department.

## 2. Capability Reuse Pass before creating a Profile

Before a new department Profile is declared, check whether the department's
actual work is already covered by an existing approved Profile.

Create a new Profile only when at least one durable boundary is real and
documented, for example:

- different SOUL/work behavior;
- different knowledge scope;
- different Skills or MCP/tool exposure;
- different credential boundary;
- different model or memory policy;
- different automation ownership;
- different risk/compliance boundary.

A department name alone is not sufficient.

Default decision:

| Department need | Provisioning result |
| --- | --- |
| Normal company assistance only | Department Group may exist; employees use general; no new Hermes Profile |
| Needs an already-approved specialist role | Grant the department Group read access to that existing Assistant/Profile path |
| Needs a durable distinct AI role/capability/risk boundary | Declare and provision a new specialist Profile |

Do not duplicate operations, general, or another specialist merely to mirror an
organization chart.

## 3. Desired-state change

A real department Group belongs in the protected company configuration under
employee_access.web.groups.

Example:

~~~yaml
employee_access:
  web:
    groups:
      - id: sales-employees
        display_name: Sales Employees
~~~

If the department uses only the company-wide General Assistant, no additional
Profile declaration is required.

If the department is authorized to use an existing specialist Profile, add the
department logical Group ID to that Profile's employee_groups only when that
authorization is intended.

If a new specialist Profile is justified, declare the complete Profile contract:

~~~yaml
core_provisioning:
  hermes:
    profile_api_key_refs:
      sales: hermes-sales-api-key

profiles:
  - id: sales
    display_name: Sales Assistant
    template: profiles/sales/SOUL.md
    employee_groups:
      - sales-employees
    knowledge_bases:
      - company-general
    capabilities:
      terminal: false
      code_execution: false
      coding_delegation: false
      web_search: false
    memory_policy: disabled
~~~

The symbolic credential ref must resolve through protected storage and map to
Profile-local API_SERVER_KEY. Never place the plaintext key in Git or in the
company YAML.

## 4. Hermes reconciliation

For a justified new specialist Profile, follow
infrastructure/hermes/PROVISIONING.md rather than inventing a second runtime
path.

Required outcome:

~~~text
native Hermes Profile exists
→ least-privilege config/SOUL applied
→ unique Profile API credential
→ shared multiplex Gateway allowlist includes the Profile
→ no independent employee listener
→ approved MCP/Skills only
→ long-term memory follows declared policy
~~~

Use the upstream Profile command for creation. Do not create Profile directories
manually and do not clone all state from another Profile.

The shared Gateway route is conceptually:

~~~text
/p/<profile-id>/v1
~~~

Do not allocate one new Hermes port per department.

## 5. Open WebUI reconciliation

Follow infrastructure/open-webui/PROVISIONING.md.

For each enabled specialist Profile:

1. resolve or create the intended Open WebUI Group;
2. create/reconcile exactly one server-side Hermes connection for the Profile;
3. use that Profile's unique API key;
4. verify the Profile's advertised model ID maps to that exact connection;
5. create/reconcile the private Model/Assistant resource;
6. grant read only to the intended Group(s);
7. preserve unrelated approved resources.

Use the Open WebUI native admin API for normal provisioning. Do not write
directly to the Open WebUI database.

A Group that uses only general does not require a duplicate department Assistant.

## 6. New employee onboarding

Department membership and Assistant authorization are additive.

For a new employee:

1. create/activate the Open WebUI identity;
2. assign the baseline company Group(s) required by company policy;
3. assign the employee's department Group;
4. verify the resulting Assistant set;
5. verify at least one unauthorized specialist path fails closed.

Do not grant Open WebUI admin merely because an employee manages work inside a
department.

## 7. Rename, removal, and department reorganization

### Rename only

Keep stable logical IDs whenever the department meaning is unchanged. Update the
human-facing display name and record the new runtime mapping. Do not create a
new Hermes Profile merely because a department display name changed.

### Department removed

Remove user membership and unnecessary Group grants first. Preserve business
records according to company policy. Delete a specialist Profile only after
confirming that no other Group, automation, credential, or workflow still
depends on it.

### Department splits/merges

Re-run the Capability Reuse Pass. Organization-chart changes do not by
themselves require Profile duplication.

## 8. Acceptance

A department change is complete only when the observable authorization path is
proven.

For every affected department:

~~~text
intended employee/group
→ intended Assistant(s): ALLOW

unauthorized employee/group
→ specialist Assistant: DENY

ordinary employee
→ default/admin Profile: DENY
~~~

For a newly created specialist Profile also verify:

- unique Profile API key;
- cross-Profile key denial;
- exact shared-Gateway route;
- container → Hermes connection;
- intended Knowledge retrieval;
- prohibited tools remain unavailable;
- memory policy remains as declared;
- restart/recovery preserves the mapping.

Record non-secret logical Group → runtime Group UUID and Profile → connection /
model mapping in protected operational state.

## 9. Administrator mental model

Use this sequence:

~~~text
Add department
→ create/reconcile Open WebUI Group
→ Capability Reuse Pass
→ choose existing AI role OR justify new Profile
→ reconcile Hermes only when needed
→ reconcile Open WebUI Assistant/ACL only when needed
→ acceptance
~~~

The absence of a same-named Hermes Profile after creating an Open WebUI Group is
therefore not an error by itself.
