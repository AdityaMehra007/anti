"""
Advanced Systems Test Suite: Teleop Gateway, Formal Safety Certifier, and Streaming Server Daemon.
"""

import pytest
import time
from terra_kinetics.protocol.ukp_schema import (
    ActionTokenPacket,
    ControlMode,
    JointTargetCommand,
    JointState,
    RobotMorphology,
    SensorTelemetryPacket,
)
from terra_kinetics.teleop.gateway import (
    ShadowTeleopGateway,
    OperatorKinematicPose,
    TeleopConnectionState,
)
from terra_kinetics.verification.formal_safety import FormalSafetyCertifier
from terra_kinetics.server.daemon import TelemetryStateStore, run_daemon


def test_shadow_teleop_gateway_flow():
    gateway = ShadowTeleopGateway(max_jitter_ms=5.0)
    granted, msg = gateway.initiate_handover("robot_alpha", "operator_neo")
    assert granted
    assert gateway.state == TeleopConnectionState.ACTIVE_CONTROL

    # Stream motion
    pose = OperatorKinematicPose(
        timestamp_ns=time.time_ns(),
        operator_id="operator_neo",
        headset_pose=(0, 0, 1.7, 1, 0, 0, 0),
        left_hand_pose=(0.2, 0.4, 1.0, 1, 0, 0, 0),
        right_hand_pose=(-0.2, 0.4, 1.0, 1, 0, 0, 0),
    )
    ok, haptic = gateway.process_kinematic_stream("robot_alpha", pose, telemetry_latency_ms=2.1)
    assert ok
    assert haptic is not None
    assert haptic.vibration_frequency_hz == 120.0

    # Archive
    gt = gateway.complete_intervention_and_archive("robot_alpha", task_success=True)
    assert gt["task_success"] is True
    assert gateway.state == TeleopConnectionState.IDLE


def test_formal_safety_certifier_iso_ple():
    certifier = FormalSafetyCertifier()
    telemetry = SensorTelemetryPacket(
        robot_id="r1",
        morphology=RobotMorphology.MANIPULATOR_6DOF,
        timestamp_ns=time.time_ns(),
        joints=[JointState(joint_id="j1", position_rad=0.0, velocity_rad_s=0.0, effort_nm=5.0, temperature_c=30.0)],
    )
    action = ActionTokenPacket(
        token_id="act_safe_1",
        target_timestamp_ns=time.time_ns(),
        control_mode=ControlMode.POSITION,
        joint_commands=[JointTargetCommand(joint_id="j1", target_position=0.1, feedforward_torque=10.0)],
        model_confidence_score=0.99,
    )

    cert = certifier.certify_step(telemetry, action, obstacle_distance_m=0.8)
    assert cert.is_provably_safe is True
    assert cert.iso_performance_level == "PL e (Category 4)"
    assert cert.underwriting_risk_score < 0.10


def test_formal_safety_certifier_breach():
    certifier = FormalSafetyCertifier()
    telemetry = SensorTelemetryPacket(
        robot_id="r1",
        morphology=RobotMorphology.MANIPULATOR_6DOF,
        timestamp_ns=time.time_ns(),
        joints=[JointState(joint_id="j1", position_rad=0.0, velocity_rad_s=0.0, effort_nm=5.0, temperature_c=30.0)],
    )
    # Low confidence action near obstacle
    unsafe_action = ActionTokenPacket(
        token_id="act_unsafe",
        target_timestamp_ns=time.time_ns(),
        control_mode=ControlMode.POSITION,
        joint_commands=[JointTargetCommand(joint_id="j1", target_position=0.1, feedforward_torque=10.0)],
        model_confidence_score=0.70,  # Below threshold
    )

    cert = certifier.certify_step(telemetry, unsafe_action, obstacle_distance_m=0.10)  # Breaches 20cm barrier
    assert cert.is_provably_safe is False
    assert cert.iso_performance_level == "UNRATED / HAZARDOUS"
    assert cert.underwriting_risk_score > 0.50


def test_telemetry_state_store_simulation():
    store = TelemetryStateStore()
    store.tick()
    snap1 = store.get_snapshot()
    assert snap1["step_count"] == 1
    assert snap1["kernel_state"] == "NOMINAL"

    incident = store.trigger_hazard()
    snap2 = store.get_snapshot()
    assert snap2["kernel_state"] == "INTERVENTION_REQUIRED"
    assert snap2["interventions_total"] == 1

    store.reset_nominal()
    assert store.get_snapshot()["kernel_state"] == "NOMINAL"


def test_daemon_api_atlas_endpoint():
    import urllib.request
    import json
    import threading

    server = run_daemon("127.0.0.1", 8099)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    time.sleep(0.1)

    try:
        with urllib.request.urlopen("http://127.0.0.1:8099/api/atlas") as response:
            assert response.status == 200
            data = json.loads(response.read().decode("utf-8"))
            assert data["total_nominal_gdp_t"] == 108.5
            assert data["total_debt_t"] == 315.0
            assert len(data["top_economies"]) == 10
            assert data["top_economies"][0]["name"] == "United States"
    finally:
        server.shutdown()
        server.server_close()


def test_daemon_api_empire_and_skills_endpoints():
    import urllib.request
    import json
    import threading

    server = run_daemon("127.0.0.1", 8098)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    time.sleep(0.1)

    try:
        with urllib.request.urlopen("http://127.0.0.1:8098/api/empire") as response:
            assert response.status == 200
            data = json.loads(response.read().decode("utf-8"))
            assert "consolidated_market_cap_t" in data
            assert data["shield_status"] == "PERMITTED"

        with urllib.request.urlopen("http://127.0.0.1:8098/api/skills") as response:
            assert response.status == 200
            data = json.loads(response.read().decode("utf-8"))
            assert data["total_skills"] == 10
            assert all(s["verified"] is True for s in data["skills"])

        with urllib.request.urlopen("http://127.0.0.1:8098/api/banking") as response:
            assert response.status == 200
            data = json.loads(response.read().decode("utf-8"))
            assert data["bic_code"] == "CONTUS33XXX"
            assert len(data["divisions_active"]) == 10
    finally:
        server.shutdown()
        server.server_close()


