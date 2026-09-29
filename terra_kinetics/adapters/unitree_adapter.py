"""
Unitree Humanoid Adapter (G1 / H1 Bipedal Humanoid).
Translates low-level MotorCmd / MotorState UDP DDS packets into UKP format.
"""

from typing import Dict, List, Optional
import time
from ..protocol.ukp_schema import (
    ActionTokenPacket,
    ControlMode,
    JointState,
    JointTargetCommand,
    RobotMorphology,
    SensorTelemetryPacket,
)


class UnitreeHumanoidAdapter:
    """
    Adapter for Unitree G1 (23-DOF) and H1 (19-27 DOF) bipedal humanoids.
    """

    HUMANOID_JOINTS = [
        # Left Leg (6 DOF)
        "left_hip_yaw", "left_hip_roll", "left_hip_pitch", "left_knee", "left_ankle_pitch", "left_ankle_roll",
        # Right Leg (6 DOF)
        "right_hip_yaw", "right_hip_roll", "right_hip_pitch", "right_knee", "right_ankle_pitch", "right_ankle_roll",
        # Waist (1 DOF)
        "waist_yaw",
        # Left Arm (4 DOF)
        "left_shoulder_pitch", "left_shoulder_roll", "left_shoulder_yaw", "left_elbow",
        # Right Arm (4 DOF)
        "right_shoulder_pitch", "right_shoulder_roll", "right_shoulder_yaw", "right_elbow",
    ]

    def __init__(self, robot_serial: str = "unitree_g1_001"):
        self.robot_serial = robot_serial
        self.morphology = RobotMorphology.BIPEDAL_HUMANOID

    def parse_dds_states(
        self,
        positions: List[float],
        velocities: List[float],
        torques: List[float],
        temperatures: Optional[List[float]] = None,
    ) -> SensorTelemetryPacket:
        """
        Parses Unitree CycloneDDS low-state struct into standardized UKP SensorTelemetryPacket.
        """
        joints = []
        temps = temperatures or [30.0] * len(self.HUMANOID_JOINTS)

        for i, name in enumerate(self.HUMANOID_JOINTS):
            joints.append(
                JointState(
                    joint_id=name,
                    position_rad=positions[i] if i < len(positions) else 0.0,
                    velocity_rad_s=velocities[i] if i < len(velocities) else 0.0,
                    effort_nm=torques[i] if i < len(torques) else 0.0,
                    temperature_c=temps[i] if i < len(temps) else 30.0,
                )
            )

        return SensorTelemetryPacket(
            robot_id=self.robot_serial,
            morphology=self.morphology,
            timestamp_ns=time.time_ns(),
            joints=joints,
            latency_ms=1.8,
        )

    def generate_low_cmd_packet(self, action: ActionTokenPacket) -> Dict[str, Dict[str, float]]:
        """
        Converts UKP action into Unitree low-level motor command map (q, dq, kp, kd, tau).
        """
        cmd_map = {cmd.joint_id: cmd for cmd in action.joint_commands}
        unitree_packet = {}

        for joint_name in self.HUMANOID_JOINTS:
            if joint_name in cmd_map:
                c = cmd_map[joint_name]
                unitree_packet[joint_name] = {
                    "q": c.target_position,
                    "dq": c.target_velocity,
                    "kp": c.kp_stiffness,
                    "kd": c.kd_damping,
                    "tau": c.feedforward_torque,
                }
            else:
                unitree_packet[joint_name] = {"q": 0.0, "dq": 0.0, "kp": 0.0, "kd": 0.0, "tau": 0.0}

        return unitree_packet
