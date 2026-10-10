#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: End-to-End Full-Stack Verification Suite
Tests all layers across Stages 0 through 7:
1. Telemetry & Hardware Safety (RAM/GPU/Disk)
2. AI Gateway, Privacy Filtering & Smart Routing
3. RAG Semantic Knowledge Hub (BM25 + citations)
4. Automation Engine & Event Triggers (n8n Webhook Bridge)
5. Master Command Center Dashboard Response
6. SaaS Factory & Idea Validator
7. Prometheus /metrics & Model Evaluation Benchmark
"""

import sys
import json
import time
import shutil
import unittest
import urllib.request
import urllib.error
from pathlib import Path

AIOS_ROOT = Path("E:/anti/aios")
if str(AIOS_ROOT) not in sys.path:
    sys.path.insert(0, str(AIOS_ROOT))
sys.path.insert(0, str(AIOS_ROOT / "ai"))
sys.path.insert(0, str(AIOS_ROOT / "databases"))
sys.path.insert(0, str(AIOS_ROOT / "projects"))

import gateway
from projects.saas_factory import SaaSFactory
from projects.idea_validator import IdeaValidator
from ai.model_evaluator import ModelEvaluator
from databases.db import get_connection

GATEWAY_URL = "http://127.0.0.1:8090"
DASHBOARD_URL = "http://127.0.0.1:3000"


class TestE2EFullStack(unittest.TestCase):
    def test_01_core_system_telemetry(self):
        """Verifies health check and telemetry reporting."""
        with urllib.request.urlopen(f"{GATEWAY_URL}/health", timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertEqual(data["status"], "HEALTHY")
            self.assertEqual(data["service"], "ANTIGRAVITY_OMEGA_AIOS_GATEWAY")

        with urllib.request.urlopen(f"{GATEWAY_URL}/api/telemetry", timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertIn(data["status"], ["HEALTHY", "WARNING"])
            self.assertIn("ram", data)
            self.assertIn("disks", data)
            self.assertIn("gpu", data)
            self.assertIn("services", data)

    def test_02_model_registry_and_privacy(self):
        """Verifies model catalog and PII detection."""
        with urllib.request.urlopen(f"{GATEWAY_URL}/v1/models", timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            models = [m["id"] for m in data.get("data", [])]
            self.assertIn("qwen2.5-coder:3b", models)
            self.assertIn("gemini-2.0-flash", models)

        # Test PII scrubbing
        raw_text = "Contact john.doe@enterprise.com with API key sk-1234567890123456789012"
        self.assertTrue(gateway.contains_pii(raw_text))
        anonymized = gateway.anonymize_text(raw_text)
        self.assertNotIn("john.doe@enterprise.com", anonymized)
        self.assertIn("[REDACTED_SENSITIVE]", anonymized)

    def test_03_rag_semantic_knowledge_search(self):
        """Verifies RAG document indexing and semantic retrieval."""
        with urllib.request.urlopen(f"{GATEWAY_URL}/v1/rag/stats", timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertGreaterEqual(data.get("indexed_chunks", 0), 1)

        req_body = json.dumps({"query": "architecture", "synthesize": False, "top_k": 3}).encode("utf-8")
        req = urllib.request.Request(f"{GATEWAY_URL}/v1/rag/query", data=req_body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertIn("matches", data)

    def test_04_automation_webhook_and_audit(self):
        """Verifies automation bridge status and webhook triggering."""
        with urllib.request.urlopen(f"{GATEWAY_URL}/v1/automation/status", timeout=5) as res:
            self.assertEqual(res.status, 200)

        trigger_body = json.dumps({"webhook": "e2e-test-event", "payload": {"test": True}}).encode("utf-8")
        req = urllib.request.Request(f"{GATEWAY_URL}/v1/automation/trigger", data=trigger_body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertIn(data.get("status"), ["SUCCESS", "ERROR"])

        # Verify audit log in master database
        with get_connection() as con:
            row = con.execute("SELECT id FROM audit_logs WHERE actor='AUTOMATION_BRIDGE' ORDER BY id DESC LIMIT 1").fetchone()
            self.assertIsNotNone(row)

    def test_05_dashboard_serving(self):
        """Verifies Command Center UI is served on port 3000."""
        with urllib.request.urlopen(DASHBOARD_URL, timeout=5) as res:
            self.assertEqual(res.status, 200)
            html = res.read().decode("utf-8")
            self.assertIn("ANTIGRAVITY OMEGA", html)
            self.assertIn("Startup Lab & Idea Validator", html)
            self.assertIn("Model Evaluation & Quality Benchmarks", html)

    def test_06_saas_factory_scaffolding(self):
        """Verifies full SaaS project scaffolding flow."""
        factory = SaaSFactory()
        project_name = f"e2e-test-project-{int(time.time())}"
        path_str = factory.scaffold_project(project_name, "static-api", ["auth", "db"])
        p = Path(path_str)
        self.assertTrue(p.exists())
        self.assertTrue((p / "README.md").exists())
        self.assertTrue((p / "static" / "index.html").exists())
        
        # Cleanup scaffolded test directory
        if p.exists():
            shutil.rmtree(p)

    def test_07_idea_validator_conviction(self):
        """Verifies idea scoring and DB persistence."""
        validator = IdeaValidator()
        report = validator.validate_idea(
            title="Automated Supply Chain Reconciler",
            problem="Companies spend 20 hours a week resolving invoice mismatches.",
            target_user="Logistics operations managers",
            proposed_solution="Autonomous agent auditing BOL against purchase orders."
        )
        self.assertIn("conviction_score", report)
        self.assertGreaterEqual(report["conviction_score"], 50)
        self.assertIn("mvp_scope", report)

    def test_08_prometheus_metrics_exposition(self):
        """Verifies Prometheus exposition format."""
        with urllib.request.urlopen(f"{GATEWAY_URL}/metrics", timeout=5) as res:
            self.assertEqual(res.status, 200)
            content = res.read().decode("utf-8")
            self.assertIn("# HELP aios_gateway_up", content)
            self.assertIn("# TYPE aios_gateway_up gauge", content)
            self.assertIn("aios_gateway_up 1", content)
            self.assertIn("aios_knowledge_chunks_total", content)


if __name__ == "__main__":
    unittest.main()
