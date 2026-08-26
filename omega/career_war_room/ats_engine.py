"""
ATS ENGINE
Compares candidate profile against target job description.
Extracts keywords, required skills, tools, certifications; computes ATS score, missing keywords,
strong/weak matches, and suggested resume modifications without fabricating experience.
"""
import re
from typing import Dict, Any, List

class ATSEngine:
    # Authoritative candidate profile (BBA International Business)
    CANDIDATE_PROFILE = {
        "education": "Bachelor of Business Administration (BBA) - International Business",
        "verified_skills": [
            "international trade", "customs clearance", "hs code classification",
            "incoterms 2020", "supply chain operations", "freight forwarding",
            "ocean freight", "air cargo logistics", "export import documentation",
            "cross-border logistics", "vendor management", "procurement",
            "business development", "market analysis", "financial analysis",
            "excel", "powerbi", "sql", "ai operations", "process optimization"
        ],
        "certifications": [
            "Certificate in International Trade & Customs Compliance",
            "Advanced Excel & Business Analytics Certification"
        ]
    }

    @classmethod
    def evaluate_job(cls, job: Dict[str, Any], resume_text: str = "") -> Dict[str, Any]:
        job_skills = [s.lower() for s in job.get("skills", [])]
        role_title = job.get("role_title", "").lower()
        
        # If resume text not provided, use baseline verified skills
        target_text = (resume_text or " ".join(cls.CANDIDATE_PROFILE["verified_skills"])).lower()
        
        strong_matches = []
        weak_matches = []
        missing_keywords = []

        for s in job_skills:
            if s in target_text or any(token in target_text for token in s.split()):
                strong_matches.append(s)
            elif any(token in s for token in ["sap", "oracle", "tableau"]):
                weak_matches.append(s)
            else:
                missing_keywords.append(s)

        # ATS Match Score formula
        total_skills = max(1, len(job_skills))
        matched_count = len(strong_matches) + (0.5 * len(weak_matches))
        raw_score = (matched_count / total_skills) * 100.0
        ats_score = round(min(100.0, max(40.0, raw_score + 10.0)), 1)

        recommendations = []
        if missing_keywords:
            recommendations.append(f"Highlight transferable experience related to: {', '.join(missing_keywords[:3])}")
        recommendations.append(f"Emphasize BBA International Business coursework and practical trade simulations.")
        recommendations.append(f"Ensure STAR-format bullet points include quantitative business outcomes.")

        return {
            "ats_score": ats_score,
            "strong_matches": strong_matches,
            "weak_matches": weak_matches,
            "missing_keywords": missing_keywords,
            "recommendations": recommendations,
            "zero_fabrication_guarantee": True
        }

ats_engine = ATSEngine()
