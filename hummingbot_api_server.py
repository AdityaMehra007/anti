#!/usr/bin/env python3
r"""
Hummingbot Autonomous Local REST API Server
===========================================
HTTP REST bridge on port 8781 exposing Hummingbot telemetry, 100+ CEX/DEX connectors,
real-time L2 order book depth, algorithmic strategies (PMM, Avellaneda-Stoikov, XEMM),
AMM arbitrage scanner, V2 smart executors, risk circuit breakers, backtesting engine,
and serving the interactive Mission Control Cockpit.

Default Port: 8781
Usage:
    python hummingbot_api_server.py [--port 8781]
"""

from __future__ import annotations

import os
import sys
import json
import logging
import argparse
from typing import Any, Dict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

from hummingbot_orchestrator import (
    HummingbotOrchestrator,
    OrderSide,
    OrderType,
    StrategyType,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("hummingbot_api_server")

BASE_DIR = Path(__file__).resolve().parent
orchestrator = HummingbotOrchestrator()


class HummingbotApiHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler for Hummingbot REST endpoints and Mission Control Cockpit."""

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json") -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self) -> None:
        self._set_headers(204)

    def _read_json_body(self) -> Dict[str, Any]:
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                raw_body = self.rfile.read(content_length)
                return json.loads(raw_body.decode("utf-8"))
        except Exception as e:
            logger.warning(f"Failed to parse request JSON: {e}")
        return {}

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        # Serve Cockpit UI
        if path in ("/", "/cockpit"):
            cockpit_file = BASE_DIR / "hummingbot_control_cockpit.html"
            if cockpit_file.exists():
                self._set_headers(200, "text/html; charset=utf-8")
                with open(cockpit_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._set_headers(404, "text/plain")
                self.wfile.write(b"Hummingbot Mission Control Cockpit file not found.")
            return

        # Health
        if path in ("/health", "/api/health"):
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "status": "HEALTHY",
                "service": "Hummingbot Autonomous Trading & Liquidity API Bridge",
                "version": orchestrator.version,
                "mode": orchestrator.mode,
                "uptime_seconds": round(time_since_start := orchestrator.get_telemetry()["uptime_seconds"], 2),
            }).encode("utf-8"))
            return

        # Telemetry
        if path == "/api/telemetry":
            self._set_headers(200)
            self.wfile.write(json.dumps(orchestrator.get_telemetry()).encode("utf-8"))
            return

        # Connectors
        if path == "/api/connectors":
            conn_type = query.get("type", ["ALL"])[0]
            conns = list(orchestrator.connectors.values())
            if conn_type != "ALL":
                conns = [c for c in conns if c.connector_type.value == conn_type]
            res = {
                "total_matching": len(conns),
                "connectors": [c.to_dict() for c in conns],
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Order Book
        if path == "/api/orderbook":
            pair = query.get("pair", ["BTC-USDT"])[0]
            levels = int(query.get("levels", [15])[0])
            book = orchestrator.order_books.get(pair)
            if not book:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": f"Order book for {pair} not found"}).encode("utf-8"))
                return
            res = book.to_dict()
            res["bids"] = res["bids"][:levels]
            res["asks"] = res["asks"][:levels]
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Arbitrage Scanner
        if path == "/api/strategies/arbitrage":
            dex = query.get("dex", ["uniswap_v3_arbitrum"])[0]
            cex = query.get("cex", ["binance"])[0]
            pair = query.get("pair", ["ETH-USDT"])[0]
            gas = float(query.get("gas", [1.20])[0])
            res = orchestrator.scan_amm_arbitrage(dex_connector=dex, cex_connector=cex, trading_pair=pair, gas_cost_usd=gas)
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Executors
        if path == "/api/executors":
            if not orchestrator.executors:
                orchestrator.create_position_executor("BTC-USDT", "binance", OrderSide.BUY, 0.1)
                orchestrator.create_grid_executor("SOL-USDT", "binance", 5, 0.005, 1.0)
                orchestrator.create_twap_executor("ETH-USDT", "binance", OrderSide.BUY, 5.0, 300.0, 5)
            self._set_headers(200)
            self.wfile.write(json.dumps([e.to_dict() for e in orchestrator.executors.values()]).encode("utf-8"))
            return

        # Risk
        if path == "/api/risk":
            telem = orchestrator.get_telemetry()
            var_data = orchestrator.risk_controller.calculate_var_99(telem["total_portfolio_value_usd"])
            res = {
                "risk_controller": orchestrator.risk_controller.to_dict(),
                "var_99": var_data,
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Gateway chains
        if path == "/api/gateway":
            gateway_info = {
                "status": "ONLINE",
                "version": "hummingbot-gateway-v2.5.0",
                "chains": [
                    {"chain": "ethereum", "network": "mainnet", "dexs": ["uniswap_v3", "curve"], "gas_price_gwei": 14.5},
                    {"chain": "arbitrum", "network": "one", "dexs": ["uniswap_v3", "camelot"], "gas_price_gwei": 0.1},
                    {"chain": "optimism", "network": "mainnet", "dexs": ["uniswap_v3", "velodrome"], "gas_price_gwei": 0.08},
                    {"chain": "base", "network": "mainnet", "dexs": ["uniswap_v3", "aerodrome"], "gas_price_gwei": 0.05},
                    {"chain": "polygon", "network": "pos", "dexs": ["quickswap", "uniswap_v3"], "gas_price_gwei": 35.0},
                    {"chain": "solana", "network": "mainnet-beta", "dexs": ["raydium", "orca", "jupiter"], "gas_price_gwei": 0.000005},
                ],
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(gateway_info).encode("utf-8"))
            return

        # 404
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": f"Endpoint {path} not found"}).encode("utf-8"))

    def do_POST(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        body = self._read_json_body()

        # Pure Market Making
        if path in ("/api/strategies/pmm", "/api/strategies/pure_market_making"):
            pair = body.get("trading_pair", "BTC-USDT")
            bid_s = float(body.get("bid_spread_bps", 20.0)) / 10000.0
            ask_s = float(body.get("ask_spread_bps", 20.0)) / 10000.0
            amount_usd = float(body.get("order_amount_usd", 5000.0))
            skew = bool(body.get("inventory_skew_enabled", True))
            res = orchestrator.calculate_pure_market_making_orders(
                trading_pair=pair,
                bid_spread_pct=bid_s,
                ask_spread_pct=ask_s,
                order_amount_usd=amount_usd,
                inventory_skew_enabled=skew,
            )
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Avellaneda-Stoikov
        if path in ("/api/strategies/avellaneda", "/api/strategies/avellaneda_stoikov"):
            pair = body.get("trading_pair", "BTC-USDT")
            gamma = float(body.get("gamma", 0.1))
            sigma = float(body.get("sigma", 0.035))
            horizon = float(body.get("time_horizon", 1.0))
            kappa = float(body.get("kappa", 1.5))
            res = orchestrator.calculate_avellaneda_stoikov(
                trading_pair=pair,
                gamma=gamma,
                sigma=sigma,
                time_horizon_t=horizon,
                kappa=kappa,
            )
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # XEMM
        if path in ("/api/strategies/xemm", "/api/strategies/cross_exchange_market_making"):
            maker = body.get("maker_exchange", "uniswap_v3_arbitrum")
            taker = body.get("taker_exchange", "binance")
            pair = body.get("trading_pair", "BTC-USDT")
            hurdle = float(body.get("min_profitability_bps", 25.0))
            amount_usd = float(body.get("order_amount_usd", 5000.0))
            res = orchestrator.calculate_cross_exchange_market_making(
                maker_exchange=maker,
                taker_exchange=taker,
                trading_pair=pair,
                min_profitability_bps=hurdle,
                order_amount_usd=amount_usd,
            )
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Backtest
        if path == "/api/backtest":
            strat = StrategyType(body.get("strategy", "pure_market_making"))
            pair = body.get("trading_pair", "BTC-USDT")
            days = int(body.get("days", 14))
            capital = float(body.get("capital", 50000.0))
            spread = float(body.get("spread_bps", 20.0))
            res = orchestrator.run_backtest(
                strategy=strat,
                trading_pair=pair,
                days=days,
                initial_capital_usd=capital,
                spread_bps=spread,
            )
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Kill Switch
        if path == "/api/kill-switch":
            reason = body.get("reason", "API Call")
            res = orchestrator.risk_controller.trigger_emergency_kill_switch(reason)
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Reset Risk
        if path == "/api/reset-risk":
            res = orchestrator.risk_controller.reset_circuit_breaker()
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # Do Everything
        if path == "/api/do-everything":
            manifest = orchestrator.do_everything()
            self._set_headers(200)
            self.wfile.write(json.dumps(manifest).encode("utf-8"))
            return

        # 404
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": f"POST endpoint {path} not found"}).encode("utf-8"))


def run_server(port: int = 8781) -> int:
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, HummingbotApiHandler)
    logger.info(f"[*] Hummingbot REST API Server listening on http://127.0.0.1:{port} (Cockpit: /cockpit)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("[*] Hummingbot API Server shutting down gracefully.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hummingbot Autonomous Local REST API Server")
    parser.add_argument("--port", type=int, default=8781, help="Port to bind (default 8781)")
    args = parser.parse_args()
    sys.exit(run_server(args.port))
