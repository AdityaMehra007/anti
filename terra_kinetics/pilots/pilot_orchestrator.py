"""
Pilot Orchestrator and SLA Verification Harness.
Monitors operational readiness, shift execution, autonomous throughput, and economic ROI.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import time


class PilotStatus(str, Enum):
    PRE_FLIGHT_CHECK = "pre_flight_check"
    ACTIVE_PRODUCTION = "active_production"
    DEGRADED_ASSISTANCE = "degraded_assistance"
    HALTED = "halted"
    COMPLETED = "completed"


@dataclass
class SitePreflightCriteria:
    min_lighting_lux: float = 300.0
    max_network_jitter_ms: float = 4.5
    estop_bus_verified: bool = True
    workspace_perimeter_clear: bool = True


@dataclass
class ShiftPerformanceMetrics:
    shift_id: str
    facility_name: str
    total_cycles_attempted: int = 0
    successful_cycles: int = 0
    autonomous_cycles: int = 0
    teleop_interventions: int = 0
    duration_hours: float = 8.0
    baseline_human_wage_hourly: float = 28.50
    terra_billing_hourly: float = 7.50

    @property
    def autonomy_rate_pct(self) -> float:
        if self.total_cycles_attempted == 0:
            return 100.0
        return (self.autonomous_cycles / self.total_cycles_attempted) * 100.0

    @property
    def cycles_per_hour(self) -> float:
        if self.duration_hours <= 0:
            return 0.0
        return self.successful_cycles / self.duration_hours

    @property
    def net_savings_usd(self) -> float:
        human_cost = self.duration_hours * self.baseline_human_wage_hourly
        terra_cost = self.duration_hours * self.terra_billing_hourly
        return round(human_cost - terra_cost, 2)


class PilotDeploymentOrchestrator:
    """
    Manages customer pilot execution, safety gating, and shift telemetry.
    """

    def __init__(self, facility_name: str, site_criteria: Optional[SitePreflightCriteria] = None):
        self.facility_name = facility_name
        self.site_criteria = site_criteria or SitePreflightCriteria()
        self.status = PilotStatus.PRE_FLIGHT_CHECK
        self.metrics_history: List[ShiftPerformanceMetrics] = []

    def run_preflight_audit(self, measured_lux: float, measured_jitter_ms: float) -> Tuple[bool, str]:
        """
        Validates environmental and network conditions before greenlighting autonomous run.
        """
        if measured_lux < self.site_criteria.min_lighting_lux:
            return False, f"Lighting below threshold: {measured_lux} lux (required {self.site_criteria.min_lighting_lux})"

        if measured_jitter_ms > self.site_criteria.max_network_jitter_ms:
            return False, f"Network latency jitter too high: {measured_jitter_ms} ms (max {self.site_criteria.max_network_jitter_ms})"

        if not self.site_criteria.estop_bus_verified:
            return False, "Hardware emergency stop loop is unverified."

        self.status = PilotStatus.ACTIVE_PRODUCTION
        return True, "Site preflight passed. Greenlighted for autonomous production."

    def execute_shift(
        self,
        shift_id: str,
        total_picks: int,
        failure_rate: float = 0.004,  # 0.4% failure -> 99.6% autonomy
        duration_hours: float = 8.0,
    ) -> ShiftPerformanceMetrics:
        """
        Executes a production shift and computes contractual SLA delivery.
        """
        if self.status != PilotStatus.ACTIVE_PRODUCTION:
            raise RuntimeError(f"Cannot execute shift while orchestrator is in status: {self.status}")

        interventions = int(total_picks * failure_rate)
        autonomous = total_picks - interventions

        shift = ShiftPerformanceMetrics(
            shift_id=shift_id,
            facility_name=self.facility_name,
            total_cycles_attempted=total_picks,
            successful_cycles=total_picks,  # All resolved autonomously or via shadow tele-op
            autonomous_cycles=autonomous,
            teleop_interventions=interventions,
            duration_hours=duration_hours,
        )

        self.metrics_history.append(shift)
        return shift
