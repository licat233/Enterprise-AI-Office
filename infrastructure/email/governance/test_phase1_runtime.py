#!/usr/bin/env python3
"""Offline Phase 1 runtime contract tests; no mailbox or network access."""

from __future__ import annotations

import unittest

from runtime import (
    Actor,
    AuthorizationError,
    AuthorizationPolicy,
    GovernanceService,
    SERVICE_ACTOR_ID,
    CRON_OPERATIONS,
    FORBIDDEN_CRON_OPERATIONS,
    MCP_TOOLS,
    dispatch_mcp,
    ROOT,
)


class FixtureProvider:
    def search_email(self, query):
        return [{"uid": "1", "message_id": "<one@example.invalid>"}]

    def get_email(self, uid, folder="INBOX"):
        return {"uid": uid, "message_id": "<one@example.invalid>"}


class Phase1RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.mailbox = "mailbox-001"
        self.policy = AuthorizationPolicy(
            service_credential="service-secret-for-test",
            service_mailboxes={self.mailbox},
            human_permissions={
                "human:reviewer": {"email.draft", "email.approve", "email.send"},
            },
        )
        self.service = GovernanceService(
            ":memory:",
            policy=self.policy,
            provider=FixtureProvider(),
        )
        self.service_actor = self.policy.authenticate_service_actor(
            "service-secret-for-test"
        )
        self.human = Actor("human", "human:reviewer")
        schema_version = self.service._db.execute(
            "SELECT schema_version FROM schema_meta WHERE schema_name=?",
            ("email_governance",),
        ).fetchone()[0]
        self.assertEqual(schema_version, 2)
        tables = {row[0] for row in self.service._db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        self.assertTrue({"logical_sends", "send_attempts", "send_reconciliations"} <= tables)

    def tearDown(self):
        self.service.close()

    def test_service_actor_identity_and_permission_matrix(self):
        self.assertEqual(self.service_actor.actor_id, SERVICE_ACTOR_ID)
        self.service.search_email(
            self.service_actor, mailbox_id=self.mailbox, query={}
        )
        self.service.get_email(
            self.service_actor, mailbox_id=self.mailbox, uid="1"
        )
        draft = self.service.prepare_reply_draft(
            self.service_actor,
            mailbox_id=self.mailbox,
            source_message_id="<one@example.invalid>",
            to_addresses=["customer@example.invalid"],
            subject="Re: Inquiry",
            body="Draft for human review.",
        )
        self.assertTrue(draft["created"])
        audit = self.service._db.execute(
            """
            SELECT actor_type, actor_id, human_actor_id
            FROM governance_audit_events
            WHERE operation=? AND decision=?
            ORDER BY occurred_at DESC
            LIMIT 1
            """,
            ("prepare_reply_draft", "ALLOW"),
        ).fetchone()
        self.assertEqual(tuple(audit), ("service", SERVICE_ACTOR_ID, None))
        with self.assertRaises(AuthorizationError):
            self.service.authorize_human_approval(
                self.service_actor, mailbox_id=self.mailbox
            )
        with self.assertRaises(AuthorizationError):
            self.service.authorize_human_send(
                self.service_actor, mailbox_id=self.mailbox
            )

    def test_human_approval_and_send_are_separate_from_service_actor(self):
        self.service.authorize_human_approval(self.human, mailbox_id=self.mailbox)
        self.service.authorize_human_send(self.human, mailbox_id=self.mailbox)

    def test_cron_idempotency_replays_mapping_without_new_revision(self):
        first = self.service.prepare_reply_draft(
            self.service_actor,
            mailbox_id=self.mailbox,
            source_message_id="<one@example.invalid>",
            to_addresses=["customer@example.invalid"],
            subject="Re: Inquiry",
            body="First draft.",
            request_key="caller-supplied-value-must-not-change-service-key",
        )
        replay = self.service.prepare_reply_draft(
            self.service_actor,
            mailbox_id=self.mailbox,
            source_message_id="<one@example.invalid>",
            to_addresses=["customer@example.invalid"],
            subject="Re: Inquiry",
            body="Must not overwrite.",
        )
        self.assertFalse(replay["created"])
        self.assertEqual(first["draft"]["draft_id"], replay["draft"]["draft_id"])
        self.assertEqual(
            self.service.draft_revisions(first["draft"]["draft_id"])[-1]["body"],
            "First draft.",
        )

    def test_new_source_message_creates_new_draft(self):
        first = self.service.prepare_reply_draft(
            self.service_actor,
            mailbox_id=self.mailbox,
            source_message_id="<one@example.invalid>",
            to_addresses=["customer@example.invalid"],
            subject="Re: Inquiry",
            body="First draft.",
        )
        second = self.service.prepare_reply_draft(
            self.service_actor,
            mailbox_id=self.mailbox,
            source_message_id="<two@example.invalid>",
            to_addresses=["customer@example.invalid"],
            subject="Re: Inquiry",
            body="Second draft.",
        )
        self.assertNotEqual(first["draft"]["draft_id"], second["draft"]["draft_id"])

    def test_human_revision_is_immutable_and_not_overwritten(self):
        first = self.service.prepare_reply_draft(
            self.service_actor,
            mailbox_id=self.mailbox,
            source_message_id="<one@example.invalid>",
            to_addresses=["customer@example.invalid"],
            subject="Re: Inquiry",
            body="Service draft.",
        )
        self.service.prepare_reply_draft(
            self.human,
            mailbox_id=self.mailbox,
            source_message_id="<one@example.invalid>",
            to_addresses=["customer@example.invalid"],
            subject="Re: Inquiry",
            body="Human revision.",
            request_key="human-revision-001",
            draft_id=first["draft"]["draft_id"],
        )
        replay = self.service.prepare_reply_draft(
            self.service_actor,
            mailbox_id=self.mailbox,
            source_message_id="<one@example.invalid>",
            to_addresses=["customer@example.invalid"],
            subject="Re: Inquiry",
            body="Changed service text.",
        )
        self.assertFalse(replay["created"])
        revisions = self.service.draft_revisions(first["draft"]["draft_id"])
        self.assertEqual([item["body"] for item in revisions], ["Service draft.", "Human revision."])

    def test_only_three_operations_are_exposed_to_cron(self):
        self.assertEqual(
            CRON_OPERATIONS,
            frozenset({"search_email", "get_email", "prepare_reply_draft"}),
        )
        self.assertIn("raw_imap", FORBIDDEN_CRON_OPERATIONS)
        self.assertIn("raw_smtp", FORBIDDEN_CRON_OPERATIONS)
        self.assertIn("approve_reply_draft", FORBIDDEN_CRON_OPERATIONS)
        self.assertIn("send_email", FORBIDDEN_CRON_OPERATIONS)

    def test_mcp_surface_lists_three_tools_and_rejects_send(self):
        listed = dispatch_mcp(
            {"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
            service=self.service,
            actor=self.service_actor,
        )
        self.assertEqual(
            {tool["name"] for tool in listed["result"]["tools"]},
            set(CRON_OPERATIONS),
        )
        self.assertEqual(len(MCP_TOOLS), 3)
        rejected = dispatch_mcp(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "send_approved_reply", "arguments": {}},
            },
            service=self.service,
            actor=self.service_actor,
        )
        self.assertTrue(rejected["result"]["isError"])
        self.assertEqual(
            rejected["result"]["content"][0]["text"],
            '{"reason": "OPERATION_NOT_EXPOSED", "status": "FAILURE"}',
        )

    def test_wrong_service_credential_is_denied_without_exposing_secret(self):
        with self.assertRaises(AuthorizationError):
            self.policy.authenticate_service_actor("wrong-secret")

    def test_operations_high_risk_boundary_and_skills_remain_closed(self):
        config = (ROOT / "private/department-profile/config.yaml").read_text(
            encoding="utf-8"
        )
        for toolset in (
            "web",
            "browser",
            "terminal",
            "file",
            "code_execution",
            "delegation",
            "cronjob",
            "memory",
            "computer_use",
            "image_gen",
        ):
            self.assertIn(f"    - {toolset}", config)
        enabled = (
            ROOT / "private/department-profile/enabled-skills.csv"
        ).read_text(encoding="utf-8")
        self.assertIn("sales-discovery-coach", enabled)
        self.assertIn("sales-coach", enabled)
        self.assertIn("product-marketing", enabled)
        self.assertNotIn("email-inbox-triage", enabled)


if __name__ == "__main__":
    unittest.main()
