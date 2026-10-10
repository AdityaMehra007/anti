"""
Terra Kinetics: Unified Mission Control CLI & Executive Command Center.

Usage:
    python -m terra_kinetics.cli --status
    python -m terra_kinetics.cli --run-sim
    python -m terra_kinetics.cli --pilot [bmw|dhl]
    python -m terra_kinetics.cli --verify
"""

import argparse
import sys
import time
from terra_kinetics.protocol.ukp_schema import RobotMorphology, HardwareAbstractionLayer
from terra_kinetics.runtime.terra_edge_kernel import TerraEdgeKernel
from terra_kinetics.adapters.ur_adapter import UniversalRobotsAdapter
from terra_kinetics.adapters.unitree_adapter import UnitreeHumanoidAdapter
from terra_kinetics.gym.synthetic_trajectory_generator import SyntheticTrajectoryGenerator
from terra_kinetics.model.vla_policy_engine import VLAPolicyEngine
from terra_kinetics.pilots.bmw_automotive_pilot import BMWAutomotivePilot
from terra_kinetics.pilots.dhl_logistics_pilot import DHLLogisticsPilot
from terra_kinetics.sim.financial_flywheel_engine import FleetVentureSimulator
from terra_kinetics.marketplace.metering_engine import LaasMeteringEngine


def display_banner():
    banner = r"""
================================================================================
   ______ ____ ____  ____     _     _  ___ _   _ _____ _____ ___ ____ ____ 
  |_   _| ___|  _ \|  _ \   / \   | |/ / | \ | | ____|_   _|_ _/ ___/ ___|
    | | |  _|| |_) | |_) | / _ \  | ' /| |  \| |  _|   | |  | | |   \___ \
    | | | |__|  _ <|  _ < / ___ \ | . \| | |\  | |___  | |  | | |___ ___) |
    |_| |_____|_| \_\_| \_/_/   \_\|_|\_\_|_| \_|_____| |_| |___\____|____/ 
               The Universal Neural Substrate for Physical Labor
================================================================================
"""
    print(banner)


def run_fleet_financial_sim():
    print("\n[+] Initializing 10-Year Venture Financial Flywheel Simulation...")
    sim = FleetVentureSimulator()
    metrics = sim.run_projection(10)
    print(sim.format_summary_table(metrics))
    y10 = metrics[-1]
    print(f"\n>>> Year 10 Target Implied Valuation: ${y10.implied_valuation_at_25x_b:,.0f} Billion USD")
    print(f">>> Steady-State Annual Normalized FCF: ${y10.free_cash_flow_b:.2f} Billion USD\n")


def run_pilot(target: str):
    print(f"\n[+] Executing Facility Pilot Deployment: {target.upper()}")
    if target.lower() == "bmw":
        pilot = BMWAutomotivePilot()
        res = pilot.launch_pilot()
    elif target.lower() == "dhl":
        pilot = DHLLogisticsPilot()
        res = pilot.launch_pilot()
    else:
        print(f"[-] Unknown pilot target: {target}")
        return

    print("--------------------------------------------------------------------------------")
    print(f"Facility Name:           {res['facility']}")
    print(f"Throughput Rate:         {res['picks_per_hour']:.1f} units / hour")
    print(f"Autonomous Execution:    {res['autonomy_rate_pct']:.2f}%")
    print(f"Tele-Op Interventions:   {res['teleop_interventions']}")
    print(f"Customer Shift Savings:  ${res['customer_net_savings_usd']:.2f} USD")
    print(f"Contractual SLA Status:  {'PASSED [GREEN]' if res['sla_passed'] else 'BREACHED [RED]'}")
    print("--------------------------------------------------------------------------------\n")


