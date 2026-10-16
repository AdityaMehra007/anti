"""
=============================================================================
VENTURE 03: BENGALURU FRESHER & STUDENT CAREER COPILOT ENGINE
Autonomous Career Intelligence, ATS Fit Scoring & Campus Matchmaking Engine
Tailored for Bangalore University Students (DSU, Christ, Jain, PES, RV)
=============================================================================
"""

import json
import os
import sqlite3
from typing import Any

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel

    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VAULT_PATH = os.path.join(
    BASE_DIR, "projects", "flagship-career-engine", "career_vault.db"
)

BANGALORE_CORRIDORS = {
    "MANYATA": ["Manyata", "Nagawara", "Hebbal", "Thanisandra"],
    "BELLANDUR_ORR": [
        "Bellandur",
        "Outer Ring Road",
        "ORR",
        "Kadubeesanahalli",
        "Marathahalli",
        "Sarjapur",
    ],
    "WHITEFIELD": ["Whitefield", "ITPB", "EPIP", "Hoodi"],
    "ELECTRONIC_CITY": ["Electronic City", "ECity", "Hosur Road"],
    "CBD": ["MG Road", "Residency Road", "Domlur", "Koramangala", "Indiranagar"],
}


class StudentProfile:
    def __init__(
        self,
        name: str,
        degree: str,
        college: str,
        graduation_year: int,
        gpa: float,
        skills: list[str],
        preferred_corridors: list[str] | None = None,
    ):
        self.name = name
        self.degree = degree
        self.college = college
        self.graduation_year = graduation_year
        self.gpa = gpa
        self.skills = [s.strip().lower() for s in skills]
        self.preferred_corridors = preferred_corridors or [
            "MANYATA",
            "BELLANDUR_ORR",
            "WHITEFIELD",
        ]


class BengaluruCareerCopilot:
    """Matches fresher student profiles against verified corporate opportunities with ATS diagnostics."""

    def __init__(self, db_path: str = VAULT_PATH):
        self.db_path = db_path

    def _get_jobs(self) -> list[dict[str, Any]]:
        if not os.path.exists(self.db_path):
            return []
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM jobs WHERE fit_score >= 65 ORDER BY fit_score DESC")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def evaluate_student(
        self, student: StudentProfile, top_n: int = 5
    ) -> dict[str, Any]:
        """
        Calculates student-specific ATS compatibility score across vault opportunities.
        """
        all_jobs = self._get_jobs()
        matched_recommendations = []

        for job in all_jobs:
            req_skills = []
            try:
                if job.get("required_skills"):
                    req_skills = json.loads(job["required_skills"])
            except Exception:
                req_skills = [
                    s.strip()
                    for s in str(job.get("required_skills", "")).split(",")
                    if s.strip()
                ]

            job_skills_lower = [s.lower() for s in req_skills]
            matched_skills = [
                s
                for s in student.skills
                if any(js in s or s in js for js in job_skills_lower)
            ]
            missing_skills = [
                js
                for js in job_skills_lower
                if not any(s in js or js in s for s in student.skills)
            ]

            # Scoring algorithm
            base_vault_score = job.get("fit_score", 70)
            skill_overlap_ratio = (
                (len(matched_skills) / len(job_skills_lower))
                if job_skills_lower
                else 0.5
            )
            skill_points = round(skill_overlap_ratio * 30.0, 1)

            # Location Corridor Bonus
            location_str = (job.get("location") or "").lower()
            corridor_matched = "OTHER_BLR"
            corridor_bonus = 0.0
            for corr, keywords in BANGALORE_CORRIDORS.items():
                if any(kw.lower() in location_str for kw in keywords):
                    corridor_matched = corr
                    if corr in student.preferred_corridors:
                        corridor_bonus = 10.0
                    break

            final_student_score = min(
                100.0,
                round((base_vault_score * 0.6) + skill_points + corridor_bonus, 1),
            )

            matched_recommendations.append(
                {
                    "job_id": job.get("job_id"),
                    "company": job.get("company"),
                    "title": job.get("title"),
                    "location": job.get("location"),
                    "corridor": corridor_matched,
                    "url": job.get("url"),
                    "student_fit_score": final_student_score,
                    "matched_skills": matched_skills,
                    "missing_skills_for_ats": missing_skills[:4],
                    "recommended_resume_version": "SUPPLY_CHAIN_PROCUREMENT"
                    if "supply" in job.get("title", "").lower()
                    else "MASTER_ATS",
                }
            )

        matched_recommendations.sort(key=lambda x: x["student_fit_score"], reverse=True)
        top_matches = matched_recommendations[:top_n]

        return {
            "student_name": student.name,
            "college": student.college,
            "degree": student.degree,
            "total_opportunities_screened": len(all_jobs),
            "top_matched_count": len(top_matches),
            "recommendations": top_matches,
        }

    def generate_tailored_pitch(
        self, student: StudentProfile, target_job_id: str
    ) -> dict[str, Any]:
        """
        Drafts a custom, non-sales recruiter message and recommended resume highlights for the selected job.
        """
        if not os.path.exists(self.db_path):
            raise ValueError("Career vault database not found.")

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM jobs WHERE job_id = ?", (target_job_id,))
        job = cur.fetchone()
        conn.close()

        if not job:
            raise ValueError(f"Job ID {target_job_id} not found.")

        job_dict = dict(job)
        message = (
            f"Dear {job_dict['company']} Campus Recruitment Team,\n\n"
            f"I am writing to express my strong interest in the {job_dict['title']} role (Requisition: {job_dict['job_id']}) "
            f"located at your {job_dict['location']} office.\n\n"
            f"I am completing my {student.degree} at {student.college} (Class of {student.graduation_year}, GPA: {student.gpa}/10). "
            f"My academic and project experience centers on {', '.join(student.skills[:3])}, directly aligning with your team's operational goals.\n\n"
            f"I would welcome the opportunity to connect for a 10-minute introductory conversation regarding this opening.\n\n"
            f"Sincerely,\n{student.name}\nPhone: [Candidate Phone] | Email: [Candidate Email]"
        )

        return {
            "job_id": job_dict["job_id"],
            "company": job_dict["company"],
            "role_title": job_dict["title"],
            "tailored_outreach_message": message,
        }


