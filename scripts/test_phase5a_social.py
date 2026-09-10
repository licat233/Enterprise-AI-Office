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
MCP_PATH = ROOT / "skills/shared/department/armor-memory/scripts/armor-vault-mcp.py"
ROUTE_PATH = ROOT / "skills/shared/department/armor-memory/scripts/armor-route.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ROUTER = load_module(ROUTE_PATH, "phase5a_router")
MCP = load_module(MCP_PATH, "phase5a_mcp")


class SocialPackageTests(unittest.TestCase):
    def package(self):
        return {
            "topic-brief.yaml": "topic: fixture\napproval_required: true\n",
            "core-draft.md": "# Core Draft\n\nA grounded buyer lesson.\n",
            "social-copy.md": "# Social Copy\n\nhttps://www.armorlighting.com\n",
            "audit-report.md": "# Audit\n\nstatus: PASS\n",
        }

    def test_social_route_is_lifecycle_neutral(self):
        route = ROUTER.route_request(object_type="work-product", domain="marketing", artifact="social-copy")
        self.assertEqual(route.path, "02-Projects/Workspaces/Marketing/Social-Media/")
        self.assertNotIn("Published", route.path)

    def test_social_package_accepts_only_required_and_optional_files(self):
        with tempfile.TemporaryDirectory() as temp:
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                package = self.package()
                package["video-package.md"] = "# Video Package\n"
                saved = MCP._save_social_package({"package_id": "Fixture Reset", "files": package})
                target = Path(temp) / saved["relative_path"]
                self.assertEqual({path.name for path in target.iterdir()}, set(package))
                with self.assertRaises(MCP.ScopedVaultError):
                    MCP._save_social_package({"package_id": "fixture", "files": {**package, "unexpected.txt": "x"}})
                with self.assertRaises(MCP.ScopedVaultError):
                    MCP._save_social_package({"package_id": "../escape", "files": package})
                with self.assertRaises(MCP.ScopedVaultError):
                    MCP._save_social_package({"package_id": "fixture", "files": {key: value for key, value in package.items() if key != "audit-report.md"}})

    def test_social_package_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            destination = root / "02-Projects/Workspaces/Marketing/Social-Media"
            destination.mkdir(parents=True)
            (destination / "escape").symlink_to(outside, target_is_directory=True)
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                with self.assertRaises(MCP.ScopedVaultError):
                    MCP._save_social_package({"package_id": "escape", "files": self.package()})

    def test_mcp_lists_social_tool_without_changing_article_tool(self):
        with tempfile.TemporaryDirectory() as temp:
            environment = dict(os.environ)
            environment["ARMOR_VAULT_ROOT"] = temp
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "save_social_package", "arguments": {"package_id": "fixture", "files": self.package()}}},
            ]
            completed = subprocess.run(
                [sys.executable, str(MCP_PATH)],
                input="\n".join(json.dumps(message) for message in messages) + "\n",
                text=True,
                capture_output=True,
                env=environment,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            replies = [json.loads(line) for line in completed.stdout.splitlines()]
            names = {tool["name"] for tool in replies[1]["result"]["tools"]}
            self.assertEqual(names, {"route_work_product", "save_article_package", "save_social_package", "save_mic_product_package", "save_website_product_materials_package", "save_product_visual_package"})
            saved = json.loads(replies[2]["result"]["content"][0]["text"])
            self.assertTrue(saved["read_back"])
            self.assertFalse(replies[2]["result"]["isError"])


if __name__ == "__main__":
    unittest.main()
