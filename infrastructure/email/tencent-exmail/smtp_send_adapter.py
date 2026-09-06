#!/usr/bin/env python3
"""Narrow SMTP submission adapter for Enterprise AI Office v2.

Installation-design artifact only. This module is intended to be called from the
trusted eao-email-governance boundary with an already-resolved immutable payload.
It does not expose an Agent-facing CLI or generic SMTP command surface.
"""

from __future__ import annotations

from dataclasses import dataclass
import smtplib
import ssl
from typing import Iterable, Protocol

SENT = "SENT"
CONFIRMED_NOT_SENT = "CONFIRMED_NOT_SENT"
OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"


class SmtpSession(Protocol):
    def mail(self, sender: str): ...
    def rcpt(self, recipient: str): ...
    def data(self, message: bytes): ...
    def rset(self): ...
    def quit(self): ...
    def close(self): ...
    def ehlo(self): ...
    def login(self, user: str, password: str): ...


@dataclass(frozen=True)
class AttemptResult:
    outcome: str
    smtp_stage: str
    smtp_code: int | None = None
    diagnostic_code: str | None = None
    diagnostic_summary: str | None = None


def _is_positive(code: int | None) -> bool:
    return isinstance(code, int) and 200 <= code < 300


def _sanitize_reply(value: object, limit: int = 240) -> str:
    if isinstance(value, bytes):
        text = value.decode("utf-8", errors="replace")
    else:
        text = str(value)
    text = " ".join(text.split())
    return text[:limit]


def _confirmed(stage: str, code: int | None, diagnostic_code: str, summary: object) -> AttemptResult:
    return AttemptResult(
        outcome=CONFIRMED_NOT_SENT,
        smtp_stage=stage,
        smtp_code=code,
        diagnostic_code=diagnostic_code,
        diagnostic_summary=_sanitize_reply(summary),
    )


def _unknown(stage: str, diagnostic_code: str, summary: object) -> AttemptResult:
    return AttemptResult(
        outcome=OUTCOME_UNKNOWN,
        smtp_stage=stage,
        diagnostic_code=diagnostic_code,
        diagnostic_summary=_sanitize_reply(summary),
    )


def _best_effort_rset(session: SmtpSession) -> None:
    try:
        session.rset()
    except Exception:
        # No DATA has been issued on this path, so failure to RSET does not turn
        # the transaction into a possible accepted message. The connection can
        # simply be discarded by the caller.
        pass


def submit_prepared_message(
    session: SmtpSession,
    *,
    envelope_from: str,
    envelope_recipients: Iterable[str],
    message_bytes: bytes,
) -> AttemptResult:
    """Submit one fully prepared message through an authenticated SMTP session.

    Safety rules:
    - all intended RCPT commands must succeed before DATA is issued;
    - any explicit pre-DATA rejection is CONFIRMED_NOT_SENT;
    - once DATA transfer begins, a transport exception without a trustworthy
      final response is OUTCOME_UNKNOWN;
    - only an explicit successful final DATA response is SENT.
    """

    recipients = tuple(envelope_recipients)
    if not recipients:
        return _confirmed("LOCAL_VALIDATION", None, "NO_RECIPIENTS", "no envelope recipients")
    if not message_bytes:
        return _confirmed("LOCAL_VALIDATION", None, "EMPTY_MESSAGE", "empty transport payload")

    try:
        code, reply = session.mail(envelope_from)
    except Exception as exc:
        return _confirmed("MAIL_FROM", None, "MAIL_FROM_TRANSPORT_ERROR", exc)

    if not _is_positive(code):
        return _confirmed("MAIL_FROM", code, "MAIL_FROM_REJECTED", reply)

    for recipient in recipients:
        try:
            code, reply = session.rcpt(recipient)
        except Exception as exc:
            _best_effort_rset(session)
            return _confirmed("RCPT_TO", None, "RCPT_TRANSPORT_ERROR", exc)

        if not _is_positive(code):
            _best_effort_rset(session)
            return _confirmed("RCPT_TO", code, "RECIPIENT_REJECTED", reply)

    # From this point onward we conservatively treat transport uncertainty as a
    # possible external side effect. smtplib.data() performs DATA + transfer +
    # final response processing. An explicit SMTPDataError contains a server
    # rejection; a transport exception without final response is ambiguous.
    try:
        code, reply = session.data(message_bytes)
    except smtplib.SMTPDataError as exc:
        return _confirmed(
            "DATA",
            getattr(exc, "smtp_code", None),
            "DATA_REJECTED",
            getattr(exc, "smtp_error", exc),
        )
    except (smtplib.SMTPServerDisconnected, TimeoutError, OSError, ssl.SSLError) as exc:
        return _unknown("DATA", "DATA_TRANSPORT_OUTCOME_UNKNOWN", exc)
    except Exception as exc:
        # Unknown library/provider exceptions after DATA begins are classified
        # conservatively. They must be reconciled before another attempt.
        return _unknown("DATA", "DATA_UNCLASSIFIED_OUTCOME_UNKNOWN", exc)

    if _is_positive(code):
        return AttemptResult(
            outcome=SENT,
            smtp_stage="FINAL_RESPONSE",
            smtp_code=code,
            diagnostic_code="PROVIDER_ACCEPTED",
            diagnostic_summary=_sanitize_reply(reply),
        )

    return _confirmed("FINAL_RESPONSE", code, "FINAL_RESPONSE_REJECTED", reply)


def send_smtp_ssl_prepared(
    *,
    host: str,
    port: int,
    username: str,
    password: str,
    envelope_from: str,
    envelope_recipients: Iterable[str],
    message_bytes: bytes,
    timeout_seconds: float = 30.0,
    smtp_factory=smtplib.SMTP_SSL,
) -> AttemptResult:
    """Open authenticated SMTP-over-SSL and submit one prepared message.

    Connection/TLS/authentication failures occur before message DATA submission
    and therefore classify as CONFIRMED_NOT_SENT for this attempt.
    """

    session = None
    try:
        context = ssl.create_default_context()
        session = smtp_factory(host, port, timeout=timeout_seconds, context=context)
        session.ehlo()
        session.login(username, password)
    except smtplib.SMTPAuthenticationError as exc:
        if session is not None:
            try:
                session.close()
            except Exception:
                pass
        return _confirmed(
            "AUTH",
            getattr(exc, "smtp_code", None),
            "AUTH_REJECTED",
            getattr(exc, "smtp_error", exc),
        )
    except Exception as exc:
        if session is not None:
            try:
                session.close()
            except Exception:
                pass
        return _confirmed("CONNECT_AUTH", None, "CONNECT_OR_AUTH_FAILED", exc)

    try:
        return submit_prepared_message(
            session,
            envelope_from=envelope_from,
            envelope_recipients=envelope_recipients,
            message_bytes=message_bytes,
        )
    finally:
        try:
            session.quit()
        except Exception:
            try:
                session.close()
            except Exception:
                pass
