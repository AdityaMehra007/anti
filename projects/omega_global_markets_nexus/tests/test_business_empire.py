"""
Unit Tests for Global Business Empire & Capital Allocation
"""
import pytest
from projects.omega_global_markets_nexus.core.business_empire import (
    BusinessCategory, StrategicMoat, FinancialProfile, EnterpriseArchetype, GlobalBusinessEmpireCatalog
)


def test_strategic_moat_composite_score():
    moat = StrategicMoat(
        network_effects=9.0,
        switching_costs=9.0,
        cost_advantage=8.0,
        intangible_ip_assets=10.0,
        geopolitical_barrier=9.0
    )
    score = moat.composite_score
    assert 80.0 <= score <= 100.0


def test_financial_profile_fcf():
    profile = FinancialProfile(
        revenue_usd_bn=100.0,
        gross_margin_pct=70.0,
        ebitda_margin_pct=50.0,
        net_margin_pct=40.0, # Net income = 40.0 bn
        roic_pct=30.0,
        fcf_conversion_pct=90.0, # FCF = 36.0 bn
        capex_intensity_pct=10.0,
        rd_intensity_pct=12.0,
        debt_to_equity=0.2
    )
    assert profile.free_cash_flow_usd_bn == 36.0


def test_dcf_valuation_and_capital_allocation():
    catalog = GlobalBusinessEmpireCatalog.get_tier_one_archetypes()
    assert len(catalog) >= 5
    ai_company = catalog[0]

    dcf = ai_company.calculate_dcf_valuation(wacc=0.09, terminal_growth=0.035, projected_5yr_cagr=0.15)
    assert dcf["enterprise_value_bn"] > 100.0
    assert dcf["implied_fcf_multiple"] > 10.0

    alloc = ai_company.allocate_capital_5yr()
    assert alloc["total_5yr_fcf_pool_bn"] > 0
    assert alloc["organic_reinvestment_bn"] > 0
    assert alloc["ma_warchest_bn"] > 0
