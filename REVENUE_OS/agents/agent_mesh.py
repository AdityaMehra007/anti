"""Agent mesh forwarder."""
import importlib

_mod = importlib.import_module("REVENUE_OS.14_AI_AGENTS.agent_mesh")
AgentMesh = _mod.AgentMesh
RevenueCommander = _mod.RevenueCommander

__all__ = ["AgentMesh", "RevenueCommander"]
