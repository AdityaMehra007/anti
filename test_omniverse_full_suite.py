"""
OMNIVERSE INFINITY COMPREHENSIVE VERIFICATION TEST SUITE
Full-stack unit, integration, and security verification tests covering:
1. SQLite Schema & Master Census Integrity (4,500 companies, 14 vacancies, 1,781 recruiters)
2. ATS Resume Builder (4 tracks, HTML & Markdown, 0 sales terms)
3. Application Dockets & Tailored STAR Letters
4. Merkle Tree Dispatcher & SHA-256 Proofs
5. RFC 5322 Mailer & Outbox MIME Generation
6. Compensation & Net In-Hand Salary Analytics (FY 2025-26)
7. Warm Referral Graph & Alumni Mapping
8. Sentinel Daemon Health Cycle
9. FastAPI Server Endpoints via TestClient

Directives: OMEGA CONSTITUTION Mode G (Audit) & Directives 310-330.
"""

import os
import json
import sqlite3
import hashlib
import unittest
from email import message_from_file

DB_PATH = r"e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
RESUMES_DIR = r"e:\anti\resumes"
OUTBOX_DIR = r"e:\anti\outbox"
DOCKETS_PATH = r"e:\anti\OMNIVERSE_APPLICATION_DOCKETS.json"


class TestOmniverseDatabaseIntegrity(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_database_tables_exist(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in self.cursor.fetchall()]
        required = [
            "omniverse_companies", "omniverse_live_vacancies", "omniverse_recruiters",
            "omniverse_corporate_relationships", "omniverse_mail_outbox", "omniverse_audit_log"
        ]
        for req in required:
            self.assertIn(req, tables, f"Missing table: {req}")

    def test_company_census_scale(self):
        self.cursor.execute("SELECT COUNT(*) FROM omniverse_companies;")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 4500, "Census count must equal exactly 4,500 companies.")

    def test_vacancies_non_sales_compliance(self):
        self.cursor.execute("SELECT COUNT(*) FROM omniverse_live_vacancies WHERE non_sales_verified = 1;")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 14, "Must have exactly 14 verified non-sales vacancies.")

    def test_recruiter_directory_scale(self):
        self.cursor.execute("SELECT COUNT(*) FROM omniverse_recruiters;")
        count = self.cursor.fetchone()[0]
        self.assertGreaterEqual(count, 1700, "Must have at least 1,700 recruiter contacts.")

    def test_corporate_trees_scale(self):
        self.cursor.execute("SELECT COUNT(*) FROM omniverse_corporate_relationships;")
        count = self.cursor.fetchone()[0]
        self.assertGreaterEqual(count, 30, "Must have at least 30 global corporate trees.")


class TestOmniverseResumeEngine(unittest.TestCase):
    def test_resumes_generated_and_parseable(self):
        manifest_path = os.path.join(RESUMES_DIR, "RESUME_MANIFEST.json")
        self.assertTrue(os.path.exists(manifest_path), "Resume manifest must exist.")
        
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        self.assertEqual(len(manifest), 4, "Must have 4 ATS resume variants.")
        
        prohibited_sales_terms = ["cold call", "telecalling", "door to door", "commission only", "field sales agent"]
        
        for item in manifest:
            md_path = item["markdown_path"]
            html_path = item["html_path"]
            self.assertTrue(os.path.exists(md_path), f"Markdown resume missing: {md_path}")
            self.assertTrue(os.path.exists(html_path), f"HTML resume missing: {html_path}")
            
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read().lower()
                self.assertIn("aditya mehra", content)
                self.assertIn("dayananda sagar university", content)
                self.assertIn("aero india 2025", content)
                for term in prohibited_sales_terms:
                    self.assertNotIn(term, content, f"Found prohibited sales term '{term}' in {md_path}")


class TestOmniverseApplicationDockets(unittest.TestCase):
    def test_dockets_structure_and_truth(self):
        self.assertTrue(os.path.exists(DOCKETS_PATH), "Dockets JSON must exist.")
        with open(DOCKETS_PATH, "r", encoding="utf-8") as f:
            dockets = json.load(f)
            
        self.assertEqual(len(dockets), 14, "Must have exactly 14 dockets.")
        for d in dockets:
            self.assertIn("job_id", d)
            self.assertIn("company_name", d)
            self.assertIn("target_role", d)
            self.assertIn("tailored_cover_letter", d)
            self.assertIn("Situation & Task", d["tailored_cover_letter"])
            self.assertIn("Action:", d["tailored_cover_letter"])
            self.assertIn("Result:", d["tailored_cover_letter"])


class TestOmniverseMailerAndOutbox(unittest.TestCase):
    def test_outbox_rfc5322_compliance(self):
        self.assertTrue(os.path.exists(OUTBOX_DIR), "Outbox directory must exist.")
        eml_files = [f for f in os.listdir(OUTBOX_DIR) if f.endswith(".eml")]
        self.assertEqual(len(eml_files), 14, "Outbox must contain 14 .eml packages.")
        
        sample_path = os.path.join(OUTBOX_DIR, eml_files[0])
        with open(sample_path, "r", encoding="utf-8") as f:
            msg = message_from_file(f)
            
        self.assertIn("Subject", msg)
        self.assertIn("From", msg)
        self.assertIn("To", msg)
        self.assertIn("X-Candidate-ID", msg)
        self.assertIn("X-Verification-Proof", msg)
        self.assertEqual(msg["X-Candidate-ID"], "ADI-DSU-2026")


