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
import select
import socket
import subprocess
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
MAX_OBSCURA_MARKDOWN_CHARS = 1_000_000
MAX_CLOAKBROWSER_MARKDOWN_CHARS = 1_000_000
OBSCURA_TIMEOUT_SECONDS = 45
CLOAKBROWSER_TIMEOUT_SECONDS = 90
DEFAULT_OBSCURA_BIN = "/Users/armor/.local/bin/obscura"
DEFAULT_OBSCURA_STORAGE_DIR = "/Users/armor/.local/share/enterprise-mcp/obscura"
DEFAULT_CLOAKBROWSER_PYTHON = "/Users/armor/.local/share/enterprise-mcp/cloakbrowser-runtime/bin/python"
DEFAULT_CLOAKBROWSER_WORKER = "/Users/armor/Enterprise-AI-Office/infrastructure/web-research/cloakbrowser_worker.py"
DEFAULT_CLOAKBROWSER_STORAGE_DIR = "/Users/armor/.local/share/enterprise-mcp/cloakbrowser"
DEFAULT_CLOAKBROWSER_VERSION = "145.0.7632.109.2"
APPROVED_CLOAKBROWSER_ROOTS = (
    "/Users/armor/.local/share/enterprise-mcp",
    "/Users/armor/.local/share/uv",
    "/Users/armor/Enterprise-AI-Office",
)
OBSCURA_PROTOCOL_VERSION = "2024-11-05"
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
SNAPSHOT_URL = re.compile(r"^URL:\s*(\S+)\s*$", re.MULTILINE)
SNAPSHOT_TITLE = re.compile(r"^Title:\s*(.*?)\s*$", re.MULTILINE)
FALLBACK_REASONS = frozenset({"BLOCKED", "TIMEOUT", "UPSTREAM_ERROR"})
DYNAMIC_SHELL_MARKERS = frozenset(
    {
        "enable javascript",
        "javascript is required",
        "checking your browser",
        "just a moment",
        "please wait while we verify",
        "loading...",
        "请验证",
    }
)
LOGIN_MARKERS = frozenset(
    {
        "login required",
        "log in to continue",
        "sign in to continue",
        "authentication required",
    }
)
CAPTCHA_MARKERS = frozenset(
    {
        "captcha required",
        "verify you are human",
        "complete the captcha",
        "recaptcha challenge",
        "hcaptcha challenge",
    }
)


class WebResearchError(ValueError):
    """A finite, safe error that may be returned to an employee task."""

    def __init__(self, reason: str, message: str) -> None:
        if reason not in FAILURE_REASONS:
            raise ValueError(f"unsupported Web Research failure reason: {reason}")
        super().__init__(message)
        self.reason = reason


class ObscuraError(WebResearchError):
    """A safe, finite error from the internal Obscura fallback."""


class CloakBrowserError(WebResearchError):
    """A safe, finite error from the internal CloakBrowser fallback."""


def _mcp_text(result: dict[str, Any], *, backend: str) -> str:
    if result.get("isError") is True:
        raise ObscuraError("UPSTREAM_ERROR", f"{backend} returned a bounded failure")
    content = result.get("content")
    if not isinstance(content, list):
        raise ObscuraError("UPSTREAM_ERROR", f"{backend} returned unreadable content")
    text_parts = [
        item.get("text")
        for item in content
        if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str)
    ]
    if not text_parts:
        raise ObscuraError("UPSTREAM_ERROR", f"{backend} returned unreadable content")
    return "\n".join(text_parts)


