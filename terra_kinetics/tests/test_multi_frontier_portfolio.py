"""
Multi-Frontier Portfolio Test Suite:
Validates Autonomous Agent Mesh, Aether Energy-Compute, and Bioma Foundry.
"""

import pytest
from terra_kinetics.agents.ceo_agent import AutonomousCeoAgent
from terra_kinetics.agents.gtm_agent import AutonomousGtmAgent, EnterpriseLead
from terra_kinetics.agents.field_ops_agent import AutonomousFieldOpsAgent
from terra_kinetics.agents.agent_mesh import ExecutiveAgentMesh

from aether_energy.smr_reactor_model import AetherThermalComputePlant, SMRModuleSpecification
from aether_energy.ppa_tollbooth_calculator import AetherVentureCalculator

from bioma_foundry.dna_compiler import MolecularDnaCompiler, TargetMoleculeSpec
from bioma_foundry.bioreactor_economics import BiomaEconomicEngine


def test_autonomous_agent_mesh_weekly_cycle():
    mesh = ExecutiveAgentMesh(initial_treasury_usd=35_000_000.0)
    lead = EnterpriseLead(
        company_name="BMW_Munich",
        facility_type="automotive",
        location="Munich, Germany",
        annual_workforce_headcount=400,
        avg_hourly_wage_usd=32.0,
    )
    cycle = mesh.run_weekly_corporate_cycle(
        active_fleet=1500,
        weekly_burn_usd=250_000.0,
        incoming_leads=[lead],
    )
    assert cycle["cycle_status"] == "COMPLETED_NOMINAL"
    assert cycle["active_fleet_count"] == 1500
    assert cycle["proposals_generated"] == 1
    assert cycle["top_proposal"]["annual_net_savings_usd"] > 1_000_000.0


def test_aether_smr_compute_coupling():
    plant = AetherThermalComputePlant()
    cluster = plant.calculate_cluster_capacity(num_reactors=10)
    assert cluster["num_reactors"] == 10
    assert cluster["continuous_clean_power_mwe"] > 600.0  # 65 MWe * 10 * 0.95 = 617.5 MWe
    assert cluster["collocated_ai_gpu_nodes"] > 200_000
    assert cluster["total_ai_compute_exaflops"] > 4.0


def test_aether_venture_valuation_milestone():
    calc = AetherVentureCalculator()
    trajectory = calc.project_10_year_trajectory()
    assert len(trajectory) == 10
    y10 = trajectory[-1]
    assert y10.year == 10
    assert y10.deployed_reactors == 1600
    assert y10.total_gigawatts_gw > 100.0
    assert y10.implied_valuation_at_25x_b >= 1000.0  # Crosses $1T threshold


def test_bioma_molecular_compiler():
    compiler = MolecularDnaCompiler()
    spec = TargetMoleculeSpec(
        molecule_name="Artemisinin_precursor",
        target_cas_number="63968-64-9",
        target_pathway="terpenoid_synthase",
    )
    plasmid = compiler.compile_pathway(spec)
    assert "bio_plasmid_" in plasmid.plasmid_id
    assert plasmid.target_molecule == "Artemisinin_precursor"
    assert plasmid.codon_adaptation_index >= 0.90
    assert 40.0 <= plasmid.gc_content_pct <= 60.0
    assert len(plasmid.cryptographic_checksum) == 64


def test_bioma_economic_engine_scale():
    engine = BiomaEconomicEngine()
    projections = engine.project_10_year_trajectory()
    assert len(projections) == 10
    y10 = projections[-1]
    assert y10.year == 10
    assert y10.annual_metric_tons_produced > 50_000_000.0
    assert y10.gross_margin_pct >= 65.0
    assert y10.implied_valuation_at_25x_b >= 1000.0  # Crosses $1T threshold
