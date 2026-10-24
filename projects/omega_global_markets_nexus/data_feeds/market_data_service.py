"""
Market Data Feeds & Synthetic Telemetry Service
Provides live streaming snapshots and high-fidelity benchmarks across Global Equities,
Money Market SOFR fixings, Sovereign Yield Ladders, FX currency pairs, and Freight indices.
"""
import random
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Any


@dataclass
class TickerQuote:
    symbol: str
    name: str
    price: float
    change_pct: float
    volume: int
    sector: str


@dataclass
class MoneyMarketRates:
    sofr_overnight_pct: float
    sofr_1m_pct: float
    fed_funds_effective_pct: float
    tbill_3m_discount_pct: float
    prime_cp_90d_pct: float
    repo_gc_overnight_pct: float


@dataclass
class CommodityFreightBenchmarks:
    brent_crude_usd: float
    shanghai_container_freight_usd_teu: float
    gold_usd_oz: float
    natural_gas_mmbtu: float


class MarketDataService:
    """Institutional market data feed provider with deterministic simulation and real-world anchors."""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self._base_equities = {
            "NVDA": {"name": "NVIDIA Corp", "base": 125.0, "sector": "Semiconductors"},
            "AAPL": {"name": "Apple Inc", "base": 228.0, "sector": "Consumer Hardware/Services"},
            "MSFT": {"name": "Microsoft Corp", "base": 420.0, "sector": "Cloud Infrastructure"},
            "TSM": {"name": "Taiwan Semiconductor", "base": 185.0, "sector": "Foundry/Lithography"},
            "BRK.B": {"name": "Berkshire Hathaway", "base": 460.0, "sector": "Merchant Banking & Float"},
            "AMZN": {"name": "Amazon.com Inc", "base": 188.0, "sector": "Commerce & Cloud"},
            "MAERSK": {"name": "A.P. Moller - Maersk", "base": 155.0, "sector": "Multi-Modal Freight"}
        }

    def get_equity_quotes(self, jitter: bool = True) -> List[Dict[str, Any]]:
        quotes = []
        for sym, meta in self._base_equities.items():
            delta = (random.uniform(-0.015, 0.02) if jitter else 0.005)
            price = round(meta["base"] * (1.0 + delta), 2)
            change_pct = round(delta * 100.0, 2)
            vol = random.randint(1_200_000, 18_000_000)
            quotes.append({
                "symbol": sym,
                "name": meta["name"],
                "price": price,
                "change_pct": change_pct,
                "volume": vol,
                "sector": meta["sector"]
            })
        return quotes

    def get_money_market_benchmarks(self) -> Dict[str, float]:
        return {
            "sofr_overnight_pct": 5.30,
            "sofr_1m_pct": 5.32,
            "fed_funds_effective_pct": 5.33,
            "tbill_3m_discount_pct": 5.15,
            "prime_cp_90d_pct": 5.45,
            "repo_gc_overnight_pct": 5.28
        }

    def get_sovereign_yield_ladder(self) -> Dict[str, float]:
        """Benchmark 10-tenor US Treasury sovereign yield curve."""
        return {
            "3M": 5.18,
            "6M": 5.05,
            "1Y": 4.85,
            "2Y": 4.33,
            "3Y": 4.25,
            "5Y": 4.22,
            "7Y": 4.30,
            "10Y": 4.45,
            "20Y": 4.70,
            "30Y": 4.62
        }

    def get_fx_matrix(self) -> Dict[str, float]:
        """Major foreign exchange currency pairs for international EXIM trade settlements."""
        return {
            "USD_INR": 85.05,
            "EUR_USD": 1.085,
            "USD_JPY": 152.40,
            "GBP_USD": 1.295,
            "USD_CNY": 7.12,
            "USD_AED": 3.6725,
            "USD_SGD": 1.315
        }

    def get_freight_and_commodity_benchmarks(self) -> Dict[str, float]:
        return {
            "brent_crude_usd_bbl": 76.50,
            "scfi_freight_usd_teu": 2450.0,
            "gold_usd_oz": 2720.0,
            "natural_gas_usd_mmbtu": 2.45
        }

    def get_unified_market_snapshot(self) -> Dict[str, Any]:
        return {
            "timestamp": time.time(),
            "equities": self.get_equity_quotes(),
            "money_market": self.get_money_market_benchmarks(),
            "yield_ladder": self.get_sovereign_yield_ladder(),
            "fx_rates": self.get_fx_matrix(),
            "commodities_freight": self.get_freight_and_commodity_benchmarks()
        }
