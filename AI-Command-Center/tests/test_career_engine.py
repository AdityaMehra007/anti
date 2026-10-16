"""
Unit and Integration Test Suite for AI Career Operations Engine
==============================================================
Tests relational integrity, deduplication, 6-factor scoring rubric,
hard disqualification warnings, resume tailoring, and outreach generation.
"""

import os
import sys
import unittest

# Add paths to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "projects", "flagship-career-engine"))
sys.path.insert(0, os.path.join(BASE_DIR, "startup-lab"))
sys.path.insert(0, os.path.join(BASE_DIR, "career"))
sys.path.insert(0, os.path.join(BASE_DIR, "automation"))


from career_engine import CareerVault, OutreachGenerator, ResumeTailorer, ScoringEngine


class TestCareerEngine(unittest.TestCase):
    def setUp(self):
        # Use an isolated in-memory or temporary SQLite database for each test
        self.test_db = os.path.join(os.path.dirname(__file__), "test_temp_vault.db")
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.vault = CareerVault(self.test_db)

    def tearDown(self):
        self.vault.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_01_schema_initialization(self):
        cursor = self.vault.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cursor.fetchall()]
        self.assertIn("jobs", tables)
        self.assertIn("applications", tables)

    def test_02_job_insertion_and_scoring(self):
        sample_job = {
            "job_id": "TEST-EY-001",
            "company": "EY",
            "title": "Business Operations Associate",
            "url": "https://careers.ey.com/jobs/TEST-EY-001",
            "location": "Bengaluru",
            "department": "Operations",
            "experience_min": 0,
            "experience_max": 1,
            "required_skills": ["Excel", "SLA", "Process", "Reporting"],
            "description": "Seeking BBA or business graduate for vendor SLA monitoring and reporting in Excel.",
        }
        success, _msg, jid = self.vault.add_job(sample_job)
        self.assertTrue(success)
        self.assertIsNotNone(jid)

        job = self.vault.get_job("TEST-EY-001")
        self.assertIsNotNone(job)
        self.assertEqual(job["company"], "EY")
        self.assertGreaterEqual(job["fit_score"], 80)

    def test_03_deduplication_by_job_id_and_url(self):
        job1 = {
            "job_id": "DUP-001",
            "company": "Accenture",
            "title": "Procurement Analyst",
            "url": "https://accenture.com/job/dup-001",
            "location": "Bengaluru",
            "experience_min": 0,
        }
        success1, _, _ = self.vault.add_job(job1)
        self.assertTrue(success1)

        # Attempt same job_id
        job2 = {
            "job_id": "DUP-001",
            "company": "Accenture",
            "title": "Procurement Analyst Different URL",
            "url": "https://accenture.com/job/different-url",
            "location": "Bengaluru",
            "experience_min": 0,
        }
        success2, msg2, _ = self.vault.add_job(job2)
        self.assertFalse(success2)
        self.assertIn("Duplicate blocked", msg2)

        # Attempt same URL with tracking parameters
        job3 = {
            "job_id": "DUP-002",
            "company": "Accenture",
            "title": "Procurement Analyst Duplicate URL",
            "url": "https://accenture.com/job/dup-001?utm_source=linkedin&ref=feed",
            "location": "Bengaluru",
            "experience_min": 0,
        }
        success3, msg3, _ = self.vault.add_job(job3)
        self.assertFalse(success3)
        self.assertIn("Duplicate blocked", msg3)

    def test_04_hard_disqualification_filters(self):
        # Senior role requiring 5+ years
        senior_job = {
            "job_id": "SR-OPS-5YR",
            "company": "Global Logistics",
            "title": "Senior Operations Manager",
            "url": "https://example.com/sr-ops",
            "location": "Bengaluru",
            "experience_min": 5,
            "description": "Requires minimum 5 years managing enterprise logistics.",
        }
        _score, breakdown, flags = ScoringEngine.evaluate(senior_job)
        self.assertEqual(breakdown["eligibility_fresher"], 0)
        self.assertTrue(any("MANDATORY_EXPERIENCE_GATE" in f for f in flags))

        # Cold calling outbound sales role
        cold_sales_job = {
            "job_id": "COLD-CALL-01",
            "company": "FastLoans",
            "title": "Outbound Telecaller Executive",
            "url": "https://example.com/telecaller",
            "location": "Bengaluru",
            "experience_min": 0,
            "description": "Daily 100 cold calls selling insurance with strict quotas.",
        }
        _score_sales, breakdown_sales, flags_sales = ScoringEngine.evaluate(
            cold_sales_job
        )
        self.assertEqual(breakdown_sales["non_sales_fit"], 0)
        self.assertTrue(any("HARD_SALES_ROLE" in f for f in flags_sales))

    def test_05_resume_tailoring_and_truth_layer_alignment(self):
        job = {
            "job_id": "VENDOR-SCM-01",
            "company": "Puma India",
            "title": "Vendor Operations Specialist",
            "description": "Manage vendor SLAs, logistics cost negotiations, and inventory buffer planning.",
        }
        tailored = ResumeTailorer.tailor(job)
        self.assertEqual(tailored["company"], "Puma India")
        self.assertGreater(len(tailored["recommended_bullets"]), 0)
        # Check that top bullet mentions vendor/cost
        top_bullet = tailored["recommended_bullets"][0].lower()
        self.assertTrue(
            "vendor" in top_bullet
            or "cost" in top_bullet
            or "procurement" in top_bullet
        )

    def test_06_recruiter_outreach_generation(self):
        job = {
            "job_id": "EY-GDS-991",
            "company": "EY",
            "title": "Operations Associate",
            "location": "Bengaluru",
        }
        msg = OutreachGenerator.generate_recruiter_message(
            job, recruiter_name="Pooja Sharma"
        )
        self.assertIn("Dear Pooja Sharma", msg)
        self.assertIn("EY-GDS-991", msg)
        self.assertIn("Dayananda Sagar University", msg)
        self.assertIn("adityamehra799@gmail.com", msg)

    def test_07_rate_card_optimizer(self):
        from rate_card_optimizer import RateCardOptimizer

        benchmark = {"Tent Structure": 18.0, "Sound Rig": 35000.0}
        optimizer = RateCardOptimizer(benchmark)
        bid = [
            {"item_name": "Tent Structure", "quantity": 1000, "quoted_unit_rate": 24.0},
            {"item_name": "Sound Rig", "quantity": 1, "quoted_unit_rate": 45000.0},
        ]
        res = optimizer.audit_quotation(bid)
        self.assertGreater(res["percentage_savings"], 15.0)
        self.assertTrue(res["meets_target_savings"])

    def test_08_dataset_qa_validator(self):
        from annotation_qa_validator import DatasetQAValidator

        validator = DatasetQAValidator(allowed_classes=["robot", "box"])
        frames = [
            {
                "frame_id": "F1",
                "annotations": [{"class": "robot", "bbox": [10, 10, 50, 50]}],
            },
            {
                "frame_id": "F2",
                "annotations": [{"class": "invalid_tag", "bbox": [10, 10, 50, 50]}],
            },
        ]
        res = validator.validate_dataset(frames)
        self.assertEqual(res["total_annotations"], 2)
        self.assertEqual(res["defect_count"], 1)
        self.assertFalse(res["meets_99_sla"])

    def test_09_event_logistics_tracker(self):
        from event_logistics_tracker import EventLogisticsTracker

        tracker = EventLogisticsTracker("Test Event", budget_inr=1000000.0)
        tracker.add_vendor(
            "V1",
            "AV Vendor",
            "AV",
            contracted_amount=200000.0,
            hourly_delay_penalty_rate=0.05,
        )
        tracker.add_milestone("M1", "AV Setup", "10:00 AM", "V1")
        tracker.complete_milestone("M1", "12:00 PM", delay_hours=2.0)
        audit = tracker.generate_financial_audit()
        self.assertEqual(audit["total_penalties_recovered_inr"], 20000.0)
        self.assertEqual(audit["net_final_expenditure_inr"], 180000.0)
        self.assertEqual(audit["net_budget_savings_inr"], 820000.0)

    def test_10_interview_prep_engine(self):
        from interview_prep_engine import InterviewPrepEngine

        engine = InterviewPrepEngine()
        playbook = engine.generate_company_playbook(
            "Target India", "Business Operations Analyst"
        )
        self.assertEqual(playbook["company"], "Target India")
        self.assertIn("Aditya Mehra", playbook["candidate_intro_30s"])
        self.assertGreaterEqual(len(playbook["tailored_answers"]), 5)
        q1 = playbook["tailored_answers"][0]
        self.assertIn("AERO India 2025", q1["star"]["situation"])

    def test_11_application_recording_and_follow_ups(self):
        job = {
            "job_id": "APP-TEST-01",
            "company": "Target India",
            "title": "Business Operations Analyst",
            "url": "https://india.target.com/test-01",
            "location": "Bengaluru",
            "experience_min": 0,
        }
        self.vault.add_job(job)
        app = self.vault.record_application(
            "APP-TEST-01",
            resume_version="MASTER_ATS",
            notes="Submitted via workday",
            follow_up_days=3,
        )
        self.assertEqual(app["job_id"], "APP-TEST-01")

        updated_job = self.vault.get_job("APP-TEST-01")
        self.assertEqual(updated_job["status"], "APPLIED")

        apps = self.vault.get_applications()
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0]["company"], "Target India")

    def test_12_pdf_resumes_integrity(self):
        career_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "career")
        )
        pdf_names = [
            "ADITYA_MEHRA_MASTER_ATS_RESUME.pdf",
            "ADITYA_MEHRA_SUPPLY_CHAIN_PROCUREMENT.pdf",
            "ADITYA_MEHRA_AI_DATA_OPERATIONS.pdf",
        ]
        for name in pdf_names:
            pdf_path = os.path.join(career_dir, name)
            self.assertTrue(os.path.exists(pdf_path), f"Missing PDF resume: {name}")
            self.assertGreater(
                os.path.getsize(pdf_path), 50000, f"PDF file size too small: {name}"
            )

    def test_13_rate_card_counter_letter_and_audit(self):
        from rate_card_optimizer import RateCardOptimizer

        benchmark = {
            "German Tent Structure (sq ft)": 18.0,
            "P3 LED Video Wall (sq ft)": 120.0,
        }
        optimizer = RateCardOptimizer(benchmark)
        bid = [
            {
                "item_name": "German Tent Structure (sq ft)",
                "quantity": 1000,
                "quoted_unit_rate": 24.0,
            },
            {
                "item_name": "P3 LED Video Wall (sq ft)",
                "quantity": 100,
                "quoted_unit_rate": 160.0,
            },
        ]
        res = optimizer.audit_quotation(bid)
        letter = optimizer.generate_counter_letter(
            res, "Apex Audio Visuals Ltd", "Bengaluru Tech Summit"
        )
        self.assertIn("Apex Audio Visuals Ltd", letter)
        self.assertIn("Bengaluru Tech Summit", letter)
        self.assertIn("Aditya Mehra", letter)
        self.assertIn("+91 99026 21107", letter)
        self.assertGreater(res["percentage_savings"], 20.0)

    def test_14_weekly_showcase_generator(self):
        from portfolio_showcase_generator import generate_weekly_showcase

        generate_weekly_showcase()
        brief_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "reports", "WEEKLY_SHOWCASE_BRIEF.md"
            )
        )
        self.assertTrue(os.path.exists(brief_path))
        with open(brief_path, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("WEEKLY PORTFOLIO & LINKEDIN SHOWCASE BRIEF", content)
        self.assertIn("Aditya Mehra", content)
        self.assertIn("Dayananda Sagar University", content)

    def test_15_bengaluru_career_copilot(self):
        from bengaluru_career_copilot import BengaluruCareerCopilot, StudentProfile

        copilot = BengaluruCareerCopilot()
        student = StudentProfile(
            name="Aditya Mehra",
            degree="BBA International Business",
            college="Dayananda Sagar University",
            graduation_year=2026,
            gpa=8.2,
            skills=["procurement", "supply chain", "excel", "vendor sla"],
            preferred_corridors=["MANYATA"],
        )
        res = copilot.evaluate_student(student, top_n=3)
        self.assertEqual(res["student_name"], "Aditya Mehra")
        self.assertGreater(res["total_opportunities_screened"], 50)
        self.assertGreater(len(res["recommendations"]), 0)
        top_rec = res["recommendations"][0]
        self.assertIn("job_id", top_rec)
        self.assertGreaterEqual(top_rec["student_fit_score"], 60.0)

    def test_16_api_server_endpoints(self):
        from api_server import app
        from starlette.testclient import TestClient

        client = TestClient(app)

        # Test health check
        health_res = client.get("/health")
        self.assertEqual(health_res.status_code, 200)
        self.assertEqual(health_res.json()["status"], "HEALTHY")

        # Test stats
        stats_res = client.get("/api/v1/stats")
        self.assertEqual(stats_res.status_code, 200)
        self.assertIn("total_opportunities", stats_res.json())
        self.assertGreater(stats_res.json()["total_opportunities"], 50)

        # Test jobs listing with filter
        jobs_res = client.get("/api/v1/jobs?min_score=80&limit=5")
        self.assertEqual(jobs_res.status_code, 200)
        self.assertLessEqual(len(jobs_res.json()["jobs"]), 5)

    def test_17_event_logistics_tracker_penalties(self):
        from event_logistics_tracker import EventLogisticsTracker

        tracker = EventLogisticsTracker("Bengaluru Logistics Summit", 500000.0)
        tracker.add_vendor(
            "V-AUDIO",
            "Sound Wave Audio",
            "Audio",
            80000.0,
            hourly_delay_penalty_rate=0.05,
        )
        tracker.record_vendor_delay("V-AUDIO", delay_hours=2.0)
        report = tracker.generate_financial_audit()
        self.assertEqual(report["total_penalties_recovered_inr"], 8000.0)
        self.assertEqual(report["net_final_expenditure_inr"], 72000.0)
        self.assertTrue(report["net_budget_savings_inr"] > 400000.0)

    def test_18_dataset_qa_validator_sla(self):
        from annotation_qa_validator import DatasetQAValidator

        validator = DatasetQAValidator(allowed_classes=["pallet", "forklift", "worker"])
        frames = [
            {
                "frame_id": "F001",
                "annotations": [
                    {"class": "pallet", "bbox": [100, 100, 200, 150]},
                    {"class": "worker", "bbox": [500, 200, 80, 120]},
                ],
            }
        ]
        res = validator.validate_dataset(frames)
        self.assertEqual(res["total_annotations"], 2)
        self.assertEqual(res["defect_count"], 0)
        self.assertEqual(res["qa_compliance_percentage"], 100.0)
        self.assertTrue(res["meets_99_sla"])

    def test_19_api_venture_endpoints(self):
        from api_server import app
        from starlette.testclient import TestClient

        client = TestClient(app)

        # 1. Event logistics audit endpoint
        payload = {
            "event_name": "Aero Logistics 2026",
            "budget_inr": 200000.0,
            "vendors": [
                {
                    "vendor_id": "V1",
                    "name": "Lighting Tech",
                    "category": "Lighting",
                    "contracted_amount": 40000.0,
                    "delay_hours": 1.0,
                }
            ],
        }
        res = client.post("/api/v1/event_logistics/audit", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["total_penalties_recovered_inr"], 2000.0)

        # 2. Dataset QA endpoint
        qa_req = {
            "allowed_classes": ["pallet", "worker"],
            "frames": [
                {
                    "frame_id": "F1",
                    "annotations": [{"class": "pallet", "bbox": [10, 10, 50, 50]}],
                }
            ],
        }
        qa_res = client.post("/api/v1/dataset_qa/validate", json=qa_req)
        self.assertEqual(qa_res.status_code, 200)
        self.assertEqual(qa_res.json()["qa_compliance_percentage"], 100.0)

        # 3. Tailor endpoint
        jobs_res = client.get("/api/v1/jobs?limit=1")
        if jobs_res.json()["count"] > 0:
            sample_jid = jobs_res.json()["jobs"][0]["job_id"]
            tailor_res = client.get(f"/api/v1/jobs/{sample_jid}/tailor")
            self.assertEqual(tailor_res.status_code, 200)
            self.assertIn("recommended_bullets", tailor_res.json())

    def test_20_vault_scale_and_deduplication(self):
        prod_db = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "projects",
                "flagship-career-engine",
                "career_vault.db",
            )
        )
        self.assertTrue(os.path.exists(prod_db))
        vault = CareerVault(prod_db)
        all_jobs = vault.list_jobs(min_score=0)
        vault.close()

        self.assertGreaterEqual(len(all_jobs), 250)
        companies = {j["company"] for j in all_jobs}
        self.assertIn("Goldman Sachs", companies)
        self.assertIn("PhonePe", companies)
        self.assertIn("Walmart Global Tech India", companies)
        self.assertIn("Diageo Global Business Operations", companies)
        self.assertIn("Adobe India", companies)
        self.assertIn("Boeing India", companies)
        self.assertIn("Schneider Electric", companies)
        self.assertIn("Shell India", companies)
        self.assertIn("Tesco Bengaluru", companies)

        # Check unique IDs and URLs
        job_ids = [j["job_id"] for j in all_jobs]
        urls = [j["url"] for j in all_jobs]
        self.assertEqual(
            len(job_ids),
            len(set(job_ids)),
            "Duplicate job_id found in production vault",
        )
        self.assertEqual(
            len(urls), len(set(urls)), "Duplicate URL found in production vault"
        )


if __name__ == "__main__":
    unittest.main()
