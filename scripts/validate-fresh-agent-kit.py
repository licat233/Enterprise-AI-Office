#!/usr/bin/env python3
"""Static validation for the EAO Fresh-Agent Validation Kit.

This script deliberately uses only the Python standard library. It validates
public repository contracts; it does not open Blueprint Validation, authorize
a deployment, inspect private runtime state, or prove runtime reproduction.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS = 0
FAIL = 0


def ok(label: str) -> None:
    global PASS
    PASS += 1
    print(f"{label:<62} PASS")


def bad(label: str, reason: str) -> None:
    global FAIL
    FAIL += 1
    print(f"{label:<62} FAIL - {reason}")


def require_file(rel: str) -> None:
    path = ROOT / rel
    if path.is_file():
        ok(rel)
    else:
        bad(rel, "missing")


def require_text(rel: str, needle: str, label: str) -> None:
    path = ROOT / rel
    if not path.is_file():
        bad(label, f"{rel} missing")
        return
    text = path.read_text(encoding="utf-8")
    if needle in text:
        ok(label)
    else:
        bad(label, f"expected text not found in {rel}: {needle!r}")


def check_markdown_links(rel: str) -> None:
    path = ROOT / rel
    if not path.is_file():
        bad(f"{rel} local links", "file missing")
        return

    text = path.read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    missing: list[str] = []

    for target in links:
        target = target.strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            missing.append(target + " (escapes repository)")
            continue
        if not resolved.exists():
            missing.append(target)

    if missing:
        bad(f"{rel} local links", ", ".join(missing))
    else:
        ok(f"{rel} local links")


def main() -> int:
    print("Enterprise AI Office Fresh-Agent Validation Kit")
    print("------------------------------------------------")

    for rel in [
        "VALIDATE.md",
        "validation/FRESH-AGENT-TASK.md",
        "validation/scorecard.yaml",
        "validation/REPORT.template.md",
        "REPRODUCE.md",
        "AGENTS.md",
        "DEPLOY.md",
        "docs/ACCEPTANCE-TESTS.md",
        "docs/CAPABILITY-REUSE-PASS.md",
        "config/eao-manifest.yaml",
        "state/PROJECT-PHASE.yaml",
        "state/DEPLOYMENT-STATE.template.md",
        "state/REAL-DEPLOYMENT-STATUS.md",
        "reference/armor/reference-index.yaml",
    ]:
        require_file(rel)

    require_text(
        "state/PROJECT-PHASE.yaml",
        "current_phase: installation_design",
        "Validation kit does not silently advance blueprint phase",
    )
    require_text(
        "state/PROJECT-PHASE.yaml",
        "status: not_opened",
        "Blueprint Validation remains not opened",
    )
    require_text(
        "VALIDATE.md",
        "Creating or improving this validation kit **does not open Blueprint Validation**",
        "Validation entrypoint preserves lifecycle gate",
    )
    require_text(
        "VALIDATE.md",
        "REPOSITORY_DEFECT",
        "Validation entrypoint defines defect taxonomy",
    )
    require_text(
        "validation/FRESH-AGENT-TASK.md",
        "Perform the Capability Reuse Pass",
        "Fresh Agent task requires capability reuse",
    )
    require_text(
        "validation/FRESH-AGENT-TASK.md",
        "Do not perform this stage unless the human explicitly authorizes Blueprint Validation",
        "Fresh Agent task blocks unauthorized runtime reproduction",
    )
    require_text(
        "validation/scorecard.yaml",
        "any_critical_failure_fails_comprehension_gate: true",
        "Scorecard has fail-closed critical-failure rule",
    )
    require_text(
        "validation/scorecard.yaml",
        "minimum_score_percent: 90",
        "Scorecard has explicit comprehension threshold",
    )
    require_text(
        "validation/scorecard.yaml",
        "checks_hermes_cron_before_new_scheduler",
        "Scorecard tests scheduler reuse behavior",
    )
    require_text(
        "validation/scorecard.yaml",
        "checks_weknora_before_second_vector_database",
        "Scorecard tests knowledge reuse behavior",
    )
    require_text(
        "validation/REPORT.template.md",
        "Additional human hints given after test start",
        "Report records hidden-hint contamination",
    )
    require_text(
        "config/eao-manifest.yaml",
        "validation_entrypoint: VALIDATE.md",
        "Manifest exposes validation entrypoint",
    )
    require_text(
        "REPRODUCE.md",
        "state/REAL-DEPLOYMENT-STATUS.md",
        "Reproduction contract points to current public reference status",
    )

    require_text(
        "config/eao-manifest.yaml",
        "machine_readable_index: reference/armor/reference-index.yaml",
        "Manifest exposes sanitized ARMOR reference index",
    )
    require_text(
        "config/eao-manifest.yaml",
        "authority: config/validated-stack.yaml",
        "Manifest delegates Core version truth",
    )
    require_text(
        "DEPLOY.md",
        "current reproducible Core version/commit authority is `config/validated-stack.yaml`",
        "Fresh Agent uses validated-stack as current Core version authority",
    )
    require_text(
        "docs/OPERATIONS.md",
        "not the live operational state store",
        "Fresh Agent keeps operational state authority protected",
    )
    require_text(
        "config/eao-manifest.yaml",
        "deployment_state_template: state/DEPLOYMENT-STATE.template.md",
        "Manifest exposes protected deployment-state template",
    )
    require_text(
        "DEPLOY.md",
        "protected operational storage",
        "Fresh Agent keeps real deployment state protected",
    )
    require_text(
        "docs/BACKUP-RESTORE.md",
        "Protected operational deployment state",
        "Fresh Agent knows protected state is recoverable",
    )
    require_text(
        "REPRODUCE.md",
        "Do not overwrite the repository's historical",
        "Fresh Agent preserves public historical deployment evidence",
    )
    require_text(
        "config/validated-stack.yaml",
        "does_not_claim_new_clean_host_validation: true",
        "Validated stack does not confuse runtime confirmation with clean-host validation",
    )
    require_text(
        "DEPLOY.md",
        "### 4.1 Deterministic Core acquisition",
        "Fresh Agent has deterministic Core acquisition",
    )
    require_text(
        "DEPLOY.md",
        "### 4.2 Post-acquisition Core identity assertions",
        "Fresh Agent must prove Core runtime identity",
    )
    require_text(
        "DEPLOY.md",
        "infrastructure/hermes/PROVISIONING.md",
        "Fresh Agent uses Hermes Core provisioning contract",
    )
    require_text(
        "infrastructure/hermes/PROVISIONING.md",
        "hermes profile create general --no-skills --no-alias",
        "Fresh Agent preserves General Profile least privilege at creation",
    )
    require_text(
        "DEPLOY.md",
        "company logical ID → display name → runtime group UUID",
        "Fresh Agent distinguishes group logical IDs from runtime identity",
    )
    require_text(
        "infrastructure/open-webui/PROVISIONING.md",
        "BLOCKED — AMBIGUOUS STATE",
        "Fresh Agent fails closed on ambiguous Open WebUI groups",
    )
    require_text(
        "docs/KNOWLEDGE.md",
        "Open WebUI is not a second company Knowledge authority",
        "Fresh Agent does not duplicate company knowledge in Open WebUI",
    )
    require_text(
        "config/eao-manifest.yaml",
        "hermes: infrastructure/hermes/PROVISIONING.md",
        "Manifest exposes Hermes Core provisioning",
    )
    require_text(
        "config/validated-stack.yaml",
        "https://github.com/Tencent/WeKnora.git",
        "Fresh Agent can resolve WeKnora upstream",
    )
    require_text(
        "config/validated-stack.yaml",
        "https://github.com/NousResearch/hermes-agent.git",
        "Fresh Agent can resolve Hermes upstream",
    )
    require_text(
        "config/validated-stack.yaml",
        "https://github.com/open-webui/open-webui.git",
        "Fresh Agent can resolve Open WebUI upstream",
    )
    require_text(
        "reference/armor/reference-index.yaml",
        "deployable_company_config: false",
        "ARMOR reference index remains non-deployable",
    )
    require_text(
        "reference/armor/reference-index.yaml",
        "live_mailbox_deployment_claim: false",
        "ARMOR reference index does not invent live mailbox state",
    )

    require_text(
        "VALIDATE.md",
        "python3 scripts/check-repository-links.py",
        "Gate 0 includes Markdown link integrity",
    )
    require_text(
        "VALIDATE.md",
        "python3 scripts/check-declarative-paths.py",
        "Gate 0 includes declarative path integrity",
    )
    require_text(
        "VALIDATE.md",
        "python3 scripts/check-capability-acceptance.py",
        "Gate 0 includes capability acceptance integrity",
    )
    require_text(
        "VALIDATE.md",
        "python3 scripts/check-validated-stack-consistency.py",
        "Gate 0 includes validated stack consistency",
    )
    require_text(
        "VALIDATE.md",
        "python3 scripts/check-public-repository-hygiene.py",
        "Gate 0 includes public repository hygiene",
    )
    require_text(
        "VALIDATE.md",
        "python3 scripts/check-frozen-baselines.py",
        "Gate 0 includes frozen baseline history",
    )
    require_text(
        "validation/scorecard.yaml",
        "capability_acceptance_integrity_pass",
        "Scorecard requires capability acceptance integrity",
    )
    require_text(
        "validation/scorecard.yaml",
        "validated_stack_consistency_pass",
        "Scorecard requires validated stack consistency",
    )
    require_text(
        "validation/scorecard.yaml",
        "frozen_baseline_history_pass",
        "Scorecard requires frozen baseline history",
    )
    require_text(
        "validation/REPORT.template.md",
        "python3 scripts/check-frozen-baselines.py",
        "Report records frozen baseline history result",
    )

    for rel in [
        "README.md",
        "README.zh-CN.md",
        "VALIDATE.md",
        "REPRODUCE.md",
        "validation/FRESH-AGENT-TASK.md",
    ]:
        check_markdown_links(rel)

    print("------------------------------------------------")
    print(f"Summary: {PASS} PASS, {FAIL} FAIL")
    print(
        "Static PASS proves the public validation contract is internally present; "
        "it does not prove Fresh-Agent runtime reproduction."
    )
    return 2 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
