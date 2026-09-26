import unittest
from pathlib import Path
from REVENUE_OS.database.db import DatabaseManager
from REVENUE_OS.finance.finance_agent import FinanceAgent
from REVENUE_OS.finance.expense_auditor import ExpenseAuditor

class TestFinance(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("e:/anti/REVENUE_OS/database/test_finance.db")
        if self.test_db_path.exists():
            self.test_db_path.unlink()
        self.db = DatabaseManager(db_path=self.test_db_path)
        self.db.initialize()
        
        self.finance = FinanceAgent(db=self.db)
        self.auditor = ExpenseAuditor()

    def tearDown(self):
        self.db.close()
        if self.test_db_path.exists():
            try:
                self.test_db_path.unlink()
            except Exception:
                pass

    def test_pnl_calculation(self):
        pnl = self.finance.calculate_pnl(
            gross_revenue_inr=105000.0, # 3 clients @ ₹35,000
            variable_costs_inr=10500.0, # Data enrichment, compute per client
            fixed_costs_inr=5000.0,     # Domains, core infrastructure
            ai_cost_usd=25.0,           # LLM API calls (~₹2,175)
            founder_hours=12.0          # 12 hours across month
        )
        self.assertEqual(pnl["gross_revenue_inr"], 105000.0)
        self.assertEqual(pnl["total_costs_inr"], 15500.0)
        self.assertEqual(pnl["contribution_profit_inr"], 89500.0)
        self.assertAlmostEqual(pnl["gross_margin_pct"], 90.0, delta=0.5)
        self.assertAlmostEqual(pnl["net_margin_pct"], 85.2, delta=0.5)
        
        # Founder leverage: ₹89,500 / 12 hrs = ~₹7,458/hr
        self.assertGreater(pnl["revenue_per_founder_hour_inr"], 7000.0)
        
        # AI leverage: Gross profit created / AI cost in INR
        self.assertGreater(pnl["revenue_per_ai_dollar_ratio"], 35.0)

    def test_expense_auditor_flags_underutilized_tools(self):
        subscriptions = [
            {
                "tool_name": "Antigravity Cloud Runner",
                "cost_usd": 20.0,
                "monthly_usage_hours": 120,
                "renewal_date": "2026-10-01",
                "essential": True
            },
            {
                "tool_name": "Unused Legacy CRM Sandbox",
                "cost_usd": 65.0,
                "monthly_usage_hours": 0,
                "renewal_date": "2026-09-28",
                "essential": False
            }
        ]
        audit = self.auditor.audit_subscriptions(subscriptions)
        self.assertEqual(len(audit["cancellation_recommendations"]), 1)
        self.assertEqual(audit["cancellation_recommendations"][0]["tool_name"], "Unused Legacy CRM Sandbox")
        self.assertGreater(audit["total_potential_savings_usd"], 0)

if __name__ == "__main__":
    unittest.main()
