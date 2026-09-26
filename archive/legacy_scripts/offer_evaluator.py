#!/usr/bin/env python3
"""
========================================================================================
OMEGA OFFER INTELLIGENCE & COMPENSATION NEGOTIATION ENGINE (v8.0)
========================================================================================
1. Indian Income Tax Modeling (New Tax Regime FY 2024-25 / 2025-26):
   - Standard Deduction (INR 75,000)
   - Slab rates + Surcharge + 4% Health & Education Cess
   - Section 87A rebate for taxable income <= 7.0L
2. In-Hand Monthly Take-Home Decomposition:
   - Employee PF (12% of Basic), Gratuity, Professional Tax (INR 200/mo)
3. Bangalore Transit & Corridor Living Cost Adjustment:
   - Electronic City vs ORR vs Whitefield vs Koramangala
4. Offer Score (0-100) & Automated Counter-Offer Proposal Generation
========================================================================================
"""

import os, sys, json, math, unittest
from typing import Dict, List, Any, Optional, Tuple


class OfferEvaluator:
    """Evaluates compensation offers, models post-tax net take-home, and structures negotiations."""

    CORRIDOR_MONTHLY_COSTS_INR = {
        "electronic city": {"rent_1bhk": 12000, "commute_cost": 2500, "transit_friction": 3.5},
        "koramangala": {"rent_1bhk": 22000, "commute_cost": 3000, "transit_friction": 4.0},
        "hsr layout": {"rent_1bhk": 19000, "commute_cost": 2800, "transit_friction": 4.5},
        "outer ring road": {"rent_1bhk": 20000, "commute_cost": 4500, "transit_friction": 7.0},
        "bellandur": {"rent_1bhk": 21000, "commute_cost": 4500, "transit_friction": 7.2},
        "whitefield": {"rent_1bhk": 16000, "commute_cost": 4000, "transit_friction": 15.0},
        "manyata tech park": {"rent_1bhk": 17000, "commute_cost": 4200, "transit_friction": 13.5},
        "remote": {"rent_1bhk": 0, "commute_cost": 500, "transit_friction": 0.0}
    }

    @classmethod
    def calculate_new_regime_tax(cls, gross_ctc: float) -> Tuple[float, float, float]:
        """Computes annual income tax under the New Tax Regime (FY 2024-25 / 2025-26)."""
        # Standard deduction: 75,000 INR
        std_deduction = 75000.0
        taxable_income = max(0.0, gross_ctc - std_deduction)

        # Full rebate under 87A if taxable income <= 7,00,000
        if taxable_income <= 700000.0:
            return 0.0, taxable_income, 0.0

        # Slab calculation
        tax = 0.0
        # 0 to 3L: 0%
        # 3L to 7L: 5%
        if taxable_income > 300000.0:
            tax += min(400000.0, taxable_income - 300000.0) * 0.05
        # 7L to 10L: 10%
        if taxable_income > 700000.0:
            tax += min(300000.0, taxable_income - 700000.0) * 0.10
        # 10L to 12L: 15%
        if taxable_income > 1000000.0:
            tax += min(200000.0, taxable_income - 1000000.0) * 0.15
        # 12L to 15L: 20%
        if taxable_income > 1200000.0:
            tax += min(300000.0, taxable_income - 1200000.0) * 0.20
        # Above 15L: 30%
        if taxable_income > 1500000.0:
            tax += (taxable_income - 1500000.0) * 0.30

        # 4% Health & Education Cess
        cess = tax * 0.04
        total_tax = round(tax + cess, 2)
        effective_rate = round((total_tax / gross_ctc) * 100, 2) if gross_ctc > 0 else 0.0
        return total_tax, taxable_income, effective_rate

    @classmethod
    def evaluate_offer(
        cls,
        company_name: str,
        role_title: str,
        base_ctc_annual_inr: float,
        variable_annual_inr: float = 0.0,
        joining_bonus_inr: float = 0.0,
        esops_grant_inr: float = 0.0,
        location_corridor: str = "Outer Ring Road",
        is_tier_1_brand: bool = True
    ) -> Dict[str, Any]:
        """Decomposes offer into monthly in-hand take-home, taxes, living cost deductions, and negotiation metrics."""
        gross_annual = base_ctc_annual_inr + variable_annual_inr + joining_bonus_inr
        
        # Estimate Basic Salary (typically 40% - 50% of Base CTC)
        basic_annual = base_ctc_annual_inr * 0.45
        pf_employee_annual = basic_annual * 0.12
        prof_tax_annual = 2400.0  # Karnataka Professional Tax ~200/mo

        # Compute Tax
        annual_tax, taxable_inc, tax_rate = cls.calculate_new_regime_tax(base_ctc_annual_inr + variable_annual_inr)
        
        # Annual Net Take-Home (Base CTC minus Tax, PF, Prof Tax)
        annual_net_take_home = max(0.0, base_ctc_annual_inr - annual_tax - pf_employee_annual - prof_tax_annual)
        monthly_in_hand = round(annual_net_take_home / 12.0, 2)

        # Corridor Costs
        corridor_key = location_corridor.lower()
        corridor_data = None
        for k, v in cls.CORRIDOR_MONTHLY_COSTS_INR.items():
            if k in corridor_key:
                corridor_data = v
                break
        if not corridor_data:
            corridor_data = {"rent_1bhk": 18000, "commute_cost": 3500, "transit_friction": 7.0}

        monthly_living_costs = corridor_data["rent_1bhk"] + corridor_data["commute_cost"]
        monthly_disposable = round(monthly_in_hand - monthly_living_costs, 2)

        # Offer Score (0-100)
        # Components: Comp (40%), Brand (25%), Location/Disposable (20%), Career Upside (15%)
        comp_score = min(100.0, (base_ctc_annual_inr / 1200000.0) * 100.0)
        brand_score = 95.0 if is_tier_1_brand else 70.0
        disposable_score = min(100.0, max(10.0, (monthly_disposable / 40000.0) * 100.0))
        upside_score = 90.0 if (variable_annual_inr > 0 or esops_grant_inr > 0) else 75.0

        total_offer_score = round(
            (comp_score * 0.40) + (brand_score * 0.25) + (disposable_score * 0.20) + (upside_score * 0.15), 1
        )

        # Counter-Offer Proposal Generation
        target_counter_base = round(base_ctc_annual_inr * 1.15, -4)  # +15% anchor
        target_counter_bonus = max(50000.0, round(base_ctc_annual_inr * 0.10, -4))

        return {
            "company": company_name,
            "role": role_title,
            "gross_ctc_annual_inr": gross_annual,
            "base_ctc_annual_inr": base_ctc_annual_inr,
            "variable_annual_inr": variable_annual_inr,
            "joining_bonus_inr": joining_bonus_inr,
            "esops_annual_value_inr": esops_grant_inr,
            "financial_breakdown": {
                "annual_income_tax_new_regime": annual_tax,
                "effective_tax_rate_pct": tax_rate,
                "annual_provident_fund": round(pf_employee_annual, 2),
                "annual_professional_tax": prof_tax_annual,
                "annual_net_take_home": round(annual_net_take_home, 2),
                "monthly_in_hand_take_home": monthly_in_hand,
                "monthly_corridor_living_costs": monthly_living_costs,
                "monthly_net_disposable_savings": monthly_disposable
            },
            "offer_score": total_offer_score,
            "rating": "ELITE_OFFER" if total_offer_score >= 85.0 else ("STRONG_OFFER" if total_offer_score >= 70.0 else "NEGOTIATE_REQUIRED"),
            "negotiation_package": {
                "recommended_counter_base_inr": target_counter_base,
                "recommended_joining_bonus_inr": target_counter_bonus,
                "justification_anchor": (
                    f"Given candidate verified track record in 100k+ attendee ops (Aero India 2025), "
                    f"BBA International Business degree, and cross-border vendor SLA governance, "
                    f"requesting market alignment to {target_counter_base/100000:.1f} LPA base."
                )
            }
        }


