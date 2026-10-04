#!/usr/bin/env python3
"""
scripts/offer_negotiator.py — Automated Compensation & Offer Negotiation Engine
================================================================================
Part of the OMEGA Sovereign Autonomous System.
Models Bangalore GCC operations compensation brackets and generates structured,
high-leverage counter-offer letters and strategy briefs for Aditya Mehra.
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, Any

REPO_ROOT = Path(__file__).resolve().parent.parent
OFFERS_DIR = REPO_ROOT / "applications_generated" / "offer_strategies"
OFFERS_DIR.mkdir(parents=True, exist_ok=True)

GCC_BENCHMARKS = {
    "entry_operations_floor": 650000,
    "market_median_base": 850000,
    "top_quartile_target": 950000,
    "elite_stretch_ceiling": 1100000,
}

class OfferNegotiator:
    """Calculates compensation leverage and generates counter-offer strategies."""

    @staticmethod
    def evaluate_offer(offered_ctc: float) -> Dict[str, Any]:
        """Evaluates an initial offer against Bangalore GCC operations benchmarks."""
        if offered_ctc < GCC_BENCHMARKS["entry_operations_floor"]:
            rating = "BELOW_MARKET"
            recommended_counter = GCC_BENCHMARKS["market_median_base"]
            stance = "FIRM_UPWARD_REVISION"
        elif offered_ctc < GCC_BENCHMARKS["market_median_base"]:
            rating = "FAIR_ENTRY"
            recommended_counter = GCC_BENCHMARKS["top_quartile_target"]
            stance = "STANDARD_TOP_TIER_COUNTER"
        elif offered_ctc < GCC_BENCHMARKS["elite_stretch_ceiling"]:
            rating = "STRONG_TARGET"
            recommended_counter = GCC_BENCHMARKS["elite_stretch_ceiling"]
            stance = "SIGN_ON_AND_BONUS_OPTIMIZATION"
        else:
            rating = "TOP_PERCENTILE"
            recommended_counter = offered_ctc * 1.08
            stance = "RAPID_ACCEPTANCE_WITH_PERFORMANCE_REVIEW"

        diff = recommended_counter - offered_ctc
        return {
            "offered_ctc": offered_ctc,
            "rating": rating,
            "recommended_counter": recommended_counter,
            "delta_inr": diff,
            "delta_percentage": round((diff / offered_ctc) * 100, 1) if offered_ctc > 0 else 0,
            "stance": stance
        }

    @classmethod
    def generate_counter_letter(cls, company_name: str, role_title: str, offered_ctc: float) -> Dict[str, Any]:
        """Generates a professional counter-offer letter for Aditya Mehra."""
        eval_result = cls.evaluate_offer(offered_ctc)
        counter_val = eval_result["recommended_counter"]

        body = f"""Subject: Regarding the Offer for {role_title} — Aditya Mehra

Dear Hiring Team at {company_name},

Thank you very much for extending the offer to join {company_name} as {role_title}. I am truly impressed by the team's operational vision and the scale of the initiatives we discussed during our interviews.

Given the scope of the responsibilities and the direct contribution I will be delivering from Day 1—combining my high-concurrency operations leadership from AERO India 2025 with proven 99.2% QA data accuracy at Instawork—I would like to discuss the compensation package.

Based on current Bangalore GCC operations benchmarks for multi-skilled operational leaders and the unique blend of field execution and data discipline I bring, I am targeting a total CTC in the range of INR {counter_val:,.0f}. 

If we can align around this figure, I am prepared to sign the offer immediately and begin onboarding preparations. Alternatively, if base flexibility is constrained, I would be very open to exploring a joining incentive or a structured 6-month performance evaluation milestone.

Thank you once again for your confidence in my candidacy. I am eager to make an immediate impact at {company_name} and look forward to your thoughts.

Warm regards,

Aditya Mehra
BBA International Business | Dayananda Sagar University ('26)
Bangalore, India
Phone: +91 99000 00000 | Email: aditya.mehra@example.com
"""
        filename = f"{company_name.replace(' ', '_')}_{role_title.replace(' ', '_')}_counter.md"
        filepath = OFFERS_DIR / filename
        filepath.write_text(body, encoding="utf-8")

        return {
            "company": company_name,
            "role": role_title,
            "evaluation": eval_result,
            "letter_path": str(filepath)
        }

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    comp = sys.argv[1] if len(sys.argv) > 1 else "Amazon India"
    role = sys.argv[2] if len(sys.argv) > 2 else "Operations Specialist"
    offer = float(sys.argv[3]) if len(sys.argv) > 3 else 700000.0

    res = OfferNegotiator.generate_counter_letter(comp, role, offer)
    print(f"[OK] Evaluated offer for {comp}: {res['evaluation']['rating']}")
    print(f"[OK] Counter generated: {res['letter_path']} targeting INR {res['evaluation']['recommended_counter']:,.0f}")
