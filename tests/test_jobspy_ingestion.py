"""
Unit and integration tests for JobSpy Ingestion & Intelligence Engine.
Follows Red-Green-Refactor TDD cycle.
"""

import os
import sys
import csv
import pytest
from pathlib import Path

# Ensure root directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from jobspy_market_scraper import (
    normalize_job_record,
    detect_bangalore_cluster,
    calculate_role_fit_score,
    deduplicate_jobs,
    format_for_job_applications_csv,
    append_to_job_applications_csv,
    JobSpyIngestionEngine,
)


def get_sample_records():
    return [
        {
            "id": "in-101",
            "title": "Business Development Executive - Enterprise SaaS",
            "company": "LeadSquared",
            "location": "Bengaluru, Karnataka, India",
            "site": "linkedin",
            "job_url": "https://www.linkedin.com/jobs/view/101",
            "job_url_direct": "https://leadsquared.com/careers/101",
            "description": "Looking for a high-energy B2B sales professional for outbound lead generation, pipeline management, client acquisition, and cold outreach. Fresher or 0-2 years experience.",
            "min_amount": 500000,
            "max_amount": 800000,
            "interval": "yearly",
            "currency": "INR",
        },
        {
            "id": "in-102",
            "title": "AI Operations & Data Annotation Associate",
            "company": "NextGen AI Lab",
            "location": "Koramangala, Bangalore",
            "site": "naukri",
            "job_url": "https://www.naukri.com/job-102",
            "job_url_direct": "",
            "description": "Responsible for dataset curation, LLM prompt engineering validation, quality audits, and AI data labeling workflows. Knowledge of automated data pipelines.",
            "min_amount": 450000,
            "max_amount": 650000,
            "interval": "yearly",
            "currency": "INR",
        },
        {
            "id": "in-103",
            "title": "Senior Chief Architect - 15+ Years Experience",
            "company": "Legacy Corp",
            "location": "Mumbai",
            "site": "indeed",
            "job_url": "https://www.indeed.com/viewjob?jk=103",
            "job_url_direct": "",
            "description": "Requires minimum 15 years in distributed systems, C++ internals, and kernel engineering. Not suitable for junior candidates.",
            "min_amount": None,
            "max_amount": None,
            "interval": None,
            "currency": None,
        }
    ]


@pytest.fixture
def sample_raw_jobspy_records():
    return get_sample_records()


def test_detect_bangalore_cluster():
    assert detect_bangalore_cluster("Koramangala, Bangalore") == "Koramangala & HSR Layout"
    assert detect_bangalore_cluster("Bellandur Outer Ring Road, Bengaluru") == "Outer Ring Road (Bellandur / Marathahalli / Sarjapur)"
    assert detect_bangalore_cluster("ITPL Main Road, Whitefield, Bangalore") == "Whitefield & ITPL"
    assert detect_bangalore_cluster("Manyata Tech Park, Hebbal") == "Manyata Tech Park (Hebbal)"
    assert detect_bangalore_cluster("Electronic City Phase 1") == "Electronic City (Phase 1 & 2)"
    assert detect_bangalore_cluster("MG Road, Bangalore") == "CBD (MG Road / Indiranagar / Richmond)"
    assert detect_bangalore_cluster("Bengaluru, Karnataka") == "Bengaluru General Corridor"


def test_normalize_job_record(sample_raw_jobspy_records):
    raw = sample_raw_jobspy_records[0]
    normalized = normalize_job_record(raw)

    assert normalized["company"] == "LeadSquared"
    assert normalized["title"] == "Business Development Executive - Enterprise SaaS"
    assert normalized["site"] == "LinkedIn"
    assert normalized["application_url"] == "https://leadsquared.com/careers/101"
    assert "Bengaluru" in normalized["location"]