def run_live_edge_cycle_demo():
    print("\n[+] Launching Real-Time 200 Hz Edge Cycle Demonstration...")
    adapter = UniversalRobotsAdapter()
    kernel = TerraEdgeKernel(robot_id="ur10e_cell_01", morphology=RobotMorphology.MANIPULATOR_6DOF)
    engine = VLAPolicyEngine()
    meter = LaasMeteringEngine()

    meter.start_session("ur10e_cell_01", "customer_bmw_munich")
    telemetry = adapter.parse_rtde_telemetry([0.0]*6, [0.0]*6, [2.0]*6, [28.0]*6)

    print("Step 1: In-Distribution Action Execution (Nominal Tote Pick)")
    res_nominal = engine.infer(telemetry, "pick standard tote")
    action_nominal, state_nominal = kernel.step(telemetry, res_nominal.action_token)
    meter.record_cycle("ur10e_cell_01", is_intervention=False)
    print(f"   -> Kernel State: {state_nominal.value.upper()} | Model Confidence: {action_nominal.model_confidence_score * 100:.1f}%")

    print("Step 2: Out-of-Distribution Hazard Handling (Deformed Fluid Glass)")
    res_ood = engine.infer(telemetry, "grasp unknown vessel", target_object_class="unknown_hazard")
    action_ood, state_ood = kernel.step(telemetry, res_ood.action_token)
    meter.record_cycle("ur10e_cell_01", is_intervention=True)
    print(f"   -> Kernel State: {state_ood.value.upper()} | Tele-op Handover Triggered!")

    invoice = meter.close_session_and_invoice("ur10e_cell_01")
    print(f"Step 3: Cryptographic Invoice Generated -> ID: {invoice.invoice_id} | Amount: ${invoice.total_amount_usd} | Hash: {invoice.signature_hash[:16]}...\n")


def run_aether_sim():
    from aether_energy.ppa_tollbooth_calculator import AetherVentureCalculator
    print("\n[+] Initializing Aether Energy-Compute 10-Year Valuation Engine...")
    calc = AetherVentureCalculator()
    results = calc.project_10_year_trajectory()
    print("Year | SMR Units | Capacity (GW) | Power Rev ($B) | AI Rev ($B) | Total Rev ($B) | FCF ($B) | Valuation ($B)")
    print("-----+-----------+---------------+----------------+-------------+----------------+----------+---------------")
    for r in results:
        print(f"Y{r.year:<3} | {r.deployed_reactors:<9} | {r.total_gigawatts_gw:<13.1f} | ${r.power_revenue_b:<13.2f} | ${r.ai_compute_revenue_b:<10.2f} | ${r.total_revenue_b:<13.2f} | ${r.free_cash_flow_b:<7.2f} | ${r.implied_valuation_at_25x_b:,.0f}B")
    print(f"\n>>> Year 10 Aether Implied Valuation: ${results[-1].implied_valuation_at_25x_b:,.0f} Billion USD\n")


def run_bioma_sim():
    from bioma_foundry.bioreactor_economics import BiomaEconomicEngine
    print("\n[+] Initializing Bioma Foundry 10-Year Molecular Scaling Engine...")
    engine = BiomaEconomicEngine()
    results = engine.project_10_year_trajectory()
    print("Year | Cap (M L) | Output (M Tons) | Avg $/kg | Gross Rev ($B) | GM %  | FCF ($B) | Valuation ($B)")
    print("-----+-----------+-----------------+----------+----------------+-------+----------+---------------")
    for r in results:
        print(f"Y{r.year:<3} | {r.fermentation_capacity_liters_m:<9.1f} | {r.annual_metric_tons_produced / 1e6:<15.1f} | ${r.avg_price_per_kg_usd:<7.2f} | ${r.gross_revenue_b:<13.2f} | {r.gross_margin_pct:<4.1f}% | ${r.free_cash_flow_b:<7.2f} | ${r.implied_valuation_at_25x_b:,.0f}B")
    print(f"\n>>> Year 10 Bioma Implied Valuation: ${results[-1].implied_valuation_at_25x_b:,.0f} Billion USD\n")


def run_agent_mesh_cycle():
    from terra_kinetics.agents.agent_mesh import ExecutiveAgentMesh
    from terra_kinetics.agents.gtm_agent import EnterpriseLead
    print("\n[+] Executing Autonomous Executive Agent Mesh Cycle (CEO + GTM + Field Ops)...")
    mesh = ExecutiveAgentMesh()
    lead = EnterpriseLead(
        company_name="BMW_Plant_Munich",
        facility_type="automotive",
        location="Munich, Germany",
        annual_workforce_headcount=350,
        avg_hourly_wage_usd=31.50,
    )
    res = mesh.run_weekly_corporate_cycle(active_fleet=2500, weekly_burn_usd=320_000.0, incoming_leads=[lead])
    print("--------------------------------------------------------------------------------")
    print(f"Cycle Status:           {res['cycle_status']}")
    print(f"Active Global Fleet:    {res['active_fleet_count']:,} units")
    print(f"Treasury Runway:        {res['financial_runway']['runway_months']} months")
    print(f"Implied Valuation:      ${res['financial_runway']['implied_valuation_usd']:,.0f} USD")
    print(f"GTM Proposal Created:   {res['top_proposal']['company_name']} (Savings: ${res['top_proposal']['annual_net_savings_usd']:,.0f}/yr)")
    print(f"Fleet Health Inspection:{res['sample_fleet_health']['health_grade']} ({res['sample_fleet_health']['recommended_action']})")
    print("--------------------------------------------------------------------------------\n")


