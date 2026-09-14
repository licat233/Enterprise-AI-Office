#!/usr/bin/env python3
"""Deterministic v1A EAO operation-envelope contract.

This module is intentionally side-effect free. It is a small adapter primitive
for a future Open WebUI Action/control-plane binding: it does not call a
network, write a file, execute a command, or persist approval state.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import re
from typing import Any, Mapping


DEFAULT_APPROVAL_TTL_MINUTES = 30
MAX_APPROVAL_TTL_MINUTES = 30
SIGNATURE_PREFIX = "hmac-sha256:"
ALLOWED_OPERATION_TYPES = frozenset(
    {
        "resource_classification",
        "capability_reuse_review",
        "knowledge_ingestion",
        "skill_review",
        "tool_review",
        "mcp_backend_review",
    }
)
FORBIDDEN_KEYS = frozenset(
    {
        "api_key",
        "command",
        "credential",
        "docker",
        "executable",
        "exec",
        "filesystem_write",
        "package_manager",
        "password",
        "private_key",
        "secret",
        "shell",
        "sudo",
        "token",
    }
)


class EnvelopeError(ValueError):
    """A deterministic operation-envelope validation failure."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _clone(value: Any) -> Any:
    return json.loads(_canonical(value))


def _parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EnvelopeError("INVALID_TIME", "timestamp must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise EnvelopeError("INVALID_TIME", "timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def _now(value: datetime | None) -> datetime:
    current = value or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise EnvelopeError("INVALID_TIME", "current time must include a timezone")
    return current.astimezone(timezone.utc)


def _validate_ttl(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise EnvelopeError("INVALID_TTL", "approval TTL must be an integer")
    if value < 1 or value > MAX_APPROVAL_TTL_MINUTES:
        raise EnvelopeError(
            "INVALID_TTL",
            f"approval TTL must be between 1 and {MAX_APPROVAL_TTL_MINUTES} minutes",
        )
    return value


def _require_signing_key(signing_key: bytes | bytearray | memoryview | None) -> bytes:
    if signing_key is None:
        raise EnvelopeError(
            "SIGNING_KEY_MISSING",
            "protected server-side signing key is required",
        )
    if not isinstance(signing_key, (bytes, bytearray, memoryview)):
        raise EnvelopeError("SIGNING_KEY_INVALID", "signing key must be bytes")
    key = bytes(signing_key)
    if not key:
        raise EnvelopeError(
            "SIGNING_KEY_MISSING",
            "protected server-side signing key is required",
        )
    return key


def _reject_forbidden_keys(value: Any, path: str = "plan") -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in FORBIDDEN_KEYS:
                raise EnvelopeError(
                    "FORBIDDEN_FIELD",
                    f"{path}.{key} is not allowed in an operation envelope",
                )
            _reject_forbidden_keys(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _reject_forbidden_keys(nested, f"{path}[{index}]")


def _validate_operation_id(operation_id: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9._:-]{7,127}", operation_id):
        raise EnvelopeError(
            "INVALID_OPERATION_ID",
            "operation_id must be a stable lowercase identifier of 8-128 chars",
        )


@dataclass(frozen=True)
class TrustedHumanContext:
    """Identity resolved by a server-side Open WebUI Action."""

    actor_id: str
    group_ids: tuple[str, ...]

    @classmethod
    def from_open_webui(cls, user: Mapping[str, Any]) -> "TrustedHumanContext":
        actor_id = str(user.get("id", "")).strip()
        if not actor_id:
            raise EnvelopeError("ACTOR_UNRESOLVED", "Open WebUI actor id is missing")
        groups = user.get("group_ids", ())
        if isinstance(groups, str):
            groups = (groups,)
        return cls(actor_id=actor_id, group_ids=tuple(sorted(str(x) for x in groups)))


@dataclass(frozen=True)
class OperationEnvelope:
    operation_id: str
    operation_type: str
    source_identity: Mapping[str, Any]
    source_fingerprint: str
    target: Mapping[str, Any]
    material_change_summary: str
    security_impact: str
    profile_exposure_impact: str
    runtime_impact: str
    expected_current_state: Mapping[str, Any]
    created_at: str
    expires_at: str
    immutable_plan_hash: str
    trusted_plan_signature: str

    def plan(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type,
            "source_identity": _clone(self.source_identity),
            "source_fingerprint": self.source_fingerprint,
            "target": _clone(self.target),
            "material_change_summary": self.material_change_summary,
            "security_impact": self.security_impact,
            "profile_exposure_impact": self.profile_exposure_impact,
            "runtime_impact": self.runtime_impact,
            "expected_current_state": _clone(self.expected_current_state),
            "created_at": self.created_at,
            "expires_at": self.expires_at,
        }

    def as_dict(self) -> dict[str, Any]:
        """Return model-safe fields; the trusted binding stays server-side."""
        result = self.plan()
        result["immutable_plan_hash"] = self.immutable_plan_hash
        return result

    def as_persisted_dict(self) -> dict[str, Any]:
        """Return the server-side persisted form, never a model/browser payload."""
        result = self.as_dict()
        result["trusted_plan_signature"] = self.trusted_plan_signature
        return result


def compute_plan_hash(plan: Mapping[str, Any]) -> str:
    """Hash the exact material plan, excluding the hash field itself."""

    material = dict(plan)
    material.pop("immutable_plan_hash", None)
    material.pop("trusted_plan_signature", None)
    _reject_forbidden_keys(material)
    return "sha256:" + hashlib.sha256(_canonical(material).encode("utf-8")).hexdigest()


def compute_plan_signature(
    plan: Mapping[str, Any],
    signing_key: bytes | bytearray | memoryview | None,
) -> str:
    """Bind the canonical plan and its hash to a protected server-side key."""

    key = _require_signing_key(signing_key)
    material = dict(plan)
    material.pop("immutable_plan_hash", None)
    material.pop("trusted_plan_signature", None)
    _reject_forbidden_keys(material)
    plan_hash = compute_plan_hash(material)
    signed_payload = _canonical({"plan": material, "plan_hash": plan_hash})
    digest = hmac.new(key, signed_payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return SIGNATURE_PREFIX + digest


def verify_plan_signature(
    envelope: OperationEnvelope,
    signing_key: bytes | bytearray | memoryview | None,
) -> None:
    """Reject missing or invalid trusted binding for an operation envelope."""

    if not envelope.trusted_plan_signature:
        raise EnvelopeError("SIGNATURE_MISSING", "trusted plan signature is missing")
    expected = compute_plan_signature(envelope.plan(), signing_key)
    if not hmac.compare_digest(envelope.trusted_plan_signature, expected):
        raise EnvelopeError("SIGNATURE_INVALID", "trusted plan signature is invalid")


def build_envelope(
    *,
    operation_id: str,
    operation_type: str,
    source_identity: Mapping[str, Any],
    source_fingerprint: str,
    target: Mapping[str, Any],
    material_change_summary: str,
    security_impact: str,
    profile_exposure_impact: str,
    runtime_impact: str,
    expected_current_state: Mapping[str, Any],
    created_at: str,
    expires_at: str | None = None,
    approval_ttl_minutes: int = DEFAULT_APPROVAL_TTL_MINUTES,
    signing_key: bytes | bytearray | memoryview | None = None,
) -> OperationEnvelope:
    _validate_operation_id(operation_id)
    if operation_type not in ALLOWED_OPERATION_TYPES:
        raise EnvelopeError("UNKNOWN_OPERATION", operation_type)
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", source_fingerprint):
        raise EnvelopeError(
            "INVALID_FINGERPRINT",
            "source fingerprint must be sha256:<64 lowercase hex chars>",
        )
    ttl_minutes = _validate_ttl(approval_ttl_minutes)
    created = _parse_time(created_at)
    expires = (
        created + timedelta(minutes=ttl_minutes)
        if expires_at is None
        else _parse_time(expires_at)
    )
    if expires <= created:
        raise EnvelopeError("INVALID_EXPIRY", "expiry must be after creation")
    if expires - created > timedelta(minutes=ttl_minutes):
        raise EnvelopeError("INVALID_TTL", "expiry exceeds the explicit approval TTL")
    plan = {
        "operation_id": operation_id,
        "operation_type": operation_type,
        "source_identity": _clone(source_identity),
        "source_fingerprint": source_fingerprint,
        "target": _clone(target),
        "material_change_summary": material_change_summary,
        "security_impact": security_impact,
        "profile_exposure_impact": profile_exposure_impact,
        "runtime_impact": runtime_impact,
        "expected_current_state": _clone(expected_current_state),
        "created_at": created,
        "expires_at": expires,
    }
    plan["created_at"] = created.isoformat().replace("+00:00", "Z")
    plan["expires_at"] = expires.isoformat().replace("+00:00", "Z")
    _reject_forbidden_keys(plan)
    immutable_plan_hash = compute_plan_hash(plan)
    return OperationEnvelope(
        operation_id=operation_id,
        operation_type=operation_type,
        source_identity=_clone(source_identity),
        source_fingerprint=source_fingerprint,
        target=_clone(target),
        material_change_summary=material_change_summary,
        security_impact=security_impact,
        profile_exposure_impact=profile_exposure_impact,
        runtime_impact=runtime_impact,
        expected_current_state=_clone(expected_current_state),
        created_at=plan["created_at"],
        expires_at=plan["expires_at"],
        immutable_plan_hash=immutable_plan_hash,
        trusted_plan_signature=compute_plan_signature(plan, signing_key),
    )


def approve_envelope(
    envelope: OperationEnvelope,
    *,
    human: TrustedHumanContext,
    required_group_id: str,
    current_state: Mapping[str, Any],
    approved_at: datetime,
    signing_key: bytes | bytearray | memoryview | None = None,
) -> dict[str, Any]:
    """Validate exact-plan approval and return non-authoritative evidence.

    The caller must persist/execute this result through the approved control
    plane. This helper never performs the material operation itself.
    """

    if not human.actor_id:
        raise EnvelopeError("ACTOR_UNRESOLVED", "trusted actor is missing")
    if required_group_id not in human.group_ids:
        raise EnvelopeError("APPROVER_UNAUTHORIZED", "required group is absent")
    now = _now(approved_at)
    if now >= _parse_time(envelope.expires_at):
        raise EnvelopeError("APPROVAL_EXPIRED", "operation envelope has expired")
    if compute_plan_hash(envelope.plan()) != envelope.immutable_plan_hash:
        raise EnvelopeError("APPROVAL_INVALIDATED", "immutable plan hash does not match")
    verify_plan_signature(envelope, signing_key)
    if _canonical(current_state) != _canonical(envelope.expected_current_state):
        raise EnvelopeError("APPROVAL_INVALIDATED", "expected current state changed")
    return {
        "operation_id": envelope.operation_id,
        "immutable_plan_hash": envelope.immutable_plan_hash,
        "approved_by_human_actor": human.actor_id,
        "approved_at": now.isoformat().replace("+00:00", "Z"),
        "status": "APPROVED_NOT_EXECUTED",
    }


def classify_replay(existing_result: str | None) -> str:
    """Return the safe result for a retried operation_id."""

    if existing_result in {"SUCCEEDED", "CONFIRMED_NOT_APPLIED", "BLOCKED"}:
        return "ALREADY_RESOLVED"
    if existing_result == "OUTCOME_UNKNOWN":
        return "RECONCILIATION_REQUIRED"
    return "NEW_OPERATION"
