#!/usr/bin/env python3
"""
test_omega_hyper_continuum.py - Verification Suite for OMEGA Hyper-Continuum Engine
"""

import unittest
import json
from pathlib import Path
from omega_hyper_continuum import (
    load_skills_summary,
    load_jobs_summary,
    load_funds_and_family_offices,
    synthesize_hyper_continuum,
    generate_hyper_dashboard,
    HYPER_TELEMETRY_OUT,
    HYPER_DASHBOARD_HTML
)

class TestOmegaHyperContinuum(unittest.TestCase):

    def test_load_skills_summary(self):
        skills = load_skills_summary()
        self.assertGreater(skills["total"], 500)
        self.assertIn("b2b_sales", skills)
        self.assertIn("finance_treasury", skills)

    def test_load_jobs_summary(self):
        jobs = load_jobs_summary()
        self.assertGreater(sum(jobs.values()), 10000)
        self.assertIn("jobfunnel_master", jobs)

    def test_load_funds_and_family_offices(self):
        funds = load_funds_and_family_offices()
        self.assertEqual(funds["family_offices_total"], 140)
        self.assertEqual(len(funds["capital_pillars"]), 8)
        self.assertGreater(len(funds["family_offices_sample"]), 0)

    def test_synthesize_hyper_continuum(self):
        telemetry = synthesize_hyper_continuum()
        self.assertIsNotNone(telemetry)
        self.assertIn("pillars", telemetry)
        p = telemetry["pillars"]
        self.assertIn("pillar_1_skills", p)
        self.assertIn("pillar_2_jobs", p)
        self.assertIn("pillar_3_agents", p)
        self.assertIn("pillar_4_funds", p)
        
        # Verify JSON file
        self.assertTrue(HYPER_TELEMETRY_OUT.exists())
        with open(HYPER_TELEMETRY_OUT, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            self.assertIn("Aditya Mehra", data["sovereign_principal"])

    def test_generate_hyper_dashboard(self):
        telemetry = synthesize_hyper_continuum()
        dash_path = generate_hyper_dashboard(telemetry)
        self.assertTrue(dash_path.exists())
        
        with open(dash_path, "r", encoding="utf-8") as fp:
            content = fp.read()
            self.assertIn("OMEGA HYPER-CONTINUUM COMMAND CENTER", content)
            self.assertIn("Skills Federation", content)
            self.assertIn("Company Jobs & Career", content)
            self.assertIn("Planetary Agent Swarms", content)
            self.assertIn("Family Offices & Funds", content)
            self.assertIn("PremjiInvest", content)


if __name__ == "__main__":
    unittest.main()
