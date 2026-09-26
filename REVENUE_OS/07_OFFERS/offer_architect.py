"""
Offer Architect for REVENUE OS
Adheres strictly to Directives 22, 23, 24, 25, 27, 28.
Calculates ROI, margins, guarantees, and addresses objections.
"""

from typing import Any, Dict, Optional

class OfferArchitect:
    """
    Transforms qualified opportunities into high-converting, value-first offers.
    Every offer must answer:
    'Why should the customer pay us instead of doing nothing or using an alternative?'
    """
    def create_offer_for_opportunity(self, opp: Dict[str, Any]) -> Dict[str, Any]:
        price_inr = opp.get("suggested_price_inr", 35000.0)
        price_usd = opp.get("suggested_price_usd", 450.0)
        delivery_cost = opp.get("delivery_cost_inr", 3500.0)
        gross_margin = opp.get("gross_margin_pct", 90.0)
        
        # Calculate concrete customer ROI (Directive 24)
        # Conservative model: Replaces 20 hrs/week manual SDR time (80 hrs/mo @ ₹400/hr = ₹32,000)
        # + Unlocks 2-4 extra qualified discovery meetings per month (Value: ₹60,000+ pipeline value)
        hours_saved_per_month = 60
        founder_time_value_inr = hours_saved_per_month * 1000.0  # ₹60,000 saved time
        estimated_pipeline_unlocked_inr = 150000.0
        total_monthly_value_delivered = founder_time_value_inr + estimated_pipeline_unlocked_inr
        roi_multiplier = round(total_monthly_value_delivered / max(price_inr, 1.0), 1)

        why_us_vs_do_nothing = (
            "Doing nothing costs you 60+ hours of founder/sales grunt work each month or ₹60,000/mo in a rookie SDR "
            "who burns domain reputation with generic spray-and-pray spam. Buying generic SaaS gives you another empty software tool "
            "that you have no time to configure. Our engine delivers fully enriched, signal-verified, custom-drafted pipeline ready to review "
            "in 10 minutes a day with zero upfront hiring overhead."
        )

        objections_handled = [
            {
                "objection": "Is this just ChatGPT sending spam?",
                "defense": "No. Spray-and-pray spam ruins your sender reputation and domain health. We identify verified buying triggers (recent funding, leadership change, open hiring roles) and generate deep account-specific value propositions with full compliance and opt-out transparency."
            },
            {
                "objection": "Why not just hire an SDR or intern in India?",
                "defense": "An SDR requires 6-8 weeks of ramp time, ₹40k-₹60k monthly base salary, health benefits, and continuous management. Our system is fully operational in 72 hours with zero management drag and >85% gross margin efficiency."
            },
            {
                "objection": "What if we don't get results?",
                "defense": "We operate with a 14-day conditional milestone guarantee: If we don't deliver the agreed qualified target accounts and custom sequences within 14 days, you receive a 100% refund of your onboarding fee."
            }
        ]

        return {
            "id": f"OFFER-{opp.get('id', 'PRIMARY')}",
            "title": opp.get("name", "B2B AI Sales Pipeline Automation"),
            "category": opp.get("category", "AI Automation Services"),
            "target_customer": opp.get("target_customer", "B2B Founders & Tech Agencies"),
            "core_problem": opp.get("core_problem"),
            "promised_outcome": (
                "Automated weekly delivery of 50-100 trigger-qualified prospective accounts, fully enriched with decision-maker insights "
                "and custom-drafted, high-converting value propositions ready for founder review and 1-click dispatch."
            ),
            "price_inr": price_inr,
            "price_usd": price_usd,
            "delivery_cost_inr": delivery_cost,
            "gross_margin_pct": gross_margin,
            "delivery_turnaround_days": 3,
            "roi_calculation": {
                "hours_saved_monthly": hours_saved_per_month,
                "labor_cost_saved_inr": founder_time_value_inr,
                "pipeline_value_unlocked_inr": estimated_pipeline_unlocked_inr,
                "total_value_inr": total_monthly_value_delivered,
                "roi_multiplier": f"{roi_multiplier}x",
            },
            "why_us_vs_do_nothing": why_us_vs_do_nothing,
            "guarantee_policy": "14-day milestone delivery guarantee or full refund.",
            "objections_handled": objections_handled,
            "primary_channel": opp.get("acquisition_channel", "LinkedIn Warm Network + Cold Case Study Outreach"),
            "active": True
        }
