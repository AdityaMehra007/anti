#!/usr/bin/env python3
r"""
Hummingbot Autonomous Model Context Protocol (MCP) Server
=========================================================
Exposes Hummingbot Algorithmic Trading & Liquidity Orchestration capabilities
to AI agents, subagents, and LLMs via standard JSON-RPC 2.0 stdio protocol.

Supported Tools:
- hummingbot_get_telemetry
- hummingbot_list_connectors
- hummingbot_get_order_book
- hummingbot_calculate_pure_market_making
- hummingbot_calculate_avellaneda_stoikov
- hummingbot_calculate_cross_exchange_market_making
- hummingbot_scan_amm_arbitrage
- hummingbot_list_executors
- hummingbot_create_position_executor
- hummingbot_create_grid_executor
- hummingbot_create_twap_executor
- hummingbot_run_backtest
- hummingbot_audit_risk_limits
- hummingbot_trigger_kill_switch
- hummingbot_reset_risk_breaker
- hummingbot_gateway_get_chains
- hummingbot_simulate_order_fill
- hummingbot_do_everything
"""

from __future__ import annotations

import sys
import json
import logging
from typing import Any, Dict

from hummingbot_orchestrator import (
    HummingbotOrchestrator,
    OrderSide,
    OrderType,
    StrategyType,
)

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("hummingbot_mcp")

orchestrator = HummingbotOrchestrator()