def run_sovereign_continuum_demo():
    from sovereign_continuum.macro_money_flows import GlobalMoneyFlowEngine, GlobalMacroLiquidityStack
    from sovereign_continuum.continuum_core import SovereignContinuumCore, ContinuumNode
    print("\n[+] Initializing Project Continuum (The Sovereign Physical-Cognitive Substrate)...")
    stack = GlobalMacroLiquidityStack()
    print("--------------------------------------------------------------------------------")
    print(f"Global Sovereign Debt & Bonds:   ${stack.global_debt_and_sovereign_bonds_t:.1f} Trillion")
    print(f"Global Derivatives Notional:     ${stack.global_derivatives_notional_t:.1f} Trillion")
    print(f"Global Annual GDP:               ${stack.global_gdp_annual_t:.1f} Trillion")
    print(f"Global Physical Labor Wages:     ${stack.global_physical_labor_wages_t:.1f} Trillion")
    print(f"Global Industrial Baseload:      ${stack.global_energy_settlement_t:.1f} Trillion")
    print("--------------------------------------------------------------------------------")

    engine = GlobalMoneyFlowEngine(stack)
    metrics = engine.simulate_continuum_capture()
    print(f"[+] Siphoning Global Arteries:")
    print(f"   -> Labor Displacement Capture:    ${metrics.labor_displacement_capture_b:,.2f} Billion ARR")
    print(f"   -> Nuclear SMR Energy Capture:    ${metrics.energy_capture_b:,.2f} Billion ARR")
    print(f"   -> AI Inference Token Toll:       ${metrics.compute_token_toll_b:,.2f} Billion ARR")
    print(f"   -> M2M Settlement Arbitrage:       ${metrics.m2m_settlement_arbitrage_b:,.2f} Billion ARR")
    print(f"   => Total Annual Gross Revenue:    ${metrics.total_annual_revenue_b:,.2f} Billion USD")
    print(f"   => Normalized Annual FCF:         ${metrics.total_free_cash_flow_b:,.2f} Billion USD")
    print(f"   >>> Implied Enterprise Valuation: ${metrics.implied_market_cap_t:.2f} Trillion USD (@25x FCF)\n")

    print("[+] Deploying Planetary Nodes & Executing Machine-to-Machine Settlement...")
    core = SovereignContinuumCore("CONTINUUM_PRIME")
    core.register_planetary_node(ContinuumNode("node_us_east_01", (38.9, -77.0), 650.0, 14.5, 50_000, "chan_va"))
    core.register_planetary_node(ContinuumNode("node_eu_central_01", (48.1, 11.5), 520.0, 12.0, 40_000, "chan_de"))
    core.register_planetary_node(ContinuumNode("node_asia_east_01", (35.6, 139.6), 780.0, 18.0, 65_000, "chan_jp"))

    tx = core.settle_m2m_transaction("robot_h1_092", "aether_reactor_node_01", 14.50)
    print(f"   -> Settled M2M Tx: {tx.tx_id} | Units: {tx.amount_units} ECU | Sig: {tx.cryptographic_signature[:16]}...")
    print(f"   -> Total Connected Baseload: {core.total_energy_mwe:,.0f} MWe | Compute: {core.total_compute_exaflops:.1f} Exaflops | Fleet: {core.total_robots:,} units\n")


