"""CRM forwarder package."""
import importlib

_mod = importlib.import_module("REVENUE_OS.05_CRM.crm_pipeline")
CRMPipeline = _mod.CRMPipeline

__all__ = ["CRMPipeline"]
