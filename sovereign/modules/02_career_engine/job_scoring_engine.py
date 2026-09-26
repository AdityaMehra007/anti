"""
ADI CAREER OS — 100-POINT JOB SCORING & EXPLAINABILITY ENGINE (Sections 16, 17, 298, 299)
Implements the 100-point rubric and transparent explainability breakdown.
"""

from typing import Dict, Any, List
from .job_entity import JobEntity

class JobScoringEngine:
    """
    Evaluates Job opportunities against candidate Aditya Mehra (Adi):
    - Target: AI-enabled Business Operations, Business Analyst, Strategy & Operations
    - Location: Bengaluru, India
    - Education: BBA International Business, DSU (2023-2026)
    """

    TARGET_ROLE_KEYWORDS = {
        "business operations": 20,
        "operations analyst": 19,
        "business analyst": 19,
        "strategy & operations": 20,
        "product operations": 18,
        "risk analyst": 16,
        "finance operations": 16,
        "international trade analyst": 17,
        "supply chain analyst": 16,
        "project coordinator": 15,
        "pmo analyst": 16,
        "process analyst": 17
    }

    TIER_1_COMPANIES = [
        "walmart global tech", "amazon", "deloitte", "ey", "pwc", "kpmg",
        "goldman sachs", "jpmorgan", "mckinsey", "bain", "bcg", "google",
        "microsoft", "maersk", "dhl", "ibm", "target", "uber", "flipkart"
    ]

    CORE_CANDIDATE_SKILLS = [
        "excel", "sql", "power bi", "business analysis", "operations",
        "process improvement", "sop", "workflow automation", "python", "ai"
    ]

    @classmethod
    def score_job(cls, job: JobEntity, sales_risk_score: int = 0) -> Dict[str, Any]:
        """
        Calculates the 100-point score breakdown:
        - Role Fit: 20
        - Eligibility: 15
        - Hiring Probability: 15
        - Company Quality: 10
        - Compensation: 10
        - Learning: 10
        - AI Relevance: 5
        - Career Capital: 5
        - Growth: 5
        - Location: 5
        Total: 100 points
        """
        title_lower = (job.title or "").lower()
        desc_lower = (job.description or "").lower()
        company_lower = (job.company_name or "").lower()
        loc_lower = (job.location or "").lower()

        # 1. Role Fit (Max 20)
        role_fit = 8.0  # baseline
        for target_role, pts in cls.TARGET_ROLE_KEYWORDS.items():
            if target_role in title_lower:
                role_fit = max(role_fit, float(pts))
            elif target_role in desc_lower:
                role_fit = max(role_fit, float(pts) * 0.7)

        # 2. Eligibility (Max 15) - Section 298
        eligibility = 15.0
        if job.experience_min > 2.0:
            # Over entry level
            exp_gap = job.experience_min - 2.0
            eligibility = max(4.0, 15.0 - (exp_gap * 4.0))
        elif job.experience_min > 1.0:
            eligibility = 12.0

        # 3. Hiring Probability (Max 15) - Section 299
        # Higher for freshers/0-1 yrs and fresh postings
        freshness = job.get_freshness()
        freshness_mult = 1.0 if freshness in ["VERY_FRESH", "FRESH"] else (0.85 if freshness == "ACTIVE" else 0.6)
        exp_factor = 1.0 if job.experience_min <= 1.0 else 0.75
        hiring_prob = round(15.0 * freshness_mult * exp_factor, 1)

        # 4. Company Quality (Max 10)
        company_quality = 6.0
        if any(t1 in company_lower for t1 in cls.TIER_1_COMPANIES):
            company_quality = 10.0
        elif len(company_lower) > 2:
            company_quality = 8.0

        # 5. Compensation (Max 10)
        comp_score = 7.0
        if job.salary_min:
            # In INR per annum
            if job.salary_min >= 800000:
                comp_score = 10.0
            elif job.salary_min >= 500000:
                comp_score = 8.5
            elif job.salary_min >= 350000:
                comp_score = 6.5
            else:
                comp_score = 5.0

        # 6. Learning Potential (Max 10)
        learning_matches = sum(1 for sk in cls.CORE_CANDIDATE_SKILLS if sk in desc_lower)
        learning_score = min(10.0, 4.0 + (learning_matches * 1.0))

        # 7. AI Relevance (Max 5)
        ai_score = 1.0
        if any(w in desc_lower or w in title_lower for w in ["ai", "automation", "llm", "machine learning", "copilot"]):
            ai_score = 5.0
        elif any(w in desc_lower for w in ["data", "analytics", "dashboard", "python"]):
            ai_score = 3.5

        # 8. Career Capital (Max 5)
        career_capital = 3.5
        if company_quality >= 9.0 or role_fit >= 18.0:
            career_capital = 5.0

        # 9. Growth (Max 5)
        growth_score = 4.0
        if any(w in desc_lower for w in ["growth", "mentorship", "fast-track", "rotation", "leadership"]):
            growth_score = 5.0

        # 10. Location (Max 5)
        loc_score = 2.0
        if "bengaluru" in loc_lower or "bangalore" in loc_lower:
            loc_score = 5.0
        elif "remote" in loc_lower or job.work_model.lower() == "remote":
            loc_score = 4.5
        elif "india" in loc_lower:
            loc_score = 3.5

        # Compute raw total
        raw_score = (
            role_fit + eligibility + hiring_prob + company_quality +
            comp_score + learning_score + ai_score + career_capital +
            growth_score + loc_score
        )

        # Sales Risk Penalty: If sales_risk_score > 30, heavily penalize total score
        sales_penalty = 0.0
        if sales_risk_score >= 40:
            sales_penalty = raw_score * 0.75  # 75% deduction for sales heavy
        elif sales_risk_score > 20:
            sales_penalty = raw_score * (sales_risk_score / 100.0)

        final_score = round(max(0.0, min(100.0, raw_score - sales_penalty)), 1)

        # Component Breakdown
        components = {
            "role_fit": round(role_fit, 1),
            "eligibility": round(eligibility, 1),
            "hiring_probability": round(hiring_prob, 1),
            "company_quality": round(company_quality, 1),
            "compensation": round(comp_score, 1),
            "learning": round(learning_score, 1),
            "ai_relevance": round(ai_score, 1),
            "career_capital": round(career_capital, 1),
            "growth": round(growth_score, 1),
            "location": round(loc_score, 1),
            "sales_risk_penalty": round(sales_penalty, 1)
        }

        # Explainability Section (Section 17)
        why_fits = []
        if role_fit >= 15:
            why_fits.append(f"Strong alignment with target operations/analyst role family ({job.role_family}).")
        if loc_score == 5.0:
            why_fits.append("Prime Bengaluru hub location matching candidate base.")
        if company_quality >= 8.0:
            why_fits.append(f"High-prestige target employer ({job.company_name}).")
        if ai_score >= 3.5:
            why_fits.append("Incorporate AI / analytics tooling directly aligned with candidate moat.")

        missing_reqs = []
        if job.experience_min > 0:
            missing_reqs.append(f"Requires {job.experience_min} years experience (Candidate is 2026 graduate).")
        missing_skills = [sk for sk in ["sql", "power bi", "excel"] if sk in desc_lower and sk not in job.skills]
        if missing_skills:
            missing_reqs.append(f"Highlight candidate project proof for: {', '.join(missing_skills)}.")

        risks = []
        if sales_risk_score > 20:
            risks.append(f"Sales risk detected ({sales_risk_score}/100). Verify role responsibilities.")
        if hiring_prob < 10.0:
            risks.append(f"Requisition freshness is {freshness}; probability decreases over time.")

        advantages = [
            f"BBA International Business degree matches multinational operating structure.",
            f"Direct verified execution experience (summit operations, workflow automation)."
        ]

        action = "PRIORITY_APPLY" if final_score >= 75 and sales_risk_score < 30 else ("REVIEW" if final_score >= 55 else "DEPENALIZE_ARCHIVE")

        explainability = {
            "why": " ".join(why_fits) or "Moderate general fit for business graduate.",
            "evidence": "Candidate positioning in AI Operations and verifiable project portfolio.",
            "missing_requirements": missing_reqs or ["None identified; fully eligible."],
            "risks": risks or ["No major disqualifying risks identified."],
            "strongest_advantages": advantages,
            "recommended_action": action
        }

        return {
            "final_fit_score": final_score,
            "components": components,
            "explainability": explainability
        }
