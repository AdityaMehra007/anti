"""
Terra Kinetics: Edge Runtime & Deterministic Safety Kernel (Terra-OS Kernel v0.1)

Provides real-time (200 Hz) execution, uncertainty-driven tele-op handover,
and deterministic ISO 13849 safety envelope enforcement.
"""

from typing import Callable, Dict, List, Optional, Tuple
import time
import logging
from ..protocol.ukp_schema import (
    ActionTokenPacket,
    ControlMode,
    HardwareAbstractionLayer,
    RobotMorphology,
    SafetyEnvelope,
    SafetyState,
    SensorTelemetryPacket,
)

logger = logging.getLogger("TerraEdgeKernel")


class ShadowInterventionVault:
    """
    Records corner-case failure trajectories and human recovery sequences.
    This directly powers the self-reinforcing training data flywheel.
    """
    def __init__(self):
        self.recorded_trajectories: List[Dict] = []

    def record_incident(self, telemetry: SensorTelemetryPacket, rejected_action: ActionTokenPacket, reason: str):
        record = {
            "timestamp": time.time_ns(),
            "robot_id": telemetry.robot_id,
            "morphology": telemetry.morphology.value,
            "rejection_reason": reason,
            "confidence": rejected_action.model_confidence_score,
            "joints_snapshot": [j.__dict__ for j in telemetry.joints],
            "rejected_action_id": rejected_action.token_id,
        }
        self.recorded_trajectories.append(record)
        logger.warning(f"[VAULT] Incident recorded for {telemetry.robot_id}: {reason}")


class TerraEdgeKernel:
    """
    The deterministic local runtime running at 200 Hz on robotic edge compute.
    """

    def __init__(
        self,
        robot_id: str,
        morphology: RobotMorphology,
        hal: Optional[HardwareAbstractionLayer] = None,
        teleop_fallback_cb: Optional[Callable[[SensorTelemetryPacket], ActionTokenPacket]] = None,
    ):
        self.robot_id = robot_id
        self.morphology = morphology
        self.hal = hal or HardwareAbstractionLayer(morphology=morphology)
        self.teleop_fallback_cb = teleop_fallback_cb
        self.intervention_vault = ShadowInterventionVault()
        self.safety_state = SafetyState.NOMINAL
        self.cycle_count = 0
        self.total_interventions = 0

    def step(
        self,
        telemetry: SensorTelemetryPacket,
        proposed_action: ActionTokenPacket,
    ) -> Tuple[ActionTokenPacket, SafetyState]:
        """
        Executes a single 200 Hz cycle (5 ms tick).
        Validates the proposed action against the physical envelope and confidence bounds.
        """
        self.cycle_count += 1
        t_start = time.perf_counter()

        # 1. Telemetry sanity check
        if telemetry.latency_ms > self.hal.safety_envelope.max_allowable_latency_ms:
            self.safety_state = SafetyState.DEGRADED_CAUTION
            self.intervention_vault.record_incident(
                telemetry, proposed_action, f"High latency spike: {telemetry.latency_ms} ms"
            )

        # 2. Tele-Op Intervention Check (Model Uncertainty / OOD Flag)
        if proposed_action.requires_human_verification or proposed_action.model_confidence_score < 0.95:
            self.safety_state = SafetyState.INTERVENTION_REQUIRED
            self.total_interventions += 1
            self.intervention_vault.record_incident(
                telemetry, proposed_action, f"Uncertainty flag (conf: {proposed_action.model_confidence_score:.3f})"
            )
            if self.teleop_fallback_cb:
                safe_action = self.teleop_fallback_cb(telemetry)
                safe_action.requires_human_verification = True
                return safe_action, self.safety_state
            else:
                return self._generate_damping_hold_command(telemetry), SafetyState.INTERVENTION_REQUIRED

        # 3. Deterministic Physical Envelope Verification
        is_valid, reason = self.hal.validate_command(proposed_action)
        if not is_valid:
            # Fatal torque or workspace breach -> Emergency Stop
            self.safety_state = SafetyState.EMERGENCY_STOP
            self.intervention_vault.record_incident(telemetry, proposed_action, f"Physical breach: {reason}")
            return self._generate_damping_hold_command(telemetry), SafetyState.EMERGENCY_STOP

        # Nominal execution
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0
        if elapsed_ms > 5.0:
            logger.warning(f"Kernel cycle exceeded 5ms deadline: {elapsed_ms:.2f} ms")

        self.safety_state = SafetyState.NOMINAL
        return proposed_action, self.safety_state

    def _generate_damping_hold_command(self, telemetry: SensorTelemetryPacket) -> ActionTokenPacket:
        """
        Generates zero-velocity high-damping hold commands to safely arrest the robot.
        """
        from ..protocol.ukp_schema import JointTargetCommand

        hold_cmds = [
            JointTargetCommand(
                joint_id=j.joint_id,
                target_position=j.position_rad,
                target_velocity=0.0,
                feedforward_torque=0.0,
                kp_stiffness=20.0,
                kd_damping=80.0,  # Pure viscous damping
            )
            for j in telemetry.joints
        ]
        return ActionTokenPacket(
            token_id=f"estop_{time.time_ns()}",
            target_timestamp_ns=time.time_ns() + 5_000_000,
            control_mode=ControlMode.TORQUE_IMPEDANCE,
            joint_commands=hold_cmds,
            model_confidence_score=1.0,
            requires_human_verification=True,
        )
