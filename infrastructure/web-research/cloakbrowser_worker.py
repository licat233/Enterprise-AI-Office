#!/usr/bin/env python3
"""Fixed internal CloakBrowser read worker for Enterprise Web Research."""

from __future__ import annotations

import json
import os
import sys
from typing import Any


MAX_MARKDOWN_CHARS = 1_000_000
DEFAULT_BROWSER_VERSION = "145.0.7632.109.2"


def _failure(reason: str = "UPSTREAM_ERROR") -> int:
    sys.stdout.write(json.dumps({"status": "FAILURE", "reason": reason}, separators=(",", ":")) + "\n")
    sys.stdout.flush()
    return 1


def main() -> int:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        return _failure("UNSUPPORTED")
    url = sys.argv[1].strip()
    browser: Any | None = None
    page: Any | None = None
    try:
        from cloakbrowser import launch

        browser = launch(
            headless=True,
            browser_version=os.environ.get("EAIO_CLOAKBROWSER_VERSION", DEFAULT_BROWSER_VERSION),
        )
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=45_000)
        try:
            page.wait_for_load_state("networkidle", timeout=10_000)
        except Exception:
            pass
        title = page.title()
        final_url = page.url
        markdown = page.locator("body").inner_text(timeout=10_000)
        if not isinstance(markdown, str) or not markdown.strip():
            return _failure("UPSTREAM_ERROR")
        if len(markdown) > MAX_MARKDOWN_CHARS:
            markdown = markdown[:MAX_MARKDOWN_CHARS]
        sys.stdout.write(
            json.dumps(
                {
                    "status": "SUCCESS",
                    "final_url": final_url if isinstance(final_url, str) else url,
                    "title": title if isinstance(title, str) else None,
                    "markdown": markdown,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n"
        )
        sys.stdout.flush()
        return 0
    except Exception:
        return _failure()
    finally:
        if page is not None:
            try:
                page.close()
            except Exception:
                pass
        if browser is not None:
            try:
                browser.close()
            except Exception:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