class ObscuraClient:
    """Fixed, internal MCP sequence for a public rendered-page fallback.

    This client intentionally does not expose or call generic browser controls.
    Each fetch gets a fresh process and uses only navigate, snapshot, and
    markdown against the approved Enterprise storage directory.
    """

    def __init__(
        self,
        *,
        command: str | None = None,
        storage_dir: str | None = None,
        timeout: float = OBSCURA_TIMEOUT_SECONDS,
        popen: Callable[..., Any] = subprocess.Popen,
    ) -> None:
        self.command = (command or os.environ.get("EAIO_OBSCURA_BIN") or DEFAULT_OBSCURA_BIN).strip()
        self.storage_dir = (
            storage_dir or os.environ.get("EAIO_OBSCURA_STORAGE_DIR") or DEFAULT_OBSCURA_STORAGE_DIR
        ).strip()
        self.timeout = timeout
        self.popen = popen
        self._process: Any | None = None
        self._next_id = 0

    def _bounded_storage_dir(self) -> str:
        if not self.storage_dir or not os.path.isabs(self.storage_dir):
            raise ObscuraError("BLOCKED", "Obscura Enterprise storage is not configured")
        if not os.path.isdir(self.storage_dir):
            raise ObscuraError("BLOCKED", "Obscura Enterprise storage is unavailable")
        approved_root = os.path.realpath(
            os.environ.get("EAIO_OBSCURA_STORAGE_ROOT") or "/Users/armor/.local/share/enterprise-mcp"
        )
        resolved = os.path.realpath(self.storage_dir)
        try:
            within_root = os.path.commonpath((approved_root, resolved)) == approved_root
        except ValueError:
            within_root = False
        if not within_root:
            raise ObscuraError("BLOCKED", "Obscura storage is outside the Enterprise boundary")
        return resolved

    def _start(self) -> None:
        if not self.command or not os.path.isfile(self.command) or not os.access(self.command, os.X_OK):
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback is unavailable")
        storage_dir = self._bounded_storage_dir()
        child_env = {
            key: os.environ[key]
            for key in (
                "PATH",
                "HOME",
                "TMPDIR",
                "TMP",
                "TEMP",
                "LANG",
                "LC_ALL",
                "SSL_CERT_FILE",
                "SSL_CERT_DIR",
            )
            if key in os.environ
        }
        try:
            self._process = self.popen(
                [self.command, "--storage-dir", storage_dir, "mcp"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                env=child_env,
                text=True,
                bufsize=1,
            )
        except (OSError, ValueError) as exc:
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback could not start") from exc

    def _request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if self._process is None or self._process.stdin is None or self._process.stdout is None:
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback is not running")
        self._next_id += 1
        message = {"jsonrpc": "2.0", "id": self._next_id, "method": method}
        if params is not None:
            message["params"] = params
        try:
            self._process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
            self._process.stdin.flush()
            ready, _, _ = select.select([self._process.stdout], [], [], self.timeout)
            if not ready:
                raise ObscuraError("TIMEOUT", "Obscura fallback timed out")
            line = self._process.stdout.readline()
            if not line:
                raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback ended unexpectedly")
            response = json.loads(line)
        except ObscuraError:
            raise
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback returned an invalid response") from exc
        if not isinstance(response, dict) or response.get("id") != self._next_id:
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback returned an invalid response")
        if isinstance(response.get("error"), dict):
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback rejected the request")
        result = response.get("result")
        if not isinstance(result, dict):
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback returned an invalid result")
        return result

    def _notify_initialized(self) -> None:
        if self._process is None or self._process.stdin is None:
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback is not running")
        try:
            self._process.stdin.write(
                json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}, separators=(",", ":")) + "\n"
            )
            self._process.stdin.flush()
        except OSError as exc:
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback could not initialize") from exc

    def close(self) -> None:
        process = self._process
        self._process = None
        if process is None:
            return
        try:
            if process.stdin is not None:
                process.stdin.close()
        except OSError:
            pass
        try:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=2)
        except (OSError, subprocess.TimeoutExpired):
            try:
                process.kill()
                process.wait(timeout=2)
            except (OSError, subprocess.TimeoutExpired):
                pass

    def fetch(self, url: str) -> dict[str, Any]:
        try:
            self._start()
            self._request(
                "initialize",
                {
                    "protocolVersion": OBSCURA_PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": {"name": "enterprise-web-research", "version": "1.0.0"},
                },
            )
            self._notify_initialized()
            tools = self._request("tools/list")
            tool_names = {
                tool.get("name")
                for tool in tools.get("tools", [])
                if isinstance(tool, dict) and isinstance(tool.get("name"), str)
            }
            required_tools = {"browser_navigate", "browser_snapshot", "browser_markdown"}
            if not required_tools.issubset(tool_names):
                raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback lacks the required read interface")
            self._request(
                "tools/call",
                {
                    "name": "browser_navigate",
                    "arguments": {"url": url, "waitUntil": "domcontentloaded"},
                },
            )
            snapshot = _mcp_text(
                self._request("tools/call", {"name": "browser_snapshot", "arguments": {"max_chars": 4_000}}),
                backend="Obscura snapshot",
            )
            markdown = _mcp_text(
                self._request(
                    "tools/call",
                    {"name": "browser_markdown", "arguments": {"max_chars": MAX_OBSCURA_MARKDOWN_CHARS}},
                ),
                backend="Obscura Markdown",
            )
            final_url = _first_match(snapshot, SNAPSHOT_URL) or url
            title = _first_match(snapshot, SNAPSHOT_TITLE)
            return {"final_url": final_url, "title": title, "markdown": markdown}
        except ObscuraError:
            raise
        except Exception as exc:
            raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback failed") from exc
        finally:
            self.close()


