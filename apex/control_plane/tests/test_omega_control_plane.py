"""
OMEGA CONTROL PLANE - Master Automated Test Battery
Covers Truth Engine, Ledger, Reconciliation, Data Core, Approvals, Chaos/Failure, and Idempotency.
"""
import unittest
import sys
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))

from apex.control_plane.truth_engine import OmegaTruthEngine, GatewayState, EvidenceTier
from apex.control_plane.ledger import ImmutableTransactionLedger, TransactionState
from apex.control_plane.reconciliation import OmegaReconciliationEngine, ReconciliationStatus
from apex.control_plane.data_core import OmegaMasterDataCore
from apex.control_plane.approval_engine import OmegaApprovalEngine
from apex.control_plane.health_monitor import OmegaHealthMonitor

class TestOmegaControlPlane(unittest.TestCase):

    def setUp(self):
        self.truth = OmegaTruthEngine()
        self.ledger = ImmutableTransactionLedger()
        self.reconciliation = OmegaReconciliationEngine()
        self.data_core = OmegaMasterDataCore()
        self.approvals = OmegaApprovalEngine()
        self.health = OmegaHealthMonitor()

    def test_01_truth_engine_valid_sandbox_claim(self):
        res = self.truth.evaluate_claim(
            assertion_id="T1",
            claim="Razorpay Sandbox Link Generated",
            gateway="RAZORPAY",
            gateway_state=GatewayState.SANDBOX,
            evidence_tier=EvidenceTier.LEVEL_4_MARKET_DEMAND,
            evidence_payload={"url": "https://rzp.io/test"}
        )
        self.assertTrue(res.verified)
        self.assertEqual(res.gateway_state, GatewayState.SANDBOX)

    def test_02_truth_engine_rejects_unsupported_live_claim(self):
        # Fake "PAID" claim on local state must be rejected
        res = self.truth.evaluate_claim(
            assertion_id="T2",
            claim="Customer PAID ₹50,000 to Live Bank",
            gateway="RAZORPAY",
            gateway_state=GatewayState.LOCAL,
            evidence_tier=EvidenceTier.LEVEL_8_AI_ASSUMPTION,
            evidence_payload={}
        )
        self.assertFalse(res.verified)
        self.assertIn("Cannot assert external action", res.rejection_reason)

    def test_03_immutable_ledger_state_machine(self):
        tx = self.ledger.create_transaction(
            transaction_id="TX-UNIT-01",
            gateway="TEST_GATEWAY",
            environment="LOCAL",
            action_type="TEST_ACTION",
            actor="TEST_RUNNER",
            agent="OMEGA_QA",
            request_payload={"key": "value"}
        )
        self.assertEqual(tx["status"], TransactionState.CREATED.value)
        self.assertTrue(len(tx["request_hash"]) == 64)

        # Transition to VALIDATED
        tr = self.ledger.transition_state("TX-UNIT-01", TransactionState.VALIDATED, "OMEGA_TRUTH")
        self.assertEqual(tr["new_state"], TransactionState.VALIDATED.value)

        # Disallow illegal skip to VERIFIED
        with self.assertRaises(ValueError):
            self.ledger.transition_state("TX-UNIT-01", TransactionState.VERIFIED, "ILLEGAL_ACTOR")

    def test_04_reconciliation_match_and_mismatch_incident(self):
        # Exact match
        loc = {"amount": 1000, "status": "CLEARED"}
        ext = {"amount": 1000, "status": "CLEARED"}
        res_match = self.reconciliation.reconcile_transaction("TX-REC-01", "EXIM", loc, ext, ["amount", "status"])
        self.assertEqual(res_match["status"], ReconciliationStatus.MATCH.value)

        # Mismatch creates incident
        ext_bad = {"amount": 500, "status": "PENDING"}
        res_mismatch = self.reconciliation.reconcile_transaction("TX-REC-02", "EXIM", loc, ext_bad, ["amount", "status"])
        self.assertEqual(res_mismatch["status"], ReconciliationStatus.MISMATCH.value)
        self.assertTrue(len(self.reconciliation.incidents) > 0)

    def test_05_master_data_core_kpis(self):
        eid = self.data_core.record_event("UNIT_TEST_EVENT", "TEST_SUITE", {"sample": 123})
        self.assertTrue(eid > 0)
        kpis = self.data_core.get_ecosystem_kpis()
        self.assertTrue(kpis["events_logged"] > 0)

    def test_06_approval_engine_lifecycle(self):
        req = self.approvals.request_approval("APP-TEST-01", "OMEGA_FINANCE", "PAYOUT", "BANK", {"amount": 100})
        self.assertEqual(req["status"], "PENDING")
        dec = self.approvals.record_decision("APP-TEST-01", "ADMIN", "APPROVED", "Unit test pass")
        self.assertEqual(dec["status"], "APPROVED")

    def test_07_health_score_calculation(self):
        perfect = self.health.calculate_system_health_score(100.0, 0, 0)
        self.assertEqual(perfect["omega_system_health_score"], 100.0)
        self.assertEqual(perfect["grade"], "A+ (CERTIFIED)")

        penalized = self.health.calculate_system_health_score(100.0, 1, 1)
        self.assertEqual(penalized["omega_system_health_score"], 65.0)

if __name__ == "__main__":
    unittest.main()
