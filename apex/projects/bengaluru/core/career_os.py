"""
APEX BENGALURU - Career OS & Talent Opportunity Engine
Matches individuals to high-value GCC, MNC, and Startup roles with strict skill-gap analytics.
"""
import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List

DB_PATH = Path(r"e:\anti\apex\projects\bengaluru\data\bengaluru.db")

class BengaluruCareerOS:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def match_user_profile(self, degree: str, user_skills: List[str], experience_level: str = "FRESHER") -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM job_postings WHERE experience_level = ? OR target_degree LIKE ?", (experience_level, f"%{degree}%"))
        jobs = [dict(r) for r in cur.fetchall()]
        conn.close()

        results = []
        user_skills_set = set(s.lower() for s in user_skills)

        for job in jobs:
            req_skills = json.loads(job["skills_required"])
            req_skills_set = set(s.lower() for s in req_skills)
            
            matched = user_skills_set.intersection(req_skills_set)
            gaps = req_skills_set.difference(user_skills_set)

            # Degree bonus
            degree_match = 1.0 if degree.lower() in job["target_degree"].lower() else 0.8
            match_pct = round(((len(matched) / max(len(req_skills), 1)) * 0.7 + (degree_match * 0.3)) * 100, 1)

            results.append({
                "job_id": job["job_id"],
                "company": job["company_name"],
                "role": job["role_title"],
                "domain": job["domain"],
                "salary_range": job["salary_range_inr"],
                "work_mode": job["work_mode"],
                "location": job["location_micro"],
                "match_percentage": match_pct,
                "matched_skills": list(matched),
                "skill_gaps": list(gaps),
                "application_priority": "TIER_1_IMMEDIATE" if match_pct >= 60 else "TIER_2_PREPARE",
                "source_url": job["source_url"]
            })

        results.sort(key=lambda x: x["match_percentage"], reverse=True)
        return results

    def generate_interview_prep(self, company: str, role: str) -> Dict[str, Any]:
        return {
            "company": company,
            "role": role,
            "core_competency_questions": [
                f"How would you optimize cross-border vendor communication and Incoterms documentation at {company}?",
                "Describe a project where you used data analytics (SQL/Python/Excel) to resolve a supply chain or financial discrepancy.",
                "How do you evaluate currency exchange volatility and tariff impacts on landed costs for imported components?"
            ],
            "case_study_prompt": f"Analyze a scenario where port congestion at Nhava Sheva increases lead times by 3 weeks for {company}'s Bengaluru assembly hub. Outline your mitigation strategy.",
            "behavioral_focus": "High-velocity ownership, cross-functional stakeholder management, and proactive communication."
        }

if __name__ == "__main__":
    career = BengaluruCareerOS()
    matches = career.match_user_profile("BBA", ["Incoterms", "Excel", "Supply Chain Analytics", "SQL"], "FRESHER")
    print(f"[CAREER_OS] Matches found for BBA Profile:\n{json.dumps(matches, indent=2)}")
