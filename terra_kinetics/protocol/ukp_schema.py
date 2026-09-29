"""
Terra Kinetics: Universal Kinematic Protocol (UKP v0.1)
Open Specification for Hardware-Agnostic Embodied Robotics & Real-Time Action Tokens.

This protocol decouples high-level physical AI world models from heterogeneous robot hardware
(industrial arms, quadrupeds, wheeled AMRs, and bipedal humanoids).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import time
import math


class RobotMorphology(str, Enum):
    MANIPULATOR_6DOF = "manipulator_6dof"
    MANIPULATOR_7DOF = "manipulator_7dof"
    DEXTEROUS_HAND_5F = "dexterous_hand_5f"
    PARALLEL_GRIPPER = "parallel_gripper"
    WHEELED_AMR = "wheeled_amr"
    QUADRUPED = "quadruped"
    BIPEDAL_HUMANOID = "bipedal_humanoid"


class ControlMode(str, Enum):
    POSITION = "position"
    VELOCITY = "velocity"
    TORQUE_IMPEDANCE = "torque_impedance"
    CARTESIAN_POSE = "cartesian_pose"


class SafetyState(str, Enum):
    NOMINAL = "nominal"
    DEGRADED_CAUTION = "degraded_caution"
    INTERVENTION_REQUIRED = "intervention_required"
    EMERGENCY_STOP = "emergency_stop"


@dataclass
class JointState:
    joint_id: str
    position_rad: float
    velocity_rad_s: float
    effort_nm: float
    temperature_c: float
    fault_flag: bool = False


@dataclass
class CartesianPose:
    x: float
    y: float
    z: float
    qw: float = 1.0
    qx: float = 0.0
    qy: float = 0.0
    qz: float = 0.0


@dataclass
class TactileArrayReading:
    sensor_id: str
    normal_forces: List[float]  # Matrix flattened
    shear_forces_x: List[float]
    shear_forces_y: List[float]
    slip_detected: bool = False


@dataclass
class SensorTelemetryPacket:
    robot_id: str
    morphology: RobotMorphology
    timestamp_ns: int
    joints: List[JointState]
    end_effector_pose: Optional[CartesianPose] = None
    tactile_feedback: List[TactileArrayReading] = field(default_factory=list)
    battery_percentage: float = 100.0
    latency_ms: float = 0.0


@dataclass
class JointTargetCommand:
    joint_id: str
    target_position: float
    target_velocity: float = 0.0
    feedforward_torque: float = 0.0
    kp_stiffness: float = 100.0
    kd_damping: float = 10.0


@dataclass
class ActionTokenPacket:
    token_id: str
    target_timestamp_ns: int
    control_mode: ControlMode
    joint_commands: List[JointTargetCommand]
    gripper_target_aperture: Optional[float] = None  # 0.0 (closed) to 1.0 (fully open)
    model_confidence_score: float = 1.0  # 0.0 to 1.0
    requires_human_verification: bool = False


@dataclass
class SafetyEnvelope:
    max_cartesian_velocity_m_s: float = 1.5
    max_joint_torque_nm: float = 120.0
    workspace_bounds_min: Tuple[float, float, float] = (-1.5, -1.5, 0.0)
    workspace_bounds_max: Tuple[float, float, float] = (1.5, 1.5, 2.2)
    max_allowable_latency_ms: float = 15.0


class HardwareAbstractionLayer:
    """
    Normalizes vendor-specific kinematic configurations into standard UKP representation.
    """

    def __init__(self, morphology: RobotMorphology, safety_envelope: Optional[SafetyEnvelope] = None):
        self.morphology = morphology
        self.safety_envelope = safety_envelope or SafetyEnvelope()

    def validate_command(self, action: ActionTokenPacket) -> Tuple[bool, str]:
        """
        Deterministic safety validator verifying that action tokens obey the physical envelope.
        """
        for cmd in action.joint_commands:
            if abs(cmd.feedforward_torque) > self.safety_envelope.max_joint_torque_nm:
                return False, f"Torque limit breached on joint {cmd.joint_id}: {cmd.feedforward_torque} Nm"

        if action.model_confidence_score < 0.95 and not action.requires_human_verification:
            return False, f"Model confidence below safety threshold: {action.model_confidence_score:.3f}"

        return True, "Nominal"

    def normalize_action(self, raw_action_tensor: List[float], joint_names: List[str]) -> ActionTokenPacket:
        """
        Converts neural model output tensor into a standard UKP ActionTokenPacket.
        """
        cmds = []
        for i, name in enumerate(joint_names):
            val = raw_action_tensor[i] if i < len(raw_action_tensor) else 0.0
            cmds.append(JointTargetCommand(
                joint_id=name,
                target_position=val,
                target_velocity=0.0,
                feedforward_torque=0.0
            ))

        return ActionTokenPacket(
            token_id=f"token_{time.time_ns()}",
            target_timestamp_ns=time.time_ns() + 5_000_000,  # 5ms forward
            control_mode=ControlMode.POSITION,
            joint_commands=cmds,
            model_confidence_score=0.99
        )
