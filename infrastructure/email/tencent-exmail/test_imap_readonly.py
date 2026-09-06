#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "mcp>=2,<3",
# ]
# ///

"""Deterministic tests for the Tencent Exmail read-only MCP adapter.

These tests do not contact a real mailbox. They verify the local safety contract:
- mailbox selection is read-only;
- folder scope fails closed;
- search uses UID SEARCH/FETCH only;
- message bodies use BODY.PEEK;
- no write-capable IMAP command is issued by the supported operations.

All identities in this public test file are synthetic. Never use a real employee
or company mailbox identifier in public fixtures/tests.
"""

from __future__ import annotations

import os
import unittest
from contextlib import contextmanager
from unittest.mock import patch

import imap_readonly_mcp as adapter


TEST_MAILBOX = "pilot@example.invalid"

MESSAGE_BYTES = b"""From: Customer <customer@example.invalid>\r\nTo: pilot@example.invalid\r\nSubject: Test inquiry\r\nDate: Sat, 06 Sep 2026 10:00:00 +0000\r\nMessage-ID: <msg-1@example.invalid>\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nHello Example Company.\r\n"""

HEADER_BYTES = b"""From: Customer <customer@example.invalid>\r\nTo: pilot@example.invalid\r\nSubject: Test inquiry\r\nDate: Sat, 06 Sep 2026 10:00:00 +0000\r\nMessage-ID: <msg-1@example.invalid>\r\n\r\n"""


class FakeIMAP:
    def __init__(self) -> None:
        self.calls: list[tuple] = []
        self.selected: tuple[str, bool] | None = None
        self.logged_in = False
        self.logged_out = False

    def login(self, username: str, password: str):
        self.calls.append(("login", username, "<redacted>"))
        self.logged_in = True
        return "OK", [b"logged in"]

    def select(self, folder: str, readonly: bool = False):
        self.calls.append(("select", folder, readonly))
        self.selected = (folder, readonly)
        return "OK", [b"1"]

    def uid(self, command: str, *args):
        self.calls.append(("uid", command, *args))
        normalized = command.lower()
        if normalized == "search":
            return "OK", [b"101"]
        if normalized == "fetch":
            uid = str(args[0])
            query = str(args[1])
            if "HEADER.FIELDS" in query:
                metadata = f"{uid} (RFC822.SIZE {len(MESSAGE_BYTES)} BODY[HEADER.FIELDS ...] {{{len(HEADER_BYTES)}}}".encode()
                return "OK", [(metadata, HEADER_BYTES), b")"]
            if "BODY.PEEK[]" in query:
                metadata = f"{uid} (BODY[]<0> {{{len(MESSAGE_BYTES)}}}".encode()
                return "OK", [(metadata, MESSAGE_BYTES), b")"]
        raise AssertionError(f"Unexpected IMAP UID command: {command!r} {args!r}")

    def logout(self):
        self.calls.append(("logout",))
        self.logged_out = True
        return "BYE", [b"logout"]


class ReadOnlyAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = patch.dict(
            os.environ,
            {
                "EAIO_EMAIL_USERNAME": TEST_MAILBOX,
                "EAIO_EMAIL_CLIENT_PASSWORD": "test-only-secret",
                "EAIO_EMAIL_ALLOWED_FOLDERS": "INBOX",
                "EAIO_EMAIL_SEARCH_SCAN_LIMIT": "100",
                "EAIO_EMAIL_MAX_BODY_BYTES": "262144",
            },
            clear=False,
        )
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_folder_scope_fails_closed(self) -> None:
        self.assertEqual(adapter._validate_folder("INBOX"), "INBOX")
        with self.assertRaises(ValueError):
            adapter._validate_folder("Sent")

    def test_readonly_mailbox_selects_readonly(self) -> None:
        fake = FakeIMAP()
        with patch.object(adapter.imaplib, "IMAP4_SSL", return_value=fake):
            with adapter._readonly_mailbox("INBOX") as client:
                self.assertIs(client, fake)

        self.assertEqual(fake.selected, ("INBOX", True))
        self.assertTrue(fake.logged_in)
        self.assertTrue(fake.logged_out)

    def test_search_email_uses_only_read_operations(self) -> None:
        fake = FakeIMAP()

        @contextmanager
        def mailbox(_folder: str):
            yield fake

        with patch.object(adapter, "_readonly_mailbox", mailbox):
            result = adapter.search_email(subject_contains="inquiry", limit=5)

        self.assertEqual(result["count"], 1)
        self.assertEqual(result["messages"][0]["uid"], "101")
        self._assert_no_write_commands(fake)
        uid_commands = [call for call in fake.calls if call[0] == "uid"]
        self.assertTrue(any(call[1].lower() == "search" for call in uid_commands))
        self.assertTrue(any(call[1].lower() == "fetch" for call in uid_commands))

    def test_get_email_uses_body_peek_and_does_not_download_attachments(self) -> None:
        fake = FakeIMAP()

        @contextmanager
        def mailbox(_folder: str):
            yield fake

        with patch.object(adapter, "_readonly_mailbox", mailbox):
            result = adapter.get_email("101")

        self.assertEqual(result["uid"], "101")
        self.assertIn("Hello Example Company", result["body_text"])
        self.assertFalse(result["attachments_downloaded"])
        self._assert_no_write_commands(fake)

        fetch_queries = [
            str(call[3])
            for call in fake.calls
            if call[0] == "uid" and call[1].lower() == "fetch"
        ]
        self.assertTrue(any("BODY.PEEK[]" in query for query in fetch_queries))

    def test_supported_surface_contains_no_send_or_mutation_tool(self) -> None:
        exposed = {"search_email", "get_email"}
        forbidden = {
            "send_email",
            "send_approved_reply",
            "delete_email",
            "move_email",
            "flag_email",
            "generic_imap_command",
            "generic_smtp_send",
        }
        self.assertTrue(exposed.isdisjoint(forbidden))
        self.assertTrue(hasattr(adapter, "search_email"))
        self.assertTrue(hasattr(adapter, "get_email"))
        for name in forbidden:
            self.assertFalse(hasattr(adapter, name), f"unexpected write-capable function {name}")

    def _assert_no_write_commands(self, fake: FakeIMAP) -> None:
        forbidden_uid_commands = {"store", "copy", "move", "expunge", "append"}
        for call in fake.calls:
            if call[0] == "uid":
                self.assertNotIn(str(call[1]).lower(), forbidden_uid_commands)


if __name__ == "__main__":
    unittest.main(verbosity=2)