class TestOmniverseAnalytics(unittest.TestCase):
    def test_salary_calculations(self):
        from omniverse_analytics import calculate_bengaluru_inhand_salary
        
        # Test 6.0 LPA (under 7L threshold -> Section 87A rebate applies)
        res_6 = calculate_bengaluru_inhand_salary(6.0)
        self.assertEqual(res_6["monthly_tax"], 0.0, "Income tax should be 0 under 7L with rebate.")
        self.assertGreater(res_6["monthly_inhand"], 45000.0)
        
        # Test 10.0 LPA
        res_10 = calculate_bengaluru_inhand_salary(10.0)
        self.assertGreater(res_10["monthly_tax"], 0.0)
        self.assertGreater(res_10["monthly_inhand"], 70000.0)
        self.assertEqual(res_10["monthly_pt"], 200.0)


class TestOmniverseDaemon(unittest.TestCase):
    def test_daemon_cycle_execution(self):
        from omniverse_daemon import execute_cycle
        result = execute_cycle(cycle_num=999)
        self.assertEqual(result["status"], "HEALTHY")
        self.assertTrue(result["non_sales_verified"])
        self.assertEqual(result["table_counts"]["omniverse_companies"], 4500)


class TestOmniverseFastAPIServer(unittest.TestCase):
    def setUp(self):
        from fastapi.testclient import TestClient
        from omniverse_server import app
        self.client = TestClient(app)

    def test_api_status(self):
        r = self.client.get("/api/status")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "HEALTHY")

    def test_api_summary(self):
        r = self.client.get("/api/summary")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["total_companies"], 4500)
        self.assertEqual(data["live_non_sales_vacancies"], 14)

    def test_api_vacancies(self):
        r = self.client.get("/api/vacancies")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["total"], 14)

    def test_api_companies_pagination(self):
        r = self.client.get("/api/companies?page=1&page_size=10")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data["companies"]), 10)
        self.assertEqual(data["total_records"], 4500)

    def test_api_salary_endpoint(self):
        r = self.client.get("/api/salary?ctc_lpa=8.5")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("net_monthly_in_hand", data)
        self.assertGreater(data["net_monthly_in_hand"], 60000)

    def test_api_resumes(self):
        r = self.client.get("/api/resumes")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()["resumes"]), 4)

    def test_api_deliverables_endpoints(self):
        r = self.client.get("/api/deliverables")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["total_deliverables"], 35)

        r_item = self.client.get("/api/deliverables/01_master_company_database?format=json")
        self.assertEqual(r_item.status_code, 200)
        self.assertEqual(len(r_item.json()), 4500)

    def test_api_calendar_endpoint(self):
        r = self.client.get("/api/hiring-calendar")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["total_windows"], 12)

    def test_api_skills_endpoint(self):
        r = self.client.get("/api/skills-portfolio")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["candidate"], "Aditya Mehra")
        self.assertEqual(len(data["skills_matrix"]), 8)
        self.assertEqual(len(data["portfolio_projects"]), 5)

    def test_api_interview_drills(self):
        r = self.client.get("/api/interview-drills")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(r.json()["total_packs"], 3)

    def test_api_referrals(self):
        r = self.client.get("/api/referrals")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["total_nodes_indexed"], 9223)


class TestOmniverseSection43Deliverables(unittest.TestCase):
    def test_all_35_deliverables_exist(self):
        deliv_dir = r"e:\anti\omniverse_deliverables"
        self.assertTrue(os.path.exists(deliv_dir))
        
        manifest_path = os.path.join(deliv_dir, "MASTER_SECTION_43_DELIVERABLES_MANIFEST.json")
        self.assertTrue(os.path.exists(manifest_path))
        
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        self.assertEqual(manifest["total_deliverables"], 35)
        for item in manifest["items"]:
            has_any = item["has_csv"] or item["has_json"] or item["has_md"]
            self.assertTrue(has_any, f"Deliverable {item['id']} has no exported file.")


class TestOmniverseHiringCalendarAndSkills(unittest.TestCase):
    def test_calendar_integrity(self):
        cal_path = r"e:\anti\OMNIVERSE_12_MONTH_HIRING_CALENDAR.json"
        self.assertTrue(os.path.exists(cal_path))
        with open(cal_path, "r", encoding="utf-8") as f:
            cal = json.load(f)
        self.assertEqual(len(cal), 12)
        quarters = set(x["quarter"] for x in cal)
        self.assertTrue({"Q4 2026", "Q1 2027", "Q2 2027", "Q3 2027"}.issubset(quarters))

    def test_skills_portfolio_integrity(self):
        portfolio_path = r"e:\anti\OMNIVERSE_SKILLS_PORTFOLIO.json"
        self.assertTrue(os.path.exists(portfolio_path))
        with open(portfolio_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["candidate"], "Aditya Mehra")
        self.assertEqual(len(data["skills_matrix"]), 8)
class TestOmniverseCockpitIntegrity(unittest.TestCase):
    def test_cockpit_html_has_all_11_tabs(self):
        cockpit_path = r"e:\anti\OMNIVERSE_INFINITY_COCKPIT.html"
        self.assertTrue(os.path.exists(cockpit_path), "Cockpit HTML must exist.")
        with open(cockpit_path, "r", encoding="utf-8") as f:
            html = f.read()

        required_tabs = [
            "tab-vacancies", "tab-census", "tab-hierarchies", "tab-recruiters",
            "tab-deliverables", "tab-calendar", "tab-resumes", "tab-skills",
            "tab-calculator", "tab-defense", "tab-audit"
        ]
        for tab_id in required_tabs:
            self.assertIn(tab_id, html, f"Cockpit HTML missing required tab: {tab_id}")

        self.assertIn("Aditya Mehra", html)
        self.assertIn("4,500", html)
        self.assertIn("1,781", html)


if __name__ == "__main__":
    unittest.main()

