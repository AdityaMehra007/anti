"""
compensation_strategist.py - Agent 6: Compensation Benchmark & Negotiation Strategist
======================================================================================
Calculates market compensation percentiles for Bangalore and Pan-India corporate roles,
deconstructs total CTC packages, and provides tactical counter-offer negotiation scripts.
"""

from typing import Dict, List, Any
from apex_career_os.core.truth_layer import get_candidate_profile

class CompensationStrategistAgent:
    def __init__(self):
        self.candidate = get_candidate_profile()

    def benchmark_role_compensation(self, track: str, company_tier: str = "Tier 1 MNC") -> Dict[str, Any]:
        """Provides data-driven salary benchmarks for Bangalore early-career roles."""
        benchmarks = {
            "Operations & Vendor Governance": {
                "25th_percentile_lpa": 5.5,
                "50th_percentile_median_lpa": 7.2,
                "75th_percentile_lpa": 9.0,
                "90th_percentile_lpa": 11.5,
                "recommended_anchor_lpa": 8.0,
                "structure": {"fixed_base_percent": 80, "performance_variable_percent": 15, "joining_retention_percent": 5}
            },
            "B2B Sales & Business Development": {
                "25th_percentile_lpa": 5.0,
                "50th_percentile_median_lpa": 7.5,
                "75th_percentile_lpa": 10.0,
                "90th_percentile_lpa": 13.5,
                "recommended_anchor_lpa": 8.5,
                "structure": {"fixed_base_percent": 65, "performance_variable_percent": 30, "joining_retention_percent": 5}
            },
            "AI & Data Operations": {
                "25th_percentile_lpa": 6.0,
                "50th_percentile_median_lpa": 7.8,
                "75th_percentile_lpa": 9.5,
                "90th_percentile_lpa": 12.0,
                "recommended_anchor_lpa": 8.5,
                "structure": {"fixed_base_percent": 85, "performance_variable_percent": 10, "joining_retention_percent": 5}
            },
            "International Trade & EXIM Logistics": {
                "25th_percentile_lpa": 5.2,
                "50th_percentile_median_lpa": 6.8,
                "75th_percentile_lpa": 8.5,
                "90th_percentile_lpa": 10.5,
                "recommended_anchor_lpa": 7.5,
                "structure": {"fixed_base_percent": 80, "performance_variable_percent": 15, "joining_retention_percent": 5}
            }
        }

        matched_data = benchmarks.get(track, benchmarks["Operations & Vendor Governance"])
        
        # Boost for top-tier MNCs or Tier 1 tech
        tier_multiplier = 1.15 if "Tier 1" in company_tier or "Unicorn" in company_tier else 1.0

        return {
            "track": track,
            "company_tier": company_tier,
            "p25_lpa": round(matched_data["25th_percentile_lpa"] * tier_multiplier, 2),
            "median_p50_lpa": round(matched_data["50th_percentile_median_lpa"] * tier_multiplier, 2),
            "p75_lpa": round(matched_data["75th_percentile_lpa"] * tier_multiplier, 2),
            "p90_aspirational_lpa": round(matched_data["90th_percentile_lpa"] * tier_multiplier, 2),
            "recommended_opening_anchor_lpa": round(matched_data["recommended_anchor_lpa"] * tier_multiplier, 2),
            "recommended_package_breakdown": matched_data["structure"]
        }

    def generate_negotiation_playbook(self, company: str, offered_ctc_lpa: float, target_ctc_lpa: float = 8.0) -> Dict[str, str]:
        """Generates tactical negotiation scripts for HR verbal and written discussions."""
        gap = round(target_ctc_lpa - offered_ctc_lpa, 2)

        phone_script = f"""HR: 'We are pleased to extend an offer of INR {offered_ctc_lpa} LPA.'

Aditya: 'Thank you so much! I am genuinely thrilled about the team and the operational mandate at {company}. Based on my market research for this scope in Bangalore, as well as my track record delivering 300+ deployments, 15% direct vendor cost reductions, and immediate Day-1 availability, I was anticipating a total package closer to INR {target_ctc_lpa} LPA. If we can bridge this closer to INR {target_ctc_lpa} LPA—whether through the fixed base or a performance/joining milestone—I am ready to sign and commit immediately.'"""

        counter_email = f"""Subject: Offer Follow-up & Discussion — Aditya Mehra ({company})

Dear Hiring & Compensation Team,

Thank you very much for extending the offer to join {company} as part of your team. I am very excited about the mission and the chance to contribute directly to your operational velocity.

After carefully reviewing the offer of INR {offered_ctc_lpa} LPA, I would like to explore whether there is flexibility to align the total package closer to INR {target_ctc_lpa} LPA. 

Given my hands-on operational leadership managing 100,000+ visitors at Aero India 2025 with zero shrinkage, my proven ability to eliminate 15% in vendor overhead, and my immediate availability (0 days notice period), I am confident I will deliver outsized ROI within my first 90 days.

If adjusting the base is constrained, I would gladly consider an initial joining bonus or an accelerated 6-month performance review milestone.

I am enthusiastic about joining {company} and look forward to finalizing our partnership.

Warm regards,

Aditya Mehra
{self.candidate.phone}"""

        return {
            "verbal_phone_counter_script": phone_script,
            "formal_counter_email": counter_email,
            "tactical_guidance": (
                "1. Always express high enthusiasm first.\n"
                "2. Anchor on proven metrics (15% vendor savings, 100k visitor throughput, 0 days notice).\n"
                "3. Offer trade-off levers: Fixed base, joining bonus, or a 6-month performance review fast-track."
            )
        }
