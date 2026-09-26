"""Forwarder module for 23_SETTINGS/config.py"""
import importlib

_mod = importlib.import_module("REVENUE_OS.23_SETTINGS.config")
get_config = _mod.get_config
RevenueOSConfig = _mod.RevenueOSConfig

__all__ = ["get_config", "RevenueOSConfig"]
