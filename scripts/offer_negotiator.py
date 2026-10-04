#!/usr/bin/env python3
"""
scripts/offer_negotiator.py — OMEGA Autonomous Offer Negotiation & CTC Maximizer Engine
Models incoming CTC offers against the Bangalore GCC & Startup compensation benchmarks,
evaluates fixed vs variable bonus sensitivity, and drafts formal counter-offer letters.
Supports both instance-based API and legacy static/class API for complete backward compatibility.
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, Union

ROOT_DIR = Path(__file__).resolve().parent.parent
OFFERS_DIR = ROOT_DIR / "applications_generated" / "offer_strategies"
OFFERS_DIR.mkdir(parents=True, exist_ok=True)

# Canonical benchmark dictionaries
BANGALORE_GCC_BENCHMARKS = {
    "P25_BASELINE": 6.5,    # 25th percentile entry CTC (in Lakhs INR)
    "P50_MEDIAN": 8.5,      # 50th percentile market median CTC
    "P75_PREMIUM": 10.5,    # 75th percentile top-tier performer CTC
    "P90_ELITE": 12.0       # 90th percentile high-growth unicorn/GCC cap
}

# Legacy benchmark dictionary in INR
GCC_BENCHMARKS = {
    "entry_operations_floor": 650000,
    "market_median_base": 850000,
    "top_quartile_target": 950000,
    "elite_stretch_ceiling": 1100000,
}


class OfferNegotiator:
    """Evaluates offers and constructs executive counter-offers for Aditya Mehra."""

    def __init__(self, candidate_name: str = "Aditya Mehra"):
        self.candidate_name = candidate_name
        self.benchmarks = BANGALORE_GCC_BENCHMARKS

    @classmethod
    def evaluate_offer(cls, offered_ctc: float) -> Dict[str, Any]:
        """
        Evaluates offer compensation.
        Supports both Lakhs (e.g. 5.5, 7.5, 9.5) and absolute INR (e.g. 550000, 750000).
        Returns a dict compatible with both test suites.
        """
        is_absolute_inr = offered_ctc > 1000.0

        if is_absolute_inr:
            # Absolute INR evaluation
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
                recommended_counter = round(offered_ctc * 1.08, 2)
                stance = "RAPID_ACCEPTANCE_WITH_PERFORMANCE_REVIEW"

            diff = recommended_counter - offered_ctc
            return {
                "offered_ctc": offered_ctc,
                "offered_ctc_lpa": round(offered_ctc / 100000.0, 2),
                "rating": rating,
                "standing": rating,
                "recommended_counter": recommended_counter,
                "suggested_counter_ctc_lpa": round(recommended_counter / 100000.0, 2),
                "delta_inr": diff,
                "net_gain_inr": int(diff),
                "delta_percentage": round((diff / offered_ctc) * 100, 1) if offered_ctc > 0 else 0,
                "percentage_bump": round((diff / offered_ctc) * 100, 1) if offered_ctc > 0 else 0,
                "stance": stance
            }
        else:
            # Lakhs evaluation (e.g. 5.5, 7.5, 8.0)
            median = BANGALORE_GCC_BENCHMARKS["P50_MEDIAN"]
            p75 = BANGALORE_GCC_BENCHMARKS["P75_PREMIUM"]

            if offered_ctc < BANGALORE_GCC_BENCHMARKS["P25_BASELINE"]:
                standing = "BELOW_MARKET"
                suggested_counter = median
            elif offered_ctc < median:
                standing = "MARKET_ENTRY"
                suggested_counter = round(offered_ctc * 1.20, 2)
            elif offered_ctc < p75:
                standing = "COMPETITIVE_MEDIAN"
                suggested_counter = round(min(offered_ctc * 1.15, p75), 2)
            else:
                standing = "TOP_TIER_ELITE"
                suggested_counter = round(offered_ctc * 1.08, 2)

            counter_diff = round(suggested_counter - offered_ctc, 2)
            percentage_bump = round((counter_diff / offered_ctc) * 100, 1)

            return {
                "offered_ctc": int(offered_ctc * 100000),
                "offered_ctc_lpa": offered_ctc,
                "standing": standing,
                "rating": standing,
                "p50_benchmark_lpa": median,
                "p75_benchmark_lpa": p75,
                "suggested_counter_ctc_lpa": suggested_counter,
                "recommended_counter": int(suggested_counter * 100000),
                "net_gain_inr": int(counter_diff * 100_000),
                "percentage_bump": percentage_bump
            }

    @classmethod
    def generate_counter_letter(
        cls,
        company: str,
        role: str,
        offered_ctc: float,
        hiring_manager: str = "Hiring Team"
    ) -> Union[str, Dict[str, Any]]:
        """
        Drafts a formal, polite, high-leverage executive counter-negotiation letter.
        Supports both string output and dict with file output for test suites.
        """
        is_absolute_inr = offered_ctc > 1000.0
        eval_metrics = cls.evaluate_offer(offered_ctc)

        if is_absolute_inr:
            offered_lpa = offered_ctc / 100000.0
            counter_val = eval_metrics["recommended_counter"]
            counter_lpa = counter_val / 100000.0
            counter_display = f"INR {counter_val:,.0f}"
        else:
            offered_lpa = offered_ctc
            counter_lpa = eval_metrics["suggested_counter_ctc_lpa"]
            counter_display = f"₹{counter_lpa:.2f}L CTC"

        letter = f"""Subject: Re: Offer of Employment — {role} | Aditya Mehra

