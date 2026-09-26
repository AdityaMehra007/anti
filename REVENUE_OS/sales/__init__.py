"""Sales forwarder package."""
import importlib

_mod = importlib.import_module("REVENUE_OS.06_SALES.sales_assistant")
SalesAssistant = _mod.SalesAssistant

__all__ = ["SalesAssistant"]
