"""
Tests for Hummingbot Autonomous Algorithmic Trading & Liquidity Orchestrator
=============================================================================
Tests high-frequency L2 order books, micro-price calculations, pure market making,
Avellaneda-Stoikov quantitative model, XEMM hedging, AMM arbitrage scanner,
V2 smart executors (Position, Grid, TWAP), risk controller (99% VaR, circuit breakers),
emergency kill-switch, backtesting engine, and 12-phase sovereign lifecycle.
"""

import os
import pytest
from pathlib import Path

from hummingbot_orchestrator import (
    HummingbotOrchestrator,
    OrderSide,
    OrderType,
    OrderStatus,
    StrategyType,
    ConnectorType,
)


@pytest.fixture
def orchestrator():
    return HummingbotOrchestrator()


def test_telemetry(orchestrator):
    telem = orchestrator.get_telemetry()
    assert telem["system"] == "Hummingbot Autonomous Algorithmic Trading & Liquidity Engine"
    assert telem["upstream_repository"] == "https://github.com/hummingbot/hummingbot"
    assert "2.14.0" in telem["version"]
    assert telem["total_connectors"] >= 100
    assert telem["cex_connectors"] >= 10
    assert telem["dex_connectors"] >= 50
    assert telem["total_portfolio_value_usd"] > 100000.0
    assert telem["risk_state"]["kill_switch_active"] is False


def test_connectors_directory(orchestrator):
    assert "binance" in orchestrator.connectors
    assert "coinbase_advanced" in orchestrator.connectors
    assert "uniswap_v3_arbitrum" in orchestrator.connectors
    assert "raydium_solana" in orchestrator.connectors

    binance = orchestrator.connectors["binance"]
    assert binance.connector_type == ConnectorType.CEX_SPOT
    assert binance.maker_fee_bps == 10.0
    assert binance.taker_fee_bps == 10.0
    assert binance.status == "ONLINE"


def test_order_book_depth_and_micro_price(orchestrator):
    book = orchestrator.order_books["BTC-USDT"]
    assert book.best_bid < book.best_ask
    assert book.mid_price > 0.0
    assert book.spread_bps > 0.0
    assert book.total_bid_depth(5) > 0.0
    assert book.total_ask_depth(5) > 0.0

    # Micro-price should be close to mid-price but reflect queue balance
    micro = book.micro_price
    assert abs(micro - book.mid_price) / book.mid_price < 0.01


def test_order_fill_simulation(orchestrator):
    book = orchestrator.order_books["BTC-USDT"]
    # Simulate buying 0.1 BTC market order
    fill = book.simulate_execution(side=OrderSide.BUY, amount=0.1, order_type=OrderType.MARKET)
    assert fill["status"] == "FILLED"
    assert fill["filled_amount"] == 0.1
    assert fill["avg_price"] >= book.best_ask
    assert fill["slippage_bps"] >= 0.0

    # Limit order below market should not fill immediately
    limit_fill = book.simulate_execution(
        side=OrderSide.BUY,
        amount=0.1,
        order_type=OrderType.LIMIT,
        limit_price=book.best_bid * 0.95,
    )
    assert limit_fill["status"] == "OPEN"
    assert limit_fill["filled_amount"] == 0.0


def test_pure_market_making_with_inventory_skew(orchestrator):
    # With base inventory BTC = 0.75 and USDT = 50,000, current base pct > target (50%)
    res = orchestrator.calculate_pure_market_making_orders(
        trading_pair="BTC-USDT",
        bid_spread_pct=0.002,
        ask_spread_pct=0.002,
        order_amount_usd=5000.0,
        inventory_skew_enabled=True,
    )
    assert res["trading_pair"] == "BTC-USDT"
    assert res["bid_order"]["side"] == "BUY"
    assert res["ask_order"]["side"] == "SELL"
    assert res["bid_order"]["price"] < res["mid_price"]
    assert res["ask_order"]["price"] > res["mid_price"]
    assert res["bid_order"]["amount"] > 0.0
    assert res["ask_order"]["amount"] > 0.0
    assert res["spread_width_bps"] > 0.0


def test_avellaneda_stoikov_model(orchestrator):
    # Test quantitative reservation price and optimal asymptotic spread
    res = orchestrator.calculate_avellaneda_stoikov(
        trading_pair="BTC-USDT",
        gamma=0.1,
        sigma=0.035,
        time_horizon_t=1.0,
        kappa=1.5,
    )
    s = res["mid_price_s"]
    r = res["reservation_price_r"]
    q = res["inventory_q"]

    # Since q (BTC holdings = 0.75) > 0, reservation price should be strictly less than mid-price
    assert q > 0
    assert r < s
    assert res["inventory_penalty_usd"] > 0.0

    # Optimal quotes
    quotes = res["quotes"]
    assert quotes["optimal_bid"] < r
    assert quotes["optimal_ask"] > r
    assert quotes["bid_spread_bps"] > 0
    assert quotes["ask_spread_bps"] > 0


