"""
Unit Tests for the Master Omega Nexus Orchestrator
"""
import pytest
from projects.omega_global_markets_nexus.core.nexus_orchestrator import OmegaNexusOrchestrator, NexusCycleReport


def test_nexus_macro_cycle_execution():
    orchestrator = OmegaNexusOrchestrator(local_currency_fx=85.0)
    report = orchestrator.run_full_macro_cycle(
        archetype_index=0, # Hyperscale AI
        trade_units=100,
        unit_price_usd=30_000.0,
        treasury_cash_pool_usd=25_000_000.0,
        equity_portfolio_capital_usd=10_000_000.0
    )

    assert isinstance(report, NexusCycleReport)
    assert report.business_archetype == "Hyperscale AI & Computing Cloud"
    assert report.annual_fcf_generated_bn > 0
    assert report.enterprise_value_bn > 0
    assert report.exim_trade_volume_usd > 0
    assert report.money_market_blended_yield_pct > 3.0
    assert report.basel3_lcr_pct >= 100.0
    assert report.bond_10y_yield_pct > 0
    assert report.stock_portfolio_sharpe > 0
    assert report.nexus_macro_verdict in ["SUPREME_GLOBAL_DOMINANCE", "OPERATIONALLY_SOUND_WITH_MONITORED_RISKS"]
