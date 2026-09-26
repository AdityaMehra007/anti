"""Agent evaluator forwarder."""
import importlib

_mod = importlib.import_module("REVENUE_OS.14_AI_AGENTS.agent_evaluator")
AgentEvaluator = _mod.AgentEvaluator

__all__ = ["AgentEvaluator"]
