import unittest
from pathlib import Path
from REVENUE_OS.database.db import DatabaseManager
from REVENUE_OS.founder_os.approval_center import ApprovalCenter
from REVENUE_OS.founder_os.cadence_engine import CadenceEngine
from REVENUE_OS.risk.risk_engine import RiskEngine

class TestFounderOS(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("e:/anti/REVENUE_OS/database/test_founder_os.db")
        if self.test_db_path.exists():
            self.test_db_path.unlink()
        self.db = DatabaseManager(db_path=self.test_db_path)
        self.db.initialize()
        
        self.approvals = ApprovalCenter(db=self.db)
        self.cadence = CadenceEngine(db=self.db)
        self.risk = RiskEngine(db=self.db)

    def tearDown(self):
        self.db.close()
        if self.test_db_path.exists():
            try:
                self.test_db_path.unlink()
            except Exception:
                pass

    def test_approval_center_workflow(self):
        req_id = self.approvals.queue_request(
            requester_agent="SalesAssistant",
            request_type="CONTRACT",
            title="Approve Service Agreement for FinTech Client",
            reason="Retainer contract of ₹35,000/mo ready for signing",
            cost_inr=0.0,
            upside_inr=35000.0,
            risk_level="LOW",
            recommendation="APPROVE"
        )
        self.assertGreater(req_id, 0)
        
        cards = self.approvals.get_pending_cards()
        self.assertEqual(len(cards), 1)
        card = cards[0]
        self.assertEqual(card["title"], "Approve Service Agreement for FinTech Client")
        self.assertIn("reason", card)
        self.assertIn("cost_inr", card)
        self.assertIn("upside_inr", card)
        self.assertIn("risk_level", card)
        self.assertIn("recommendation", card)

        # Founder approves
        self.approvals.approve_request(req_id, notes="Approved by Aditya Mehra")
        self.assertEqual(len(self.approvals.get_pending_cards()), 0)

    def test_daily_revenue_brief_format(self):
        brief = self.cadence.generate_daily_brief(
            revenue_yesterday_inr=0.0,
            revenue_month_inr=70000.0,
            pipeline_inr=140000.0,
            best_lead="Apex Dynamics Technologies",
            biggest_risk="Slow outbound lead response cycle",
            highest_roi_opp="B2B AI Sales Pipeline Automation Engine",
            one_thing_to_stop="Manual copy-pasting of prospect data into spreadsheets"
        )
        self.assertIn("revenue_yesterday", brief)
        self.assertIn("revenue_this_month", brief)
        self.assertIn("pipeline", brief)
        self.assertIn("best_lead", brief)
        self.assertIn("biggest_risk", brief)
        self.assertIn("highest_roi_opportunity", brief)
        self.assertIn("top_3_actions", brief)
        self.assertIn("one_thing_to_stop", brief)
        self.assertEqual(len(brief["top_3_actions"]), 3)

    def test_risk_register_and_thesis_destruction(self):
        analysis = self.risk.destruct_thesis(
            engine_name="B2B AI Sales Pipeline Automation",
            hypothesis="Founders will pay ₹35k/mo to replace manual SDR work with verified pipeline."
        )
        self.assertIn("failure_modes", analysis)
        self.assertIn("abandonment_evidence", analysis)
        self.assertIn("mitigation_strategy", analysis)
        self.assertGreater(len(analysis["failure_modes"]), 0)

if __name__ == "__main__":
    unittest.main()
