"""
test_apex_career_os.py - Comprehensive Test Suite for APEX CAREER SUPREMACY OS
==============================================================================
Verifies candidate truth integrity, continuous learning vault, job harvesting,
multi-agent tailoring, recruiter search, interview simulation, and cockpit generation.
"""

import os
import pytest
from pathlib import Path

from apex_career_os.core.truth_layer import (
    get_candidate_profile, VERIFIED_EVIDENCE, VERIFIED_CERTIFICATIONS,
    VERIFIED_SKILLS, validate_claim_provenance
)
from apex_career_os.core.knowledge_learning_vault import KnowledgeLearningVault
from apex_career_os.scrapers.multi_portal_harvester import MultiPortalHarvester
from apex_career_os.agents.sentinel_learner import SentinelLearnerAgent
from apex_career_os.agents.truth_tailor import TruthTailorAgent
from apex_career_os.agents.network_strike import NetworkStrikeAgent
from apex_career_os.agents.auto_apply_dispatcher import AutoApplyDispatcherAgent
from apex_career_os.agents.interview_master import InterviewMasterAgent
from apex_career_os.agents.compensation_strategist import CompensationStrategistAgent
from apex_career_os.agents.career_growth_architect import CareerGrowthArchitectAgent
from apex_career_os.orchestrator import ApexCareerOrchestrator
from apex_career_os.ui.cockpit_generator import generate_cockpit_html

def test_truth_layer_integrity():
    profile = get_candidate_profile()
    assert profile.full_name == "Aditya Mehra"
    assert profile.institution == "Dayananda Sagar University (DSU), Bengaluru"
    assert profile.degree == "Bachelor of Business Administration (BBA) - International Business"
    assert "Immediate" in profile.status

    # Assert evidence claims
    assert "EXP-001" in VERIFIED_EVIDENCE
    assert "EXP-004" in VERIFIED_EVIDENCE # Aero India
    assert "EXP-006" in VERIFIED_EVIDENCE # 300+ events, 15% cost savings
    assert "100,000+" in VERIFIED_EVIDENCE["EXP-004"]["metrics"][0]

    # Validate provenance guards
    assert validate_claim_provenance("Delivered 300+ events with 15% cost savings.") is True
    with pytest.raises(ValueError):
        validate_claim_provenance("Graduated from Harvard Business School with honors.")

def test_knowledge_learning_vault(tmp_path):
    test_db = tmp_path / "test_vault.db"
    vault = KnowledgeLearningVault(db_path=test_db)
    
    # Test learning from job
    sample_job = {
        "company": "Titan Scaleup",
        "title": "Vendor Operations Specialist",
        "description": "Lead vendor SLA contracts, procurement negotiation, and supply chain logistics in Bangalore.",
        "location": "Bengaluru",
        "url": "https://careers.titan.com/job123"
    }
    learn_res = vault.learn_from_job_posting(sample_job)
    assert learn_res["status"] == "learned"
    assert learn_res["keywords_extracted"] > 0

    # Test company intelligence retrieval
    intel = vault.get_company_intelligence("Titan Scaleup")
    assert intel is not None
    assert intel["name"] == "Titan Scaleup"
    assert "Active" in intel["hiring_velocity"]

    # Test learning from online snippet
    snippet_res = vault.learn_from_online_snippet(
        "Titan Scaleup",
        "During the interview they asked me: How would you handle a supplier failing 2 hours before an event?",
        source="Glassdoor Review"
    )
    assert snippet_res["questions_learned"] >= 1

    questions = vault.get_interview_questions_for_company("Titan Scaleup")
    assert len(questions) >= 1

def test_multi_portal_harvester():
    harvester = MultiPortalHarvester()
    jobs = harvester.harvest_from_sqlite_master(limit=10)
    assert len(jobs) > 0
    first = jobs[0]
    assert "id" in first
    assert "title" in first
    assert "company" in first
    assert "track" in first
    assert "salary_estimate" in first

