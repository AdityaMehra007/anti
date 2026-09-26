"""First Zero-Capital Revenue Experiment (EXP-01).

Title: Account-Based B2B Lead Intelligence & Competitor Gap Audit
Opportunity Category: Productized Intelligence Service
Capital Requirement: ₹0 (Bootstrapped via founder time + AI leverage)
Target Market: US/UK Mid-Market B2B SaaS & High-Growth Digital Agencies
"""

from typing import Any
from datetime import datetime
from ..core.config import settings
from ..core.models import CurrencyCode
from ..agents.revenue_commander import revenue_commander
from ..agents.compliance_agent import compliance_agent
from ..core.database import db

THESIS_ATTACK_DEFENSE = {
    "opportunity_thesis": "US/UK mid-market B2B SaaS and agencies actively hire SDRs and waste hundreds of hours on stale lead databases with high bounce rates. Delivering 100% verified decision-makers with specific buying triggers and custom AI icebreakers solves their biggest pipeline bottleneck with ₹0 upfront capital and 95%+ gross margins.",
    "counter_theses_and_refutations": [
        {
            "attack": "Commoditization: Anyone can use Apollo, ZoomInfo, or Lusha directly.",
            "defense": "Standard database tools suffer from 25–40% bounce rates, outdated job changes, and zero contextual trigger intelligence. Mid-market VPs of Sales don't want raw databases—they want verified, zero-bounce pipeline ready for immediate outreach. Proof point: Previous client deliverable achieved 100% zero-bounce verification for Elevate Talent Partners ($600 collected)."
        },
        {
            "attack": "Payment Trust: International clients will hesitate to wire money to a solo founder in India.",
            "defense": "Mitigated by using reputable, compliant international payment rails: Wise Business local ACH routing in USD/GBP and Upwork escrow. Terms provide a clear risk-reversal guarantee: instant 100% replacement for any bounced contact."
        },
        {
            "attack": "Founder Time Trap: Delivering lead lists manually cannot scale.",
            "defense": "Following the Revenue Ladder: Starts as a high-margin founder-assisted service ($56-$72/hour real return), converts into standardized SOPs, integrates automated scrapers/APIs, and transitions into a subscription intelligence feed."
        }
    ]
}

OFFER_SPECIFICATION = {
    "offer_name": "High-Intent B2B Pipeline Accelerator",
    "tier_1_starter": {
        "title": "100 Verified ICP Decision-Makers + Custom AI Icebreakers",
        "price_usd": 450.0,
        "price_inr": 37500.0,
        "delivery_time_days": 2,
        "target_audience": "B2B SaaS companies actively hiring SDRs or expanding sales teams",
        "deliverables": [
            "100 triple-verified decision-maker contacts (Zero bounce guarantee)",
            "Direct work email + verified LinkedIn URL",
            "Identified recent buying trigger (Series A/B funding, hiring, tech rollout)",
            "Hyper-personalized 1-sentence AI icebreaker referencing their specific trigger"
        ]
    },
    "tier_2_growth": {
        "title": "300 Verified Decision-Makers + Competitor Gap Audit Dossier",
        "price_usd": 950.0,
        "price_inr": 78000.0,
        "delivery_time_days": 4,
        "deliverables": [
            "300 triple-verified decision-maker contacts with custom icebreakers",
            "Comprehensive 5-page Competitor Gap Audit Dossier",
            "3-touch tailored cold email sequence copy optimized for reply rate"
        ]
    },
    "payment_terms": "50% prepayment upon kickoff via Wise Business USD payment link; 50% upon delivery review.",
    "tax_compliance": "Export of services under GST Letter of Undertaking (LUT); 0% IGST with mandatory e-FIRC generation."
}


class RevenueExperiment01:
    @staticmethod
    def get_experiment_details() -> dict[str, Any]:
        return {
            "experiment_id": "EXP-01",
            "thesis_defense": THESIS_ATTACK_DEFENSE,
            "offer": OFFER_SPECIFICATION,
            "unit_economics": {
                "capital_required_inr": 0.0,
                "price_inr": 37500.0,
                "delivery_cost_inr": 1500.0,  # AI API usage + verification credits
                "gross_profit_inr": 36000.0,
                "gross_margin_pct": 96.0,
                "statutory_tax_reserve_inr": 37500.0 * settings.DEFAULT_TAX_RESERVE_PCT,
                "net_cash_retained_inr": 37500.0 * (1.0 - settings.DEFAULT_TAX_RESERVE_PCT) - 1500.0
            }
        }

    @staticmethod
    def get_priority_campaign_prospects() -> list[dict[str, Any]]:
        """Extracts the top 5 hot prospects with tailored icebreakers ready for outreach."""
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, company_name, website, contact_name, contact_title,
                       contact_email, location, buying_trigger, custom_icebreaker
                FROM leads
                WHERE lead_score = 'Hot'
                ORDER BY created_at ASC LIMIT 5
            """)
            return [dict(r) for r in cur.fetchall()]

    @staticmethod
    def simulate_deal_won_and_reconciliation(lead_id: str) -> dict[str, Any]:
        """Simulates winning the first client deal, booking revenue, and segregating taxes."""
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
            lead = cur.fetchone()
            if not lead:
                raise ValueError(f"Lead {lead_id} not found.")

        # Record ₹37,500 ($450) collected revenue
        res = revenue_commander.record_collected_revenue(
            client_name=lead["company_name"],
            amount_usd=450.0,
            amount_inr=37500.0,
            service_description=f"EXP-01: 100 Verified ICP Leads + Trigger Icebreakers for {lead['company_name']}"
        )
        return res


exp01 = RevenueExperiment01()
