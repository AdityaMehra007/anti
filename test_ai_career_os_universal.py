import unittest
import os
import sqlite3
from pathlib import Path

from ai_career_os_universal_engine import (
    CompetitorIntelligenceEngine,
    PaidSubscriptionsAuditEngine,
    FeatureMatrixEngine,
    TruthLayerEngine,
    AntiGhostingEngine,
    OfferDefenseEngine,
    CareerCompoundingEngine,
    CommandCenterBuilder,
    DB_PATH
)

class TestAICareerOSUniversal(unittest.TestCase):

    def test_database_exists(self):
        self.assertTrue(os.path.exists(DB_PATH), "Database file must exist")

    def test_competitor_census(self):
        summary = CompetitorIntelligenceEngine.get_summary()
        self.assertGreaterEqual(summary["total_competitors"], 50, "Must have at least 50 competitors")
        self.assertEqual(summary["total_categories"], 15, "Must cover all 15 categories A through O")
        
        # Test filtering by category
        cat_a = CompetitorIntelligenceEngine.list_competitors("A")
        self.assertGreater(len(cat_a), 0, "Category A must have platforms")
        names = [c["name"] for c in cat_a]
        self.assertIn("LinkedIn", names)
        self.assertIn("Indeed", names)

    def test_paid_subscriptions_audit(self):
        audit = PaidSubscriptionsAuditEngine.audit_all()
        self.assertGreaterEqual(audit["total_plans_audited"], 10)
        self.assertGreater(audit["annual_os_savings_inr"], 50000.0, "Must calculate positive savings")
        self.assertGreater(len(audit["b2c_plans"]), 0)
        self.assertGreater(len(audit["b2b_plans"]), 0)

    def test_feature_matrix(self):
        matrix = FeatureMatrixEngine.get_matrix()
        self.assertGreaterEqual(len(matrix), 10)
        areas = {f["area"] for f in matrix}
        self.assertIn("Job Discovery", areas)
        self.assertIn("Career Profiles", areas)
        self.assertIn("AI-Powered Matching", areas)

    def test_truth_layer_cryptography(self):
        truth = TruthLayerEngine.verify_all_proofs()
        self.assertEqual(truth["total_proofs"], 9, "Must have EXP-001 through EXP-009")
        self.assertIn("100% VALID", truth["cryptographic_integrity"])
        for p in truth["proofs"]:
            self.assertEqual(len(p["sha256_hash"]), 64, f"Hash for {p['proof_id']} must be valid SHA-256")

    def test_anti_ghosting_engine(self):
        ghost = AntiGhostingEngine.audit_pipeline()
        self.assertGreater(ghost["total_tracked_applications"], 0)
        letter = AntiGhostingEngine.generate_follow_up_letter("Test Corp", "Operations Analyst")
        self.assertIn("Aditya Mehra", letter)
        self.assertIn("Test Corp", letter)
        self.assertIn("EXP-001", letter)

    def test_offer_defense_engine(self):
        benchmarks = OfferDefenseEngine.get_benchmarks()
        self.assertGreaterEqual(len(benchmarks), 4)
        letter = OfferDefenseEngine.generate_counter_negotiation_letter(
            "Acme Global", "Operations Specialist", 450000, 600000
        )
        self.assertIn("450,000", letter)
        self.assertIn("600,000", letter)
        self.assertIn("Acme Global", letter)

    def test_career_compounding_engine(self):
        milestones = CareerCompoundingEngine.get_milestones()
        self.assertEqual(len(milestones), 5)
        horizons = [m["horizon"] for m in milestones]
        self.assertIn("DAY_30", horizons)
        self.assertIn("DAY_365", horizons)

    def test_command_center_html_builder(self):
        out_path = CommandCenterBuilder.build_html()
        self.assertTrue(os.path.exists(out_path), "HTML cockpit must be generated")
        self.assertGreater(os.path.getsize(out_path), 5000, "HTML cockpit must not be empty")

if __name__ == "__main__":
    unittest.main()
