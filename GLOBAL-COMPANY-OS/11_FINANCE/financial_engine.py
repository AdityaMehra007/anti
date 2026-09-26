import os
import json

class FinancialEngine:
    @staticmethod
    def calculate_scale_ladder():
        """Generates detailed unit economics and resource models from ₹1 to ₹1,000 Crore ARR."""
        milestones = [
            {"tier": "₹1", "arr_inr": 1, "mrr_inr": 1, "clients": 1, "team": "1 Founder", "gross_margin": 0.99},
            {"tier": "₹1,000", "arr_inr": 12000, "mrr_inr": 1000, "clients": 1, "team": "1 Founder", "gross_margin": 0.95},
            {"tier": "₹10,000", "arr_inr": 120000, "mrr_inr": 10000, "clients": 1, "team": "1 Founder", "gross_margin": 0.90},
            {"tier": "₹1 Lakh", "arr_inr": 1200000, "mrr_inr": 100000, "clients": 3, "team": "1 Founder + AI Swarm", "gross_margin": 0.88},
            {"tier": "₹10 Lakh", "arr_inr": 12000000, "mrr_inr": 1000000, "clients": 28, "team": "1 Founder + AI Swarm", "gross_margin": 0.88},
            {"tier": "₹1 Crore", "arr_inr": 120000000, "mrr_inr": 10000000, "clients": 250, "team": "1 Founder + 3 Engineers", "gross_margin": 0.86},
            {"tier": "₹10 Crore", "arr_inr": 1200000000, "mrr_inr": 100000000, "clients": 2000, "team": "15 Core Team + Global Mesh", "gross_margin": 0.85},
            {"tier": "₹100 Crore", "arr_inr": 12000000000, "mrr_inr": 1000000000, "clients": 15000, "team": "40 Core Team + Autonomous Fabric", "gross_margin": 0.84},
            {"tier": "₹1,000 Crore", "arr_inr": 120000000000, "mrr_inr": 10000000000, "clients": 80000, "team": "150 Institutional Core", "gross_margin": 0.82}
        ]
        return milestones

    @staticmethod
    def project_scenarios(months=12):
        """Projects 3 scenarios: Survival, Base, Breakout."""
        return {
            "Survival": {"end_mrr_inr": 150000, "active_clients": 5, "cash_flow_positive": True, "burn_rate_inr": 35000},
            "Base": {"end_mrr_inr": 700000, "active_clients": 20, "cash_flow_positive": True, "burn_rate_inr": 80000},
            "Breakout": {"end_mrr_inr": 2500000, "active_clients": 70, "cash_flow_positive": True, "burn_rate_inr": 200000}
        }