Dear {hiring_manager},

Thank you very much for extending the offer to join {company} as {role}. I am genuinely enthusiastic about the company's trajectory and the high-impact operational responsibilities outlined throughout our discussions.

Having reviewed the offer package of ₹{offered_lpa:.2f}L CTC, and considering the cross-functional scope of the role, I would like to discuss adjusting the compensation structure to {counter_display}.

This adjustment is grounded in my proven on-ground operational execution capabilities:
1. High-Precision Execution & QA Standard: Delivered a verified 99.2% QA Precision rating on Instawork's AI data operations pipeline, eliminating manual reconciliation overhead.
2. Large-Scale Event Logistics & Defense Protocols: Led VIP airside transport, protocol management, and zero-loss inventory staging across 100,000+ attendees at AERO India 2025 under strict security standards.
3. Rapid Onboarding & Immediate Ownership: With rigorous academic grounding in BBA International Business (Dayananda Sagar University '26) and hands-on vendor SLA governance, I will drive immediate operational stability and margin recovery from Day 1.

I am deeply committed to joining {company} and contributing directly to the team's operational excellence. If we can align on {counter_display}, I am prepared to sign and finalize my acceptance immediately.

Thank you again for your time and consideration. I look forward to your thoughts.

Warm regards,

Aditya Mehra
BBA International Business | Dayananda Sagar University Class of 2026
Bangalore, India | linkedin.com/in/adityamehra007
"""
        # If absolute INR was passed, save file and return dict for test_interview_cockpit
        if is_absolute_inr:
            filename = f"{company.replace(' ', '_')}_{role.replace(' ', '_')}_counter.md"
            filepath = OFFERS_DIR / filename
            filepath.write_text(letter, encoding="utf-8")
            return {
                "company": company,
                "role": role,
                "evaluation": eval_metrics,
                "letter_path": str(filepath)
            }

        return letter


def main():
    parser = argparse.ArgumentParser(description="OMEGA Offer Counter-Negotiation Engine")
    parser.add_argument("--company", type=str, default="Deloitte USI", help="Hiring organization")
    parser.add_argument("--role", type=str, default="Business Operations Associate", help="Target position")
    parser.add_argument("--offered-ctc", type=float, default=7.5, help="Offered CTC in Lakhs INR (LPA)")
    parser.add_argument("--manager", type=str, default="Talent Acquisition Team", help="Contact name")
    parser.add_argument("--export", type=str, default=None, help="Optional markdown file path to save letter")

    args = parser.parse_args()

    negotiator = OfferNegotiator()
    metrics = negotiator.evaluate_offer(args.offered_ctc)
    letter = negotiator.generate_counter_letter(args.company, args.role, args.offered_ctc, args.manager)

    print("=" * 80)
    print(f"  OMEGA CTC OFFER EVALUATOR & EXECUTIVE COUNTER-NEGOTIATOR")
    print("=" * 80)
    print(f"Company:               {args.company}")
    print(f"Role:                  {args.role}")
    print(f"Offered CTC:           ₹{metrics['offered_ctc_lpa']:.2f} Lakhs")
    print(f"Market Standing:       {metrics['standing']}")
    print(f"Suggested Counter CTC: ₹{metrics['suggested_counter_ctc_lpa']:.2f} Lakhs (+{metrics['percentage_bump']}%)")
    print(f"Net Realized Gain:     ₹{metrics['net_gain_inr']:,} INR / year")
    print("-" * 80)
    print("DRAFT COUNTER-OFFER LETTER:")
    print("-" * 80)
    print(letter)
    print("=" * 80)

    if args.export:
        out_path = Path(args.export)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(letter if isinstance(letter, str) else letter["letter_path"], encoding="utf-8")
        print(f"[OK] Exported counter-offer letter to: {out_path}")


if __name__ == "__main__":
    main()
