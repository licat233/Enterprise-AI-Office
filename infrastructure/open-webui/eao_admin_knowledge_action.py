"""
title: EAO Admin Knowledge Approval
author: Enterprise AI Office Blueprint
version: 1.0.0
required_open_webui: v0.11.3 reference line

Server-side Open WebUI Action for EAO Administrator Console v1A.

The Action derives the exact source from the current owned chat, resolves the
authenticated HumanActor and group membership server-side, signs the immutable
operation plan with the shared EAO envelope helper, asks for native Open WebUI
confirmation, re-resolves the source after confirmation, and performs only the
bounded WeKnora contributor operation.

No repository mutation, shell, package manager, generic filesystem, Docker,
browser, profile switching, or provider administration is exposed.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import hashlib
import importlib.util
import ipaddress
import json
import mimetypes
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Optional


_URL_RE = re.compile(r"https?://[^\\s<>\\[\\]{}\\\"']+", re.IGNORECASE)
_MAX_MANUAL_CHARS = 12000
_DEFAULT_HTTP_TIMEOUT = 30


class ActionError(RuntimeError):
    pass


def _extract_urls(text: str) -> list[str]:
    values: list[str] = []
    for raw in _URL_RE.findall(text or ""):
        value = raw.rstrip(".,;:!?")
        if value not in values:
            values.append(value)
    return values


def _validate_public_http_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ActionError("SOURCE_URL_INVALID")
    if parsed.username or parsed.password:
        raise ActionError("SOURCE_URL_CREDENTIALS_FORBIDDEN")
    host = parsed.hostname.lower().rstrip(".")
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        raise ActionError("SOURCE_URL_LOCAL_FORBIDDEN")
    try:
        literal_ip = ipaddress.ip_address(host)
    except ValueError:
        literal_ip = None
    if literal_ip is not None and not literal_ip.is_global:
        raise ActionError("SOURCE_URL_NON_GLOBAL_IP_FORBIDDEN")
    return urllib.parse.urlunsplit(parsed)


def _file_ids(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    values: list[str] = []
    for item in items:
        value = None
        if isinstance(item, str):
            value = item
        elif isinstance(item, dict):
            value = item.get("id") or item.get("file_id")
            if not value and isinstance(item.get("file"), dict):
                value = item["file"].get("id")
        if value:
            value = str(value)
            if value not in values:
                values.append(value)
    return values


def _manual_title(content: str) -> str:
    for line in content.splitlines():
        line = line.strip().lstrip("#").strip()
        if line:
            return line[:120]
    return "EAO Admin manual knowledge"


def _sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _operation_id(chat_id: str, message_id: str, fingerprint: str, kb_id: str) -> str:
    material = "\0".join((chat_id, message_id, fingerprint, kb_id)).encode("utf-8")
    digest = hashlib.sha256(material).hexdigest()[:32]
    return f"knowledge-ingestion:{digest}"


def _unwrap_data(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    data = payload.get("data")
    return data if isinstance(data, dict) else payload


def _knowledge_id(payload: Any) -> str | None:
    data = _unwrap_data(payload)
    value = data.get("id") or data.get("knowledge_id")
    return str(value) if value else None


def _parse_status(payload: Any) -> str | None:
    data = _unwrap_data(payload)
    value = data.get("parse_status") or data.get("processing_status") or data.get("status")
    return str(value) if value is not None else None


def _load_envelope_module():
    try:
        import eao_operation_envelope as module  # type: ignore
        return module
    except Exception:
        pass

    explicit = os.getenv("EAIO_EAO_ADMIN_OPERATION_ENVELOPE_PATH", "").strip()
    if explicit:
        path = Path(explicit)
    else:
        module_dir = os.getenv("EAIO_EAO_ADMIN_MODULE_DIR", "").strip()
        if module_dir:
            path = Path(module_dir) / "eao_operation_envelope.py"
        else:
            path = Path(__file__).resolve().with_name("eao_operation_envelope.py")

    if not path.is_file():
        raise ActionError("OPERATION_ENVELOPE_MODULE_UNAVAILABLE")

    spec = importlib.util.spec_from_file_location("eao_operation_envelope_runtime", path)
    if spec is None or spec.loader is None:
        raise ActionError("OPERATION_ENVELOPE_MODULE_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _multipart_file_body(
    filename: str,
    content: bytes,
    content_type: str | None = None,
) -> tuple[bytes, str]:
    boundary = "eao-" + uuid.uuid4().hex
    safe_name = os.path.basename(filename).replace('"', "")
    mime = content_type or mimetypes.guess_type(safe_name)[0] or "application/octet-stream"
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{safe_name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8")
    tail = (
        f"\r\n--{boundary}\r\n"
        'Content-Disposition: form-data; name="channel"\r\n\r\n'
        "eao-admin\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")
    return head + content + tail, f"multipart/form-data; boundary={boundary}"


class Action:
    def __init__(self):
        self.admin_group_id = os.getenv("EAIO_EAO_ADMIN_GROUP_ID", "").strip()
        self.assistant_id = os.getenv("EAIO_EAO_ADMIN_ASSISTANT_ID", "maintainer").strip()
        self.weknora_base_url = os.getenv("EAIO_EAO_ADMIN_WEKNORA_BASE_URL", "").rstrip("/")
        self.weknora_api_key = os.getenv("EAIO_EAO_ADMIN_WEKNORA_API_KEY", "")
        self.knowledge_base_id = os.getenv("EAIO_EAO_ADMIN_KB_ID", "").strip()
        self.knowledge_base_name = os.getenv(
            "EAIO_EAO_ADMIN_KB_DISPLAY_NAME", "Company Knowledge"
        ).strip()
        self.signing_key = os.getenv("EAIO_EAO_ADMIN_APPROVAL_SIGNING_KEY", "")
        self.approval_ttl_minutes = int(
            os.getenv("EAIO_EAO_ADMIN_APPROVAL_TTL_MINUTES", "30")
        )
        self.http_timeout = int(
            os.getenv(
                "EAIO_EAO_ADMIN_HTTP_TIMEOUT_SECONDS",
                str(_DEFAULT_HTTP_TIMEOUT),
            )
        )

    def _require_config(self) -> None:
        if not self.admin_group_id:
            raise ActionError("EAO_ADMIN_GROUP_UNRESOLVED")
        if not self.weknora_base_url or not self.weknora_api_key or not self.knowledge_base_id:
            raise ActionError("WEKNORA_CONTRIBUTOR_BINDING_UNRESOLVED")
        if not self.signing_key:
            raise ActionError("SIGNING_KEY_MISSING")
        if self.approval_ttl_minutes < 1 or self.approval_ttl_minutes > 30:
            raise ActionError("INVALID_APPROVAL_TTL")

    @staticmethod
    def _history_message(chat: Any, message_id: str) -> dict[str, Any]:
        if chat is None or not isinstance(getattr(chat, "chat", None), dict):
            raise ActionError("REVIEW_CONTEXT_NOT_FOUND")
        messages = (chat.chat.get("history") or {}).get("messages") or {}
        message = messages.get(message_id)
        if not isinstance(message, dict):
            raise ActionError("REVIEW_CONTEXT_NOT_FOUND")
        return message

    async def _resolve_source(
        self,
        chat_id: str,
        assistant_message_id: str,
        user_id: str,
    ) -> dict[str, Any]:
        from open_webui.models.chats import Chats
        from open_webui.models.files import Files
        from open_webui.storage.provider import Storage

        chat = await Chats.get_chat_by_id(chat_id)
        if chat is None or str(chat.user_id) != user_id:
            raise ActionError("REVIEW_CONTEXT_NOT_OWNED")

        assistant = self._history_message(chat, assistant_message_id)
        if assistant.get("role") != "assistant":
            raise ActionError("REVIEW_CONTEXT_NOT_ASSISTANT")

        parent_id = assistant.get("parentId")
        if not parent_id:
            raise ActionError("SOURCE_MESSAGE_UNRESOLVED")
        user_message = self._history_message(chat, str(parent_id))
        if user_message.get("role") != "user":
            raise ActionError("SOURCE_MESSAGE_UNRESOLVED")

        content = user_message.get("content")
        content = content if isinstance(content, str) else ""

        message_files = await Chats.get_message_metadata(
            chat_id,
            str(parent_id),
            "files",
        )
        if not isinstance(message_files, list):
            message_files = (
                user_message.get("files")
                if isinstance(user_message.get("files"), list)
                else []
            )
        ids = _file_ids(message_files)

        if ids:
            if len(ids) != 1:
                raise ActionError("MULTIPLE_SOURCES_REQUIRE_SEPARATE_APPROVALS")
            file_item = await Files.get_file_by_id(ids[0])
            if (
                file_item is None
                or str(file_item.user_id) != user_id
                or not file_item.path
            ):
                raise ActionError("SOURCE_FILE_NOT_OWNED")
            resolved = await asyncio.to_thread(Storage.get_file, file_item.path)
            path = Path(resolved)
            if not path.is_file():
                raise ActionError("SOURCE_FILE_UNAVAILABLE")

            hasher = hashlib.sha256()
            size = 0
            with path.open("rb") as handle:
                while True:
                    chunk = handle.read(1024 * 1024)
                    if not chunk:
                        break
                    hasher.update(chunk)
                    size += len(chunk)

            return {
                "kind": "file",
                "user_message_id": str(parent_id),
                "fingerprint": "sha256:" + hasher.hexdigest(),
                "file_id": str(file_item.id),
                "filename": os.path.basename(file_item.filename),
                "content_type": (
                    (file_item.meta or {}).get("content_type")
                    if isinstance(file_item.meta, dict)
                    else None
                ),
                "size": size,
                "path": str(path),
            }

        urls = _extract_urls(content)
        if urls:
            if len(urls) != 1:
                raise ActionError("MULTIPLE_SOURCES_REQUIRE_SEPARATE_APPROVALS")
            url = _validate_public_http_url(urls[0])
            return {
                "kind": "url",
                "user_message_id": str(parent_id),
                "fingerprint": _sha256_bytes(url.encode("utf-8")),
                "url": url,
            }

        manual = content.strip()
        if not manual:
            raise ActionError("KNOWLEDGE_SOURCE_EMPTY")
        if len(manual) > _MAX_MANUAL_CHARS:
            raise ActionError("MANUAL_SOURCE_TOO_LARGE_USE_FILE")
        return {
            "kind": "manual",
            "user_message_id": str(parent_id),
            "fingerprint": _sha256_bytes(manual.encode("utf-8")),
            "title": _manual_title(manual),
            "content": manual,
            "length": len(manual),
        }

    def _current_state(
        self,
        chat_id: str,
        assistant_message_id: str,
        source: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "chat_id": chat_id,
            "assistant_message_id": assistant_message_id,
            "user_message_id": source["user_message_id"],
            "source_fingerprint": source["fingerprint"],
            "knowledge_base_id": self.knowledge_base_id,
        }

    def _source_identity(self, source: dict[str, Any]) -> dict[str, Any]:
        if source["kind"] == "file":
            return {
                "kind": "file",
                "file_id": source["file_id"],
                "filename": source["filename"],
                "size": source["size"],
            }
        if source["kind"] == "url":
            return {"kind": "url", "url": source["url"]}
        return {
            "kind": "manual",
            "title": source["title"],
            "length": source["length"],
        }

    def _preview(
        self,
        source: dict[str, Any],
        operation_id: str,
        plan_hash: str,
    ) -> str:
        lines = [
            f"Operation: {operation_id}",
            f"Target: {self.knowledge_base_name}",
            f"Source fingerprint: {source['fingerprint']}",
            f"Plan hash: {plan_hash}",
            "",
        ]
        if source["kind"] == "file":
            lines.extend(
                [
                    "Source type: file",
                    f"Filename: {source['filename']}",
                    f"Size: {source['size']} bytes",
                ]
            )
        elif source["kind"] == "url":
            lines.extend(["Source type: URL", f"URL: {source['url']}"])
        else:
            lines.extend(
                [
                    "Source type: manual text",
                    f"Title: {source['title']}",
                    "",
                    source["content"],
                ]
            )
        return "\n".join(lines)

    async def _persist_record(
        self,
        chat_id: str,
        message_id: str,
        record: dict[str, Any],
    ) -> None:
        from open_webui.models.chats import Chats

        updated = await Chats.upsert_message_to_chat_by_id_and_message_id(
            chat_id,
            message_id,
            {"eao_admin_operation": record},
            touch=False,
        )
        if updated is None:
            raise ActionError("OPERATION_RECORD_PERSIST_FAILED")

    async def _existing_record(
        self,
        chat_id: str,
        message_id: str,
    ) -> dict[str, Any] | None:
        from open_webui.models.chats import Chats

        chat = await Chats.get_chat_by_id(chat_id)
        message = self._history_message(chat, message_id)
        record = message.get("eao_admin_operation")
        return record if isinstance(record, dict) else None

    def _request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        body: bytes | None = None,
        content_type: str | None = None,
    ) -> tuple[int, dict[str, Any]]:
        headers = {
            "X-API-Key": self.weknora_api_key,
            "Accept": "application/json",
        }
        data = body
        if json_body is not None:
            data = json.dumps(
                json_body,
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif content_type:
            headers["Content-Type"] = content_type

        request = urllib.request.Request(
            f"{self.weknora_base_url}{path}",
            data=data,
            method=method,
            headers=headers,
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=self.http_timeout,
            ) as response:
                raw = response.read().decode("utf-8")
                return int(response.status), json.loads(raw or "{}")
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw or "{}")
            except Exception:
                parsed = {"error": raw[:2000]}
            return int(exc.code), parsed

    def _execute_ingestion(
        self,
        source: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        kb = urllib.parse.quote(self.knowledge_base_id, safe="")
        prefix = f"/knowledge-bases/{kb}/knowledge"

        if source["kind"] == "url":
            return self._request(
                "POST",
                f"{prefix}/url",
                json_body={
                    "url": source["url"],
                    "channel": "eao-admin",
                },
            )

        if source["kind"] == "manual":
            return self._request(
                "POST",
                f"{prefix}/manual",
                json_body={
                    "title": source["title"],
                    "content": source["content"],
                    "status": "publish",
                    "channel": "eao-admin",
                },
            )

        with open(source["path"], "rb") as handle:
            content = handle.read()
        body, content_type = _multipart_file_body(
            source["filename"],
            content,
            source.get("content_type"),
        )
        return self._request(
            "POST",
            f"{prefix}/file",
            body=body,
            content_type=content_type,
        )

    def _get_knowledge(
        self,
        knowledge_id: str,
    ) -> tuple[int, dict[str, Any]]:
        item = urllib.parse.quote(knowledge_id, safe="")
        return self._request("GET", f"/knowledge/{item}")

    async def _reconcile_unknown(
        self,
        chat_id: str,
        message_id: str,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        knowledge_id = record.get("knowledge_id")
        if not knowledge_id:
            return {
                "status": "RECONCILIATION_REQUIRED",
                "operation_id": record.get("operation_id"),
                "plan_hash": record.get("plan_hash"),
                "message": (
                    "Previous outcome is unknown and no bounded knowledge ID "
                    "is available. No retry was attempted."
                ),
            }

        status, payload = await asyncio.to_thread(
            self._get_knowledge,
            str(knowledge_id),
        )
        if status == 200:
            updated = {
                **record,
                "status": "SUCCEEDED",
                "parse_status": _parse_status(payload),
            }
            await self._persist_record(chat_id, message_id, updated)
            return {
                "status": "ALREADY_RESOLVED",
                "operation_id": updated.get("operation_id"),
                "knowledge_id": knowledge_id,
                "parse_status": updated.get("parse_status"),
                "message": (
                    "Previous outcome reconciled from WeKnora. "
                    "No duplicate write was attempted."
                ),
            }

        return {
            "status": "RECONCILIATION_REQUIRED",
            "operation_id": record.get("operation_id"),
            "knowledge_id": knowledge_id,
            "message": (
                "Previous outcome could not be confirmed. "
                "No retry was attempted."
            ),
        }

    async def action(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_call__=None,
    ):
        self._require_config()

        if not __user__ or not __user__.get("id"):
            raise ActionError("ACTOR_UNRESOLVED")
        if __event_call__ is None:
            raise ActionError("CONFIRMATION_CHANNEL_UNAVAILABLE")

        chat_id = str(body.get("chat_id") or "")
        assistant_message_id = str(body.get("id") or "")
        model_id = str(body.get("model") or "")
        if not chat_id or not assistant_message_id:
            raise ActionError("REVIEW_CONTEXT_UNRESOLVED")
        if model_id != self.assistant_id:
            raise ActionError("ASSISTANT_CONTEXT_MISMATCH")

        user_id = str(__user__["id"])
        from open_webui.models.groups import Groups

        groups = await Groups.get_groups_by_member_id(user_id)
        group_ids = tuple(sorted(str(group.id) for group in groups))
        if self.admin_group_id not in group_ids:
            raise ActionError("APPROVER_UNAUTHORIZED")

        existing = await self._existing_record(
            chat_id,
            assistant_message_id,
        )
        if existing:
            existing_status = str(existing.get("status") or "")
            if existing_status == "OUTCOME_UNKNOWN":
                return await self._reconcile_unknown(
                    chat_id,
                    assistant_message_id,
                    existing,
                )
            if existing_status in {
                "SUCCEEDED",
                "CONFIRMED_NOT_APPLIED",
                "BLOCKED",
            }:
                return {
                    "status": "ALREADY_RESOLVED",
                    "operation_id": existing.get("operation_id"),
                    "knowledge_id": existing.get("knowledge_id"),
                    "parse_status": existing.get("parse_status"),
                    "message": (
                        "This operation was already resolved. "
                        "No duplicate write was attempted."
                    ),
                }

        source = await self._resolve_source(
            chat_id,
            assistant_message_id,
            user_id,
        )

        envelope_module = _load_envelope_module()
        created_at = (
            datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )
        operation_id = _operation_id(
            chat_id,
            assistant_message_id,
            source["fingerprint"],
            self.knowledge_base_id,
        )
        current_state = self._current_state(
            chat_id,
            assistant_message_id,
            source,
        )

        envelope = envelope_module.build_envelope(
            operation_id=operation_id,
            operation_type="knowledge_ingestion",
            source_identity=self._source_identity(source),
            source_fingerprint=source["fingerprint"],
            target={
                "kind": "weknora_knowledge_base",
                "knowledge_base_id": self.knowledge_base_id,
            },
            material_change_summary=(
                "Ingest the exact current chat source into the configured "
                "Company Knowledge base."
            ),
            security_impact=(
                "Uses the scoped WeKnora contributor credential only; "
                "no KB lifecycle/admin capability."
            ),
            profile_exposure_impact="No Profile exposure change.",
            runtime_impact=(
                "Creates one WeKnora knowledge item after exact human approval."
            ),
            expected_current_state=current_state,
            created_at=created_at,
            approval_ttl_minutes=self.approval_ttl_minutes,
            signing_key=self.signing_key.encode("utf-8"),
        )

        confirmed = await __event_call__(
            {
                "type": "confirmation",
                "data": {
                    "title": "Approve this exact knowledge ingestion?",
                    "message": self._preview(
                        source,
                        operation_id,
                        envelope.immutable_plan_hash,
                    ),
                },
            }
        )
        if confirmed is not True:
            return {
                "status": "cancelled",
                "message": "Knowledge ingestion was not approved.",
            }

        groups = await Groups.get_groups_by_member_id(user_id)
        group_ids = tuple(sorted(str(group.id) for group in groups))
        human = envelope_module.TrustedHumanContext(
            actor_id=user_id,
            group_ids=group_ids,
        )

        fresh_source = await self._resolve_source(
            chat_id,
            assistant_message_id,
            user_id,
        )
        fresh_state = self._current_state(
            chat_id,
            assistant_message_id,
            fresh_source,
        )

        approval = envelope_module.approve_envelope(
            envelope,
            human=human,
            required_group_id=self.admin_group_id,
            current_state=fresh_state,
            approved_at=datetime.now(timezone.utc),
            signing_key=self.signing_key.encode("utf-8"),
        )

        record = {
            "operation_id": operation_id,
            "plan_hash": envelope.immutable_plan_hash,
            "source_fingerprint": source["fingerprint"],
            "knowledge_base_id": self.knowledge_base_id,
            "approved_by_human_actor": approval["approved_by_human_actor"],
            "approved_at": approval["approved_at"],
            "status": "OUTCOME_UNKNOWN",
        }

        # Persist fail-closed before the external write. If the process dies
        # after WeKnora accepts the request, the same chat message will never
        # blindly retry the mutation.
        await self._persist_record(
            chat_id,
            assistant_message_id,
            record,
        )

        try:
            http_status, payload = await asyncio.to_thread(
                self._execute_ingestion,
                fresh_source,
            )
        except Exception as exc:
            raise ActionError(
                f"WEKNORA_OUTCOME_UNKNOWN:{type(exc).__name__}"
            ) from None

        knowledge_id = _knowledge_id(payload)

        if http_status in {200, 201}:
            if not knowledge_id:
                raise ActionError("WEKNORA_RESPONSE_MISSING_KNOWLEDGE_ID")

            detail_status, detail = await asyncio.to_thread(
                self._get_knowledge,
                knowledge_id,
            )
            parse_status = (
                _parse_status(detail)
                if detail_status == 200
                else _parse_status(payload)
            )
            resolved = {
                **record,
                "status": "SUCCEEDED",
                "knowledge_id": knowledge_id,
                "parse_status": parse_status,
            }
            await self._persist_record(
                chat_id,
                assistant_message_id,
                resolved,
            )
            return {
                "status": "SUCCEEDED",
                "operation_id": operation_id,
                "plan_hash": envelope.immutable_plan_hash,
                "knowledge_id": knowledge_id,
                "parse_status": parse_status,
                "message": (
                    "Knowledge ingestion request succeeded. Treat the item as "
                    "ACTIVE only after parse/index and retrieval acceptance pass."
                ),
            }

        if http_status == 409:
            if knowledge_id:
                detail_status, detail = await asyncio.to_thread(
                    self._get_knowledge,
                    knowledge_id,
                )
                parse_status = (
                    _parse_status(detail)
                    if detail_status == 200
                    else _parse_status(payload)
                )
                resolved = {
                    **record,
                    "status": "SUCCEEDED",
                    "knowledge_id": knowledge_id,
                    "parse_status": parse_status,
                    "deduplicated": True,
                }
                await self._persist_record(
                    chat_id,
                    assistant_message_id,
                    resolved,
                )
                return {
                    "status": "SUCCEEDED",
                    "operation_id": operation_id,
                    "knowledge_id": knowledge_id,
                    "parse_status": parse_status,
                    "deduplicated": True,
                    "message": (
                        "WeKnora reported an existing matching source. "
                        "No duplicate write was created."
                    ),
                }

            resolved = {
                **record,
                "status": "CONFIRMED_NOT_APPLIED",
                "http_status": http_status,
            }
            await self._persist_record(
                chat_id,
                assistant_message_id,
                resolved,
            )
            return {
                "status": "CONFIRMED_NOT_APPLIED",
                "operation_id": operation_id,
                "message": (
                    "WeKnora rejected the duplicate/conflicting source and "
                    "no new knowledge item was confirmed."
                ),
            }

        resolved = {
            **record,
            "status": "CONFIRMED_NOT_APPLIED",
            "http_status": http_status,
        }
        await self._persist_record(
            chat_id,
            assistant_message_id,
            resolved,
        )
        raise ActionError(
            f"WEKNORA_INGESTION_REJECTED:{http_status}"
        )
