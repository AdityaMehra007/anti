"""
Ather Energy Project GridMatrix: Vehicle-to-Grid (V2G) Energy Telemetry & Load Balancer
Monitors battery state-of-charge (SoC), grid frequency harmonics, and dynamically schedules
high-power charging to prevent transformer brownouts.
"""
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ChargingPod:
    pod_id: str
    max_kw: float
    current_kw: float
    connected_vehicle_id: str = ""
    battery_soc_pct: float = 0.0

class GridMatrixController:
    def __init__(self, substation_capacity_kw: float = 500.0):
        self.capacity_kw = substation_capacity_kw
        self.pods: Dict[str, ChargingPod] = {}

    def register_pod(self, pod_id: str, max_kw: float = 22.0):
        self.pods[pod_id] = ChargingPod(pod_id=pod_id, max_kw=max_kw, current_kw=0.0)

    def optimize_load(self, grid_frequency_hz: float):
        total_requested = sum(p.max_kw for p in self.pods.values() if p.connected_vehicle_id)
        if total_requested == 0:
            return

        # If grid frequency is low (< 49.8 Hz), throttle charging rate
        scale_factor = 1.0
        if grid_frequency_hz < 49.8:
            scale_factor = 0.5 # Reduce demand by 50% to prevent grid failure
        elif total_requested > self.capacity_kw:
            scale_factor = self.capacity_kw / total_requested

        for p in self.pods.values():
            if p.connected_vehicle_id:
                # Prioritize vehicles with low SoC (< 30%)
                boost = 1.2 if p.battery_soc_pct < 30.0 else 0.9
                p.current_kw = round(min(p.max_kw, p.max_kw * scale_factor * boost), 2)
            else:
                p.current_kw = 0.0
