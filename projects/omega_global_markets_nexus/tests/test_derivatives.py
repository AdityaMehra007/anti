"""
Unit Tests for Multi-Asset Derivatives & Hedging Desk
"""
import pytest
from projects.omega_global_markets_nexus.core.derivatives_engine import (
    BlackScholesEngine, OptionType, InterestRateSwapContract, FreightForwardAgreementPricer
)


def test_black_scholes_call_and_put():
    # Spot 100, Strike 100, T=1.0, r=0.05, sigma=0.20
    call_greeks = BlackScholesEngine.price_option(
        spot=100.0,
        strike=100.0,
        maturity_years=1.0,
        risk_free_rate=0.05,
        volatility=0.20,
        option_type=OptionType.CALL
    )
    assert 10.0 < call_greeks.price < 11.0  # Theoretical ~10.45
    assert 0.55 < call_greeks.delta < 0.70
    assert call_greeks.gamma > 0
    assert call_greeks.vega > 0
    assert call_greeks.theta < 0  # Time decay is negative

    put_greeks = BlackScholesEngine.price_option(
        spot=100.0,
        strike=100.0,
        maturity_years=1.0,
        risk_free_rate=0.05,
        volatility=0.20,
        option_type=OptionType.PUT
    )
    assert 5.0 < put_greeks.price < 6.5   # Theoretical ~5.57
    assert -0.50 < put_greeks.delta < -0.30

    # Put-Call Parity: C - P = S - K * exp(-rT)
    # 100 - 100 * exp(-0.05) = 100 - 95.1229 = 4.877
    assert abs((call_greeks.price - put_greeks.price) - 4.877) < 0.05


def test_implied_volatility_solver():
    target_price = 10.45
    solved_iv = BlackScholesEngine.solve_implied_volatility(
        target_price=target_price,
        spot=100.0,
        strike=100.0,
        maturity_years=1.0,
        risk_free_rate=0.05,
        option_type=OptionType.CALL
    )
    assert abs(solved_iv - 0.20) < 0.01


def test_interest_rate_swap():
    swap = InterestRateSwapContract(
        notional_usd=10_000_000.0,
        tenor_years=5,
        fixed_rate_pct=4.50,
        floating_sofr_benchmark_pct=5.30
    )
    curve_map = {1: 0.045, 2: 0.045, 3: 0.045, 4: 0.045, 5: 0.045}
    val = swap.calculate_swap_valuation(curve_map)
    assert val["notional_usd"] == 10_000_000.0
    assert val["par_swap_rate_pct"] > 0
    assert val["swap_dv01_usd"] > 0


def test_ffa_freight_hedge():
    res = FreightForwardAgreementPricer.price_ffa_hedge(
        spot_freight_usd_teu=2400.0,
        forward_contract_rate_usd_teu=2500.0,
        contracted_teu_volume=100,
        settlement_spot_freight_usd_teu=3200.0
    )
    # Physical cost = 100 * 3200 = 320,000
    # FFA gain = 100 * (3200 - 2500) = 70,000
    # Net cost = 250,000 (locked at 2500)
    assert res["unhedged_physical_cost_usd"] == 320_000.0
    assert res["ffa_hedging_pnl_usd"] == 70_000.0
    assert res["net_effective_freight_cost_usd"] == 250_000.0
    assert res["cost_variance_saved_usd"] == 70_000.0
