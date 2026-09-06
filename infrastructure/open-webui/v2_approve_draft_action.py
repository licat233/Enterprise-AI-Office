"""
title: EAO Approve Draft
author: Enterprise AI Office Blueprint
version: 1.0.0
required_open_webui: v0.11.3 reference line

Installation Design template only. Import/provision this as an Open WebUI
server-side Action only on an explicitly authorized target.
"""

from __future__ import annotations

import asyncio
import json
import os
import urllib.error
import urllib.request
from typing import Any, Optional

from open_webui.models.groups import Groups


class Action:
    """Deterministically approve the exact governance-backed Draft shown to the user."""

    def __init__(self):
        self.governance_url = os.getenv("EAIO_GOVERNANCE_URL", "").rstrip("/")
        self.forwarder_token = os.getenv("EAIO_TRUSTED_FORWARDER_TOKEN", "")

    @staticmethod
    def _json_request(method: str, url: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={"Content-Type": "application/json", **headers},
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            # Never include request headers/secrets in the raised error.
            detail = exc.read().decode("utf-8", errors="replace")[:2000]
            raise RuntimeError(f"Governance request failed ({exc.code}): {detail}") from None
        except Exception as exc:
            raise RuntimeError(f"Governance request failed: {type(exc).__name__}") from None

        parsed = json.loads(body or "{}")
        if not isinstance(parsed, dict):
            raise RuntimeError("Governance response was not a JSON object")
        return parsed

    @staticmethod
    def _preview(review: dict[str, Any]) -> str:
        to_list = review.get("to_addresses") or []
        cc_list = review.get("cc_addresses") or []
        return "\n".join(
            [
                f"From: {review.get('sender_mailbox_address') or review.get('sender_mailbox_id') or ''}",
                f"To: {', '.join(str(v) for v in to_list)}",
                f"Cc: {', '.join(str(v) for v in cc_list)}" if cc_list else "Cc: —",
                f"Subject: {review.get('subject') or ''}",
                "",
                str(review.get("body") or ""),
            ]
        )

    async def action(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_call__=None,
    ):
        if not self.governance_url or not self.forwarder_token:
            raise RuntimeError("EAO Governance Action is not configured")
        if not __user__ or not __user__.get("id"):
            raise RuntimeError("ACTOR_UNRESOLVED")
        if __event_call__ is None:
            raise RuntimeError("Open WebUI confirmation channel is unavailable")

        user_id = str(__user__["id"])
        chat_id = str(body.get("chat_id") or "")
        message_id = str(body.get("id") or "")
        assistant_id = str(body.get("model") or "")
        if not chat_id or not message_id:
            raise RuntimeError("REVIEW_CONTEXT_UNRESOLVED")

        groups = await Groups.get_groups_by_member_id(user_id)
        group_ids = [str(group.id) for group in groups]

        headers = {
            "Authorization": f"Bearer {self.forwarder_token}",
            "X-EAO-Human-Actor-Id": user_id,
            "X-EAO-Human-Group-Ids": ",".join(group_ids),
            "X-EAO-Chat-Id": chat_id,
            "X-EAO-Message-Id": message_id,
            "X-EAO-Assistant-Id": assistant_id,
        }
        selector = {"chat_id": chat_id, "message_id": message_id}

        # Resolve the review subject from governance-owned server-side binding.
        # Do not parse draft identifiers/hashes out of model-generated text.
        review = await asyncio.to_thread(
            self._json_request,
            "POST",
            f"{self.governance_url}/v1/actions/resolve-current-review",
            headers,
            selector,
        )

        required = ("draft_id", "revision", "content_hash", "sender_mailbox_id", "subject", "body")
        if any(review.get(key) in (None, "") for key in required):
            raise RuntimeError("Governance returned an incomplete review subject")

        confirmed = await __event_call__(
            {
                "type": "confirmation",
                "data": {
                    "title": "Approve this exact email draft?",
                    "message": self._preview(review),
                },
            }
        )
        if confirmed is not True:
            return {"status": "cancelled", "message": "Draft was not approved."}

        # Re-submit the exact server-resolved revision/hash observed immediately
        # before human confirmation. Governance re-loads current state and fails
        # closed if the draft changed between resolve and approve.
        approval = await asyncio.to_thread(
            self._json_request,
            "POST",
            f"{self.governance_url}/v1/actions/approve-current-review",
            headers,
            {
                **selector,
                "expected_draft_id": review["draft_id"],
                "expected_revision": review["revision"],
                "expected_content_hash": review["content_hash"],
            },
        )

        return {
            "status": "approved",
            "approval_id": approval.get("approval_id"),
            "draft_id": approval.get("draft_id", review["draft_id"]),
            "revision": approval.get("draft_revision", review["revision"]),
            "content_hash": approval.get("draft_content_hash", review["content_hash"]),
            "message": "Exact draft approved. No provider send is performed by this Stage 3 action.",
        }
