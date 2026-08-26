"""
EMPIRICAL PROVIDER HEALTH ENGINE (HARDENED)
Tracks real latency, uptime, error rates, and failure history.
No synthetic health values. Default state is UNKNOWN until measured.
Maturity Lifecycle: UNKNOWN -> PROVISIONAL -> HEALTHY -> DEGRADED -> DOWN
"""
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class ProviderHealthRecord:
    provider: str
    model: str
    status: str = "UNKNOWN"  # UNKNOWN, PROVISIONAL, HEALTHY, DEGRADED, DOWN
    sample_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    success_rate: float = 0.0
    latency_ms_p50: Optional[float] = None
    latency_ms_p95: Optional[float] = None
    last_success_time: Optional[float] = None
    last_failure_time: Optional[float] = None
    last_error: Optional[str] = None
    last_checked: float = field(default_factory=time.time)
    _latencies: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("_latencies", None)
        return d

class EmpiricalHealthEngine:
    def __init__(
        self,
        min_provisional_samples: int = 1,
        min_healthy_samples: int = 3,
        healthy_threshold: float = 0.85,
        degraded_threshold: float = 0.40
    ):
        self.min_provisional_samples = min_provisional_samples
        self.min_healthy_samples = min_healthy_samples
        self.healthy_threshold = healthy_threshold
        self.degraded_threshold = degraded_threshold
        self._records: Dict[str, ProviderHealthRecord] = {}

    def _get_key(self, provider: str, model: str) -> str:
        return f"{provider}::{model}"

    def get_health(self, provider: str, model: str) -> ProviderHealthRecord:
        key = self._get_key(provider, model)
        if key not in self._records:
            self._records[key] = ProviderHealthRecord(provider=provider, model=model)
        return self._records[key]

    def record_real_call(
        self,
        provider: str,
        model: str,
        success: bool,
        latency_ms: float,
        error: Optional[str] = None
    ) -> ProviderHealthRecord:
        rec = self.get_health(provider, model)
        rec.sample_count += 1
        rec.last_checked = time.time()

        if success:
            rec.success_count += 1
            rec.last_success_time = time.time()
            rec._latencies.append(latency_ms)
            if len(rec._latencies) > 100:
                rec._latencies.pop(0)
        else:
            rec.failure_count += 1
            rec.last_failure_time = time.time()
            rec.last_error = error or "Unknown execution error"

        rec.success_rate = round(rec.success_count / max(1, rec.sample_count), 4)

        # Compute Latency percentiles if samples exist
        if rec._latencies:
            sorted_lats = sorted(rec._latencies)
            p50_idx = int(len(sorted_lats) * 0.5)
            p95_idx = int(len(sorted_lats) * 0.95)
            rec.latency_ms_p50 = round(sorted_lats[p50_idx], 2)
            rec.latency_ms_p95 = round(sorted_lats[min(len(sorted_lats)-1, p95_idx)], 2)

        # Mature State Transition Logic based strictly on real evidence
        if rec.sample_count == 0:
            rec.status = "UNKNOWN"
        elif rec.sample_count < self.min_healthy_samples:
            if rec.success_count > 0:
                rec.status = "PROVISIONAL"
            else:
                rec.status = "DOWN"
        else:
            if rec.success_rate >= self.healthy_threshold:
                rec.status = "HEALTHY"
            elif rec.success_rate >= self.degraded_threshold:
                rec.status = "DEGRADED"
            else:
                rec.status = "DOWN"

        return rec

    def get_all_records(self) -> Dict[str, Dict[str, Any]]:
        return {k: v.to_dict() for k, v in self._records.items()}

    def get_all_scores(self) -> Dict[str, Dict[str, Any]]:
        return self.get_all_records()

empirical_health = EmpiricalHealthEngine()

# Backwards compatibility aliases
ProviderHealthEngine = EmpiricalHealthEngine
ProviderHealthScore = ProviderHealthRecord
