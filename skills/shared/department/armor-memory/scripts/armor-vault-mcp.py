#!/usr/bin/env python3
"""Scoped ARMOR Vault MCP server.

This is intentionally not a generic filesystem tool. It exposes only the
deterministic work-product router and closed Article, Social, and MIC package
saves.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROUTER_PATH = SCRIPT_DIR / "armor-route.py"
VAULT_ROOT_ENV = "ARMOR_VAULT_ROOT"
ARTICLE_FILES = frozenset(
    {"article-brief.json", "seo-blueprint.json", "article.md", "audit-report.md"}
)
SOCIAL_REQUIRED_FILES = frozenset(
    {"topic-brief.yaml", "core-draft.md", "social-copy.md", "audit-report.md"}
)
SOCIAL_OPTIONAL_FILES = frozenset({"video-package.md", "subtitles.srt"})
SOCIAL_ALLOWED_FILES = SOCIAL_REQUIRED_FILES | SOCIAL_OPTIONAL_FILES
MIC_REQUIRED_FILES = frozenset(
    {"mic-product-data.yaml", "mic-bulkfill.txt", "mic-audit.md"}
)
MIC_OPTIONAL_FILES = frozenset({"mic-detail-page.md"})
MIC_ALLOWED_FILES = MIC_REQUIRED_FILES | MIC_OPTIONAL_FILES
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_PACKAGE_BYTES = 20 * 1024 * 1024


def _load_router():
    spec = importlib.util.spec_from_file_location("armor_route", ROUTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load ARMOR Router: {ROUTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ROUTER = _load_router()


class ScopedVaultError(ValueError):
    """A safe, user-visible rejection from the scoped Vault boundary."""


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _vault_root() -> Path:
    raw = os.environ.get(VAULT_ROOT_ENV, "").strip()
    if not raw:
        raise ScopedVaultError(f"{VAULT_ROOT_ENV} is required for Vault operations")
    root = Path(raw).expanduser().resolve()
    if not root.is_dir():
        raise ScopedVaultError(f"{VAULT_ROOT_ENV} must name an existing directory")
    return root


def _article_destination(root: Path) -> tuple[str, Path]:
    route = ROUTER.route_request(
        object_type="work-product", domain="website", artifact="article"
    )
    relative = Path(route.path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ScopedVaultError("Router returned an unsafe destination")
    if relative.parts[:2] == ("03-Records", "Published"):
        raise ScopedVaultError("Published evidence cannot be an editable Article source")
    destination = (root / relative).resolve()
    if not _is_under(destination, root):
        raise ScopedVaultError("Router destination escapes ARMOR_VAULT_ROOT")
    return route.path, destination


def _social_destination(root: Path) -> tuple[str, Path]:
    route = ROUTER.route_request(
        object_type="work-product", domain="marketing", artifact="social-copy"
    )
    relative = Path(route.path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ScopedVaultError("Router returned an unsafe Social destination")
    if relative.parts[:2] == ("03-Records", "Published"):
        raise ScopedVaultError("Published evidence cannot be an editable Social source")
    destination = (root / relative).resolve()
    if not _is_under(destination, root):
        raise ScopedVaultError("Social Router destination escapes ARMOR_VAULT_ROOT")
    return route.path, destination


def _mic_destination(root: Path) -> tuple[str, Path]:
    route = ROUTER.route_request(
        object_type="work-product", domain="products", artifact="mic-product"
    )
    relative = Path(route.path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ScopedVaultError("Router returned an unsafe MIC destination")
    if relative.parts[:2] == ("03-Records", "Published"):
        raise ScopedVaultError("Published evidence cannot be an editable MIC source")
    destination = (root / relative).resolve()
    if not _is_under(destination, root):
        raise ScopedVaultError("MIC Router destination escapes ARMOR_VAULT_ROOT")
    return route.path, destination


def _safe_package_dir(root: Path, destination: Path, package_id: str) -> tuple[str, Path]:
    if not isinstance(package_id, str):
        raise ScopedVaultError("package_id must be a string")
    try:
        package_slug = ROUTER.slugify_name(package_id)
    except ValueError as exc:
        raise ScopedVaultError(str(exc)) from exc
    package_dir = destination / package_slug
    if package_dir.is_symlink():
        raise ScopedVaultError("Article package directory must not be a symlink")
    resolved = package_dir.resolve()
    if not _is_under(resolved, root):
        raise ScopedVaultError("Article package escapes ARMOR_VAULT_ROOT")
    return package_slug, package_dir


def _safe_social_package_dir(root: Path, destination: Path, package_id: str) -> tuple[str, Path]:
    if not isinstance(package_id, str):
        raise ScopedVaultError("package_id must be a string")
    try:
        package_slug = ROUTER.slugify_name(package_id)
    except ValueError as exc:
        raise ScopedVaultError(str(exc)) from exc
    package_dir = destination / package_slug
    if package_dir.is_symlink():
        raise ScopedVaultError("Social package directory must not be a symlink")
    resolved = package_dir.resolve()
    if not _is_under(resolved, root):
        raise ScopedVaultError("Social package escapes ARMOR_VAULT_ROOT")
    return package_slug, package_dir


def _safe_mic_package_dir(root: Path, destination: Path, package_id: str) -> tuple[str, Path]:
    if not isinstance(package_id, str):
        raise ScopedVaultError("package_id must be a string")
    try:
        package_slug = ROUTER.slugify_name(package_id)
    except ValueError as exc:
        raise ScopedVaultError(str(exc)) from exc
    package_dir = destination / package_slug
    if package_dir.is_symlink():
        raise ScopedVaultError("MIC package directory must not be a symlink")
    resolved = package_dir.resolve()
    if not _is_under(resolved, root):
        raise ScopedVaultError("MIC package escapes ARMOR_VAULT_ROOT")
    return package_slug, package_dir


def _validate_package(files: Any) -> dict[str, str]:
    if not isinstance(files, dict):
        raise ScopedVaultError("files must be an object containing exactly the four Article files")
    names = set(files)
    if names != ARTICLE_FILES:
        missing = sorted(ARTICLE_FILES - names)
        extra = sorted(names - ARTICLE_FILES)
        details = []
        if missing:
            details.append(f"missing={','.join(missing)}")
        if extra:
            details.append(f"unexpected={','.join(extra)}")
        raise ScopedVaultError("Article package file contract rejected: " + "; ".join(details))
    normalized: dict[str, str] = {}
    total = 0
    for name in ARTICLE_FILES:
        value = files[name]
        if not isinstance(value, str):
            raise ScopedVaultError(f"{name} must be supplied as UTF-8 text")
        encoded = value.encode("utf-8")
        if len(encoded) > MAX_FILE_BYTES:
            raise ScopedVaultError(f"{name} exceeds the per-file size limit")
        total += len(encoded)
        normalized[name] = value
    if total > MAX_PACKAGE_BYTES:
        raise ScopedVaultError("Article package exceeds the total size limit")
    for name in ("article-brief.json", "seo-blueprint.json"):
        try:
            parsed = json.loads(normalized[name])
        except json.JSONDecodeError as exc:
            raise ScopedVaultError(f"{name} must contain valid JSON: {exc.msg}") from exc
        if not isinstance(parsed, dict):
            raise ScopedVaultError(f"{name} must contain a JSON object")
    for name in ("article.md", "audit-report.md"):
        if not normalized[name].strip():
            raise ScopedVaultError(f"{name} must not be empty")
    return normalized


def _validate_social_package(files: Any) -> dict[str, str]:
    if not isinstance(files, dict):
        raise ScopedVaultError(
            "files must be an object containing the required Social files and only approved video files"
        )
    names = set(files)
    missing = sorted(SOCIAL_REQUIRED_FILES - names)
    extra = sorted(names - SOCIAL_ALLOWED_FILES)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing={','.join(missing)}")
        if extra:
            details.append(f"unexpected={','.join(extra)}")
        raise ScopedVaultError("Social package file contract rejected: " + "; ".join(details))
    normalized: dict[str, str] = {}
    total = 0
    for name in names:
        value = files[name]
        if not isinstance(value, str):
            raise ScopedVaultError(f"{name} must be supplied as UTF-8 text")
        encoded = value.encode("utf-8")
        if len(encoded) > MAX_FILE_BYTES:
            raise ScopedVaultError(f"{name} exceeds the per-file size limit")
        if not value.strip():
            raise ScopedVaultError(f"{name} must not be empty")
        total += len(encoded)
        normalized[name] = value
    if total > MAX_PACKAGE_BYTES:
        raise ScopedVaultError("Social package exceeds the total size limit")
    return normalized


def _validate_mic_package(files: Any) -> dict[str, str]:
    if not isinstance(files, dict):
        raise ScopedVaultError(
            "files must contain the required MIC files and optional mic-detail-page.md"
        )
    names = set(files)
    missing = sorted(MIC_REQUIRED_FILES - names)
    extra = sorted(names - MIC_ALLOWED_FILES)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing={','.join(missing)}")
        if extra:
            details.append(f"unexpected={','.join(extra)}")
        raise ScopedVaultError("MIC package file contract rejected: " + "; ".join(details))

    normalized: dict[str, str] = {}
    total = 0
    for name in names:
        value = files[name]
        if not isinstance(value, str):
            raise ScopedVaultError(f"{name} must be supplied as UTF-8 text")
        encoded = value.encode("utf-8")
        if len(encoded) > MAX_FILE_BYTES:
            raise ScopedVaultError(f"{name} exceeds the per-file size limit")
        if not value.strip():
            raise ScopedVaultError(f"{name} must not be empty")
        total += len(encoded)
        normalized[name] = value
    if total > MAX_PACKAGE_BYTES:
        raise ScopedVaultError("MIC package exceeds the total size limit")

    bulkfill = normalized["mic-bulkfill.txt"]
    if "# 产品详情" in bulkfill or "# 产品展示" in bulkfill:
        raise ScopedVaultError("mic-bulkfill.txt must not contain manual-only MIC sections")
    return normalized


def _validate_file_target(path: Path) -> None:
    if path.is_symlink():
        raise ScopedVaultError(f"Refusing to overwrite symlink: {path.name}")
    if path.exists() and not path.is_file():
        raise ScopedVaultError(f"Refusing to overwrite non-file: {path.name}")


def _atomic_write(path: Path, content: str) -> None:
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()


def _save_article_package(arguments: dict[str, Any]) -> dict[str, Any]:
    allowed = {"package_id", "files"}
    if set(arguments) != allowed:
        raise ScopedVaultError("save_article_package accepts only package_id and files")
    root = _vault_root()
    relative, destination = _article_destination(root)
    package_slug, package_dir = _safe_package_dir(root, destination, arguments["package_id"])
    files = _validate_package(arguments["files"])
    existed_before = package_dir.is_dir()

    package_dir.mkdir(parents=True, exist_ok=True)
    if package_dir.is_symlink() or not package_dir.is_dir():
        raise ScopedVaultError("Article package target is not a regular directory")
    resolved_package = package_dir.resolve()
    if not _is_under(resolved_package, root):
        raise ScopedVaultError("Article package escapes ARMOR_VAULT_ROOT")

    targets = {name: package_dir / name for name in ARTICLE_FILES}
    originals: dict[str, bytes | None] = {}
    for name, target in targets.items():
        _validate_file_target(target)
        originals[name] = target.read_bytes() if target.exists() else None

    replaced: list[str] = []
    try:
        for name in sorted(ARTICLE_FILES):
            _atomic_write(targets[name], files[name])
            replaced.append(name)
        for name in sorted(ARTICLE_FILES):
            if targets[name].read_text(encoding="utf-8") != files[name]:
                raise ScopedVaultError(f"Read-back verification failed for {name}")
    except Exception:
        for name in reversed(replaced):
            target = targets[name]
            previous = originals[name]
            if previous is None:
                if target.exists() or target.is_symlink():
                    target.unlink()
            else:
                _atomic_write(target, previous.decode("utf-8"))
        if not existed_before:
            try:
                package_dir.rmdir()
            except OSError:
                pass
        raise

    return {
        "status": "saved",
        "package_id": package_slug,
        "relative_path": f"{relative}{package_slug}/",
        "absolute_path": str(package_dir.resolve()),
        "files": sorted(ARTICLE_FILES),
        "read_back": True,
        "sha256": {
            name: hashlib.sha256(targets[name].read_bytes()).hexdigest()
            for name in sorted(ARTICLE_FILES)
        },
    }


def _save_social_package(arguments: dict[str, Any]) -> dict[str, Any]:
    allowed = {"package_id", "files"}
    if set(arguments) != allowed:
        raise ScopedVaultError("save_social_package accepts only package_id and files")
    root = _vault_root()
    relative, destination = _social_destination(root)
    package_slug, package_dir = _safe_social_package_dir(root, destination, arguments["package_id"])
    files = _validate_social_package(arguments["files"])
    existed_before = package_dir.is_dir()

    package_dir.mkdir(parents=True, exist_ok=True)
    if package_dir.is_symlink() or not package_dir.is_dir():
        raise ScopedVaultError("Social package target is not a regular directory")
    resolved_package = package_dir.resolve()
    if not _is_under(resolved_package, root):
        raise ScopedVaultError("Social package escapes ARMOR_VAULT_ROOT")
    existing_names = {child.name for child in package_dir.iterdir()}
    unexpected_existing = existing_names - set(files)
    if unexpected_existing:
        raise ScopedVaultError(
            "Social package contains files outside the submitted closed contract: "
            + ",".join(sorted(unexpected_existing))
        )

    targets = {name: package_dir / name for name in files}
    originals: dict[str, bytes | None] = {}
    for name, target in targets.items():
        _validate_file_target(target)
        originals[name] = target.read_bytes() if target.exists() else None

    replaced: list[str] = []
    try:
        for name in sorted(files):
            _atomic_write(targets[name], files[name])
            replaced.append(name)
        for name in sorted(files):
            if targets[name].read_text(encoding="utf-8") != files[name]:
                raise ScopedVaultError(f"Read-back verification failed for {name}")
    except Exception:
        for name in reversed(replaced):
            target = targets[name]
            previous = originals[name]
            if previous is None:
                if target.exists() or target.is_symlink():
                    target.unlink()
            else:
                _atomic_write(target, previous.decode("utf-8"))
        if not existed_before:
            try:
                package_dir.rmdir()
            except OSError:
                pass
        raise

    return {
        "status": "saved",
        "package_id": package_slug,
        "relative_path": f"{relative}{package_slug}/",
        "absolute_path": str(package_dir.resolve()),
        "files": sorted(files),
        "read_back": True,
        "sha256": {
            name: hashlib.sha256(targets[name].read_bytes()).hexdigest()
            for name in sorted(files)
        },
    }


def _save_mic_product_package(arguments: dict[str, Any]) -> dict[str, Any]:
    allowed = {"package_id", "files"}
    if set(arguments) != allowed:
        raise ScopedVaultError("save_mic_product_package accepts only package_id and files")
    root = _vault_root()
    relative, destination = _mic_destination(root)
    package_slug, package_dir = _safe_mic_package_dir(root, destination, arguments["package_id"])
    files = _validate_mic_package(arguments["files"])
    existed_before = package_dir.is_dir()

    package_dir.mkdir(parents=True, exist_ok=True)
    if package_dir.is_symlink() or not package_dir.is_dir():
        raise ScopedVaultError("MIC package target is not a regular directory")
    resolved_package = package_dir.resolve()
    if not _is_under(resolved_package, root):
        raise ScopedVaultError("MIC package escapes ARMOR_VAULT_ROOT")
    existing_names = {child.name for child in package_dir.iterdir()}
    unexpected_existing = existing_names - set(files)
    if unexpected_existing:
        raise ScopedVaultError(
            "MIC package contains files outside the submitted closed contract: "
            + ",".join(sorted(unexpected_existing))
        )

    targets = {name: package_dir / name for name in files}
    originals: dict[str, bytes | None] = {}
    for name, target in targets.items():
        _validate_file_target(target)
        originals[name] = target.read_bytes() if target.exists() else None

    replaced: list[str] = []
    try:
        for name in sorted(files):
            _atomic_write(targets[name], files[name])
            replaced.append(name)
        for name in sorted(files):
            if targets[name].read_text(encoding="utf-8") != files[name]:
                raise ScopedVaultError(f"Read-back verification failed for {name}")
    except Exception:
        for name in reversed(replaced):
            target = targets[name]
            previous = originals[name]
            if previous is None:
                if target.exists() or target.is_symlink():
                    target.unlink()
            else:
                _atomic_write(target, previous.decode("utf-8"))
        if not existed_before:
            try:
                package_dir.rmdir()
            except OSError:
                pass
        raise

    return {
        "status": "saved",
        "package_id": package_slug,
        "relative_path": f"{relative}{package_slug}/",
        "absolute_path": str(package_dir.resolve()),
        "files": sorted(files),
        "read_back": True,
        "sha256": {
            name: hashlib.sha256(targets[name].read_bytes()).hexdigest()
            for name in sorted(files)
        },
    }


def _route_work_product(arguments: dict[str, Any]) -> dict[str, Any]:
    allowed = {"domain", "artifact", "project", "entity"}
    if not set(arguments) <= allowed:
        raise ScopedVaultError("route_work_product received an unsupported field")
    if not arguments.get("domain") or not arguments.get("artifact"):
        raise ScopedVaultError("domain and artifact are required")
    if not isinstance(arguments["domain"], str) or not isinstance(arguments["artifact"], str):
        raise ScopedVaultError("domain and artifact must be strings")
    try:
        route = ROUTER.route_request(
            object_type="work-product",
            domain=arguments["domain"],
            artifact=arguments["artifact"],
            project=arguments.get("project"),
            entity=arguments.get("entity"),
        )
    except (KeyError, ValueError) as exc:
        raise ScopedVaultError(str(exc)) from exc
    result: dict[str, Any] = {
        "relative_path": route.path,
        "category": route.category,
        "reason": route.reason,
    }
    if os.environ.get(VAULT_ROOT_ENV):
        root = _vault_root()
        result["absolute_path"] = str((root / route.path).resolve())
    return result


TOOLS = [
    {
        "name": "route_work_product",
        "description": "Map a closed-enum ARMOR work product to its deterministic relative Vault path.",
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "domain": {"type": "string", "enum": list(ROUTER.DOMAIN_CHOICES)},
                "artifact": {"type": "string", "enum": list(ROUTER.ARTIFACT_CHOICES)},
                "project": {"type": "string"},
                "entity": {"type": "string"},
            },
            "required": ["domain", "artifact"],
        },
    },
    {
        "name": "save_article_package",
        "description": "Atomically save exactly the Article v1.3 four-file package under the deterministic Article workspace.",
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "package_id": {"type": "string", "minLength": 1},
                "files": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        name: {"type": "string"} for name in sorted(ARTICLE_FILES)
                    },
                    "required": sorted(ARTICLE_FILES),
                },
            },
            "required": ["package_id", "files"],
        },
    },
    {
        "name": "save_social_package",
        "description": "Atomically save the required Social v2.0 package and only the approved optional video artifacts under the deterministic Social workspace.",
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "package_id": {"type": "string", "minLength": 1},
                "files": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        name: {"type": "string"} for name in sorted(SOCIAL_ALLOWED_FILES)
                    },
                    "required": sorted(SOCIAL_REQUIRED_FILES),
                },
            },
        "required": ["package_id", "files"],
        },
    },
    {
        "name": "save_mic_product_package",
        "description": "Atomically save the closed MIC product package under the deterministic MIC Products workspace.",
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "package_id": {"type": "string", "minLength": 1},
                "files": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        name: {"type": "string"} for name in sorted(MIC_ALLOWED_FILES)
                    },
                    "required": sorted(MIC_REQUIRED_FILES),
                },
            },
            "required": ["package_id", "files"],
        },
    },
]


def _tool_result(payload: dict[str, Any], *, error: bool = False) -> dict[str, Any]:
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(payload, ensure_ascii=False, sort_keys=True),
            }
        ],
        "isError": error,
    }


def _dispatch(message: dict[str, Any]) -> dict[str, Any] | None:
    if "id" not in message:
        return None
    request_id = message["id"]
    method = message.get("method")
    params = message.get("params") or {}
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "armor-vault-scoped-router", "version": "1.0.0"},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        if not isinstance(params, dict):
            return {"jsonrpc": "2.0", "id": request_id, "result": _tool_result({"error": "params must be an object"}, error=True)}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, dict):
            return {"jsonrpc": "2.0", "id": request_id, "result": _tool_result({"error": "arguments must be an object"}, error=True)}
        try:
            if name == "route_work_product":
                payload = _route_work_product(arguments)
            elif name == "save_article_package":
                payload = _save_article_package(arguments)
            elif name == "save_social_package":
                payload = _save_social_package(arguments)
            elif name == "save_mic_product_package":
                payload = _save_mic_product_package(arguments)
            else:
                raise ScopedVaultError(f"Unknown scoped Vault tool: {name}")
            result = _tool_result(payload)
        except (ScopedVaultError, OSError) as exc:
            result = _tool_result({"error": str(exc)}, error=True)
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"},
    }


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            if not isinstance(message, dict):
                continue
            response = _dispatch(message)
            if response is not None:
                sys.stdout.write(json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            continue
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