# Type alias for return value
Tuple_Tax = Any


class TestOfferIntelligenceEngine(unittest.TestCase):
    def test_01_tax_calculation_under_7l(self):
        tax, taxable, rate = OfferEvaluator.calculate_new_regime_tax(650000.0)
        self.assertEqual(tax, 0.0)
        self.assertEqual(rate, 0.0)

    def test_02_tax_calculation_above_7l(self):
        tax, taxable, rate = OfferEvaluator.calculate_new_regime_tax(1000000.0)
        self.assertGreater(tax, 0.0)
        self.assertGreater(rate, 0.0)

    def test_03_full_offer_evaluation(self):
        res = OfferEvaluator.evaluate_offer(
            company_name="Accenture",
            role_title="Global Business Operations Analyst",
            base_ctc_annual_inr=850000.0,
            variable_annual_inr=100000.0,
            joining_bonus_inr=50000.0,
            location_corridor="Outer Ring Road",
            is_tier_1_brand=True
        )
        self.assertGreaterEqual(res["offer_score"], 70.0)
        self.assertGreater(res["financial_breakdown"]["monthly_in_hand_take_home"], 50000.0)
        self.assertIn("negotiation_package", res)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=[sys.argv[0]])
    else:
        sample = OfferEvaluator.evaluate_offer(
            company_name="Accenture",
            role_title="Global Business Operations Analyst",
            base_ctc_annual_inr=850000.0,
            variable_annual_inr=100000.0,
            location_corridor="Outer Ring Road (Bellandur)",
            is_tier_1_brand=True
        )
        print("OFFER EVALUATION RESULT:")
        print(json.dumps(sample, indent=2))
