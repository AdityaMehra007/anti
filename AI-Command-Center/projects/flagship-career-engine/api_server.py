"""
=============================================================================
ANTIGRAVITY OMNISYSTEM: FLAGSHIP CAREER ENGINE REST API & SERVER
High-Performance Local FastAPI Backend for Career OS Cockpit & Venture Suite
=============================================================================
"""

import os
import sqlite3
import sys
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VAULT_PATH = os.path.join(os.path.dirname(__file__), "career_vault.db")
HTML_PATH = os.path.join(os.path.dirname(__file__), "index.html")

sys.path.insert(0, os.path.join(BASE_DIR, "startup-lab"))
sys.path.insert(0, os.path.dirname(__file__))

from annotation_qa_validator import DatasetQAValidator
from bengaluru_career_copilot import BengaluruCareerCopilot, StudentProfile
from career_engine import CareerVault, OutreachGenerator, ResumeTailorer
from event_logistics_tracker import EventLogisticsTracker
from rate_card_optimizer import RateCardOptimizer

app = FastAPI(
    title="Antigravity Omnisystem Career & Venture API",
    version="3.2.0",
    description="Local-first REST API powering the Flagship Career Engine, Rate Card Optimizer, Event Logistics Tracker, and Bengaluru Career Copilot.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect(VAULT_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Models
class QuoteAuditRequest(BaseModel):
    vendor_name: str
    event_name: str = "Bengaluru Corporate Summit 2026"
    items: list[dict[str, Any]]


class StudentEvalRequest(BaseModel):
    name: str
    degree: str
    college: str
    graduation_year: int = 2026
    gpa: float = 8.0
    skills: list[str]
    preferred_corridors: list[str] | None = None


class EventAuditRequest(BaseModel):
    event_name: str = "Bengaluru Tech Summit 2026"
    budget_inr: float = 500000.0
    vendors: list[dict[str, Any]]
    milestones: list[dict[str, Any]] | None = None


class DatasetQARequest(BaseModel):
    allowed_classes: list[str] = ["pallet", "forklift", "worker", "box", "tote"]
    frames: list[dict[str, Any]]
    min_box_size: int = 10


class ApplicationCreateRequest(BaseModel):
    job_id: str
    resume_version: str = "MASTER_ATS"
    notes: str = ""
    follow_up_days: int = 3


@app.get("/health")
def health():
    return {
        "status": "HEALTHY",
        "service": "AntigravityCareerAPI",
        "version": "3.1.0",
        "database_exists": os.path.exists(VAULT_PATH),
    }


@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serves the Cockpit v3.0 HTML directly."""
    if os.path.exists(HTML_PATH):
        with open(HTML_PATH, encoding="utf-8") as f:
            return f.read()
    return "<h1>Cockpit HTML not compiled yet. Run generate_dashboard.py</h1>"


@app.get("/api/v1/stats")
def get_vault_stats():
    """Provides real-time pipeline telemetry and distribution metrics."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM jobs")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM jobs WHERE fit_score >= 80")
    tier1 = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM jobs WHERE fit_score >= 70 AND fit_score < 80")
    tier2 = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM applications")
    applied = cur.fetchone()[0]

    cur.execute(
        "SELECT company, COUNT(*) FROM jobs GROUP BY company ORDER BY COUNT(*) DESC LIMIT 8"
    )
    top_companies = [{"company": r[0], "count": r[1]} for r in cur.fetchall()]
    conn.close()

    return {
        "total_opportunities": total,
        "high_fit_tier1": tier1,
        "high_potential_tier2": tier2,
        "applications_active": applied,
        "top_employers": top_companies,
    }


@app.get("/api/v1/jobs")
def list_jobs(
    min_score: int = Query(0, ge=0, le=100),
    company: str | None = None,
    search: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Queries indexed jobs with deterministic filtering."""
    conn = get_db()
    cur = conn.cursor()

    query = "SELECT * FROM jobs WHERE fit_score >= ?"
    params: list[Any] = [min_score]

    if company:
        query += " AND company LIKE ?"
        params.append(f"%{company}%")
    if search:
        query += " AND (title LIKE ? OR description LIKE ? OR location LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    query += " ORDER BY fit_score DESC, id ASC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cur.execute(query, params)
    jobs = [dict(r) for r in cur.fetchall()]
    conn.close()

    return {"count": len(jobs), "limit": limit, "offset": offset, "jobs": jobs}


@app.get("/api/v1/jobs/{job_id}")
def get_job(job_id: str):
    """Retrieves full detail and breakdown for a specific requisition."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found in vault.")
    return dict(row)


