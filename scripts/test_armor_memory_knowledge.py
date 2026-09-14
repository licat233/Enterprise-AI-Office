from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/shared/department/armor-memory/scripts"
KNOWLEDGE = SCRIPTS / "knowledge.sh"
ROUTE = SCRIPTS / "route.sh"
SCOPED_MCP = SCRIPTS / "armor-vault-mcp.py"


def run_script(
    script: Path,
    *args: str,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.pop("ARMOR_ARCH_ROOT", None)
    environment["BASH_ENV"] = "/dev/null"
    if env:
        environment.update(env)
    command = [str(script), *args]
    if script.suffix == ".sh":
        command = ["/bin/bash", *command]
    return subprocess.run(
        command,
        text=True,
        capture_output=True,
        env=environment,
        check=False,
    )


def create_minimal_vault(root: Path) -> Path:
    knowledge = root / "01-Knowledge"
    knowledge.mkdir(parents=True)
    fixture = knowledge / "fixture.md"
    fixture.write_text(
        "---\n"
        "authority: canonical\n"
        "source_ref: test://armor-memory-knowledge-helper\n"
        "---\n"
        "# Fixture Knowledge\n\n"
        "This fixture is used only for read-only helper validation.\n",
        encoding="utf-8",
    )
    return fixture


def relative_entries(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))


class KnowledgeHelperTests(unittest.TestCase):
    def test_check_finds_sibling_helper_without_arch_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture = create_minimal_vault(root)
            before = fixture.read_bytes()
            result = run_script(KNOWLEDGE, "check", "--vault", str(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Knowledge files: 1", result.stdout)
            self.assertIn("Errors: 0", result.stdout)
            self.assertEqual(fixture.read_bytes(), before)

    def test_diff_is_read_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            current = root / "current.md"
            candidate = root / "candidate.md"
            current.write_text("# Current\n", encoding="utf-8")
            candidate.write_text("# Candidate\n", encoding="utf-8")
            before_entries = relative_entries(root)
            before_current = current.read_bytes()
            before_candidate = candidate.read_bytes()
            result = run_script(KNOWLEDGE, "diff", str(current), str(candidate))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--- ", result.stdout)
            self.assertIn("+++ ", result.stdout)
            self.assertEqual(relative_entries(root), before_entries)
            self.assertEqual(current.read_bytes(), before_current)
            self.assertEqual(candidate.read_bytes(), before_candidate)

    def test_missing_or_invalid_vault_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            missing = run_script(KNOWLEDGE, "check", "--vault", str(root / "missing"))
            self.assertEqual(missing.returncode, 2)
            self.assertIn("vault root does not exist", missing.stderr)
            invalid_root = root / "invalid"
            invalid_root.mkdir()
            invalid = run_script(KNOWLEDGE, "check", "--vault", str(invalid_root))
            self.assertEqual(invalid.returncode, 2)
            self.assertIn("knowledge directory not found", invalid.stderr)

    def test_route_behavior_is_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            result = run_script(
                ROUTE,
                "--absolute",
                "--object",
                "work-product",
                "--domain",
                "website",
                "--artifact",
                "article",
                env={"ARMOR_VAULT_ROOT": temp},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                result.stdout.splitlines()[0],
                f"{temp}/02-Projects/Workspaces/Website/Articles/",
            )
            self.assertNotIn("ARMOR_ARCH_ROOT", ROUTE.read_text(encoding="utf-8"))

    def test_scoped_mcp_surface_is_unchanged(self):
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        ]
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                [sys.executable, str(SCOPED_MCP)],
                input="\n".join(json.dumps(message) for message in messages) + "\n",
                text=True,
                capture_output=True,
                env={**os.environ, "ARMOR_VAULT_ROOT": temp},
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        replies = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(replies[0]["result"]["serverInfo"]["version"], "1.0.0")
        self.assertEqual(
            {tool["name"] for tool in replies[1]["result"]["tools"]},
            {
                "route_work_product",
                "save_article_package",
                "save_social_package",
                "save_mic_product_package",
                "save_website_product_materials_package",
                "save_product_visual_package",
            },
        )


if __name__ == "__main__":
    unittest.main()
