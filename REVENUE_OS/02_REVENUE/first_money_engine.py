"""
First-Money Engine for REVENUE OS
Adheres strictly to Directives 10, 96, 97, 98, 99, 100, 101.
Models the step-by-step financial unit economics from ₹1 to ₹1 Crore and $10k to $100k USD.
"""

from typing import Any, Dict
import math

class FirstMoneyEngine:
    """
    Calculates exact customer count, price, conversion rates, leads required,
    delivery costs, and gross margins across each financial milestone.
    """
    
    MILESTONE_DEFINITIONS = {
        "first_rupee": {
            "name": "First Rupee Proof of Concept",
            "target_amount": 1.0,
            "currency": "INR",
            "customers_needed": 1,
            "average_price": 1.0,
            "conversion_rate_pct": 50.0,
            "leads_required": 2,
            "costs_inr": 0.0,
            "gross_margin_pct": 100.0,
            "effort_description": "Micro-transaction proof via UPI or digital payment gateway link.",
            "delivery_mechanism": "Instant digital download or link confirmation."
        },
        "first_thousand": {
            "name": "First ₹1,000 Milestone",
            "target_amount": 1000.0,
            "currency": "INR",
            "customers_needed": 1,
            "average_price": 1000.0,
            "conversion_rate_pct": 20.0,
            "leads_required": 5,
            "costs_inr": 50.0,
            "gross_margin_pct": 95.0,
            "effort_description": "Sell single verified B2B hiring & technology intelligence dossier.",
            "delivery_mechanism": "Curated PDF/Markdown intelligence report."
        },
        "first_ten_thousand": {
            "name": "First ₹10,000 Milestone",
            "target_amount": 10000.0,
            "currency": "INR",
            "customers_needed": 2,
            "average_price": 5000.0,
            "conversion_rate_pct": 10.0,
            "leads_required": 20,
            "costs_inr": 600.0,
            "gross_margin_pct": 94.0,
            "effort_description": "2 boutique agency audits or curated lead packs.",
            "delivery_mechanism": "Semi-automated report generation."
        },
        "first_lakh": {
            "name": "First ₹1,00,000 Milestone (Directive 97)",
            "target_amount": 100000.0,
            "currency": "INR",
            "customers_needed": 3,
            "average_price": 35000.0,
            "conversion_rate_pct": 5.0,
            "leads_required": 60,
            "costs_inr": 10500.0,
            "gross_margin_pct": 89.5,
            "effort_description": "3 recurring B2B clients on the Primary AI Pipeline Engine.",
            "delivery_mechanism": "Turnkey weekly outbound intelligence and custom copy delivery."
        },
        "first_ten_lakh": {
            "name": "First ₹10,00,000 Milestone (Directive 98)",
            "target_amount": 1000000.0,
            "currency": "INR",
            "customers_needed": 10,
            "average_price": 100000.0, # 10 clients paying ₹35k/mo over ~3 months
            "conversion_rate_pct": 4.0,
            "leads_required": 250,
            "costs_inr": 105000.0,
            "gross_margin_pct": 89.5,
            "effort_description": "10 retained clients paying monthly retaining fees across 90 days.",
            "delivery_mechanism": "Automated pipeline delivery with founder approval gate."
        },
        "first_crore_arr": {
            "name": "₹1 Crore Annual Recurring Revenue (Directive 99)",
            "target_amount": 10000000.0,
            "currency": "INR",
            "customers_needed": 24, # 24 clients @ ₹35,000/mo = ₹8.4L/mo = ~₹1 Crore ARR
            "average_price": 420000.0, # Annual contract value per client
            "conversion_rate_pct": 3.5,
            "leads_required": 685,
            "costs_inr": 1200000.0,
            "gross_margin_pct": 88.0,
            "effort_description": "24 steady B2B accounts on productized subscription.",
            "delivery_mechanism": "Full autonomous multi-agent pipeline."
        },
        "first_global_10k_usd": {
            "name": "First $10,000 Global Revenue (Directive 100)",
            "target_amount": 10000.0,
            "currency": "USD",
            "customers_needed": 10,
            "average_price": 1000.0,
            "conversion_rate_pct": 4.0,
            "leads_required": 250,
            "costs_inr": 100000.0,
            "gross_margin_pct": 88.5,
            "effort_description": "10 international clients ($1,000 onboarding / retainer).",
            "delivery_mechanism": "Stripe/Paddle compliant cross-border invoicing."
        },
        "first_global_100k_usd_arr": {
            "name": "First $100,000 Global ARR (Directive 101)",
            "target_amount": 100000.0,
            "currency": "USD",
            "customers_needed": 17, # 17 clients @ $500/mo = $8,500/mo = ~$100,000 ARR
            "average_price": 5882.0, # Annual value
            "conversion_rate_pct": 3.0,
            "leads_required": 566,
            "costs_inr": 1100000.0,
            "gross_margin_pct": 87.5,
            "effort_description": "17 recurring global clients across US, UK, EU, UAE.",
            "delivery_mechanism": "Self-serve and automated delivery workflows."
        }
    }

    def get_stage_plan(self, stage_key: str) -> Dict[str, Any]:
        if stage_key not in self.MILESTONE_DEFINITIONS:
            raise KeyError(f"Unknown milestone stage: {stage_key}")
        return self.MILESTONE_DEFINITIONS[stage_key]

    def get_all_stages(self) -> Dict[str, Any]:
        return self.MILESTONE_DEFINITIONS
