"""
Unit tests for Bengaluru Startup Intelligence Engine & Cockpit Suite.
Ensures zero-vibe coding and deterministic execution.
"""

import unittest
import os
import sqlite3
import csv
import json

from bengaluru_startup_intel_engine import (
    init_database,
    export_csvs,
    calculate_fit_score,
    get_db,
    DATA_DIR,
    DB_PATH,
    DOSSIER_DIR
)

class TestBengaluruStartupIntel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_database()
        export_csvs()

    def test_database_tables_exist(self):
        """Verify all relational tables are created and seeded."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in c.fetchall()]
        conn.close()

        expected = ["startups", "jobs", "funding_rounds", "ecosystem_news", "change_log"]
        for t in expected:
            self.assertIn(t, tables, f"Missing table: {t}")

    def test_job_counts_and_high_fit(self):
        """Verify job counts and presence of tier-1 high fit roles."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM jobs")
        total_jobs = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM jobs WHERE fit_score >= 95")
        high_fit = c.fetchone()[0]

        conn.close()
        self.assertGreaterEqual(total_jobs, 10, "Total jobs should be at least 10")
        self.assertGreaterEqual(high_fit, 3, "High-fit (95%+) roles should be at least 3")

    def test_specific_priority_jobs_exist(self):
        """Verify top tracked roles from the briefing exist in the database."""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id, startup_name, role_title, fit_score FROM jobs WHERE id IN ('JOB-078', 'JOB-073', 'JOB-072')")
        rows = {r[0]: dict(r) for r in c.fetchall()}
        conn.close()

        self.assertIn("JOB-078", rows)
        self.assertEqual(rows["JOB-078"]["startup_name"], "Zethic Technologies")
        self.assertGreaterEqual(rows["JOB-078"]["fit_score"], 95)

        self.assertIn("JOB-073", rows)
        self.assertEqual(rows["JOB-073"]["startup_name"], "Y-Not Design & Manufacturing")
        self.assertGreaterEqual(rows["JOB-073"]["fit_score"], 95)

        self.assertIn("JOB-072", rows)
        self.assertEqual(rows["JOB-072"]["startup_name"], "Samaaro")
        self.assertGreaterEqual(rows["JOB-072"]["fit_score"], 95)

    def test_fit_score_calculation(self):
        """Verify algorithmic scoring reflects BBA and non-sales purity."""
        # Case A: Ideal BBA Operations role
        ideal_job = {
            "role_title": "Founder's Office & Strategy Intern",
            "duties": "Market research, Excel financial models, executive dashboards",
            "eligibility": "BBA, Commerce or Business graduates; freshers welcome",
            "stipend_published": "₹20,000 / month",
            "work_mode": "In-Office (Bengaluru)"
        }
        score, reasons = calculate_fit_score(ideal_job)
        self.assertGreaterEqual(score, 90, "Ideal job should score 90+")

        # Case B: Cold outbound sales role
        sales_job = {
            "role_title": "Sales Development Representative Intern",
            "duties": "Cold calling, prospecting, outbound sales quota, field sales",
            "eligibility": "Any graduate",
            "stipend_published": "Commission only",
            "work_mode": "Bengaluru"
        }
        sales_score, _ = calculate_fit_score(sales_job)
        self.assertLess(sales_score, 75, "Sales role should be penalized")
        self.assertLess(sales_score, score, "Operational role must score higher than sales role")

    def test_csv_exports_exist_and_non_empty(self):
        """Verify CSV export files are generated with valid data."""
        csv_files = [
            os.path.join(DATA_DIR, "bengaluru_startup_jobs.csv"),
            os.path.join(DATA_DIR, "bengaluru_startup_funding.csv"),
            os.path.join(DATA_DIR, "bengaluru_startup_news.csv"),
            os.path.join(DATA_DIR, "bengaluru_startup_daily_delta.csv"),
            os.path.join(DATA_DIR, "bengaluru_startup_directory_1000.csv"),
            os.path.join(DATA_DIR, "bengaluru_startup_vcs.csv")
        ]
        for path in csv_files:
            self.assertTrue(os.path.exists(path), f"File missing: {path}")
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
                self.assertGreater(len(rows), 1, f"CSV should have header and at least 1 data row: {path}")

    def test_bangalore_startup_map_ecosystem(self):
        """Verify complete 1,000+ startups and 70+ VCs from Bangalore Startup Map."""
        conn = get_db()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM startups")
        total_startups = c.fetchone()[0]
        self.assertGreaterEqual(total_startups, 1000, "Should have 1,000+ startups indexed")

        c.execute("SELECT COUNT(*) FROM venture_capital_firms")
        total_vcs = c.fetchone()[0]
        self.assertGreaterEqual(total_vcs, 70, "Should have 70+ VC firms indexed")

        # Verify key geographic clusters exist
        c.execute("SELECT COUNT(*) FROM startups WHERE area LIKE '%HSR%' OR blr_location LIKE '%HSR%'")
        hsr_count = c.fetchone()[0]
        self.assertGreaterEqual(hsr_count, 150, "HSR cluster should have 150+ startups")

        c.execute("SELECT COUNT(*) FROM startups WHERE area LIKE '%Koramangala%' OR blr_location LIKE '%Koramangala%'")
        kora_count = c.fetchone()[0]
        self.assertGreaterEqual(kora_count, 100, "Koramangala cluster should have 100+ startups")

        # Verify geocoding coordinates
        c.execute("SELECT COUNT(*) FROM startups WHERE lat IS NOT NULL AND lng IS NOT NULL")
        geocoded = c.fetchone()[0]
        self.assertGreaterEqual(geocoded, 500, "At least 500 startups should be geocoded with coordinates")

        conn.close()

    def test_dossiers_exist_and_complete(self):
        """Verify all 5 enterprise application dossiers are generated."""
        expected_dossiers = [
            "JOB-078_Zethic_Technologies_Founders_Office.md",
            "JOB-073_Y_Not_Emerging_Talent_Program.md",
            "JOB-072_Samaaro_Customer_Success_Intern.md",
            "JOB-071_Vantrix_Ventures_Founders_Office.md",
            "JOB-074_Vats_Mobility_Digital_Growth.md"
        ]
        for fname in expected_dossiers:
            dpath = os.path.join(DOSSIER_DIR, fname)
            self.assertTrue(os.path.exists(dpath), f"Dossier missing: {fname}")
            with open(dpath, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertGreater(len(content), 800, f"Dossier {fname} is too short")
                self.assertIn("ATS-Optimized", content)
                self.assertIn("Cover Letter", content)

    def test_cockpit_html_exists(self):
        """Verify the interactive cockpit HTML exists and has core elements."""
        cockpit_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bengaluru_startup_cockpit.html")
        self.assertTrue(os.path.exists(cockpit_path))
        with open(cockpit_path, "r", encoding="utf-8") as f:
            html = f.read()
            self.assertIn("Bengaluru Startup Intelligence Cockpit", html)
            self.assertIn("kpi-grid", html)
            self.assertIn("Zethic Technologies", html)
            self.assertIn("Y-Not Design & Manufacturing", html)

if __name__ == "__main__":
    unittest.main()
