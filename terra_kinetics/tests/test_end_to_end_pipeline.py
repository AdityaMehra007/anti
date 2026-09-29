"""
End-to-End Integration Test Suite for the Entire Terra Kinetics Substrate.
Validates Adapters, Sim-to-Real Gym, VLA Model, Marketplace, and LaaS Metering.
"""

import pytest
import time
from terra_kinetics.protocol.ukp_schema import (
    ActionTokenPacket,
    ControlMode,
    JointTargetCommand,
    RobotMorphology,
)
from terra_kinetics.adapters.ur_adapter import UniversalRobotsAdapter
from terra_kinetics.adapters.unitree_adapter import UnitreeHumanoidAdapter
from terra_kinetics.gym.domain_randomizer import DomainRandomizer
from terra_kinetics.gym.synthetic_trajectory_generator import SyntheticTrajectoryGenerator
from terra_kinetics.model.vla_policy_engine import VLAPolicyEngine
from terra_kinetics.marketplace.skill_registry import (
    PhysicalSkillPackage,
    SkillCertificationLevel,
    SkillMarketplaceRegistry,
)
from terra_kinetics.marketplace.metering_engine import LaasMeteringEngine


def test_ur_adapter_rtde_and_servoj():
    adapter = UniversalRobotsAdapter(robot_ip="192.168.1.100")
    q = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]
    qd = [0.0] * 6
    tau = [2.5] * 6
    temps = [32.0] * 6

    telemetry = adapter.parse_rtde_telemetry(q, qd, tau, temps)
    assert telemetry.robot_id == "ur_192_168_1_100"
    assert len(telemetry.joints) == 6
    assert telemetry.joints[1].position_rad == -1.57

    action = ActionTokenPacket(
        token_id="act_ur_1",
        target_timestamp_ns=time.time_ns(),
        control_mode=ControlMode.POSITION,
        joint_commands=[
            JointTargetCommand(joint_id="shoulder_pan_joint", target_position=0.25),
            JointTargetCommand(joint_id="elbow_joint", target_position=1.10),
        ],
    )
    urscript = adapter.format_urscript_servoj(action)
    assert "servoj([" in urscript
    assert "0.25000" in urscript


def test_unitree_humanoid_adapter():
    adapter = UnitreeHumanoidAdapter(robot_serial="g1_prototype_04")
    positions = [0.0] * 23
    velocities = [0.0] * 23
    torques = [10.0] * 23

    telemetry = adapter.parse_dds_states(positions, velocities, torques)
    assert telemetry.robot_id == "g1_prototype_04"
    assert telemetry.morphology == RobotMorphology.BIPEDAL_HUMANOID
    assert len(telemetry.joints) == len(adapter.HUMANOID_JOINTS)

    action = ActionTokenPacket(
        token_id="act_humanoid_1",
        target_timestamp_ns=time.time_ns(),
        control_mode=ControlMode.POSITION,
        joint_commands=[
            JointTargetCommand(joint_id="waist_yaw", target_position=0.15, feedforward_torque=3.0)
        ],
    )
    low_cmds = adapter.generate_low_cmd_packet(action)
    assert "waist_yaw" in low_cmds
    assert low_cmds["waist_yaw"]["q"] == 0.15
    assert low_cmds["waist_yaw"]["tau"] == 3.0


def test_sim_to_real_procedural_gym():
    randomizer = DomainRandomizer()
    generator = SyntheticTrajectoryGenerator(randomizer=randomizer)
    episode = generator.generate_pick_and_place_episode(num_steps=20, seed=42)

    assert len(episode) == 20
    assert episode[0].step_index == 0
    assert episode[-1].task_success is True
    assert episode[-1].reward == 1.0


def test_vla_policy_engine_ood_uncertainty_trigger():
    engine = VLAPolicyEngine()
    adapter = UniversalRobotsAdapter()
    telemetry = adapter.parse_rtde_telemetry([0.0]*6, [0.0]*6, [0.0]*6, [30.0]*6)

    # In-distribution test
    nominal_res = engine.infer(telemetry, "pick standard box", target_object_class="standard_tote")
    assert not nominal_res.is_out_of_distribution
    assert nominal_res.action_token.requires_human_verification is False

    # Out-of-distribution test (triggers tele-op)
    ood_res = engine.infer(telemetry, "grasp fragile chemical vessel", target_object_class="unknown_hazard")
    assert ood_res.is_out_of_distribution
    assert ood_res.entropy_score > 0.28
    assert ood_res.action_token.requires_human_verification is True


def test_skill_marketplace_lifecycle_and_metering():
    registry = SkillMarketplaceRegistry(platform_take_rate=0.30)
    skill = PhysicalSkillPackage(
        skill_id="skill_bin_picking_v2",
        name="Universal 3D Bin Picking",
        author="DevOrg_Automation",
        version="2.1.0",
        supported_morphologies=[RobotMorphology.MANIPULATOR_6DOF],
        certification=SkillCertificationLevel.INDUSTRIAL_ISO,
        hourly_license_fee_usd=2.50,
        per_cycle_fee_usd=0.01,
        description="High-speed bin picking for reflective automotive fasteners.",
    )
    skill.sign("test_secret")
    assert skill.verify("test_secret")
    assert registry.register_skill(skill)

    # Deployment
    deployed, msg = registry.deploy_skill_to_robot("ur_cell_1", "skill_bin_picking_v2", RobotMorphology.MANIPULATOR_6DOF)
    assert deployed

    # Metering and Invoicing
    meter = LaasMeteringEngine(base_os_hourly_rate_usd=2.00, teleop_intervention_rate_usd=0.50, pick_cycle_rate_usd=0.01)
    meter.start_session("ur_cell_1", "customer_bmw_munich")
    for _ in range(50):
        meter.record_cycle("ur_cell_1", is_intervention=False, skill_id="skill_bin_picking_v2")
    meter.record_cycle("ur_cell_1", is_intervention=True)

    invoice = meter.close_session_and_invoice("ur_cell_1", secret_key="test_secret")
    assert invoice is not None
    assert invoice.customer_id == "customer_bmw_munich"
    assert invoice.total_amount_usd > 0.0
    assert len(invoice.signature_hash) == 64
