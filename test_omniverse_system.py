"""
COMPREHENSIVE TEST SUITE FOR OMNIVERSE INFINITY ULTIMATE SYSTEM
Verifies database integrity, census sizing, vacancy scoring,
application dockets, dispatcher execution, and cockpit UI generation.
"""

import os
import unittest
import sqlite3
import json

import omniverse_engine
import omniverse_dockets
import omniverse_dispatcher


class TestOmniverseSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = r"e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
        omniverse_engine.populate_omniverse_data(cls.db_path)

    def test_database_table_presence(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cur.fetchall()]
        conn.close()

        expected = [
            "omniverse_companies",
            "omniverse_corporate_relationships",
            "omniverse_live_vacancies",
            "omniverse_recruiters",
            "omniverse_applications",
            "omniverse_audit_log"
        ]
        for tbl in expected:
            self.assertIn(tbl, tables, f"Expected table {tbl} must exist.")

    def test_companies_census_scale(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM omniverse_companies;")
        count = cur.fetchone()[0]
        conn.close()

        self.assertGreaterEqual(count, 4500, "Census must contain at least 4,500 unique verified companies.")

    def test_corporate_hierarchies_scale(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM omniverse_corporate_relationships;")
        count = cur.fetchone()[0]
        conn.close()

        self.assertGreaterEqual(count, 25, "Corporate hierarchy graph must have at least 25 nodes.")

    def test_live_vacancies_non_sales_compliance(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM omniverse_live_vacancies WHERE non_sales_verified = 1;")
        verified_count = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM omniverse_live_vacancies;")
        total_count = cur.fetchone()[0]
        conn.close()

        self.assertEqual(verified_count, total_count, "All live vacancies must be 100% non-sales verified.")
        self.assertGreaterEqual(total_count, 12, "Must have at least 12 verified live vacancies.")

    def test_recruiter_network_scale(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM omniverse_recruiters;")
        count = cur.fetchone()[0]
        conn.close()

        self.assertGreaterEqual(count, 1700, "Must have at least 1,700 recruiter contacts.")

    def test_application_dockets_generation(self):
        dockets = omniverse_dockets.build_application_dockets()
        self.assertGreaterEqual(len(dockets), 12, "Must generate at least 12 dockets.")
        
        self.assertTrue(os.path.exists(r"e:\anti\OMNIVERSE_APPLICATION_DOCKETS.json"))
        self.assertTrue(os.path.exists(r"e:\anti\OMNIVERSE_APPLICATION_DOCKETS.md"))

        with open(r"e:\anti\OMNIVERSE_APPLICATION_DOCKETS.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("tailored_cover_letter", data[0])
        self.assertIn("Aditya Mehra", data[0]["tailored_cover_letter"])

    def test_dispatcher_execution_and_hashes(self):
        omniverse_dispatcher.execute_batch_dispatch()
        counts, apps = omniverse_dispatcher.get_pipeline_status()
        
        self.assertIn("DISPATCHED", counts)
        self.assertGreaterEqual(counts["DISPATCHED"], 12)
        
        # Check SHA-256 hash formatting
        for app in apps:
            self.assertTrue(app[6].startswith("SHA256:"), f"Invalid hash proof: {app[6]}")

    def test_cockpit_html_generation(self):
        out_html = r"e:\anti\OMNIVERSE_INFINITY_COCKPIT.html"
        omniverse_engine.generate_cockpit_html(self.db_path, out_html)
        self.assertTrue(os.path.exists(out_html))
        self.assertGreater(os.path.getsize(out_html), 25000, "Cockpit HTML must be richly populated (>25KB).")

    def test_interview_defense_compendium(self):
        import omniverse_interview_defense
        packs = omniverse_interview_defense.generate_interview_defense_compendium()
        self.assertGreaterEqual(len(packs), 4)
        self.assertTrue(os.path.exists(r"e:\anti\OMNIVERSE_INTERVIEW_DEFENSE_COMPENDIUM.md"))

    def test_warm_referral_matrix(self):
        import omniverse_referral_graph
        clusters = omniverse_referral_graph.build_warm_referral_matrix()
        self.assertGreaterEqual(len(clusters), 10)
        self.assertTrue(os.path.exists(r"e:\anti\OMNIVERSE_WARM_REFERRAL_MATRIX.md"))

    def test_compensation_analytics(self):
        import omniverse_analytics
        sal = omniverse_analytics.calculate_bengaluru_inhand_salary(8.5)
        self.assertGreater(sal["monthly_inhand"], 50000.0)
        self.assertLess(sal["monthly_inhand"], 85000.0)

        leverage = omniverse_analytics.evaluate_career_leverage("Ops Analyst", "Tier 1 Global Titan", 8.5, 30)
        self.assertGreaterEqual(leverage, 70.0)


if __name__ == "__main__":
    unittest.main()
