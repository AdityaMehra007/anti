"""
OMNIVERSE Flagship Platform - Comprehensive Automated Test Suite
"""
import unittest
import sys
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))

from apex.projects.omniverse.core.engine import OmniverseCoreEngine
from apex.kernel.runtime import ApexExecutionKernel
from apex.fabric.dynamic_loader import ApexDynamicSpecialistLoader

class TestOmniverseFlagship(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = OmniverseCoreEngine()
        cls.kernel = ApexExecutionKernel()
        cls.loader = ApexDynamicSpecialistLoader()

    def test_01_core_engine_kpis(self):
        kpis = self.engine.generate_enterprise_kpis()
        self.assertTrue(len(kpis) >= 5)
        self.assertEqual(kpis[0].status, "OPTIMAL")

    def test_02_financial_forecast_dcf(self):
        forecast = self.engine.simulate_financial_forecast(initial_capital=1000000.0, months=12)
        self.assertEqual(forecast["horizon_months"], 12)
        self.assertTrue(forecast["projected_annual_revenue"] > 1000000.0)
        self.assertTrue(len(forecast["monthly_trajectory"]) == 12)

    def test_03_database_transactions(self):
        res = self.engine.record_transaction("TX-OMNI-9999", "FINTECH", 50000.0, 0.12)
        self.assertEqual(res["status"], "APPROVED_AND_SETTLED")
        stats = self.engine.get_database_stats()
        self.assertTrue(stats["total_transactions"] >= 1)

    def test_04_dynamic_specialist_integration(self):
        specs = self.loader.search_specialists("Fintech", limit=1)
        self.assertTrue(len(specs) >= 1)
        agent = self.loader.instantiate_specialist(specs[0]["agent_id"])
        self.assertIsNotNone(agent)

    def test_05_kernel_mission_dispatch(self):
        res = self.kernel.run_goal_mission("Omniverse Enterprise Pipeline Verification", project_id="omniverse_test")
        self.assertEqual(res["status"], "MISSION_ACCOMPLISHED")
        self.assertEqual(res["verification"]["verification_state"], "FULLY_VERIFIED")

    def test_06_frontend_assets_integrity(self):
        frontend_dir = WORKSPACE / "apex" / "projects" / "omniverse" / "frontend"
        index_file = frontend_dir / "index.html"
        style_file = frontend_dir / "style.css"
        app_file = frontend_dir / "app.js"
        
        self.assertTrue(index_file.exists() and index_file.stat().st_size > 100)
        self.assertTrue(style_file.exists() and style_file.stat().st_size > 100)
        self.assertTrue(app_file.exists() and app_file.stat().st_size > 100)

if __name__ == "__main__":
    unittest.main()
