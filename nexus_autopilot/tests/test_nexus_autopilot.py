"""
NEXUS AUTOPILOT - Comprehensive Automated Test Suite
Validates database integrity, command parsing, financial math, agent gates, and webhook reconciliation.
"""
import unittest
import sys
import os
import time
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(WORKSPACE / "nexus_autopilot"))

from core.whatsapp_parser import WhatsAppCommandParser
from core.finance_engine import NexusFinanceEngine
from core.agent_system import NexusAgentSystem
from core.razorpay_gateway import RazorpayGateway

class TestNexusAutopilot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = WhatsAppCommandParser()
        cls.finance = NexusFinanceEngine()
        cls.agents = NexusAgentSystem()
        cls.razorpay = RazorpayGateway()

    def test_01_whatsapp_command_parsing(self):
        # 1. Quotation parsing
        quote_cmd = "Send Ramesh the quotation for 250 boxes at Rs 420."
        res = self.parser.parse_command(quote_cmd)
        self.assertEqual(res["intent"], "CREATE_QUOTATION")
        self.assertEqual(res["entities"]["quantity"], 250)
        self.assertEqual(res["entities"]["unit_rate"], 420.0)
        self.assertEqual(res["entities"]["total_amount"], 105000.0)

        # 2. Overdue query
        due_cmd = "Who owes me money?"
        res_due = self.parser.parse_command(due_cmd)
        self.assertEqual(res_due["intent"], "GET_RECEIVABLES_REPORT")

    def test_02_finance_engine_kpis(self):
        snap = self.finance.get_executive_financial_snapshot("ORG-ABC-001")
        self.assertTrue(snap["total_revenue_invoiced"] >= 700000.0)
        self.assertTrue(snap["total_overdue_receivables"] >= 300000.0)
        self.assertTrue(snap["cash_forecast_30d"]["base_scenario"] > 0)

    def test_03_receivables_risk_scoring(self):
        debtors = self.finance.get_receivables_risk_report("ORG-ABC-001")
        self.assertTrue(len(debtors) >= 3)
        # Check risk tiering
        critical = [d for d in debtors if d["risk_tier"] == "CRITICAL_RISK"]
        self.assertTrue(len(critical) >= 1)

    def test_04_agent_permission_gates(self):
        # Collections Agent attempting unauthorized fund transfer (Forbidden)
        chk_forbidden = self.agents.evaluate_action_permission("Collections_Agent", "waive_debt", 50000.0)
        self.assertFalse(chk_forbidden["permitted"])
        self.assertEqual(chk_forbidden["approval_level"], 4)

        # Sales Agent creating quote > 50,000 (Requires Owner Level 2 Approval)
        chk_quote = self.agents.evaluate_action_permission("Sales_Agent", "draft_quotes", 120000.0)
        self.assertTrue(chk_quote["permitted"])
        self.assertTrue(chk_quote["approval_required"])
        self.assertEqual(chk_quote["approval_level"], 2)

    def test_05_razorpay_link_and_reconciliation(self):
        # 1. Create Link
        link_res = self.razorpay.create_payment_link(
            "ORG-ABC-001", "INV-1002", "CUST-002", "Kumar Enterprises", "+919845023456", 120000.0, "Packaging"
        )
        self.assertEqual(link_res["status"], "CREATED_AND_LINKED")
        self.assertTrue("https://rzp.io" in link_res["payment_url"])

        # 2. Process Webhook Payment
        hook_res = self.razorpay.process_webhook_payment(
            "ORG-ABC-001", "INV-1002", "pay_test_kumar_12345", 120000.0
        )
        self.assertEqual(hook_res["invoice_status"], "PAID")
        self.assertEqual(hook_res["reconciliation"], "AUTOMATICALLY_RECONCILED")

if __name__ == "__main__":
    unittest.main()
