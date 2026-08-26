import os, sys, unittest

sys.path.insert(0, os.path.join(r"e:\anti", "omega", "apps", "nexus_omega"))
from nexus_engine import NexusOmegaEngine

class TestNexusOmega(unittest.TestCase):
    def setUp(self):
        self.engine = NexusOmegaEngine("test_nexus.db")

    def tearDown(self):
        if os.path.exists("test_nexus.db"):
            try: os.remove("test_nexus.db")
            except Exception: pass

    def test_01_create_event_and_ros(self):
        evt_id = self.engine.create_event("Global Aviation Summit", "Aviation & Defense", 3000, 1200000)
        self.assertTrue(evt_id.startswith("EVT-"))

    def test_02_sponsor_matching(self):
        sponsors = self.engine.match_sponsors_from_network()
        self.assertGreaterEqual(len(sponsors), 5)
        self.assertEqual(sponsors[0]["company"], "Tata Communications")

    def test_03_roi_calculator(self):
        roi = self.engine.calculate_event_roi(1000000, 2000000, 500000)
        self.assertEqual(roi["financial_verdict"], "PROFITABLE")
        self.assertEqual(roi["net_profit_inr"], 1500000)

if __name__ == "__main__":
    unittest.main()
