"""
APEX Observability, Telemetry & Cost Tracking
Collects step execution time, tool invocations, token throughput, and financial cost metrics.
"""
import time
from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class TelemetrySpan:
    span_id: str
    name: str
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    duration_ms: float = 0.0
    status: str = "RUNNING"
    token_usage: Dict[str, int] = field(default_factory=dict)
    cost_usd: float = 0.0

class ApexTelemetry:
    def __init__(self):
        self.spans: List[TelemetrySpan] = []
        self.active_spans: Dict[str, TelemetrySpan] = {}
        self.total_cost_usd: float = 0.0
        self.total_tokens: int = 0

    def start_span(self, span_id: str, name: str) -> TelemetrySpan:
        span = TelemetrySpan(span_id=span_id, name=name)
        self.active_spans[span_id] = span
        return span

    def end_span(self, span_id: str, status: str = "SUCCESS", tokens: int = 0, cost: float = 0.0):
        span = self.active_spans.pop(span_id, None)
        if span:
            span.end_time = time.time()
            span.duration_ms = round((span.end_time - span.start_time) * 1000, 2)
            span.status = status
            span.token_usage = {"total_tokens": tokens}
            span.cost_usd = cost
            self.spans.append(span)
            
            self.total_cost_usd += cost
            self.total_tokens += tokens

    def get_summary(self) -> Dict[str, Any]:
        total_spans = len(self.spans)
        successes = sum(1 for s in self.spans if s.status == "SUCCESS")
        failures = sum(1 for s in self.spans if s.status == "FAILED")
        avg_latency = (
            round(sum(s.duration_ms for s in self.spans) / total_spans, 2)
            if total_spans > 0 else 0.0
        )
        return {
            "total_spans": total_spans,
            "success_rate": round(successes / total_spans, 4) if total_spans > 0 else 1.0,
            "failures": failures,
            "avg_latency_ms": avg_latency,
            "total_tokens_consumed": self.total_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6)
        }
