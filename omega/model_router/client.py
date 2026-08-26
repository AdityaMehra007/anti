"""
TRUTHFUL OMNIROUTE GATEWAY CLIENT (NO FAKE RESPONSES)
Connects to OmniRoute OpenAI-compatible gateway (e.g., http://localhost:20128/v1).
Strictly distinguishes LIVE, SANDBOX, and SIMULATION modes.
Never converts live network failures into simulated successes.
"""
import os
import time
import uuid
import json
import urllib.request
import urllib.parse
import urllib.error
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from .health_engine import empirical_health

class ExecutionMode(str, Enum):
    LIVE = "LIVE"
    SANDBOX = "SANDBOX"
    SIMULATION = "SIMULATION"

@dataclass
class ModelResponse:
    content: str
    model: str
    provider: str
    gateway: str
    status: str  # SUCCESS, FAILED, UNAVAILABLE, RATE_LIMITED, BLOCKED
    execution_mode: str  # LIVE, SANDBOX, SIMULATION
    success: bool
    verified: bool
    error: Optional[str] = None
    latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    tokens_estimated: bool = False
    cost_usd: float = 0.0
    cost_source: str = "UNKNOWN"  # DISCOVERED_PRICE, CONFIGURED_PRICE, UNKNOWN
    trace_id: str = ""
    cached: bool = False
    compressed: bool = False
    fallback_used: bool = False
    fallback_from: Optional[str] = None
    fallback_to: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class OmniRouteClient:
    def __init__(
        self,
        base_url: str = "http://localhost:20128/v1",
        api_key: Optional[str] = None,
        default_mode: ExecutionMode = ExecutionMode.LIVE,
        timeout: float = 1.5
    ):
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key or os.environ.get("OMNIROUTE_API_KEY", "")
        self.default_mode = default_mode
        self.timeout = timeout
        self.total_requests = 0
        self.total_successes = 0
        self.total_failures = 0

    def generate(
        self,
        model: str,
        messages: List[Dict[str, str]],
        provider: str = "OmniRoute",
        mode: Optional[ExecutionMode] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        trace_id: Optional[str] = None
    ) -> ModelResponse:
        exec_mode = mode or self.default_mode
        tr_id = trace_id or f"TRC-{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        self.total_requests += 1

        # If explicitly in SIMULATION mode, return simulated mock data marked unverified
        if exec_mode == ExecutionMode.SIMULATION:
            latency = (time.time() - start_time) * 1000 + 5.0
            sim_content = f"[SIMULATION: {model}] Task processed in dry-run mode."
            p_tok = sum(len(m.get("content", "").split()) * 2 for m in messages)
            c_tok = len(sim_content.split()) * 2
            return ModelResponse(
                content=sim_content,
                model=model,
                provider=provider,
                gateway="SIMULATED_LOCAL",
                status="SUCCESS",
                execution_mode="SIMULATION",
                success=True,
                verified=False,
                error=None,
                latency_ms=round(latency, 2),
                prompt_tokens=p_tok,
                completion_tokens=c_tok,
                total_tokens=p_tok + c_tok,
                tokens_estimated=True,
                cost_usd=0.0,
                cost_source="UNKNOWN",
                trace_id=tr_id
            )

        # LIVE / SANDBOX execution -> Real HTTP Request to OmniRoute Gateway
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if tools:
            payload["tools"] = tools

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Omega-OmniRoute-Client/2.0"
        }
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/chat/completions",
                data=req_data,
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                latency = (time.time() - start_time) * 1000
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                p_tok = usage.get("prompt_tokens", 0)
                c_tok = usage.get("completion_tokens", 0)

                empirical_health.record_real_call(provider, model, True, latency)
                self.total_successes += 1

                return ModelResponse(
                    content=content,
                    model=model,
                    provider=data.get("provider", provider),
                    gateway=self.base_url,
                    status="SUCCESS",
                    execution_mode=exec_mode.value,
                    success=True,
                    verified=True,
                    error=None,
                    latency_ms=round(latency, 2),
                    prompt_tokens=p_tok,
                    completion_tokens=c_tok,
                    total_tokens=p_tok + c_tok,
                    tokens_estimated=False if usage else True,
                    cost_usd=round(usage.get("total_cost", 0.0), 6),
                    cost_source="DISCOVERED_PRICE" if "total_cost" in usage else "CONFIGURED_PRICE",
                    trace_id=tr_id
                )

        except urllib.error.HTTPError as he:
            latency = (time.time() - start_time) * 1000
            err_msg = f"HTTP_{he.code}: {he.reason}"
            status_code = "RATE_LIMITED" if he.code == 429 else "FAILED"
            empirical_health.record_real_call(provider, model, False, latency, err_msg)
            self.total_failures += 1

            return ModelResponse(
                content="",
                model=model,
                provider=provider,
                gateway=self.base_url,
                status=status_code,
                execution_mode=exec_mode.value,
                success=False,
                verified=False,
                error=err_msg,
                latency_ms=round(latency, 2),
                cost_source="UNKNOWN",
                trace_id=tr_id
            )

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            err_msg = f"{type(e).__name__}: {str(e)}"
            empirical_health.record_real_call(provider, model, False, latency, err_msg)
            self.total_failures += 1

            # CRITICAL: Return explicit UNAVAILABLE status. DO NOT SILENTLY SIMULATE.
            return ModelResponse(
                content="",
                model=model,
                provider=provider,
                gateway=self.base_url,
                status="UNAVAILABLE",
                execution_mode=exec_mode.value,
                success=False,
                verified=False,
                error=err_msg,
                latency_ms=round(latency, 2),
                cost_source="UNKNOWN",
                trace_id=tr_id
            )