TOOLS = [
    {
        "name": "hummingbot_get_telemetry",
        "description": "Get Hummingbot runtime architecture, active bots, portfolio USD valuation, and risk state.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_list_connectors",
        "description": "List 100+ CEX and DEX connectors across spot, perps, and EVM/Solana AMMs with fee tiers and status.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["ALL", "CEX_SPOT", "CEX_PERP", "DEX_AMM", "DEX_CLOB"],
                    "description": "Filter by connector type",
                },
                "limit": {"type": "integer", "description": "Maximum number of connectors to return (default 25)"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_get_order_book",
        "description": "Inspect real-time L2 order book depth, bids/asks ladder, mid-price, and micro-price with order queue weighting.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "trading_pair": {"type": "string", "description": "Trading pair, e.g. BTC-USDT, ETH-USDT, SOL-USDT"},
                "levels": {"type": "integer", "description": "Number of depth levels (default 10)"},
            },
            "required": ["trading_pair"],
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_calculate_pure_market_making",
        "description": "Calculate dual-sided limit orders with dynamic inventory skewing and spread adjustments for Pure Market Making (PMM).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "trading_pair": {"type": "string", "description": "Trading pair, e.g. BTC-USDT"},
                "bid_spread_bps": {"type": "number", "description": "Bid spread in basis points (default 20.0)"},
                "ask_spread_bps": {"type": "number", "description": "Ask spread in basis points (default 20.0)"},
                "order_amount_usd": {"type": "number", "description": "Order amount in USD (default 5000.0)"},
                "inventory_skew_enabled": {"type": "boolean", "description": "Enable dynamic inventory skewing (default true)"},
            },
            "required": ["trading_pair"],
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_calculate_avellaneda_stoikov",
        "description": "Run Avellaneda & Stoikov (2008) quantitative market making model to calculate reservation price and optimal asymptotic spreads.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "trading_pair": {"type": "string", "description": "Trading pair, e.g. BTC-USDT"},
                "gamma": {"type": "number", "description": "Risk aversion parameter (default 0.1)"},
                "sigma": {"type": "number", "description": "Daily volatility parameter (default 0.035)"},
                "time_horizon": {"type": "number", "description": "Normalized trading horizon T - t (default 1.0)"},
                "kappa": {"type": "number", "description": "Order book liquidity / arrival intensity (default 1.5)"},
            },
            "required": ["trading_pair"],
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_calculate_cross_exchange_market_making",
        "description": "Calculate maker order prices and taker hedge requirements with guaranteed minimum net profitability hurdles for XEMM.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "maker_exchange": {"type": "string", "description": "Maker exchange connector (e.g. uniswap_v3_arbitrum)"},
                "taker_exchange": {"type": "string", "description": "Taker hedge exchange connector (e.g. binance)"},
                "trading_pair": {"type": "string", "description": "Trading pair, e.g. BTC-USDT"},
                "min_profitability_bps": {"type": "number", "description": "Minimum net profit hurdle in bps (default 25.0)"},
                "order_amount_usd": {"type": "number", "description": "Order amount in USD (default 5000.0)"},
            },
            "required": ["maker_exchange", "taker_exchange", "trading_pair"],
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_scan_amm_arbitrage",
        "description": "Scan Constant-Product x*y=k & concentrated liquidity DEX AMM vs CEX order book arbitrage with gas thresholding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dex_connector": {"type": "string", "description": "DEX connector (e.g. uniswap_v3_arbitrum)"},
                "cex_connector": {"type": "string", "description": "CEX connector (e.g. binance)"},
                "trading_pair": {"type": "string", "description": "Trading pair (default ETH-USDT)"},
                "gas_cost_usd": {"type": "number", "description": "Estimated gas cost in USD (default 1.20)"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_list_executors",
        "description": "List all active Hummingbot V2 smart executors (PositionExecutor, GridExecutor, TWAPExecutor).",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_create_position_executor",
        "description": "Create a V2 PositionExecutor with a triple-barrier risk setup (Take Profit, Stop Loss, Time Limit, Trailing Stop).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "trading_pair": {"type": "string", "description": "Trading pair (e.g. BTC-USDT)"},
                "connector": {"type": "string", "description": "Exchange connector (e.g. binance)"},
                "side": {"type": "string", "enum": ["BUY", "SELL"], "description": "Position direction"},
                "amount": {"type": "number", "description": "Order quantity in base asset units"},
                "take_profit_pct": {"type": "number", "description": "Take profit percentage (e.g. 0.015 for 1.5%)"},
                "stop_loss_pct": {"type": "number", "description": "Stop loss percentage (e.g. 0.008 for 0.8%)"},
            },
            "required": ["trading_pair", "connector", "side", "amount"],
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_create_grid_executor",
        "description": "Create a V2 GridExecutor maintaining multiple grid rungs with automated rebalancing upon execution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "trading_pair": {"type": "string", "description": "Trading pair (e.g. SOL-USDT)"},
                "connector": {"type": "string", "description": "Exchange connector (e.g. binance)"},
                "grid_levels": {"type": "integer", "description": "Number of grid levels (default 5)"},
                "grid_spread_pct": {"type": "number", "description": "Spread per rung (e.g. 0.006 for 0.6%)"},
                "order_amount": {"type": "number", "description": "Amount per grid rung in base units"},
            },
            "required": ["trading_pair", "connector"],
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_create_twap_executor",
        "description": "Create a V2 TWAPExecutor that slices large orders into equal tranches executed at regular intervals.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "trading_pair": {"type": "string", "description": "Trading pair (e.g. ETH-USDT)"},
                "connector": {"type": "string", "description": "Exchange connector (e.g. binance)"},
                "side": {"type": "string", "enum": ["BUY", "SELL"], "description": "Order side"},
                "total_amount": {"type": "number", "description": "Total order amount"},
                "total_duration_sec": {"type": "number", "description": "Total execution horizon in seconds"},
                "num_slices": {"type": "integer", "description": "Number of order slices"},
            },
            "required": ["trading_pair", "connector", "side", "total_amount"],
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_run_backtest",
        "description": "Run historical HFT backtest: returns Sharpe ratio, Sortino ratio, max drawdown, win rate, and equity curve.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "strategy": {"type": "string", "enum": ["pure_market_making", "avellaneda_stoikov", "grid_trading"]},
                "trading_pair": {"type": "string", "description": "Trading pair (default BTC-USDT)"},
                "days": {"type": "integer", "description": "Duration in days (default 14)"},
                "capital": {"type": "number", "description": "Starting capital in USD (default 50000.0)"},
                "spread_bps": {"type": "number", "description": "Market making spread in bps (default 20.0)"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_audit_risk_limits",
        "description": "Audit portfolio 99% Parametric Value-at-Risk (VaR), drawdown levels, and circuit breaker status.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_trigger_kill_switch",
        "description": "Trigger Emergency 1-Click Panic Kill-Switch to halt all active strategies and cancel open orders immediately.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string", "description": "Reason for triggering kill-switch"}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_reset_risk_breaker",
        "description": "Reset circuit breaker back to OPERATIONAL status after emergency investigation.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_gateway_get_chains",
        "description": "Get Hummingbot Gateway Web3 multi-chain DEX status (Ethereum, Arbitrum, Optimism, Base, Polygon, Solana).",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_simulate_order_fill",
        "description": "Simulate market/limit order execution against live order book depth with slippage and fill accounting.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "trading_pair": {"type": "string", "description": "Trading pair (e.g. BTC-USDT)"},
                "side": {"type": "string", "enum": ["BUY", "SELL"], "description": "Order side"},
                "amount": {"type": "number", "description": "Order quantity in base units"},
                "order_type": {"type": "string", "enum": ["MARKET", "LIMIT"], "default": "MARKET"},
                "limit_price": {"type": "number", "description": "Optional limit price"},
            },
            "required": ["trading_pair", "side", "amount"],
            "additionalProperties": False,
        },
    },
    {
        "name": "hummingbot_do_everything",
        "description": "Execute the comprehensive 12-phase sovereign lifecycle and output atomic verification manifest.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Any:
    if name == "hummingbot_get_telemetry":
        return orchestrator.get_telemetry()

    elif name == "hummingbot_list_connectors":
        c_type = arguments.get("type", "ALL")
        limit = arguments.get("limit", 25)
        conns = list(orchestrator.connectors.values())
        if c_type != "ALL":
            conns = [c for c in conns if c.connector_type.value == c_type]
        return {
            "total_matching": len(conns),
            "connectors": [c.to_dict() for c in conns[:limit]],
        }

    elif name == "hummingbot_get_order_book":
        pair = arguments["trading_pair"]
        levels = arguments.get("levels", 10)
        book = orchestrator.order_books.get(pair)
        if not book:
            raise ValueError(f"Order book for {pair} not found")
        res = book.to_dict()
        res["bids"] = res["bids"][:levels]
        res["asks"] = res["asks"][:levels]
        return res

    elif name == "hummingbot_calculate_pure_market_making":
        pair = arguments["trading_pair"]
        bid_s = float(arguments.get("bid_spread_bps", 20.0)) / 10000.0
        ask_s = float(arguments.get("ask_spread_bps", 20.0)) / 10000.0
        amt = float(arguments.get("order_amount_usd", 5000.0))
        skew = bool(arguments.get("inventory_skew_enabled", True))
        return orchestrator.calculate_pure_market_making_orders(
            trading_pair=pair,
            bid_spread_pct=bid_s,
            ask_spread_pct=ask_s,
            order_amount_usd=amt,
            inventory_skew_enabled=skew,
        )

    elif name == "hummingbot_calculate_avellaneda_stoikov":
        return orchestrator.calculate_avellaneda_stoikov(
            trading_pair=arguments["trading_pair"],
            gamma=float(arguments.get("gamma", 0.1)),
            sigma=float(arguments.get("sigma", 0.035)),
            time_horizon_t=float(arguments.get("time_horizon", 1.0)),
            kappa=float(arguments.get("kappa", 1.5)),
        )

    elif name == "hummingbot_calculate_cross_exchange_market_making":
        return orchestrator.calculate_cross_exchange_market_making(
            maker_exchange=arguments["maker_exchange"],
            taker_exchange=arguments["taker_exchange"],
            trading_pair=arguments["trading_pair"],
            min_profitability_bps=float(arguments.get("min_profitability_bps", 25.0)),
            order_amount_usd=float(arguments.get("order_amount_usd", 5000.0)),
        )

    elif name == "hummingbot_scan_amm_arbitrage":
        return orchestrator.scan_amm_arbitrage(
            dex_connector=arguments.get("dex_connector", "uniswap_v3_arbitrum"),
            cex_connector=arguments.get("cex_connector", "binance"),
            trading_pair=arguments.get("trading_pair", "ETH-USDT"),
            gas_cost_usd=float(arguments.get("gas_cost_usd", 1.20)),
        )

    elif name == "hummingbot_list_executors":
        if not orchestrator.executors:
            orchestrator.create_position_executor("BTC-USDT", "binance", OrderSide.BUY, 0.1)
            orchestrator.create_grid_executor("SOL-USDT", "binance", 5, 0.005, 1.0)
            orchestrator.create_twap_executor("ETH-USDT", "binance", OrderSide.BUY, 5.0, 300.0, 5)
        return [e.to_dict() for e in orchestrator.executors.values()]

    elif name == "hummingbot_create_position_executor":
        pe = orchestrator.create_position_executor(
            trading_pair=arguments["trading_pair"],
            connector=arguments["connector"],
            side=OrderSide(arguments["side"]),
            amount=float(arguments["amount"]),
            take_profit_pct=float(arguments.get("take_profit_pct", 0.015)),
            stop_loss_pct=float(arguments.get("stop_loss_pct", 0.008)),
        )
        return pe.to_dict()

    elif name == "hummingbot_create_grid_executor":
        ge = orchestrator.create_grid_executor(
            trading_pair=arguments["trading_pair"],
            connector=arguments["connector"],
            grid_levels=int(arguments.get("grid_levels", 5)),
            grid_spread_pct=float(arguments.get("grid_spread_pct", 0.006)),
            order_amount=float(arguments.get("order_amount", 2.0)),
        )
        return ge.to_dict()

    elif name == "hummingbot_create_twap_executor":
        te = orchestrator.create_twap_executor(
            trading_pair=arguments["trading_pair"],
            connector=arguments["connector"],
            side=OrderSide(arguments["side"]),
            total_amount=float(arguments["total_amount"]),
            total_duration_sec=float(arguments.get("total_duration_sec", 300.0)),
            num_slices=int(arguments.get("num_slices", 5)),
        )
        return te.to_dict()

    elif name == "hummingbot_run_backtest":
        strat = StrategyType(arguments.get("strategy", "pure_market_making"))
        return orchestrator.run_backtest(
            strategy=strat,
            trading_pair=arguments.get("trading_pair", "BTC-USDT"),
            days=int(arguments.get("days", 14)),
            initial_capital_usd=float(arguments.get("capital", 50000.0)),
            spread_bps=float(arguments.get("spread_bps", 20.0)),
        )

    elif name == "hummingbot_audit_risk_limits":
        telem = orchestrator.get_telemetry()
        var_data = orchestrator.risk_controller.calculate_var_99(telem["total_portfolio_value_usd"])
        return {
            "risk_controller": orchestrator.risk_controller.to_dict(),
            "var_99": var_data,
        }

    elif name == "hummingbot_trigger_kill_switch":
        reason = arguments.get("reason", "MCP Request")
        return orchestrator.risk_controller.trigger_emergency_kill_switch(reason)

    elif name == "hummingbot_reset_risk_breaker":
        return orchestrator.risk_controller.reset_circuit_breaker()

    elif name == "hummingbot_gateway_get_chains":
        return {
            "status": "ONLINE",
            "version": "hummingbot-gateway-v2.5.0",
            "chains": ["ethereum", "arbitrum", "optimism", "base", "polygon", "solana"],
            "supported_dex_protocols": ["uniswap_v3", "curve", "raydium", "pancakeswap", "balancer"],
        }

    elif name == "hummingbot_simulate_order_fill":
        pair = arguments["trading_pair"]
        side = OrderSide(arguments["side"])
        amount = float(arguments["amount"])
        order_type = OrderType(arguments.get("order_type", "MARKET"))
        limit_price = float(arguments["limit_price"]) if "limit_price" in arguments else None
        book = orchestrator.order_books.get(pair)
        if not book:
            raise ValueError(f"Order book for {pair} not found")
        return book.simulate_execution(side=side, amount=amount, order_type=order_type, limit_price=limit_price)

    elif name == "hummingbot_do_everything":
        return orchestrator.do_everything()

    else:
        raise ValueError(f"Unknown tool: {name}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            logger.error(f"Failed to parse JSON-RPC request: {e}")
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": TOOLS},
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                result = handle_tool_call(tool_name, arguments)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]
                    },
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)},
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "hummingbot_mcp_server", "version": "2.14.0"},
                },
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
