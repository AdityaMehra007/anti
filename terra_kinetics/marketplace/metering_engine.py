"""
Labor-as-a-Service (LaaS) Micro-Metering and Billing Engine.
Tracks operating seconds, action cycles, tele-op intervention fees, and generates cryptographic invoices.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import hashlib
import time


@dataclass
class RobotUsageSession:
    session_id: str
    robot_id: str
    customer_id: str
    start_time_ns: int
    end_time_ns: Optional[int] = None
    total_operating_seconds: float = 0.0
    action_cycles_executed: int = 0
    teleop_interventions_count: int = 0
    active_skills: List[str] = field(default_factory=list)


@dataclass
class CryptographicInvoiceReceipt:
    invoice_id: str
    customer_id: str
    robot_id: str
    total_operating_hours: float
    base_os_rate_hourly: float
    total_amount_usd: float
    timestamp_ns: int
    signature_hash: str


class LaasMeteringEngine:
    """
    Sub-second micro-metering engine for robotic fleet operations.
    """

    def __init__(
        self,
        base_os_hourly_rate_usd: float = 1.75,
        teleop_intervention_rate_usd: float = 0.50,
        pick_cycle_rate_usd: float = 0.005,
    ):
        self.base_os_hourly_rate_usd = base_os_hourly_rate_usd
        self.teleop_intervention_rate_usd = teleop_intervention_rate_usd
        self.pick_cycle_rate_usd = pick_cycle_rate_usd
        self.active_sessions: Dict[str, RobotUsageSession] = {}
        self.invoice_ledger: List[CryptographicInvoiceReceipt] = []

    def start_session(self, robot_id: str, customer_id: str) -> str:
        session_id = f"sess_{robot_id}_{time.time_ns()}"
        self.active_sessions[robot_id] = RobotUsageSession(
            session_id=session_id,
            robot_id=robot_id,
            customer_id=customer_id,
            start_time_ns=time.time_ns(),
        )
        return session_id

    def record_cycle(self, robot_id: str, is_intervention: bool = False, skill_id: Optional[str] = None):
        if robot_id not in self.active_sessions:
            return
        sess = self.active_sessions[robot_id]
        sess.action_cycles_executed += 1
        if is_intervention:
            sess.teleop_interventions_count += 1
        if skill_id and skill_id not in sess.active_skills:
            sess.active_skills.append(skill_id)

    def close_session_and_invoice(self, robot_id: str, secret_key: str = "terra_internal_key") -> Optional[CryptographicInvoiceReceipt]:
        if robot_id not in self.active_sessions:
            return None

        sess = self.active_sessions.pop(robot_id)
        sess.end_time_ns = time.time_ns()
        elapsed_sec = (sess.end_time_ns - sess.start_time_ns) / 1e9
        sess.total_operating_seconds = elapsed_sec

        operating_hours = elapsed_sec / 3600.0

        # Calculations
        base_os_cost = operating_hours * self.base_os_hourly_rate_usd
        cycle_cost = sess.action_cycles_executed * self.pick_cycle_rate_usd
        teleop_cost = sess.teleop_interventions_count * self.teleop_intervention_rate_usd

        total_due = round(base_os_cost + cycle_cost + teleop_cost, 4)

        invoice_id = f"inv_{time.time_ns()}"
        payload = f"{invoice_id}:{sess.customer_id}:{sess.robot_id}:{total_due}:{secret_key}"
        sig = hashlib.sha256(payload.encode()).hexdigest()

        receipt = CryptographicInvoiceReceipt(
            invoice_id=invoice_id,
            customer_id=sess.customer_id,
            robot_id=sess.robot_id,
            total_operating_hours=round(operating_hours, 4),
            base_os_rate_hourly=self.base_os_hourly_rate_usd,
            total_amount_usd=total_due,
            timestamp_ns=time.time_ns(),
            signature_hash=sig,
        )

        self.invoice_ledger.append(receipt)
        return receipt
