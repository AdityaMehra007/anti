"""
Terra Kinetics: Comprehensive Test Suite
Validates UKP Protocol, Edge Kernel Safety Envelopes, and Economic Projections.
"""

import pytest
import time
from terra_kinetics.protocol.ukp_schema import (
    ActionTokenPacket,
    ControlMode,
    HardwareAbstractionLayer,
    JointState,
    JointTargetCommand,
    RobotMorphology,
    SafetyEnvelope,
    SafetyState,
    SensorTelemetryPacket,
)
from terra_kinetics.runtime.terra_edge_kernel import TerraEdgeKernel
from terra_kinetics.sim.financial_flywheel_engine import FleetVentureSimulator


def test_ukp_safety_envelope_torque_breach():
    """Verify that excessive joint torque command is rejected by HAL."""
    hal = HardwareAbstractionLayer(
        morphology=RobotMorphology.MANIPULATOR_6DOF,
        safety_envelope=SafetyEnvelope(max_joint_torque_nm=100.0),
    )

    unsafe_action = ActionTokenPacket(
        token_id="tok_unsafe_1",
        target_timestamp_ns=time.time_ns(),
        control_mode=ControlMode.POSITION,
        joint_commands=[
            JointTargetCommand(joint_id="j1", target_position=0.5, feedforward_torque=150.0)  # > 100 Nm
        ],
        model_confidence_score=0.99,
    )

    is_valid, reason = hal.validate_command(unsafe_action)
    assert not is_valid
    assert "Torque limit breached" in reason


def test_edge_kernel_teleop_handover_on_uncertainty():
    """Verify that low model confidence triggers tele-op intervention handover."""
    def mock_human_teleop(telemetry: SensorTelemetryPacket) -> ActionTokenPacket:
        return ActionTokenPacket(
            token_id="tok_human_guided",
            target_timestamp_ns=time.time_ns(),
            control_mode=ControlMode.POSITION,
            joint_commands=[JointTargetCommand(joint_id="j1", target_position=0.1)],
            model_confidence_score=1.0,
            requires_human_verification=True,
        )

    kernel = TerraEdgeKernel(
        robot_id="robot_factory_alpha_01",
        morphology=RobotMorphology.MANIPULATOR_6DOF,
        teleop_fallback_cb=mock_human_teleop,
    )

    telemetry = SensorTelemetryPacket(
        robot_id="robot_factory_alpha_01",
        morphology=RobotMorphology.MANIPULATOR_6DOF,
        timestamp_ns=time.time_ns(),
        joints=[JointState(joint_id="j1", position_rad=0.0, velocity_rad_s=0.0, effort_nm=5.0, temperature_c=35.0)],
        latency_ms=2.1,
    )

    # Low confidence action (e.g. novel reflective object)
    uncertain_action = ActionTokenPacket(
        token_id="tok_uncertain_1",
        target_timestamp_ns=time.time_ns(),
        control_mode=ControlMode.POSITION,
        joint_commands=[JointTargetCommand(joint_id="j1", target_position=0.2)],
        model_confidence_score=0.72,  # < 0.95 threshold
    )

    executed_action, state = kernel.step(telemetry, uncertain_action)
    assert state == SafetyState.INTERVENTION_REQUIRED
    assert executed_action.token_id == "tok_human_guided"
    assert kernel.total_interventions == 1
    assert len(kernel.intervention_vault.recorded_trajectories) == 1


def test_financial_flywheel_trillion_dollar_threshold():
    """Verify that 10-year venture economics cross $1T implied enterprise value."""
    sim = FleetVentureSimulator()
    projection = sim.run_projection(10)

    y10 = projection[-1]
    assert y10.year == 10
    assert y10.active_robots > 15_000_000  # Multi-million global unit fleet
    assert y10.gross_revenue_b > 100.0    # > $100B revenue
    assert y10.free_cash_flow_b > 40.0    # > $40B FCF benchmark
    assert y10.implied_valuation_at_25x_b >= 1000.0  # Crosses $1 Trillion milestone
