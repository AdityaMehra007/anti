"""
Unit tests for PowerBI Vendor SLA Model
"""
import unittest
from build_model import build_and_validate_model


class TestPowerBIModel(unittest.TestCase):
    def test_model_build_and_metrics(self):
        metrics = build_and_validate_model()
        self.assertEqual(metrics["total_records"], 500)
        self.assertEqual(metrics["vendor_count"], 5)
        self.assertGreater(metrics["breach_count"], 0)
        self.assertGreater(metrics["total_penalty_recovery"], 0)
    def test_portfolio_dossier_exists(self):
        import os
        dossier_path = os.path.join(os.path.dirname(__file__), "POWERBI_PORTFOLIO_DOSSIER.md")
        self.assertTrue(os.path.exists(dossier_path))
        with open(dossier_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Fact_Vendor_SLA", content)
        self.assertIn("INR 3,108,800", content)


if __name__ == "__main__":
    unittest.main()