class CloakBrowserClient:
    """Fixed, internal read-only sequence using the approved CloakBrowser worker.

    This client starts a fresh worker for each URL. The worker has no input
    surface beyond the already-validated URL and performs navigate, bounded
    wait, final URL/title read, and body-text read only.
    """

    def __init__(
        self,
        *,
        python: str | None = None,
        worker: str | None = None,
        storage_dir: str | None = None,
        browser_version: str | None = None,
        timeout: float = CLOAKBROWSER_TIMEOUT_SECONDS,
        runner: Callable[..., Any] = subprocess.run,
    ) -> None:
        self.python = (python or os.environ.get("EAIO_CLOAKBROWSER_PYTHON") or DEFAULT_CLOAKBROWSER_PYTHON).strip()
        self.worker = (worker or os.environ.get("EAIO_CLOAKBROWSER_WORKER") or DEFAULT_CLOAKBROWSER_WORKER).strip()
        self.storage_dir = (
            storage_dir
            or os.environ.get("EAIO_CLOAKBROWSER_STORAGE_DIR")
            or DEFAULT_CLOAKBROWSER_STORAGE_DIR
        ).strip()
        self.browser_version = (
            browser_version
            or os.environ.get("EAIO_CLOAKBROWSER_VERSION")
            or DEFAULT_CLOAKBROWSER_VERSION
        ).strip()
        self.timeout = timeout
        self.runner = runner

    def _bounded_path(self, value: str, *, executable: bool = False) -> str:
        if not value or not os.path.isabs(value):
            raise CloakBrowserError("BLOCKED", "CloakBrowser Enterprise runtime is not configured")
        resolved = os.path.realpath(value)
        try:
            within_root = any(os.path.commonpath((root, resolved)) == root for root in APPROVED_CLOAKBROWSER_ROOTS)
        except ValueError:
            within_root = False
        if not within_root:
            raise CloakBrowserError("BLOCKED", "CloakBrowser runtime is outside the Enterprise boundary")
        if executable and (not os.path.isfile(resolved) or not os.access(resolved, os.X_OK)):
            raise CloakBrowserError("UPSTREAM_ERROR", "CloakBrowser fallback is unavailable")
        # Preserve an approved virtual-environment launcher symlink for the
        # interpreter. Executing its realpath directly can drop the venv's
        # import context even though the target remains Enterprise-owned.
        return os.path.abspath(value) if executable else resolved

    def fetch(self, url: str) -> dict[str, Any]:
        python = self._bounded_path(self.python, executable=True)
        worker = self._bounded_path(self.worker, executable=False)
        storage_dir = self._bounded_path(self.storage_dir, executable=False)
        if not os.path.isdir(storage_dir):
            raise CloakBrowserError("UPSTREAM_ERROR", "CloakBrowser fallback is unavailable")
        child_env = {
            key: os.environ[key]
            for key in (
                "PATH",
                "HOME",
                "TMPDIR",
                "TMP",
                "TEMP",
                "LANG",
                "LC_ALL",
                "SSL_CERT_FILE",
                "SSL_CERT_DIR",
            )
            if key in os.environ
        }
        child_env.update(
            {
                "CLOAKBROWSER_CACHE_DIR": storage_dir,
                "CLOAKBROWSER_VERSION": self.browser_version,
                "EAIO_CLOAKBROWSER_VERSION": self.browser_version,
            }
        )
        try:
            completed = self.runner(
                [python, worker, url],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
                env=child_env,
            )
        except subprocess.TimeoutExpired as exc:
            raise CloakBrowserError("TIMEOUT", "CloakBrowser fallback timed out") from exc
        except (OSError, ValueError) as exc:
            raise CloakBrowserError("UPSTREAM_ERROR", "CloakBrowser fallback could not start") from exc
        if getattr(completed, "returncode", 1) != 0:
            raise CloakBrowserError("UPSTREAM_ERROR", "CloakBrowser fallback failed")
        stdout = getattr(completed, "stdout", "")
        if not isinstance(stdout, str):
            raise CloakBrowserError("UPSTREAM_ERROR", "CloakBrowser fallback returned invalid output")
        response: dict[str, Any] | None = None
        for line in reversed(stdout.splitlines()):
            if not line.strip():
                continue
            try:
                candidate = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(candidate, dict):
                response = candidate
                break
        if response is None:
            raise CloakBrowserError("UPSTREAM_ERROR", "CloakBrowser fallback returned invalid output")
        if response.get("status") != "SUCCESS":
            reason = response.get("reason")
            if reason not in FAILURE_REASONS:
                reason = "UPSTREAM_ERROR"
            raise CloakBrowserError(reason, "CloakBrowser fallback could not retrieve the public page")
        markdown = response.get("markdown")
        if not isinstance(markdown, str) or not markdown.strip() or len(markdown) > MAX_CLOAKBROWSER_MARKDOWN_CHARS:
            raise CloakBrowserError("UPSTREAM_ERROR", "CloakBrowser fallback returned unreadable content")
        return {
            "final_url": response.get("final_url"),
            "title": response.get("title"),
            "markdown": markdown,
        }


