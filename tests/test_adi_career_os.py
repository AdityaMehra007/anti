import os
import sys
import pytest
from pathlib import Path

# Ensure root is on pythonpath
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from adi_career_os import (
    load_verified_profile,
    JobHunter,
    JobValidator,
    JobScorer,
    CompanyIntelligence,
    CVCommander,
    ApplicationManager,
    RecruiterHunter,
    NetworkingManager,
    InterviewCoach,
    InterviewSimulator,
    SkillArchitect,
    PortfolioBuilder,
    CareerAnalyst,
    OpportunityScout,
    ExecutiveCareerStrategist,
    AdiCareerOS
)

@pytest.fixture
def sample_jobs():
    return [
        {
            "Job ID": "BLR-TEST-001",
            "Company": "Accenture India",
            "Role": "Global Business Operations & BD Analyst",
            "Location": "Bengaluru / Bangalore",
            "Remote": "Hybrid / On-site",
            "Experience": "Fresher / 0-2 Yrs",
            "Salary": "Market Competitive",
            "Skills": "Business Operations, International Business, Consulting, Client Management",
            "Match Score": "92",
            "Status": "DRAFT_READY"
        },
        {
            "Job ID": "BLR-TEST-002",
            "Company": "Pure Cold Call Sales Org",
            "Role": "Telecalling SDR Outbound Sales Executive",
            "Location": "Bengaluru / Bangalore",
            "Remote": "On-site",
            "Experience": "0-1 Yrs",
            "Salary": "Commission Based",
            "Skills": "Cold Calling, Telecalling, SDR, Outbound Lead Generation",
            "Match Score": "30",
            "Status": "DRAFT_READY"
        },
        {
            "Job ID": "BLR-TEST-003",
            "Company": "Amazon Bangalore",
            "Role": "Operations & Vendor Management Executive",
            "Location": "Bengaluru",
            "Remote": "On-site",
            "Experience": "Fresher / 0-2 Yrs",
            "Salary": "Market Competitive",
            "Skills": "Operations, Vendor Management, SLA Governance",
            "Match Score": "91",
            "Status": "DRAFT_READY"
        },
        {
            "Job ID": "BLR-TEST-004",
            "Company": "AI Tech Labs",
            "Role": "AI Data Operations & Quality Analyst",
            "Location": "Bengaluru",
            "Remote": "Remote",
            "Experience": "0-2 Yrs",
            "Salary": "8.0 LPA",
            "Skills": "AI, Data Ops, Annotation, Quality Assurance",
            "Match Score": "90",
            "Status": "DRAFT_READY"
        }
    ]


def test_verified_profile_loading():
    profile = load_verified_profile()
    assert "Aditya Mehra" in profile.get("name", profile.get("candidate", {}).get("full_name", ""))
    assert "BBA" in profile.get("education", profile.get("candidate", {}).get("education", ""))
    assert len(profile.get("verified_experience", [])) >= 3


def test_job_hunter_scan_and_filters(sample_jobs):
    hunter = JobHunter(sample_jobs)
    
    # All jobs
    all_res = hunter.scan()
    assert len(all_res) == 4
    
    # Category filter
    ai_res = hunter.scan(category="ai")
    assert len(ai_res) == 1
    assert ai_res[0]["Job ID"] == "BLR-TEST-004"
    
    ops_res = hunter.scan(category="ops")
    assert len(ops_res) >= 2
    
    # MNC filter
    mnc_res = hunter.scan(mnc_only=True)
    assert any("Accenture" in j["Company"] for j in mnc_res)
    assert any("Amazon" in j["Company"] for j in mnc_res)

    # Channel query generator
    queries = hunter.generate_channel_queries("Operations Analyst", "Bengaluru")
    assert "LinkedIn" in queries
    assert "linkedin.com" in queries["LinkedIn"]
    assert "Indeed" in queries
    assert "Google Jobs" in queries


def test_job_validator(sample_jobs):
    validator = JobValidator()
    
    # Valid job
    is_valid, reasons = validator.validate(sample_jobs[0])
    assert is_valid is True
    assert len(reasons) == 0

    # Sales exclusion job
    is_valid_sales, sales_reasons = validator.validate(sample_jobs[1])
    assert is_valid_sales is False
    assert any("sales exclusion" in r.lower() for r in sales_reasons)

    # Invalid location job
    bad_loc_job = {"Company": "XYZ", "Role": "Analyst", "Location": "Tokyo", "Skills": "Ops"}
    is_valid_loc, loc_reasons = validator.validate(bad_loc_job)
    assert is_valid_loc is False
    assert any("unverified location" in r.lower() for r in loc_reasons)


def test_job_scorer_10_factor(sample_jobs):
    scorer = JobScorer()
    
    # Good operations role
    res = scorer.score(sample_jobs[0], recruiter_count=5)
    assert res["score"] >= 80.0
    assert res["priority"] == "P0 - High Fit"
    assert res["is_sales_excluded"] is False
    assert "role_fit" in res["components"]
    assert "commute_score" in res["components"]
    assert "network_access" in res["components"]
    
    # Pure sales role
    res_sales = scorer.score(sample_jobs[1])
    assert res_sales["is_sales_excluded"] is True
    assert res_sales["priority"] == "EXCLUDE"
    assert res_sales["score"] <= 35.0


