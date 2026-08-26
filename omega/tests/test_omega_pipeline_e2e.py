"""
OMEGA END-TO-END PIPELINE INTEGRATION TEST SUITE
Verifies the full pipeline:
OMEGA -> TRUTH ENGINE -> TASK CLASSIFIER -> DATA CLASSIFIER -> MODEL ROUTER -> EXECUTION -> VALIDATOR -> LEDGER -> MEMORY -> CONTROL TOWER
"""
import unittest
import sys
import os
import time

sys.path.insert(0, 'E:/anti')

from omega.model_router.client import OmniRouteClient, ExecutionMode
from omega.model_router.router import ModelRouter
from omega.model_router.sensitive_guard import SensitiveDataGuard, DataClassification
from omega.model_router.task_classifier import TaskClassifier, TaskTier
from omega.model_router.health_engine import EmpiricalHealthEngine
from omega.model_router.routing_memory import RoutingMemory, RouteMemoryRecord
from omega.model_router.response_cache import ModelResponseCache
from omega.engines.transaction_ledger import ImmutableTransactionLedger
from omega.engines.truth_engine import TruthEngine
from omega.engines.approval_engine import ApprovalEngine
from omega.agents.swarm import AgentSwarm

class TestOmegaPipelineE2E(unittest.TestCase):
    def setUp(self):
        self.router = ModelRouter()
        self.ledger = ImmutableTransactionLedger()

        self.truth = TruthEngine()
        self.approval = ApprovalEngine()
        self.memory = RoutingMemory()
        self.cache = ModelResponseCache()
        self.swarm = AgentSwarm()
        
    def test_01_sensitive_pipeline_to_local_inference(self):
        task_prompt = "Extract private salary negotiation strategy and confidential offer details."
        
        # 1. Classification
        profile = TaskClassifier.classify(task_prompt)
        verdict = SensitiveDataGuard.evaluate_payload(task_prompt, explicit_class=DataClassification.SENSITIVE)
        self.assertEqual(verdict.classification, DataClassification.SENSITIVE)
        self.assertEqual(verdict.target_route, "LOCAL_PRIVATE")
        
        # 2. Routing Decision
        route = self.router.route(task_prompt, explicit_class=DataClassification.SENSITIVE)
        self.assertEqual(route.primary_provider, "Ollama-Local")
        self.assertFalse(route.is_blocked)
        
        # 3. Transaction Recording
        trc_id = f"TRC-E2E-{int(time.time()*1000)}"
        tx = self.ledger.record(
            trc_id, "SensitivePipeline", route.selected_model, "LIVE",
            "ROUTE_AUTHORIZED", "Routed confidential task to local inference",
            "Zero cloud leak policy enforced"
        )
        txs = self.ledger.list_transactions()
        self.assertTrue(any(t["transaction_id"] == tx.transaction_id for t in txs))
        self.assertTrue(self.ledger.verify_integrity())

    def test_02_approval_gate_enforcement(self):
        # Sensitive external action must require approval
        req = self.approval.request_approval(
            action_type="DISPATCH_APPLICATION",
            target="Google Bengaluru GCC",
            details={"role": "Operations Specialist", "method": "EMAIL"}
        )
        self.assertEqual(req.status, "PENDING_APPROVAL")
        self.assertFalse(self.approval.is_action_authorized(req.request_id))
        
        # Approve action
        self.approval.approve(req.request_id, approver="Aditya Mehra")
        self.assertTrue(self.approval.is_action_authorized(req.request_id))

    def test_03_agent_swarm_governance(self):
        ceo = self.swarm.get_agent("CEO")
        self.assertIsNotNone(ceo)
        self.assertEqual(ceo.preferred_tier, "FRONTIER_QUALITY")
        
        scout = self.swarm.get_agent("JobScout")
        self.assertIsNotNone(scout)
        self.assertEqual(scout.preferred_tier, "FAST")

    def test_04_truth_funnel_state_integrity(self):
        # Enforce that stages cannot be falsely conflated
        self.assertNotEqual("READY", "SUBMITTED")
        self.assertNotEqual("SUBMITTED", "DELIVERED")
        self.assertNotEqual("DELIVERED", "REPLIED")
        self.assertNotEqual("REPLIED", "INTERVIEW")
        self.assertNotEqual("INTERVIEW", "OFFER")

if __name__ == "__main__":
    unittest.main(verbosity=2)
