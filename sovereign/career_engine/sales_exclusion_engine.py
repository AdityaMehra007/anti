"""
ADI CAREER OS — SALES EXCLUSION ENGINE (Section 11)
Explicitly detects and deprioritizes sales-heavy roles.
Inspects job titles, responsibilities, KPIs, compensation structures, and cold outreach indicators.
Outputs sales_risk_score (0-100) and risk taxonomy.
"""

import re
from typing import Dict, List, Any, Optional

class SalesExclusionEngine:
    """
    Evaluates job postings to protect the candidate from disguised sales roles.
    Candidate explicitly excludes: BDE, BDM, SDR, BDR, field sales, telecalling,
    telesales, commission-only, lead generation, door-to-door, quota-driven acquisition.
    """

    DISQUALIFIED_TITLES = [
        r"\bbde\b", r"\bbdm\b", r"\bsdr\b", r"\bbdr\b",
        r"\bbusiness\s+development\s+(executive|associate|trainee|representative|manager|intern)\b",
        r"\bsales\s+(executive|representative|associate|officer|trainee|manager|specialist|lead|intern|agent)\b",
        r"\bfield\s+sales\b", r"\bdirect\s+sales\b", r"\binsurance\s+sales\b",
        r"\breal\s+estate\s+sales\b", r"\btelecalling\b", r"\btelesales\b",
        r"\btele-sales\b", r"\btele-caller\b", r"\btelecaller\b",
        r"\binside\s+sales\b", r"\boutbound\s+sales\b", r"\bdoor\s*to\s*door\b",
        r"\bappointment\s+setter\b", r"\bmlm\b", r"\bnetwork\s+marketing\b"
    ]

    HIGH_RISK_KEYWORDS = {
        # High impact penalties (15-25 pts each)
        "cold calling": 25,
        "cold calls": 25,
        "cold call": 25,
        "cold outreach": 20,
        "telecalling": 25,
        "telesales": 25,
        "door to door": 25,
        "field visits": 20,
        "client acquisition targets": 20,
        "revenue targets": 15,
        "monthly quota": 20,
        "quarterly quota": 20,
        "sales quota": 25,
        "commission only": 30,
        "commission based": 20,
        "variable pay structure": 15,
        "uncapped incentives": 20,
        "lead generation": 15,
        "generating leads": 15,
        "pitching products": 15,
        "closing deals": 15,
        "pipeline conversion": 10,
        "b2b sales": 15,
        "b2c sales": 25,
        "customer acquisition": 15,
        "conversion rate targets": 10,
        "prospecting leads": 15,
        "selling solutions": 15
    }

    TARGET_SAFE_KEYWORDS = [
        "operations", "process improvement", "business analysis", "workflow automation",
        "data analysis", "sop", "standard operating procedure", "reporting",
        "dashboard", "sql", "excel", "power bi", "strategy & operations",
        "product operations", "supply chain", "logistics", "risk analysis",
        "quality assurance", "compliance", "cross-functional coordination"
    ]

    @classmethod
    def evaluate(cls, title: str, description: str = "", responsibilities: Optional[List[str]] = None,
                 compensation_type: str = "fixed") -> Dict[str, Any]:
        """
        Evaluates title and description, returning sales_risk_score (0-100),
        disqualification flag, flagged terms, and detailed explanation.
        """
        score = 0
        flagged_signals = []
        clean_title = (title or "").lower().strip()
        desc_text = (description or "").lower()
        if responsibilities:
            desc_text += " " + " ".join(responsibilities).lower()

        # 1. Title Disqualification Checks (Immediate 50-80 base risk)
        for pat in cls.DISQUALIFIED_TITLES:
            if re.search(pat, clean_title):
                match_str = re.search(pat, clean_title).group(0)
                score += 60
                flagged_signals.append(f"Disqualified sales title pattern matched: '{match_str}'")
                break

        # Check for disguised titles (e.g. 'Associate - BD' or 'Growth Specialist')
        if "growth" in clean_title and "analyst" not in clean_title and "product" not in clean_title:
            score += 20
            flagged_signals.append("Growth title without analytical qualifier")
        if "business development" in clean_title and "operations" not in clean_title:
            score += 40
            flagged_signals.append("Business Development title lacking Operations qualifier")

        # 2. Description & Responsibilities Keyword Density Analysis
        matched_kw_count = 0
        for kw, weight in cls.HIGH_RISK_KEYWORDS.items():
            occurrences = len(re.findall(r"\b" + re.escape(kw) + r"\b", desc_text))
            if occurrences > 0:
                kw_impact = min(weight * occurrences, weight * 2)
                score += kw_impact
                matched_kw_count += occurrences
                flagged_signals.append(f"Sales indicator found: '{kw}' ({occurrences}x)")

        # 3. Compensation Structure Penalties
        comp_lower = compensation_type.lower()
        if "commission" in comp_lower or "variable" in comp_lower or "incentive" in comp_lower:
            score += 25
            flagged_signals.append(f"Commission/Incentive-weighted compensation: '{compensation_type}'")

        # 4. Mitigating Factors (Genuine Operations / Analysis content)
        safe_matches = sum(1 for sk in cls.TARGET_SAFE_KEYWORDS if re.search(r"\b" + re.escape(sk) + r"\b", desc_text))
        if safe_matches >= 4 and not any("cold call" in sig or "quota" in sig for sig in flagged_signals):
            # Mitigate if it's clearly an operations role (e.g. Sales Operations / Revenue Operations)
            mitigation = min(safe_matches * 3, 20)
            score = max(0, score - mitigation)

        # Cap score at 100
        sales_risk_score = min(100, max(0, score))

        # Risk Classification
        if sales_risk_score >= 60:
            risk_level = "CRITICAL_DISQUALIFIED"
            is_disqualified = True
        elif sales_risk_score >= 40:
            risk_level = "HIGH_SALES_RISK"
            is_disqualified = True
        elif sales_risk_score >= 20:
            risk_level = "MODERATE_SUSPICIOUS"
            is_disqualified = False
        else:
            risk_level = "SAFE_NON_SALES"
            is_disqualified = False

        explanation = (
            f"Sales Risk Score {sales_risk_score}/100 ({risk_level}). "
            f"Detected {len(flagged_signals)} sales signals. "
            f"{'Strictly disqualified from candidate application pipeline.' if is_disqualified else 'Eligible for candidate operations pipeline.'}"
        )

        return {
            "sales_risk_score": sales_risk_score,
            "risk_level": risk_level,
            "is_disqualified": is_disqualified,
            "flagged_signals": flagged_signals,
            "safe_signals_count": safe_matches,
            "explanation": explanation
        }