def test_company_intelligence():
    intel = CompanyIntelligence()
    
    accenture = intel.inspect("Accenture India")
    assert "Bellandur" in accenture["corridor"] or "Whitefield" in accenture["corridor"]
    assert "Tier-1" in accenture["tier"]

    generic = intel.inspect("Unknown Startup XYZ")
    assert "Bengaluru" in generic["corridor"] or "Bangalore" in generic["corridor"]


def test_cv_commander_recommendations():
    cv = CVCommander()
    
    # Operations
    rec_ops = cv.recommend_variant("Operations Lead & Run-of-Show Coordinator", "Vendor governance, SLA")
    assert rec_ops["recommended_code"] in ["A", "B"]
    
    # AI Data
    rec_ai = cv.recommend_variant("AI Data Operations Specialist", "Annotation, model evaluation, precision")
    assert rec_ai["recommended_code"] == "C"

    # Supply Chain
    rec_sc = cv.recommend_variant("Global Trade & EXIM Compliance Associate", "Incoterms, customs clearance, freight")
    assert rec_sc["recommended_code"] == "D"

    # Risk / Compliance
    rec_risk = cv.recommend_variant("Risk & Compliance Advisory Analyst", "Audit, regulatory, governance, due diligence")
    assert rec_risk["recommended_code"] == "E"


def test_application_manager_approval_gate(tmp_path):
    test_db = tmp_path / "test_approvals.db"
    mgr = ApplicationManager(approvals_db=test_db)
    
    # Request approval
    app_id = mgr.request_submission_approval("BLR-TEST-999", "Target Company", "Analyst")
    assert app_id.startswith("APP-REQ-BLR-TEST-999")
    
    # Queue check
    queue = mgr.get_approval_queue()
    assert len(queue) == 1
    assert queue[0]["target_system"] == "Target Company"
    assert queue[0]["status"] == "PENDING_APPROVAL"
    
    # Approve
    ok = mgr.approve("BLR-TEST-999", approver="Aditya Mehra")
    assert ok is True
    
    # Re-check queue (should be empty now)
    assert len(mgr.get_approval_queue()) == 0


def test_recruiter_hunter():
    rh = RecruiterHunter()
    # If file exists, find recruiter should return list
    recs = rh.find_recruiters("Accenture")
    assert isinstance(recs, list)
    
    url = rh.generate_search_url("Goldman Sachs", "Campus Recruiter")
    assert "linkedin.com/search/results/people" in url
    assert "Goldman+Sachs" in url


def test_networking_manager_cadence():
    net = NetworkingManager()
    cadence = net.draft_cadence("Ananya Sharma", "Accenture", "Operations Analyst")
    assert len(cadence) == 4
    assert cadence[0]["touch"] == 1
    assert "Aero India 2025" in cadence[0]["body"]
    assert "Ananya" in cadence[0]["body"]
    assert cadence[3]["touch"] == 4


def test_interview_coach_and_simulator():
    coach = InterviewCoach()
    sheet = coach.get_prep_sheet("Deloitte", "Advisory Analyst")
    assert len(sheet["core_behavioral_stories"]) >= 3
    assert len(sheet["reverse_interview_questions"]) >= 2
    
    sim = InterviewSimulator()
    # Good quantified answer
    good_ans = ("At Aero India 2025, I led operations for Salt in My Coca across 100k+ attendees, "
                "enforcing Tier-1 vendor SLA governance with zero shrinkage and 100% on-time opening.")
    res = sim.evaluate_answer("Tell me about a project", good_ans)
    assert res["total_score"] >= 60
    
    # Poor answer
    bad_ans = "I did stuff and worked hard."
    bad_res = sim.evaluate_answer("Tell me about a project", bad_ans)
    assert bad_res["passed"] is False
    assert len(bad_res["feedback"]) > 0


def test_skill_architect_and_portfolio():
    arch = SkillArchitect()
    assert len(arch.SKILL_MATRIX) >= 5
    roadmap = arch.generate_roadmap()
    assert "7_day_plan" in roadmap
    assert "14_day_plan" in roadmap
    assert "30_day_plan" in roadmap

    pb = PortfolioBuilder()
    projects = pb.get_projects()
    assert len(projects) >= 4
    ops_proj = pb.get_projects("Operations")
    assert len(ops_proj) >= 1


def test_career_analyst_and_strategist(sample_jobs):
    analyst = CareerAnalyst()
    metrics = analyst.analyze(sample_jobs, [])
    assert metrics["funnel"]["total_opportunities_discovered"] == 4
    assert metrics["average_match_score"] > 0
    assert "primary_bottleneck" in metrics

    strat = ExecutiveCareerStrategist()
    plan = strat.get_plan()
    assert len(plan) == 3
    assert "Year 1" in plan[0]["stage"]
    assert "Year 2" in plan[1]["stage"]
    assert "Year 3" in plan[2]["stage"]


def test_master_os_integration():
    cos = AdiCareerOS()
    assert len(cos.jobs) > 0
    assert cos.hunter is not None
    assert cos.scorer is not None
    assert cos.app_manager is not None
    assert cos.interview_coach is not None


def test_adaptive_career_learning_engine():
    from adaptive_career_learning_engine import AdaptiveCareerLearningEngine
    learner = AdaptiveCareerLearningEngine()
    instincts = learner.load_instincts()
    assert len(instincts) >= 5
    res = learner.evaluate_and_optimize()
    assert res["generation"] >= 1
    assert "avg_score" in res
    assert res["status"] == "IMPROVED"
