from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "skills/shared/department/armor-memory/scripts/armor-route.py"
WRAPPER = ROOT / "skills/shared/department/armor-memory/scripts/route.sh"
SCOPED_MCP = ROOT / "skills/shared/department/armor-memory/scripts/armor-vault-mcp.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ROUTER_MODULE = load_module(ROUTER, "phase4c_armor_route")
MCP_MODULE = load_module(SCOPED_MCP, "phase4c_scoped_vault_mcp")


class RouterTests(unittest.TestCase):
    def test_wrapper_uses_local_router_without_arch_root(self):
        environment = dict(os.environ)
        environment.pop("ARMOR_ARCH_ROOT", None)
        result = subprocess.run(
            [str(WRAPPER), "--object", "work-product", "--domain", "website", "--artifact", "article"],
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[0], "02-Projects/Workspaces/Website/Articles/")
        self.assertNotIn("ARMOR_ARCH_ROOT", WRAPPER.read_text(encoding="utf-8"))

    def test_closed_routes_and_published_semantics(self):
        self.assertEqual(
            ROUTER_MODULE.route_request(object_type="work-product", domain="marketing", artifact="social-copy").path,
            "02-Projects/Workspaces/Marketing/Social-Media/",
        )
        self.assertEqual(
            ROUTER_MODULE.route_request(object_type="record", record_type="published").path,
            "03-Records/Published/",
        )
        with self.assertRaises(ValueError):
            ROUTER_MODULE.route_request(object_type="work-product", domain="website", artifact="unknown")
        with self.assertRaises(ValueError):
            ROUTER_MODULE.route_request(object_type="work-product", domain="website", artifact="article", project="../escape")


class ScopedVaultTests(unittest.TestCase):
    def package(self):
        return {
            "article-brief.json": json.dumps({"title": "Fixture"}),
            "seo-blueprint.json": json.dumps({"primary_keyword": "fixture"}),
            "article.md": "# Fixture Article\n",
            "audit-report.md": "# Audit\n\nPASS\n",
        }

    def test_only_four_files_and_no_unsafe_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                saved = MCP_MODULE._save_article_package({"package_id": "E2E Fixture", "files": self.package()})
                target = Path(temp) / saved["relative_path"]
                self.assertTrue(target.is_dir())
                self.assertEqual(set(p.name for p in target.iterdir()), set(MCP_MODULE.ARTICLE_FILES))
                with self.assertRaises(MCP_MODULE.ScopedVaultError):
                    MCP_MODULE._save_article_package({"package_id": "fixture", "files": {**self.package(), "extra.txt": "x"}})
                with self.assertRaises(MCP_MODULE.ScopedVaultError):
                    MCP_MODULE._save_article_package({"package_id": "../escape", "files": self.package()})
                with self.assertRaises(MCP_MODULE.ScopedVaultError):
                    MCP_MODULE._save_article_package({"package_id": "fixture", "files": self.package(), "destination": "03-Records/Published"})

    def test_mcp_initialize_tools_and_readback(self):
        with tempfile.TemporaryDirectory() as temp:
            environment = dict(os.environ)
            environment["ARMOR_VAULT_ROOT"] = temp
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "save_article_package", "arguments": {"package_id": "fixture", "files": self.package()}}},
            ]
            completed = subprocess.run(
                [sys.executable, str(SCOPED_MCP)],
                input="\n".join(json.dumps(message) for message in messages) + "\n",
                text=True,
                capture_output=True,
                env=environment,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            replies = [json.loads(line) for line in completed.stdout.splitlines()]
            self.assertEqual(replies[0]["result"]["serverInfo"]["version"], "1.0.0")
            self.assertEqual({tool["name"] for tool in replies[1]["result"]["tools"]}, {"route_work_product", "save_article_package"})
            saved = json.loads(replies[2]["result"]["content"][0]["text"])
            self.assertTrue(saved["read_back"])
            self.assertFalse(replies[2]["result"]["isError"])


if __name__ == "__main__":
    unittest.main()
