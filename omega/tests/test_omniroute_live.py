import unittest
import sys
import os

sys.path.insert(0, 'E:/anti')

from omega.model_router.client import OmniRouteClient, ModelResponse, ExecutionMode
from omega.model_router.provider_discovery import live_discovery
from omega.model_router.health_engine import EmpiricalHealthEngine
from omega.model_router.sensitive_guard import SensitiveDataGuard, DataClassification
from omega.model_router.fallback_engine import FallbackEngine
from omega.model_router.provider_catalog import provider_catalog, ProviderCategory
from omega.model_router.response_cache import ModelResponseCache
from omega.model_router.routing_memory import RoutingMemory, RouteMemoryRecord
from omega.model_router.ensembles import MultiModelDebate
from omega.model_router.a2a_engine import A2AEngine
from omega.engines.transaction_ledger import ImmutableTransactionLedger
from omega.core.paths import PRODUCTION_ROOT, SCRATCH_ROOT, is_production_path

class TestOmniRouteP0Hardened(unittest.TestCase):
    def setUp(self):
        self.ledger = ImmutableTransactionLedger()
        self.health = EmpiricalHealthEngine()
        self.cache = ModelResponseCache()
        self.memory = RoutingMemory()

    # TEST 01: Gateway Discovery
    def test_01_gateway_discovery(self):
        report = live_discovery.discover(force_refresh=True)
        self.assertIsNotNone(report)
        self.assertIsInstance(report.gateway_connected, bool)
        self.assertIsInstance(report.local_executable_found, bool)

    # TEST 02: Version Truth (Never invented)
    def test_02_version_truth(self):
        report = live_discovery.discover(force_refresh=True)
        self.assertIsInstance(report.gateway_version, str)
        # If no gateway is active, version MUST be UNKNOWN
        if not report.gateway_connected:
            self.assertEqual(report.gateway_version, "UNKNOWN")

    # TEST 03: Model Discovery (Live vs Template)
    def test_03_model_discovery(self):
        models = provider_catalog.list_all()
        self.assertGreaterEqual(len(models), 5)
        for m in models:
            self.assertIn(m.status, ["DISCOVERED", "ESTIMATED_TEMPLATE", "UNREACHABLE"])
            if m.status == "ESTIMATED_TEMPLATE":
                self.assertFalse(m.verified)

    # TEST 04: Ollama Local Discovery
    def test_04_ollama_discovery(self):
        report = live_discovery.discover(force_refresh=True)
        self.assertIsInstance(report.local_daemon_running, bool)
        self.assertIsInstance(report.local_models, list)

    # TEST 05: Live Generation Mode Distinctions
    def test_05_live_generation_modes(self):
        sim_client = OmniRouteClient(default_mode=ExecutionMode.SIMULATION)
        resp_sim = sim_client.generate("gpt-4o", [{"role": "user", "content": "ping"}])
        self.assertEqual(resp_sim.execution_mode, "SIMULATION")
        self.assertFalse(resp_sim.verified)
        self.assertTrue(resp_sim.success)

    # TEST 06: Structured Output Handling
    def test_06_structured_output(self):
        sim_client = OmniRouteClient(default_mode=ExecutionMode.SIMULATION)
        resp = sim_client.generate("gpt-4o", [{"role": "user", "content": "Return json: {\"ok\": true}"}])
        self.assertIsNotNone(resp.content)
        self.assertGreater(len(resp.content), 0)

    # TEST 07: Live Failure Handling
    def test_07_live_failure(self):
        offline_client = OmniRouteClient(base_url="http://localhost:59999/v1", default_mode=ExecutionMode.LIVE, timeout=0.2)
        resp = offline_client.generate("claude-3-7-sonnet-20250219", [{"role": "user", "content": "Test"}])
        self.assertFalse(resp.success)
        self.assertEqual(resp.status, "UNAVAILABLE")

    # TEST 08: THE MOST IMPORTANT TEST - No Fake Success on Live Failure
    def test_08_live_failure_never_becomes_success(self):
        offline_client = OmniRouteClient(base_url="http://localhost:59999/v1", default_mode=ExecutionMode.LIVE, timeout=0.2)
        resp = offline_client.generate("claude-3-7-sonnet-20250219", [{"role": "user", "content": "Important payload"}])
        # Strict assertions
        self.assertFalse(resp.success, "LIVE failure must NEVER return success=True")
        self.assertFalse(resp.verified, "LIVE failure must NEVER return verified=True")
        self.assertEqual(resp.status, "UNAVAILABLE")
        self.assertEqual(resp.execution_mode, "LIVE")
        self.assertEqual(resp.content, "", "Content must be empty on live network failure")
        self.assertIsNotNone(resp.error)
        # Verify no cache entry created
        self.cache.set("claude-3-7-sonnet-20250219", "Important payload", resp)
        cached = self.cache.get("claude-3-7-sonnet-20250219", "Important payload")
        self.assertIsNone(cached, "Failed responses must NEVER be cached")

    # TEST 09: Fallback Execution & Ledger Audit
    def test_09_fallback_execution(self):
        offline_client = OmniRouteClient(base_url="http://localhost:59999/v1", default_mode=ExecutionMode.LIVE, timeout=0.2)
        fb = FallbackEngine(client=offline_client, ledger=self.ledger)
        resp = fb.execute_with_fallback(["primary-model", "secondary-model"], [{"role": "user", "content": "task"}])
        self.assertFalse(resp.success)
        self.assertEqual(resp.status, "UNAVAILABLE")
        self.assertIn("ALL_FALLBACKS_EXHAUSTED", resp.error)
        txs = self.ledger.list_transactions()
        self.assertGreaterEqual(len(txs), 2)

    # TEST 10: Provider Health Telemetry Maturity (UNKNOWN -> PROVISIONAL -> HEALTHY / DEGRADED / DOWN)
    def test_10_health_telemetry_maturity(self):
        health = EmpiricalHealthEngine(min_healthy_samples=3)
        # 1. Zero samples = UNKNOWN
        rec0 = health.get_health("TestProv", "model-test")
        self.assertEqual(rec0.status, "UNKNOWN")
        self.assertEqual(rec0.sample_count, 0)

        # 2. 1 Sample = PROVISIONAL
        health.record_real_call("TestProv", "model-test", True, 200.0)
        rec1 = health.get_health("TestProv", "model-test")
        self.assertEqual(rec1.status, "PROVISIONAL")
        self.assertEqual(rec1.sample_count, 1)

        # 3. 3 Successes = HEALTHY
        health.record_real_call("TestProv", "model-test", True, 210.0)
        health.record_real_call("TestProv", "model-test", True, 190.0)
        rec3 = health.get_health("TestProv", "model-test")
        self.assertEqual(rec3.status, "HEALTHY")
        self.assertEqual(rec3.sample_count, 3)
        self.assertEqual(rec3.success_rate, 1.0)

        # 4. Mixed Failures = DEGRADED
        health.record_real_call("TestProv", "model-test", False, 1000.0, "Err")
        health.record_real_call("TestProv", "model-test", False, 1000.0, "Err")
        rec5 = health.get_health("TestProv", "model-test")
        self.assertEqual(rec5.status, "DEGRADED")

        # 5. All Failures = DOWN
        health_down = EmpiricalHealthEngine()
        health_down.record_real_call("TestProv", "down-model", False, 1500.0, "Timeout")
        rec_down = health_down.get_health("TestProv", "down-model")
        self.assertEqual(rec_down.status, "DOWN")

    # TEST 11: Token Truth & Estimation Flag
    def test_11_token_truth(self):
        sim_client = OmniRouteClient(default_mode=ExecutionMode.SIMULATION)
        resp = sim_client.generate("gpt-4o", [{"role": "user", "content": "Hello world"}])
        self.assertTrue(resp.tokens_estimated)
        self.assertGreater(resp.total_tokens, 0)

    # TEST 12: Cost Truth
    def test_12_cost_truth(self):
        model_spec = provider_catalog.get_model("claude-3-7-sonnet-20250219")
        self.assertIsNotNone(model_spec)
        self.assertIn(model_spec.cost_source, ["CONFIGURED_PRICE", "DISCOVERED_PRICE", "UNKNOWN"])

    # TEST 13: Cache Safety (No simulation in cache)
    def test_13_cache_safety(self):
        sim_client = OmniRouteClient(default_mode=ExecutionMode.SIMULATION)
        resp_sim = sim_client.generate("gpt-4o", [{"role": "user", "content": "Simulation Cache Test"}])
        self.cache.set("gpt-4o", "Simulation Cache Test", resp_sim)
        cached = self.cache.get("gpt-4o", "Simulation Cache Test")
        self.assertIsNone(cached, "Simulation responses must NEVER be cached")

    # TEST 14: Sensitive Data Routing & Local Private Gating
    def test_14_sensitive_routing(self):
        verdict = SensitiveDataGuard.evaluate_payload(
            "Secret credentials and encryption private key",
            explicit_class=DataClassification.SENSITIVE
        )
        if not live_discovery.discover().local_daemon_running:
            self.assertFalse(verdict.allowed)
            self.assertEqual(verdict.target_route, "BLOCKED")

    # TEST 15: Multi-Model Ensemble Degradation
    def test_15_ensemble_degradation(self):
        offline_client = OmniRouteClient(base_url="http://localhost:59999/v1", default_mode=ExecutionMode.LIVE, timeout=0.2)
        debate = MultiModelDebate(client=offline_client)
        result = debate.run_debate("High stakes strategy", mode=ExecutionMode.LIVE)
        self.assertEqual(result.status, "FAILED")
        self.assertFalse(result.verified)

    # TEST 16: A2A Traceability & Governance
    def test_16_a2a_traceability(self):
        a2a = A2AEngine()
        msg = a2a.dispatch(
            sender="OrchestratorAgent",
            recipient="ResearchAgent",
            action="EXECUTE_RESEARCH",
            payload={"query": "Deep learning"},
            mission_id="MSN-001",
            model="gpt-4o"
        )
        self.assertEqual(msg.mission_id, "MSN-001")
        self.assertEqual(msg.model, "gpt-4o")
        self.assertIn("READ", msg.permissions)
        traces = a2a.get_trace_messages(msg.trace_id)
        self.assertEqual(len(traces), 1)

    # TEST 17: Production Path Separation
    def test_17_production_path_separation(self):
        self.assertEqual(os.path.normpath(PRODUCTION_ROOT), os.path.normpath("E:/anti"))
        self.assertTrue(is_production_path("E:/anti/omega/core/orchestrator.py"))
        self.assertFalse(is_production_path("C:/Users/amehr/.gemini/antigravity/scratch/test.py"))

    # TEST 18: Secret Non-Disclosure
    def test_18_secret_non_disclosure(self):
        report = live_discovery.discover(force_refresh=True)
        for key_name, status_dict in report.api_keys_status.items():
            status_val = status_dict["status"]
            self.assertIn(status_val, ["PRESENT", "MISSING"])
            # Ensure no secret strings or partial keys are exposed
            self.assertNotIn("sk-", str(status_dict))
            self.assertNotIn("AIza", str(status_dict))

if __name__ == "__main__":
    unittest.main(verbosity=2)

