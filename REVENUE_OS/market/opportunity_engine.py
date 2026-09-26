"""Market forwarder package."""
import importlib

_mod = importlib.import_module("REVENUE_OS.03_MARKET.opportunity_engine")
OpportunityEngine = _mod.OpportunityEngine

__all__ = ["OpportunityEngine"]
