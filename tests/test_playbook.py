import json
import socket
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from playbook.core import (
    AgentPortal,
    CodebaseIndex,
    DeviceMemoryTracker,
    LogConverter,
    MockSmnClient,
    OidcProviderService,
    ProductCatalog,
    SmnAlertPlugin,
    SmnConfig,
    TcpScanner,
    User,
    calculate_category_inventory,
    calculate_roi,
    diagnose_maturity,
    group_users_by_age,
)
from playbook.server import make_server
from playbook.codearts import get_case, load_matrix, verify_case

ROOT = Path(__file__).resolve().parents[1]


class CoreCasesTest(unittest.TestCase):
    def test_grouping_filters_invalid_users(self):
        grouped = group_users_by_age([User("A", 28), None, User("B", -1), User("C", 28)])
        self.assertEqual(["A", "C"], [user.name for user in grouped[28]])
        self.assertNotIn(-1, grouped)
        self.assertEqual({}, group_users_by_age(None))

    def test_inventory_refactor_preserves_behavior(self):
        self.assertEqual(10, calculate_category_inventory({"p1": 10, "p2": None}, {"p1": "book", "p2": "book"}, "book"))
        self.assertEqual(0, calculate_category_inventory(None, {}, "book"))

    def test_product_catalog_crud_and_atomic_stock(self):
        catalog = ProductCatalog()
        created = catalog.create({"name": "测试商品", "price": 10, "stock": 2})
        self.assertEqual("测试商品", catalog.get(created["id"])["name"])
        order = catalog.reserve([{"productId": created["id"], "quantity": 2}])
        self.assertEqual(20.0, order["total"])
        with self.assertRaises(ValueError):
            catalog.reserve([{"productId": created["id"], "quantity": 1}])
        self.assertTrue(catalog.delete(created["id"]))

    def test_codebase_index_never_invents_missing_symbols(self):
        index = CodebaseIndex([ROOT / "java"])
        self.assertGreater(index.build(), 5)
        answer = index.answer("解释 ProductController 和 NotARealClass")
        self.assertIn("ProductController", answer["matchedSymbols"])
        self.assertNotIn("NotARealClass", answer["matchedSymbols"])

    def test_log_converter_isolates_bad_lines(self):
        converter = LogConverter()
        result = converter.convert_lines(["100|work|X|1|2|50", "bad|row"])
        self.assertEqual(1, len(result["traceEvents"]))
        self.assertEqual(1, result["metadata"]["skippedLines"])
        self.assertEqual(50, result["traceEvents"][0]["dur"])

    def test_smn_plugin_reuses_client_for_test_and_alert(self):
        client = MockSmnClient()
        plugin = SmnAlertPlugin(SmnConfig("https://smn.demo.local", "p", "urn:smn:region:p:t"), client)
        self.assertEqual("TEST_SEND", plugin.send("test", "body", test=True)["mode"])
        self.assertEqual("ALERT", plugin.send("alert", "body")["mode"])
        self.assertEqual(2, len(client.messages))
        with self.assertRaises(ValueError):
            SmnConfig("http://unsafe", "p", "urn:smn:r:p:t").validate()

    def test_oidc_trust_boundary_and_exchange(self):
        service = OidcProviderService()
        provider = service.create_provider({"issuer": "https://idp.demo.local", "clientIds": ["client-a"]})
        self.assertEqual(900, service.exchange(provider["id"], "client-a", "demo.token")["expiresIn"])
        with self.assertRaises(PermissionError):
            service.exchange(provider["id"], "client-b", "demo.token")
        with self.assertRaises(ValueError):
            service.create_provider({"issuer": "http://169.254.169.254", "clientIds": ["x"]})

    def test_agent_lifecycle_rejects_illegal_transition(self):
        portal = AgentPortal()
        created = portal.create({"name": "Demo", "tags": ["制造"]})
        published = portal.transition(created["id"], "PUBLISHED")
        self.assertEqual("PUBLISHED", published["state"])
        with self.assertRaises(ValueError):
            portal.transition(created["id"], "DRAFT")

    def test_device_memory_reference_model(self):
        tracker = DeviceMemoryTracker(128, 64)
        tracker.report(1, 32)
        tracker.report(2, 48)
        self.assertEqual(272, tracker.total())
        tracker.process_exit(1)
        self.assertEqual(240, tracker.total())
        self.assertEqual(300, tracker.retry_schedule()["windowSeconds"])

    def test_maturity_and_roi_book_examples(self):
        self.assertEqual("生成膨胀期", diagnose_maturity(.68, .31, .27)["stage"])
        self.assertEqual("规范内耗期", diagnose_maturity(.45, .12, .41)["stage"])
        roi = calculate_roi(345, 278, .71, .29, .19)
        self.assertAlmostEqual(.4083, roi["nec"], places=4)
        self.assertAlmostEqual(-.4933, roi["netRoi"], places=3)

    def test_tcp_scanner_detects_open_and_closed_local_ports(self):
        listener = socket.socket()
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        open_port = listener.getsockname()[1]
        threading.Thread(target=lambda: listener.accept()[0].close(), daemon=True).start()
        probe = socket.socket()
        probe.bind(("127.0.0.1", 0))
        closed_port = probe.getsockname()[1]
        probe.close()
        results = TcpScanner(timeout=.2).scan_many([("127.0.0.1", open_port), ("127.0.0.1", closed_port)])
        listener.close()
        self.assertEqual([True, False], [row.reachable for row in results])


