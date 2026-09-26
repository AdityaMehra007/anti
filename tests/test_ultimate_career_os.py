import os
import sys
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.job_matching_100pt import JobMatching100Engine
from core.ats_optimizer import ATSOptimizer
from core.skill_gap_engine import SkillGapEngine
from core.interview_engine_30q import InterviewEngine30Q
from core.resume_vault import ResumeVault
from core.daily_cadence import DailyCadenceEngine
from core.career_copilot import CareerCopilot
from adi_career_os_ultimate import UltimateCareerOS

@pytest.fixture
def sample_job():
    return {
        "id": "BLR-TEST-001",
        "company": "Accenture India",
        "title": "Global Business Operations & BD Analyst",
        "location": "Bengaluru (Bellandur / Ecospace)",
        "experience": "Fresher / 0-2 Yrs",
        "skills": "Business Operations, Process Mapping, Vendor SLAs, Excel Modeling, Incoterms 2020",
        "url": "https://www.accenture.com/in-en/careers"
    }

def test_100_point_matching_engine(sample_job):
    res = JobMatching100Engine.compute_match_score(sample_job)
    assert "match_score" in res
    assert res["match_score"] >= 90.0, "Accenture role should score in Tier 1 Priority"
    assert "interview_probability" in res
    assert "career_roi_score" in res
    assert "transit_corridor" in res
    assert res["commute_friction_penalty"] > 0
    assert "breakdown" in res
    assert len(res["breakdown"]) == 11

def test_ats_optimizer(sample_job):
    profile = {"candidate": {"full_name": "Aditya Mehra"}}
    res = ATSOptimizer.optimize_for_job(sample_job, profile)
    assert res["ats_score"] >= 80.0
    assert len(res["matched_keywords"]) > 0
    assert "why_this_job" in res
    assert "why_me" in res
    assert "what_to_change_before_applying" in res
    assert res["formatting_status"] == "Harvard 1-Page ATS Standard Compliant"

def test_skill_gap_engine():
    res = SkillGapEngine.audit_profile_against_role("Global Business Operations Analyst")
    assert "readiness_badges" in res
    assert len(res["readiness_badges"]["green"]) >= 5
    assert len(res["readiness_badges"]["yellow"]) >= 3
    assert len(res["readiness_badges"]["red"]) >= 2
    assert len(res["seven_day_high_impact_plan"]) == 4
    assert len(res["thirty_day_skill_plan"]) == 4
    assert len(res["ninety_day_career_compounding_plan"]) == 3

def test_interview_engine_30q():
    res = InterviewEngine30Q.get_compendium()
    assert res["total_questions"] == 30
    assert len(res["questions"]) == 30
    assert "Aero_India_Queue_Triage" in res["star_frameworks"]
    assert "Puma_Brand_Activation_SLA" in res["star_frameworks"]
    assert "Instawork_AI_Precision" in res["star_frameworks"]

def test_resume_vault():
    variants = ResumeVault.list_variants()
    assert len(variants) == 12, "Must provide exactly 12 specialized resume variants"
    v1 = ResumeVault.get_variant("1")
    assert v1["key"] == "master_operations"
    assert "Aero India" in v1["summary"]
    v4 = ResumeVault.get_variant("exim_trade_ops")
    assert "Incoterms 2020" in v4["summary"]

def test_daily_cadence(sample_job):
    brief = DailyCadenceEngine.generate_morning_brief([sample_job], {"health_score": 96})
    assert brief["briefing_type"] == "MORNING_JOB_BRIEF"
    assert len(brief["top_3_must_do_actions"]) == 3
    assert "strategic_insight" in brief
    
    retro = DailyCadenceEngine.generate_evening_review({"completed_applications": 61})
    assert retro["review_type"] == "EVENING_DAILY_RETRO"
    assert "biggest_bottleneck" in retro

def test_career_copilot():
    act = CareerCopilot.what_should_i_do_next()
    assert "action_title" in act
    assert "step_1" in act
    assert "urgency" in act
    
    ans = CareerCopilot.answer_query("Which jobs should I apply to today?")
    assert "recommendation" in ans
    assert "Accenture" in ans["recommendation"]

def test_master_orchestrator_payload():
    os_engine = UltimateCareerOS()
    payload = os_engine.get_full_dashboard_payload()
    assert payload["health_score"] >= 90
    assert len(payload["top_openings"]) >= 5
    assert len(payload["resume_variants"]) == 12
    assert len(payload["bangalore_agencies"]) == 15
    assert len(payload["funded_startups_and_global_mncs"]) >= 40
    assert "emergency_mode" in payload["modes"]
    assert "premium_mode" in payload["modes"]

