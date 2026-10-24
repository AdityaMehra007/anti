"""
Unit Tests for Bond Market Nelson-Siegel Yield Curves, Bond Valuation, and Credit Spreads
"""
import pytest
from projects.omega_global_markets_nexus.core.bond_market_engine import (
    NelsonSiegelCurve, FixedCouponBond, CorporateCreditSpreadAnalyzer
)


def test_nelson_siegel_curve():
    curve = NelsonSiegelCurve(beta_0=0.045, beta_1=-0.015, beta_2=0.010, tau=2.5)
    ladder = curve.generate_tenor_ladder()
    assert "2Y" in ladder
    assert "10Y" in ladder
    assert ladder["10Y"] > 0
    inversion = curve.check_curve_inversion()
    assert "is_inverted" in inversion
    assert "spread_10y_2y_bps" in inversion


def test_bond_pricing_and_duration():
    bond = FixedCouponBond(
        cusip="US-CORP-01",
        issuer="Apex Sovereign Corp",
        par_value=1000.0,
        coupon_rate_pct=5.0,
        maturity_years=10.0,
        frequency=2
    )
    # Price at par yield should be par
    price_par = bond.price_at_yield(5.0)
    assert abs(price_par - 1000.0) < 0.01

    # Price when yield rises to 6.0% should drop below par
    price_discount = bond.price_at_yield(6.0)
    assert price_discount < 1000.0

    # Test YTM solver
    solved_ytm = bond.solve_ytm(price_discount)
    assert abs(solved_ytm - 6.0) < 0.01

    # Test Duration & Convexity
    dur_metrics = bond.calculate_duration_convexity(5.0)
    assert 6.0 < dur_metrics["modified_duration_years"] < 9.0
    assert dur_metrics["convexity"] > 0
    assert dur_metrics["dv01_per_million_usd"] > 0


def test_corporate_credit_spread():
    spread_res = CorporateCreditSpreadAnalyzer.analyze_spread(
        corporate_ytm_pct=6.50,
        benchmark_sovereign_ytm_pct=4.50,
        expected_recovery_rate_pct=40.0
    )
    assert spread_res["credit_spread_bps"] == 200.0
    assert spread_res["annual_hazard_rate_pct"] > 0
    assert spread_res["cumulative_5yr_default_prob_pct"] > 0
