"""Deterministic, realpath-based authorization for Hermes skill_manage mutations.

The module intentionally has no Hermes imports. It can therefore be tested with
temporary fixtures and reused by the Hermes plugin registration entry point.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional


MUTATION_ACTIONS = frozenset(
    {"create", "edit", "patch", "delete", "write_file", "remove_file"}
)
BATCH_ACTIONS = frozenset({"create", "patch", "write_file", "remove_file"})
ALLOWED_SUPPORT_DIRS = frozenset({"references", "templates", "scripts", "assets"})
VALID_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
VALID_NAMESPACE_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*-$")


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def _block(reason: str) -> dict[str, str]:
    return {
        "action": "block",
        "message": f"EAO Skill mutation guard blocked skill_manage: {reason}",
    }


@dataclass(frozen=True)
class SkillMutationGuard:
    """Authorize only learned namespace mutations under one resolved root."""

    profile_name: str
    learning_root: Optional[Path]
    allowed_namespace: Optional[str]
    configuration_error: Optional[str] = None

    @classmethod
    def from_config(
        cls,
        *,
        profile_name: str,
        learning_root: Any,
        allowed_namespace: Any,
    ) -> "SkillMutationGuard":
        errors = []
        resolved_root: Optional[Path] = None

        if not isinstance(profile_name, str) or not profile_name.strip():
            errors.append("active Profile is missing")
        if not isinstance(learning_root, (str, os.PathLike)) or not str(learning_root).strip():
            errors.append("learning_root is missing")
        else:
            try:
                root_candidate = Path(os.path.expanduser(os.fspath(learning_root)))
                if not root_candidate.is_absolute():
                    errors.append("learning_root must be absolute after expansion")
                else:
                    resolved_root = root_candidate.resolve(strict=True)
                    if not resolved_root.is_dir():
                        errors.append("learning_root is not a directory")
            except (OSError, RuntimeError, TypeError, ValueError):
                errors.append("learning_root cannot be resolved safely")

        namespace = allowed_namespace if isinstance(allowed_namespace, str) else None
        if not namespace or not VALID_NAMESPACE_RE.fullmatch(namespace):
            errors.append("allowed_namespace is missing or invalid")

        return cls(
            profile_name=str(profile_name),
            learning_root=resolved_root,
            allowed_namespace=namespace,
            configuration_error="; ".join(errors) if errors else None,
        )

    def pre_tool_call(
        self,
        *,
        tool_name: Any,
        args: Any,
        **_: Any,
    ) -> Optional[dict[str, str]]:
        """Return a Hermes block directive for unsafe skill_manage calls.

        Returning None leaves read-only tools and authorized learned mutations
        unchanged. Every internal error is converted to a block directive.
        """
        if tool_name != "skill_manage":
            return None

        try:
            if self.configuration_error:
                return _block(f"guard configuration is invalid ({self.configuration_error})")
            if self.learning_root is None or self.allowed_namespace is None:
                return _block("guard configuration is incomplete")
            if not isinstance(args, Mapping):
                return _block("tool arguments are malformed")

            operations = args.get("operations")
            if operations is not None:
                return self._check_batch(operations, args.get("name"))

            return self._check_single(args)
        except Exception:
            return _block("mutation could not be classified safely")

    def _check_single(self, args: Mapping[str, Any]) -> Optional[dict[str, str]]:
        action = args.get("action")
        if not isinstance(action, str) or action not in MUTATION_ACTIONS:
            return _block("operation is unknown or unsupported")

        name = args.get("name")
        reason = self._namespace_reason(name)
        if reason:
            return _block(reason)

        if action == "create":
            category = args.get("category")
            category_reason = self._category_reason(category)
            if category_reason:
                return _block(category_reason)
            target = self._create_target(name, category)
            if reason := self._authorize_path(target, allow_missing=True):
                return _block(reason)
            return None

        candidate = self._find_existing(str(name))
        if candidate is None:
            return _block("Skill target is unknown or not in the learning root")

        if reason := self._authorize_existing(candidate):
            return _block(reason)

        if action in {"patch", "write_file", "remove_file"}:
            file_path = args.get("file_path")
            if action == "patch" and file_path is None:
                file_path = "SKILL.md"
            if not self._safe_file_path(file_path):
                return _block("supporting file path is malformed or escapes the Skill")

            if reason := self._authorize_file(candidate, str(file_path)):
                return _block(reason)

        return None

    def _check_batch(
        self,
        operations: Any,
        default_name: Any,
    ) -> Optional[dict[str, str]]:
        if not isinstance(operations, list) or not operations:
            return _block("batch operations are malformed")

        planned_creates: dict[str, Path] = {}
        for operation in operations:
            if not isinstance(operation, Mapping):
                return _block("batch operation is malformed")

            action = operation.get("action")
            name = operation.get("name") or default_name
            if action == "delete":
                if len(operations) != 1:
                    return _block("delete must be the sole batch operation")
            elif action not in BATCH_ACTIONS:
                return _block("batch operation is unknown or unsupported")

            reason = self._namespace_reason(name)
            if reason:
                return _block(reason)

            if action == "create":
                category_reason = self._category_reason(operation.get("category"))
                if category_reason:
                    return _block(category_reason)
                target = self._create_target(str(name), operation.get("category"))
                if reason := self._authorize_path(target, allow_missing=True):
                    return _block(reason)
                planned_creates[str(name)] = target
                continue

            candidate = planned_creates.get(str(name))
            if candidate is None:
                candidate = self._find_existing(str(name))
                if candidate is None:
                    return _block("batch Skill target is unknown or not in the learning root")
                if reason := self._authorize_existing(candidate):
                    return _block(reason)
            else:
                if reason := self._authorize_path(candidate, allow_missing=True):
                    return _block(reason)

            if action in {"patch", "write_file", "remove_file"}:
                file_path = operation.get("file_path")
                if action == "patch" and file_path is None:
                    file_path = "SKILL.md"
                if not self._safe_file_path(file_path):
                    return _block("batch supporting file path is malformed or escapes the Skill")
                if reason := self._authorize_file(candidate, str(file_path)):
                    return _block(reason)

        return None

    def _namespace_reason(self, name: Any) -> Optional[str]:
        if not isinstance(name, str) or not VALID_NAME_RE.fullmatch(name):
            return "Skill name is malformed"
        if self.allowed_namespace is None or not name.startswith(self.allowed_namespace):
            return "Skill name is outside the allowed learned namespace"
        if len(name) == len(self.allowed_namespace):
            return "learned namespace requires a Skill name suffix"
        return None

    @staticmethod
    def _category_reason(category: Any) -> Optional[str]:
        if category is None or category == "":
            return None
        if not isinstance(category, str) or not VALID_NAME_RE.fullmatch(category):
            return "Skill category is malformed"
        return None

    def _create_target(self, name: str, category: Any) -> Path:
        target = self.learning_root / name  # type: ignore[operator]
        if category:
            target = self.learning_root / str(category) / name  # type: ignore[operator]
        return target

    def _authorize_path(self, candidate: Path, *, allow_missing: bool) -> Optional[str]:
        try:
            resolved = candidate.resolve(strict=False)
        except (OSError, RuntimeError, ValueError):
            return "Skill target cannot be resolved safely"
        if self.learning_root is None or not _inside(self.learning_root, resolved):
            return "resolved Skill target escapes the learning root"
        if not allow_missing and not candidate.exists():
            return "Skill target does not exist"
        return None

    def _find_existing(self, name: str) -> Optional[Path]:
        if self.learning_root is None:
            return None

        direct = self.learning_root / name
        if os.path.lexists(str(direct)):
            return direct

        try:
            for directory, dirnames, _ in os.walk(
                self.learning_root, topdown=True, followlinks=False
            ):
                dirnames.sort()
                if name in dirnames:
                    return Path(directory) / name
        except (OSError, RuntimeError):
            return None
        return None

    def _authorize_existing(self, candidate: Path) -> Optional[str]:
        if reason := self._authorize_path(candidate, allow_missing=False):
            return reason
        try:
            resolved = candidate.resolve(strict=True)
            skill_md = candidate / "SKILL.md"
            if not resolved.is_dir() or not skill_md.is_file():
                return "Skill target is not a complete local Skill"
            if not _inside(self.learning_root, skill_md.resolve(strict=True)):  # type: ignore[arg-type]
                return "Skill file escapes the learning root"
        except (OSError, RuntimeError, ValueError):
            return "Skill target cannot be resolved safely"
        return None

    @staticmethod
    def _safe_file_path(file_path: Any) -> bool:
        if not isinstance(file_path, str) or not file_path or "\x00" in file_path:
            return False
        path = Path(file_path)
        if path.is_absolute():
            return False
        parts = path.parts
        if not parts or any(part in {".", ".."} for part in parts):
            return False
        if parts[-1] == "SKILL.md" and len(parts) in {1, 2}:
            return True
        return parts[0] in ALLOWED_SUPPORT_DIRS and len(parts) >= 2

    def _authorize_file(self, candidate: Path, file_path: str) -> Optional[str]:
        target = candidate / file_path
        try:
            resolved = target.resolve(strict=False)
        except (OSError, RuntimeError, ValueError):
            return "mutation file cannot be resolved safely"
        if self.learning_root is None or not _inside(self.learning_root, resolved):
            return "mutation file escapes the learning root"
        return None
