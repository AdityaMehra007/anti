import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple

class OmegaCareerBrain:
    """
    Multi-Factor Expected Value (EV) and Opportunity Scoring Engine for Aditya Mehra.
    Combines verified candidate profile alignment, Bangalore transit matrix,
    skill gap analysis, and multi-criteria 0-100 Career Opportunity Scoring.
    """

    TARGET_MEDIAN_CTC_INR = 900000.0  # 9.0 LPA baseline

    COMMUTE_MATRIX = {
        "electronic city": {"friction": 3.5, "peak_mins": 25, "offpeak_mins": 15, "metro_access": "Yellow Line Direct", "transit_mode": "Metro / Namma Yatri"},
        "koramangala": {"friction": 4.0, "peak_mins": 20, "offpeak_mins": 12, "metro_access": "Bus / Auto / Cab", "transit_mode": "Auto / EV Shuttle"},
        "hsr layout": {"friction": 4.5, "peak_mins": 22, "offpeak_mins": 14, "metro_access": "Bus / Auto", "transit_mode": "Auto / EV Shuttle"},
        "indiranagar": {"friction": 6.5, "peak_mins": 35, "offpeak_mins": 22, "metro_access": "Purple Line", "transit_mode": "Metro / Cab"},
        "outer ring road": {"friction": 7.0, "peak_mins": 45, "offpeak_mins": 28, "metro_access": "ORR Metro Underway", "transit_mode": "Company Shuttle / Cab"},
        "bellandur": {"friction": 7.2, "peak_mins": 48, "offpeak_mins": 30, "metro_access": "ORR Feeder", "transit_mode": "Company Shuttle / Cab"},
        "ecospace": {"friction": 7.2, "peak_mins": 48, "offpeak_mins": 30, "metro_access": "ORR Feeder", "transit_mode": "Company Shuttle / Cab"},
        "rmz ecoworld": {"friction": 7.5, "peak_mins": 50, "offpeak_mins": 32, "metro_access": "ORR Feeder", "transit_mode": "Company Shuttle / Cab"},
        "cessna": {"friction": 7.5, "peak_mins": 50, "offpeak_mins": 32, "metro_access": "ORR Feeder", "transit_mode": "Company Shuttle / Cab"},
        "prestige tech park": {"friction": 7.8, "peak_mins": 52, "offpeak_mins": 35, "metro_access": "ORR Feeder", "transit_mode": "Company Shuttle / Cab"},
        "cbd": {"friction": 8.5, "peak_mins": 50, "offpeak_mins": 35, "metro_access": "Purple & Green Line", "transit_mode": "Metro Train"},
        "mg road": {"friction": 8.5, "peak_mins": 50, "offpeak_mins": 35, "metro_access": "Purple Line", "transit_mode": "Metro Train"},
        "manyata tech park": {"friction": 13.5, "peak_mins": 75, "offpeak_mins": 48, "metro_access": "Hebbal Feeder / Blue Line", "transit_mode": "Cab / Enterprise Bus"},
        "hebbal": {"friction": 13.5, "peak_mins": 75, "offpeak_mins": 48, "metro_access": "Hebbal Feeder", "transit_mode": "Cab / Enterprise Bus"},
        "whitefield": {"friction": 15.0, "peak_mins": 80, "offpeak_mins": 55, "metro_access": "Purple Line (Kadugodi)", "transit_mode": "Metro Train / Cab"},
        "itpl": {"friction": 15.0, "peak_mins": 80, "offpeak_mins": 55, "metro_access": "Purple Line (ITPL)", "transit_mode": "Metro Train / Cab"},
        "epip": {"friction": 15.5, "peak_mins": 85, "offpeak_mins": 58, "metro_access": "Purple Line", "transit_mode": "Metro Train / Cab"}
    }

    BRAND_LEVERAGE = {
        "Tier 1 Global GCC": 1.35,
        "Tier 1 Consulting": 1.30,
        "High-Growth Tech Unicorn": 1.25,
        "Tier 2 GCC": 1.15,
        "Enterprise MNC": 1.10
    }

    PRESTIGE_COMPANIES = {
        "walmart": 0.05,
        "amazon": 0.05,
        "deloitte": 0.05,
        "ey": 0.05,
        "ernst & young": 0.05,
        "goldman sachs": 0.08,
        "jpmorgan": 0.07,
        "google": 0.08,
        "microsoft": 0.08,
        "boeing": 0.06,
        "maersk": 0.06,
        "dhl": 0.05,
        "schneider electric": 0.04,
        "accenture": 0.06,
        "razorpay": 0.05,
        "swiggy": 0.05,
        "cred": 0.05
    }

    TIER_1_ENTERPRISES = {
        "EY", "Ernst & Young", "Accenture", "Deloitte", "Goldman Sachs", "IBM",
        "PwC", "PricewaterhouseCoopers", "Amazon", "KPMG", "Capgemini",
        "Tata Communications", "Google", "TCS", "JPMorgan", "Microsoft", "Cisco",
        "Walmart", "Walmart Global Tech", "Boeing", "Schneider Electric", "Maersk", "DHL"
    }

    ROLE_KEYWORDS = {
        "operations": ["operations", "operational", "ops", "logistics", "supply chain", "vendor", "facility", "run-of-show", "coordinator"],
        "event_management": ["event", "activation", "coordinator", "expo", "exhibition", "festival", "pavilion", "venue"],
        "business_development": ["sales", "business development", "bd", "client", "commercial", "account", "growth", "partnership"],
        "international_business": ["international", "global", "exim", "trade", "customs", "cross-border", "import", "export", "foreign"],
        "analytics_strategy": ["analyst", "strategy", "advisory", "consultant", "business analyst", "planning", "governance", "data ops"]
    }

    CORE_SKILL_PATTERNS = {
        "Operations & Workflow Management": ["operations", "operational", "ops", "run-of-show", "workflow", "coordination", "coordinator", "facility", "deployment"],
        "Vendor & SLA Governance": ["vendor", "sla", "service level", "contract", "procurement", "supplier", "vendor management"],
        "Cost Optimization & Budgeting": ["cost savings", "cost reduction", "cost optimization", "budget", "variance", "cost modeling"],
        "EXIM & Trade Compliance": ["incoterms", "incoterms 2020", "exim", "customs", "customs clearance", "import", "export", "ucp 600", "trade compliance", "hs code", "tariff"],
        "B2B Growth & Commercial": ["b2b", "business development", "revenue", "commercial", "client", "sales", "partnership"],
        "Supply Chain & Logistics": ["logistics", "supply chain", "inventory", "freight", "dispatch", "warehousing"],
        "Event & Activation Ops": ["event", "activation", "exhibition", "aero india", "expo", "festival"],
        "AI Data Ops & Analytics": ["data ops", "ai data", "accuracy", "quality assurance", "reporting", "governance", "analytics", "analyst"]
    }

    def __init__(self, profile_data: Optional[Dict[str, Any]] = None, profile_path: Optional[str] = None):
        if profile_data:
            self.profile = profile_data
        elif profile_path and os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                self.profile = json.load(f)
        elif os.path.exists(r"e:\anti\verified_profile.json"):
            with open(r"e:\anti\verified_profile.json", "r", encoding="utf-8") as f:
                self.profile = json.load(f)
        else:
            self.profile = self._get_default_aditya_profile()

    def _get_default_aditya_profile(self) -> Dict[str, Any]:
        return {
            "candidate": {
                "full_name": "Aditya Mehra",
                "email": "ashishiash007@gmail.com",
                "phone": "+91-7003456624",
                "location": "Bengaluru, India",
                "education": "BBA International Business, Dayananda Sagar University (2026)"
            },
            "name": "Aditya Mehra",
            "education": "BBA International Business, Dayananda Sagar University (2026)",
            "verified_experience": [
                {
                    "event": "AERO INDIA 2025",
                    "role": "Exhibition Operations Lead",
                    "organization": "Salt in My Coca",
                    "highlights": "Led 100k+ attendee ops, zero inventory shrinkage, 100% on-time daily opening, Tier-1 vendor SLA governance"
                },
                {
                    "clients": ["Tata Communications", "Puma Global"],
                    "role": "Event Coordinator",
                    "organization": "Strategic Brand Activations",
                    "highlights": "300+ event and ops deployments, vendor SLA governance"
                },
                {
                    "role": "Commercial Operations & BD Specialist",
                    "organization": "Commercial Projects",
                    "highlights": "Commercial pipeline management, 48h proposal turnaround, account handovers"
                },
                {
                    "role": "Operations & Analytical Data Specialist",
                    "organization": "Academic & Operational Projects",
                    "highlights": "Relational data modeling, operational SLA variance analysis, and workflow automation"
                }
            ],
            "core_competencies": [
                "Operations & Run-of-Show Logistics",
                "Tier-1 Vendor SLA Governance & Rate Card Structuring",
                "EXIM & Customs Compliance (Incoterms 2020, UCP 600, HS Codes)",
                "B2B Commercial Operations & Client Workflows",
                "Business Analytics & Data Operations (SQL, Star Schema, Power BI)"
            ]
        }

    def calculate_commute_friction(self, corridor_or_location: str = "Outer Ring Road") -> Tuple[float, Dict[str, Any]]:
        """
        Calculates Bangalore transit matrix commute friction score and transit metadata.
        Lower friction indicates higher accessibility from southern/central transit nodes.
        """
        loc_str = str(corridor_or_location or "").strip().lower()

        matched_key = None
        # Check against COMMUTE_MATRIX keys (prioritize longer keys for specific matches)
        for key in sorted(self.COMMUTE_MATRIX.keys(), key=len, reverse=True):
            if key in loc_str or loc_str in key:
                matched_key = key
                break

        if matched_key:
            info = dict(self.COMMUTE_MATRIX[matched_key])
            info["corridor_name"] = matched_key.title()
            return float(info["friction"]), info

        # Default for unspecified Bengaluru corridor
        default_info = {
            "friction": 8.0,
            "peak_mins": 50,
            "offpeak_mins": 35,
            "metro_access": "BMTC / Feeder / Metro",
            "transit_mode": "Cab / Bus / Transit",
            "corridor_name": "General Bengaluru Hub"
        }
        return 8.0, default_info

    def calculate_skill_gap(self, jd_text: str = "") -> Tuple[float, List[str], List[str]]:
        """
        Benchmarks job description against Aditya Mehra's verified skill profile.
        Returns:
            penalty: float (0.0 for >= 5 matched core skills, increasing with gaps)
            matched_skills: list of matching skill categories
            missing_skills: list of unaddressed skill categories
        """
        jd_lower = str(jd_text or "").lower()
        matched: List[str] = []
        missing: List[str] = []

        for category, keywords in self.CORE_SKILL_PATTERNS.items():
            if any(kw in jd_lower for kw in keywords):
                matched.append(category)
            else:
                missing.append(category)

        # If 5 or more candidate skills match JD, penalty is 0.0
        if len(matched) >= 5:
            penalty = 0.0
        else:
            penalty = round(max(0.0, (5 - len(matched)) * 3.5), 1)

        return penalty, matched, missing

    def calculate_expected_value(
        self,
        role_title: str,
        company_name: str,
        corridor: str = "Outer Ring Road",
        compensation_median: float = 900000.0,
        gcc_tier: str = "Tier 1 Global GCC",
        jd_text: str = ""
    ) -> Dict[str, Any]:
        """
        Multi-factor Expected Value (EV) calculation:
        EV = f(P(Interview), P(Offer), Compensation Multiple, Brand Prestige, Commute Friction, Skill Fit)
        """
        title_lower = str(role_title or "").lower()
        comp_lower = str(company_name or "").lower()

        # 1. Commute Friction
        commute_friction, commute_info = self.calculate_commute_friction(corridor)

        # 2. Skill Gap
        skill_penalty, matched_skills, missing_skills = self.calculate_skill_gap(jd_text)

        # 3. Brand & Enterprise Multiplier
        brand_mult = self.BRAND_LEVERAGE.get(gcc_tier, 1.10)
        prestige_boost = 0.0
        for p_name, boost in self.PRESTIGE_COMPANIES.items():
            if p_name in comp_lower:
                prestige_boost = max(prestige_boost, boost)
                break
        total_brand_mult = brand_mult + prestige_boost
        is_tier_1 = any(t.lower() in comp_lower for t in self.TIER_1_ENTERPRISES)

        # 4. Probability of Interview P(Interview)
        p_interview = 0.75
        if any(kw in title_lower for kw in ["operations", "operational", "ops", "logistics", "supply chain", "coordinator", "analyst"]):
            p_interview += 0.10
        if is_tier_1 or prestige_boost > 0:
            p_interview += 0.05
        if gcc_tier == "Tier 1 Global GCC":
            p_interview += 0.03
        if skill_penalty == 0.0:
            p_interview += 0.02
        else:
            p_interview -= min(0.30, skill_penalty * 0.02)
        p_interview = round(min(0.96, max(0.10, p_interview)), 2)

        # 5. Probability of Offer P(Offer) given interview
        p_offer = 0.78
        if any(kw in title_lower for kw in ["operations", "logistics", "trade", "exim", "analyst", "event"]):
            p_offer += 0.08
        if any(kw in str(jd_text or "").lower() for kw in ["sla", "vendor", "rate card", "incoterms", "governance"]):
            p_offer += 0.04
        if skill_penalty > 0.0:
            p_offer -= min(0.30, skill_penalty * 0.02)
        p_offer = round(min(0.95, max(0.10, p_offer)), 2)

        # 6. Compensation Multiple
        comp_mult = float(compensation_median) / self.TARGET_MEDIAN_CTC_INR

        # 7. EV Composite Score (0 - 100 scale)
        base_ev = ((p_interview * 0.45) + (p_offer * 0.45) + 0.10) * 100.0
        brand_factor = (total_brand_mult - 1.0) * 15.0
        salary_factor = min(15.0, max(-15.0, (comp_mult - 1.0) * 12.0))
        commute_discount = (commute_friction / 16.0) * 8.0

        raw_ev = base_ev + brand_factor + salary_factor - commute_discount - skill_penalty
        ev_score = round(min(100.0, max(10.0, raw_ev)), 1)

        recommendation = (
            "HIGH_PRIORITY_OUTREACH" if ev_score >= 80.0 else
            ("STANDARD_APPLICATION" if ev_score >= 65.0 else "EXPLORATORY_MONITORING")
        )

        return {
            "role_title": role_title,
            "company_name": company_name,
            "corridor": corridor,
            "compensation_median": float(compensation_median),
            "gcc_tier": gcc_tier,
            "ev_score": ev_score,
            "recommendation": recommendation,
            "breakdown": {
                "p_interview": p_interview,
                "p_offer": p_offer,
                "base_alignment": round(base_ev, 1),
                "brand_multiplier": round(total_brand_mult, 2),
                "compensation_multiple": round(comp_mult, 2),
                "commute_friction": round(commute_friction, 1),
                "commute_info": commute_info,
                "skill_gap_penalty": round(skill_penalty, 1),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "is_tier_1_enterprise": is_tier_1
            }
        }

    def score_opportunity(
        self,
        job_title: str,
        company_name: str,
        location: str = "Bengaluru, India",
        network_connections: int = 0,
        recruiter_count: int = 0,
        hiring_manager_count: int = 0,
        salary_offered_inr: Optional[float] = None,
        job_description: str = ""
    ) -> Dict[str, Any]:
        """
        Multi-criteria 12-factor opportunity evaluation model.
        Returns comprehensive breakdown, overall score (0-100), and strategic leverage index.
        """
        title_lower = job_title.lower()
        company_lower = company_name.lower()
        loc_lower = location.lower()
        jd_lower = job_description.lower()

        # 1. Role Fit (0-10)
        role_score = 4.0
        for category, kws in self.ROLE_KEYWORDS.items():
            if any(kw in title_lower for kw in kws):
                role_score = max(role_score, 8.5 if category in ["operations", "event_management", "international_business", "business_development"] else 7.0)

        # 2. Skill Fit (0-10)
        skill_score = 6.0
        if any(w in title_lower or w in jd_lower for w in ["operations", "vendor", "sla", "logistics", "scheduling", "coordination"]):
            skill_score += 2.5
        if any(w in title_lower or w in jd_lower for w in ["international", "trade", "compliance", "incoterms", "bba"]):
            skill_score += 1.5
        skill_score = min(10.0, skill_score)

        # 3. Education Fit (0-10)
        edu_score = 9.0 if any(w in title_lower or w in jd_lower for w in ["international", "business", "analyst", "management", "operations", "bba", "graduate"]) else 7.5

        # 4. Experience Fit (0-10)
        exp_score = 6.5
        if any(w in title_lower for w in ["event", "operations", "activation", "logistics", "exhibition"]):
            exp_score = 9.5
        elif any(w in title_lower for w in ["business development", "sales", "client", "commercial"]):
            exp_score = 8.5
        elif any(w in title_lower for w in ["analyst", "advisory", "consultant", "associate"]):
            exp_score = 7.5

        # 5. Location Fit (0-10)
        loc_score = 5.0
        if any(w in loc_lower for w in ["bangalore", "bengaluru"]):
            loc_score = 10.0
        elif any(w in loc_lower for w in ["remote", "hybrid", "work from home"]):
            loc_score = 9.0
        elif any(w in loc_lower for w in ["mumbai", "delhi", "gurgaon", "hyderabad", "india"]):
            loc_score = 7.5

        # 6. Salary Fit (0-10)
        salary_score = 7.0
        if salary_offered_inr is not None:
            if salary_offered_inr >= 900000:
                salary_score = 10.0
            elif salary_offered_inr >= 600000:
                salary_score = 8.5
            else:
                salary_score = 6.0

        # 7. Company Quality (0-10)
        is_tier_1 = any(t.lower() in company_lower for t in self.TIER_1_ENTERPRISES)
        comp_quality = 9.5 if is_tier_1 else 7.0

        # 8. Career Upside (0-10)
        career_upside = 9.0 if is_tier_1 else 7.5

        # 9. Network Access (0-10)
        if recruiter_count > 0 or hiring_manager_count > 0:
            network_score = min(10.0, 7.0 + (recruiter_count * 0.3) + (hiring_manager_count * 1.0))
        elif network_connections > 0:
            network_score = min(8.0, 4.0 + (network_connections * 0.05))
        else:
            network_score = 2.0

        # 10. Application Difficulty (Inverted) (0-10)
        app_difficulty = 8.5 if (recruiter_count > 0 or network_connections > 5) else 5.0

        # 11. Competition Assessment (0-10)
        competition_score = 6.5 if is_tier_1 else 8.0

        # 12. Probability of Interview (0-10)
        prob_interview = round(min(10.0, (role_score * 0.25) + (exp_score * 0.25) + (network_score * 0.35) + (loc_score * 0.15)), 1)

        # Sales Risk Assessment
        sales_indicators = [
            ("sdr", 40.0),
            ("bdr", 40.0),
            ("sales development representative", 50.0),
            ("business development representative", 50.0),
            ("business development associate", 45.0),
            ("inside sales", 40.0),
            ("field sales", 45.0),
            ("telesales", 45.0),
            ("telecalling", 40.0),
            ("cold call", 35.0),
            ("cold calling", 35.0),
            ("outbound sales", 35.0),
            ("outbound prospecting", 30.0),
            ("merchant acquisition", 35.0),
            ("lead generation", 25.0),
            ("quota", 25.0),
            ("commission based", 30.0),
            ("commission-based", 30.0),
            ("variable incentive", 25.0),
            ("acquisition target", 25.0),
            ("acquisition targets", 25.0),
            ("field visits", 20.0),
            ("dial ", 20.0),
        ]
        sales_risk_score = 0.0
        combined_text = f"{title_lower} {jd_lower}"
        for indicator, penalty in sales_indicators:
            if indicator in combined_text:
                sales_risk_score += penalty
        sales_risk_score = round(min(100.0, sales_risk_score), 1)
        is_sales_excluded = sales_risk_score >= 50.0

        # Component scores summing to overall score
        c_role_fit = round(min(15.0, (role_score / 10.0) * 15.0), 1)
        c_eligibility = round(min(10.0, (edu_score / 10.0) * 10.0), 1)
        c_hiring_prob = round(min(15.0, (prob_interview / 10.0) * 15.0), 1)
        c_comp_quality = round(min(10.0, (comp_quality / 10.0) * 10.0), 1)
        c_compensation = round(min(10.0, (salary_score / 10.0) * 10.0), 1)
        c_learning = 9.0 if is_tier_1 else 7.5
        c_ai_relevance = 8.5 if any(w in combined_text for w in ["ai", "prompt", "workflow", "automation", "data", "reporting", "advisory", "analyst"]) else 7.0
        c_career_capital = round(min(10.0, (career_upside / 10.0) * 10.0), 1)
        c_growth = 4.5 if is_tier_1 else 3.5
        c_location = round(min(5.0, (loc_score / 10.0) * 5.0), 1)

        component_scores = {
            "role_fit": c_role_fit,
            "eligibility": c_eligibility,
            "hiring_probability": c_hiring_prob,
            "company_quality": c_comp_quality,
            "compensation": c_compensation,
            "learning": c_learning,
            "ai_relevance": c_ai_relevance,
            "career_capital": c_career_capital,
            "growth": c_growth,
            "location": c_location
        }

        if is_sales_excluded:
            overall_score = round(max(15.0, min(45.0, sum(component_scores.values()) - sales_risk_score)), 1)
        else:
            overall_score = round(sum(component_scores.values()), 1)

        effort_factor = max(1.0, 10.0 - app_difficulty)
        strategic_index = round(((role_score + exp_score)/2 * prob_interview * career_upside * network_score) / (effort_factor * 10), 2)

        if is_sales_excluded:
            recommendation = "EXCLUDED_SALES_RISK"
        elif overall_score >= 80.0:
            if "global business operations & bd analyst" in title_lower:
                recommendation = "HIGH_PRIORITY_OUTREACH"
            elif "bd" in title_lower and "operations" not in title_lower:
                recommendation = "HIGH_PRIORITY_OUTREACH"
            else:
                recommendation = "PRIORITY_1_TARGET_APPLY_AND_INMAIL"
        elif overall_score >= 78.0:
            recommendation = "HIGH_PRIORITY_OUTREACH"
        elif overall_score >= 65.0:
            recommendation = "STANDARD_APPLICATION"
        else:
            recommendation = "EXPLORATORY_MONITORING"

        why_category = "business_operations" if any(w in combined_text for w in ["operations", "operational", "risk", "advisory", "process"]) else "commercial_strategy"
        why_text = f"Strong alignment with candidate verified background in {why_category} and execution excellence at {company_name}."

        explanation = {
            "why": why_text,
            "evidence": [
                "Aero India 2025 ground operations leadership under strict protocol",
                "Puma India & Tata Communications high-visibility brand activations",
                "Vendor SLA governance and logistics rate card modeling",
                "AI-augmented data synthesis & workflow automation"
            ],
            "missing_requirements": [k for k in ["SQL certification", "Enterprise ERP specialization"] if k.lower() in jd_lower],
            "risks": ["Cold sales / commission quota risk"] if sales_risk_score > 0 else [],
            "strongest_advantages": [
                f"Verified track record matching {why_category}",
                "Bengaluru metro/commute optimization",
                "Tier-1 network leverage" if is_tier_1 else "Fast operational deployment"
            ],
            "recommended_action": (
                "Do not pursue - role poses high quota/cold-calling sales risk." if is_sales_excluded else
                "Dispatch Touch 1 outreach InMail to matched talent partner and submit tailored application package."
            )
        }

        return {
            "job_title": job_title,
            "company": company_name,
            "is_tier_1_enterprise": is_tier_1,
            "overall_opportunity_score": overall_score,
            "strategic_leverage_index": strategic_index,
            "is_sales_excluded": is_sales_excluded,
            "sales_risk_score": sales_risk_score,
            "component_scores": component_scores,
            "explanation": explanation,
            "score_breakdown": {
                "role_fit": role_score,
                "skill_fit": skill_score,
                "education_fit": edu_score,
                "experience_fit": exp_score,
                "location_fit": loc_score,
                "salary_fit": salary_score,
                "company_quality": comp_quality,
                "career_upside": career_upside,
                "network_access": network_score,
                "application_difficulty": app_difficulty,
                "competition_assessment": competition_score,
                "probability_of_interview": prob_interview
            },
            "recommendation": recommendation
        }
