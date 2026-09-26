import unittest
import sqlite3
import os
from pathlib import Path
from REVENUE_OS.database.db import DatabaseManager

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("e:/anti/REVENUE_OS/database/test_revenue_os.db")
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

    def test_tables_created(self):
        with self.db.get_cursor() as cur:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cur.fetchall()}
            expected_tables = {
                "revenue_metrics",
                "opportunities",
                "leads",
                "deals",
                "offers",
                "approval_requests",
                "audit_logs",
                "experiments",
                "automations",
            }
            for table in expected_tables:
                self.assertIn(table, tables, f"Table {table} not created.")

    def test_audit_log_insertion(self):
        log_id = self.db.log_audit(
            agent_name="RevenueCommander",
            action_tier="RECOMMEND",
            action_name="prioritize_pipeline",
            details={"priority": "high", "impact": "immediate"},
        )
        self.assertGreater(log_id, 0)
        logs = self.db.get_recent_audit_logs(limit=5)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["agent_name"], "RevenueCommander")

    def test_approval_request_lifecycle(self):
        req_id = self.db.create_approval_request(
            requester_agent="SalesAssistant",
            request_type="HIGH_VALUE_OUTREACH",
            title="Approve enterprise proposal for AcquiredTech",
            reason="High contract value ₹1,50,000 requiring formal founder signoff",
            cost_inr=0.0,
            upside_inr=150000.0,
            risk_level="MEDIUM",
            recommendation="APPROVE - ICP fit is 95/100",
        )
        self.assertGreater(req_id, 0)
        pending = self.db.get_pending_approvals()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["id"], req_id)

        # Approve it
        self.db.resolve_approval(req_id, decision="APPROVED", notes="Founder approved via dashboard")
        pending_after = self.db.get_pending_approvals()
        self.assertEqual(len(pending_after), 0)

if __name__ == "__main__":
    unittest.main()
