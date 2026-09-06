# Enterprise AI Office v2 — Recovery / Clean-host Installation Contract

Status: recovery / clean-host installation contract frozen / real deployment not authorized
Version: 1.0
Date: 2026-09-07

This document closes `ID-7 — Rollback / recovery / clean-host acceptance` for the Enterprise AI Office v2 `installation_design` phase.

It defines how a future authorized installer must preserve v1, back up and restore v2 Governance state, recover safely after process/host failure, roll back or disable v2 capabilities, and prove that the complete blueprint can be reproduced on a clean validation target without creating duplicate external side effects.

It does **not** authorize a real company installation, real mailbox credential, real provider connection, real customer send, reboot of a real host, or transition into `blueprint_validation`.

Use with:

- `DEPLOY.md`
- `docs/BACKUP-RESTORE.md`
- `docs/OPERATIONS.md`
- `docs/V2-INSTALLATION-ARCHITECTURE.md`
- `docs/V2-CONFIG-PROTECTED-INPUTS.md`
- `docs/V2-STAGE-CONTRACTS.md`
- `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`
- `docs/V2-GOVERNANCE-RUNTIME.md`
- `docs/V2-SEND-RECONCILIATION.md`
- `docs/acceptance/TENCENT-EXMAIL.md`
- `config/capabilities.yaml`
- `state/DEPLOYMENT-STATE.template.md`
- `infrastructure/email/governance/backup_state.py`
- `infrastructure/email/governance/restore_state.py`
- `infrastructure/email/governance/test_recovery.py`

---

## 1. ID-7 objective

ID-1 through ID-6 already define what must be installed.

ID-7 proves the installation blueprint has a complete lifecycle around those components:

```text
clean target
→ inspect
→ resolve desired state
→ install/reconcile
→ accept Stage 0–4 when Email is enabled
→ restart/recover safely
→ back up/restore owned state
→ repeat installer without duplicate resources/business actions
→ disable/rollback v2 without damaging v1
→ record evidence
```

The goal is recoverability and reproducibility, not a new orchestration platform.

---

## 2. v1 preservation is a hard invariant

The validated baseline remains independent:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes general Profile
→ WeKnora
```

v2 failure or rollback must not require deleting/rebuilding this path.

Before any v2 mutation on an authorized target:

```text
1. establish Stage 0 / v1 baseline evidence
2. inspect existing Open WebUI/Hermes/WeKnora resources
3. create required pre-change recovery point
4. mutate only v2-owned resources
```

After every major v2 rollback/recovery rehearsal, re-run the representative v1 employee-path acceptance.

Failure of `eao-email-governance`, provider credentials, SMTP, Communication Assistant, or Email tools must degrade Email capability rather than take down General Assistant.

---

## 3. v2-owned recovery scope

When Email capability is enabled, recoverable v2-owned state includes at least:

```text
Governance SQLite database
  DraftReply revisions
  review bindings
  SendApproval evidence
  ApprovalClaims
  LogicalSend evidence
  SendAttempt / result evidence
  reconciliation evidence
  governance audit events

company-private non-secret desired state
logical → runtime group mappings / resource identifiers as operational state
Communication Assistant / tool-connection reconstruction metadata
symbolic secret references
```

Protected secret **values** remain in the selected secret-recovery mechanism, not inside public deployment state.

Provider mailbox content remains provider-owned and is not mirrored merely for disaster recovery.

---

## 4. Governance SQLite backup rule

Do not casually copy a live `state.sqlite3` file while WAL transactions may be active.

Reference backup method:

```text
SQLite online backup API
source DB opened read-only/read-safe
→ consistent destination snapshot
→ PRAGMA integrity_check
→ schema version recorded
→ SHA-256 recorded by outer backup manifest
```

Reference helper:

```text
python3 infrastructure/email/governance/backup_state.py \
  <source-state.sqlite3> \
  <backup-state.sqlite3>
