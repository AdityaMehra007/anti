"""Daily profit engine forwarder."""
import importlib

_mod = importlib.import_module("REVENUE_OS.13_FINANCE.daily_profit_engine")
DailyProfitEngine = _mod.DailyProfitEngine

__all__ = ["DailyProfitEngine"]
