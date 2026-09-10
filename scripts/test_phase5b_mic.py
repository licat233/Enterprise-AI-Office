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


ROUTER = load_module(ROUTE_PATH, "phase5b_router")
MCP = load_module(MCP_PATH, "phase5b_mcp")


MIC_DATA = """schema: armor-mic-product/v1
product:
  name: Slim Magnetic LED Shelf Light for Retail Cabinet with 10x10mm Profile
  model: HM-MSL-S10-24V-65K80-S-V1
  category: LED Light
facts:
  profile_size:
    value: 10x10mm
    class: MIC_EXISTING_SOURCE
    source: 02-Projects/Workspaces/Products/MIC-Products/2026-06-15_10x10-Slender-Magnetic-LED-Shelf-Light/MIC-BulkFill-Paste-Ready.md
  magnetic_mount:
    value: 30mm magnets, 6 per meter
    class: CANONICAL_KNOWLEDGE
    source: 01-Knowledge/Products/entities/magnetic-mounting-system.md
  voltage:
    value: 12V; 24V variants
    class: CANONICAL_KNOWLEDGE
    source: 01-Knowledge/Products/entities/armor-10x10mm-slim-magnetic-led-shelf-light.md
  package_dimensions:
    value: UNKNOWN
    class: UNKNOWN
    source: not supplied in the acceptance input
unknowns:
  - Current MIC edit-page candidate list for center words
  - Current packaging evidence
blockers: []
approval_status: APPROVED_FOR_SAVE
publication_performed: false
"""


MIC_BULKFILL = """# 基本信息
产品名称：Slim Magnetic LED Shelf Light for Retail Cabinet with 10x10mm Profile
中心词：Light; Shelf; Cabinet; LED; Magnetic
关键词：Magnetic LED Shelf Light; Slim LED Cabinet Light; 10x10 LED Bar Light; Retail Display Shelf Light; Under Cabinet LED Light; Magnetic Mount LED Light; Aluminum Profile LED Light; SMD2835 Rigid Light; Showcase LED Light; Custom Length Shelf Light
产品分组：Armor Lighting
产品型号：HM-MSL-S10-24V-65K80-S-V1

# 产品亮点
产品亮点1：Slim 10x10mm Profile: Compact rigid bar fits under shelves and inside cabinets.
产品亮点2：Magnetic Mount: Built-in magnets support tool-free placement on compatible metal surfaces.
产品亮点3：Uniform Light Output: Rigid bar design supports even merchandise illumination.
产品亮点4：Dual Voltage Options: Available in verified 12V and 24V variants.
产品亮点5：6063 Aluminum Housing: Anodized aluminum supports durable shelf-light construction.

# 产品属性
认证：CE; RoHS
功率：6-12W
发光颜色：White
电压：12V
防护等级：IP44
运输包装：Carton
规格：Customized
商标：Armor Lighting
原产地：China
LED Chip：SMD2835
Profile Size：10x10mm
Housing Material：6063 Anodized Aluminum
Magnet System：30mm, 6 per meter

# 规格管理
规格名称：Voltage
规格值：12V; 24V

# FOB价格设置
价格区间1起订量：100
价格区间1单价：6.80
价格区间2起订量：1000
价格区间2单价：6.50
库存：100000

# 计量单位
计量单位：个

# 发货效率信息
港口：Huangpu

# 样品单交易设置
提供样品：是
样品单价：8.00
样品单位：个
单次最多拿样数量：1
样品描述：10x10mm magnetic shelf light

# FAQ
FAQ问题1：What is the profile size?
FAQ答案1：The verified profile size is 10x10mm.
FAQ问题2：How is the light mounted?
FAQ答案2：Built-in magnets support tool-free placement on compatible metal surfaces.
"""


MIC_AUDIT = """# MIC Audit Report

schema: armor-mic-audit/v1
status: PASS
fact_audit: PASS - every buyer-facing claim maps to a listed source or is omitted.
unknown_behavior: PASS - package dimensions and current edit-page candidates remain explicit unknowns.
bulkfill_audit: PASS - recognized sections only; no product detail or display section; one FOB mode.
ascii_audit: PASS - non-system input values contain ASCII characters only.
ai_writing_audit: ai-writing-audit v0.3.1 applied where editorial style adds value.
approval_status: APPROVED_FOR_SAVE
publication_performed: false
"""


