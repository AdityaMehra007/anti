"""
DETERMINISTIC MODEL RESPONSE CACHE (HARDENED & SAFE)
Caches safe, deterministic tasks (company metadata, standard summaries, classifications).
STRICT CACHE SAFETY: Never caches simulations, failures, unknowns, or unverified results.
"""
import time
import json
import hashlib
from typing import Optional, Dict, Any
from .client import ModelResponse

class ModelResponseCache:
    def __init__(self, ttl_seconds: int = 7200):
        self.ttl = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _hash_request(
        self,
        model: str,
        prompt: str,
        provider: str = "",
        tools: Optional[Any] = None,
        temperature: Optional[float] = None
    ) -> str:
        tools_str = json.dumps(tools, sort_keys=True) if tools else ""
        temp_str = str(temperature) if temperature is not None else ""
        raw = f"{provider}:{model}:{prompt}:{tools_str}:{temp_str}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(
        self,
        model: str,
        prompt: str,
        provider: str = "",
        tools: Optional[Any] = None,
        temperature: Optional[float] = None
    ) -> Optional[ModelResponse]:
        k = self._hash_request(model, prompt, provider, tools, temperature)
        entry = self._cache.get(k)
        if not entry:
            return None
        if time.time() > entry["expires_at"]:
            del self._cache[k]
            return None
        r = entry["response"]
        r.cached = True
        return r

    def set(
        self,
        model: str,
        prompt: str,
        response: ModelResponse,
        provider: str = "",
        tools: Optional[Any] = None,
        temperature: Optional[float] = None
    ):
        # STRICT CACHE SAFETY RULE: Only cache verified, live successful executions
        if not (response.success and response.verified and response.execution_mode == "LIVE"):
            return

        k = self._hash_request(model, prompt, provider or response.provider, tools, temperature)
        self._cache[k] = {
            "response": response,
            "expires_at": time.time() + self.ttl
        }
