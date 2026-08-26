"""
OMEGA CAREER WAR ROOM COMPREHENSIVE TEST SUITE
Tests all 14 engines, pipelines, and zero-delusion invariants:
- Job discovery & verification
- Deduplication hash integrity
- Multi-factor opportunity scoring
- ATS keyword extraction & matching
- Resume engine role variants & zero fabrication
- Application state machine (READY != SUBMITTED)
- Outreach approval gating
- Follow-up scheduling
- STAR interview preparation
- Offer negotiation modeling
- Career analytics & database normalization
- Career War Room Brain master daily loop
"""
import unittest
import sys
import os
import time

sys.path.insert(0, 'E:/anti')

from omega.career_war_room.database import war_room_db
from omega.career_war_room.company_intelligence import company_intelligence
from omega.career_war_room.job_discovery import job_discovery
from omega.career_war_room.job_verification import job_verifier, VerificationStatus
from omega.career_war_room.opportunity_scoring import opportunity_scorer
from omega.career_war_room.ats_engine import ats_engine
from omega.career_war_room.resume_engine import resume_engine, ResumeVariant
from omega.career_war_room.application_manager import application_manager, ApplicationStage
from omega.career_war_room.outreach_engine import outreach_engine, OutreachStatus
from omega.career_war_room.followup_engine import followup_engine
from omega.career_war_room.interview_engine import interview_engine
from omega.career_war_room.offer_engine import offer_engine
from omega.career_war_room.career_analytics import career_analytics
from omega.career_war_room.career_brain import career_war_room_brain

