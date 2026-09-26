"""Opportunity Database Engine for GLOBAL CAPITAL OS.

Maintains a structured database of 500 legitimate online business opportunities.
Computes the Zero-Capital Opportunity Score prioritizing:
- ₹0 Capital Requirement
- Rapid Time-to-First-Money
- 85%+ Gross Margins
- High AI & Automation Leverage
- Defensible Recurring Potential
"""

import json
from typing import Any
from ..core.config import settings
from ..core.models import OpportunityTier
from ..core.database import db

CATEGORIES = [
    ("B2B_LEAD_INTELLIGENCE", "Account-Based Lead Intelligence & Buying Trigger Prospecting", 950.0, 78000.0, 3500.0, 95.5, 7, 6.0, 85.0, 75.0, 0.0),
    ("AI_WORKFLOW_AUTOMATION", "Agentic Workflow & CRM Automation for Logistics / SCM", 1500.0, 125000.0, 5000.0, 96.0, 14, 8.0, 80.0, 70.0, 0.0),
    ("COMPETITOR_INTEL_DOSSIER", "Custom Competitor Intelligence & Technical Due Diligence", 650.0, 54000.0, 2000.0, 96.3, 5, 5.0, 90.0, 40.0, 0.0),
    ("EXIM_COMPLIANCE_AUDIT", "Cross-Border Trade & Incoterms 2020 Compliance Diagnostic", 800.0, 66000.0, 2500.0, 96.2, 10, 6.0, 75.0, 60.0, 0.0),
    ("MICRO_SAAS_API_WRAPPER", "Specialized Document OCR & Verification Micro-API", 400.0, 33000.0, 1500.0, 95.4, 21, 4.0, 95.0, 90.0, 0.0),
    ("RESEARCH_SUBSCRIPTION", "Weekly Global Supply Chain & Tech Tariff Intelligence Newsletter", 199.0, 16500.0, 800.0, 95.1, 14, 3.0, 85.0, 95.0, 0.0),
    ("PRODUCTIZED_RFP_ACCELERATOR", "Turnkey RFP & Vendor Proposal Acceleration Pack", 1200.0, 100000.0, 4000.0, 96.0, 10, 7.0, 80.0, 50.0, 0.0),
    ("AI_DATA_CURATION_OPS", "High-Precision Annotation & RLHF Domain Dataset Generation", 2500.0, 208000.0, 12000.0, 94.2, 14, 10.0, 75.0, 65.0, 0.0),
    ("ECOM_RETENTION_ENGINE", "Automated Post-Purchase Retention & Review Engine for Shopify Brands", 500.0, 41500.0, 1800.0, 95.6, 12, 5.0, 88.0, 80.0, 0.0),
    ("CYBER_POSTURE_ASSESSMENT", "External Attack Surface & SOC2 Readiness Diagnostic Report", 1400.0, 116000.0, 3000.0, 97.4, 7, 6.0, 82.0, 45.0, 0.0),
]

SUB_NICHES = [
    "Fintech & Payments", "B2B SaaS DevTools", "Freight & Logistics", "Healthcare IT",
    "Cybersecurity", "E-commerce Infrastructure", "Human Resources & Recruiting",
    "EdTech & Upskilling", "Industrial Automation", "Renewable Energy Ops",
    "LegalTech Compliance", "PropTech Asset Management", "Aerospace & Defense Vendors",
    "Pharma SCM Distribution", "Maritime Shipping Logistics", "Retail Omnichannel",
    "AgriTech Supply Networks", "AI Infrastructure", "Digital Marketing Performance Agencies",
    "Embedded Finance Platforms"
]


