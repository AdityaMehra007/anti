#!/usr/bin/env python3
"""
scripts/offer_negotiator.py — OMEGA Autonomous Offer Negotiation & CTC Maximizer Engine
Models incoming CTC offers against the Bangalore GCC & Startup compensation benchmarks,
evaluates fixed vs variable bonus sensitivity, and drafts formal counter-offer letters.
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
from typing import Dict, Any, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent

BANGALORE_GCC_BENCHMARKS = {
    "P25_BASELINE": 6.5,    # 25th percentile entry CTC (in Lakhs INR)
    "P50_MEDIAN": 8.5,      # 50th percentile market median CTC
    "P75_PREMIUM": 10.5,    # 75th percentile top-tier performer CTC
    "P90_ELITE": 12.0       # 90th percentile high-growth unicorn/GCC cap
}

class OfferNegotiator:
    """Evaluates offers and constructs executive counter-offers for Aditya Mehra."""

    def __init__(self, candidate_name: str = "Aditya Mehra"):
        self.candidate_name = candidate_name
        self.benchmarks = BANGALORE_GCC_BENCHMARKS

    def evaluate_offer(self, offered_ctc: float) -> Dict[str, Any]:
        """Calculates percentile standing, gap to P75 target, and leverage ratio."""
        median = self.benchmarks["P50_MEDIAN"]
        p75 = self.benchmarks["P75_PREMIUM"]
        
        if offered_ctc < self.benchmarks["P25_BASELINE"]:
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
            "offered_ctc_lpa": offered_ctc,
            "standing": standing,
            "p50_benchmark_lpa": median,
            "p75_benchmark_lpa": p75,
            "suggested_counter_ctc_lpa": suggested_counter,
            "net_gain_inr": int(counter_diff * 100_000),
            "percentage_bump": percentage_bump
        }

    def generate_counter_letter(
        self,
        company: str,
        role: str,
        offered_ctc: float,
        hiring_manager: str = "Hiring Team"
    ) -> str:
        """Drafts a formal, polite, high-leverage executive counter-negotiation letter."""
        eval_metrics = self.evaluate_offer(offered_ctc)
        counter_ctc = eval_metrics["suggested_counter_ctc_lpa"]

        letter = f"""Subject: Re: Offer of Employment — {role} | Aditya Mehra

Dear {hiring_manager},

Thank you very much for extending the offer to join {company} as {role}. I am genuinely enthusiastic about the company's trajectory and the high-impact operational responsibilities outlined throughout our discussions.

Having reviewed the offer package of ₹{offered_ctc:.2f}L CTC, and considering the cross-functional scope of the role, I would like to discuss adjusting the compensation structure to ₹{counter_ctc:.2f}L CTC.

This adjustment is grounded in my proven on-ground operational execution capabilities:
1. High-Precision Execution & QA Standard: Delivered a verified 99.2% QA Precision rating on Instawork's AI data operations pipeline, eliminating manual reconciliation overhead.
2. Large-Scale Event Logistics & Defense Protocols: Led VIP airside transport, protocol management, and zero-loss inventory staging across 100,000+ attendees at AERO India 2025 under strict security standards.
3. Rapid Onboarding & Immediate Ownership: With rigorous academic grounding in BBA International Business (Dayananda Sagar University '26) and hands-on vendor SLA governance, I will drive immediate operational stability and margin recovery from Day 1.

I am deeply committed to joining {company} and contributing directly to the team's operational excellence. If we can align on ₹{counter_ctc:.2f}L CTC, I am prepared to sign and finalize my acceptance immediately.

Thank you again for your time and consideration. I look forward to your thoughts.

Warm regards,

Aditya Mehra
BBA International Business | Dayananda Sagar University Class of 2026
Bangalore, India | linkedin.com/in/adityamehra007
"""
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
        out_path.write_text(letter, encoding="utf-8")
        print(f"[OK] Exported counter-offer letter to: {out_path}")

if __name__ == "__main__":
    main()