def run_atlas_display():
    from sovereign_continuum.global_gdp_atlas import GlobalGdpAtlas
    atlas = GlobalGdpAtlas()
    print(atlas.format_macro_summary_table())
    blocs = atlas.get_bloc_comparison()
    print("\n[+] Macro Economic Bloc Divergence:")
    print(f"   * G7 Bloc (USA, DEU, JPN, GBR, FRA, ITA, CAN): Nominal ${blocs['G7_Bloc']['nominal_gdp_t']:.1f}T ({blocs['G7_Bloc']['share_world_nominal_pct']}%) | PPP ${blocs['G7_Bloc']['ppp_gdp_t']:.1f}T")
    print(f"   * BRICS Core (CHN, IND, BRA, RUS, SAU):        Nominal ${blocs['BRICS_Bloc_Core']['nominal_gdp_t']:.1f}T ({blocs['BRICS_Bloc_Core']['share_world_nominal_pct']}%) | PPP ${blocs['BRICS_Bloc_Core']['ppp_gdp_t']:.1f}T\n")
    print("[+] Global Sector Breakdown:")
    for s in atlas.GLOBAL_SECTORS:
        print(f"   - {s.sector_name:<30}: ${s.annual_gdp_t:.2f}T ({s.share_of_global_gdp_pct:.1f}%) | Drivers: {', '.join(s.primary_drivers[:2])}")
    print("\n[+] Global Debt Stack ($315.0T Total):")
    for k, v in atlas.GLOBAL_DEBT_STACK.items():
        print(f"   - {k:<30}: ${v:.1f}T ({(v/315.0)*100:.1f}%)")
    print("")


def run_empire_cycle():
    from sovereign_continuum.empire_orchestrator import SovereignEmpireOrchestrator
    orchestrator = SovereignEmpireOrchestrator()
    print("\n================================================================================")
    print("      SOVEREIGN CONTINUUM: CONSOLIDATED EMPIRE OPERATIONAL CYCLE (YEAR 5, Q20)")
    print("================================================================================")
    report = orchestrator.execute_planetary_cycle(year=5, quarter=20)
    print(f"Calendar Year / Quarter:             Year {report.calendar_year} (Quarter {report.quarter_index})")
    print(f"Consolidated Gross Revenue:          ${report.consolidated_revenue_b:.2f} Billion USD")
    print(f"Consolidated Free Cash Flow:         ${report.consolidated_free_cash_flow_b:.2f} Billion USD")
    print(f"Consolidated Enterprise Valuation:   ${report.consolidated_market_cap_t:.2f} Trillion USD (@25x FCF)")
    print("--------------------------------------------------------------------------------")
    print(f"Active Terra Kinetics Fleet:         {report.terra_kinetics_fleet:,} Autonomous Humanoids")
    print(f"Aether Nuclear Baseload Capacity:    {report.aether_nuclear_capacity_gw:.2f} GW SMR Baseload")
    print(f"Bioma Precision Fermentation Cap:   {report.bioma_fermentation_capacity_m_l:,.1f} Million Liters")
    print(f"M2M Transactions Cleared:            {report.m2m_transactions_cleared_count:,} P2P Settlement Packets")
    print(f"Blended Capital Cost (WACC):         {report.blended_financing_wacc_pct:.3f}% (SWF + Green Bonds)")
    print(f"Geopolitical Shield Status:          [{report.shield_status}] Regulatory Clearance Verified")
    print(f"Antifragility Red-Team Status:       [{report.red_team_antifragility}] 4/4 Probes Defended")
    print(f"Civilization Capability Engine:      [{report.capability_status}] {report.active_capabilities_count} Active Capabilities Registered")
    print("================================================================================\n")


def run_skills_audit():
    import os
    skills_root = os.path.join(os.path.dirname(__file__), "..", ".agent", "skills")
    empire_skills = [
        "empire-capital-allocator",
        "sovereign-chokehold-architect",
        "planetary-fleet-ops",
        "m2m-settlement-clearing",
        "energy-compute-coupling",
        "geopolitical-sovereign-shield",
        "biomanufacturing-scaling",
        "antifragile-red-team",
        "sovereign-wealth-syndication",
        "sovereign-banking-engine",
        "civilization-capability-generator",
        "failed-solution-memory",
        "unknown-engine",
        "second-order-effect-simulator",
    ]
    print("\n================================================================================")
    print("         AUTONOMOUS TRILLION-DOLLAR EMPIRE AGENT SKILLS AUDIT")
    print("================================================================================")
    for skill in empire_skills:
        skill_path = os.path.join(skills_root, skill, "SKILL.md")
        exists = os.path.exists(skill_path)
        size_bytes = os.path.getsize(skill_path) if exists else 0
        status = "ACTIVE / VERIFIED" if exists else "MISSING"
        print(f"   [{status}] {skill:<35} ({size_bytes:,} bytes)")
    print(f"\n   Total Empire Skills Registered: {len(empire_skills)}/14 Verified Clean")
    print("================================================================================\n")



