"""
Unit Tests for Macroeconomic Stress-Testing & Monte Carlo Engine
"""
import pytest
from projects.omega_global_markets_nexus.core.monte_carlo_stress_engine import (
    MonteCarloStressEngine, StressScenario, EnterpriseBalanceSheet
)


def test_enterprise_balance_sheet():
    sheet = EnterpriseBalanceSheet(
        equities_portfolio_usd=20_000_000.0,
        bond_portfolio_usd=15_000_000.0,
        money_market_cash_usd=10_000_000.0,
        exim_trade_receivables_usd=5_000_000.0
    )
    assert sheet.total_balance_sheet_usd == 50_000_000.0


def test_deterministic_stress_scenarios():
    sheet = EnterpriseBalanceSheet()
    res_gfc = MonteCarloStressEngine.run_deterministic_shock(sheet, StressScenario.GFC_2008_LIQUIDITY_CRUNCH)
    assert res_gfc.dollar_loss_usd > 0
    assert res_gfc.percentage_drawdown_pct > 15.0
    assert res_gfc.stress_var_99_usd > res_gfc.dollar_loss_usd

    res_stagflation = MonteCarloStressEngine.run_deterministic_shock(sheet, StressScenario.GREAT_STAGFLATION_1970S)
    assert res_stagflation.bonds_loss_usd > 0


def test_stochastic_monte_carlo_engine():
    sheet = EnterpriseBalanceSheet()
    res = MonteCarloStressEngine.run_stochastic_monte_carlo(
        sheet=sheet,
        num_simulations=500,
        horizon_days=30,
        seed=42
    )
    assert res["num_simulations"] == 500
    assert res["percentile_1st_worst_usd"] < res["median_terminal_value_usd"]
    assert res["mc_var_99_usd"] > 0
    assert res["mc_cvar_99_usd"] >= res["mc_var_99_usd"]
