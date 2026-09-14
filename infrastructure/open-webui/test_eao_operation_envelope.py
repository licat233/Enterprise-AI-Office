#!/usr/bin/env python3
"""Offline checks for the v1A operation-envelope boundary."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import json

from eao_operation_envelope import (
    EnvelopeError,
    TrustedHumanContext,
    approve_envelope,
    build_envelope,
    classify_replay,
    compute_plan_hash,
)


NOW = datetime(2026, 9, 14, 10, 0, tzinfo=timezone.utc)
SOURCE_FINGERPRINT = "sha256:" + hashlib.sha256(b"source-v1").hexdigest()
SIGNING_KEY = b"offline-test-only-protected-key"


def make_envelope():
    return build_envelope(
        operation_id="op-eao-knowledge-001",
        operation_type="knowledge_ingestion",
        source_identity={"kind": "url", "canonical_uri": "https://example.invalid/policy"},
        source_fingerprint=SOURCE_FINGERPRINT,
        target={"knowledge_base_id": "company-general", "status": "current"},
        material_change_summary="Add one reviewed external reference to Company Knowledge.",
        security_impact="External Reference; public source; no credential content.",
        profile_exposure_impact="No Profile exposure change.",
        runtime_impact="Bounded WeKnora ingestion only after approval.",
        expected_current_state={"source_present": False, "target_version": "v1"},
        created_at="2026-09-14T10:00:00Z",
        expires_at="2026-09-14T10:30:00Z",
        signing_key=SIGNING_KEY,
    )


def main() -> None:
    envelope = make_envelope()
    assert envelope.immutable_plan_hash == compute_plan_hash(envelope.plan())
    assert compute_plan_hash(envelope.as_persisted_dict()) == envelope.immutable_plan_hash
    assert envelope.trusted_plan_signature.startswith("hmac-sha256:")
    assert "trusted_plan_signature" not in envelope.as_dict()
    assert envelope.as_persisted_dict()["trusted_plan_signature"]

    # Canonical JSON makes key order irrelevant, while material edits change the hash.
    assert compute_plan_hash({"b": 2, "a": 1}) == compute_plan_hash({"a": 1, "b": 2})
    changed = envelope.as_dict()
    changed["target"] = {"knowledge_base_id": "other-kb", "status": "current"}
    assert compute_plan_hash(changed) != envelope.immutable_plan_hash

    approved = approve_envelope(
        envelope,
        human=TrustedHumanContext("open-webui:admin-001", ("eao-administrators",)),
        required_group_id="eao-administrators",
        current_state={"source_present": False, "target_version": "v1"},
        approved_at=NOW,
        signing_key=SIGNING_KEY,
    )
    assert approved["status"] == "APPROVED_NOT_EXECUTED"
    assert approved["approved_by_human_actor"] == "open-webui:admin-001"

    cases = [
        ("wrong group", {"required_group_id": "all-employees"}, "APPROVER_UNAUTHORIZED"),
        ("changed state", {"current_state": {"source_present": True}}, "APPROVAL_INVALIDATED"),
        ("expired", {"approved_at": datetime(2026, 9, 14, 10, 30, tzinfo=timezone.utc)}, "APPROVAL_EXPIRED"),
    ]
    for label, overrides, expected in cases:
        kwargs = {
            "human": TrustedHumanContext("open-webui:admin-001", ("eao-administrators",)),
            "required_group_id": "eao-administrators",
            "current_state": {"source_present": False, "target_version": "v1"},
            "approved_at": NOW,
            "signing_key": SIGNING_KEY,
        }
        kwargs.update(overrides)
        try:
            approve_envelope(envelope, **kwargs)
        except EnvelopeError as exc:
            assert exc.code == expected, (label, exc.code)
        else:
            raise AssertionError(f"{label} unexpectedly approved")

    signature_cases = [
        (
            "missing signature",
            replace(envelope, trusted_plan_signature=""),
            SIGNING_KEY,
            "SIGNATURE_MISSING",
        ),
        (
            "invalid signature",
            replace(envelope, trusted_plan_signature="hmac-sha256:" + "0" * 64),
            SIGNING_KEY,
            "SIGNATURE_INVALID",
        ),
        ("wrong key", envelope, b"a-different-protected-key", "SIGNATURE_INVALID"),
    ]
    for label, candidate, key, expected in signature_cases:
        try:
            approve_envelope(
                candidate,
                human=TrustedHumanContext(
                    "open-webui:admin-001", ("eao-administrators",)
                ),
                required_group_id="eao-administrators",
                current_state={"source_present": False, "target_version": "v1"},
                approved_at=NOW,
                signing_key=key,
            )
        except EnvelopeError as exc:
            assert exc.code == expected, (label, exc.code)
        else:
            raise AssertionError(f"{label} unexpectedly approved")

    try:
        build_envelope(
            operation_id="op-eao-key-001",
            operation_type="resource_classification",
            source_identity={"kind": "text", "canonical_uri": "urn:eao:key"},
            source_fingerprint=SOURCE_FINGERPRINT,
            target={"classification": "external_reference"},
            material_change_summary="classify",
            security_impact="none",
            profile_exposure_impact="none",
            runtime_impact="none",
            expected_current_state={},
            created_at="2026-09-14T10:00:00Z",
        )
    except EnvelopeError as exc:
        assert exc.code == "SIGNING_KEY_MISSING"
    else:
        raise AssertionError("missing protected signing key unexpectedly accepted")

    generated = build_envelope(
        operation_id="op-eao-ttl-001",
        operation_type="resource_classification",
        source_identity={"kind": "text", "canonical_uri": "urn:eao:ttl"},
        source_fingerprint=SOURCE_FINGERPRINT,
        target={"classification": "external_reference"},
        material_change_summary="classify",
        security_impact="none",
        profile_exposure_impact="none",
        runtime_impact="none",
        expected_current_state={},
        created_at="2026-09-14T10:00:00Z",
        signing_key=SIGNING_KEY,
    )
    assert generated.expires_at == "2026-09-14T10:30:00Z"

    lowered = build_envelope(
        operation_id="op-eao-ttl-002",
        operation_type="resource_classification",
        source_identity={"kind": "text", "canonical_uri": "urn:eao:ttl-2"},
        source_fingerprint=SOURCE_FINGERPRINT,
        target={"classification": "external_reference"},
        material_change_summary="classify",
        security_impact="none",
        profile_exposure_impact="none",
        runtime_impact="none",
        expected_current_state={},
        created_at="2026-09-14T10:00:00Z",
        expires_at="2026-09-14T10:15:00Z",
        approval_ttl_minutes=15,
        signing_key=SIGNING_KEY,
    )
    assert lowered.expires_at == "2026-09-14T10:15:00Z"

    ttl_cases = [
        {"expires_at": "2026-09-14T10:31:00Z", "expected": "INVALID_TTL"},
        {"expires_at": "2026-09-14T09:59:00Z", "expected": "INVALID_EXPIRY"},
        {"approval_ttl_minutes": 31, "expected": "INVALID_TTL"},
    ]
    for overrides in ttl_cases:
        kwargs = {
            "operation_id": "op-eao-ttl-case",
            "operation_type": "resource_classification",
            "source_identity": {"kind": "text", "canonical_uri": "urn:eao:ttl-case"},
            "source_fingerprint": SOURCE_FINGERPRINT,
            "target": {"classification": "external_reference"},
            "material_change_summary": "classify",
            "security_impact": "none",
            "profile_exposure_impact": "none",
            "runtime_impact": "none",
            "expected_current_state": {},
            "created_at": "2026-09-14T10:00:00Z",
            "signing_key": SIGNING_KEY,
        }
        expected = overrides.pop("expected")
        kwargs.update(overrides)
        try:
            build_envelope(**kwargs)
        except EnvelopeError as exc:
            assert exc.code == expected, (overrides, exc.code)
        else:
            raise AssertionError(f"TTL case unexpectedly accepted: {overrides}")

    try:
        build_envelope(
            operation_id="op-eao-fingerprint-001",
            operation_type="resource_classification",
            source_identity={
                "kind": "text",
                "canonical_uri": "urn:eao:bad-fingerprint",
            },
            source_fingerprint="sha256:not-a-real-digest",
            target={"classification": "external_reference"},
            material_change_summary="classify",
            security_impact="none",
            profile_exposure_impact="none",
            runtime_impact="none",
            expected_current_state={},
            created_at="2026-09-14T10:00:00Z",
            signing_key=SIGNING_KEY,
        )
    except EnvelopeError as exc:
        assert exc.code == "INVALID_FINGERPRINT"
    else:
        raise AssertionError("invalid source fingerprint unexpectedly accepted")

    try:
        build_envelope(
            operation_id="op-eao-dangerous-001",
            operation_type="knowledge_ingestion",
            source_identity={"kind": "url", "canonical_uri": "https://example.invalid"},
            source_fingerprint=SOURCE_FINGERPRINT,
            target={"shell": "rm -rf"},
            material_change_summary="unsafe",
            security_impact="unsafe",
            profile_exposure_impact="unsafe",
            runtime_impact="unsafe",
            expected_current_state={},
            created_at="2026-09-14T10:00:00Z",
            expires_at="2026-09-14T10:30:00Z",
            signing_key=SIGNING_KEY,
        )
    except EnvelopeError as exc:
        assert exc.code == "FORBIDDEN_FIELD"
    else:
        raise AssertionError("forbidden raw command field unexpectedly accepted")

    assert classify_replay(None) == "NEW_OPERATION"
    assert classify_replay("SUCCEEDED") == "ALREADY_RESOLVED"
    assert classify_replay("OUTCOME_UNKNOWN") == "RECONCILIATION_REQUIRED"

    # The serialized envelope is JSON-safe and contains no secret-bearing field.
    json.dumps(envelope.as_dict(), sort_keys=True)
    assert all(key not in envelope.as_dict() for key in ("token", "password", "command"))
    print("PASS — v1A EAO operation-envelope/approval boundary")


if __name__ == "__main__":
    main()
