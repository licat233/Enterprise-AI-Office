import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("phase4b_runtime_check.py")
SPEC = importlib.util.spec_from_file_location("phase4b_runtime_check", MODULE_PATH)
CHECKER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECKER)


class Phase4BCheckerTests(unittest.TestCase):
    def test_forbidden_active_reference_detection(self):
        self.assertTrue(CHECKER.has_forbidden_active_reference("/Users/licat/.hermes/skills"))
        self.assertTrue(CHECKER.has_forbidden_active_reference("mcp_Obsidian_search"))
        self.assertFalse(CHECKER.has_forbidden_active_reference("$ARMOR_VAULT_ROOT/02-Projects"))

    def test_router_requires_an_available_implementation(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            status, detail = CHECKER.router_state(repo)
            self.assertEqual("BLOCKED", status)
            self.assertIn("SCOPED_ROUTER_WRITE_BLOCKED", detail)

    def test_router_accepts_explicit_architecture_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            arch = Path(tmp) / "arch"
            (repo / "minimal-stable/scripts").mkdir(parents=True)
            (arch / "minimal-stable/scripts").mkdir(parents=True)
            route = arch / "minimal-stable/scripts/armor-route.py"
            route.write_text("# fixture\n", encoding="utf-8")
            status, detail = CHECKER.router_state(repo, arch)
            self.assertEqual("READY", status)
            self.assertEqual(str(route), detail)


if __name__ == "__main__":
    unittest.main()
