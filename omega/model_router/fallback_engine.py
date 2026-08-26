"""
EXPLICIT FALLBACK ENGINE (HARDENED)
Executes failovers: PRIMARY -> SECONDARY -> TERTIARY -> LOCAL -> QUEUE.
Logs all transition steps in the ledger. Zero silent simulation in live mode.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .client import OmniRouteClient, ModelResponse, ExecutionMode
from ..engines.transaction_ledger import ImmutableTransactionLedger

@dataclass
class FallbackLog:
    attempted_models: List[str]
    successful_model: Optional[str]
    errors: List[str]
    status: str

class FallbackEngine:
    def __init__(self, client: Optional[OmniRouteClient] = None, ledger: Optional[ImmutableTransactionLedger] = None):
        self.client = client or OmniRouteClient()
        self.ledger = ledger or ImmutableTransactionLedger()

    def execute_with_fallback(
        self,
        chain: List[str],
        messages: List[Dict[str, str]],
        mode: ExecutionMode = ExecutionMode.LIVE,
        temperature: float = 0.7,
        trace_id: Optional[str] = None
    ) -> ModelResponse:
        tr_id = trace_id or f"TRC-FB-{int(self.client.total_requests+1)}"
        attempted = []
        errors = []

        for idx, model in enumerate(chain):
            attempted.append(model)
            resp = self.client.generate(
                model=model,
                messages=messages,
                mode=mode,
                temperature=temperature,
                trace_id=tr_id
            )
            if resp.success and resp.content:
                if idx > 0:
                    resp.fallback_used = True
                    resp.fallback_from = chain[0]
                    resp.fallback_to = model
                    self.ledger.record(
                        tr_id, "FallbackEngine", model, mode.value, "FALLBACK_SUCCESS",
                        f"Failover from {chain[0]} to {model}", f"Succeeded with latency {resp.latency_ms}ms"
                    )
                return resp
            else:
                err = resp.error or "Unknown failure"
                errors.append(f"{model}: {err}")
                self.ledger.record(
                    tr_id, "FallbackEngine", model, mode.value, "FALLBACK_ATTEMPT_FAILED",
                    f"Attempted {model}", f"Failed with {err}"
                )

        err_summary = "; ".join(errors)
        return ModelResponse(
            content="",
            model=chain[0] if chain else "none",
            provider="OmniRoute-Fallback",
            gateway=self.client.base_url,
            status="UNAVAILABLE",
            execution_mode=mode.value,
            success=False,
            verified=False,
            error=f"ALL_FALLBACKS_EXHAUSTED: {err_summary}",
            fallback_used=True if len(chain) > 1 else False,
            fallback_from=chain[0] if chain else None,
            trace_id=tr_id
        )
