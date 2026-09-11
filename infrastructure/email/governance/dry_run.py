#!/usr/bin/env python3
"""Safe operator-side Phase 1 dry run with synthetic email data only."""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Mapping

from runtime import (
    Actor,
    AuthorizationPolicy,
    GovernanceService,
    SERVICE_ACTOR_ID,
)


class FixtureProvider:
    def search_email(self, query: Mapping[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "uid": "fixture-001",
                "message_id": "<synthetic-inquiry-001@example.invalid>",
                "subject": "Synthetic product inquiry",
                "from": ["synthetic-customer@example.invalid"],
                "to": ["pilot@example.invalid"],
                "body": "Please provide a synthetic quotation.",
            }
        ]

    def get_email(self, uid: str, folder: str = "INBOX") -> dict[str, Any]:
        return self.search_email({})[0]


def main() -> None:
    mailbox_id = "synthetic-pilot-mailbox"
    source_message_id = "<synthetic-inquiry-001@example.invalid>"
    policy = AuthorizationPolicy(
        service_credential="dry-run-only",
        service_mailboxes={mailbox_id},
        human_permissions={
            "human:operator-001": {"email.draft", "email.approve", "email.send"},
        },
    )
    service = GovernanceService(
        ":memory:",
        policy=policy,
        provider=FixtureProvider(),
    )
    try:
        actor = policy.authenticate_service_actor("dry-run-only")
        message = service.get_email(
            actor,
            mailbox_id=mailbox_id,
            uid="fixture-001",
        )
        decision = "DRAFT_FOR_REVIEW"
        first = service.prepare_reply_draft(
            actor,
            mailbox_id=mailbox_id,
            source_message_id=source_message_id,
            to_addresses=["synthetic-customer@example.invalid"],
            subject="Re: Synthetic product inquiry",
            body="Thank you for the synthetic inquiry. A human operator must review this draft.",
        )
        replay = service.prepare_reply_draft(
            actor,
            mailbox_id=mailbox_id,
            source_message_id=source_message_id,
            to_addresses=["synthetic-customer@example.invalid"],
            subject="Re: Synthetic product inquiry",
            body="This changed body must not overwrite the existing draft.",
        )
        human = Actor("human", "human:operator-001")
        service.prepare_reply_draft(
            human,
            mailbox_id=mailbox_id,
            source_message_id=source_message_id,
            to_addresses=["synthetic-customer@example.invalid"],
            subject="Re: Synthetic product inquiry",
            body="Human revision for review.",
            request_key="human-revision-key",
            draft_id=first["draft"]["draft_id"],
        )
        revisions = service.draft_revisions(first["draft"]["draft_id"])
        assert decision == "DRAFT_FOR_REVIEW"
        assert message["message_id"] == source_message_id
        assert replay["created"] is False
        assert len(revisions) == 2
        assert revisions[-1]["body"] == "Human revision for review."
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "decision": decision,
                    "message_id": source_message_id,
                    "draft_id": first["draft"]["draft_id"],
                    "revisions": len(revisions),
                    "idempotent_replay": True,
                    "customer_send": "NOT_PERFORMED",
                    "service_actor": SERVICE_ACTOR_ID,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    finally:
        service.close()


if __name__ == "__main__":
    main()
