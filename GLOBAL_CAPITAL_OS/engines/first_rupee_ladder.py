"""First Rupee Ladder Engine for GLOBAL CAPITAL OS.

Maps out the deterministic economic progression from ₹1 to ₹1 Crore:
₹1 -> ₹1,000 -> ₹10,000 -> ₹1,00,000 (1 Lakh) -> ₹10,00,000 (10 Lakh) -> ₹1,00,00,000 (1 Crore)
Each stage has an actual economic mechanism, customer pain, deliverable, and transition seam.
"""

from typing import Any

LADDER_STAGES = [
    {
        "stage": "FIRST_RUPEE",
        "target_amount_inr": 1.0,
        "name": "The Technical Handshake",
        "economic_mechanism": "Payment Gateway Test Charge / Micro-handshake verification",
        "customer_pain": "Verifying merchant payment gateway routing, invoice settlement, and bank reconciliation.",
        "deliverable": "End-to-end receipt generated, INR settlement confirmed, zero bounce.",
        "transition_trigger": "Successful credit to ACC-IN-OPS-01 or Wise Business vault."
    },
    {
        "stage": "MICRO_DELIVERABLE",
        "target_amount_inr": 1000.0,
        "name": "Targeted Diagnostic Snapshot",
        "economic_mechanism": "Micro-audit / Single competitor breakdown dossier",
        "customer_pain": "Immediate need to assess a competitor's hiring push or target account signals.",
        "deliverable": "1-page executive intelligence brief with verified source citations.",
        "transition_trigger": "Client accepts snapshot deliverable and requests full campaign scope."
    },
    {
        "stage": "PRODUCTIZED_SERVICE",
        "target_amount_inr": 10000.0,
        "name": "B2B Lead Intelligence Pack",
        "economic_mechanism": "100 Verified ICP Leads + Custom AI Icebreakers + Buying Triggers ($150 - $250)",
        "customer_pain": "Sales team is wasting SDR hours on bounced emails and generic cold outreach.",
        "deliverable": "Clean CSV / CRM import package with 99%+ deliverability guarantee.",
        "transition_trigger": "Zero bounce rate verified, client schedules follow-up sprint."
    },
    {
        "stage": "HIGH_TICKET_RETAINER",
        "target_amount_inr": 100000.0,
        "name": "Monthly Pipeline Acceleration Retainer (1 Lakh)",
        "economic_mechanism": "Ongoing Account Intelligence & Buying Trigger Prospecting ($1,200 / month)",
        "customer_pain": "Need consistent, high-intent outbound meetings without hiring a $6,000/mo US SDR.",
        "deliverable": "500 verified decision-makers + weekly buying signal updates + cold email copy.",
        "transition_trigger": "Customer prepays monthly retainer via Wise Business / Stripe."
    },
    {
        "stage": "SCALED_B2B_ENGINE",
        "target_amount_inr": 1000000.0,
        "name": "Multi-Client Autonomous Engine (10 Lakh)",
        "economic_mechanism": "8-10 recurring enterprise/mid-market clients + Automated Scraper/API workflow",
        "customer_pain": "Companies scaling demand generation across North America, UK, and APAC.",
        "deliverable": "Fully productized account intelligence with automated data pipelines.",
        "transition_trigger": "Cumulative profit exceeds ₹5 Lakhs, allowing allocation to software micro-SaaS development."
    },
    {
        "stage": "COMPOUNDING_CAPITAL_MACHINE",
        "target_amount_inr": 10000000.0,
        "name": "Compounding Global Capital Machine (1 Crore)",
        "economic_mechanism": "SaaS Subscriptions + High-Margin Enterprise Services + Yield-Bearing Treasury Buffers",
        "customer_pain": "Mission-critical demand generation and cross-border trade intelligence.",
        "deliverable": "Proprietary software platform, digital assets, recurring enterprise contracts.",
        "transition_trigger": "Diversified cash reserves, zero structural debt, compounding treasury yields."
    }
]


class FirstRupeeLadder:
    @staticmethod
    def get_ladder_stages() -> list[dict[str, Any]]:
        return LADDER_STAGES

    @staticmethod
    def get_current_stage(cumulative_revenue_inr: float) -> dict[str, Any]:
        """Determines the current milestone achieved and the active target rung."""
        current_milestone = LADDER_STAGES[0]
        next_milestone = LADDER_STAGES[1]

        for i, stage in enumerate(LADDER_STAGES):
            if cumulative_revenue_inr >= stage["target_amount_inr"]:
                current_milestone = stage
                if i + 1 < len(LADDER_STAGES):
                    next_milestone = LADDER_STAGES[i + 1]
                else:
                    next_milestone = stage

        progress_pct = min(100.0, (cumulative_revenue_inr / next_milestone["target_amount_inr"]) * 100.0) if next_milestone["target_amount_inr"] > 0 else 100.0

        return {
            "cumulative_revenue_inr": cumulative_revenue_inr,
            "current_milestone_achieved": current_milestone["name"],
            "next_target_rung": next_milestone["name"],
            "next_target_amount_inr": next_milestone["target_amount_inr"],
            "progress_to_next_rung_pct": round(progress_pct, 2),
            "active_deliverable": next_milestone["deliverable"],
            "active_transition_trigger": next_milestone["transition_trigger"]
        }


rupee_ladder = FirstRupeeLadder()
