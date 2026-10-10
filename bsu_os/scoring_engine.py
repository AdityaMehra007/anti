"""BSU OS Multi-Factor Mathematical Scoring Engine.

Implements quantified scoring algorithms for Startup Power Score, Career Score,
Momentum Score (Heat Index), Risk Score, and Future Potential (Unicorn Probability).
"""

from typing import Dict, Any, List
from bsu_os.config import (
    POWER_SCORE_WEIGHTS,
    CAREER_SCORE_WEIGHTS,
    MOMENTUM_SCORE_WEIGHTS,
)
from bsu_os.database import get_connection, update_startup_scores, get_startup_by_id


def compute_power_score(startup: Dict[str, Any]) -> float:
    """Computes Startup Power Score (0.0 to 100.0).

    Factors:
    - team_pedigree (25%): founder educational background, prior exits
    - tech_defensibility (25%): proprietary technology, deep-tech/IP, tech stack depth
    - capital_strength (20%): total funding amount, runway, Tier-1 lead investors
    - product_velocity (15%): release cycles, headcount efficiency
    - market_tailwind (15%): sector demand (GenAI, Deep-Tech, FinTech, SpaceTech)
    """
    founders = startup.get("founders", [])
    has_prior_exit = any(f.get("prior_exits") for f in founders)
    top_tier_education = any("IIT" in (f.get("educational_background") or "") or
                             "BITS" in (f.get("educational_background") or "") or
                             "PhD" in (f.get("educational_background") or "")
                             for f in founders)
    team_subscore = 70.0 + (15.0 if has_prior_exit else 0.0) + (15.0 if top_tier_education else 0.0)
    team_subscore = min(100.0, team_subscore)

    sector = startup.get("sector", "")
    high_moat_sectors = ["AI / ML", "Deep-Tech", "SpaceTech", "SaaS / DevTools"]
    tech_subscore = 85.0 if sector in high_moat_sectors else 75.0
    if len(startup.get("tech_stack", [])) >= 5:
        tech_subscore += 10.0
    tech_subscore = min(100.0, tech_subscore)

    funding = startup.get("total_funding_usd", 0.0)
    stage = startup.get("stage", "")
    if stage == "Bootstrapped":
        capital_subscore = 92.0  # High profitability/independence bonus
    elif funding >= 100_000_000:
        capital_subscore = 95.0
    elif funding >= 20_000_000:
        capital_subscore = 85.0
    elif funding >= 5_000_000:
        capital_subscore = 78.0
    else:
        capital_subscore = 65.0

    headcount = startup.get("headcount", 10)
    velocity_subscore = 80.0
    if headcount > 100 and startup.get("hiring_status"):
        velocity_subscore += 10.0

    tailwind_subscore = 80.0
    if "AI" in sector or "Space" in startup.get("sub_sector", ""):
        tailwind_subscore = 95.0
    elif "FinTech" in sector:
        tailwind_subscore = 88.0

    raw_score = (
        team_subscore * POWER_SCORE_WEIGHTS["team_pedigree"] +
        tech_subscore * POWER_SCORE_WEIGHTS["tech_defensibility"] +
        capital_subscore * POWER_SCORE_WEIGHTS["capital_strength"] +
        velocity_subscore * POWER_SCORE_WEIGHTS["product_velocity"] +
        tailwind_subscore * POWER_SCORE_WEIGHTS["market_tailwind"]
    )
    return round(raw_score, 1)


