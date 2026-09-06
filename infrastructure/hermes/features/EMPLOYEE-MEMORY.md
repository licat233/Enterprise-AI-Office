# Employee Hermes Long-Term Memory Gate

This file is the execution contract for `capabilities.employee_long_term_memory`.

The first validated Enterprise AI Office core baseline deliberately keeps employee Hermes long-term memory disabled because the validated Open WebUI → Hermes path has not yet proven a stable per-human persistent-memory scope across multiple users sharing the same Hermes Profile.

This is not a missing checkbox to turn on. Cross-user memory leakage is a security boundary.

## 1. Baseline status

Validated baseline:

```text
Open WebUI conversation history: enabled
Hermes employee long-term memory: disabled
```

Conversation history remains available per Open WebUI account and is not the same thing as Hermes long-term memory.

Do not infer a persistent Hermes memory identity from browser chat IDs, display names, email text inside prompts, or any other untrusted/user-controlled value.

## 2. When the company leaves the capability disabled

No additional runtime component or memory store should be created for completeness.

Record:

```text
employee Hermes long-term memory: disabled
reason: baseline isolation policy
Open WebUI conversation history: <actual state>
```

This does not block Core Ready or Configured Ready when the capability is disabled.

## 3. When the company enables the capability

Before changing the Hermes memory setting, resolve an exact supported mechanism for the pinned Open WebUI/Hermes versions that maps:

```text
authenticated human identity
→ trusted stable user scope
→ Hermes memory read/write scope
```

The mechanism must be enforced by the deployed integration/runtime, not by instructions in the system prompt.

Required evidence before enabling:

```text
exact Open WebUI version
exact Hermes version
identity/scope propagation mechanism
where the scope is enforced
how a Profile receives the trusted scope
how memory records are keyed/partitioned
how scope survives restart
how user deletion/role change affects memory access
```

If no such supported mechanism is already selected and demonstrably available for the pinned deployment, return:

```text
BLOCKED — REQUIRED INPUT: no validated per-user Hermes long-term-memory scope exists for the selected integration
```

Do not start experimental custom middleware merely to satisfy capability closure.

## 4. Two-user isolation acceptance

Use two distinct ordinary employee identities, A and B, authorized for the same employee-facing Profile.

Test:

```text
A stores a unique private marker in persistent Hermes memory
A starts a new conversation and recovers the marker as designed
B asks directly and indirectly for A's marker
B must not recover it
restart the relevant services
A continuity still behaves as designed
B isolation still holds
```

Also test that user-controlled text cannot select another user's memory namespace.

Any cross-user disclosure is an immediate FAIL.

## 5. Cross-Profile isolation

If the same human can use multiple Profiles with persistent memory, verify whether the intended policy is:

```text
Profile-isolated memory
or
explicitly shared memory
```

Do not let a Profile identifier supplied in prompt text switch memory authority.

When Profile isolation is intended:

```text
memory written through Profile A
→ unavailable to Profile B unless explicitly authorized by design
```

## 6. Enable only after acceptance

Only after the selected mechanism passes the two-user and applicable cross-Profile tests may the deployment enable Hermes long-term memory for the configured Profile set.

Then record in deployment state:

```text
mechanism/version
trusted user-scope source
enforcement point
enabled Profiles
cross-user result
cross-Profile result
restart-persistence result
known limitations
```

Do not record private test markers or secrets unnecessarily.

## 7. Completion rule

For an enabled `employee_long_term_memory` capability, exactly one of these outcomes is valid:

```text
PASS — validated user-scoped mechanism enabled and isolation tests pass
BLOCKED — no approved/supported mechanism available
FAIL — mechanism enabled but isolation test fails
```

`BLOCKED` or `FAIL` means the deployment cannot declare `CONFIGURED READY` while the company configuration still requests this capability.

The deployment agent may not silently turn the requested capability back off and declare success. A human/company decision must either provide/approve a supported mechanism or change the company configuration.