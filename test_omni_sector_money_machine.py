#!/usr/bin/env python3
"""
test_omni_sector_money_machine.py - Verification Suite for Omni-Sector Wealth Machine
"""

import unittest
import json
from pathlib import Path
from omni_sector_money_machine import (
    compute_omni_sector_metrics,
    generate_omni_sector_dashboard,
    TELEMETRY_OUT,
    DASHBOARD_HTML,
    DB_PATH
)

class TestOmniSectorMoneyMachine(unittest.TestCase):

    def test_database_exists(self):
        self.assertTrue(DB_PATH.exists(), f"Database {DB_PATH} must exist.")

    def test_compute_omni_sector_metrics(self):
        telemetry = compute_omni_sector_metrics()
        self.assertIsNotNone(telemetry)
        self.assertIn("macro_metrics", telemetry)
        self.assertIn("sectors", telemetry)
        self.assertIn("top_pipeline_accounts", telemetry)
        
        # Verify 6 sectors are populated
        self.assertEqual(len(telemetry["sectors"]), 6)
        
        # Verify mathematical consistency
        m = telemetry["macro_metrics"]
        self.assertGreater(m["total_active_pipeline_usd"], 0)
        self.assertGreater(m["total_expected_value_usd"], 0)
        self.assertGreater(m["daily_pipeline_velocity_usd"], 0)
        self.assertEqual(m["total_outbound_leads"], 192)
        
        # Verify JSON file persistence
        self.assertTrue(TELEMETRY_OUT.exists())
        with open(TELEMETRY_OUT, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            self.assertEqual(data["founder"], "Aditya Mehra")

    def test_generate_omni_sector_dashboard(self):
        telemetry = compute_omni_sector_metrics()
        dash_path = generate_omni_sector_dashboard(telemetry)
        self.assertTrue(dash_path.exists())
        
        with open(dash_path, "r", encoding="utf-8") as fp:
            content = fp.read()
            self.assertIn("AME GLOBAL • OMNI-SECTOR WEALTH MACHINE", content)
            self.assertIn("Enterprise Tech & AI Automation", content)
            self.assertIn("Global Trade, EXIM & Supply Chain Arbitrage", content)
            self.assertIn("Autonomous AI Agent Swarms & Micro-APIs", content)
            self.assertIn("Sovereign Treasury, FX Spreads & Yield Compounding", content)
            self.assertIn("Digital Intellectual Property & Knowledge Monopolies", content)
            self.assertIn("Global Capability Centers (GCC) & Founders' Office Advisory", content)
            self.assertIn("INTERACTIVE DAILY HARVEST SIMULATOR", content)


if __name__ == "__main__":
    unittest.main()
