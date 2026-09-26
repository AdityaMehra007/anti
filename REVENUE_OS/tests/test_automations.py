import unittest
from pathlib import Path
from REVENUE_OS.database.db import DatabaseManager
from REVENUE_OS.automations.automations import AutomationEngine
from REVENUE_OS.automations.scheduler import TaskScheduler

class TestAutomations(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("e:/anti/REVENUE_OS/database/test_automations.db")
        if self.test_db_path.exists():
            self.test_db_path.unlink()
        self.db = DatabaseManager(db_path=self.test_db_path)
        self.db.initialize()
        
        self.engine = AutomationEngine(db=self.db)
        self.scheduler = TaskScheduler(engine=self.engine)

    def tearDown(self):
        self.db.close()
        if self.test_db_path.exists():
            try:
                self.test_db_path.unlink()
            except Exception:
                pass

    def test_all_10_automations_exist(self):
        routines = self.engine.list_automations()
        expected = [
            "daily_market_scan",
            "lead_discovery",
            "lead_scoring",
            "competitor_monitoring",
            "weekly_revenue_report",
            "failed_payment_alert",
            "customer_follow_up",
            "opportunity_alert",
            "expense_audit",
            "content_research"
        ]
        self.assertEqual(len(routines), 10)
        for r in expected:
            self.assertIn(r, routines, f"Automation {r} missing.")

    def test_execute_automation_pipeline(self):
        # Run daily market scan
        res = self.engine.run_automation("daily_market_scan")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("market_signals_analyzed", res["output"])

        # Run lead discovery
        res_lead = self.engine.run_automation("lead_discovery")
        self.assertEqual(res_lead["status"], "SUCCESS")
        self.assertGreater(res_lead["output"]["leads_discovered"], 0)

        # Run expense audit
        res_exp = self.engine.run_automation("expense_audit")
        self.assertEqual(res_exp["status"], "SUCCESS")

    def test_scheduler_registry(self):
        jobs = self.scheduler.get_scheduled_jobs()
        self.assertGreaterEqual(len(jobs), 5)
        frequencies = {j["frequency"] for j in jobs}
        self.assertIn("DAILY", frequencies)
        self.assertIn("WEEKLY", frequencies)

if __name__ == "__main__":
    unittest.main()
