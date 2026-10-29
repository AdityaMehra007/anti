"""
Unit & Integration Tests for Blackbird OSINT & Defensive Intelligence Suite.
Tests census metrics, permutations, filtering, risk scoring, AI profiling,
report exporters, and API request handlers.
"""

import json
import os
import shutil
import sys
import unittest
from pathlib import Path

# Add workspace root to path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from blackbird_orchestrator import BlackbirdOrchestrator, CockpitRequestHandler


class TestBlackbirdOrchestrator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.orchestrator = BlackbirdOrchestrator()
        cls.test_output_dir = WORKSPACE_ROOT / "blackbird_reports" / "test_scratch"
        cls.test_output_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if cls.test_output_dir.exists():
            shutil.rmtree(cls.test_output_dir, ignore_errors=True)

    def test_census_and_datasets_loaded(self):
        stats = self.orchestrator.get_statistics()
        self.assertIn("total_username_platforms", stats)
        self.assertGreaterEqual(stats["total_username_platforms"], 600)
        self.assertGreaterEqual(stats["total_email_platforms"], 10)
        self.assertIn("social", stats["category_distribution"])
        self.assertIn("tech", stats["category_distribution"])
        self.assertTrue(stats["datasets_loaded"]["wmn_data"])
        self.assertGreater(stats["datasets_loaded"]["user_agents_count"], 0)

    def test_permutations_generation(self):
        elements = ["alice", "bob"]
        perms_strict = self.orchestrator.generate_permutations(elements, mode="strict")
        self.assertIn("alice_bob", perms_strict)
        self.assertIn("bob_alice", perms_strict)
        self.assertIn("alice.bob", perms_strict)
        self.assertIn("alice-bob", perms_strict)

        single = self.orchestrator.generate_permutations(["solo"])
        self.assertEqual(single, ["solo"])

    def test_site_filtering(self):
        # Category filter
        tech_sites = self.orchestrator.filter_sites(category="tech")
        self.assertGreater(len(tech_sites), 0)
        for s in tech_sites:
            self.assertEqual((s.get("cat") or "").lower(), "tech")

        # NSFW stripping
        all_sites = self.orchestrator.filter_sites(no_nsfw=False)
        safe_sites = self.orchestrator.filter_sites(no_nsfw=True)
        self.assertLess(len(safe_sites), len(all_sites))

        # Site name filter
        github_matches = self.orchestrator.filter_sites(site_name="github")
        self.assertTrue(any("github" in s.get("name", "").lower() for s in github_matches))

    def test_defensive_risk_scoring(self):
        mock_accounts = [
            {"name": "GitHub", "category": "tech"},
            {"name": "Twitter / X", "category": "social"},
            {"name": "Reddit", "category": "social"},
            {"name": "Binance", "category": "finance"},
            {"name": "Steam", "category": "gaming"}
        ]
        threat = self.orchestrator.calculate_defensive_risk_score(
            target="target_alpha",
            target_type="username",
            found_accounts=mock_accounts,
            total_probed=692
        )

        self.assertIn("footprint_index", threat)
        self.assertGreater(threat["footprint_index"], 0.0)
        self.assertLessEqual(threat["footprint_index"], 100.0)
        self.assertIn("threat_tier", threat)
        self.assertIn("recommendations", threat)
        self.assertGreaterEqual(len(threat["recommendations"]), 3)
        self.assertIn("impersonation_vulnerability", threat)
        self.assertIn("credential_stuffing_risk", threat)

    def test_behavioral_profiling(self):
        dev_accounts = [
            {"name": "GitHub", "category": "coding"},
            {"name": "GitLab", "category": "coding"},
            {"name": "DockerHub", "category": "tech"},
            {"name": "HackerNews", "category": "tech"}
        ]
        profile = self.orchestrator.generate_behavioral_profile("dev_guru", dev_accounts)

        self.assertIn("profile_type", profile)
        self.assertEqual(profile["profile_type"], "Software Architect / Technologist")
        self.assertIn("Developer", profile["tags"])
        self.assertIn("summary", profile)
        self.assertIn("risk_flags", profile)

    def test_mock_simulation_scan(self):
        scan = self.orchestrator.run_mock_scan("test_user")
        self.assertEqual(scan["status"], "SUCCESS")
        self.assertEqual(scan["mode"], "SIMULATION / FAST_DEMO")
        self.assertEqual(scan["target"], "test_user")
        self.assertGreater(scan["found_count"], 0)
        self.assertIn("threat_audit", scan)
        self.assertIn("ai_profile", scan)

    def test_multi_format_exports(self):
        scan = self.orchestrator.run_mock_scan("export_test_user")

        p_json = self.test_output_dir / "test.json"
        p_csv = self.test_output_dir / "test.csv"
        p_md = self.test_output_dir / "test.md"
        p_html = self.test_output_dir / "test.html"

        res_json = self.orchestrator.export_json(scan, output_path=p_json)
        res_csv = self.orchestrator.export_csv(scan, output_path=p_csv)
        res_md = self.orchestrator.export_markdown_dossier(scan, output_path=p_md)
        res_html = self.orchestrator.export_html_report(scan, output_path=p_html)

        # Assert files exist and have non-trivial content
        self.assertTrue(res_json.exists())
        self.assertGreater(res_json.stat().st_size, 100)

        self.assertTrue(res_csv.exists())
        self.assertGreater(res_csv.stat().st_size, 50)

        self.assertTrue(res_md.exists())
        with open(res_md, "r", encoding="utf-8") as f:
            md_content = f.read()
            self.assertIn("BLACKBIRD OSINT & DEFENSIVE THREAT AUDIT", md_content)
            self.assertIn("Footprint Index", md_content)

        self.assertTrue(res_html.exists())
        with open(res_html, "r", encoding="utf-8") as f:
            html_content = f.read()
            self.assertIn("Blackbird OSINT Dossier", html_content)
            self.assertIn("Footprint Index", html_content)


if __name__ == "__main__":
    unittest.main()
