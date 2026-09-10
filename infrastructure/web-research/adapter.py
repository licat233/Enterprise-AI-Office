#!/usr/bin/env python3
"""Bounded Enterprise Web Research MCP adapter.

The adapter is the only Operations-facing surface for public web research.
It calls Firecrawl's read-only Search and Scrape API endpoints, normalizes
their responses, and rejects unsafe URLs before any upstream request.
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
import socket
import sys
from datetime import datetime, timezone
from typing import Any, Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


ALLOWED_SCHEMES = frozenset({"http", "https"})
ALLOWED_PORTS = frozenset({80, 443})
MAX_QUERY_CHARS = 2_000
MAX_RESULTS = 20
MAX_RESPONSE_BYTES = 12 * 1024 * 1024
TRUST_CLASS = "UNTRUSTED_WEB_CONTENT"
FAILURE_REASONS = frozenset(
    {
        "BLOCKED",
        "LOGIN_REQUIRED",
        "CAPTCHA_REQUIRED",
        "TIMEOUT",
        "UNSUPPORTED",
        "SECURITY_REJECTED",
        "UPSTREAM_ERROR",
    }
)
INTERNAL_HOSTNAMES = frozenset(
    {
        "localhost",
        "localhost.localdomain",
        "broadcasthost",
        "ip6-localhost",
        "ip6-loopback",
    }
)
INTERNAL_SUFFIXES = (".localhost", ".local", ".internal", ".intranet", ".home.arpa")
NUMERIC_HOSTNAME = re.compile(r"^[0-9.]+$")


class WebResearchError(ValueError):
    """A finite, safe error that may be returned to an employee task."""

    def __init__(self, reason: str, message: str) -> None:
        if reason not in FAILURE_REASONS:
            raise ValueError(f"unsupported Web Research failure reason: {reason}")
        super().__init__(message)
        self.reason = reason


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _is_control_text(value: str) -> bool:
    return any(ord(char) < 32 or ord(char) == 127 for char in value)


def _ip_from_resolved(value: Any) -> ipaddress._BaseAddress | None:
    if isinstance(value, tuple):
        try:
            value = value[4][0]
        except (IndexError, TypeError):
            return None
    if not isinstance(value, str):
        return None
    value = value.split("%", 1)[0]
    try:
        return ipaddress.ip_address(value)
    except ValueError:
        return None


def _reject_non_global(ip: ipaddress._BaseAddress, host: str) -> None:
    if not ip.is_global:
        raise WebResearchError(
            "SECURITY_REJECTED",
            f"public Web Research does not allow non-public address for host {host!r}",
        )


def _resolve_public_addresses(host: str, port: int, resolver: Callable[[str, int], Iterable[Any]]) -> None:
    try:
        addresses = list(resolver(host, port))
    except (OSError, socket.gaierror) as exc:
        raise WebResearchError(
            "SECURITY_REJECTED", f"host could not be resolved safely: {host!r}"
        ) from exc
    if not addresses:
        raise WebResearchError("SECURITY_REJECTED", f"host has no resolved address: {host!r}")
    for address in addresses:
        ip = _ip_from_resolved(address)
        if ip is None:
            raise WebResearchError("SECURITY_REJECTED", f"host resolved to an invalid address: {host!r}")
        _reject_non_global(ip, host)


def _default_resolver(host: str, port: int) -> list[Any]:
    return socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)


def validate_public_url(
    value: str,
    *,
    resolver: Callable[[str, int], Iterable[Any]] = _default_resolver,
) -> str:
    """Validate an employee-supplied public HTTP(S) URL and return it."""

    if not isinstance(value, str) or not value.strip():
        raise WebResearchError("UNSUPPORTED", "url must be a non-empty string")
    value = value.strip()
    if _is_control_text(value):
        raise WebResearchError("SECURITY_REJECTED", "url contains control characters")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError as exc:
        raise WebResearchError("SECURITY_REJECTED", "url is malformed") from exc

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise WebResearchError("SECURITY_REJECTED", "only http and https URLs are allowed")
    if not hostname:
        raise WebResearchError("SECURITY_REJECTED", "url must include a host")
    if parsed.username is not None or parsed.password is not None:
        raise WebResearchError("SECURITY_REJECTED", "URL credentials are not allowed")
    hostname = hostname.rstrip(".").lower()
    if hostname in INTERNAL_HOSTNAMES or hostname.endswith(INTERNAL_SUFFIXES):
        raise WebResearchError("SECURITY_REJECTED", "internal hostnames are not allowed")
    if port is not None and port not in ALLOWED_PORTS:
        raise WebResearchError("SECURITY_REJECTED", "only standard HTTP(S) ports are allowed")

    try:
        literal_ip = ipaddress.ip_address(hostname)
    except ValueError:
        literal_ip = None
    if literal_ip is None and NUMERIC_HOSTNAME.fullmatch(hostname):
        try:
            literal_ip = ipaddress.ip_address(socket.inet_ntoa(socket.inet_aton(hostname)))
        except OSError as exc:
            raise WebResearchError("SECURITY_REJECTED", "numeric host is not a valid IPv4 address") from exc
    if literal_ip is not None:
        _reject_non_global(literal_ip, hostname)
    else:
        if "." not in hostname:
            raise WebResearchError("SECURITY_REJECTED", "single-label internal hostnames are not allowed")
        _resolve_public_addresses(hostname, port or (443 if parsed.scheme.lower() == "https" else 80), resolver)
    return value


def _json_object(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise WebResearchError("UPSTREAM_ERROR", "Firecrawl returned an unexpected response")
    if value.get("success") is False:
        message = value.get("error") or value.get("message") or "Firecrawl rejected the request"
        raise WebResearchError("UPSTREAM_ERROR", str(message)[:500])
    data = value.get("data")
    return data if isinstance(data, dict) else value


class FirecrawlAPIClient:
    """Small REST client for the two Firecrawl read endpoints used by Stage 1."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_url: str | None = None,
        opener: Callable[..., Any] = urlopen,
    ) -> None:
        self.api_key = (api_key if api_key is not None else os.environ.get("FIRECRAWL_API_KEY", "")).strip()
        self.api_url = (api_url or os.environ.get("FIRECRAWL_API_URL") or "https://api.firecrawl.dev").rstrip("/")
        self.opener = opener

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise WebResearchError("BLOCKED", "BLOCKED — REQUIRED INPUT: Enterprise FIRECRAWL_API_KEY")
        request = Request(
            f"{self.api_url}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with self.opener(request, timeout=60) as response:
                body = response.read(MAX_RESPONSE_BYTES + 1)
        except HTTPError as exc:
            if exc.code in {401, 403}:
                message = "Firecrawl credential was rejected"
            elif exc.code in {408, 504}:
                raise WebResearchError("TIMEOUT", "Firecrawl request timed out") from exc
            else:
                message = f"Firecrawl upstream HTTP {exc.code}"
            raise WebResearchError("UPSTREAM_ERROR", message) from exc
        except (TimeoutError, socket.timeout) as exc:
            raise WebResearchError("TIMEOUT", "Firecrawl request timed out") from exc
        except URLError as exc:
            raise WebResearchError("UPSTREAM_ERROR", "Firecrawl upstream connection failed") from exc
        if len(body) > MAX_RESPONSE_BYTES:
            raise WebResearchError("UPSTREAM_ERROR", "Firecrawl response exceeded the size limit")
        try:
            parsed = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WebResearchError("UPSTREAM_ERROR", "Firecrawl returned invalid JSON") from exc
        return _json_object(parsed)

    def search(self, query: str, limit: int) -> dict[str, Any]:
        return self._post("/v2/search", {"query": query, "limit": limit})

    def fetch(self, url: str) -> dict[str, Any]:
        return self._post(
            "/v2/scrape",
            {"url": url, "formats": ["markdown"], "onlyMainContent": True},
        )


def _validate_search_args(arguments: dict[str, Any]) -> tuple[str, int]:
    if set(arguments) - {"query", "limit"}:
        raise WebResearchError("UNSUPPORTED", "web_search accepts only query and limit")
    query = arguments.get("query")
    if not isinstance(query, str) or not query.strip() or len(query.strip()) > MAX_QUERY_CHARS:
        raise WebResearchError("UNSUPPORTED", "query must be a non-empty string within the size limit")
    limit = arguments.get("limit", 10)
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_RESULTS:
        raise WebResearchError("UNSUPPORTED", f"limit must be an integer from 1 to {MAX_RESULTS}")
    return query.strip(), limit


def _validate_fetch_args(arguments: dict[str, Any]) -> str:
    if set(arguments) != {"url"}:
        raise WebResearchError("UNSUPPORTED", "web_fetch accepts only url")
    return validate_public_url(arguments["url"])


def _iter_search_items(raw: dict[str, Any]) -> Iterable[dict[str, Any]]:
    groups = raw.get("web") or raw.get("results")
    if isinstance(groups, list):
        for item in groups:
            if isinstance(item, dict):
                yield item
    for group_name in ("news", "images", "pdf"):
        group = raw.get(group_name)
        if isinstance(group, list):
            for item in group:
                if isinstance(item, dict):
                    yield item


def _first_text(item: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _normalize_search_result(item: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for output_key, source_keys in (
        ("title", ("title", "name")),
        ("url", ("url", "link")),
        ("snippet", ("description", "snippet", "content")),
        ("published_at", ("published_at", "publishedDate", "date")),
        ("source", ("source",)),
    ):
        value = _first_text(item, source_keys)
        if value is not None:
            result[output_key] = value
    return result


def _candidate_redirect_urls(raw: dict[str, Any]) -> list[str]:
    data = raw.get("data") if isinstance(raw.get("data"), dict) else raw
    metadata = data.get("metadata") if isinstance(data, dict) else None
    candidates: list[str] = []
    for container in (raw, data, metadata):
        if not isinstance(container, dict):
            continue
        for key in ("final_url", "finalUrl", "sourceURL", "sourceUrl", "url"):
            value = container.get(key)
            if isinstance(value, str) and value.strip() and value.strip() not in candidates:
                candidates.append(value.strip())
    return candidates


def _failure(error: WebResearchError, *, url: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": "FAILURE",
        "reason": error.reason,
        "error": str(error),
    }
    if url is not None:
        payload["url"] = url
    if error.reason == "SECURITY_REJECTED":
        payload["trust_class"] = TRUST_CLASS
    return payload


class WebResearchAdapter:
    """Normalize Firecrawl into the two-tool Enterprise contract."""

    def __init__(
        self,
        client: FirecrawlAPIClient | Any | None = None,
        *,
        clock: Callable[[], str] = _utc_now,
        resolver: Callable[[str, int], Iterable[Any]] = _default_resolver,
    ) -> None:
        self.client = client or FirecrawlAPIClient()
        self.clock = clock
        self.resolver = resolver

    def web_search(self, arguments: dict[str, Any]) -> dict[str, Any]:
        try:
            query, limit = _validate_search_args(arguments)
            raw = self.client.search(query, limit)
            results = [_normalize_search_result(item) for item in _iter_search_items(raw)]
            return {
                "status": "SUCCESS",
                "query": query,
                "results": results,
                "searched_at": self.clock(),
                "trust_class": TRUST_CLASS,
            }
        except WebResearchError as exc:
            return _failure(exc)
        except Exception:
            return _failure(WebResearchError("UPSTREAM_ERROR", "Web Research upstream failure"))

    def web_fetch(self, arguments: dict[str, Any]) -> dict[str, Any]:
        requested_url: str | None = None
        try:
            if isinstance(arguments.get("url"), str):
                requested_url = arguments["url"].strip()
            if set(arguments) != {"url"}:
                raise WebResearchError("UNSUPPORTED", "web_fetch accepts only url")
            requested_url = validate_public_url(arguments["url"], resolver=self.resolver)
            raw = self.client.fetch(requested_url)
            for candidate in _candidate_redirect_urls(raw):
                validate_public_url(candidate, resolver=self.resolver)
            data = _json_object(raw)
            metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
            markdown = data.get("markdown")
            if not isinstance(markdown, str):
                raise WebResearchError("UPSTREAM_ERROR", "Firecrawl did not return readable Markdown")
            final_url = _first_text(metadata, ("final_url", "finalUrl", "url", "sourceURL", "sourceUrl")) or _first_text(data, ("final_url", "finalUrl", "url", "sourceURL", "sourceUrl")) or requested_url
            result: dict[str, Any] = {
                "status": "SUCCESS",
                "url": requested_url,
                "final_url": final_url,
                "title": _first_text(metadata, ("title",)),
                "markdown": markdown,
                "metadata": {
                    "description": _first_text(metadata, ("description",)),
                    "language": _first_text(metadata, ("language", "lang")),
                },
                "retrieval": {
                    "method": "firecrawl",
                    "fallback_level": 1,
                    "retrieved_at": self.clock(),
                },
                "trust_class": TRUST_CLASS,
                "warnings": [],
            }
            return result
        except WebResearchError as exc:
            return _failure(exc, url=requested_url)
        except Exception:
            return _failure(WebResearchError("UPSTREAM_ERROR", "Web Research upstream failure"), url=requested_url)


TOOLS = [
    {
        "name": "web_search",
        "description": "Search the public Internet through the bounded Enterprise Web Research adapter.",
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "query": {"type": "string", "minLength": 1, "maxLength": MAX_QUERY_CHARS},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_RESULTS},
            },
            "required": ["query"],
        },
    },
    {
        "name": "web_fetch",
        "description": "Fetch readable Markdown from one public HTTP(S) page through Firecrawl.",
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {"url": {"type": "string", "minLength": 1}},
            "required": ["url"],
        },
    },
]


def _tool_result(payload: dict[str, Any], *, error: bool = False) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, sort_keys=True)}],
        "isError": error,
    }


def dispatch(message: dict[str, Any], adapter: WebResearchAdapter) -> dict[str, Any] | None:
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
                "serverInfo": {"name": "enterprise-web-research", "version": "1.0.0"},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        if not isinstance(params, dict) or not isinstance(params.get("arguments") or {}, dict):
            return {"jsonrpc": "2.0", "id": request_id, "result": _tool_result({"reason": "UNSUPPORTED", "error": "arguments must be an object"}, error=True)}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name == "web_search":
            payload = adapter.web_search(arguments)
        elif name == "web_fetch":
            payload = adapter.web_fetch(arguments)
        else:
            payload = {"status": "FAILURE", "reason": "UNSUPPORTED", "error": "unknown Web Research tool"}
        return {"jsonrpc": "2.0", "id": request_id, "result": _tool_result(payload, error=payload.get("status") == "FAILURE")}
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}


def main() -> int:
    adapter = WebResearchAdapter()
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            if isinstance(message, dict):
                response = dispatch(message, adapter)
                if response is not None:
                    sys.stdout.write(json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n")
                    sys.stdout.flush()
        except json.JSONDecodeError:
            continue
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
