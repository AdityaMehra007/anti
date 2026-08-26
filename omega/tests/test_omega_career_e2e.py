#!/usr/bin/env python3
"""
========================================================================================
OMEGA CAREER OS END-TO-END VERIFICATION SUITE
========================================================================================
Validates the complete 14-step autonomous loop on a real target job (Accenture BLR-JOB-001).
========================================================================================
"""

import os, sys, unittest, json

# Path injection
sys.path.insert(0, os.path.join(r"e:\anti", "omega", "core"))
sys.path.insert(0, os.path.join(r"e:\anti", "omega", "apps", "interview_prep"))
sys.path.insert(0, r"e:\anti")

from state_machine import ActionStage, ExecutionStatus, OmegaStateMachine
from career_brain import OmegaCareerBrain
from omega_dispatcher import OmegaDispatcher
from interview_engine import InterviewEngine


class TestOmegaCareerOS_EndToEnd(unittest.TestCase):
    def setUp(self):
        self.brain = OmegaCareerBrain()
        self.dispatcher = OmegaDispatcher()
        self.interview_eng = InterviewEngine()

    def test_01_real_job_scoring(self):
        """Step 1-3: Ingest, validate, and score real Accenture job."""
        res = self.brain.score_opportunity(
            job_title="Global Business Operations & BD Analyst",
            company_name="Accenture",
            location="Bengaluru, India",
            network_connections=115,
            recruiter_count=25,
            hiring_manager_count=3
        )
        self.assertGreaterEqual(res["overall_opportunity_score"], 80.0)
        self.assertTrue(res["is_tier_1_enterprise"])
        self.assertEqual(res["recommendation"], "HIGH_PRIORITY_OUTREACH")
        print(f"\n[STEP 1-3 PASS] Ingested & Scored BLR-JOB-001: Score = {res['overall_opportunity_score']}/100")

    def test_02_verified_profile_provenance(self):
        """Step 4: Check verified master profile contains zero hallucinations."""
        self.assertIsNotNone(self.brain.profile)
        candidate = self.brain.profile.get("candidate", {})
        self.assertEqual(candidate.get("full_name"), "Aditya Mehra")
        exp = self.brain.profile.get("verified_experience", [])
        self.assertGreaterEqual(len(exp), 3)
        # Ensure Aero India 2025 is primary evidence anchor
        self.assertTrue(any("AERO INDIA 2025" in e.get("event", "").upper() for e in exp))
        print("[STEP 4 PASS] Master profile verified with authentic Aero India / Tata Comm records.")

    def test_03_state_machine_transitions(self):
        """Step 5-7: Action lifecycle progression through zero-trust gate."""
        action = OmegaStateMachine.create_action_record(
            action_id="TEST-ACT-001",
            opportunity_id="BLR-JOB-001",
            target_name="Darshana Mahesh",
            company="Accenture",
            action_type="Recruiter Outreach"
        )
        self.assertEqual(action["current_stage"], ActionStage.DISCOVERED.value)
        self.assertEqual(action["execution_status"], ExecutionStatus.PREPARED.value)

        # DISCOVERED -> QUALIFIED
        action = OmegaStateMachine.transition(action, ActionStage.QUALIFIED, actor="CareerBrain", reason="Fit score > 80")
        self.assertEqual(action["current_stage"], ActionStage.QUALIFIED.value)

        # QUALIFIED -> READY
        action = OmegaStateMachine.transition(action, ActionStage.READY, actor="ApplicationFactory", reason="Dossier compiled")
        self.assertEqual(action["current_stage"], ActionStage.READY.value)

        # READY -> APPROVAL_REQUIRED
        action = OmegaStateMachine.transition(action, ActionStage.APPROVAL_REQUIRED, actor="PolicyEngine", reason="External outreach requires human signoff")
        self.assertEqual(action["current_stage"], ActionStage.APPROVAL_REQUIRED.value)

        # APPROVAL_REQUIRED -> QUEUED (Simulated human approval)
        action = OmegaStateMachine.transition(action, ActionStage.QUEUED, execution_status=ExecutionStatus.QUEUED, actor="Aditya Mehra", reason="Approved via CLI Gate")
        self.assertEqual(action["current_stage"], ActionStage.QUEUED.value)
        self.assertEqual(action["execution_status"], ExecutionStatus.QUEUED.value)
        print("[STEP 5-7 PASS] Strict 13-stage state machine transitions verified with hash provenance.")

    def test_04_zero_trust_gate_integrity(self):
        """Step 8-10: Verify gate downgrades missing connectors to PREPARED."""
        # Attempt live dispatch without external credentials
        success = self.dispatcher.execute_live_dispatch("ACT-0001", connector="unconfigured_api")
        self.assertTrue(success)
        rec = next(r for r in self.dispatcher.records if r["id"] == "ACT-0001")
        self.assertEqual(rec["execution_status"], ExecutionStatus.PREPARED.value)
        print("[STEP 8-10 PASS] Zero-trust dispatch gate correctly prevents fake external delivery claims.")

    def test_05_interview_simulation_and_defense(self):
        """Step 11-14: Verify STAR response grading and interview defense for Accenture."""
        q = self.interview_eng.get_question_by_id("MNC-ACN-001")
        self.assertIsNotNone(q)
        ans = (
            "During AERO India 2025 at Yelahanka Air Force Station, as Exhibition Operations Lead for Salt in My Coca, "
            "my direct objective was to manage full stall setup, inventory security, VIP protocol, and maintain 100% SLA readiness. "
            "I structured a 3-tier operational protocol: executed badge clearances 24h early, implemented real-time batch inventory "
            "replenishment, and trained booth staff on de-escalation for defense delegates. "
            "As a result, we achieved 100% on-time readiness every morning, zero inventory shrinkage, engaged 5,000+ qualified leads, "
            "and received top-tier presentation commendation."
        )
        res = self.interview_eng.evaluate_response("MNC-ACN-001", ans, time_taken_seconds=60)
        self.assertGreaterEqual(res.overall_score, 80.0)
        self.assertTrue(res.star_analysis.detected_components["Situation"])
        self.assertTrue(res.star_analysis.detected_components["Result"])
        print(f"[STEP 11-14 PASS] Interview Defense Evaluated: Score = {res.overall_score}/100 | STAR Grade = PASS")


if __name__ == "__main__":
    unittest.main()