def _first_match(value: str, pattern: re.Pattern[str]) -> str | None:
    match = pattern.search(value)
    if not match:
        return None
    candidate = match.group(1).strip()
    return candidate or None


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


def _page_access_reason(markdown: str) -> str | None:
    compact = " ".join(markdown.split()).lower()
    if any(marker in compact for marker in CAPTCHA_MARKERS):
        return "CAPTCHA_REQUIRED"
    if any(marker in compact for marker in LOGIN_MARKERS):
        return "LOGIN_REQUIRED"
    return None


def _needs_dynamic_fallback(markdown: str) -> bool:
    compact = " ".join(markdown.split()).lower()
    if not compact:
        return True
    if any(marker in compact for marker in DYNAMIC_SHELL_MARKERS) and len(compact) <= 2_000:
        return True
    return False


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


def _normalize_fetch_result(
    raw: dict[str, Any],
    *,
    requested_url: str,
    method: str,
    fallback_level: int,
    clock: Callable[[], str],
    resolver: Callable[[str, int], Iterable[Any]],
) -> dict[str, Any]:
    for candidate in _candidate_redirect_urls(raw):
        validate_public_url(candidate, resolver=resolver)
    data = _json_object(raw)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    markdown = data.get("markdown")
    if not isinstance(markdown, str) or not markdown.strip():
        raise WebResearchError("UPSTREAM_ERROR", "Web Research did not return readable Markdown")
    access_reason = _page_access_reason(markdown)
    if access_reason is not None:
        messages = {
            "LOGIN_REQUIRED": "The public page requires login",
            "CAPTCHA_REQUIRED": "The public page requires CAPTCHA completion",
        }
        raise WebResearchError(access_reason, messages[access_reason])
    final_url = (
        _first_text(metadata, ("final_url", "finalUrl", "url", "sourceURL", "sourceUrl"))
        or _first_text(data, ("final_url", "finalUrl", "url", "sourceURL", "sourceUrl"))
        or requested_url
    )
    return {
        "status": "SUCCESS",
        "url": requested_url,
        "final_url": final_url,
        "title": _first_text(metadata, ("title",)) or _first_text(data, ("title",)),
        "markdown": markdown,
        "metadata": {
            "description": _first_text(metadata, ("description",)),
            "language": _first_text(metadata, ("language", "lang")),
        },
        "retrieval": {
            "method": method,
            "fallback_level": fallback_level,
            "retrieved_at": clock(),
        },
        "trust_class": TRUST_CLASS,
        "warnings": [],
    }


