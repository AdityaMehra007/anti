"""
NEXUS-EXIM - Automated Test Battery
Validates customs duty math, BCD/SWS/IGST arithmetic, and demurrage mitigation logic.
"""
import unittest
import sys
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))

from apex.projects.nexus_exim.data.init_db import init_exim_db
from apex.projects.nexus_exim.core.customs_engine import NexusEximCustomsEngine

class TestNexusExim(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_exim_db()
        cls.engine = NexusEximCustomsEngine()

    def test_01_landed_cost_fob_math(self):
        res = self.engine.calculate_customs_landed_cost(
            invoice_value_usd=100000.0,
            exchange_rate_inr=80.0,
            incoterm="FOB",
            freight_usd=3000.0,
            insurance_usd=1000.0,
            bcd_rate_pct=40.0,
            igst_rate_pct=18.0
        )
        self.assertEqual(res["assessable_value_inr"], 8320000.0)
        self.assertEqual(res["bcd_amount_inr"], 3328000.0)
        self.assertEqual(res["sws_amount_inr"], 332800.0)
        self.assertEqual(res["igst_amount_inr"], 2156544.0)
        self.assertEqual(res["total_customs_duty_inr"], 5817344.0)
        self.assertEqual(res["total_landed_cost_inr"], 14137344.0)

    def test_02_demurrage_mitigation_math(self):
        dem = self.engine.evaluate_demurrage_risk(free_days_allowed=14, days_at_port=18, penalty_per_day_inr=25000.0)
        self.assertEqual(dem["demurrage_overdue_days"], 4)
        self.assertEqual(dem["accrued_demurrage_loss_inr"], 100000.0)
        self.assertEqual(dem["ai_mitigated_savings_inr"], 85000.0)
        self.assertEqual(dem["recommended_action"], "EXPEDITE_AEO_CLEARANCE")

if __name__ == "__main__":
    unittest.main()
