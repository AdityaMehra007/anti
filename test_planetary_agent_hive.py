#!/usr/bin/env python3
"""
test_planetary_agent_hive.py - Verification Suite for Planetary Agent Swarm
"""

import unittest
import json
from pathlib import Path
from planetary_agent_hive import (
    scan_skills_ecosystem,
    synthesize_planetary_telemetry,
    generate_planetary_dashboard,
    TELEMETRY_OUT,
    DASHBOARD_HTML,
    PLANETARY_NODES,
    AGENT_DIVISIONS
)

class TestPlanetaryAgentHive(unittest.TestCase):

    def test_scan_skills_ecosystem(self):
        skills_data = scan_skills_ecosystem()
        self.assertIsNotNone(skills_data)
        self.assertIn("total_skills", skills_data)
        self.assertGreater(skills_data["total_skills"], 500, "Should catalog over 500 skills from .agents/skills")
        self.assertIn("categories", skills_data)

    def test_synthesize_planetary_telemetry(self):
        telemetry = synthesize_planetary_telemetry()
        self.assertIsNotNone(telemetry)
        self.assertEqual(telemetry["supreme_principal"], "Aditya Mehra")
        
        s = telemetry["summary"]
        self.assertEqual(s["total_planetary_nodes"], len(PLANETARY_NODES))
        self.assertEqual(s["total_agent_divisions"], len(AGENT_DIVISIONS))
        self.assertGreater(s["total_active_agents"], 100)
        
        # Verify JSON export
        self.assertTrue(TELEMETRY_OUT.exists())
        with open(TELEMETRY_OUT, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            self.assertEqual(data["command_headquarters"], "Bengaluru, Karnataka, India")

    def test_generate_planetary_dashboard(self):
        telemetry = synthesize_planetary_telemetry()
        dash_path = generate_planetary_dashboard(telemetry)
        self.assertTrue(dash_path.exists())
        
        with open(dash_path, "r", encoding="utf-8") as fp:
            content = fp.read()
            self.assertIn("CIVILIZATION Ω∞ • PLANETARY AGENT SWARM", content)
            self.assertIn("United States", content)
            self.assertIn("India (Bengaluru (HQ))", content)
            self.assertIn("United Arab Emirates", content)
            self.assertIn("DIV-MACRO-01", content)


if __name__ == "__main__":
    unittest.main()