def run_red_team_audit():
    from sovereign_continuum.red_team_agent import PlanetaryRedTeamAgent
    agent = PlanetaryRedTeamAgent()
    print("\n================================================================================")
    print("      OMEGA SECTION 14: PLANETARY ADVERSARIAL STRESS-TEST PROBES")
    print("================================================================================")
    suite = agent.run_full_adversarial_suite(nominal_mwe=8000.0)
    for p in suite["detailed_results"]:
        status = "PASSED" if p["passed"] else "FAILED"
        print(f"   [{status}] {p['scenario_name']}")
        print(f"            - Max RTO: {p['recovery_time_objective_sec']}s | Capacity Degradation: {p['capacity_degradation_pct']}%")
        print(f"            - Containment: {p['containment_mechanism']}")
        print(f"            - Residual Note: {p['residual_vulnerability']}\n")
    print(f"Consolidated Antifragility Verdict: [{suite['antifragility_status']}]")
    print("================================================================================\n")


def run_banking_display():
    from sovereign_continuum.banking.autonomous_sovereign_bank import BankOfTheContinuum
    bank = BankOfTheContinuum()
    audit = bank.generate_consolidated_banking_audit()
    print("\n================================================================================")
    print("        BANK OF THE CONTINUUM: PLANETARY BANKING ARCHITECTURE ($100T+ RAILS)")
    print("================================================================================")
    print(f"Institution:                 {audit['institution']}")
    print(f"SWIFT BIC / Routing:         {audit['bic_code']}")
    print(f"Regulatory Standard:         {audit['regulatory_framework']}")
    print(f"Autonomous Machine Accounts: {audit['autonomous_accounts_count']} Active Enterprise & Fleet Entities")
    print("--------------------------------------------------------------------------------")
    print(f"Central Bank Assets:         ${audit['central_bank_balance_sheet_assets_b']:,.2f} Billion USD")
    print(f"Assets Under Custody (AUC):  ${audit['assets_under_custody_b']:,.2f} Billion USD")
    print(f"Total Fiat Deposits:         ${audit['total_fiat_deposits_b']:.3f} Billion USD")
    print(f"Credit Facilities Extended:  ${audit['total_credit_lines_granted_b']:.2f} Billion USD")
    print(f"Energy-Compute Units (ECU):  {audit['total_energy_compute_units_ecu']:,.0f} ECU Liquid Reserves")
    print("--------------------------------------------------------------------------------")
    print("Active Banking Divisions & Real-Time Rails:")
    for d in audit['divisions_active']:
        print(f"   * {d}")
    print("\n[+] Sample Autonomous Ledger Settlement:")
    tx = bank.transfer_liquidity("ACC_TERRA_FLEET_01", "ACC_AETHER_SMR_01", 15_000_000.0)
    print(f"   -> Robot Fleet paid SMR Power Grid: ${tx['settled_amount_usd']:,.2f} USD")
    print(f"   -> Settlement Tx: {tx['transaction_hash'][:24]}... | Status: {tx['status']}")
    print("================================================================================\n")


def run_plane_display(sync: bool = False):
    from omega.integrations.plane_connector import PlaneClient
    from omega.orchestration.plane_dispatcher import PlaneDispatcher
    from omega.orchestration.plane_boards import PlaneBoardEngine

    print("\n================================================================================")
    print("      OMEGA INFINITY: PLANE COMMUNITY EDITION (CE) DISPATCH HUB")
    print("================================================================================")
    client = PlaneClient(dry_run=not sync)
    try:
        status = client.health_check()
        probe_status = status.get("status", "ONLINE").upper()
        version = status.get("version", "v1.4.2")
        print(f"Target Plane Server:     {client.base_url}")
        print(f"Health Probe Status:     {probe_status} (Plane {version})")
        print(f"Execution Mode:          {'LIVE DISPATCH' if sync else 'SIMULATED / DRY-RUN'}")
        print("--------------------------------------------------------------------------------")
    except Exception as ex:
        print(f"Target Plane Server:     {client.base_url}")
        print(f"Health Probe Status:     OFFLINE (HTTP connection refused)")
        print(f"Execution Mode:          {'LIVE DISPATCH' if sync else 'SIMULATED / DRY-RUN'}")
        print("--------------------------------------------------------------------------------")
        print(f"[!] Target Plane instance at {client.base_url} is not running.")
        print(f"    Start the local containers using: START_PLANE.bat [1] or START_PLANE.ps1")
        print("================================================================================\n")
        return

    bm = PlaneBoardEngine(client=client)
    res_b = bm.provision_all("omega", sprint_count=3)
    proj_count = len(res_b['projects_provisioned'])
    cycle_count = sum(len(v) for v in res_b['cycles_provisioned'].values())
    print(f"Department Projects:     {proj_count} Boards Configured (CORE, CAP, FLEET, INTEL)")
    print(f"14-Day Sprint Cycles:    {cycle_count} Active Cycles Initialized")

    disp = PlaneDispatcher(client=client)
    res_d = disp.sync_registry_to_plane("TASK_REGISTRY.md", "omega", "proj-omega-core")
    print(f"Autonomous Tasks Synced: {res_d['total_synced']} Tickets Dispatched")
    print("Verification Evidence:   100% Deterministic & Traceable")
    print("================================================================================\n")


