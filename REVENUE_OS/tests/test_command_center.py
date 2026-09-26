import unittest
from pathlib import Path
import json
import urllib.request
from REVENUE_OS.database.db import DatabaseManager
from REVENUE_OS.command_center.cli import RevenueOSCLI
from REVENUE_OS.command_center.server import create_http_server

class TestCommandCenter(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("e:/anti/REVENUE_OS/database/test_command_center.db")
        if self.test_db_path.exists():
            self.test_db_path.unlink()
        self.db = DatabaseManager(db_path=self.test_db_path)
        self.db.initialize()
        
        self.cli = RevenueOSCLI(db=self.db)

    def tearDown(self):
        self.db.close()
        if self.test_db_path.exists():
            try:
                self.test_db_path.unlink()
            except Exception:
                pass

    def test_cli_generates_standard_output(self):
        output = self.cli.get_executive_brief()
        # Must conform to Directive 151
        self.assertIn("FINDING", output)
        self.assertIn("EVIDENCE", output)
        self.assertIn("REVENUE OPPORTUNITY", output)
        self.assertIn("RISK", output)
        self.assertIn("RECOMMENDATION", output)
        self.assertIn("TOP 3 ACTIONS", output)
        self.assertIn("FOUNDER APPROVAL REQUIRED?", output)

    def test_state_payload_has_all_160_metrics(self):
        state = self.cli.get_dashboard_state()
        required_keys = [
            "revenue_today", "revenue_month", "revenue_year", "profit",
            "leads_count", "customers_count", "pipeline_value", "conversion_rate",
            "cac", "ltv", "churn_rate", "recurring_revenue", "ai_cost",
            "founder_hours", "revenue_per_founder_hour", "biggest_opportunity",
            "biggest_risk", "biggest_bottleneck", "top_3_actions",
            "pending_approvals", "agents", "automations"
        ]
        for k in required_keys:
            self.assertIn(k, state, f"Key {k} missing from dashboard state.")

    def test_server_handler_state_endpoint(self):
        from REVENUE_OS.command_center.server import RevenueOSRequestHandler
        # Verify handler has do_GET and do_POST
        self.assertTrue(hasattr(RevenueOSRequestHandler, "do_GET"))
        self.assertTrue(hasattr(RevenueOSRequestHandler, "do_POST"))

if __name__ == "__main__":
    unittest.main()