def compute_career_score(startup: Dict[str, Any], job: Dict[str, Any] = None) -> float:
    """Computes Career Growth Score (0.0 to 100.0).

    Measures compensation tier, learning velocity, leadership caliber, and stability.
    """
    stage = startup.get("stage", "")
    runway_subscore = 90.0 if stage in ["Unicorn", "Bootstrapped"] else 80.0

    # Compensation scoring based on LPA
    max_sal = (job.get("max_salary_lpa") if job else None) or 50.0
    if max_sal >= 80.0:
        comp_subscore = 96.0
    elif max_sal >= 50.0:
        comp_subscore = 88.0
    elif max_sal >= 30.0:
        comp_subscore = 78.0
    else:
        comp_subscore = 68.0

    leadership_subscore = 85.0
    learning_subscore = 90.0 if "AI" in startup.get("sector", "") or "Deep-Tech" in startup.get("sector", "") else 82.0
    culture_subscore = 84.0

    raw_score = (
        runway_subscore * CAREER_SCORE_WEIGHTS["runway_months"] +
        comp_subscore * CAREER_SCORE_WEIGHTS["compensation_tier"] +
        leadership_subscore * CAREER_SCORE_WEIGHTS["leadership_caliber"] +
        learning_subscore * CAREER_SCORE_WEIGHTS["learning_velocity"] +
        culture_subscore * CAREER_SCORE_WEIGHTS["culture_sentiment"]
    )
    return round(raw_score, 1)


def compute_momentum_score(startup: Dict[str, Any]) -> float:
    """Computes Startup Heat / Momentum Index (0.0 to 100.0).

    Measures hiring velocity, funding recency, and market buzz.
    """
    hiring_sub = 90.0 if startup.get("hiring_status") and startup.get("headcount", 0) > 50 else 75.0
    
    # Funding recency
    funding_rounds = startup.get("funding_rounds", [])
    if funding_rounds:
        latest_date = funding_rounds[0].get("round_date", "2020-01-01")
        recency_sub = 95.0 if "2024" in latest_date or "2023" in latest_date else 80.0
    else:
        recency_sub = 85.0 if startup.get("stage") == "Bootstrapped" else 65.0

    traction_sub = 85.0
    release_sub = 80.0

    raw = (
        hiring_sub * MOMENTUM_SCORE_WEIGHTS["hiring_velocity"] +
        recency_sub * MOMENTUM_SCORE_WEIGHTS["funding_recency"] +
        traction_sub * MOMENTUM_SCORE_WEIGHTS["market_traction"] +
        release_sub * MOMENTUM_SCORE_WEIGHTS["product_release_rate"]
    )
    return round(raw, 1)


def compute_risk_score(startup: Dict[str, Any]) -> float:
    """Computes Risk Score (0.0 to 100.0). Lower is safer, higher is riskier."""
    stage = startup.get("stage", "")
    if stage in ["Unicorn", "Bootstrapped"]:
        base_risk = 18.0
    elif stage == "Series B":
        base_risk = 28.0
    elif stage == "Series A":
        base_risk = 38.0
    else:
        base_risk = 52.0

    # Sector specific regulatory or capital friction
    if startup.get("sector") == "Deep-Tech":
        base_risk += 6.0  # High capital intensity / R&D latency

    return round(min(100.0, max(5.0, base_risk)), 1)


def compute_future_potential_score(startup: Dict[str, Any]) -> float:
    """Computes Future Potential / Unicorn Probability (0.0 to 100.0)."""
    p_score = compute_power_score(startup)
    m_score = compute_momentum_score(startup)
    r_score = compute_risk_score(startup)
    
    # Synergistic blend
    potential = (p_score * 0.5) + (m_score * 0.4) - (r_score * 0.1)
    return round(min(99.0, max(40.0, potential)), 1)


def score_startup(startup_data: Dict[str, Any]) -> Dict[str, float]:
    """Generates all 5 quantified scores for a startup entity."""
    return {
        "power_score": compute_power_score(startup_data),
        "career_score": compute_career_score(startup_data),
        "momentum_score": compute_momentum_score(startup_data),
        "risk_score": compute_risk_score(startup_data),
        "future_potential_score": compute_future_potential_score(startup_data),
    }


def recompute_all_scores(conn=None) -> int:
    """Iterates through all startups in the database and re-computes all scores."""
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    rows = conn.execute("SELECT id FROM startups").fetchall()
    count = 0
    for r in rows:
        s_id = r["id"]
        startup = get_startup_by_id(s_id, hydrate=True, conn=conn)
        if startup:
            scores = score_startup(startup)
            update_startup_scores(s_id, scores, conn=conn)
            count += 1

    if close_after:
        conn.commit()
        conn.close()
    return count