class TestOmegaCareerWarRoom(unittest.TestCase):
    def setUp(self):
        self.db = war_room_db
        self.brain = career_war_room_brain

    def test_01_database_tables_exist(self):
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [r[0] for r in cur.fetchall()]
            required = [
                "companies", "jobs", "contacts", "applications", "outreach",
                "followups", "interviews", "offers", "skills", "documents",
                "model_runs", "tool_runs", "truth_events", "approvals"
            ]
            for t in required:
                self.assertIn(t, tables, f"Mandatory table {t} missing from schema")

    def test_02_company_intelligence_tiers(self):
        companies = company_intelligence.list_companies()
        self.assertGreaterEqual(len(companies), 5)
        amzn = company_intelligence.get_company("COMP-AMZN")
        self.assertIsNotNone(amzn)
        self.assertEqual(amzn["tier"], "TIER_S")
        self.assertTrue(amzn["active_hiring_signal"])
        self.assertTrue("Bangalore" in amzn["bangalore_office"] or "Bengaluru" in amzn["bangalore_office"])

    def test_03_job_verification_and_deduplication(self):
        # 1. Authoritative portal verification
        job_auth = {
            "company_name": "Amazon",
            "role_title": "Global Trade Compliance Analyst",
            "location": "Bengaluru",
            "source": "Amazon Official Jobs Portal",
            "application_url": "https://amazon.jobs/en/jobs/2648192/apply"
        }
        res_auth = job_verifier.verify_job_record(job_auth, live_http_verified=True)
        self.assertEqual(res_auth["status"], VerificationStatus.CONFIRMED_OPENING.value)
        self.assertTrue(res_auth["is_confirmed"])

        # 2. Dedup hash stability
        hash1 = job_verifier.generate_dedup_hash("Amazon", "Trade Analyst", "Bengaluru", "https://amazon.jobs/1")
        hash2 = job_verifier.generate_dedup_hash("Amazon", "Trade Analyst", "Bengaluru", "https://amazon.jobs/1")
        self.assertEqual(hash1, hash2)

    def test_04_opportunity_scoring(self):
        job_sample = {
            "role_title": "Global Trade & Customs Compliance Analyst",
            "category": "SUPPLY_CHAIN_TRADE",
            "location": "Bengaluru, India",
            "skills": ["Customs", "Incoterms 2020", "International Trade", "Logistics"]
        }
        comp = {"tier": "TIER_S"}
        score = opportunity_scorer.calculate_score(job_sample, comp)
        self.assertGreaterEqual(score["opportunity_score"], 80.0)
        self.assertEqual(score["priority_tier"], "HIGH")

    def test_05_ats_engine_matching(self):
        job = {
            "role_title": "Global Trade Compliance Analyst",
            "skills": ["customs clearance", "incoterms 2020", "international trade", "supply chain operations"]
        }
        eval_res = ats_engine.evaluate_job(job)
        self.assertGreaterEqual(eval_res["ats_score"], 80.0)
        self.assertTrue(len(eval_res["strong_matches"]) >= 3)
        self.assertTrue(eval_res["zero_fabrication_guarantee"])

    def test_06_resume_engine_variants_and_integrity(self):
        variants = [
            ResumeVariant.INTERNATIONAL_BUSINESS,
            ResumeVariant.SUPPLY_CHAIN,
            ResumeVariant.OPERATIONS,
            ResumeVariant.BUSINESS_DEVELOPMENT,
            ResumeVariant.MARKETING,
            ResumeVariant.AI_ENABLED_BUSINESS,
            ResumeVariant.MNC_GCC,
            ResumeVariant.GENERAL
        ]
        for v in variants:
            doc = resume_engine.generate_variant(v)
            self.assertEqual(doc["variant_type"], v.value)
            self.assertTrue(doc["zero_fabrication_audit_pass"])
            self.assertIn("Aditya Mehra", doc["content_markdown"])
            self.assertIsNotNone(doc["integrity_hash"])

    def test_07_application_pipeline_truth_invariants(self):
        apps = application_manager.list_applications()
        self.assertGreaterEqual(len(apps), 1)
        
        # Test invariant: SUBMITTED requires real proof ref
        app_id = apps[0]["application_id"]
        res_fail = application_manager.transition_stage(app_id, ApplicationStage.SUBMITTED, proof_ref=None)
        self.assertFalse(res_fail["success"])
        self.assertTrue(res_fail["delusion_prevented"])

        # Test valid submission with proof ref
        res_pass = application_manager.transition_stage(app_id, ApplicationStage.SUBMITTED, proof_ref="PORTAL_RECEIPT_REF_#88921")
        self.assertTrue(res_pass["success"])
        self.assertEqual(res_pass["new_stage"], "SUBMITTED")
        # Clean up / reset to READY to preserve zero-delusion baseline
        application_manager.transition_stage(app_id, ApplicationStage.READY)

    def test_08_outreach_approval_gating(self):
        drafts = outreach_engine.list_outreach(status="DRAFT")
        self.assertGreaterEqual(len(drafts), 1)
        
        target_id = drafts[0]["outreach_id"]
        res = outreach_engine.approve_outreach(target_id, approver="Aditya Mehra")
        self.assertTrue(res["success"])
        self.assertEqual(res["status"], "APPROVED")

    def test_09_followup_and_interview_prep(self):
        # Follow-up
        fols = followup_engine.list_followups()
        self.assertGreaterEqual(len(fols), 1)
        self.assertEqual(fols[0]["cadence_days"], 7)

        # Interview STAR prep
        prep = interview_engine.generate_star_prep("Amazon Global Operations", "Global Trade Analyst")
        self.assertEqual(prep["simulation_readiness"], "VERIFIED_READY")
        self.assertGreaterEqual(len(prep["star_framework_questions"]), 2)

    def test_10_offer_engine_and_career_analytics(self):
        # Offer negotiation
        offer_mock = {
            "company_name": "Amazon",
            "role_title": "Global Trade Compliance Analyst",
            "ctc_annual": 850000.0,
            "base_salary": 650000.0,
            "variable_pay": 100000.0,
            "joining_bonus": 100000.0
        }
        res = offer_engine.analyze_offer(offer_mock)
        self.assertEqual(res["market_competitiveness"], "COMPETITIVE")
        self.assertGreaterEqual(len(res["negotiation_strategy"]), 2)

        # Career analytics
        metrics = career_analytics.get_funnel_metrics()
        self.assertEqual(metrics["jobs_confirmed_openings"], 0) # Reality standard: 0 until live-scraped
        self.assertEqual(metrics["truth_standard"], "STRICT_REALITY_AUDITED")

    def test_11_career_war_room_daily_loop(self):
        loop_res = self.brain.run_daily_loop()
        self.assertEqual(loop_res["status"], "DAILY_LOOP_EXECUTED")
        self.assertEqual(loop_res["total_confirmed_jobs"], 0)
        
        brief = self.brain.get_morning_briefing()
        self.assertIn("OMEGA CAREER WAR ROOM REALITY BRIEFING", brief)

if __name__ == "__main__":
    unittest.main(verbosity=2)