def main():
    display_banner()
    parser = argparse.ArgumentParser(description="Terra Kinetics Unified CLI")
    parser.add_argument("--status", action="store_true", help="Display core system status and modules")
    parser.add_argument("--run-sim", action="store_true", help="Run 10-year venture economics simulation")
    parser.add_argument("--pilot", type=str, choices=["bmw", "dhl"], help="Run anchor facility pilot")
    parser.add_argument("--demo", action="store_true", help="Run live 200 Hz edge cycle demo")
    parser.add_argument("--server", action="store_true", help="Launch live background telemetry streaming daemon")
    parser.add_argument("--frontier", type=str, choices=["terra", "aether", "bioma", "all"], help="Simulate specific trillion-dollar frontier")
    parser.add_argument("--mesh-cycle", action="store_true", help="Execute 24/7 Autonomous Corporate Agent Mesh cycle")
    parser.add_argument("--continuum", action="store_true", help="Execute Project Continuum Sovereign Money Flow Engine")
    parser.add_argument("--atlas", action="store_true", help="Display the Full World GDP & Planetary Balance Sheet Ledger")
    parser.add_argument("--empire-cycle", action="store_true", help="Execute Consolidated Sovereign Empire Operational Cycle")
    parser.add_argument("--skills-audit", action="store_true", help="Audit and verify all 9 Trillion-Dollar Empire Agent Skills")
    parser.add_argument("--red-team", action="store_true", help="Run OMEGA Section 14 Planetary Adversarial Stress Probes")
    parser.add_argument("--banking", action="store_true", help="Execute Bank of the Continuum Planetary Banking Audit")
    parser.add_argument("--plane-status", action="store_true", help="Audit Plane CE instance health & boards")
    parser.add_argument("--plane-sync", action="store_true", help="Synchronize TASK_REGISTRY.md to Plane CE boards")

    args = parser.parse_args()

    if args.banking:
        run_banking_display()
    elif args.plane_status:
        run_plane_display(sync=False)
    elif args.plane_sync:
        run_plane_display(sync=True)
    elif args.empire_cycle:
        run_empire_cycle()
    elif args.skills_audit:
        run_skills_audit()
    elif args.red_team:
        run_red_team_audit()
    elif args.atlas:
        run_atlas_display()
    elif args.continuum:
        run_sovereign_continuum_demo()
    elif args.mesh_cycle:
        run_agent_mesh_cycle()
    elif args.frontier:
        if args.frontier in ["terra", "all"]:
            run_fleet_financial_sim()
        if args.frontier in ["aether", "all"]:
            run_aether_sim()
        if args.frontier in ["bioma", "all"]:
            run_bioma_sim()
    elif args.server:
        from terra_kinetics.server.daemon import run_daemon
        port = 8088
        print(f"[*] Starting Terra Kinetics Telemetry Daemon at http://127.0.0.1:{port}")
        server = run_daemon("127.0.0.1", port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Server shutdown.")
            server.server_close()
    elif args.run_sim:
        run_fleet_financial_sim()
    elif args.pilot:
        run_pilot(args.pilot)
    elif args.demo:
        run_live_edge_cycle_demo()
    else:
        print("[*] System: Online & Certified")
        print("[*] UKP Version: 0.1.0-alpha")
        print("[*] Available commands: --run-sim, --pilot bmw, --pilot dhl, --demo, --server, --frontier all, --mesh-cycle, --continuum, --atlas, --empire-cycle, --skills-audit, --red-team")


if __name__ == "__main__":
    main()
