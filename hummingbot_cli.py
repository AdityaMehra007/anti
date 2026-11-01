#!/usr/bin/env python3
r"""
Hummingbot Universal CLI
========================
Autonomous command-line interface for Hummingbot algorithmic trading,
L2 order book inspection, market making strategies (PMM, Avellaneda-Stoikov, XEMM),
CEX-DEX arbitrage, V2 smart executors, risk circuit breakers, and 12-phase attestation.

Usage Examples:
    python hummingbot_cli.py info
    python hummingbot_cli.py connectors --type CEX_SPOT
    python hummingbot_cli.py orderbook --pair BTC-USDT --levels 10
    python hummingbot_cli.py pmm --pair BTC-USDT --spread 25 --skew
    python hummingbot_cli.py avellaneda --pair BTC-USDT --gamma 0.1 --sigma 0.035
    python hummingbot_cli.py xemm --maker uniswap_v3_arbitrum --taker binance --hurdle 25
    python hummingbot_cli.py arbitrage --dex uniswap_v3_arbitrum --cex binance --pair ETH-USDT
    python hummingbot_cli.py executors
    python hummingbot_cli.py backtest --strategy pure_market_making --days 14
    python hummingbot_cli.py risk
    python hummingbot_cli.py kill-switch
    python hummingbot_cli.py do-everything
    python hummingbot_cli.py serve --port 8780
"""

from __future__ import annotations

import os
import sys
import json
import argparse
from typing import Any, Dict

