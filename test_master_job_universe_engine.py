#!/usr/bin/env python3
"""
test_master_job_universe_engine.py - Verification Suite for Master Job Universe
"""

import unittest
import json
from pathlib import Path
from master_job_universe_engine import (
    extract_database_counts,
    synthesize_job_universe_telemetry,
    generate_job_universe_dashboard,
    TELEMETRY_OUT,
    DASHBOARD_HTML,
    TOP_20_UNICORNS
)

class TestMasterJobUniverseEngine(unittest.TestCase):

    def test_extract_database_counts(self):
        counts, sample_jobs = extract_database_counts()
        self.assertIsNotNone(counts)
        self.assertIn("jobfunnel_master", counts)
        self.assertGreater(counts["jobfunnel_master"]["count"], 5000)
        self.assertGreater(len(sample_jobs), 0)

    def test_synthesize_job_universe_telemetry(self):
        telemetry = synthesize_job_universe_telemetry()
        self.assertIsNotNone(telemetry)
        self.assertIn("macro_summary", telemetry)
        m = telemetry["macro_summary"]
        self.assertGreater(m["total_indexed_opportunities"], 10000)
        self.assertEqual(len(telemetry["unicorns"]), len(TOP_20_UNICORNS))
        
        # Verify JSON file
        self.assertTrue(TELEMETRY_OUT.exists())
        with open(TELEMETRY_OUT, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            self.assertIn("Aditya Mehra", data["candidate"])

    def test_generate_job_universe_dashboard(self):
        telemetry = synthesize_job_universe_telemetry()
        dash_path = generate_job_universe_dashboard(telemetry)
        self.assertTrue(dash_path.exists())
        
        with open(dash_path, "r", encoding="utf-8") as fp:
            content = fp.read()
            self.assertIn("OMEGA MASTER CAREER & JOB UNIVERSE", content)
            self.assertIn("ByteDance Ltd. (TikTok)", content)
            self.assertIn("STRK-001", content)


if __name__ == "__main__":
    unittest.main()
