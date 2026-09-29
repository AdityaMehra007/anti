"""
Universal Robots (UR) Hardware Adapter (UR5e / UR10e / UR20).
Translates RTDE (Real-Time Data Exchange) joint vectors to/from UKP format.
"""

from typing import Dict, List, Tuple
import time
from ..protocol.ukp_schema import (
    ActionTokenPacket,
    ControlMode,
    JointState,
    JointTargetCommand,
    RobotMorphology,
    SensorTelemetryPacket,
)


class UniversalRobotsAdapter:
    """
    Adapter for Universal Robots e-Series and Next-Gen manipulators.
    Standard 6-DOF configuration: [base, shoulder, elbow, wrist_1, wrist_2, wrist_3].
    """

    JOINT_NAMES = [
        "shoulder_pan_joint",
        "shoulder_lift_joint",
        "elbow_joint",
        "wrist_1_joint",
        "wrist_2_joint",
        "wrist_3_joint",
    ]

    def __init__(self, robot_ip: str = "127.0.0.1", port: int = 30004):
        self.robot_ip = robot_ip
        self.port = port
        self.morphology = RobotMorphology.MANIPULATOR_6DOF

    def parse_rtde_telemetry(
        self,
        actual_q: List[float],
        actual_qd: List[float],
        target_moment: List[float],
        temperatures: List[float],
    ) -> SensorTelemetryPacket:
        """
        Parses raw RTDE binary vectors into standardized UKP SensorTelemetryPacket.
        """
        joints = []
        for i, name in enumerate(self.JOINT_NAMES):
            joints.append(
                JointState(
                    joint_id=name,
                    position_rad=actual_q[i] if i < len(actual_q) else 0.0,
                    velocity_rad_s=actual_qd[i] if i < len(actual_qd) else 0.0,
                    effort_nm=target_moment[i] if i < len(target_moment) else 0.0,
                    temperature_c=temperatures[i] if i < len(temperatures) else 25.0,
                )
            )

        return SensorTelemetryPacket(
            robot_id=f"ur_{self.robot_ip.replace('.', '_')}",
            morphology=self.morphology,
            timestamp_ns=time.time_ns(),
            joints=joints,
            latency_ms=1.2,
        )

    def format_urscript_servoj(self, action: ActionTokenPacket, time_step: float = 0.005) -> str:
        """
        Translates a UKP ActionTokenPacket into high-speed RTDE `servoj` command string.
        """
        # Build map for quick indexing
        cmd_map = {cmd.joint_id: cmd.target_position for cmd in action.joint_commands}
        targets = [cmd_map.get(name, 0.0) for name in self.JOINT_NAMES]

        targets_str = ", ".join(f"{t:.5f}" for t in targets)
        # servoj([q0, q1, q2, q3, q4, q5], a=0, v=0, t=0.005, lookahead_time=0.1, gain=300)
        return f"servoj([{targets_str}], t={time_step:.4f}, lookahead_time=0.08, gain=250)"
