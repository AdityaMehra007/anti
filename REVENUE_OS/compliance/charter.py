"""Forwarder module for 22_COMPLIANCE/charter.py"""
import importlib

_mod = importlib.import_module("REVENUE_OS.22_COMPLIANCE.charter")
PermissionTier = _mod.PermissionTier
SecurityViolationError = _mod.SecurityViolationError
EthicalCharter = _mod.EthicalCharter

__all__ = ["PermissionTier", "SecurityViolationError", "EthicalCharter"]
