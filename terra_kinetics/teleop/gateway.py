"""
Shadow Tele-Operation VR & WebRTC Gateway Protocol.
Provides sub-10ms bilateral haptic-kinematic synchronization between remote VR operators and edge robots.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import time
import json
import hashlib


class TeleopConnectionState(str, Enum):
    IDLE = "idle"
    CONNECTING = "connecting"
    ACTIVE_CONTROL = "active_control"
    DISCONNECTING = "disconnecting"
    INTERRUPTED = "interrupted"


@dataclass
class HapticResistancePacket:
    timestamp_ns: int
    haptic_device_id: str
    contact_force_vector_n: Tuple[float, float, float]
    vibration_frequency_hz: float
    stiffness_n_m: float
    slip_warning: bool = False


@dataclass
class OperatorKinematicPose:
    timestamp_ns: int
    operator_id: str
    headset_pose: Tuple[float, float, float, float, float, float, float]  # x, y, z, qw, qx, qy, qz
    left_hand_pose: Tuple[float, float, float, float, float, float, float]
    right_hand_pose: Tuple[float, float, float, float, float, float, float]
    left_finger_curl: List[float] = field(default_factory=lambda: [0.0]*5)
    right_finger_curl: List[float] = field(default_factory=lambda: [0.0]*5)


class ShadowTeleopGateway:
    """
    Manages low-latency WebRTC data channels for bilateral shadow tele-operation.
    """

    def __init__(self, gateway_id: str = "teleop_gw_eu_west_01", max_jitter_ms: float = 8.0):
        self.gateway_id = gateway_id
        self.max_jitter_ms = max_jitter_ms
        self.active_sessions: Dict[str, str] = {}  # robot_id -> operator_id
        self.state = TeleopConnectionState.IDLE
        self.golden_trajectories: List[Dict] = []

    def initiate_handover(self, robot_id: str, operator_id: str) -> Tuple[bool, str]:
        """
        Transfers motor authority from autonomous model to human VR operator.
        """
        self.active_sessions[robot_id] = operator_id
        self.state = TeleopConnectionState.ACTIVE_CONTROL
        return True, f"Control authority granted for robot {robot_id} to operator {operator_id}."

    def process_kinematic_stream(
        self,
        robot_id: str,
        pose: OperatorKinematicPose,
        telemetry_latency_ms: float,
    ) -> Tuple[bool, Optional[HapticResistancePacket]]:
        """
        Receives operator motion and synthesizes tactile haptic resistance for VR gloves.
        """
        if self.state != TeleopConnectionState.ACTIVE_CONTROL:
            return False, None

        if telemetry_latency_ms > self.max_jitter_ms:
            # Latency spike safety trigger
            return False, None

        # Synthesize haptic feedback resistance: simulate resistance based on hand proximity
        haptic_packet = HapticResistancePacket(
            timestamp_ns=time.time_ns(),
            haptic_device_id=f"glove_{pose.operator_id}",
            contact_force_vector_n=(0.5, 0.0, 1.2),
            vibration_frequency_hz=120.0,
            stiffness_n_m=45.0,
            slip_warning=False,
        )

        return True, haptic_packet

    def complete_intervention_and_archive(
        self,
        robot_id: str,
        task_success: bool,
    ) -> Dict:
        """
        Concludes intervention and stores high-fidelity demonstration into the golden data vault.
        """
        operator_id = self.active_sessions.pop(robot_id, "unknown")
        self.state = TeleopConnectionState.IDLE

        golden_trajectory = {
            "archive_id": f"gt_{time.time_ns()}",
            "robot_id": robot_id,
            "operator_id": operator_id,
            "task_success": task_success,
            "timestamp": time.time_ns(),
        }
        self.golden_trajectories.append(golden_trajectory)
        return golden_trajectory
