"""
End-to-End Integration Test for REVENUE OS
Adheres strictly to Directives 4, 151, 165, 171.
Verifies the complete 24/7 operating loop:
DISCOVER -> VERIFY -> SCORE -> PRIORITIZE -> CREATE OFFER ->
CAPTURE LEADS -> QUALIFY -> PIPELINE -> FOUNDER APPROVAL -> P&L TELEMETRY
"""

import unittest
from pathlib import Path
from REVENUE_OS.database.db import DatabaseManager
from REVENUE_OS.market.opportunity_engine import OpportunityEngine
from REVENUE_OS.offers.offer_architect import OfferArchitect
from REVENUE_OS.leads.lead_engine import LeadEngine
from REVENUE_OS.crm.crm_pipeline import CRMPipeline
from REVENUE_OS.sales.sales_assistant import SalesAssistant
from REVENUE_OS.founder_os.approval_center import ApprovalCenter
from REVENUE_OS.finance.finance_agent import FinanceAgent
from REVENUE_OS.command_center.cli import RevenueOSCLI

class TestEndToEndSystem(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("e:/anti/REVENUE_OS/database/test_e2e_system.db")
        if self.test_db_path.exists():
            self.test_db_path.unlink()
        self.db = DatabaseManager(db_path=self.test_db_path)
        self.db.initialize()

    def tearDown(self):
        self.db.close()
        if self.test_db_path.exists():
            try:
                self.test_db_path.unlink()
            except Exception:
                pass

    def test_complete_autonomous_revenue_loop(self):
        # 1. DISCOVER & SCORE OPPORTUNITIES
        opp_engine = OpportunityEngine()
        funnel = opp_engine.compress_funnel()
        primary_engine = funnel["primary_engine"]
        self.assertEqual(primary_engine["id"], "OPP-001")
        self.assertGreaterEqual(primary_engine["total_score"], 85.0)

        # 2. ARCHITECT THE OFFER
        architect = OfferArchitect()
        offer = architect.create_offer_for_opportunity(primary_engine)
        self.assertEqual(offer["price_inr"], 35000.0)
        self.assertIn("roi_calculation", offer)

        # 3. DISCOVER & INGEST ETHICAL LEADS
        lead_engine = LeadEngine(db=self.db)
        lead_id = lead_engine.ingest_lead({
            "company": "Cognitive Cloud Tech",
            "industry": "B2B AI Platforms",
            "geography": "Bengaluru, India",
            "contact_name": "Arjun Nair",
            "contact_role": "Co-founder & CRO",
            "contact_email": "arjun@cognitivecloud.example.com",
            "buying_trigger": "Series A announcement, building outbound pipeline",
            "source": "Verified Public Filing",
            "icp_fit_score": 9.5,
            "pain_score": 9.0,
            "trigger_score": 9.5,
            "ability_to_pay_score": 9.0,
            "urgency_score": 8.5,
            "reachability_score": 9.0,
        })
        lead = lead_engine.get_lead(lead_id)
        self.assertEqual(lead["status"], "QUALIFIED")

        # 4. PREPARE PERSONALIZED VALUE-FIRST OUTREACH
        sales = SalesAssistant(db=self.db)
        outreach = sales.draft_personalized_outreach(lead)
        self.assertIn("Arjun", outreach["body"])
        self.assertIn("Cognitive Cloud Tech", outreach["body"])

        # 5. CREATE & ADVANCE DEAL IN 12-STAGE CRM
        crm = CRMPipeline(db=self.db)
        deal_id = crm.create_deal(
            lead_id=lead_id,
            deal_name="Cognitive Cloud Turnkey AI Retainer",
            deal_value_inr=35000.0,
            stage="DISCOVERY"
        )
        crm.advance_stage(deal_id, "PROPOSAL")

        # 6. QUEUE CONSEQUENTIAL ACTION TO FOUNDER APPROVAL CENTER
        approvals = ApprovalCenter(db=self.db)
        req_id = approvals.queue_request(
            requester_agent="SalesAssistant",
            request_type="CONTRACT",
            title="Approve Service Agreement for Cognitive Cloud Tech",
            reason="Discovery completed, client agreed to ₹35k/mo retainer pilot.",
            cost_inr=0.0,
            upside_inr=35000.0,
            risk_level="LOW",
            recommendation="APPROVE - Standard 14-day milestone delivery."
        )
        self.assertEqual(len(approvals.get_pending_cards()), 1)

        # 7. FOUNDER APPROVES
        approvals.approve_request(req_id, notes="Approved by Aditya Mehra")
        self.assertEqual(len(approvals.get_pending_cards()), 0)

        # 8. ADVANCE DEAL TO WON & RECORD FINANCIAL TELEMETRY
        crm.advance_stage(deal_id, "WON")
        finance = FinanceAgent(db=self.db)
        pnl = finance.calculate_pnl(
            gross_revenue_inr=35000.0,
            variable_costs_inr=3500.0,
            fixed_costs_inr=1500.0,
            ai_cost_usd=8.0,
            founder_hours=4.0
        )
        self.assertEqual(pnl["contribution_profit_inr"], 30000.0)
        self.assertAlmostEqual(pnl["gross_margin_pct"], 90.0, delta=0.5)

        # 9. CLI COMMAND CENTER AGGREGATION & EXECUTIVE BRIEF
        cli = RevenueOSCLI(db=self.db)
        state = cli.get_dashboard_state()
        self.assertEqual(state["customers_count"], 2) # minimum active baseline
        brief = cli.get_executive_brief()
        self.assertIn("FINDING", brief)
        self.assertIn("FOUNDER APPROVAL REQUIRED?", brief)

        # 10. VERIFY TAMPER-EVIDENT AUDIT LOGS RECORDED COMPLETE TRAIL
        logs = self.db.get_recent_audit_logs(limit=20)
        action_names = {log["action_name"] for log in logs}
        self.assertIn("ingest_lead", action_names)
        self.assertIn("draft_outreach", action_names)
        self.assertIn("create_deal", action_names)
        self.assertIn("advance_stage", action_names)
        self.assertIn("queue_approval_request", action_names)
        self.assertIn("resolve_approval", action_names)
        self.assertIn("calculate_pnl", action_names)

if __name__ == "__main__":
    unittest.main()
