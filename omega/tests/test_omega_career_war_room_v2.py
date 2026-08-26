"""
OMEGA CAREER WAR ROOM v2 COMPREHENSIVE TEST SUITE
Tests:
- Job truth auditor with cryptographic evidence hashing
- Job change detection & truth event logging
- Application proof audit & automatic downgrade of unverified submissions
- 20 confirmed Bangalore GCC & MNC opportunities
- Contact intelligence & outreach proof enforcement
- Call preparation assistant with objection defense
- 365-day radar automation proof logging
"""
import unittest
import sys
import os
import time

sys.path.insert(0, 'E:/anti')

from omega.career_war_room.database import war_room_db
from omega.career_war_room.job_discovery import job_discovery
from omega.career_war_room.job_truth_auditor import job_truth_auditor
from omega.career_war_room.application_proof import application_proof_engine
from omega.career_war_room.contact_intelligence import contact_intelligence
from omega.career_war_room.call_assistant import call_assistant
from omega.career_war_room.radar_365 import radar_365
from omega.career_war_room.application_manager import application_manager, ApplicationStage

class TestOmegaCareerWarRoomV2(unittest.TestCase):
    def setUp(self):
        self.db = war_room_db

    def test_01_twenty_confirmed_opportunities(self):
        jobs = job_discovery.list_jobs(confirmed_only=True, limit=50)
        self.assertEqual(len(jobs), 20, f"Expected 20 confirmed opportunities, found {len(jobs)}")
        
        # Verify all have valid application URLs and positive ECV scores
        for j in jobs:
            self.assertEqual(j["verification_status"], "CONFIRMED_OPENING")
            self.assertTrue(j["application_url"].startswith("http"))
            self.assertGreater(j["opportunity_score"], 70.0)

    def test_02_job_truth_auditor_evidence_hashing(self):
        audit_res = job_truth_auditor.audit_all_jobs()
        self.assertEqual(audit_res["status"], "JOB_TRUTH_AUDIT_COMPLETE")
        self.assertEqual(audit_res["total_jobs_audited"], 20)
        self.assertEqual(audit_res["confirmed_openings"], 20)
        
        # Verify evidence hashes are valid 64-char SHA-256 strings
        for rec in audit_res["audit_records"]:
            self.assertEqual(len(rec["evidence_hash"]), 64)

    def test_03_application_proof_downgrade_mechanism(self):
        # 1. Insert an unverified SUBMITTED application (missing proof)
        unverified_app_id = "APP-TEST-UNVERIFIED"
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT OR REPLACE INTO applications (
                application_id, job_id, company_name, role_title, current_stage,
                resume_variant, custom_notes, ats_score, submission_proof_ref,
                submitted_at, source, verification_status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                unverified_app_id, "JOB-AMZN-001", "Amazon Global Operations",
                "Global Trade Compliance Analyst", "SUBMITTED",
                "INTERNATIONAL_BUSINESS", "Unverified test application", 90.0,
                None, None, "TestRunner", "UNVERIFIED",
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            ))
            conn.commit()

        # 2. Run proof audit
        audit_res = application_proof_engine.audit_application_proofs()
        self.assertGreaterEqual(audit_res["downgraded_unverified"], 1)

        # 3. Verify the application was downgraded to READY
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT current_stage FROM applications WHERE application_id = ?", (unverified_app_id,))
            row = cur.fetchone()
            self.assertEqual(row["current_stage"], "READY")

    def test_04_application_proof_artifact_generation(self):
        proof = application_proof_engine.create_proof_artifact(
            "APP-AMZN-001", "Amazon Global Operations", "Global Trade Analyst", "CONF_PORTAL_#8921"
        )
        self.assertTrue(proof["is_valid"])
        self.assertEqual(len(proof["evidence_artifact_hash"]), 64)
        self.assertIn("Amazon", proof["provider_source"])

    def test_05_contact_intelligence_truth(self):
        contacts = contact_intelligence.list_contacts()
        self.assertGreaterEqual(len(contacts), 3)
        amzn_contacts = contact_intelligence.list_contacts("Amazon")
        self.assertGreaterEqual(len(amzn_contacts), 1)
        self.assertEqual(amzn_contacts[0]["verification_status"], "VERIFIED")

    def test_06_call_preparation_assistant(self):
        brief = call_assistant.generate_call_briefing(
            "Amazon Global Operations", "Priya Sharma", "Senior Recruiter", "Global Trade Compliance Analyst"
        )
        self.assertEqual(brief["status"], "PREPARED")
        self.assertTrue(brief["human_authorization_required"])
        self.assertIn("Aditya Mehra", brief["elevator_opening"])
        self.assertIn("Customs", brief["talking_points"][0])
        self.assertIn("Experience Level", brief["objection_defense"])

    def test_07_radar_365_automation_proof_logging(self):
        run_proof = radar_365.execute_scheduled_radar_run()
        self.assertEqual(run_proof["status"], "SUCCESS")
        self.assertGreater(run_proof["items_processed"], 20)
        self.assertTrue(os.path.exists(radar_365.proof_log_path))

if __name__ == "__main__":
    unittest.main(verbosity=2)
