"""
NEXUS-EXIM - Extended Document Parser & Discrepancy Test Suite
"""
import unittest
import sys
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))

from apex.projects.nexus_exim.core.document_parser import NexusEximDocumentParser
from nexus_autopilot.core.razorpay_live_client import RazorpayLiveClient

class TestNexusEximLiveExtensions(unittest.TestCase):

    def setUp(self):
        self.parser = NexusEximDocumentParser()
        self.rzp = RazorpayLiveClient()

    def test_01_razorpay_payment_link_generation(self):
        link = self.rzp.create_payment_link("INV-9099", 50000.0, "Test Exporter", "+919876543210")
        self.assertIn("payment_link_id", link)
        self.assertEqual(link["amount_inr"], 50000.0)

    def test_02_shipping_bill_parsing_whitefield_port(self):
        raw = "SHIPPING BILL NO: SB-INWFD6-2026-9012. PORT: INWFD6. HS CODE: 8541.40.11. TOTAL USD: $85,000. QTY: 250 UNITS. TERMS: CIF."
        parsed = self.parser.parse_shipping_bill_text(raw)
        self.assertEqual(parsed["port_code"], "INWFD6")
        self.assertEqual(parsed["port_name"], "ICD Whitefield, Bengaluru")
        self.assertEqual(parsed["hs_code"], "85414011")
        self.assertEqual(parsed["invoice_value_usd"], 85000.0)
        self.assertEqual(parsed["quantity"], 250)

    def test_03_discrepancy_auditor_clean_vs_flagged(self):
        clean_inv = {"quantity": 250, "hs_code": "85414011", "invoice_value_usd": 85000.0, "port_code": "INWFD6"}
        clean_pack = {"quantity": 250, "hs_code": "85414011"}
        clean_audit = self.parser.audit_trade_discrepancies(clean_inv, clean_pack)
        self.assertTrue(clean_audit["is_clean_for_icegate"])
        self.assertEqual(clean_audit["discrepancies_found"], 0)

        # Mismatch quantity
        dirty_pack = {"quantity": 240, "hs_code": "85414011"}
        dirty_audit = self.parser.audit_trade_discrepancies(clean_inv, dirty_pack)
        self.assertFalse(dirty_audit["is_clean_for_icegate"])
        self.assertEqual(dirty_audit["discrepancies_found"], 1)
        self.assertIn("QUANTITY_MISMATCH", dirty_audit["discrepancy_details"][0])

if __name__ == "__main__":
    unittest.main()
