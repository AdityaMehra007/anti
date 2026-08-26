"""
OFFER ENGINE
Analyzes compensation packages: CTC, base, variable, bonus, benefits, probation, notice period.
Distingushes VERIFIED, ESTIMATED, UNVERIFIED market benchmarks.
Generates structured, professional negotiation strategies.
"""
from typing import Dict, Any, Optional

class OfferEngine:
    @staticmethod
    def analyze_offer(offer_dict: Dict[str, Any]) -> Dict[str, Any]:
        ctc = float(offer_dict.get("ctc_annual", 0.0))
        base = float(offer_dict.get("base_salary", ctc * 0.75))
        variable = float(offer_dict.get("variable_pay", ctc * 0.15))
        bonus = float(offer_dict.get("joining_bonus", 0.0))
        company = offer_dict.get("company_name", "Target Company")
        role = offer_dict.get("role_title", "Specialist Role")

        # Market Benchmark (Estimated for early-career Bangalore GCC/MNC)
        benchmark_min = 600000.0
        benchmark_max = 950000.0
        competitiveness = "ABOVE_MARKET" if ctc >= benchmark_max else ("COMPETITIVE" if ctc >= benchmark_min else "BELOW_MARKET")

        strategy = [
            f"1. Base Salary Optimization: Request 8-12% upward adjustment on fixed component (currently INR {base:,.0f}).",
            "2. Signing Bonus Leverage: Propose a one-time joining bonus if fixed base cannot be moved.",
            "3. Growth Milestone: Request an accelerated 6-month performance review cycle for promotion track."
        ]

        return {
            "company": company,
            "role": role,
            "ctc_annual": ctc,
            "base_salary": base,
            "variable_pay": variable,
            "joining_bonus": bonus,
            "market_competitiveness": competitiveness,
            "benchmark_range_estimated": f"INR {benchmark_min:,.0f} - {benchmark_max:,.0f}",
            "negotiation_strategy": strategy,
            "evidence_class": "ESTIMATED_BENCHMARK"
        }

offer_engine = OfferEngine()