MIC_DETAIL = """# MIC Detail Page Reference

status: READY_FOR_REVIEW
editor: MIC module-based rich text editor; do not paste raw HTML.

## Product signal

The 10x10mm rigid bar is intended for retail shelf and cabinet lighting. Use
only the verified profile, voltage variants, housing, and mounting facts from
the structured product data.

## Image plan

Use supplied product images for the front profile, rear mounting surface, and
an installation context. Do not infer shelf material or claim an installation
scene that is not observable.

## Approval boundary

This reference prepares manual editor content only. No live listing edit or
publication was performed.
"""


def package(include_detail: bool = True) -> dict[str, str]:
    result = {
        "mic-product-data.yaml": MIC_DATA,
        "mic-bulkfill.txt": MIC_BULKFILL,
        "mic-audit.md": MIC_AUDIT,
    }
    if include_detail:
        result["mic-detail-page.md"] = MIC_DETAIL
    return result


class MICPackageTests(unittest.TestCase):
    def test_mic_route_is_lifecycle_neutral(self):
        route = ROUTER.route_request(object_type="work-product", domain="products", artifact="mic-product")
        self.assertEqual(route.path, "02-Projects/Workspaces/Products/MIC-Products/")
        self.assertNotIn("Published", route.path)
        self.assertNotIn("Draft", route.path)

    def test_mic_package_saves_required_files_and_optional_detail(self):
        with tempfile.TemporaryDirectory() as temp:
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                saved = MCP._save_mic_product_package({"package_id": "HM-MSL-S10-24V-65K80-S-V1", "files": package()})
                target = Path(temp) / saved["relative_path"]
                self.assertEqual({path.name for path in target.iterdir()}, set(package()))
                self.assertTrue(saved["read_back"])
                self.assertEqual(saved["files"], sorted(package()))

    def test_mic_package_is_closed_and_rejects_unsafe_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                with self.assertRaises(MCP.ScopedVaultError):
                    MCP._save_mic_product_package({"package_id": "../escape", "files": package()})
                with self.assertRaises(MCP.ScopedVaultError):
                    MCP._save_mic_product_package({"package_id": "fixture", "files": {**package(), "extra.md": "x"}})
                with self.assertRaises(MCP.ScopedVaultError):
                    MCP._save_mic_product_package({"package_id": "fixture", "files": {**package(), "destination": "03-Records/Published"}})
                bad_bulkfill = {**package(), "mic-bulkfill.txt": MIC_BULKFILL + "\n# 产品详情\n"}
                with self.assertRaises(MCP.ScopedVaultError):
                    MCP._save_mic_product_package({"package_id": "manual-only", "files": bad_bulkfill})

    def test_mic_package_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            destination = Path(temp) / "02-Projects/Workspaces/Products/MIC-Products"
            destination.mkdir(parents=True)
            (destination / "escape").symlink_to(outside, target_is_directory=True)
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                with self.assertRaises(MCP.ScopedVaultError):
                    MCP._save_mic_product_package({"package_id": "escape", "files": package()})

    def test_fact_boundary_fixture_keeps_unknowns_out_of_buyer_copy(self):
        self.assertIn("class: UNKNOWN", MIC_DATA)
        self.assertIn("unknown_behavior: PASS", MIC_AUDIT)
        self.assertNotIn("UNKNOWN", MIC_BULKFILL)
        self.assertNotIn("[TO CONFIRM]", MIC_BULKFILL)
        self.assertIn("publication_performed: false", MIC_AUDIT)

    def test_mcp_lists_mic_tool_and_reads_back(self):
        with tempfile.TemporaryDirectory() as temp:
            environment = dict(os.environ)
            environment["ARMOR_VAULT_ROOT"] = temp
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "route_work_product", "arguments": {"domain": "products", "artifact": "mic-product"}}},
                {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "save_mic_product_package", "arguments": {"package_id": "fixture", "files": package(include_detail=False)}}},
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
            self.assertEqual(names, {"route_work_product", "save_article_package", "save_social_package", "save_mic_product_package", "save_website_product_materials_package"})
            route = json.loads(replies[2]["result"]["content"][0]["text"])
            saved = json.loads(replies[3]["result"]["content"][0]["text"])
            self.assertEqual(route["relative_path"], "02-Projects/Workspaces/Products/MIC-Products/")
            self.assertTrue(saved["read_back"])
            self.assertFalse(replies[3]["result"]["isError"])
            self.assertFalse((Path(temp) / "03-Records/Published").exists())


if __name__ == "__main__":
    unittest.main()