class RepositoryContractTest(unittest.TestCase):
    def test_manifest_has_20_unique_runnable_cases(self):
        cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
        self.assertEqual(20, len(cases))
        self.assertEqual([f"{value:02d}" for value in range(1, 21)], [case["id"] for case in cases])
        for case in cases:
            self.assertTrue(case["entry"].startswith("python3 demo.py case "))
            self.assertIn("PDF", case["source"])

    def test_web_pages_are_self_contained(self):
        expected = ["portal", "meeting-room", "openai-mock", "dashboard", "api-hub", "ecommerce", "agent-portal", "harmony-shop", "metrics", "roi"]
        for name in expected:
            text = (ROOT / "web" / f"{name}.html").read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", text.lower())
            self.assertNotIn('src="http', text)
            self.assertNotIn('href="http', text)
        meeting_room = (ROOT / "web/meeting-room.html").read_text(encoding="utf-8")
        self.assertIn("function toggleSlot", meeting_room)
        self.assertIn("请选择与当前时段相邻的连续时段", meeting_room)

    def test_sdd_evidence_chain_is_complete(self):
        for name in ["log-converter", "smn-alert-plugin", "iam-oidc", "device-memory"]:
            directory = ROOT / ".codeartsdoer/specs" / name
            for document in ["spec.md", "design.md", "tasks.md"]:
                self.assertGreater((directory / document).stat().st_size, 100)
        log_spec = (ROOT / ".codeartsdoer/specs/log-converter/spec.md").read_text(encoding="utf-8")
        self.assertIn("5 条合法事件并跳过 1 条错误记录", log_spec)

    def test_codearts_matrix_covers_all_cases(self):
        cases = load_matrix()
        self.assertEqual([f"{value:02d}" for value in range(1, 21)], [case["id"] for case in cases])
        self.assertEqual({"Spec-Driven"}, {case["mode"] for case in cases if case["id"] in {"13", "14", "15", "17"}})
        for case in cases:
            expected_mode = "Spec-Driven" if case["id"] in {"13", "14", "15", "17"} else "Vibe-Coding"
            self.assertEqual(expected_mode, case["mode"])
            self.assertGreater(len(case["context"]), 1)
            self.assertGreater(len(case["prompt"]), 30)
            self.assertEqual(f"python3 demo.py codearts verify {case['id']}", case["acceptance"])
            for context in case["context"]:
                if context.startswith("#File "):
                    self.assertTrue((ROOT / context.removeprefix("#File ")).exists(), context)

    def test_codearts_project_rules_skill_commands_and_build(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("python3 demo.py codearts verify <ID>", agents)
        skill = ROOT / ".codeartsdoer/skills/codearts-demo-runner/SKILL.md"
        self.assertIn("name: codearts-demo-runner", skill.read_text(encoding="utf-8"))
        status = (ROOT / ".codeartsdoer/skills/ProjectSkillStatus.txt").read_text(encoding="utf-8")
        self.assertEqual("codearts-demo-runner=true", status.strip())
        for name in ["demo-list", "demo-case", "demo-verify"]:
            command = (ROOT / f".codeartsdoer/commands/{name}.md").read_text(encoding="utf-8")
            self.assertTrue(command.startswith("---\n"))
            self.assertIn("description:", command)
        build = (ROOT / ".cloudbuild/build.yml").read_text(encoding="utf-8")
        self.assertIn("version: 2.0", build)
        self.assertIn("python3 demo.py verify --verbose", build)

    def test_codearts_case_lookup_and_http_acceptance(self):
        self.assertEqual("Spec-Driven", get_case("13")["mode"])
        self.assertTrue(verify_case("08"))

    def test_ui_ide_demo_guide_covers_workflow_and_all_cases(self):
        guide = (ROOT / "docs/UI-IDE-DEMO.md").read_text(encoding="utf-8")
        for marker in ["Simple Browser: Show", "#` 上下文", "Vibe-Coding", "Spec-Driven", "套餐已恢复", "预约成功"]:
            self.assertIn(marker, guide)
        for case_id in range(1, 21):
            self.assertIn(f"| {case_id:02d} |", guide)

    def test_ui_ide_screenshot_walkthrough_has_all_98_images(self):
        index = (ROOT / "docs/UI-IDE-CASE-SCREENSHOTS.md").read_text(encoding="utf-8")
        self.assertIn("华为云账号套餐已恢复", index)
        self.assertNotIn("当前华为云账号套餐被冻结", index)
        case_guides = sorted((ROOT / "docs/ui-ide-cases").glob("CASE-*.md"))
        image_root = ROOT / "docs/ui-ide-cases"
        images = sorted(image_root.glob("case-*.jpg"))
        self.assertEqual(20, len(case_guides))
        self.assertEqual(98, len(images))
        for case_id in range(1, 21):
            expected = 6 if case_id in {7, 8, 9, 11, 12, 16, 18, 19, 20} else 4
            case_images = sorted(image_root.glob(f"case-{case_id:02d}-*.jpg"))
            case_guide_path = ROOT / f"docs/ui-ide-cases/CASE-{case_id:02d}.md"
            case_guide = case_guide_path.read_text(encoding="utf-8")
            self.assertEqual(expected, len(case_images), case_id)
            self.assertIn(f"ui-ide-cases/CASE-{case_id:02d}.md", index)
            self.assertIn(f"# 案例 {case_id:02d}", case_guide)
            for marker in [
                "## 项目背景",
                "## 本案例使用的码道能力",
                "| 工作模式 |",
                "| 关键上下文 |",
                "| 智能工程动作 |",
                "| 验证与治理 |",
                "| 客户价值 |",
            ]:
                self.assertIn(marker, case_guide, f"{marker}: case {case_id:02d}")
            for image in case_images:
                self.assertGreater(image.stat().st_size, 50_000, image)
                self.assertIn(f"./{image.name}", case_guide)


class HttpDemoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server("127.0.0.1", 0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path, method="GET", payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        request = Request(self.base + path, data=data, method=method, headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=3) as response:
            return response.status, response.headers, json.loads(response.read().decode())

    def test_portal_health_and_products(self):
        with urlopen(self.base + "/", timeout=3) as response:
            self.assertIn("20 个可运行案例", response.read().decode())
        status, _, health = self.request("/api/health")
        self.assertEqual((200, 20), (status, health["examples"]))
        status, _, created = self.request("/api/products", "POST", {"name": "新增商品", "price": 12.5, "stock": 3})
        self.assertEqual((201, "新增商品"), (status, created["data"]["name"]))

    def test_openai_tool_call_two_step_and_cors(self):
        tools = [{"type": "function", "function": {"name": "get_weather"}}]
        _, headers, first = self.request("/v1/chat/completions", "POST", {"messages": [{"role": "user", "content": "weather"}], "tools": tools})
        self.assertEqual("*", headers["Access-Control-Allow-Origin"])
        self.assertEqual("tool_calls", first["choices"][0]["finish_reason"])
        call = first["choices"][0]["message"]["tool_calls"][0]
        messages = [{"role": "user", "content": "weather"}, first["choices"][0]["message"], {"role": "tool", "tool_call_id": call["id"], "content": "sunny"}]
        _, _, second = self.request("/v1/chat/completions", "POST", {"messages": messages, "tools": tools})
        self.assertEqual("stop", second["choices"][0]["finish_reason"])

    def test_oidc_http_contract(self):
        _, _, created = self.request("/api/oidc/providers", "POST", {"issuer": "https://idp.demo.local", "clientIds": ["client-http"]})
        provider_id = created["data"]["id"]
        _, _, exchanged = self.request(f"/api/oidc/providers/{provider_id}/exchange", "POST", {"clientId": "client-http", "subjectToken": "demo.subject"})
        self.assertEqual(900, exchanged["data"]["expiresIn"])

    def test_metrics_and_roi_http(self):
        _, _, metric = self.request("/api/metrics/diagnose", "POST", {"generationRate": .68, "reworkRate": .31, "violationRate": .27})
        self.assertEqual("生成膨胀期", metric["data"]["stage"])
        _, _, roi = self.request("/api/roi/calculate", "POST", {"grossBenefit": 345, "totalCost": 278, "generationRate": .71, "reworkRate": .29, "violationRate": .19})
        self.assertLess(roi["data"]["netRoi"], 0)


if __name__ == "__main__":
    unittest.main()