def test_cross_exchange_market_making_hurdle(orchestrator):
    res = orchestrator.calculate_cross_exchange_market_making(
        maker_exchange="uniswap_v3_arbitrum",
        taker_exchange="binance",
        trading_pair="BTC-USDT",
        min_profitability_bps=25.0,
        order_amount_usd=5000.0,
    )
    mid = res["mid_price"]
    maker_orders = res["maker_orders"]
    assert maker_orders["maker_bid"] < mid
    assert maker_orders["maker_ask"] > mid
    assert res["fees_and_hurdles"]["min_profitability_bps"] == 25.0
    assert res["expected_net_profit_per_cycle_usd"] == 5000.0 * 0.0025


def test_amm_arbitrage_scanner(orchestrator):
    res = orchestrator.scan_amm_arbitrage(
        dex_connector="uniswap_v3_arbitrum",
        cex_connector="binance",
        trading_pair="ETH-USDT",
        gas_cost_usd=1.20,
    )
    assert res["trading_pair"] == "ETH-USDT"
    assert res["arbitrage_evaluation"]["direction"] in ("BUY_CEX_SELL_AMM", "BUY_AMM_SELL_CEX", "NO_ARBITRAGE")
    assert "gross_spread_bps" in res["arbitrage_evaluation"]
    assert "net_profit_usd" in res["arbitrage_evaluation"]


def test_v2_position_executor_triple_barrier(orchestrator):
    pe = orchestrator.create_position_executor(
        trading_pair="BTC-USDT",
        connector="binance",
        side=OrderSide.BUY,
        amount=0.1,
        take_profit_pct=0.015,
        stop_loss_pct=0.008,
    )
    assert pe.status == "RUNNING"
    entry = pe.entry_price

    # Simulate price surge beyond take-profit threshold (+2.0%)
    update = pe.update(entry * 1.02)
    assert update["status"] == "COMPLETED"
    assert update["close_type"] == "TAKE_PROFIT"
    assert update["realized_pnl"] > 0.0


def test_v2_grid_executor_rebalance(orchestrator):
    ge = orchestrator.create_grid_executor(
        trading_pair="SOL-USDT",
        connector="binance",
        grid_levels=5,
        grid_spread_pct=0.006,
        order_amount=2.0,
    )
    assert ge.status == "ACTIVE"
    assert len(ge.levels) == 10  # 5 buy levels + 5 sell levels

    # Price drops below first buy level
    first_buy_price = ge.levels[0]["price"]
    events = ge.simulate_tick(first_buy_price * 0.999)
    assert len(events) >= 1
    assert ge.fills_count >= 1
    assert ge.total_grid_pnl > 0.0


def test_v2_twap_executor_slicing(orchestrator):
    te = orchestrator.create_twap_executor(
        trading_pair="ETH-USDT",
        connector="binance",
        side=OrderSide.BUY,
        total_amount=5.0,
        total_duration_sec=300.0,
        num_slices=5,
    )
    assert te.slice_amount == 1.0
    assert te.status == "RUNNING"

    # Step through all slices
    for _ in range(5):
        te.step()

    assert te.executed_amount == 5.0
    assert te.status == "COMPLETED"


def test_risk_controller_var_and_drawdown(orchestrator):
    rc = orchestrator.risk_controller
    var = rc.calculate_var_99(portfolio_value=100000.0, daily_volatility=0.035)
    # VaR_99 = 100,000 * 2.32635 * 0.035 = ~8,142.23
    assert var["confidence_level"] == 0.99
    assert 8000.0 < var["var_1d_usd"] < 8300.0

    # Drawdown check: drop from 100k to 93k (7% drawdown, limit is 5%)
    ok = rc.update_portfolio_value(93000.0)
    assert ok is False
    assert rc.circuit_breaker_tripped is True
    assert "Max drawdown exceeded" in rc.tripped_reason

    # Reset
    rc.reset_circuit_breaker()
    assert rc.circuit_breaker_tripped is False


def test_emergency_kill_switch(orchestrator):
    rc = orchestrator.risk_controller
    res = rc.trigger_emergency_kill_switch("Test Kill Switch")
    assert res["status"] == "HALTED"
    assert res["kill_switch_active"] is True
    assert rc.circuit_breaker_tripped is True

    rc.reset_circuit_breaker()
    assert rc.kill_switch_active is False


def test_backtest_engine(orchestrator):
    res = orchestrator.run_backtest(
        strategy=StrategyType.PURE_MARKET_MAKING,
        trading_pair="BTC-USDT",
        days=7,
        initial_capital_usd=50000.0,
        spread_bps=20.0,
    )
    assert res["duration_days"] == 7
    assert res["total_hourly_intervals"] == 7 * 24
    assert res["final_equity_usd"] > 0.0
    assert res["total_trades"] > 0
    assert res["annualized_sharpe_ratio"] > 0.0
    assert len(res["equity_curve_samples"]) > 10


def test_sovereign_12_phase_lifecycle(orchestrator):
    manifest = orchestrator.do_everything()
    assert manifest["total_phases_executed"] == 12
    assert "SOVEREIGN HUMMINGBOT SUITE OPERATIONAL" in manifest["overall_status"]
    assert len(manifest["phases"]) == 12
    for p in manifest["phases"]:
        assert p["status"] == "PASSED"

    # Verify manifest file exists on disk
    manifest_file = Path(__file__).resolve().parent.parent / "omega" / "data" / "hummingbot_do_everything_manifest.json"
    assert manifest_file.exists()
