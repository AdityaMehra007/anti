"""Risk forwarder package."""
import importlib

_mod = importlib.import_module("REVENUE_OS.18_RISK.risk_engine")
RiskEngine = _mod.RiskEngine

__all__ = ["RiskEngine"]
