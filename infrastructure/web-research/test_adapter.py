from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import adapter  # noqa: E402


PUBLIC_RESOLVER = lambda host, port: ["93.184.216.34"]


class StubFirecrawl:
    def __init__(self, *, search=None, fetch=None):
        self.search_response = search or {"web": []}
        self.fetch_response = fetch or {
            "markdown": "# Example",
            "metadata": {"title": "Example", "description": "A page", "language": "en"},
        }
        self.calls: list[tuple[str, object]] = []

    def search(self, query, limit):
        self.calls.append(("search", (query, limit)))
        return self.search_response

    def fetch(self, url):
        self.calls.append(("fetch", url))
        return self.fetch_response


class WebResearchAdapterTests(unittest.TestCase):
    def test_public_http_and_https_urls_are_allowed(self):
        self.assertEqual(adapter.validate_public_url("https://example.com/", resolver=PUBLIC_RESOLVER), "https://example.com/")
        self.assertEqual(adapter.validate_public_url("http://example.com/path", resolver=PUBLIC_RESOLVER), "http://example.com/path")

    def test_unsafe_url_classes_are_rejected(self):
        urls = (
            "file:///etc/passwd",
            "ftp://example.com/file",
            "http://localhost/",
            "http://127.0.0.1/",
            "http://127.1/",
            "http://[::1]/",
            "http://10.0.0.1/",
            "http://172.16.0.1/",
            "http://192.168.1.1/",
            "http://169.254.169.254/",
        )
        for url in urls:
            with self.subTest(url=url):
                with self.assertRaises(adapter.WebResearchError) as ctx:
                    adapter.validate_public_url(url, resolver=PUBLIC_RESOLVER)
                self.assertEqual(ctx.exception.reason, "SECURITY_REJECTED")

    def test_dns_resolution_must_be_public(self):
        with self.assertRaises(adapter.WebResearchError) as ctx:
            adapter.validate_public_url("https://example.com/", resolver=lambda host, port: ["192.168.1.1"])
        self.assertEqual(ctx.exception.reason, "SECURITY_REJECTED")

    def test_search_normalizes_firecrawl_results_without_fabricating_metadata(self):
        client = StubFirecrawl(
            search={
                "web": [
                    {"title": "Example result", "url": "https://example.com", "description": "Evidence", "publishedDate": "2026-09-10"},
                    {"title": "No optional metadata", "url": "https://example.org"},
                ]
            }
        )
        result = adapter.WebResearchAdapter(client, clock=lambda: "2026-09-10T00:00:00Z").web_search({"query": "example", "limit": 2})
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["searched_at"], "2026-09-10T00:00:00Z")
        self.assertEqual(result["trust_class"], "UNTRUSTED_WEB_CONTENT")
        self.assertEqual(result["results"][0]["published_at"], "2026-09-10")
        self.assertNotIn("snippet", result["results"][1])
        self.assertEqual(client.calls, [("search", ("example", 2))])

    def test_fetch_normalizes_response_and_marks_web_content_untrusted(self):
        client = StubFirecrawl(
            fetch={
                "data": {
                    "markdown": "# Example",
                    "metadata": {"title": "Example", "description": "A page", "language": "en", "url": "https://example.com/final"},
                }
            }
        )
        result = adapter.WebResearchAdapter(client, clock=lambda: "2026-09-10T00:00:00Z", resolver=PUBLIC_RESOLVER).web_fetch({"url": "https://example.com/"})
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["trust_class"], "UNTRUSTED_WEB_CONTENT")
        self.assertEqual(result["retrieval"], {"method": "firecrawl", "fallback_level": 1, "retrieved_at": "2026-09-10T00:00:00Z"})
        self.assertEqual(result["final_url"], "https://example.com/final")
        self.assertEqual(result["metadata"]["language"], "en")

    def test_public_to_private_redirect_is_rejected_after_upstream_response(self):
        client = StubFirecrawl(
            fetch={
                "markdown": "not returned to caller",
                "metadata": {"url": "http://127.0.0.1/"},
            }
        )
        result = adapter.WebResearchAdapter(client, resolver=PUBLIC_RESOLVER).web_fetch({"url": "https://example.com/"})
        self.assertEqual(result["status"], "FAILURE")
        self.assertEqual(result["reason"], "SECURITY_REJECTED")
        self.assertEqual(client.calls, [("fetch", "https://example.com/")])

    def test_blocked_url_makes_no_upstream_call(self):
        client = StubFirecrawl()
        result = adapter.WebResearchAdapter(client, resolver=PUBLIC_RESOLVER).web_fetch({"url": "http://127.0.0.1/"})
        self.assertEqual(result["reason"], "SECURITY_REJECTED")
        self.assertEqual(client.calls, [])

    def test_missing_credential_is_explicit_and_does_not_persist(self):
        client = adapter.FirecrawlAPIClient(api_key="", opener=lambda request, timeout: None)
        with self.assertRaises(adapter.WebResearchError) as ctx:
            client.search("example", 1)
        self.assertEqual(ctx.exception.reason, "BLOCKED")
        self.assertIn("BLOCKED — REQUIRED INPUT: Enterprise FIRECRAWL_API_KEY", str(ctx.exception))
        self.assertFalse(any(ROOT.glob("**/web-research-state*")))

        result = adapter.WebResearchAdapter(client).web_search({"query": "example", "limit": 1})
        self.assertEqual(result["status"], "FAILURE")
        self.assertEqual(result["reason"], "BLOCKED")
        self.assertEqual(result["error"], "BLOCKED — REQUIRED INPUT: Enterprise FIRECRAWL_API_KEY")

    def test_mcp_surface_is_exactly_two_tools_and_rejects_raw_firecrawl_names(self):
        client = StubFirecrawl()
        research = adapter.WebResearchAdapter(client, resolver=PUBLIC_RESOLVER)
        listed = adapter.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, research)
        self.assertEqual({tool["name"] for tool in listed["result"]["tools"]}, {"web_search", "web_fetch"})
        called = adapter.dispatch(
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "firecrawl_scrape", "arguments": {"url": "https://example.com/"}}},
            research,
        )
        self.assertTrue(called["result"]["isError"])
        self.assertEqual(client.calls, [])


class FirecrawlAPIClientTests(unittest.TestCase):
    def test_firecrawl_rest_request_is_normalized(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self, size):
                return json.dumps({"success": True, "data": {"markdown": "ok"}}).encode()

        seen = {}

        def opener(request, timeout):
            seen["url"] = request.full_url
            seen["authorization"] = request.headers["Authorization"]
            seen["body"] = json.loads(request.data.decode())
            seen["timeout"] = timeout
            return Response()

        client = adapter.FirecrawlAPIClient(api_key="enterprise-test-key", opener=opener)
        self.assertEqual(client.fetch("https://example.com/")["markdown"], "ok")
        self.assertEqual(seen["url"], "https://api.firecrawl.dev/v2/scrape")
        self.assertEqual(seen["body"]["formats"], ["markdown"])
        self.assertEqual(seen["timeout"], 60)


if __name__ == "__main__":
    unittest.main()