def test_calculate_role_fit_score(sample_raw_jobspy_records):
    b2b_job = normalize_job_record(sample_raw_jobspy_records[0])
    score_b2b, evidence_b2b, rationale_b2b = calculate_role_fit_score(b2b_job)
    assert score_b2b >= 80
    assert "EXP-002" in evidence_b2b  # Pencil Mark BD revenue evidence
    assert "B2B" in rationale_b2b or "Sales" in rationale_b2b or "pipeline" in rationale_b2b.lower()

    ai_job = normalize_job_record(sample_raw_jobspy_records[1])
    score_ai, evidence_ai, rationale_ai = calculate_role_fit_score(ai_job)
    assert score_ai >= 80
    assert "EXP-001" in evidence_ai  # Instawork AI Data evidence

    senior_job = normalize_job_record(sample_raw_jobspy_records[2])
    score_senior, _, rationale_senior = calculate_role_fit_score(senior_job)
    assert score_senior < 60  # Seniority mismatch / 15+ years penalty


def test_deduplicate_jobs(sample_raw_jobspy_records):
    normalized = [normalize_job_record(r) for r in sample_raw_jobspy_records]
    existing_records = [
        {
            "Company Name": "LeadSquared",
            "Role Title": "Business Development Executive - Enterprise SaaS",
            "Application URL": "https://leadsquared.com/careers/101"
        }
    ]
    filtered = deduplicate_jobs(normalized, existing_records)
    # LeadSquared should be filtered out
    assert len(filtered) == 2
    assert not any(j["company"] == "LeadSquared" for j in filtered)


def test_format_for_job_applications_csv(sample_raw_jobspy_records):
    job = normalize_job_record(sample_raw_jobspy_records[0])
    row = format_for_job_applications_csv(job, fit_score=88, fit_rationale="Target role fit: 88/100. Focus: B2B pipeline, outbound lead gen.")
    
    assert row["Company Name"] == "LeadSquared"
    assert row["Role Title"] == "Business Development Executive - Enterprise SaaS"
    assert row["Status"] == "READY_TO_APPLY"
    assert row["Job Board / Portal"] == "LinkedIn"
    assert "88/100" in row["Notes"]


def test_safe_append_to_job_applications_csv(tmp_path):
    csv_file = tmp_path / "test_applications.csv"
    headers = ["Date", "Company Name", "Role Title", "Location/Remote", "Job Board / Portal", "Application URL", "Status", "Follow-Up Date", "Contact Person", "Notes"]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerow({
            "Date": "2026-09-09",
            "Company Name": "Deloitte",
            "Role Title": "Risk Analyst",
            "Location/Remote": "Bengaluru",
            "Job Board / Portal": "Direct Portal",
            "Application URL": "https://deloitte.com",
            "Status": "READY_TO_APPLY",
            "Follow-Up Date": "2026-09-12",
            "Contact Person": "HR",
            "Notes": "Initial test note"
        })

    new_row = {
        "Date": "2026-09-10",
        "Company Name": "NewTech",
        "Role Title": "BD Executive",
        "Location/Remote": "Bengaluru (Koramangala)",
        "Job Board / Portal": "Naukri",
        "Application URL": "https://naukri.com/newtech",
        "Status": "READY_TO_APPLY",
        "Follow-Up Date": "2026-09-13",
        "Contact Person": "Talent Acquisition Partner",
        "Notes": "Target role fit: 85/100."
    }

    append_to_job_applications_csv(csv_file, [new_row])

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 2
        assert reader[1]["Company Name"] == "NewTech"


if __name__ == "__main__":
    import tempfile
    print("Running standalone JobSpy ingestion tests...")
    test_detect_bangalore_cluster()
    print("✓ test_detect_bangalore_cluster passed")
    
    records = get_sample_records()
    test_normalize_job_record(records)
    print("✓ test_normalize_job_record passed")
    
    test_calculate_role_fit_score(records)
    print("✓ test_calculate_role_fit_score passed")
    
    test_deduplicate_jobs(records)
    print("✓ test_deduplicate_jobs passed")
    
    test_format_for_job_applications_csv(records)
    print("✓ test_format_for_job_applications_csv passed")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_safe_append_to_job_applications_csv(Path(tmp_dir))
    print("✓ test_safe_append_to_job_applications_csv passed")
    
    print("\nALL JOBSPY TESTS PASSED SUCCESSFULLY! (100% GREEN)")
