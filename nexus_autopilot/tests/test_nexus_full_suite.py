"""
NEXUS AUTOPILOT - Master Full-Suite Automated Test Battery
Validates all 10 core subsystems with fresh idempotent database seeding.
"""
import unittest
import sys
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(WORKSPACE / "nexus_autopilot"))

from data.init_db import init_nexus_database
from data.seed_demo import seed_demo_company
from core.whatsapp_parser import WhatsAppCommandParser
from core.finance_engine import NexusFinanceEngine
from core.agent_system import NexusAgentSystem
from core.razorpay_gateway import RazorpayGateway
from core.vertical_templates import VerticalTemplatesEngine
from core.automation_engine import AutomationEngine
from core.document_engine import DocumentEngine
from core.management_reports import ManagementReportEngine
from core.ca_partner_portal import CAPartnerPortalEngine

class TestNexusFullSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_nexus_database()
        seed_demo_company()
        cls.parser = WhatsAppCommandParser()
        cls.finance = NexusFinanceEngine()
        cls.agents = NexusAgentSystem()
        cls.razorpay = RazorpayGateway()
        cls.verticals = VerticalTemplatesEngine()
        cls.automation = AutomationEngine()
        cls.docs = DocumentEngine()
        cls.reports = ManagementReportEngine()
        cls.ca = CAPartnerPortalEngine()

    def test_01_whatsapp_hinglish_command_parsing(self):
        cmd = "Ramesh ko 250 boxes ka quotation bhejo at Rs 420"
        res = self.parser.parse_command(cmd)
        self.assertEqual(res["intent"], "CREATE_QUOTATION")
        self.assertEqual(res["entities"]["quantity"], 250)
        self.assertEqual(res["entities"]["unit_rate"], 420.0)

    def test_02_finance_ledger_aggregation(self):
        snap = self.finance.get_executive_financial_snapshot("ORG-ABC-001")
        self.assertTrue(snap["total_revenue_invoiced"] >= 700000.0)
        self.assertTrue(snap["current_cash_balance"] > 0)

    def test_03_receivables_risk_tiering(self):
        debtors = self.finance.get_receivables_risk_report("ORG-ABC-001")
        self.assertTrue(len(debtors) >= 3)
        self.assertTrue(any(d["risk_score"] > 70 for d in debtors))

    def test_04_agent_permission_gates(self):
        # Forbidden action check
        chk_forbid = self.agents.evaluate_action_permission("Finance_Agent", "transfer_funds", 100000.0)
        self.assertFalse(chk_forbid["permitted"])
        self.assertEqual(chk_forbid["approval_level"], 4)

    def test_05_razorpay_webhook_reconciliation(self):
        res = self.razorpay.process_webhook_payment("ORG-ABC-001", "INV-1001", "pay_webhook_test_99", 50000.0)
        self.assertEqual(res["reconciliation"], "AUTOMATICALLY_RECONCILED")

    def test_06_vertical_templates(self):
        tmpl = self.verticals.get_template("DISTRIBUTOR")
        self.assertEqual(tmpl["payment_terms_days"], 15)
        self.assertTrue(len(tmpl["core_workflows"]) >= 5)

    def test_07_automation_engine_triggers(self):
        actions = self.automation.evaluate_trigger("INVOICE_OVERDUE", {"days_overdue": 12, "amount": 100000.0})
        self.assertTrue(len(actions) >= 1)
        self.assertEqual(actions[0]["action"], "DRAFT_WHATSAPP_REMINDER")

    def test_08_document_extraction_accuracy(self):
        raw = "TAX INVOICE. Vendor: Shree Balaji Mfg. GSTIN: 29AABCS4567D1Z4. Total: Rs 1,60,000."
        extracted = self.docs.extract_document(raw)
        self.assertEqual(extracted["document_type"], "INVOICE")
        self.assertEqual(extracted["extracted_fields"]["gstin"], "29AABCS4567D1Z4")
        self.assertEqual(extracted["extracted_fields"]["total_amount_inr"], 160000.0)

    def test_09_management_reports_and_cfo_mode(self):
        snap = self.finance.get_executive_financial_snapshot("ORG-ABC-001")
        cfo_rep = self.reports.execute_ceo_cfo_strategic_mode("Think like my CFO", snap)
        self.assertEqual(cfo_rep["mode"], "STRATEGIC_CFO_PERSPECTIVE")
        self.assertTrue("receivables" in cfo_rep["observation"])

    def test_10_ca_partner_portal_and_commissions(self):
        ca_dash = self.ca.get_partner_dashboard("PARTNER-CA-BLR-01")
        self.assertEqual(ca_dash["total_managed_clients"], 3)
        self.assertTrue(ca_dash["monthly_commission_earned_inr"] > 0)

if __name__ == "__main__":
    unittest.main()
