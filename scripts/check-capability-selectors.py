#!/usr/bin/env python3
"""Validate capability selectors and required deployment-record metadata.

This is intentionally dependency-free and checks stable selector paths against
the company schema plus the rule that every conditional capability and every
Production Ready control declares what non-secret operational evidence must be
recorded after deployment.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPS = ROOT / "config" / "capabilities.yaml"
COMPANY = ROOT / "config" / "company.example.yaml"
PRIVATE_COMPANY = ROOT / "config" / "company.private.example.yaml"

CAP_RE = re.compile(r"^  ([A-Za-z0-9_.-]+):\s*$")
KEY_RE = re.compile(r"^(\s*)([A-Za-z0-9_.-]+):(?:\s|$)")


def company_paths(text: str) -> set[str]:
    paths: set[str] = set()
    stack: list[tuple[int, str]] = []

    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        normalized = line
        stripped = normalized.lstrip()
        if stripped.startswith("- "):
            indent = len(normalized) - len(stripped)
            normalized = " " * indent + stripped[2:]
        match = KEY_RE.match(normalized)
        if not match:
            continue

        indent = len(match.group(1))
        key = match.group(2)
        while stack and stack[-1][0] >= indent:
            stack.pop()
        stack.append((indent, key))
        paths.add(".".join(item[1] for item in stack))

    return paths


def selector_blocks(text: str) -> list[tuple[str, str, list[str], str]]:
    lines = text.splitlines()
    current = ""
    result: list[tuple[str, str, list[str], str]] = []
    i = 0

    while i < len(lines):
        cap = CAP_RE.match(lines[i])
        if cap:
            current = cap.group(1)

        if lines[i] != "    selection:":
            i += 1
            continue

        source = ""
        scope = ""
        paths: list[str] = []
        i += 1
        while i < len(lines):
            line = lines[i]
            if line and len(line) - len(line.lstrip(" ")) <= 4:
                break
            stripped = line.strip()
            if stripped.startswith("source:"):
                source = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("scope:"):
                scope = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("path:"):
                paths.append(stripped.split(":", 1)[1].strip())
            elif stripped.startswith("- path:"):
                paths.append(stripped.split(":", 1)[1].strip())
            i += 1

        result.append((current or "<unknown>", source, paths, scope))

    return result


def conditional_capabilities(text: str) -> set[str]:
    lines = text.splitlines()
    current = ""
    result: set[str] = set()
    for line in lines:
        cap = CAP_RE.match(line)
        if cap:
            current = cap.group(1)
            continue
        if current and line.strip() == "kind: conditional":
            result.add(current)
    return result


def recorded_capabilities(text: str) -> set[str]:
    lines = text.splitlines()
    current = ""
    result: set[str] = set()
    for line in lines:
        cap = CAP_RE.match(line)
        if cap:
            current = cap.group(1)
            continue
        if current and line == "    records:":
            result.add(current)
    return result


def production_controls(text: str) -> set[str]:
    result: set[str] = set()
    in_production = False
    for line in text.splitlines():
        if line == "production_controls:":
            in_production = True
            continue
        if not in_production:
            continue
        if line and not line.startswith(" "):
            break
        control = CAP_RE.match(line)
        if control:
            result.add(control.group(1))
    return result


def declared_profile_ids(text: str) -> set[str]:
    result: set[str] = set()
    lines = text.splitlines()
    in_profiles = False
    base_indent = 0

    for raw in lines:
        stripped = raw.strip()
        if not in_profiles:
            if stripped == "profiles:" and len(raw) - len(raw.lstrip(" ")) == 0:
                in_profiles = True
                base_indent = 0
            continue

        if not stripped:
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        if indent <= base_indent:
            break

        match = re.match(r"^\s*-\s+id:\s*([A-Za-z0-9_.-]+)\s*$", raw)
        if match:
            result.add(match.group(1))

    return result


def profile_api_key_refs(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    lines = text.splitlines()
    in_block = False
    base_indent = 0

    for raw in lines:
        stripped = raw.strip()
        if not in_block:
            if stripped == "profile_api_key_refs:":
                in_block = True
                base_indent = len(raw) - len(raw.lstrip(" "))
            continue

        if not stripped:
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        if indent <= base_indent:
            break

        match = re.match(r"^\s*([A-Za-z0-9_.-]+):\s*(.*?)\s*$", raw)
        if match:
            value = match.group(2).strip().strip("'\"")
            result[match.group(1)] = "" if value in {"", "null", "~"} else value

    return result


def default_api_key_ref(text: str) -> str:
    match = re.search(r"^\s+default_api_key_ref:\s*(.*?)\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip().strip("'\"")
    return "" if value in {"", "null", "~"} else value


def top_level_block(text: str, name: str) -> str:
    lines = text.splitlines()
    result: list[str] = []
    in_block = False

    for raw in lines:
        if not in_block:
            if raw.strip() == f"{name}:" and len(raw) - len(raw.lstrip(" ")) == 0:
                in_block = True
                result.append(raw)
            continue

        if raw.strip() and len(raw) - len(raw.lstrip(" ")) == 0:
            break
        result.append(raw)

    return "\n".join(result)


def mapping_values(text: str, header: str) -> list[str]:
    values: list[str] = []
    lines = text.splitlines()
    in_block = False
    base_indent = 0

    for raw in lines:
        stripped = raw.strip()
        if not in_block:
            if stripped == f"{header}:":
                in_block = True
                base_indent = len(raw) - len(raw.lstrip(" "))
            continue

        if not stripped:
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        if indent <= base_indent:
            break

        match = re.match(r"^\s*[A-Za-z0-9_.-]+:\s*(.*?)\s*$", raw)
        if match:
            value = match.group(1).strip().strip("'\"")
            if value not in {"", "null", "~"}:
                values.append(value)

    return values


def secret_ref_metadata(text: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    lines = text.splitlines()
    in_block = False
    current_ref = ""

    for raw in lines:
        stripped = raw.strip()
        if not in_block:
            if stripped == "secret_refs:" and len(raw) - len(raw.lstrip(" ")) == 0:
                # Public shape may intentionally use secret_refs: {}.
                if raw.split(":", 1)[1].strip():
                    return result
                in_block = True
            continue

        if not stripped:
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 0:
            break

        ref_match = re.match(r"^  ([A-Za-z0-9_.-]+):\s*$", raw)
        if ref_match:
            current_ref = ref_match.group(1)
            result[current_ref] = {}
            continue

        field_match = re.match(r"^    ([A-Za-z0-9_.-]+):\s*(.*?)\s*$", raw)
        if field_match and current_ref:
            value = field_match.group(2).strip().strip("'\"")
            result[current_ref][field_match.group(1)] = value

    return result


def secret_ref_names(text: str) -> set[str]:
    return set(secret_ref_metadata(text))


def core_provisioning_symbolic_refs(text: str) -> set[str]:
    block = top_level_block(text, "core_provisioning")
    if not block:
        return set()

    result: set[str] = set()

    for match in re.finditer(r"^\s+password_ref:\s*(.*?)\s*$", block, flags=re.MULTILINE):
        value = match.group(1).strip().strip("'\"")
        if value not in {"", "null", "~"}:
            result.add(value)

    default_ref = default_api_key_ref(block)
    if default_ref:
        result.add(default_ref)

    result.update(mapping_values(block, "profile_api_key_refs"))
    result.update(mapping_values(block, "runtime_secret_refs"))
    return result


def validate_core_secret_ref_metadata(
    label: str,
    text: str,
    failures: list[str],
) -> int:
    refs = core_provisioning_symbolic_refs(text)
    metadata = secret_ref_metadata(text)
    required_fields = ("class", "consumer", "native_binding")

    for ref in sorted(refs):
        if ref not in metadata:
            failures.append(
                f"{label}: Core provisioning symbolic ref is not declared in secret_refs: {ref}"
            )
            continue

        for field_name in required_fields:
            value = metadata[ref].get(field_name, "").strip()
            if not value or value in {"null", "~"}:
                failures.append(
                    f"{label}: secret_refs.{ref} missing non-empty {field_name}"
                )

    return len(refs)


def validate_profile_credential_contract(
    label: str,
    text: str,
    failures: list[str],
) -> tuple[int, int]:
    profiles = declared_profile_ids(text)
    refs = profile_api_key_refs(text)
    secrets = secret_ref_names(text)

    for profile_id in sorted(profiles):
        if profile_id not in refs:
            failures.append(
                f"{label}: declared Profile has no core_provisioning.hermes.profile_api_key_refs entry: {profile_id}"
            )

    checked_refs = 0
    for profile_id, ref in sorted(refs.items()):
        if not ref:
            continue
        checked_refs += 1
        if ref not in secrets:
            failures.append(
                f"{label}: Profile API-key ref is not declared in secret_refs: {profile_id} -> {ref}"
            )

    default_ref = default_api_key_ref(text)
    if default_ref:
        checked_refs += 1
        if default_ref not in secrets:
            failures.append(
                f"{label}: default Hermes API-key ref is not declared in secret_refs: {default_ref}"
            )

    return len(profiles), checked_refs


def main() -> int:
    if not CAPS.is_file() or not COMPANY.is_file() or not PRIVATE_COMPANY.is_file():
        print("FAIL required config file missing")
        return 2

    caps_text = CAPS.read_text(encoding="utf-8")
    company_text = COMPANY.read_text(encoding="utf-8")
    private_company_text = PRIVATE_COMPANY.read_text(encoding="utf-8")

    schema_paths = company_paths(company_text)
    selectors = selector_blocks(caps_text)
    conditional = conditional_capabilities(caps_text)
    production = production_controls(caps_text)
    recorded = recorded_capabilities(caps_text)
    failures: list[str] = []

    if "operational_records_contract:" not in caps_text:
        failures.append("registry: missing operational_records_contract")
    if "sink_template: state/DEPLOYMENT-STATE.template.md" not in caps_text:
        failures.append("registry: operational records sink must be state/DEPLOYMENT-STATE.template.md")
    if "record_every_declared_records_item_for_each_enabled_capability" not in caps_text:
        failures.append("registry: conditional capability records sink rule is missing")
    if "secret_values_in_record: forbidden" not in caps_text:
        failures.append("registry: records contract must forbid secret values")
    selected_names = {name for name, _, _, _ in selectors}

    public_profile_count, public_credential_refs = validate_profile_credential_contract(
        "config/company.example.yaml",
        company_text,
        failures,
    )
    private_profile_count, private_credential_refs = validate_profile_credential_contract(
        "config/company.private.example.yaml",
        private_company_text,
        failures,
    )

    public_core_secret_refs = validate_core_secret_ref_metadata(
        "config/company.example.yaml",
        company_text,
        failures,
    )
    private_core_secret_refs = validate_core_secret_ref_metadata(
        "config/company.private.example.yaml",
        private_company_text,
        failures,
    )

    for capability in sorted(conditional):
        if capability not in selected_names:
            failures.append(f"{capability}: conditional capability has no selection metadata")
        if capability not in recorded:
            failures.append(f"{capability}: conditional capability has no records metadata")

    for control in sorted(production):
        if control not in recorded:
            failures.append(f"{control}: production control has no records metadata")

    checked_paths = 0
    for capability, source, paths, scope in selectors:
        if scope == "ARMOR_reference_specific":
            if source == "company_configuration":
                failures.append(
                    f"{capability}: ARMOR-specific selector must not masquerade as generic company schema"
                )
            continue

        if source != "company_configuration":
            failures.append(
                f"{capability}: generic selector must declare source: company_configuration"
            )
            continue

        if not paths:
            failures.append(f"{capability}: company selector declares no path")
            continue

        for path in paths:
            checked_paths += 1
            if path not in schema_paths:
                failures.append(
                    f"{capability}: selector path missing from config/company.example.yaml: {path}"
                )

    print("Enterprise AI Office Capability Selector Integrity")
    print("------------------------------------------------")
    print(f"Conditional capabilities: {len(conditional)}")
    print(f"Selector blocks: {len(selectors)}")
    print(f"Conditional record blocks: {len(conditional & recorded)}")
    print(f"Production controls: {len(production)}")
    print(f"Production control record blocks: {len(production & recorded)}")
    print(f"Company selector paths checked: {checked_paths}")
    print(
        "Profile credential mappings checked: "
        f"{public_profile_count + private_profile_count} declared Profiles / "
        f"{public_credential_refs + private_credential_refs} non-empty refs"
    )
    print(
        "Core provisioning symbolic refs checked: "
        f"{public_core_secret_refs + private_core_secret_refs}"
    )

    if failures:
        print(f"Selector failures: {len(failures)}")
        for failure in failures:
            print(f"FAIL {failure}")
        return 2

    print("Selector/record failures: 0")
    print("CAPABILITY SELECTOR / RECORD INTEGRITY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
