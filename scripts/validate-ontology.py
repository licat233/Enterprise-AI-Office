#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "PyYAML>=6,<7",
# ]
# ///

"""Validate Enterprise AI Office Ontology design examples.

This is deliberately a structural validator, not an Ontology runtime or
business-policy engine. It checks mechanical consistency that has already
caused schema drift during the design experiments.

Run from the repository root with:

    uv run scripts/validate-ontology.py

Or pass one or more YAML files/directories explicitly.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
OBJECT_PROP_RE = re.compile(r"\b([A-Z][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)\b")
OBJECT_CALL_RE = re.compile(r"\b([A-Z][A-Za-z0-9_]*)\s*\(")
TOKEN_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_.]*\b")
AUTHORITY_CLASSES = {"source-backed", "ontology-owned", "derived"}
RESERVED_EXPR_TOKENS = {"true", "false", "none", "null", "and", "or", "not"}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_mapping(
    loader: yaml.Loader,
    node: yaml.Node,
    deep: bool = False,
) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


class Validator:
    def __init__(self, path: Path, doc: dict[str, Any]):
        self.path = path
        self.doc = doc
        self.errors: list[str] = []
        self.systems = self._mapping(doc.get("systems"), "systems")
        self.objects = self._mapping(doc.get("objects"), "objects")
        self.relations = self._mapping(doc.get("relations", {}), "relations")
        self.read_operations = self._mapping(doc.get("read_operations", {}), "read_operations")
        self.actions = self._mapping(doc.get("actions", {}), "actions")

    def error(self, location: str, message: str) -> None:
        self.errors.append(f"{location}: {message}")

    def _mapping(self, value: Any, location: str) -> dict[str, Any]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            self.error(location, "must be a mapping")
            return {}
        return value

    def validate(self) -> list[str]:
        self._validate_root()
        self._validate_objects()
        self._validate_relations()
        self._validate_read_operations()
        self._validate_actions()
        self._validate_operation_surface()
        return self.errors

    def _validate_root(self) -> None:
        version = self.doc.get("schema_version")
        if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
            self.error("schema_version", "must be a quoted semantic version like 0.3.0")

        if self.doc.get("kind") != "enterprise-ontology-example":
            self.error("kind", "must be enterprise-ontology-example")

        metadata = self._mapping(self.doc.get("metadata"), "metadata")
        if metadata:
            if metadata.get("source_contract") != "docs/ONTOLOGY.md":
                self.error("metadata.source_contract", "must reference docs/ONTOLOGY.md")

            meta_version = metadata.get("version")
            if not isinstance(meta_version, str) or not SEMVER_RE.fullmatch(meta_version):
                self.error("metadata.version", "must be a semantic version")

            contract_version = metadata.get("source_contract_version")
            if contract_version is not None and (
                not isinstance(contract_version, str)
                or not SEMVER_RE.fullmatch(contract_version)
            ):
                self.error(
                    "metadata.source_contract_version",
                    "must be a semantic version when present",
                )

            if metadata.get("normative") is not False:
                self.error("metadata.normative", "design examples must remain false")

            if metadata.get("runtime_enforcement") is not False:
                self.error(
                    "metadata.runtime_enforcement",
                    "design examples must remain false",
                )

        if not self.systems:
            self.error("systems", "must declare at least one conceptual system/authority")

        if not self.objects:
            self.error("objects", "must declare at least one Object Type")

    def _validate_authority(
        self,
        authority: Any,
        location: str,
        *,
        allow_derived: bool = True,
    ) -> None:
        if not isinstance(authority, dict):
            self.error(location, "authority must be a mapping")
            return

        authority_class = authority.get("class")
        if authority_class not in AUTHORITY_CLASSES:
            self.error(
                location + ".class",
                f"must be one of {sorted(AUTHORITY_CLASSES)}",
            )
            return

        if authority_class == "derived":
            if not allow_derived:
                self.error(location + ".class", "derived is not valid here")
            for ref in authority.get("inputs", []) or []:
                self._validate_property_ref(ref, location + ".inputs")
            return

        system = authority.get("system")
        if not isinstance(system, str) or system not in self.systems:
            self.error(
                location + ".system",
                f"references unknown system {system!r}",
            )

    def _validate_objects(self) -> None:
        for object_name, raw in self.objects.items():
            location = f"objects.{object_name}"
            if not isinstance(raw, dict):
                self.error(location, "must be a mapping")
                continue

            properties = self._mapping(raw.get("properties"), location + ".properties")
            identity = self._mapping(raw.get("identity"), location + ".identity")
            primary_key = identity.get("primary_key")
            if not isinstance(primary_key, str) or primary_key not in properties:
                self.error(
                    location + ".identity.primary_key",
                    f"must reference a declared property on {object_name}",
                )

            if "authority" in identity:
                self._validate_authority(
                    identity.get("authority"),
                    location + ".identity.authority",
                )

            visibility = self._mapping(raw.get("visibility"), location + ".visibility")
            if visibility.get("default") != "deny":
                self.error(
                    location + ".visibility.default",
                    "operational design examples must fail closed with deny",
                )

            read_requirements = visibility.get("read_requirements")
            if not isinstance(read_requirements, list) or not read_requirements:
                self.error(
                    location + ".visibility.read_requirements",
                    "must declare at least one read requirement",
                )

            for property_name, prop in properties.items():
                property_location = f"{location}.properties.{property_name}"
                if not isinstance(prop, dict):
                    self.error(property_location, "must be a mapping")
                    continue
                self._validate_authority(
                    prop.get("authority"),
                    property_location + ".authority",
                )

    def _validate_relations(self) -> None:
        for relation_name, raw in self.relations.items():
            location = f"relations.{relation_name}"
            if not isinstance(raw, dict):
                self.error(location, "must be a mapping")
                continue

            for field in ("from", "to"):
                target = raw.get(field)
                if target not in self.objects:
                    self.error(
                        f"{location}.{field}",
                        f"references unknown Object Type {target!r}",
                    )

            self._validate_authority(
                raw.get("authority"),
                location + ".authority",
                allow_derived=False,
            )

            binding = raw.get("binding")
            if binding is not None:
                if not isinstance(binding, dict):
                    self.error(location + ".binding", "must be a mapping")
                else:
                    for field in ("source_property", "target_property"):
                        if field in binding:
                            self._validate_property_ref(
                                binding[field],
                                f"{location}.binding.{field}",
                            )

    def _validate_read_operations(self) -> None:
        for name, raw in self.read_operations.items():
            location = f"read_operations.{name}"
            if not isinstance(raw, dict):
                self.error(location, "must be a mapping")
                continue

            target = raw.get("target")
            if target not in self.objects:
                self.error(
                    location + ".target",
                    f"references unknown Object Type {target!r}",
                )
                continue

            entitlements = self._entitlements(
                raw.get("actor_requirements"),
                location + ".actor_requirements",
            )
            required = set(self._object_entitlements(target))

            for field in ("filters", "projections"):
                values = raw.get(field, []) or []
                if not isinstance(values, list):
                    self.error(f"{location}.{field}", "must be a list")
                    continue
                for ref in values:
                    object_name = self._validate_property_ref(
                        ref,
                        f"{location}.{field}",
                    )
                    if object_name:
                        required.update(self._object_entitlements(object_name))

            traversals = raw.get("traversals", []) or []
            if not isinstance(traversals, list):
                self.error(location + ".traversals", "must be a list")
                traversals = []

            for relation_name in traversals:
                relation = self.relations.get(relation_name)
                if not isinstance(relation, dict):
                    self.error(
                        location + ".traversals",
                        f"references unknown Relation {relation_name!r}",
                    )
                    continue

                for endpoint in (relation.get("from"), relation.get("to")):
                    if isinstance(endpoint, str):
                        required.update(self._object_entitlements(endpoint))
                required.update(
                    self._requirement_entitlements(relation.get("read_requirements"))
                )

            self._require_entitlements(entitlements, required, location)
            self._validate_tool_binding(
                raw.get("tool_binding"),
                location + ".tool_binding",
            )

    def _validate_actions(self) -> None:
        for name, raw in self.actions.items():
            location = f"actions.{name}"
            if not isinstance(raw, dict):
                self.error(location, "must be a mapping")
                continue

            target = raw.get("target")
            if target not in self.objects:
                self.error(
                    location + ".target",
                    f"references unknown Object Type {target!r}",
                )
                continue

            parameters = self._mapping(
                raw.get("parameters", {}),
                location + ".parameters",
            )
            entitlements = self._entitlements(
                raw.get("actor_requirements"),
                location + ".actor_requirements",
            )
            required = set(self._object_entitlements(target))

            preconditions = raw.get("preconditions", []) or []
            if not isinstance(preconditions, list):
                self.error(location + ".preconditions", "must be a list")
                preconditions = []

            for index, precondition in enumerate(preconditions):
                precondition_location = f"{location}.preconditions[{index}]"
                if not isinstance(precondition, dict):
                    self.error(precondition_location, "must be a mapping")
                    continue

                rule = precondition.get("rule")
                if isinstance(rule, str):
                    for object_name, property_name in OBJECT_PROP_RE.findall(rule):
                        self._validate_property_ref(
                            f"{object_name}.{property_name}",
                            precondition_location + ".rule",
                        )
                        required.update(self._object_entitlements(object_name))

                    for object_name in OBJECT_CALL_RE.findall(rule):
                        if object_name not in self.objects:
                            self.error(
                                precondition_location + ".rule",
                                f"references unknown Object Type {object_name!r}",
                            )
                        else:
                            required.update(self._object_entitlements(object_name))

            approval = raw.get("approval")
            if approval is not None:
                self._validate_approval(
                    approval,
                    location + ".approval",
                    required,
                )

            self._require_entitlements(entitlements, required, location)
            self._validate_authority(
                raw.get("authority"),
                location + ".authority",
                allow_derived=False,
            )
            self._validate_tool_binding(
                raw.get("tool_binding"),
                location + ".tool_binding",
            )
            self._validate_effects(
                raw.get("effects", []) or [],
                location + ".effects",
            )
            self._validate_failure_behavior(
                raw.get("failure_behavior"),
                parameters,
                location + ".failure_behavior",
            )

    def _validate_approval(
        self,
        approval: Any,
        location: str,
        required_entitlements: set[str],
    ) -> None:
        if not isinstance(approval, dict):
            self.error(location, "must be a mapping")
            return

        mode = approval.get("mode")
        if mode not in {"none", "explicit-human-approval", "role-based-approval"}:
            self.error(
                location + ".mode",
                "must be none, explicit-human-approval, or role-based-approval",
            )

        binding = approval.get("binding")
        if binding is None:
            return
        if not isinstance(binding, dict):
            self.error(location + ".binding", "must be a mapping")
            return

        for key, value in binding.items():
            if key == "relation":
                relation = self.relations.get(value)
                if not isinstance(relation, dict):
                    self.error(
                        location + ".binding.relation",
                        f"references unknown Relation {value!r}",
                    )
                    continue

                for endpoint in (relation.get("from"), relation.get("to")):
                    if isinstance(endpoint, str):
                        required_entitlements.update(
                            self._object_entitlements(endpoint)
                        )
                required_entitlements.update(
                    self._requirement_entitlements(
                        relation.get("read_requirements")
                    )
                )

            elif isinstance(value, str) and "." in value:
                object_name = self._validate_property_ref(
                    value,
                    f"{location}.binding.{key}",
                )
                if object_name:
                    required_entitlements.update(
                        self._object_entitlements(object_name)
                    )

    def _validate_effects(self, effects: Any, location: str) -> None:
        if not isinstance(effects, list):
            self.error(location, "must be a list")
            return

        for index, effect in enumerate(effects):
            effect_location = f"{location}[{index}]"
            if not isinstance(effect, dict):
                self.error(effect_location, "must be a mapping")
                continue

            system = effect.get("system")
            if system is not None and system not in self.systems:
                self.error(
                    effect_location + ".system",
                    f"references unknown system {system!r}",
                )

            object_name = effect.get("object")
            if object_name is not None and object_name not in self.objects:
                self.error(
                    effect_location + ".object",
                    f"references unknown Object Type {object_name!r}",
                )

            property_ref = effect.get("property")
            if property_ref is not None:
                self._validate_property_ref(
                    property_ref,
                    effect_location + ".property",
                )

    def _validate_failure_behavior(
        self,
        behavior: Any,
        parameters: dict[str, Any],
        location: str,
    ) -> None:
        if behavior is None:
            return
        if not isinstance(behavior, dict):
            self.error(location, "must be a mapping")
            return

        expression = behavior.get("idempotency_key")
        if not isinstance(expression, str):
            return

        for token in TOKEN_RE.findall(expression):
            if token.lower() in RESERVED_EXPR_TOKENS:
                continue
            if token.startswith("actor."):
                continue
            if "." in token:
                object_name, _, _ = token.partition(".")
                if object_name in self.objects:
                    self._validate_property_ref(
                        token,
                        location + ".idempotency_key",
                    )
                    continue
                self.error(
                    location + ".idempotency_key",
                    f"uses undeclared reference {token!r}",
                )
                continue
            if token not in parameters:
                self.error(
                    location + ".idempotency_key",
                    f"uses undeclared action parameter {token!r}",
                )

    def _validate_operation_surface(self) -> None:
        surface = self.doc.get("operation_surface")
        if surface is None:
            return
        if not isinstance(surface, dict):
            self.error("operation_surface", "must be a mapping")
            return

        for name in surface.get("reads", []) or []:
            if name not in self.read_operations:
                self.error(
                    "operation_surface.reads",
                    f"references unknown Read Operation {name!r}",
                )

        for name in surface.get("actions", []) or []:
            if name not in self.actions:
                self.error(
                    "operation_surface.actions",
                    f"references unknown Action {name!r}",
                )

    def _validate_tool_binding(self, binding: Any, location: str) -> None:
        if not isinstance(binding, dict):
            self.error(location, "must be a mapping")
            return

        operation = binding.get("operation")
        if not isinstance(operation, str) or "." not in operation:
            self.error(
                location + ".operation",
                "must be a namespaced operation like crm.get_inquiry",
            )
            return

        system = operation.split(".", 1)[0]
        if system not in self.systems:
            self.error(
                location + ".operation",
                f"references unknown system namespace {system!r}",
            )

    def _validate_property_ref(self, ref: Any, location: str) -> str | None:
        if not isinstance(ref, str) or "." not in ref:
            self.error(
                location,
                f"expected Object.property reference, got {ref!r}",
            )
            return None

        object_name, property_name = ref.split(".", 1)
        raw = self.objects.get(object_name)
        if not isinstance(raw, dict):
            self.error(
                location,
                f"references unknown Object Type {object_name!r}",
            )
            return None

        properties = raw.get("properties")
        if not isinstance(properties, dict) or property_name not in properties:
            self.error(location, f"references unknown property {ref!r}")
            return object_name

        return object_name

    def _object_entitlements(self, object_name: Any) -> list[str]:
        raw = self.objects.get(object_name)
        if not isinstance(raw, dict):
            return []
        visibility = raw.get("visibility")
        if not isinstance(visibility, dict):
            return []
        return self._requirement_entitlements(
            visibility.get("read_requirements")
        )

    @staticmethod
    def _requirement_entitlements(requirements: Any) -> list[str]:
        if not isinstance(requirements, list):
            return []
        result: list[str] = []
        for item in requirements:
            if isinstance(item, dict) and isinstance(
                item.get("entitlement"),
                str,
            ):
                result.append(item["entitlement"])
        return result

    def _entitlements(self, requirements: Any, location: str) -> set[str]:
        if not isinstance(requirements, dict):
            self.error(location, "must be a mapping")
            return set()

        entitlements = requirements.get("entitlements", [])
        if not isinstance(entitlements, list) or not all(
            isinstance(item, str) for item in entitlements
        ):
            self.error(
                location + ".entitlements",
                "must be a list of strings",
            )
            return set()
        return set(entitlements)

    def _require_entitlements(
        self,
        actual: set[str],
        required: Iterable[str],
        location: str,
    ) -> None:
        missing = sorted(set(required) - actual)
        if missing:
            self.error(
                location + ".actor_requirements.entitlements",
                f"missing authorization closure: {missing}",
            )


def load_yaml(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = yaml.load(handle, Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as exc:
        print(
            f"ERROR {path}: YAML load failed: {exc}",
            file=sys.stderr,
        )
        return None

    if not isinstance(value, dict):
        print(
            f"ERROR {path}: top-level YAML value must be a mapping",
            file=sys.stderr,
        )
        return None

    return value


def discover_paths(arguments: list[str]) -> list[Path]:
    if arguments:
        discovered: list[Path] = []
        for raw in arguments:
            path = Path(raw)
            if path.is_dir():
                discovered.extend(sorted(path.glob("*.yaml")))
                discovered.extend(sorted(path.glob("*.yml")))
            else:
                discovered.append(path)
        return discovered

    repo_root = Path(__file__).resolve().parents[1]
    return sorted((repo_root / "ontology" / "examples").glob("*.y*ml"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Enterprise AI Office ontology design examples."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="YAML files or directories; defaults to ontology/examples",
    )
    args = parser.parse_args()

    paths = discover_paths(args.paths)
    if not paths:
        print("ERROR: no ontology example YAML files found", file=sys.stderr)
        return 2

    failed = False
    for path in paths:
        doc = load_yaml(path)
        if doc is None:
            failed = True
            continue

        errors = Validator(path, doc).validate()
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
