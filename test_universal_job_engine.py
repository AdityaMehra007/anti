#!/usr/bin/env python3
"""
test_universal_job_engine.py - Complete Verification Suite for Universal Job & Skill Intelligence
=================================================================================================
Verifies:
  1. Universal Job Taxonomy completeness (13 families, 30+ archetypes, JSON/SQLite exports)
  2. Universal JD Intelligence Engine parsing across multiple distinct domains
  3. Skill extraction precision & ATS score computation with semantic clustering
  4. Google X-Y-Z resume bullet synthesis and STAR interview battlecard structures
  5. Master Skill generation, Job-to-Skills matrix, and Cockpit HTML integrity
"""

import json
import sqlite3
import unittest
from pathlib import Path

from universal_job_taxonomy_master import (
    UNIVERSAL_JOB_TAXONOMY,
    get_all_job_families,
    get_all_archetypes,
    get_archetype_by_key,
    export_taxonomy_to_json,
    export_taxonomy_to_sqlite,
    JSON_EXPORT_PATH,
    SQLITE_DB_PATH
)
from universal_jd_intelligence_engine import UniversalJDIntelligenceEngine
from universal_skill_generator import (
    build_job_to_skill_matrix,
    generate_master_archetype_skills,
    MATRIX_JSON_PATH,
    MATRIX_CSV_PATH,
    SKILLS_DIR
)

ROOT_DIR = Path(r"e:\anti")
COCKPIT_HTML = ROOT_DIR / "universal_job_cockpit.html"


class TestUniversalJobEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        export_taxonomy_to_json()
        export_taxonomy_to_sqlite()
        cls.engine = UniversalJDIntelligenceEngine()
        cls.matrix = build_job_to_skill_matrix()

    def test_01_taxonomy_integrity(self):
        families = get_all_job_families()
        self.assertGreaterEqual(len(families), 13, "Must have at least 13 job families")

        archetypes = get_all_archetypes()
        self.assertGreaterEqual(len(archetypes), 30, "Must have at least 30 job archetypes")

        # Verify essential fields in every archetype
        for a in archetypes:
            self.assertIn("title", a)
            self.assertIn("hard_skills", a)
            self.assertIn("ats_keywords", a)
            self.assertIn("sample_kpis", a)
            self.assertIn("star_interview_prep", a)
            self.assertIn("thirty_sixty_ninety_plan", a)
            self.assertGreater(len(a["hard_skills"]), 2)
            self.assertGreater(len(a["ats_keywords"]), 2)

    def test_02_database_exports(self):
        self.assertTrue(JSON_EXPORT_PATH.exists(), "Taxonomy JSON must exist")
        with open(JSON_EXPORT_PATH, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            self.assertIn("families", data)

        self.assertTrue(SQLITE_DB_PATH.exists(), "Taxonomy SQLite DB must exist")
        conn = sqlite3.connect(str(SQLITE_DB_PATH))
        c = conn.cursor()
        c.execute("SELECT count(*) FROM job_archetypes")
        count = c.fetchone()[0]
        self.assertGreaterEqual(count, 30)
        conn.close()

    def test_03_dissect_ai_ml_job(self):
        jd = """
        We need a Senior Generative AI Engineer to build enterprise RAG pipelines, fine-tune models with LoRA,
        and manage vector databases like Pinecone. Must know Python, PyTorch, FastAPI, and Docker.
        """
        res = self.engine.dissect_jd(jd, role_title="Senior Generative AI Engineer", company="OpenAI")
        self.assertEqual(res["classification"]["matched_archetype_key"], "genai_llm_engineer")
        self.assertEqual(res["classification"]["family_key"], "ai_ml_data")
        self.assertIn("Python", res["skills_extracted"]["hard_skills"])
        self.assertIn("PyTorch", res["skills_extracted"]["hard_skills"])
        self.assertIn("RAG", res["skills_extracted"]["hard_skills"])
        self.assertEqual(res["classification"]["seniority_tier"]["code"], "L4")

    def test_04_dissect_b2b_sales_job(self):
        jd = """
        Hiring an Enterprise Account Executive to drive B2B Sales quotas.
        Must excel at cold outreach, Apollo.io, pipeline management, and closing MSAs in Salesforce.
        """
        res = self.engine.dissect_jd(jd, role_title="Enterprise Account Executive", company="Zepto")
        self.assertEqual(res["classification"]["matched_archetype_key"], "account_executive")
        self.assertIn("Cold Outreach", res["skills_extracted"]["hard_skills"])
        self.assertIn("Salesforce", res["skills_extracted"]["hard_skills"])
        self.assertGreaterEqual(res["ats_compatibility"]["ats_score_pct"], 60.0)

    def test_05_dissect_exim_logistics_job(self):
        jd = """
        Seeking an International Trade & EXIM Specialist to manage customs clearance, HS Code classification,
        Incoterms 2020 compliance, Bill of Lading, and Letters of Credit via ICEGATE.
        """
        res = self.engine.dissect_jd(jd, role_title="International Trade Specialist", company="Flexport")
        self.assertEqual(res["classification"]["matched_archetype_key"], "exim_international_trade_specialist")
        self.assertIn("Incoterms 2020", res["skills_extracted"]["hard_skills"])
        self.assertIn("Bill of Lading", res["skills_extracted"]["hard_skills"])

    def test_06_dissect_chief_of_staff_job(self):
        jd = """
        High-growth startup seeking Chief of Staff to the CEO to lead board decks, OKRs,
        financial modeling, and strategic initiatives.
        """
        res = self.engine.dissect_jd(jd, role_title="Chief of Staff to CEO", company="Tech Unicorn")
        self.assertEqual(res["classification"]["matched_archetype_key"], "chief_of_staff")
        self.assertIn(res["classification"]["seniority_tier"]["code"], ["L6", "L7"])

    def test_07_resume_bullets_and_star_defense(self):
        jd = "Looking for a Frontend Engineer with React, TypeScript, and Core Web Vitals optimization."
        res = self.engine.dissect_jd(jd, role_title="Frontend Engineer")
        bullets = res["tailored_resume_bullets_xyz"]
        self.assertGreaterEqual(len(bullets), 3)
        for b in bullets:
            self.assertIn("as measured by", b)

        star_cards = res["star_interview_defense"]
        self.assertGreaterEqual(len(star_cards), 1)
        self.assertIn("question", star_cards[0])
        self.assertIn("competency", star_cards[0])

    def test_08_matrix_and_master_skills_generation(self):
        self.assertTrue(MATRIX_JSON_PATH.exists())
        self.assertTrue(MATRIX_CSV_PATH.exists())

        created = generate_master_archetype_skills(self.matrix, limit=5)
        self.assertGreaterEqual(len(created), 5)
        for p in created:
            self.assertTrue(p.exists())
            with open(p, "r", encoding="utf-8") as fp:
                text = fp.read()
                self.assertIn("Master Capability Module", text)
                self.assertIn("Standard Operating Procedure", text)

    def test_09_cockpit_html_existence(self):
        self.assertTrue(COCKPIT_HTML.exists())
        with open(COCKPIT_HTML, "r", encoding="utf-8") as fp:
            content = fp.read()
            self.assertIn("OMEGA Job & Skill Intelligence Cockpit", content)
            self.assertIn("Live JD Dissector & Builder", content)
            self.assertIn("Universal Job Taxonomy", content)

    def test_10_database_batch_dissection_census(self):
        census_json = ROOT_DIR / "data" / "universal_dissected_jobs_500.json"
        self.assertTrue(census_json.exists(), "Census JSON must exist")
        with open(census_json, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            self.assertGreaterEqual(data["total_dissected"], 500)
            self.assertIn("average_ats_score", data)
            self.assertIn("top_in_demand_skills", data)
            self.assertIn("fit_tier_summary", data)

        conn = sqlite3.connect(str(SQLITE_DB_PATH))
        c = conn.cursor()
        c.execute("SELECT count(*) FROM dissected_jobs_census")
        row_count = c.fetchone()[0]
        self.assertGreaterEqual(row_count, 500, "SQLite dissected_jobs_census table must have >= 500 rows")

        # Verify columns exist
        c.execute("SELECT company, title, ats_score_pct, top_xyz_bullet, modality FROM dissected_jobs_census LIMIT 1")
        sample = c.fetchone()
        self.assertIsNotNone(sample[0])
        self.assertIsNotNone(sample[1])
        self.assertGreater(sample[2], 0.0)
        self.assertIn("as measured by", sample[3])
        conn.close()

    def test_11_application_dockets_generation(self):
        dockets_json = ROOT_DIR / "data" / "universal_application_dockets.json"
        self.assertTrue(dockets_json.exists(), "Application dockets JSON must exist")
        with open(dockets_json, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            self.assertGreaterEqual(data["total_dockets"], 100)
            first_doc = data["dockets"][0]
            self.assertIn("docket_id", first_doc)
            self.assertIn("cover_letter_hook", first_doc)
            self.assertIn("recruiter_inmail", first_doc)
            self.assertIn("tailored_resume_bullets", first_doc)
            self.assertIn("star_interview_defense", first_doc)
            self.assertGreaterEqual(len(first_doc["tailored_resume_bullets"]), 3)

    def test_12_cockpit_census_tab_integrity(self):
        with open(COCKPIT_HTML, "r", encoding="utf-8") as fp:
            content = fp.read()
            self.assertIn("tab-census", content)
            self.assertIn("view-census", content)
            self.assertIn("docket-modal", content)
            self.assertIn("dissectFromCensus", content)
            self.assertIn("openDocketModal", content)

    def test_13_cockpit_approval_queue_and_packages_tabs(self):
        with open(COCKPIT_HTML, "r", encoding="utf-8") as fp:
            content = fp.read()
            self.assertIn("tab-queue", content, "Cockpit must include Tab 5: Approval Queue")
            self.assertIn("tab-packages", content, "Cockpit must include Tab 6: Compiled Dossiers")
            self.assertIn("queue-table-tbody", content, "Queue table body must exist")
            self.assertIn("packages-cards-grid", content, "Packages cards grid must exist")
            self.assertIn("loadCompiledPackages", content, "Compiled packages loader must exist")

    def test_14_compiled_pdf_packages_integrity(self):
        pdf_dir = ROOT_DIR / "reports" / "enterprise_target_pdf_packages"
        self.assertTrue(pdf_dir.exists(), "Consolidated PDF report directory must exist")
        pdfs = list(pdf_dir.glob("*.pdf"))
        self.assertGreaterEqual(len(pdfs), 20, "Must have at least 20 compiled PDF packages")
        for p in pdfs[:5]:
            self.assertGreater(p.stat().st_size, 5000, f"PDF file {p.name} must be > 5KB")

    def test_15_approval_queue_csv_json_sync(self):
        csv_file = ROOT_DIR / "data" / "approval_queue.csv"
        json_file = ROOT_DIR / "data" / "approval_queue.json"
        self.assertTrue(csv_file.exists(), "Approval queue CSV must exist")
        self.assertTrue(json_file.exists(), "Approval queue JSON must exist")
        with open(json_file, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            actions = data["actions"] if isinstance(data, dict) else data
            self.assertGreaterEqual(len(actions), 400, "Approval queue must have >= 400 staged actions")


if __name__ == "__main__":
    unittest.main()
