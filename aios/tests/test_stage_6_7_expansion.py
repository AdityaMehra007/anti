import unittest
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

AIOS_ROOT = Path("E:/anti/aios")
if str(AIOS_ROOT) not in sys.path:
    sys.path.insert(0, str(AIOS_ROOT))
sys.path.insert(0, str(AIOS_ROOT / "ai"))
sys.path.insert(0, str(AIOS_ROOT / "projects"))
sys.path.insert(0, str(AIOS_ROOT / "databases"))

from projects.idea_validator import IdeaValidator
from ai.cloud_adapters import GeminiAdapter, ClaudeAdapter, OpenAIAdapter, SmartRouter
from ai.model_evaluator import ModelEvaluator
from databases.db import get_connection

GATEWAY_BASE_URL = "http://127.0.0.1:8090"


class TestStage6And7Expansion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure database tables exist
        cls.validator = IdeaValidator(gateway_url=GATEWAY_BASE_URL)
        cls.evaluator = ModelEvaluator(gateway_url=GATEWAY_BASE_URL)
        cls.router = SmartRouter()

    def test_01_idea_validator_structure_and_scoring(self):
        idea = self.validator.validate_idea(
            title="Test Automated Invoice Parser",
            problem="Small businesses spend 10 hours monthly keying paper invoices into accounting software.",
            target_user="Bookkeepers and SMB owners",
            proposed_solution="Zero-setup agent that reads scanned PDFs and drafts payments automatically.",
            category="FINTECH_AUTOMATION"
        )
        self.assertIn("id", idea)
        self.assertTrue(idea["id"].startswith("IDEA-"))
        self.assertEqual(idea["title"], "Test Automated Invoice Parser")
        self.assertGreaterEqual(idea["conviction_score"], 10)
        self.assertLessEqual(idea["conviction_score"], 98)
        self.assertIn("status", idea)
        self.assertIn("mvp_scope", idea)
        self.assertIn("ai_insights", idea)

    def test_02_idea_db_persistence_and_retrieval(self):
        title = "Test Logistics Manifest Tracker"
        report = self.validator.validate_idea(
            title=title,
            problem="Customs declarations have 5-day delays due to manual paperwork and missing HS codes.",
            target_user="Freight forwarders and customs brokers",
            proposed_solution="Automated pipeline matching manifests with national tariff registers.",
            category="EXIM_LOGISTICS"
        )
        idea_id = report["id"]
        
        # Verify get_idea
        fetched = self.validator.get_idea(idea_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["title"], title)

        # Verify in list_ideas
        all_ideas = self.validator.list_ideas()
        matching = [i for i in all_ideas if i["id"] == idea_id]
        self.assertEqual(len(matching), 1)

    def test_03_cloud_adapters_simulation(self):
        gemini = GeminiAdapter()
        res_g = gemini.generate("gemini-2.0-flash", [{"role": "user", "content": "Hello"}])
        self.assertEqual(res_g["provider"], "Google")
        self.assertIn("content", res_g)
        self.assertTrue(res_g["simulated"])

        claude = ClaudeAdapter()
        res_c = claude.generate("claude-3-5-sonnet", [{"role": "user", "content": "Hello"}])
        self.assertEqual(res_c["provider"], "Anthropic")
        self.assertIn("content", res_c)
        self.assertTrue(res_c["simulated"])

        openai = OpenAIAdapter()
        res_o = openai.generate("gpt-4o-mini", [{"role": "user", "content": "Hello"}])
        self.assertEqual(res_o["provider"], "OpenAI")
        self.assertIn("content", res_o)
        self.assertTrue(res_o["simulated"])

    def test_04_smart_router_dispatch(self):
        res1 = self.router.route_request("gemini-2.0-flash", [{"role": "user", "content": "Test"}])
        self.assertEqual(res1["provider"], "Google")

        res2 = self.router.route_request("claude-3-5-sonnet", [{"role": "user", "content": "Test"}])
        self.assertEqual(res2["provider"], "Anthropic")

        res3 = self.router.route_request("gpt-4o", [{"role": "user", "content": "Test"}])
        self.assertEqual(res3["provider"], "OpenAI")

    def test_05_model_evaluator_history(self):
        history = self.evaluator.get_eval_history(limit=5)
        self.assertIsInstance(history, list)

    def test_06_gateway_metrics_prometheus(self):
        try:
            req = urllib.request.urlopen(f"{GATEWAY_BASE_URL}/metrics", timeout=5)
            self.assertEqual(req.status, 200)
            content = req.read().decode("utf-8")
            self.assertIn("aios_gateway_up 1", content)
            self.assertIn("aios_knowledge_chunks_total", content)
            self.assertIn("aios_ideas_validated_total", content)
            self.assertIn("aios_saas_projects_total", content)
        except urllib.error.URLError as e:
            self.fail(f"Gateway /metrics unreachable: {e}")

    def test_07_gateway_get_endpoints(self):
        endpoints = ["/v1/ideas", "/v1/saas/projects", "/v1/eval/results"]
        for ep in endpoints:
            try:
                req = urllib.request.urlopen(f"{GATEWAY_BASE_URL}{ep}", timeout=5)
                self.assertEqual(req.status, 200)
                data = json.loads(req.read().decode("utf-8"))
                self.assertIsInstance(data, dict)
            except urllib.error.URLError as e:
                self.fail(f"Gateway endpoint {ep} unreachable: {e}")

    def test_08_gateway_cloud_chat_completion(self):
        try:
            payload = json.dumps({
                "model": "claude-3-5-sonnet",
                "messages": [{"role": "user", "content": "Assess system architecture."}]
            }).encode("utf-8")
            req = urllib.request.Request(
                f"{GATEWAY_BASE_URL}/v1/chat/completions",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode("utf-8"))
                self.assertIn("choices", data)
                self.assertEqual(data["omega_router"]["routed_to"], "cloud_gateway")
                self.assertEqual(data["omega_router"]["provider"], "Anthropic")
        except urllib.error.URLError as e:
            self.fail(f"Gateway cloud completions failed: {e}")


if __name__ == "__main__":
    unittest.main()
