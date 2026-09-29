"""
Procedural Synthetic Trajectory Generator for Robotic Foundation Models.
Generates multi-step physical interaction episodes across randomized environments.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import time
import math
from .domain_randomizer import DomainRandomizer, RandomizedPhysicsEnvironment
from ..protocol.ukp_schema import (
    ActionTokenPacket,
    ControlMode,
    JointState,
    JointTargetCommand,
    RobotMorphology,
    SensorTelemetryPacket,
)


@dataclass
class TrajectoryStep:
    step_index: int
    telemetry: SensorTelemetryPacket
    action: ActionTokenPacket
    reward: float
    task_success: bool


class SyntheticTrajectoryGenerator:
    """
    Procedural trajectory generator modeling 6-DOF and bipedal manipulation tasks.
    """

    def __init__(self, randomizer: Optional[DomainRandomizer] = None):
        self.randomizer = randomizer or DomainRandomizer()

    def generate_pick_and_place_episode(
        self,
        robot_id: str = "sim_robot_01",
        num_steps: int = 50,
        seed: Optional[int] = None,
    ) -> List[TrajectoryStep]:
        """
        Generates an end-to-end pick-and-place trajectory under randomized physics.
        """
        env = self.randomizer.sample_environment(seed=seed)
        trajectory: List[TrajectoryStep] = []

        joint_names = [f"joint_{i+1}" for i in range(6)]
        current_q = [0.0] * 6

        for step_idx in range(num_steps):
            # Target trajectory follows smooth minimum-jerk sinusoids
            phase = (step_idx / float(num_steps)) * math.pi
            target_q = [
                0.5 * math.sin(phase),
                -0.8 * math.sin(phase),
                0.6 * math.sin(phase),
                -0.3 * math.cos(phase),
                0.2 * math.sin(phase * 2),
                0.1 * math.sin(phase),
            ]

            # Perturb actual readings by sensor noise and actuator backlash
            perturbed_q = self.randomizer.perturb_telemetry(current_q, env)
            joints = [
                JointState(
                    joint_id=name,
                    position_rad=perturbed_q[i],
                    velocity_rad_s=0.05 * math.cos(phase),
                    effort_nm=12.0 * math.sin(phase) * env.link_mass_multiplier,
                    temperature_c=32.0 + (step_idx * 0.1),
                )
                for i, name in enumerate(joint_names)
            ]

            telemetry = SensorTelemetryPacket(
                robot_id=robot_id,
                morphology=RobotMorphology.MANIPULATOR_6DOF,
                timestamp_ns=time.time_ns() + int(step_idx * 5_000_000),
                joints=joints,
                latency_ms=env.camera_latency_jitter_ms,
            )

            commands = [
                JointTargetCommand(
                    joint_id=name,
                    target_position=target_q[i],
                    target_velocity=0.05 * math.cos(phase),
                    feedforward_torque=5.0,
                )
                for i, name in enumerate(joint_names)
            ]

            action = ActionTokenPacket(
                token_id=f"sim_act_{step_idx}",
                target_timestamp_ns=telemetry.timestamp_ns + 5_000_000,
                control_mode=ControlMode.POSITION,
                joint_commands=commands,
                gripper_target_aperture=1.0 if step_idx < 25 else 0.0,
                model_confidence_score=0.985,
            )

            # Move current_q toward target
            current_q = [
                current_q[i] + (target_q[i] - current_q[i]) * 0.25
                for i in range(6)
            ]

            success = step_idx == (num_steps - 1)
            trajectory.append(
                TrajectoryStep(
                    step_index=step_idx,
                    telemetry=telemetry,
                    action=action,
                    reward=1.0 if success else 0.02 * step_idx,
                    task_success=success,
                )
            )

        return trajectory
