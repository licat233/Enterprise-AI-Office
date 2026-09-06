#!/usr/bin/env python3
"""Offline deterministic tests for the narrow v2 SMTP send adapter.

No DNS, socket, mailbox, credential, or real provider access is used.
"""

from __future__ import annotations

import smtplib
import unittest

from smtp_send_adapter import (
    CONFIRMED_NOT_SENT,
    OUTCOME_UNKNOWN,
    SENT,
    send_smtp_ssl_prepared,
    submit_prepared_message,
)


class FakeSession:
    def __init__(self, *, mail=(250, b"ok"), rcpt=None, data=(250, b"queued"), data_exc=None):
        self.mail_reply = mail
        self.rcpt_replies = list(rcpt or [])
        self.data_reply = data
        self.data_exc = data_exc
        self.calls = []
        self.closed = False

    def mail(self, sender):
        self.calls.append(("mail", sender))
        return self.mail_reply

    def rcpt(self, recipient):
        self.calls.append(("rcpt", recipient))
        if self.rcpt_replies:
            return self.rcpt_replies.pop(0)
        return (250, b"ok")

    def data(self, message):
        self.calls.append(("data", message))
        if self.data_exc is not None:
            raise self.data_exc
        return self.data_reply

    def rset(self):
        self.calls.append(("rset", None))
        return (250, b"reset")

    def ehlo(self):
        self.calls.append(("ehlo", None))
        return (250, b"hello")

    def login(self, user, password):
        self.calls.append(("login", user))
        return (235, b"authenticated")

    def quit(self):
        self.calls.append(("quit", None))
        return (221, b"bye")

    def close(self):
        self.closed = True
        self.calls.append(("close", None))


class AuthFailSession(FakeSession):
    def login(self, user, password):
        self.calls.append(("login", user))
        raise smtplib.SMTPAuthenticationError(535, b"authentication failed")


class AdapterTests(unittest.TestCase):
    def payload(self):
        return b"From: sales@example.invalid\r\nTo: customer@example.invalid\r\n\r\nHello\r\n"

    def test_successful_final_response_is_sent(self):
        session = FakeSession(
            rcpt=[(250, b"ok"), (250, b"ok")],
            data=(250, b"queued"),
        )
        result = submit_prepared_message(
            session,
            envelope_from="sales@example.invalid",
            envelope_recipients=["a@example.invalid", "b@example.invalid"],
            message_bytes=self.payload(),
        )
        self.assertEqual(result.outcome, SENT)
        self.assertEqual(result.smtp_stage, "FINAL_RESPONSE")
        self.assertEqual(result.smtp_code, 250)
        self.assertEqual([c[0] for c in session.calls].count("data"), 1)

    def test_any_recipient_rejection_aborts_before_data(self):
        session = FakeSession(
            rcpt=[(250, b"ok"), (550, b"no such recipient")],
        )
        result = submit_prepared_message(
            session,
            envelope_from="sales@example.invalid",
            envelope_recipients=["a@example.invalid", "bad@example.invalid"],
            message_bytes=self.payload(),
        )
        self.assertEqual(result.outcome, CONFIRMED_NOT_SENT)
        self.assertEqual(result.smtp_stage, "RCPT_TO")
        self.assertNotIn("data", [c[0] for c in session.calls])
        self.assertIn("rset", [c[0] for c in session.calls])

    def test_explicit_data_rejection_is_confirmed_not_sent(self):
        session = FakeSession(
            data_exc=smtplib.SMTPDataError(554, b"message rejected"),
        )
        result = submit_prepared_message(
            session,
            envelope_from="sales@example.invalid",
            envelope_recipients=["a@example.invalid"],
            message_bytes=self.payload(),
        )
        self.assertEqual(result.outcome, CONFIRMED_NOT_SENT)
        self.assertEqual(result.smtp_stage, "DATA")
        self.assertEqual(result.smtp_code, 554)

    def test_timeout_after_data_begins_is_unknown(self):
        session = FakeSession(data_exc=TimeoutError("final response timed out"))
        result = submit_prepared_message(
            session,
            envelope_from="sales@example.invalid",
            envelope_recipients=["a@example.invalid"],
            message_bytes=self.payload(),
        )
        self.assertEqual(result.outcome, OUTCOME_UNKNOWN)
        self.assertEqual(result.smtp_stage, "DATA")

    def test_explicit_final_negative_response_is_confirmed_not_sent(self):
        session = FakeSession(data=(451, b"temporary local problem"))
        result = submit_prepared_message(
            session,
            envelope_from="sales@example.invalid",
            envelope_recipients=["a@example.invalid"],
            message_bytes=self.payload(),
        )
        self.assertEqual(result.outcome, CONFIRMED_NOT_SENT)
        self.assertEqual(result.smtp_stage, "FINAL_RESPONSE")
        self.assertEqual(result.smtp_code, 451)

    def test_auth_failure_is_confirmed_not_sent(self):
        session = AuthFailSession()

        def factory(host, port, timeout, context):
            self.assertEqual(host, "smtp.example.invalid")
            self.assertEqual(port, 465)
            return session

        result = send_smtp_ssl_prepared(
            host="smtp.example.invalid",
            port=465,
            username="sales@example.invalid",
            password="synthetic-secret",
            envelope_from="sales@example.invalid",
            envelope_recipients=["a@example.invalid"],
            message_bytes=self.payload(),
            smtp_factory=factory,
        )
        self.assertEqual(result.outcome, CONFIRMED_NOT_SENT)
        self.assertEqual(result.smtp_stage, "AUTH")
        self.assertNotIn("data", [c[0] for c in session.calls])

    def test_empty_recipient_set_never_calls_smtp(self):
        session = FakeSession()
        result = submit_prepared_message(
            session,
            envelope_from="sales@example.invalid",
            envelope_recipients=[],
            message_bytes=self.payload(),
        )
        self.assertEqual(result.outcome, CONFIRMED_NOT_SENT)
        self.assertEqual(session.calls, [])


if __name__ == "__main__":
    unittest.main()