```

The helper must not:

```text
modify source DB
vacuum/rewrite source DB
start Governance service
open provider network connections
send/retry email
print secrets
```

A missing Governance DB is normal when v2 Email is not enabled.

---

## 5. Backup set integration

The existing repository `scripts/backup.sh` remains the full-stack reference helper for the validated local topology.

When Governance state exists, the v2 extension adds to the same backup generation:

```text
governance/state.sqlite3
```

and records it in the manifest/checksum set.

When Governance state does not exist:

```text
v1 backup continues normally
→ Email Governance reported as not enabled / state absent
```

Do not make v1 backup fail merely because a conditional v2 capability is disabled.

For an actual production target, keep at least one encrypted backup copy independent from the primary host disk per `docs/BACKUP-RESTORE.md`.

---

## 6. Governance restore rule

A Governance restore is always first materialized into a **new isolated target path**.

Reference helper:

```text
python3 infrastructure/email/governance/restore_state.py \
  <backup-state.sqlite3> \
  <new-target-state.sqlite3>
```

The target must not already exist.

Restore validation performs at least:

```text
PRAGMA integrity_check == ok
expected governance schema metadata exists
schema version is understood by the selected runtime
foreign-key check has no violations
```

Unknown newer schema:

```text
BLOCKED — SCHEMA VERSION NEWER THAN RUNTIME
```

Corrupt/inconsistent backup:

```text
FAIL — GOVERNANCE BACKUP INTEGRITY
```

Do not start provider sending merely because a database restore succeeds.

---

## 7. Restore never manufactures a retry

This is the most important recovery invariant introduced by ID-6.

After restore/startup:

```text
SendAttempt exists
+
no terminal SendAttemptResult
→ RECONCILIATION_REQUIRED
```

Likewise:

```text
latest result OUTCOME_UNKNOWN
→ RECONCILIATION_REQUIRED
```

Recovery must never transform either condition into:

```text
CONFIRMED_NOT_SENT
READY_TO_ATTEMPT
automatic retry
```

A restored `SENT` remains terminal.

A restored `CONFIRMED_NOT_SENT` may be eligible for a controlled retry only after the normal ID-6 authorization/payload checks are re-run; startup itself does not execute that retry.

---

## 8. Governance service startup recovery

Reference startup order for v2 Governance:

```text
1. load validated desired state / protected bindings
2. open SQLite
3. enable foreign_keys / WAL / synchronous / busy_timeout policy
4. inspect schema version
5. apply only known forward migrations when explicitly required
6. run lightweight integrity/schema checks
7. load mailbox authorization policy
8. scan unresolved send attempts / reconciliation-required logical sends
9. expose read/draft/approval/send surfaces only for accepted Stage
10. become ready
```

Unresolved sends are operational warnings/blocked send records, not a reason to hide history or auto-retry.

If schema migration fails:

```text
Governance readiness FAILS CLOSED
v1 General Assistant remains independent
```

---

## 9. Schema migration / rollback boundary

ID-5/ID-6 use forward schema evolution.

Before a destructive or compatibility-risking Governance migration on an authorized target:

```text
create pre-migration Governance backup
record current schema version
record application/version contract
stop provider-send activation if required
apply migration
run integrity + contract tests
```

Downgrading application code over a newer incompatible database is forbidden.

If rollback requires the old schema/runtime:

```text
stop Governance service
→ restore the pre-migration Governance snapshot into a new target
→ start compatible old runtime against restored copy
→ run recovery acceptance
```

Do not attempt ad-hoc reverse SQL merely to avoid restoring a known-good snapshot.

---

## 10. Capability rollback levels

Rollback is capability-oriented, not “delete everything”.

### Level 1 — disable send only

```text
remove/disable Approve & Send / send action
remove/revoke provider send credential binding
disable Stage 4 send surface
preserve read/draft/approval evidence
preserve Governance database
v1 unaffected
```

### Level 2 — downgrade Email to read-only

```text
disable send action
disable approval Action
disable prepare_reply_draft
keep search_email/get_email if desired
preserve Governance evidence according to retention policy
v1 unaffected
```

### Level 3 — disable v2 Email capability

```text
remove Communication Assistant employee access
remove Email Governance tool connection
stop/disable Governance service if unused
remove provider credentials from runtime
preserve/archive/delete Governance state only under explicit retention/removal policy
leave Open WebUI General Assistant, Hermes general, WeKnora untouched
```

Externally sent email is never rolled back.

---

## 11. Installer re-run / convergence contract

A capable installer must be safe to re-run after interruption.

Re-run may reconcile infrastructure/configuration facts such as:

```text
directories
service definitions
Communication Assistant
Open WebUI groups/resources owned by config
Hermes communication Profile
Governance service config
SQLite schema version
provider adapter binding
stage-enabled tool surfaces
```

Re-run must **not** create business side effects:

```text
no new DraftReply merely because installer re-runs
no new SendApproval
no new ApprovalClaim
no new LogicalSend
no new SendAttempt
no customer-visible send
no reconciliation conclusion fabricated
```

Installer identity/idempotency belongs to provisioning resources; it is not business-operation replay.

---

## 12. Clean-host blueprint acceptance target

`blueprint_validation` later uses an explicitly approved clean/synthetic target.

A clean target should begin with no prior EAO runtime state except the repository checkout and approved host/runtime prerequisites.

The validation agent must be able to derive the complete requested target from:

```text
AGENTS.md
state/PROJECT-PHASE.yaml
DEPLOY.md
company config + private overlay shape
config/capabilities.yaml
ID-1 through ID-7 contracts
component/provider playbooks
acceptance documents
protected-input prompts
```

It must not require hidden knowledge from this design conversation.

---

## 13. Clean-host execution sequence

Reference validation sequence:

```text
A. repository readiness / lifecycle gate
B. read-only host preflight
C. resolve company desired state + capability closure
D. deploy/accept v1 Core employee path
E. Stage 0 v1 baseline evidence
F. provision isolated Communication Profile / Assistant
G. install Governance runtime + schema
H. Stage 1 read-only Email
I. Stage 2 DraftReply
J. Stage 3 deterministic Approval
K. Stage 4 governed send/reconciliation using synthetic/fake provider first
L. optional Stage 5/6 only when requested
M. backup Governance/full required state
N. isolated restore
O. restart/failure recovery tests
P. installer second-run convergence test
Q. rollback/degrade v2 and re-prove v1
R. re-enable/reconcile requested v2 state where validation scope requires it
S. record acceptance/deployment-state evidence
```

A real provider credential is not required to prove repository-level deterministic contracts. Live provider acceptance belongs only to an explicitly authorized validation/deployment target.

---

## 14. Mandatory offline / synthetic tests before live provider acceptance

At minimum run:

```text
python3 infrastructure/email/governance/test_schema.py
python3 infrastructure/email/governance/test_send_reconciliation.py
python3 infrastructure/email/governance/test_recovery.py
python3 infrastructure/email/tencent-exmail/test_imap_readonly.py
python3 infrastructure/email/tencent-exmail/test_smtp_send_adapter.py
scripts/repository-readiness-check.sh
```

These tests must use synthetic/in-memory/temp resources and no real mail credentials.

A repository-level PASS is necessary blueprint evidence but is not equivalent to a live company deployment PASS.

---

## 15. Failure-injection matrix

Clean-host/recovery validation must exercise at least these classes:

```text
Governance process restart with persisted Draft/Approval
Governance restart with unresolved SendAttempt
attempt row committed, no terminal result
OUTCOME_UNKNOWN persisted
SQLite backup + isolated restore
corrupt backup rejected
unknown newer schema rejected
provider connection/auth failure → CONFIRMED_NOT_SENT where no DATA side effect began
synthetic DATA timeout → OUTCOME_UNKNOWN
removed email.send permission before send/retry → deny
removed Open WebUI group grant → deny on next governed request per identity sync semantics
v2 Governance service unavailable → General Assistant still works
Email capability disabled/removed → no autonomous sender remains
installer re-run → no duplicate v2 resources/business actions
```

Do not inject destructive failure into a real production mailbox merely to satisfy blueprint validation.

---

## 16. Backup / restore acceptance

When v2 Email is enabled, acceptance must prove:

```text
[ ] Governance DB included in full backup generation
[ ] backup uses consistent SQLite snapshot method
[ ] backup checksum/manifest covers Governance snapshot
[ ] isolated restore passes integrity/foreign-key/schema checks
[ ] Draft revisions preserved
[ ] SendApproval / claims preserved
[ ] LogicalSend / attempt/result evidence preserved
[ ] reconciliation evidence preserved
[ ] unresolved attempt remains RECONCILIATION_REQUIRED after restore
[ ] restore starts no provider send by itself
[ ] secrets are recoverable through protected mechanism but absent from public manifest/state
```

---

## 17. Restart / recovery acceptance

Reference assertions:

```text
[ ] Governance service can restart without losing committed Draft/Approval state
[ ] schema migration runs before write readiness
[ ] unknown newer schema fails closed
[ ] unresolved send is surfaced, not retried
[ ] SENT logical send remains non-retryable
[ ] General Assistant remains healthy when Governance is stopped/unhealthy
[ ] Communication Assistant fails safely/degrades when Governance is unavailable
```

Host-reboot acceptance is performed only on an explicitly authorized validation/deployment host. Installation Design defines the procedure; it does not reboot a real host.

---

## 18. Rollback acceptance

At least one clean/synthetic rehearsal must prove:

```text
[ ] Stage 4 send surface can be disabled without deleting Governance history
[ ] provider send credential can be removed without affecting v1
[ ] Communication Assistant/Email tool access can be removed without affecting General Assistant
[ ] v2 service can be stopped while Open WebUI + Hermes general + WeKnora remain usable
[ ] no Cron/messaging capability can bypass disabled Email send gate
[ ] restoring/re-enabling desired v2 config converges without duplicate resources
```

---

## 19. Deployment-state evidence

When an actual validation/deployment target enables v2 Email, `state/DEPLOYMENT-STATE.md` or the protected equivalent records non-secret truth including:

```text
Governance service version/contract
Governance state path
schema version
Communication Assistant/tool connection IDs
logical group → runtime group mappings
mailbox grant summary
provider endpoint mode
secret reference classes, never values
latest backup generation / Governance snapshot inclusion
last isolated restore result
startup/recovery result
unresolved reconciliation count/status when operationally relevant
Stage 0–4 results
rollback/re-enable rehearsal result
installer second-run convergence result
known limitations
```

Do not copy Draft bodies, mailbox passwords, forwarder tokens, or provider credentials into deployment state.

---

## 20. Installation Design final closure gate

ID-7 is complete when the repository contains consistent, agent-readable contracts for:

```text
v1 preservation
Governance backup / restore
schema migration and downgrade safety
startup recovery
unresolved-send preservation
capability rollback/degradation
clean-host installation sequence
second-run convergence
failure injection
acceptance/evidence recording
```

and repository readiness checks require those artifacts.

At that point:

```text
INSTALLATION DESIGN FINAL REVIEW: PASS
INSTALLATION DESIGN: COMPLETE
```

may be recorded if ID-1 through ID-7 have no structural contradiction.

This milestone does **not** change `blueprint_lifecycle.current_phase` automatically.

Opening:

```text
blueprint_validation
```

still requires explicit human direction per `state/PROJECT-PHASE.yaml`.

---

## 21. Explicitly rejected ID-7 alternatives

### New backup platform

Rejected. Existing full-stack backup/restore plus SQLite-native Governance snapshot is sufficient for the baseline.

### Automatic retry on service restart

Rejected. Recovery uncertainty must never become duplicate-send behavior.

### Delete Governance DB when disabling Email

Rejected as default. Retention/removal is an explicit policy decision because the database contains governance evidence.

### Reverse migrations by hand

Rejected for baseline rollback. Restore a known pre-migration snapshot with the compatible runtime instead.

### Clean-host validation on production

Rejected. Blueprint validation should use an explicitly approved isolated/synthetic target unless the human separately authorizes a production deployment task.

---

## 22. Result

```text
RECOVERY / CLEAN-HOST INSTALLATION CONTRACT FROZEN
```