# =====================================================================
# FASTAPI MICROSERVICE REST LAYER
# =====================================================================

if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="Bengaluru Fresher Career Copilot API",
        version="1.0.0",
        description="Local intelligence and matchmaking REST API for Bengaluru university graduates.",
    )

    class StudentEvaluateRequest(BaseModel):
        name: str
        degree: str
        college: str
        graduation_year: int = 2026
        gpa: float = 8.0
        skills: list[str]
        preferred_corridors: list[str] | None = None

    class PitchRequest(BaseModel):
        student: StudentEvaluateRequest
        job_id: str

    @app.get("/health")
    def health_check():
        return {
            "status": "HEALTHY",
            "service": "BengaluruCareerCopilot",
            "vault": os.path.exists(VAULT_PATH),
        }

    @app.get("/api/v1/corridors")
    def get_corridors():
        return BANGALORE_CORRIDORS

    @app.post("/api/v1/evaluate_student")
    def evaluate(req: StudentEvaluateRequest):
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

    @app.post("/api/v1/generate_tailored_pitch")
    def generate_pitch(req: PitchRequest):
        copilot = BengaluruCareerCopilot()
        profile = StudentProfile(
            name=req.student.name,
            degree=req.student.degree,
            college=req.student.college,
            graduation_year=req.student.graduation_year,
            gpa=req.student.gpa,
            skills=req.student.skills,
            preferred_corridors=req.student.preferred_corridors,
        )
        try:
            return copilot.generate_tailored_pitch(profile, req.job_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    copilot = BengaluruCareerCopilot()
    # Demo profile: DSU BBA graduate
    demo_student = StudentProfile(
        name="Aditya Mehra",
        degree="BBA International Business",
        college="Dayananda Sagar University",
        graduation_year=2026,
        gpa=8.2,
        skills=[
            "Supply Chain Management",
            "Procurement Operations",
            "Vendor SLA Governance",
            "Excel",
            "Data Analytics",
        ],
        preferred_corridors=["MANYATA", "BELLANDUR_ORR"],
    )

    eval_result = copilot.evaluate_student(demo_student, top_n=3)
    print("=== BENGALURU CAREER COPILOT EVALUATION ===")
    print(f"Student: {eval_result['student_name']} ({eval_result['college']})")
    print(f"Opportunities Screened: {eval_result['total_opportunities_screened']}")
    for i, rec in enumerate(eval_result["recommendations"], 1):
        print(f"\n[{i}] {rec['company']} - {rec['title']}")
        print(f"    Location:   {rec['location']} ({rec['corridor']})")
        print(f"    Fit Score:  {rec['student_fit_score']}/100")
        print(f"    Matched:    {', '.join(rec['matched_skills'])}")
        print(f"    Missing:    {', '.join(rec['missing_skills_for_ats'])}")