from hummingbot_orchestrator import (
    HummingbotOrchestrator,
    OrderSide,
    OrderType,
    StrategyType,
    ConnectorType,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def format_json(data: Any) -> None:
    print(json.dumps(data, indent=2, default=str))


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="hummingbot_cli",
        description="Hummingbot Sovereign Algorithmic Trading & Liquidity CLI (https://github.com/hummingbot/hummingbot)",
    )
    parser.add_argument("--version", action="version", version="hummingbot_cli 2.14.0-sovereign")
    parser.add_argument("--json", action="store_true", help="Force JSON output for all commands")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # info
    subparsers.add_parser("info", help="Display Hummingbot runtime architecture, active bots, and portfolio summary")

    # connectors
    p_conn = subparsers.add_parser("connectors", help="List 100+ CEX and DEX connectors with status and fee tiers")
    p_conn.add_argument("--type", type=str, choices=["CEX_SPOT", "CEX_PERP", "DEX_AMM", "DEX_CLOB", "ALL"], default="ALL")
    p_conn.add_argument("--limit", type=int, default=25, help="Max connectors to display")

    # orderbook
    p_ob = subparsers.add_parser("orderbook", help="Inspect real-time L2 order book depth, mid-price, and micro-price")
    p_ob.add_argument("--pair", type=str, default="BTC-USDT", help="Trading pair (e.g. BTC-USDT, ETH-USDT, SOL-USDT)")
    p_ob.add_argument("--levels", type=int, default=10, help="Number of depth levels to display")

    # pmm
    p_pmm = subparsers.add_parser("pmm", help="Run Pure Market Making order calculation with inventory skewing")
    p_pmm.add_argument("--pair", type=str, default="BTC-USDT", help="Trading pair")
    p_pmm.add_argument("--bid-spread", type=float, default=20.0, help="Bid spread in basis points (bps)")
    p_pmm.add_argument("--ask-spread", type=float, default=20.0, help="Ask spread in basis points (bps)")
    p_pmm.add_argument("--amount-usd", type=float, default=5000.0, help="Order amount in USD")
    p_pmm.add_argument("--skew", action="store_true", default=True, help="Enable dynamic inventory skewing")

    # avellaneda
    p_av = subparsers.add_parser("avellaneda", help="Run Avellaneda-Stoikov quantitative reservation price & optimal spread model")
    p_av.add_argument("--pair", type=str, default="BTC-USDT", help="Trading pair")
    p_av.add_argument("--gamma", type=float, default=0.1, help="Risk aversion parameter gamma")
    p_av.add_argument("--sigma", type=float, default=0.035, help="Daily volatility sigma")
    p_av.add_argument("--kappa", type=float, default=1.5, help="Order book arrival intensity kappa")
    p_av.add_argument("--horizon", type=float, default=1.0, help="Normalized time horizon (T - t)")

    # xemm
    p_xemm = subparsers.add_parser("xemm", help="Run Cross-Exchange Market Making (XEMM) maker-taker hedge calculations")
    p_xemm.add_argument("--maker", type=str, default="uniswap_v3_arbitrum", help="Maker exchange connector")
    p_xemm.add_argument("--taker", type=str, default="binance", help="Taker hedge exchange connector")
    p_xemm.add_argument("--pair", type=str, default="BTC-USDT", help="Trading pair")
    p_xemm.add_argument("--hurdle", type=float, default=25.0, help="Min net profitability hurdle in bps")
    p_xemm.add_argument("--amount-usd", type=float, default=5000.0, help="Order amount in USD")

    # arbitrage
    p_arb = subparsers.add_parser("arbitrage", help="Scan AMM Constant-Product (x*y=k) vs CEX order book arbitrage")
    p_arb.add_argument("--dex", type=str, default="uniswap_v3_arbitrum", help="DEX connector")
    p_arb.add_argument("--cex", type=str, default="binance", help="CEX connector")
    p_arb.add_argument("--pair", type=str, default="ETH-USDT", help="Trading pair")
    p_arb.add_argument("--gas-usd", type=float, default=1.20, help="Estimated gas fee in USD")

    # executors
    subparsers.add_parser("executors", help="List active Hummingbot V2 Position, Grid, and TWAP executors")

    # backtest
    p_bt = subparsers.add_parser("backtest", help="Simulate historical HFT strategy backtest (Sharpe, Sortino, PnL, Drawdown)")
    p_bt.add_argument("--strategy", type=str, choices=["pure_market_making", "avellaneda_stoikov", "grid_trading"], default="pure_market_making")
    p_bt.add_argument("--pair", type=str, default="BTC-USDT", help="Trading pair")
    p_bt.add_argument("--days", type=int, default=14, help="Backtest duration in days")
    p_bt.add_argument("--capital", type=float, default=50000.0, help="Initial capital in USD")
    p_bt.add_argument("--spread", type=float, default=20.0, help="Market making spread in bps")

    # risk
    subparsers.add_parser("risk", help="Audit portfolio risk, 99% Parametric VaR, drawdown, and circuit breaker status")

    # kill-switch
    subparsers.add_parser("kill-switch", help="Trigger Emergency 1-Click Panic Kill-Switch to halt bots and cancel open orders")

    # reset-risk
    subparsers.add_parser("reset-risk", help="Reset circuit breaker state back to OPERATIONAL")

    # do-everything
    subparsers.add_parser("do-everything", help="Execute 12-phase sovereign lifecycle and write verification manifest")

    # serve
    p_serve = subparsers.add_parser("serve", help="Start Hummingbot Local REST API bridge & Cockpit Server")
    p_serve.add_argument("--port", type=int, default=8781, help="Port to bind (default 8781)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    orchestrator = HummingbotOrchestrator()

    if args.command == "info":
        telemetry = orchestrator.get_telemetry()
        if args.json:
            format_json(telemetry)
        else:
            print("=" * 75)
            print("  HUMMINGBOT AUTONOMOUS ALGORITHMIC TRADING ENGINE")
            print(f"  Upstream:  {telemetry['upstream_repository']}")
            print(f"  Version:   {telemetry['version']} | Mode: {telemetry['mode']}")
            print(f"  Portfolio: ${telemetry['total_portfolio_value_usd']:,.2f} USD")
            print(f"  Connectors: {telemetry['total_connectors']} ({telemetry['cex_connectors']} CEX, {telemetry['dex_connectors']} DEX)")
            print(f"  OrderBooks: {telemetry['active_order_books']} active markets")
            print(f"  Risk Stat: {'HALTED / KILL-SWITCH' if telemetry['risk_state']['kill_switch_active'] else 'NORMAL / OPERATIONAL'}")
            print("=" * 75)

    elif args.command == "connectors":
        conns = list(orchestrator.connectors.values())
        if args.type != "ALL":
            conns = [c for c in conns if c.connector_type.value == args.type]
        display_conns = [c.to_dict() for c in conns[:args.limit]]
        if args.json:
            format_json(display_conns)
        else:
            print(f"\n[*] Hummingbot Connectors Registry ({len(conns)} matching '{args.type}'):")
            print(f"    {'NAME':<28} | {'TYPE':<10} | {'MAKER':<6} | {'TAKER':<6} | {'PING':<7} | {'STATUS'}")
            print("    " + "-" * 75)
            for c in display_conns:
                print(f"    {c['name']:<28} | {c['type']:<10} | {c['maker_fee_bps']:>4.1f}bp | {c['taker_fee_bps']:>4.1f}bp | {c['ping_ms']:>5.1f}ms | {c['status']}")
            if len(conns) > args.limit:
                print(f"    ... and {len(conns) - args.limit} more connectors.")

    elif args.command == "orderbook":
        book = orchestrator.order_books.get(args.pair)
        if not book:
            print(f"[-] Error: Order book for pair '{args.pair}' not found.", file=sys.stderr)
            return 1
        ob_dict = book.to_dict()
        if args.json:
            format_json(ob_dict)
        else:
            print(f"\n=== Order Book: {book.trading_pair} ===")
            print(f"Mid Price:   ${book.mid_price:,.4f} | Micro Price: ${book.micro_price:,.4f}")
            print(f"Spread:      {book.spread_bps:.2f} bps (${book.best_ask - book.best_bid:,.4f})")
            print(f"Best Bid:    ${book.best_bid:,.4f} | Best Ask: ${book.best_ask:,.4f}")
            print("\n--- ASKS (Sell Orders) ---")
            for a in reversed(book.asks[:args.levels]):
                print(f"  ${a.price:>10.4f} | Vol: {a.amount:>8.4f} | Cum: {a.cumulative_amount:>8.4f}")
            print("   " + "-" * 35)
            print("--- BIDS (Buy Orders) ---")
            for b in book.bids[:args.levels]:
                print(f"  ${b.price:>10.4f} | Vol: {b.amount:>8.4f} | Cum: {b.cumulative_amount:>8.4f}")

    elif args.command == "pmm":
        orders = orchestrator.calculate_pure_market_making_orders(
            trading_pair=args.pair,
            bid_spread_pct=args.bid_spread / 10000.0,
            ask_spread_pct=args.ask_spread / 10000.0,
            order_amount_usd=args.amount_usd,
            inventory_skew_enabled=args.skew,
        )
        format_json(orders)

    elif args.command == "avellaneda":
        res = orchestrator.calculate_avellaneda_stoikov(
            trading_pair=args.pair,
            gamma=args.gamma,
            sigma=args.sigma,
            time_horizon_t=args.horizon,
            kappa=args.kappa,
        )
        format_json(res)

    elif args.command == "xemm":
        res = orchestrator.calculate_cross_exchange_market_making(
            maker_exchange=args.maker,
            taker_exchange=args.taker,
            trading_pair=args.pair,
            min_profitability_bps=args.hurdle,
            order_amount_usd=args.amount_usd,
        )
        format_json(res)

    elif args.command == "arbitrage":
        res = orchestrator.scan_amm_arbitrage(
            dex_connector=args.dex,
            cex_connector=args.cex,
            trading_pair=args.pair,
            gas_cost_usd=args.gas_usd,
        )
        format_json(res)

    elif args.command == "executors":
        # Create sample executors if empty
        if not orchestrator.executors:
            orchestrator.create_position_executor("BTC-USDT", "binance", OrderSide.BUY, 0.1)
            orchestrator.create_grid_executor("SOL-USDT", "binance", 5, 0.005, 1.0)
            orchestrator.create_twap_executor("ETH-USDT", "binance", OrderSide.BUY, 5.0, 300.0, 5)

        execs_data = [e.to_dict() for e in orchestrator.executors.values()]
        format_json(execs_data)

    elif args.command == "backtest":
        st = StrategyType(args.strategy)
        res = orchestrator.run_backtest(
            strategy=st,
            trading_pair=args.pair,
            days=args.days,
            initial_capital_usd=args.capital,
            spread_bps=args.spread,
        )
        format_json(res)

    elif args.command == "risk":
        telemetry = orchestrator.get_telemetry()
        var_data = orchestrator.risk_controller.calculate_var_99(telemetry["total_portfolio_value_usd"])
        risk_summary = {
            "risk_controller": orchestrator.risk_controller.to_dict(),
            "parametric_var_99": var_data,
        }
        format_json(risk_summary)

    elif args.command == "kill-switch":
        res = orchestrator.risk_controller.trigger_emergency_kill_switch("CLI Command")
        format_json(res)

    elif args.command == "reset-risk":
        res = orchestrator.risk_controller.reset_circuit_breaker()
        format_json(res)

    elif args.command == "do-everything":
        manifest = orchestrator.do_everything()
        if args.json:
            format_json(manifest)
        else:
            print("\n" + "=" * 75)
            print(f"  HUMMINGBOT SOVEREIGN 12-PHASE 'DO EVERYTHING' COMPLETED")
            print(f"  Execution ID:   {manifest['execution_id']}")
            print(f"  Overall Status: {manifest['overall_status']}")
            print(f"  Elapsed Time:   {manifest['total_elapsed_seconds']}s")
            print("=" * 75)
            for p in manifest["phases"]:
                print(f"  Phase {p['phase']:>2}: [{p['status']}] {p['name']:<45} ({p['elapsed_seconds']}s)")
            print("=" * 75)

    elif args.command == "serve":
        from hummingbot_api_server import run_server
        return run_server(port=args.port)

    return 0


if __name__ == "__main__":
    sys.exit(main())
