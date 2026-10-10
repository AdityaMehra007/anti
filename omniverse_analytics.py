"""
OMNIVERSE ANALYTICS & COMPENSATION ENGINE
Calculates realistic net monthly in-hand compensation for Bengaluru corporate roles
under the New Tax Regime, and scores career leverage across multi-dimensional metrics.

Directives: OMEGA CONSTITUTION & CONTEXT.md
"""

import json


def calculate_bengaluru_inhand_salary(ctc_lpa):
    """
    Calculates detailed salary breakdown for an Indian salaried professional
    based in Bengaluru, Karnataka under the New Tax Regime (FY 2025-26 / 2026-27).
    """
    ctc = float(ctc_lpa) * 100000.0

    # Standard component breakdown
    basic_salary = ctc * 0.40  # 40% Basic
    hra = ctc * 0.20           # 20% HRA
    special_allowance = ctc * 0.28
    employer_pf = min(basic_salary * 0.12, 21600.0) # 12% of basic or standard cap
    gratuity = basic_salary * 0.0481

    # Total Deductions from Employee
    employee_pf = employer_pf
    professional_tax = 2400.0  # Karnataka PT: ₹200/mo = ₹2,400/yr

    # Taxable Income calculation (New Tax Regime)
    standard_deduction = 75000.0
    taxable_income = max(0.0, ctc - employer_pf - gratuity - standard_deduction)

    # Tax Slabs (New Regime with Section 87A rebate up to ₹7,00,000)
    tax = 0.0
    if taxable_income > 700000.0:
        # Slabs:
        # 0 - 3L: 0%
        # 3L - 7L: 5% = 20,000
        # 7L - 10L: 10%
        # 10L - 12L: 15%
        # 12L - 15L: 20%
        # > 15L: 30%
        remaining = taxable_income
        if remaining > 300000.0:
            taxable_slab = min(remaining - 300000.0, 400000.0)
            tax += taxable_slab * 0.05
        if remaining > 700000.0:
            taxable_slab = min(remaining - 700000.0, 300000.0)
            tax += taxable_slab * 0.10
        if remaining > 1000000.0:
            taxable_slab = min(remaining - 1000000.0, 200000.0)
            tax += taxable_slab * 0.15
        if remaining > 1200000.0:
            taxable_slab = min(remaining - 1200000.0, 300000.0)
            tax += taxable_slab * 0.20
        if remaining > 1500000.0:
            tax += (remaining - 1500000.0) * 0.30

        # Health & Education Cess: 4%
        tax *= 1.04

    total_annual_deductions = employee_pf + professional_tax + tax + employer_pf + gratuity
    annual_inhand = max(0.0, ctc - total_annual_deductions)
    monthly_inhand = annual_inhand / 12.0

    return {
        "ctc_lpa": ctc_lpa,
        "gross_annual": round(ctc, 2),
        "basic_annual": round(basic_salary, 2),
        "monthly_inhand": round(monthly_inhand, 2),
        "annual_inhand": round(annual_inhand, 2),
        "monthly_employee_pf": round(employee_pf / 12.0, 2),
        "monthly_tax": round(tax / 12.0, 2),
        "monthly_pt": 200.0
    }


def evaluate_career_leverage(role_name, company_tier, ctc_lpa, transit_friction_index=40):
    """
    Computes Career Leverage Score (0-100) based on compensation, brand equity,
    analytical scope, and operational mobility.
    """
    # 1. Base Score
    score = 50.0

    # 2. Compensation weight
    if ctc_lpa >= 9.0:
        score += 20.0
    elif ctc_lpa >= 6.5:
        score += 15.0
    elif ctc_lpa >= 5.0:
        score += 10.0
    else:
        score += 5.0

    # 3. Brand Equity / Tier
    if "Titan" in company_tier or "Tier 1" in company_tier:
        score += 20.0
    elif "GCC" in company_tier or "MNC" in company_tier:
        score += 15.0
    elif "Unicorn" in company_tier:
        score += 12.0
    else:
        score += 8.0

    # 4. Transit Friction Penalty (0-100 friction)
    friction_penalty = (transit_friction_index / 100.0) * 8.0
    score -= friction_penalty

    score = min(99.0, max(20.0, score))
    return round(score, 1)


if __name__ == "__main__":
    sample_roles = [
        ("Deutsche Bank Early Talent", "Tier 1 Global Titan", 8.5, 35),
        ("KPMG Audit Associate", "Tier 2 GCC/MNC", 6.2, 45),
        ("Salesforce Futureforce", "Tier 1 Global Titan", 10.5, 30),
        ("Quess Corp HR Associate", "Tier 3 Enterprise Services", 4.2, 50)
    ]

    print("=== BENGALURU IN-HAND SALARY & CAREER LEVERAGE EVALUATOR ===")
    for title, tier, ctc, friction in sample_roles:
        sal = calculate_bengaluru_inhand_salary(ctc)
        leverage = evaluate_career_leverage(title, tier, ctc, friction)
        print(f"\nRole: {title} ({tier})")
        print(f"  CTC: {ctc} LPA | Est In-Hand: INR {sal['monthly_inhand']:,.2f} / month")
        print(f"  Career Leverage Score: {leverage}/100")
