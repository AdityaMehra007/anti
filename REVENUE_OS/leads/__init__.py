"""Leads forwarder package."""
import importlib

_mod = importlib.import_module("REVENUE_OS.04_LEADS.lead_engine")
LeadEngine = _mod.LeadEngine

__all__ = ["LeadEngine"]
