"""
OPPORTUNITY SCORING ENGINE
Calculates multi-factor weighted Expected Career Value (ECV) and role match score (0-100).
Evaluates: Role Fit, Skill Fit, International Exposure, AI Alignment, Company Quality, Location Friction.
"""
from typing import Dict, Any, List, Optional

class OpportunityScoringEngine:
    PROFILE_KEYWORDS = {
        "international business": 1.5,
        "cross-border": 1.5,
        "global operations": 1.5,
        "supply chain": 1.3,
        "logistics": 1.3,
        "customs": 1.4,
        "trade compliance": 1.5,
        "business development": 1.2,
        "procurement": 1.2,
        "operations analyst": 1.3,
        "project coordinator": 1.1,
        "data analytics": 1.2,
        "market research": 1.1,
        "export": 1.4,
        "import": 1.4,
        "bengaluru": 1.2,
        "bangalore": 1.2,
        "gcc": 1.5,
        "mnc": 1.5
    }

    @classmethod
    def calculate_score(cls, job: Dict[str, Any], company_dossier: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        role_text = (job.get("role_title", "") + " " + job.get("category", "") + " " + " ".join(job.get("skills", []))).lower()
        
        # 1. Keyword & Profile Match (Max 40 pts)
        weight_sum = 0.0
        for kw, weight in cls.PROFILE_KEYWORDS.items():
            if kw in role_text:
                weight_sum += weight
        
        role_fit_score = min(40.0, max(15.0, (weight_sum / 3.5) * 40.0))

        # 2. Company Prestige & Tier (Max 25 pts)
        company_tier = company_dossier.get("tier", "TIER_B") if company_dossier else "TIER_B"
        tier_points = {
            "TIER_S": 25.0,
            "TIER_A": 22.0,
            "TIER_B": 18.0,
            "TIER_C": 12.0
        }.get(company_tier, 18.0)

        # 3. Location & Commute Friction (Max 15 pts)
        loc = job.get("location", "").lower()
        if "remote" in loc or "hybrid" in loc:
            loc_score = 15.0
        elif "bangalore" in loc or "bengaluru" in loc:
            loc_score = 14.0
        elif "india" in loc:
            loc_score = 10.0
        else:
            loc_score = 7.0

        # 4. Career Upside & Learning (Max 20 pts)
        upside_score = 20.0 if company_tier in ["TIER_S", "TIER_A"] else 15.0

        total_score = round(role_fit_score + tier_points + loc_score + upside_score, 1)
        total_score = min(100.0, max(0.0, total_score))

        return {
            "opportunity_score": total_score,
            "role_fit_score": round(role_fit_score, 1),
            "company_tier_score": tier_points,
            "location_score": loc_score,
            "career_upside_score": upside_score,
            "priority_tier": "HIGH" if total_score >= 80.0 else ("MEDIUM" if total_score >= 65.0 else "STANDARD")
        }

opportunity_scorer = OpportunityScoringEngine()
