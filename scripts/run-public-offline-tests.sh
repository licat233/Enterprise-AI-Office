#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

run() {
  printf '\n==> %s\n' "$1"
  shift
  "$@"
}

printf '%s\n' 'Enterprise AI Office Public Offline Tests'
printf '%s\n' '----------------------------------------'
printf '%s\n' 'These tests use repository fixtures, in-memory/temporary state, and fake providers.'
printf '%s\n' 'They must not contact real mailboxes, production services, or private runtime state.'

run 'Email Governance schema'   python3 infrastructure/email/governance/test_schema.py

run 'Email Governance send/reconciliation'   python3 infrastructure/email/governance/test_send_reconciliation.py

run 'Email Governance backup/restore recovery'   python3 infrastructure/email/governance/test_recovery.py

run 'Email Governance Phase 1 runtime'   python3 infrastructure/email/governance/test_phase1_runtime.py

run 'SMTP send outcome safety'   python3 infrastructure/email/tencent-exmail/test_smtp_send_adapter.py

run 'Enterprise Web Research'   python3 infrastructure/web-research/test_adapter.py

printf '\n%s\n' 'PUBLIC OFFLINE TESTS: PASS'
