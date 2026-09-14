import importlib.util
import os
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).with_name("eao_admin_knowledge_action.py")
spec = importlib.util.spec_from_file_location("eao_admin_knowledge_action", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ActionUtilityTests(unittest.TestCase):
    def test_extract_urls_unique(self):
        self.assertEqual(
            module._extract_urls(
                "read https://example.com/a and https://example.com/a."
            ),
            ["https://example.com/a"],
        )

    def test_reject_local_url(self):
        with self.assertRaises(module.ActionError):
            module._validate_public_http_url(
                "http://localhost:8080/private"
            )

    def test_manual_title(self):
        self.assertEqual(
            module._manual_title("# Title\nBody"),
            "Title",
        )

    def test_file_ids_nested(self):
        self.assertEqual(
            module._file_ids(
                [
                    {"id": "a"},
                    {"file": {"id": "b"}},
                    {"file_id": "a"},
                ]
            ),
            ["a", "b"],
        )

    def test_operation_id_is_stable_and_bounded(self):
        first = module._operation_id(
            "chat",
            "msg",
            "sha256:" + "a" * 64,
            "kb",
        )
        second = module._operation_id(
            "chat",
            "msg",
            "sha256:" + "a" * 64,
            "kb",
        )
        self.assertEqual(first, second)
        self.assertTrue(
            first.startswith("knowledge-ingestion:")
        )
        self.assertLessEqual(len(first), 128)

    def test_knowledge_helpers(self):
        payload = {
            "success": True,
            "data": {
                "id": "k1",
                "parse_status": "completed",
            },
        }
        self.assertEqual(
            module._knowledge_id(payload),
            "k1",
        )
        self.assertEqual(
            module._parse_status(payload),
            "completed",
        )

    def test_multipart_contains_only_bounded_fields(self):
        body, content_type = module._multipart_file_body(
            "demo.txt",
            b"hello",
            "text/plain",
        )
        self.assertIn(b'name="file"', body)
        self.assertIn(b"hello", body)
        self.assertIn(b'name="channel"', body)
        self.assertIn(b"eao-admin", body)
        self.assertTrue(
            content_type.startswith(
                "multipart/form-data; boundary="
            )
        )

    def test_action_requires_bounded_ttl(self):
        old = dict(os.environ)
        try:
            os.environ["EAIO_EAO_ADMIN_GROUP_ID"] = "admins"
            os.environ[
                "EAIO_EAO_ADMIN_WEKNORA_BASE_URL"
            ] = "http://example.invalid/api/v1"
            os.environ[
                "EAIO_EAO_ADMIN_WEKNORA_API_KEY"
            ] = "test"
            os.environ["EAIO_EAO_ADMIN_KB_ID"] = "kb"
            os.environ[
                "EAIO_EAO_ADMIN_APPROVAL_SIGNING_KEY"
            ] = "secret"
            os.environ[
                "EAIO_EAO_ADMIN_APPROVAL_TTL_MINUTES"
            ] = "31"

            action = module.Action()
            with self.assertRaises(module.ActionError):
                action._require_config()
        finally:
            os.environ.clear()
            os.environ.update(old)


if __name__ == "__main__":
    unittest.main()
