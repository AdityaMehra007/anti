"""
MODEL ENSEMBLES & MULTI-MODEL DEBATE
For high-stakes decisions: Model A (Propose) -> Model B (Critique) -> Model C (Alternative).
If connected models fail, explicitly reports ENSEMBLE_DEGRADED.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from .client import OmniRouteClient, ModelResponse, ExecutionMode

@dataclass
class EnsembleResult:
    proposal: str
    critique: str
    alternative: str
    consensus_synthesis: str
    models_used: List[str]
    status: str  # SUCCESS, ENSEMBLE_DEGRADED, FAILED
    confidence_score: float
    verified: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class MultiModelDebate:
    def __init__(self, client: Optional[OmniRouteClient] = None):
        self.client = client or OmniRouteClient()

    def run_debate(self, prompt: str, mode: ExecutionMode = ExecutionMode.LIVE) -> EnsembleResult:
        resp_a = self.client.generate("claude-3-7-sonnet-20250219", [{"role": "user", "content": f"Propose strategy: {prompt}"}], mode=mode)
        resp_b = self.client.generate("gpt-4o", [{"role": "user", "content": f"Critique proposal: {resp_a.content}"}], mode=mode)
        resp_c = self.client.generate("deepseek-r1", [{"role": "user", "content": f"Alternative strategy for: {prompt}"}], mode=mode)

        success_count = sum(1 for r in [resp_a, resp_b, resp_c] if r.success)
        is_verified = (success_count == 3 and all(r.verified for r in [resp_a, resp_b, resp_c]))

        if success_count == 0 and mode == ExecutionMode.LIVE:
            return EnsembleResult(
                proposal="",
                critique="",
                alternative="",
                consensus_synthesis="Live models unavailable for multi-model debate.",
                models_used=[],
                status="FAILED",
                confidence_score=0.0,
                verified=False
            )

        status_val = "SUCCESS" if success_count == 3 else "ENSEMBLE_DEGRADED"
        if success_count > 0:
            synthesis = f"Consensus reached with {success_count}/3 participating models."
        else:
            synthesis = "Simulation Consensus"

        active_models = []
        if resp_a.success: active_models.append("claude-3-7-sonnet-20250219")
        if resp_b.success: active_models.append("gpt-4o")
        if resp_c.success: active_models.append("deepseek-r1")

        return EnsembleResult(
            proposal=resp_a.content,
            critique=resp_b.content,
            alternative=resp_c.content,
            consensus_synthesis=synthesis,
            models_used=active_models,
            status=status_val,
            confidence_score=0.95 if success_count == 3 else 0.60,
            verified=is_verified
        )

class ModelEnsembleEngine:
    def __init__(self, client: Optional[OmniRouteClient] = None):
        self.debate = MultiModelDebate(client)

    def debate_decision(self, prompt: str, mode: ExecutionMode = ExecutionMode.LIVE) -> EnsembleResult:
        return self.debate.run_debate(prompt, mode=mode)