def test_bangalore_agencies_subsystem():
    from scripts.apply_all_agencies_bangalore import load_agencies, generate_agency_emails, export_csv
    agencies = load_agencies()
    assert len(agencies) == 15, "Expected 15 top Bangalore recruitment agencies"
    for a in agencies:
        assert a["portal_url"].startswith("http")
        assert "@" in a["email"]
        assert "Bengaluru" in a["location"] or "Bangalore" in a["location"]
    
    eml_count = generate_agency_emails(agencies)
    assert eml_count == 15
    
    csv_file = export_csv(agencies)
    assert csv_file.exists()
    assert csv_file.stat().st_size > 500

def test_funded_startups_and_global_mncs_subsystem():
    from scripts.compile_funded_startups_and_global_mncs import load_directory, export_csv
    companies = load_directory()
    assert len(companies) >= 40, "Expected at least 40 verified funded startups & global MNCs"
    
    for c in companies:
        assert c["company_name"], "Missing company name"
        assert c["direct_apply_url"].startswith("http"), "Invalid direct apply URL"
        assert "@" in c["hr_email"], f"Invalid HR email for {c['company_name']}"
        assert c["sales_risk"] is False, f"Sales risk violation in {c['company_name']}"
        if c.get("id", "").startswith("MASS-"):
            assert c["total_ctc_min"] >= 3.5, f"Compensation below mass hiring floor for {c['company_name']}"
            assert c["monthly_in_hand_est"] >= 25000, f"In-hand monthly below mass floor for {c['company_name']}"
        else:
            assert c["total_ctc_min"] >= 5.0, f"Compensation below fresh graduate floor for {c['company_name']}"
            assert c["monthly_in_hand_est"] > 30000, f"In-hand monthly below minimum for {c['company_name']}"

    csv_count = export_csv()
    assert csv_count >= 40

def test_mass_and_bulk_hiring_subsystem():
    from scripts.compile_mass_and_bulk_hiring import load_mass_hiring, export_mass_csv
    companies = load_mass_hiring()
    assert len(companies) >= 15, "Expected at least 15 verified mass & bulk hiring giants"
    
    for c in companies:
        assert c["company_name"], "Missing company name"
        assert c["direct_apply_url"].startswith("http"), "Invalid apply URL"
        assert "@" in c["hr_email"], f"Invalid HR email for {c['company_name']}"
        assert c["sales_risk"] is False, f"Sales risk violation in {c['company_name']}"
        b = c.get("benefits_package", {})
        assert b.get("transport"), f"Missing transport benefit in {c['company_name']}"
        assert b.get("medical_insurance"), f"Missing medical insurance in {c['company_name']}"
        assert b.get("shift_allowance"), f"Missing shift allowance in {c['company_name']}"

    csv_count = export_mass_csv()
    assert csv_count >= 15

def test_mega_4500_non_stop_outreach_subsystem():
    from pathlib import Path
    import json
    root = Path(__file__).resolve().parent.parent
    master_json = root / "data" / "bangalore_4500_companies_master.json"
    master_csv = root / "BANGALORE_4500_ALL_COMPANIES_NON_STOP_OUTREACH.csv"
    launcher_bat = root / "LAUNCH_NON_STOP_OUTREACH.bat"
    studio_html = root / "apps" / "job_application_studio" / "bangalore_non_stop_outreach_studio.html"

    assert master_json.exists(), "Missing bangalore_4500_companies_master.json"
    assert master_csv.exists(), "Missing BANGALORE_4500_ALL_COMPANIES_NON_STOP_OUTREACH.csv"
    assert launcher_bat.exists(), "Missing LAUNCH_NON_STOP_OUTREACH.bat"
    assert studio_html.exists(), "Missing bangalore_non_stop_outreach_studio.html"

    companies = json.loads(master_json.read_text(encoding="utf-8"))
    assert len(companies) == 4500, f"Expected exactly 4500 companies, found {len(companies)}"

    # Audit random samples for strict compliance
    for c in companies[:50]:
        assert c["company"], "Missing company name"
        assert "@" in c["hr_email"], f"Invalid HR email in {c['company']}"
        assert c["phone"].startswith("+91-80"), f"Invalid phone format in {c['company']}"
        assert c["target_role"], f"Missing target role in {c['company']}"
        assert "sales executive" not in c["target_role"].lower(), f"Sales violation in {c['company']}"
        assert "cold calling" not in c["target_role"].lower(), f"Sales violation in {c['company']}"

    # Verify CSV has header + 4500 data rows
    with open(master_csv, "r", encoding="utf-8-sig") as f:
        rows = list(f)
        assert len(rows) >= 4501, f"Expected at least 4501 lines in CSV, found {len(rows)}"