@app.post("/api/v1/rate_card/audit")
def audit_vendor_quote(req: QuoteAuditRequest):
    """Audits vendor quotation and synthesizes negotiation counter-letter."""
    benchmark_rates = {
        "German Tent Structure (sq ft)": 18.0,
        "JBL Line Array Sound Setup (day)": 35000.0,
        "P3 LED Video Wall (sq ft)": 120.0,
        "VIP Lounge Sofa Set (unit/day)": 1200.0,
        "Silent Generator 125 kVA (day)": 8500.0,
        "Security Marshal Deployment (shift)": 1100.0,
    }
    optimizer = RateCardOptimizer(benchmark_rates)
    result = optimizer.audit_quotation(req.items)
    counter_letter = optimizer.generate_counter_letter(
        result, req.vendor_name, req.event_name
    )
    return {"audit_summary": result, "counter_negotiation_letter": counter_letter}


@app.post("/api/v1/copilot/evaluate")
def evaluate_student_profile(req: StudentEvalRequest):
    """Evaluates student profile across Bangalore corporate corridors."""
    copilot = BengaluruCareerCopilot()
    profile = StudentProfile(
        name=req.name,
        degree=req.degree,
        college=req.college,
        graduation_year=req.graduation_year,
        gpa=req.gpa,
        skills=req.skills,
        preferred_corridors=req.preferred_corridors,
    )
    return copilot.evaluate_student(profile)


@app.post("/api/v1/event_logistics/audit")
def audit_event_logistics(req: EventAuditRequest):
    """Audits event logistics, milestone adherence, and calculates contractual delay penalties."""
    tracker = EventLogisticsTracker(req.event_name, req.budget_inr)
    for v in req.vendors:
        tracker.add_vendor(
            vendor_id=v["vendor_id"],
            name=v["name"],
            category=v.get("category", "General"),
            contracted_amount=float(v["contracted_amount"]),
            hourly_delay_penalty_rate=float(v.get("hourly_delay_penalty_rate", 0.05)),
        )
        if v.get("delay_hours", 0) > 0:
            tracker.record_vendor_delay(v["vendor_id"], float(v["delay_hours"]))

    if req.milestones:
        for m in req.milestones:
            tracker.add_milestone(
                milestone_id=m["milestone_id"],
                description=m["description"],
                target_time=m.get("target_time", "08:00 AM"),
                owner_vendor_id=m.get("owner_vendor_id", ""),
            )
            if m.get("completed_at"):
                tracker.complete_milestone(
                    milestone_id=m["milestone_id"],
                    completed_at=m["completed_at"],
                    delay_hours=float(m.get("delay_hours", 0.0)),
                )

    return tracker.generate_financial_audit()


@app.post("/api/v1/dataset_qa/validate")
def validate_dataset_qa(req: DatasetQARequest):
    """Validates multi-modal annotation bounding boxes and taxonomy for AI robotics models."""
    validator = DatasetQAValidator(
        allowed_classes=req.allowed_classes, min_box_size=req.min_box_size
    )
    return validator.validate_dataset(req.frames)


@app.get("/api/v1/jobs/{job_id}/tailor")
def tailor_resume_for_job(job_id: str):
    """Tailors verified candidate evidence bullets for a specific job requisition."""
    vault = CareerVault(VAULT_PATH)
    job = vault.get_job(job_id)
    vault.close()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    return ResumeTailorer.tailor(job)


@app.get("/api/v1/jobs/{job_id}/outreach")
def generate_job_outreach(job_id: str, recruiter_name: str = "Hiring Team"):
    """Synthesizes a personalized outreach message referencing verified candidate accomplishments."""
    vault = CareerVault(VAULT_PATH)
    job = vault.get_job(job_id)
    vault.close()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    message = OutreachGenerator.generate_recruiter_message(
        job, recruiter_name=recruiter_name
    )
    return {
        "job_id": job["job_id"],
        "company": job["company"],
        "title": job["title"],
        "recruiter_name": recruiter_name,
        "outreach_message": message,
    }


@app.get("/api/v1/applications")
def list_applications():
    """Retrieves all tracked applications and outreach statuses."""
    vault = CareerVault(VAULT_PATH)
    apps = vault.get_applications()
    vault.close()
    return {"count": len(apps), "applications": apps}


@app.post("/api/v1/applications")
def record_application(req: ApplicationCreateRequest):
    """Records an application submission and schedules automated follow-up triage."""
    vault = CareerVault(VAULT_PATH)
    try:
        app_record = vault.record_application(
            job_id=req.job_id,
            resume_version=req.resume_version,
            notes=req.notes,
            follow_up_days=req.follow_up_days,
        )
        vault.close()
        return {"status": "SUCCESS", "application": app_record}
    except Exception as e:
        vault.close()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/follow_ups")
def get_due_follow_ups(date: str | None = None):
    """Retrieves all applications with overdue or pending follow-up deadlines."""
    vault = CareerVault(VAULT_PATH)
    due = vault.get_due_follow_ups(as_of_date=date)
    vault.close()
    return {"count": len(due), "follow_ups": due}


if __name__ == "__main__":
    import uvicorn

    print("[*] Starting Antigravity Career Engine API on http://127.0.0.1:8080...")
    uvicorn.run("api_server:app", host="127.0.0.1", port=8080, reload=False)
