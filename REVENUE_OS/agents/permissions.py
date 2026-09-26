"""Permissions forwarder."""
import importlib

_mod = importlib.import_module("REVENUE_OS.14_AI_AGENTS.permissions")
PermissionEnforcer = _mod.PermissionEnforcer
PermissionDeniedError = _mod.PermissionDeniedError

__all__ = ["PermissionEnforcer", "PermissionDeniedError"]
