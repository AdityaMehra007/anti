import unittest
from REVENUE_OS.revenue.first_money_engine import FirstMoneyEngine
from REVENUE_OS.revenue.currency_engine import CurrencyEngine
from REVENUE_OS.revenue.revenue_health import RevenueHealthCalculator

class TestRevenueEngine(unittest.TestCase):
    def setUp(self):
        self.money_engine = FirstMoneyEngine()
        self.currency_engine = CurrencyEngine()
        self.health_calc = RevenueHealthCalculator()

    def test_milestone_calculations(self):
        stages = [
            "first_rupee",
            "first_thousand",
            "first_ten_thousand",
            "first_lakh",
            "first_ten_lakh",
            "first_crore_arr",
            "first_global_10k_usd",
            "first_global_100k_usd_arr"
        ]
        for stage in stages:
            plan = self.money_engine.get_stage_plan(stage)
            self.assertIn("target_amount", plan)
            self.assertIn("customers_needed", plan)
            self.assertIn("average_price", plan)
            self.assertIn("leads_required", plan)
            self.assertIn("conversion_rate_pct", plan)
            self.assertIn("gross_margin_pct", plan)
            self.assertIn("effort_description", plan)
            self.assertGreater(plan["customers_needed"], 0)
            self.assertGreater(plan["leads_required"], 0)
            self.assertGreater(plan["gross_margin_pct"], 70.0)

    def test_currency_conversion(self):
        # 100 USD to INR (approx 8700)
        inr_val = self.currency_engine.convert(100.0, from_curr="USD", to_curr="INR")
        self.assertAlmostEqual(inr_val, 8700.0, delta=100.0)
        
        # Cross conversion: USD to EUR
        eur_val = self.currency_engine.convert(100.0, from_curr="USD", to_curr="EUR")
        self.assertGreater(eur_val, 80.0)
        self.assertLess(eur_val, 110.0)

    def test_revenue_health_score(self):
        health = self.health_calc.calculate_health_score(
            monthly_growth_rate_pct=15.0,
            gross_margin_pct=88.0,
            retention_rate_pct=95.0,
            pipeline_coverage_ratio=3.5,
            top_customer_revenue_pct=20.0,
            cac_payback_months=1.5,
            runway_months=12.0
        )
        self.assertGreaterEqual(health["total_score"], 0.0)
        self.assertLessEqual(health["total_score"], 100.0)
        self.assertEqual(health["rating"], "EXCELLENT")

if __name__ == "__main__":
    unittest.main()
