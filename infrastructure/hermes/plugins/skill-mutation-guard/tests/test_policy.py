import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN_DIR))

from policy import SkillMutationGuard  # noqa: E402


def load_plugin_module():
    init_file = PLUGIN_DIR / "__init__.py"
    module_name = "eao_skill_mutation_guard_test_plugin"
    spec = importlib.util.spec_from_file_location(
        module_name,
        init_file,
        submodule_search_locations=[str(PLUGIN_DIR)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class FakeContext:
    profile_name = "operations"

    def __init__(self, settings):
        self.settings = settings
        self.hooks = []

    def get_config(self, key, default=None):
        return self.settings.get(key, default)

    def register_hook(self, name, callback):
        self.hooks.append((name, callback))


class SkillMutationGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "profile" / "skills"
        self.root.mkdir(parents=True)
        self.company_root = Path(self.temp.name) / "repo" / "skills" / "shared" / "department"
        self.company_root.mkdir(parents=True)
        self.company_skill = self.company_root / "company-skill"
        self.company_skill.mkdir()
        (self.company_skill / "SKILL.md").write_text("# company\n", encoding="utf-8")
        self.third_party_root = Path(self.temp.name) / "third-party"
        self.third_party_root.mkdir()
        self.third_party = self.third_party_root / "third-party-skill"
        self.third_party.mkdir()
        (self.third_party / "SKILL.md").write_text("# third party\n", encoding="utf-8")
        self.guard = SkillMutationGuard.from_config(
            profile_name="operations",
            learning_root=str(self.root),
            allowed_namespace="learned-",
        )

    def tearDown(self):
        self.temp.cleanup()

    def skill(self, name="learned-existing"):
        target = self.root / name
        target.mkdir(parents=True, exist_ok=True)
        (target / "SKILL.md").write_text("# learned\n", encoding="utf-8")
        return target

    def assertAllowed(self, args):
        self.assertIsNone(self.guard.pre_tool_call(tool_name="skill_manage", args=args))

    def assertBlocked(self, args):
        result = self.guard.pre_tool_call(tool_name="skill_manage", args=args)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("action"), "block")

    def test_read_only_tools_are_unaffected(self):
        self.assertIsNone(self.guard.pre_tool_call(tool_name="skill_view", args={}))
        self.assertIsNone(self.guard.pre_tool_call(tool_name="skills_list", args={}))

    def test_positive_single_mutations(self):
        self.skill()
        self.skill("learned-file")
        self.assertAllowed({"action": "create", "name": "learned-created"})
        self.assertAllowed({"action": "edit", "name": "learned-existing", "content": "# v2\n"})
        self.assertAllowed({"action": "patch", "name": "learned-existing", "old_string": "x", "new_string": "y"})
        self.assertAllowed({
            "action": "write_file",
            "name": "learned-file",
            "file_path": "references/example.md",
            "file_content": "x",
        })
        self.assertAllowed({
            "action": "remove_file",
            "name": "learned-file",
            "file_path": "references/example.md",
        })
        self.assertAllowed({"action": "delete", "name": "learned-existing"})

    def test_category_create_stays_inside_root(self):
        self.assertAllowed({"action": "create", "name": "learned-categorized", "category": "department"})
        self.assertBlocked({"action": "create", "name": "learned-escape", "category": "../company"})

    def test_non_learned_and_unknown_operations_block(self):
        self.assertBlocked({"action": "create", "name": "company-skill"})
        self.assertBlocked({"action": "archive", "name": "learned-existing"})
        self.assertBlocked({"name": "learned-existing"})
        self.assertBlocked({"action": "create", "name": "learned-existing/../../company-skill"})

    def test_company_symlink_blocks_every_mutation(self):
        link = self.root / "company-skill"
        os.symlink(self.company_skill, link)
        for action in ("edit", "patch", "delete", "write_file", "remove_file"):
            args = {"action": action, "name": "company-skill"}
            if action in {"patch", "write_file", "remove_file"}:
                args["file_path"] = "references/example.md"
            self.assertBlocked(args)

    def test_learned_namespace_symlink_to_company_blocks_every_mutation(self):
        link = self.root / "learned-company"
        os.symlink(self.company_skill, link)
        for action in ("create", "edit", "patch", "delete", "write_file", "remove_file"):
            args = {"action": action, "name": "learned-company"}
            if action in {"patch", "write_file", "remove_file"}:
                args["file_path"] = "references/example.md"
            self.assertBlocked(args)

    def test_learned_symlink_outside_and_third_party_block(self):
        outside = Path(self.temp.name) / "outside-skill"
        outside.mkdir()
        (outside / "SKILL.md").write_text("# outside\n", encoding="utf-8")
        os.symlink(outside, self.root / "learned-outside")
        self.assertBlocked({"action": "edit", "name": "learned-outside"})
        self.assertBlocked({"action": "create", "name": "third-party-skill"})
        self.assertBlocked({"action": "patch", "name": "third-party-skill"})

    def test_path_escape_and_bad_support_file_block(self):
        self.skill()
        self.assertBlocked({"action": "patch", "name": "/tmp/learned-existing"})
        self.assertBlocked({"action": "patch", "name": "learned-existing", "file_path": "../../company/SKILL.md"})
        self.assertBlocked({"action": "write_file", "name": "learned-existing", "file_path": "/tmp/outside", "file_content": "x"})
        self.assertBlocked({"action": "remove_file", "name": "learned-existing", "file_path": "unknown/file.md"})

    def test_batch_fails_before_mixed_mutation(self):
        self.assertBlocked({
            "operations": [
                {"action": "create", "name": "learned-ok", "content": "# ok\n"},
                {"action": "patch", "name": "company-skill", "file_path": "SKILL.md", "old_string": "x", "new_string": "y"},
            ]
        })
        self.assertAllowed({
            "operations": [
                {"action": "create", "name": "learned-new", "content": "# new\n"},
                {"action": "patch", "name": "learned-new", "old_string": "a", "new_string": "b"},
            ]
        })

    def test_malformed_batch_and_resolution_error_block(self):
        self.assertBlocked({"operations": None})
        self.assertBlocked({"operations": [{"action": "create", "name": "learned-x"}, "bad"]})
        cycle = self.root / "learned-cycle"
        os.symlink(cycle, cycle)
        self.assertBlocked({"action": "edit", "name": "learned-cycle"})

    def test_missing_configuration_blocks(self):
        guard = SkillMutationGuard.from_config(
            profile_name="operations",
            learning_root=None,
            allowed_namespace=None,
        )
        self.assertBlockedWith(guard, {"action": "create", "name": "learned-new"})

    def assertBlockedWith(self, guard, args):
        result = guard.pre_tool_call(tool_name="skill_manage", args=args)
        self.assertEqual(result.get("action"), "block")


class PluginRegistrationTests(unittest.TestCase):
    def test_operations_registers_hook(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_plugin_module()
            context = FakeContext({
                "profile": "operations",
                "learning_root": str(Path(tmp)),
                "allowed_namespace": "learned-",
            })
            module.register(context)
            self.assertEqual([name for name, _ in context.hooks], ["pre_tool_call"])

    def test_other_profile_is_not_implicitly_scoped(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_plugin_module()
            context = FakeContext({
                "profile": "operations",
                "learning_root": str(Path(tmp)),
                "allowed_namespace": "learned-",
            })
            context.profile_name = "general"
            module.register(context)
            self.assertEqual(context.hooks, [])


if __name__ == "__main__":
    unittest.main()
