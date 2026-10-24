"""
Unit Tests for Stock Market Limit Order Book, Alpha Models, and Risk Optimization
"""
import pytest
from projects.omega_global_markets_nexus.core.stock_market_engine import (
    LimitOrderBook, Order, OrderSide, OrderType,
    EquityFactorProfile, AlgorithmicExecutionSlicer, PortfolioRiskOptimizer
)


def test_order_book_matching():
    lob = LimitOrderBook(symbol="NVDA-SIM")
    # Add Sell Limit order at 120.0 for 100 shares
    sell_order = Order(
        order_id="ORD-S1",
        symbol="NVDA-SIM",
        side=OrderSide.SELL,
        order_type=OrderType.LIMIT,
        price=120.0,
        quantity=100
    )
    lob.add_order(sell_order)

    depth = lob.get_order_book_depth()
    assert depth["best_ask"] == 120.0
    assert depth["ask_volume"] == 100

    # Add Buy Market order for 40 shares
    buy_order = Order(
        order_id="ORD-B1",
        symbol="NVDA-SIM",
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        price=0.0,
        quantity=40
    )
    fills = lob.add_order(buy_order)

    assert len(fills) == 1
    assert fills[0].price == 120.0
    assert fills[0].quantity == 40
    assert sell_order.remaining_quantity == 60


def test_equity_factor_alpha_scoring():
    profile = EquityFactorProfile(
        symbol="NVDA",
        company_name="Nvidia Corp",
        sector="Semiconductors",
        current_price=125.0,
        momentum_12m_pct=65.0,
        earnings_yield_pct=4.2,
        roic_pct=48.0,
        debt_to_equity=0.2,
        realized_volatility_pct=22.0
    )
    alpha = profile.compute_composite_alpha()
    assert alpha > 5.0


def test_execution_slicers():
    twap = AlgorithmicExecutionSlicer.generate_twap_schedule(total_quantity=1000, duration_minutes=30, interval_minutes=5)
    assert len(twap) == 6
    total_qty = sum(item["target_quantity"] for item in twap)
    assert total_qty == 1000

    vwap = AlgorithmicExecutionSlicer.generate_vwap_schedule(
        total_quantity=1000,
        historical_hourly_distribution=[0.20, 0.15, 0.10, 0.10, 0.15, 0.30]
    )
    assert len(vwap) == 6
    total_vwap_qty = sum(item["allocated_quantity"] for item in vwap)
    assert total_vwap_qty == 1000


def test_portfolio_risk_optimizer():
    weights = [0.4, 0.3, 0.3]
    returns = [0.15, 0.12, 0.10]
    vols = [0.20, 0.18, 0.15]
    corr = [
        [1.0, 0.4, 0.2],
        [0.4, 1.0, 0.3],
        [0.2, 0.3, 1.0]
    ]
    res = PortfolioRiskOptimizer.evaluate_portfolio(
        weights, returns, vols, corr, risk_free_rate=0.045, portfolio_value_usd=1_000_000.0
    )
    assert res["expected_annual_return_pct"] > 0
    assert res["annualized_volatility_pct"] > 0
    assert res["sharpe_ratio"] > 0
    assert res["daily_var_95_usd"] > 0