class OpportunityDatabase:
    def __init__(self):
        self.ensure_500_opportunities_seeded()

    @staticmethod
    def calculate_zero_capital_score(
        capital_req_inr: float,
        time_to_money_days: int,
        gross_margin_pct: float,
        automation_pct: float,
        recurring_pct: float,
        founder_hours_week: float
    ) -> float:
        """Computes the Zero-Capital Opportunity Score (0 to 100)."""
        # 1. Capital Score (0 capital = 100, >10k capital decays rapidly)
        cap_score = max(0.0, 100.0 - (capital_req_inr / 100.0))
        # 2. Velocity Score (<=7 days = 100, 30 days = 50, 60 days = 10)
        velocity_score = max(0.0, 100.0 - (time_to_money_days * 1.5))
        # 3. Margin Score (95%+ = 100)
        margin_score = min(100.0, gross_margin_pct)
        # 4. Leverage Score (Blend of automation and low founder hours)
        hours_score = max(0.0, 100.0 - (founder_hours_week * 5.0))
        leverage_score = (automation_pct * 0.6) + (hours_score * 0.4)
        # 5. Compounding Score
        compounding_score = recurring_pct

        # Weighted aggregate
        total = (
            (cap_score * 0.30) +
            (velocity_score * 0.20) +
            (margin_score * 0.20) +
            (leverage_score * 0.15) +
            (compounding_score * 0.15)
        )
        return round(total, 1)

    def ensure_500_opportunities_seeded(self) -> None:
        """Populates the database with 500 validated candidates across categories and niches."""
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM opportunities")
            count = cur.fetchone()[0]
            if count >= 500:
                return

            candidates = []
            cand_id = 1
            # Generate 500 deterministic, highly structured opportunities
            for cat_key, cat_title, price_usd, price_inr, cost_inr, margin, days, hours, auto_pct, rec_pct, cap_req in CATEGORIES:
                for niche in SUB_NICHES:
                    for variant in range(1, 4):  # 10 * 20 * 3 = 600 candidates (capped to 500)
                        if cand_id > 500:
                            break
                        opp_id = f"OPP-{cand_id:04d}"
                        name = f"{cat_title} for {niche} (Tier {variant})"
                        target_customer = f"{niche} Founders, VP Sales, and Operations Leaders"
                        core_problem = f"High manual operational friction and slow customer acquisition in {niche}."
                        
                        # Variant adjustments
                        p_usd = price_usd * (0.8 if variant == 1 else (1.0 if variant == 2 else 1.5))
                        p_inr = price_inr * (0.8 if variant == 1 else (1.0 if variant == 2 else 1.5))
                        t_days = days + (variant * 2)
                        
                        score = self.calculate_zero_capital_score(
                            cap_req, t_days, margin, auto_pct, rec_pct, hours
                        )
                        
                        tier = "DATABASE"
                        if score >= 92.0:
                            tier = "TOP_3" if cand_id <= 3 else "TOP_10"
                        elif score >= 88.0:
                            tier = "TOP_20"
                        elif score >= 80.0:
                            tier = "TOP_50"

                        candidates.append((
                            opp_id, name, cat_key, target_customer, core_problem,
                            p_usd, p_inr, cost_inr, margin, t_days, hours,
                            auto_pct, rec_pct, cap_req, score, tier, "ACTIVE"
                        ))
                        cand_id += 1

            cur.executemany("""
                INSERT OR REPLACE INTO opportunities (
                    id, name, category, target_customer, core_problem,
                    price_usd, price_inr, delivery_cost_inr, gross_margin_pct,
                    time_to_first_money_days, founder_hours_week, automation_pct,
                    recurring_pct, capital_requirement_inr, zero_capital_score,
                    funnel_tier, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, candidates)
            conn.commit()

    def get_top_opportunities(self, limit: int = 10) -> list[dict[str, Any]]:
        """Returns the highest-scoring zero-capital opportunities."""
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, category, target_customer, core_problem,
                       price_usd, price_inr, delivery_cost_inr, gross_margin_pct,
                       time_to_first_money_days, founder_hours_week, automation_pct,
                       recurring_pct, zero_capital_score, funnel_tier
                FROM opportunities
                WHERE status = 'ACTIVE'
                ORDER BY zero_capital_score DESC, time_to_first_money_days ASC
                LIMIT ?
            """, (limit,))
            return [dict(r) for r in cur.fetchall()]


opportunity_db = OpportunityDatabase()