def test_truth_tailor_agent():
    tailor = TruthTailorAgent()
    job = {
        "id": "JOB-TEST01",
        "company": "Amazon",
        "title": "Operations Specialist",
        "description": "Manage vendor SLAs, high-stakes logistics, and procurement cost optimization.",
        "track": "Operations & Vendor Governance"
    }
    match_eval = tailor.evaluate_ats_match(job)
    assert match_eval["match_score_percent"] >= 75.0
    assert len(match_eval["matched_skills"]) > 0

    resume_md = tailor.generate_tailored_resume(job, output_format="markdown")
    assert "ADITYA MEHRA" in resume_md
    assert "AERO INDIA 2025" in resume_md
    assert "Amazon" in resume_md

    cover_letter = tailor.generate_cover_letter(job)
    assert "Amazon" in cover_letter
    assert "Dayananda Sagar University" in cover_letter

    pitches = tailor.generate_elevator_pitches(job)
    assert "30_second_phone_screen" in pitches
    assert "linkedin_connection_note" in pitches

def test_network_strike_agent():
    network = NetworkStrikeAgent()
    recruiters = network.find_recruiters_for_company("Accenture", limit=3)
    assert len(recruiters) > 0
    rec = recruiters[0]
    assert "name" in rec
    assert "email" in rec

    outreach = network.generate_outreach_dossier({"company": "Accenture", "title": "Operations Analyst"}, contact=rec)
    assert "stage_1_cold_email" in outreach
    assert "stage_2_followup" in outreach
    assert "warm_referral_request" in outreach
    assert "Accenture" in outreach["stage_1_cold_email"]

def test_auto_apply_dispatcher():
    dispatcher = AutoApplyDispatcherAgent()
    job = {
        "id": "JOB-TEST-AUTO",
        "company": "Zepto",
        "title": "Operations Associate",
        "track": "Operations",
        "url": "https://zepto.com/jobs/123"
    }
    payload = dispatcher.generate_ats_payload(job)
    assert payload["candidate_info"]["first_name"] == "Aditya"
    assert payload["screening_responses"]["notice_period"] == "0 Days (Immediate Joiner)"

    reg = dispatcher.register_application(job, initial_stage="TAILORED")
    assert reg["status"] == "UPDATED"
    assert reg["stage"] == "TAILORED"

def test_interview_master_agent():
    interview = InterviewMasterAgent()
    prep = interview.generate_interview_prep_pack("Deloitte", "Advisory Analyst")
    assert prep["target_company"] == "Deloitte"
    assert len(prep["tailored_qa_bank"]) > 0
    assert len(prep["curveball_defenses"]) > 0

def test_compensation_and_growth_agents():
    comp = CompensationStrategistAgent()
    bench = comp.benchmark_role_compensation("Operations & Vendor Governance")
    assert bench["median_p50_lpa"] > 0
    playbook = comp.generate_negotiation_playbook("Deloitte", offered_ctc_lpa=6.0, target_ctc_lpa=8.0)
    assert "verbal_phone_counter_script" in playbook

    growth = CareerGrowthArchitectAgent()
    blueprint = growth.generate_30_60_90_day_blueprint("Deloitte", "Operations Analyst")
    assert "day_1_to_30_listen_and_map" in blueprint
    ladder = growth.generate_5_year_career_ladder()
    assert len(ladder["phases"]) == 3

def test_orchestrator_and_cockpit_generation(tmp_path):
    orch = ApexCareerOrchestrator()
    instant = orch.execute_instant_strike_for_custom_role(
        company="Goldman Sachs",
        title="Operations Analyst",
        description="Global market operations, trade reconciliation, and vendor SLAs.",
        track="Operations & Vendor Governance"
    )
    assert instant["ats_evaluation"]["match_score_percent"] >= 75.0
    assert len(instant["recruiters"]) > 0

    # Test Cockpit generation
    mock_telemetry = {
        "cycle_timestamp": "2026-10-21T12:00:00",
        "total_jobs_evaluated": 1,
        "top_tier_matches": 1,
        "kanban_pipeline": {"stages": {"TAILORED": [{"title": "Operations Analyst", "company": "Goldman Sachs"}]}},
        "trending_skills": [{"keyword": "Operations", "category": "Operations", "occurrence_count": 10}],
        "opportunities": [instant]
    }
    out_html = tmp_path / "test_cockpit.html"
    res_path = generate_cockpit_html(mock_telemetry, output_path=out_html)
    assert Path(res_path).exists()
    assert Path(res_path).stat().st_size > 1000