class WebResearchAdapter:
    """Normalize Firecrawl and the bounded internal fallback chain."""

    def __init__(
        self,
        client: FirecrawlAPIClient | Any | None = None,
        *,
        obscura: Any | None = None,
        cloakbrowser: Any | None = None,
        clock: Callable[[], str] = _utc_now,
        resolver: Callable[[str, int], Iterable[Any]] = _default_resolver,
    ) -> None:
        self.client = client or FirecrawlAPIClient()
        self.obscura = obscura if obscura is not None else ObscuraClient()
        self.cloakbrowser = cloakbrowser if cloakbrowser is not None else CloakBrowserClient()
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
            try:
                raw = self.client.fetch(requested_url)
                result = _normalize_fetch_result(
                    raw,
                    requested_url=requested_url,
                    method="firecrawl",
                    fallback_level=1,
                    clock=self.clock,
                    resolver=self.resolver,
                )
                if _needs_dynamic_fallback(result["markdown"]):
                    raise WebResearchError("UPSTREAM_ERROR", "Firecrawl returned an empty or dynamic shell")
                return result
            except WebResearchError as primary_error:
                if primary_error.reason not in FALLBACK_REASONS:
                    raise
                try:
                    obscura_raw = self.obscura.fetch(requested_url)
                    if not isinstance(obscura_raw, dict):
                        raise ObscuraError("UPSTREAM_ERROR", "Obscura fallback returned an invalid response")
                    obscura_result = _normalize_fetch_result(
                        obscura_raw,
                        requested_url=requested_url,
                        method="obscura",
                        fallback_level=2,
                        clock=self.clock,
                        resolver=self.resolver,
                    )
                    if _needs_dynamic_fallback(obscura_result["markdown"]):
                        raise WebResearchError("UPSTREAM_ERROR", "Obscura returned an empty or verification shell")
                    return obscura_result
                except WebResearchError as fallback_error:
                    if fallback_error.reason in {"SECURITY_REJECTED", "LOGIN_REQUIRED", "CAPTCHA_REQUIRED"}:
                        raise
                    try:
                        cloakbrowser_raw = self.cloakbrowser.fetch(requested_url)
                        if not isinstance(cloakbrowser_raw, dict):
                            raise CloakBrowserError("UPSTREAM_ERROR", "CloakBrowser fallback returned an invalid response")
                        return _normalize_fetch_result(
                            cloakbrowser_raw,
                            requested_url=requested_url,
                            method="cloakbrowser",
                            fallback_level=3,
                            clock=self.clock,
                            resolver=self.resolver,
                        )
                    except WebResearchError as cloakbrowser_error:
                        if cloakbrowser_error.reason in {"SECURITY_REJECTED", "LOGIN_REQUIRED", "CAPTCHA_REQUIRED"}:
                            raise
                        raise WebResearchError("UPSTREAM_ERROR", "Web Research could not retrieve the public page") from cloakbrowser_error
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
