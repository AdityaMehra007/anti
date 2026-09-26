import unittest
from pathlib import Path
from REVENUE_OS.market.opportunity_engine import OpportunityEngine
from REVENUE_OS.offers.offer_architect import OfferArchitect

class TestOpportunities(unittest.TestCase):
    def setUp(self):
        self.engine = OpportunityEngine()
        self.architect = OfferArchitect()

    def test_200_opportunities_loaded(self):
        opps = self.engine.get_all_opportunities()
        self.assertEqual(len(opps), 200, f"Expected 200 opportunities, got {len(opps)}")

    def test_opportunity_schema_and_scoring(self):
        opp = self.engine.get_all_opportunities()[0]
        # Check required fields
        for field in [
            "id", "name", "category", "target_customer", "core_problem",
            "demand_signal", "willingness_to_pay_score", "suggested_price_inr",
            "acquisition_channel", "competition_level", "delivery_cost_inr",
            "automation_potential_pct", "gross_margin_pct", "recurring_potential_pct",
            "scalability_score", "founder_time_hours_per_week", "legal_risk_level",
            "platform_risk_level", "ai_leverage_score", "time_to_first_money_days",
            "total_score"
        ]:
            self.assertIn(field, opp, f"Missing field: {field}")
            
        self.assertGreaterEqual(opp["total_score"], 0.0)
        self.assertLessEqual(opp["total_score"], 100.0)

    def test_compression_funnel(self):
        funnel = self.engine.compress_funnel()
        self.assertEqual(len(funnel["tier_200"]), 200)
        self.assertEqual(len(funnel["tier_50"]), 50)
        self.assertEqual(len(funnel["tier_20"]), 20)
        self.assertEqual(len(funnel["tier_10"]), 10)
        self.assertEqual(len(funnel["tier_5"]), 5)
        self.assertEqual(len(funnel["tier_3"]), 3)
        self.assertIsNotNone(funnel["primary_engine"])
        self.assertEqual(len(funnel["secondary_experiments"]), 2)
        
        # Verify primary engine is highest scoring and meets criteria
        primary = funnel["primary_engine"]
        self.assertGreaterEqual(primary["total_score"], 85.0)
        self.assertGreaterEqual(primary["gross_margin_pct"], 80.0)
        self.assertLessEqual(primary["time_to_first_money_days"], 14)

    def test_offer_architect_generates_valid_offer(self):
        funnel = self.engine.compress_funnel()
        primary = funnel["primary_engine"]
        offer = self.architect.create_offer_for_opportunity(primary)
        
        self.assertIn("target_customer", offer)
        self.assertIn("promised_outcome", offer)
        self.assertIn("price_inr", offer)
        self.assertIn("roi_calculation", offer)
        self.assertIn("why_us_vs_do_nothing", offer)
        self.assertGreater(offer["gross_margin_pct"], 75.0)

if __name__ == "__main__":
    unittest.main()
