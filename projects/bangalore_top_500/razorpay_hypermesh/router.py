"""
Razorpay Project HyperMesh: Multi-Rail Payment Route Arbiter
Dynamically monitors bank gateway health telemetry, error rates, and latency,
routing transactions across optimal acquiring banks in <2ms with zero downtime.
"""
import time
import math
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class BankGatewayNode:
    bank_code: str
    gateway_id: str
    success_rate_window: List[bool] = field(default_factory=list)
    latency_ms_window: List[float] = field(default_factory=list)
    max_window: int = 100
    is_active: bool = True

    def record_attempt(self, success: bool, latency_ms: float):
        self.success_rate_window.append(success)
        self.latency_ms_window.append(latency_ms)
        if len(self.success_rate_window) > self.max_window:
            self.success_rate_window.pop(0)
            self.latency_ms_window.pop(0)

    @property
    def health_score(self) -> float:
        if not self.is_active or not self.success_rate_window:
            return 0.0
        sr = sum(self.success_rate_window) / len(self.success_rate_window)
        avg_lat = sum(self.latency_ms_window) / len(self.latency_ms_window)
        lat_penalty = min(avg_lat / 500.0, 1.0) * 0.3
        return max(0.0, (sr * 0.7) + (0.3 - lat_penalty))

class HyperMeshRouter:
    def __init__(self):
        self.gateways: Dict[str, BankGatewayNode] = {}

    def register_gateway(self, bank_code: str, gateway_id: str):
        self.gateways[gateway_id] = BankGatewayNode(bank_code=bank_code, gateway_id=gateway_id)

    def select_optimal_gateway(self, preferred_bank: Optional[str] = None) -> Optional[BankGatewayNode]:
        candidates = list(self.gateways.values())
        if preferred_bank:
            bank_candidates = [g for g in candidates if g.bank_code == preferred_bank and g.health_score > 0.4]
            if bank_candidates:
                return max(bank_candidates, key=lambda g: g.health_score)

        healthy_candidates = [g for g in candidates if g.health_score > 0.3]
        if not healthy_candidates:
            return None
        return max(healthy_candidates, key=lambda g: g.health_score)

    def route_and_execute(self, payment_intent_id: str, amount_inr: float, preferred_bank: Optional[str] = None):
        t0 = time.perf_counter()
        gateway = self.select_optimal_gateway(preferred_bank)
        if not gateway:
            return {
                "intent_id": payment_intent_id,
                "status": "FAILED_ALL_RAILS_DEGRADED",
                "route_latency_ms": (time.perf_counter() - t0) * 1000
            }
        
        # Simulated routing decision in <2ms
        route_latency = (time.perf_counter() - t0) * 1000
        return {
            "intent_id": payment_intent_id,
            "status": "ROUTED_SUCCESS",
            "selected_bank": gateway.bank_code,
            "gateway_id": gateway.gateway_id,
            "health_score": round(gateway.health_score, 4),
            "route_latency_ms": round(route_latency, 3)
        }
