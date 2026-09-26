"""
Comprehensive Automated Test Suite for ADI CAREER OS Engine (Module 02).
Validates Sales Exclusion, Job Normalization, Deduplication, 100-Point Scoring,
Application Pipeline State Machine, Truth Rule, ATS Matching, Recruiter CRM, and Skill Intelligence.
"""

import os
import sys
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sovereign.career_engine import (
    SalesExclusionEngine,
    JobEntity,
    JobNormalizer,
    JobDeduplicator,
    JobScoringEngine,
    ApplicationRecord,
    ApplicationState,
    InvalidStateTransitionError,
    MissingSubmissionProofError,
    ATSEngine,
    RecruiterCRM,
    RecruiterContact,
    OutreachEngine,
    SkillIntelligenceEngine,
    CareerOrchestrator
)

class TestCareerEngine(unittest.TestCase):

    def test_sales_exclusion_titles(self):
        """Validates that predatory/pure sales titles are strictly disqualified."""
        disqualified_titles = [
            "Business Development Executive (BDE)",
            "Field Sales Executive - Bangalore",
            "Inside Sales Representative",
            "Telecalling Officer / Telecaller",
            "Outbound Telesales Associate"
        ]
        for title in disqualified_titles:
            eval_res = SalesExclusionEngine.evaluate(title=title)
            self.assertTrue(eval_res["is_disqualified"], f"Failed to disqualify title: {title}")
            self.assertGreaterEqual(eval_res["sales_risk_score"], 40)

        # Non-sales operational titles must pass
        safe_titles = [
            "Business Operations Analyst",
            "Junior Business Analyst",
            "Strategy & Operations Associate",
            "Process Improvement Specialist"
        ]
        for title in safe_titles:
            eval_res = SalesExclusionEngine.evaluate(title=title, description="Responsible for Excel reporting, SOP documentation, and workflow analysis.")
            self.assertFalse(eval_res["is_disqualified"], f"Incorrectly disqualified safe title: {title}")
            self.assertLessEqual(eval_res["sales_risk_score"], 20)

    def test_sales_exclusion_description_signals(self):
        """Verifies detection of cold calling, aggressive quotas, and commission-only compensation."""
        desc = "Candidate will perform cold calling 80 leads per day, meet aggressive quarterly sales quota, commission only variable pay."
        eval_res = SalesExclusionEngine.evaluate(title="Client Relationship Coordinator", description=desc, compensation_type="commission based")
        self.assertTrue(eval_res["is_disqualified"])
        self.assertGreaterEqual(eval_res["sales_risk_score"], 60)
        self.assertIn("CRITICAL", eval_res["risk_level"])

    def test_job_normalizer(self):
        """Tests location, experience, and salary normalization."""
        # Location
        self.assertEqual(JobNormalizer.normalize_location("Bangalore Urban"), "Bengaluru, Karnataka, India")
        self.assertEqual(JobNormalizer.normalize_location("Bengaluru, KA"), "Bengaluru, Karnataka, India")

        # Experience
        exp1 = JobNormalizer.normalize_experience("Fresher / Entry Level")
        self.assertTrue(exp1["is_fresher"])
        self.assertEqual(exp1["min"], 0.0)

        exp2 = JobNormalizer.normalize_experience("0 to 2 years experience")
        self.assertEqual(exp2["min"], 0.0)
        self.assertEqual(exp2["max"], 2.0)

        # Salary
        sal1 = JobNormalizer.normalize_salary("₹6.5 LPA - ₹10 LPA")
        self.assertEqual(sal1["currency"], "INR")
        self.assertEqual(sal1["min"], 650000.0)
        self.assertEqual(sal1["max"], 1000000.0)

    def test_job_deduplication(self):
        """Verifies duplicate job detection based on canonical hash and URL."""
        dedup = JobDeduplicator()
        job1 = JobEntity(
            id="JOB-001",
            source="LinkedIn",
            title="Business Operations Analyst",
            description="Process management and analytics.",
            location="Bengaluru",
            company_name="Walmart Global Tech",
            application_url="https://walmart.com/careers/123"
        )
        job2 = JobEntity(
            id="JOB-002",
            source="Naukri",
            title="Business Operations Analyst",
            description="Process management and analytics duplicate.",
            location="Bangalore",
            company_name="Walmart Global Tech",
            application_url="https://walmart.com/careers/123"
        )

        self.assertTrue(dedup.register_job(job1))
        self.assertFalse(dedup.register_job(job2), "Duplicate job was not blocked")

    def test_100_point_scoring_matrix(self):
        """Tests 100-point rubric breakdown and sales risk penalty."""
        job = JobEntity(
            id="JOB-100",
            source="Direct Career Portal",
            title="Business Operations Analyst",
            description="Work with SQL, Excel, and Power BI to improve corporate workflow SOPs. Involves AI automation.",
            location="Bengaluru",
            company_name="Walmart Global Tech",
            salary_min=750000.0,
            experience_min=0.0
        )
        score_eval = JobScoringEngine.score_job(job, sales_risk_score=0)
        self.assertGreaterEqual(score_eval["final_fit_score"], 80.0)
        components = score_eval["components"]
        self.assertIn("role_fit", components)
        self.assertIn("eligibility", components)
        self.assertIn("hiring_probability", components)
        self.assertIn("company_quality", components)

        # Explainability structure
        exp = score_eval["explainability"]
        self.assertIn("why", exp)
        self.assertIn("evidence", exp)
        self.assertIn("recommended_action", exp)
        self.assertEqual(exp["recommended_action"], "PRIORITY_APPLY")

    def test_scoring_sales_penalty(self):
        """Ensures high sales risk significantly penalizes the overall score."""
        job = JobEntity(
            id="JOB-101",
            source="Portal",
            title="Operations Associate",
            description="Cold calling leads and meeting sales quota.",
            location="Bengaluru",
            company_name="Sales Startup"
        )
        score_eval = JobScoringEngine.score_job(job, sales_risk_score=70)
        self.assertLessEqual(score_eval["final_fit_score"], 30.0)

    def test_application_pipeline_valid_lifecycle(self):
        """Tests valid state machine traversal from DISCOVERED to ACCEPTED."""
        app = ApplicationRecord("APP-001", "JOB-100", "Walmart Global Tech", "Business Operations Analyst")
        self.assertEqual(app.current_state, ApplicationState.DISCOVERED)

        app.transition_to(ApplicationState.SHORTLISTED)
        self.assertEqual(app.current_state, ApplicationState.SHORTLISTED)

        app.transition_to(ApplicationState.READY_TO_APPLY)
        self.assertEqual(app.current_state, ApplicationState.READY_TO_APPLY)

        # Transition to APPLIED requires verified submission proof
        app.transition_to(ApplicationState.APPLIED, submission_proof="CONF-WM-99824 Submitted via Workday Portal")
        self.assertEqual(app.current_state, ApplicationState.APPLIED)

        app.transition_to(ApplicationState.SCREENING)
        app.transition_to(ApplicationState.INTERVIEW_1)
        app.transition_to(ApplicationState.FINAL_ROUND)
        app.transition_to(ApplicationState.OFFER)
        app.transition_to(ApplicationState.ACCEPTED)
        self.assertEqual(app.current_state, ApplicationState.ACCEPTED)
        self.assertEqual(len(app.history), 9)

    def test_application_pipeline_invalid_jump(self):
        """Tests that illegal state transitions are blocked."""
        app = ApplicationRecord("APP-002", "JOB-100", "Amazon", "Operations Analyst")
        with self.assertRaises(InvalidStateTransitionError):
            # Cannot skip straight from DISCOVERED to OFFER
            app.transition_to(ApplicationState.OFFER)

    def test_application_truth_rule(self):
        """Section 19: Never mark APPLIED without verified submission evidence."""
        app = ApplicationRecord("APP-003", "JOB-100", "Deloitte", "Strategy Analyst", initial_state=ApplicationState.READY_TO_APPLY)
        with self.assertRaises(MissingSubmissionProofError):
            # Attempting to mark APPLIED with empty proof must fail
            app.transition_to(ApplicationState.APPLIED, submission_proof="")

    def test_ats_engine_profile_selection(self):
        """Verifies profile selection and verified evidence recommendations."""
        # Business Analyst selection
        ba_match = ATSEngine.analyze_match("Junior Business Analyst", "Drafting BRDs, user stories, acceptance criteria, and SQL reporting.")
        self.assertEqual(ba_match["selected_profile"], "business_analyst")
        self.assertGreaterEqual(ba_match["match_percentage"], 80.0)

        # International Trade selection
        trade_match = ATSEngine.analyze_match("EXIM Specialist", "Handling customs documentation, international freight, and port logistics.")
        self.assertEqual(trade_match["selected_profile"], "international_operations")

        # Zero hallucination check: all bullets map to verified EXP ledger
        for rec in ba_match["tailoring_recommendations"]:
            self.assertTrue(rec["experience_id"].startswith("EXP-"))

    def test_recruiter_crm_cooldown(self):
        """Verifies anti-spam cooldown prevents duplicate outreach."""
        crm = RecruiterCRM(cooldown_days=14)
        contact = RecruiterContact(
            contact_id="REC-001",
            full_name="Priya Sharma",
            company="Deloitte",
            title="Lead Recruiter"
        )
        crm.add_contact(contact)

        check1 = crm.can_contact("REC-001")
        self.assertTrue(check1["can_contact"])

        crm.record_outreach("REC-001", "LinkedIn InMail")
        check2 = crm.can_contact("REC-001")
        self.assertFalse(check2["can_contact"])
        self.assertIn("cooldown", check2["reason"].lower())

    def test_outreach_engine(self):
        """Verifies generated messages contain candidate background and role details."""
        msg = OutreachEngine.generate_recruiter_inmail(
            candidate_name="Adi",
            target_company="Walmart Global Tech",
            target_role="Business Operations Analyst",
            recruiter_name="Rahul Verma"
        )
        self.assertIn("Business Operations Analyst", msg)
        self.assertIn("Walmart Global Tech", msg)
        self.assertIn("Rahul", msg)
        self.assertIn("BBA", msg)

    def test_skill_intelligence_ranking(self):
        """Verifies Section 28 priority formula and skill coverage audit."""
        ranked = SkillIntelligenceEngine.get_ranked_skills()
        self.assertEqual(len(ranked), 6)
        self.assertGreater(ranked[0]["priority_score"], 0)

        audit = SkillIntelligenceEngine.audit_job_posting_skills("Requires SQL queries, advanced Excel dashboards, and standard operating procedures (SOPs).")
        self.assertGreaterEqual(audit["skills_in_job_count"], 3)
        self.assertGreaterEqual(audit["candidate_competency_match"], 3)

    def test_career_orchestrator_end_to_end(self):
        """Tests complete pipeline run via CareerOrchestrator."""
        orchestrator = CareerOrchestrator()
        raw_job = {
            "title": "Business Operations Analyst - Global Tech Hub",
            "company": "Walmart Global Tech",
            "location": "Bengaluru",
            "experience": "0-1 years",
            "salary": "₹8.0 LPA",
            "description": "Looking for a Business Operations Analyst to streamline cross-functional SOPs, analyze metrics in SQL and Excel, and automate workflows.",
            "application_url": "https://walmart.com/jobs/99245"
        }
        res = orchestrator.process_job_posting(raw_job)
        self.assertTrue(res["is_new_opportunity"])
        self.assertFalse(res["sales_evaluation"]["is_disqualified"])
        self.assertGreaterEqual(res["scoring"]["final_fit_score"], 80.0)
        self.assertIn("executive_view", res)
        self.assertEqual(res["executive_view"]["next_action"], "PRIORITY_APPLY")

        overview = orchestrator.get_career_overview()
        self.assertEqual(overview["candidate"], "Aditya Mehra (Adi)")

if __name__ == "__main__":
    unittest.main()
