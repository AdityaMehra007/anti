"""
OMEGA INFINITY (Ω-OS) — FOUNDER SOVEREIGN TERMINAL CLI
Command-line interface for the autonomous enterprise holding system.
Enforces OMEGA_CONSTITUTION.md & ADI_OMNI_CODEX.md.
"""

import os
import sys
import json
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import get_kernel, CONSTITUTIONAL_MODES
from omega_infinity.omega_vectis_adapter import VectisEnterpriseAdapter
from omega_infinity.omega_intel_engine import IntelSearchEngine
from omega_infinity.omega_swarm_matrix import SwarmMatrix
from omega_infinity.omega_all_agents import get_fleet
from omega_infinity.omega_temporal_learner import TemporalLearningEngine
from omega_infinity.omega_infinity_server import run_server
from omega_infinity.omega_enterprise_erp import get_erp
from omega_infinity.omega_hyper_orchestrator import get_orchestrator
from omega_infinity.omega_red_team_engine import get_red_team
from omega_infinity.omega_valuation_compounding import get_valuation_engine
from omega_infinity.omega_trillion_dollar_engine import get_trillion_engine
from omega_infinity.omega_planetary_gdp_asi_engine import get_planetary_gdp_asi_engine
from omega_infinity.omega_workflow_engine import get_workflow_engine


def cmd_status(args):
    kernel = get_kernel()
    summary = kernel.get_summary()
    print("=" * 68)
    print("  OMEGA INFINITY (Ω-OS) — SOVEREIGN ENTERPRISE STATUS")
    print("=" * 68)
    print(f"Holding Entity    : {summary['holding']}")
    print(f"Primary Operating : {summary['primary_entity']}")
    print(f"Founder / Location: {summary['founder']} | Bengaluru, India")
    print(f"Active Mode       : Mode {summary['active_mode']['code']} ({summary['active_mode']['name']})")
    print(f"Mode Focus        : {summary['active_mode']['desc']}")
    print("-" * 68)
    print(f"Capital Reserves  : ₹{summary['financials']['capital_reserves_inr']:,.2f}")
    print(f"Monthly Burn Rate : ₹{summary['financials']['monthly_burn_inr']:,.2f}")
    print(f"Operational Runway: {summary['financials']['runway_months']:.1f} months")
    print(f"DPIIT Recognition : {summary['financials']['dpiit_status']}")
    print("-" * 68)
    print("TELEMETRY:")
    for k, v in summary['telemetry'].items():
        print(f"  • {k.replace('_', ' ').title():<28}: {v}")
    print("-" * 68)
    v_stat = summary['ledger_status']
    print(f"Cryptographic Ledger: {'VALID' if v_stat['valid'] else 'INVALID'} ({v_stat.get('total_blocks', 0)} blocks)")
    print("=" * 68)


def cmd_mode(args):
    kernel = get_kernel()
    try:
        res = kernel.set_mode(args.mode_code)
        print(f"[SUCCESS] Activated Mode {res['mode']} ({res['name']})")
        print(f"Directive Focus: {res['description']}")
    except Exception as e:
        print(f"[ERROR] Failed to switch mode: {e}")


def cmd_swarm(args):
    matrix = SwarmMatrix()
    print("[SWARM] Initializing 12-department sovereign swarm cycle...")
    res = matrix.run_full_swarm_cycle()
    print(f"[SUCCESS] Cycle {res['cycle_id']} finished in {res['elapsed_seconds']}s.")
    print(f"Departments synchronized: {res['agents_executed']} / 12 optimal.")


def cmd_fleet(args):
    fleet = get_fleet()
    print("[FLEET] Initializing 24-agent sovereign autonomous fleet cycle...")
    res = fleet.run_full_fleet_cycle()
    print(f"[SUCCESS] Cycle {res['cycle_id']} finished across {res['agents_executed']} agents in {res['elapsed_seconds']}s.")
    print("=" * 72)
    print("  24-AGENT SOVEREIGN FLEET EXECUTION REPORT")
    print("=" * 72)
    divisions = fleet.get_divisions()
    for div_name, agents in divisions.items():
        print(f"\n▼ DIVISION: {div_name.upper()}")
        for a in agents:
            cap = a.get("specialized_capability", a["focus"][:50])
            status = a.get("status", "OPTIMAL")
            print(f"  • [{a['id'].upper():<10}] {a['name']:<24} [{status}]")
            print(f"    Capability: {cap}")
            if a.get("kpi_metrics"):
                kpis = ", ".join(f"{k}: {v}" for k, v in a["kpi_metrics"].items())
                print(f"    KPIs      : {kpis}")
    print("=" * 72)


def cmd_temporal(args):
    learner = TemporalLearningEngine()
    learner.learn_and_synthesize()
    year = args.year or "2027"
    h = learner.get_horizon(year)
    print("=" * 68)
    print(f"  OMEGA INFINITY — TEMPORAL INTELLIGENCE VECTOR ({year})")
    print("=" * 68)
    if h:
        print(f"Theme             : {h.get('theme')}")
        print(f"Target ARR        : ₹{h.get('target_arr_inr', 0):,.2f}")
        print(f"Customer Base     : {h.get('customers')} enterprises")
        print("Capabilities      :")
        for c in h.get("capabilities", []):
            print(f"  • {c}")
    else:
        print(f"Available Horizons: {list(learner.matrix.get('future_horizons', {}).keys())}")
    print("=" * 68)


def cmd_intel(args):
    engine = IntelSearchEngine()
    q = args.query
    print(f"[INTEL] Querying intelligence across 4.5k targets & 9.2k network for '{q}'...")
    comps = engine.search_companies(q, limit=5)
    conns = engine.search_network(q, limit=5)
    leads = engine.search_trade_leads(q, limit=5)

    print(f"\n--- Target Companies (Found {len(comps)}) ---")
    for c in comps:
        print(f"  • {c['name']} | Sector: {c['sector']} | Hub: {c['location']}")

    print(f"\n--- Network Connections (Found {len(conns)}) ---")
    for n in conns:
        print(f"  • {n['name']} | {n['company']} — {n['position']}")

    print(f"\n--- Mined Trade Leads (Found {len(leads)}) ---")
    for l in leads:
        print(f"  • {l.get('name') or l.get('contact')} | {l.get('company')} — {l.get('position') or l.get('role')}")


def cmd_trade_audit(args):
    adapter = VectisEnterpriseAdapter()
    if not os.path.exists(args.file_path):
        print(f"[ERROR] File not found: {args.file_path}")
        return
    with open(args.file_path, "r", encoding="utf-8") as f:
        docket = json.load(f)
    print(f"[VECTIS] Auditing trade docket '{args.file_path}' under ICC UCP 600 / ISBP 745...")
    res = adapter.audit_docket(docket)
    if not res.get("success"):
        print(f"[ERROR] Audit failed: {res.get('error')}")
        return

    if res["passed"]:
        print(f"🟢 [PASSED] 0 Fatal Discrepancies. Ready for bank presentation.")
        print(f"SHA-256 Audit Seal: {res['certificate_seal']}")
    else:
        print(f"🔴 [REJECT] {res['discrepancy_count']} Discrepancies Found:")
        for d in res["discrepancies"]:
            print(f"  • [{d['severity']}] {d['code']} ({d['rule']}): {d['description']}")
            print(f"    Remediation: {d['remediation']}")


def cmd_ledger_verify(args):
    kernel = get_kernel()
    print("[LEDGER] Verifying SHA-256 cryptographic chain integrity...")
    res = kernel.ledger.verify_integrity()
    if res["valid"]:
        print(f"✅ Cryptographic Integrity Confirmed!")
        print(f"Total Blocks   : {res['total_blocks']}")
        print(f"Genesis Hash   : {res['genesis_hash']}")
        print(f"Latest Block   : {res['latest_block_hash']}")
    else:
        print(f"❌ INTEGRITY VIOLATION: {res['reason']}")


def cmd_finance(args):
    erp = get_erp()
    fin = erp.generate_financial_statement()
    print("=" * 70)
    print(f"  OMEGA INFINITY — MNC ENTERPRISE P&L & BALANCE SHEET")
    print(f"  Period: {fin.reporting_period} | Standard: Ind AS / GAAP")
    print("=" * 70)
    print(f"Gross Revenue (Annualized): ₹{fin.total_gross_revenue_inr:,.2f}")
    print(f"  • SaaS Software ARR     : ₹{fin.gross_saas_revenue_inr:,.2f}")
    print(f"  • Trade Auditing Fees   : ₹{fin.audit_transaction_fees_inr:,.2f}")
    print(f"  • EU CBAM Advisory      : ₹{fin.cbam_consulting_revenue_inr:,.2f}")
    print(f"Cost of Goods Sold (COGS) : ₹{fin.total_cogs_inr:,.2f}")
    print(f"Gross Profit              : ₹{fin.gross_profit_inr:,.2f} ({fin.gross_margin_pct}% Gross Margin)")
    print(f"Operating Expenses (OPEX) : ₹{fin.total_opex_inr:,.2f}")
    print(f"EBITDA                    : ₹{fin.ebitda_inr:,.2f} ({fin.ebitda_margin_pct}% EBITDA Margin)")
    print(f"Tax Expense (Sec 80-IAC)  : ₹{fin.tax_expense_inr:,.2f} (0.00% Tax Holiday)")
    print(f"Net Income (PAT)          : ₹{fin.net_income_inr:,.2f} ({fin.net_margin_pct}% Net Margin)")
    print("-" * 70)
    print("BALANCE SHEET & UNIT ECONOMICS:")
    print(f"  • Cash & Reserves       : ₹{fin.cash_and_reserves_inr:,.2f}")
    print(f"  • Total Assets          : ₹{fin.total_assets_inr:,.2f}")
    print(f"  • Net Shareholder Equity: ₹{fin.total_equity_inr:,.2f}")
    print(f"  • ARPU                  : ₹{fin.arpu_inr:,.2f} | CAC: ₹{fin.cac_inr:,.2f}")
    print(f"  • LTV / CAC Ratio       : {fin.ltv_cac_ratio}x")
    print(f"  • Monthly Burn Rate     : ₹{fin.monthly_burn_inr:,.2f} | Runway: {fin.runway_months} mos")
    print("=" * 70)

    if getattr(args, "generate_reports", False):
        reports = erp.generate_markdown_reports()
        print(f"✅ Generated: {reports['financial_report']}")
        print(f"✅ Generated: {reports['portfolio_report']}")


def cmd_orders(args):
    erp = get_erp()
    summary = erp.get_portfolio_summary()
    print("=" * 70)
    print(f"  OMEGA INFINITY — ENTERPRISE ORDER MANAGEMENT SYSTEM (OMS)")
    print(f"  Total Consignment Value : €{summary['total_consignment_value_eur']:,.2f} EUR")
    print(f"  Platform Fees Earned    : ₹{summary['total_platform_fees_earned_inr']:,.2f} INR")
    print("=" * 70)
    for o in erp.orders.values():
        cbam_str = f"CBAM: €{o.cbam_tariff_eur:,.2f}" if o.cbam_required else "CBAM Exempt"
        print(f"[{o.order_id}] {o.client_name[:26]:<26} -> {o.buyer_country} ({o.docket_status})")
        print(f"         Value: €{o.consignment_value_eur:,.2f} | Fee: ₹{o.platform_fee_inr:,.2f} | LC: {o.lc_number} | {cbam_str}")
        print(f"         Seal: {o.sha256_audit_seal[:32]}...")
    print("=" * 70)


def cmd_clients(args):
    erp = get_erp()
    summary = erp.get_portfolio_summary()
    print("=" * 70)
    print(f"  OMEGA INFINITY — ENTERPRISE CLIENT CRM DIRECTORY")
    print(f"  Total Active ARR: ₹{summary['total_arr_inr']:,.2f} | Active Clients: {summary['active_clients']}")
    print("=" * 70)
    for c in erp.clients.values():
        print(f"[{c.account_id}] {c.company_name} ({c.contract_tier} - Rating: {c.credit_rating})")
        print(f"         Hub: {c.hub_location} | Sector: {c.industry_sector}")
        print(f"         Contact: {c.decision_maker_name} ({c.decision_maker_title}) | ARR: ₹{c.arr_inr:,.2f} | {c.payment_terms}")
    print("=" * 70)


def cmd_do_everything(args):
    orch = get_orchestrator()
    print("=" * 72)
    print("  OMEGA INFINITY — SUPREME CONSTITUTIONAL 'DO EVERYTHING' PROTOCOL")
    print("  Enforcing Section 101 across All 13 Modes (A - M) & 24 Autonomous Agents")
    print("=" * 72)
    manifest = orch.do_everything()
    print(f"Status           : {manifest['overall_status']}")
    print(f"Execution ID     : {manifest['execution_id']}")
    print(f"Total Modes Run  : {manifest['total_modes_executed']} / 13")
    print(f"Total Time       : {manifest['total_elapsed_seconds']}s")
    print("-" * 72)
    print("MODES EXECUTED:")
    for m in manifest['modes']:
        print(f"  • Mode {m['mode_code']} ({m['mode_name']:<12}): {m['description']} [{m['elapsed_seconds']}s]")
    print("-" * 72)
    snap = manifest['financial_snapshot']
    print("FINANCIAL & ENTERPRISE SNAPSHOT:")
    print(f"  • Gross Revenue (ARR) : ₹{snap['gross_revenue_annualized_inr']:,.2f} ({snap['gross_margin_pct']}% Gross Margin)")
    print(f"  • Net Income (PAT)    : ₹{snap['net_income_inr']:,.2f} (0% Tax under Sec 80-IAC)")
    print(f"  • Liquid Reserves     : ₹{snap['cash_and_reserves_inr']:,.2f} ({snap['runway_months']:.1f} mos runway)")
    print(f"  • Enterprise Valuation: ₹{snap['implied_enterprise_valuation_inr']:,.2f} INR (10x ARR multiple)")
    print(f"  • Red Team Verdict    : {manifest['red_team_verdict']['status']} ({manifest['red_team_verdict']['average_survival_pct']}% survival)")
    print("=" * 72)


def cmd_red_team(args):
    rt = get_red_team()
    print("=" * 72)
    print("  OMEGA INFINITY — ADVERSARIAL RED TEAM STRESS-TEST SUITE")
    print("  Constitution Section 14: 12 Canonical Probes")
    print("=" * 72)
    res = rt.run_all_12_probes()
    for p in res['probes']:
        print(f"[{p['probe_id']}] {p['probe_name']} -> {p['resilience_rating']} ({p['survival_probability_pct']}%)")
        print(f"         Scenario: {p['stress_scenario']}")
        print(f"         Defense : {p['mitigation_mechanism']}")
    print("-" * 72)
    print(f"Overall Verdict   : {res['overall_resilience_verdict']}")
    print(f"Average Survival  : {res['average_survival_probability_pct']}% across 12 probes in {res['elapsed_seconds']}s")
    print("=" * 72)


def cmd_valuation(args):
    val = get_valuation_engine()
    res = val.compute_all_horizons()
    print("=" * 72)
    print("  OMEGA INFINITY — SOVEREIGN VALUATION & CAPITAL ALLOCATION")
    print(f"  Holding: {res['holding_entity']} | Founder: {res['founder']} (100% Equity)")
    print("=" * 72)
    for h in res['horizons']:
        print(f"[{h['year']}] {h['phase_name']}")
        print(f"       ARR Target: ₹{h['target_arr_inr']:,.2f} (${h['target_arr_usd']:,.2f} USD) | Clients: {h['enterprise_clients']}")
        print(f"       Multiple  : {h['valuation_multiple_arr']}x ARR | Implied Valuation: ₹{h['implied_valuation_inr']:,.2f} (${h['implied_valuation_usd']:,.2f} USD)")
        print(f"       Founder Net Worth: ₹{h['founder_net_worth_inr']:,.2f} (${h['founder_net_worth_usd']:,.2f} USD) [{h['founder_equity_pct']}% equity]")
        print(f"       Milestone : {h['strategic_milestone']}")
        print("-" * 72)
    print("=" * 72)


def cmd_serve(args):
    run_server(port=args.port)


def cmd_autopilot(args):
    from omega_infinity.omega_autonomous_daemon_247 import get_autonomous_daemon
    import time
    daemon = get_autonomous_daemon()

    if getattr(args, "start", False):
        print("[AUTOPILOT] Initializing OMEGA ∞ 24/7 Continuous Sovereign Engine...")
        if getattr(args, "foreground", False):
            print("Running in foreground mode (Press Ctrl+C to terminate)...")
            daemon.start_background()
            try:
                while True:
                    time.sleep(1.0)
            except KeyboardInterrupt:
                daemon.stop()
                print("\n[AUTOPILOT] Autopilot stopped gracefully.")
        else:
            res = daemon.start_background()
            print(f"[SUCCESS] {res['message']}")
            print(f"Status: {res['status']} | Started At: {res.get('started_at')}")
        return

    if getattr(args, "stop", False):
        print("[AUTOPILOT] Halting 24/7 Sovereign Engine...")
        res = daemon.stop()
        print(f"[SUCCESS] {res['message']}")
        return

    if getattr(args, "once", False):
        print("[AUTOPILOT] Executing single-pass multi-cadence cycle (Realtime + Hourly + Daily + Weekly)...")
        res = daemon.step(force_all=True)
        print("=" * 72)
        print("  OMEGA INFINITY — 24/7 AUTONOMOUS PULSE EXECUTION RECEIPT")
        print("=" * 72)
        print(f"Cadences Executed : {', '.join(res['cadences_executed'])}")
        print(f"Realtime Dockets  : {res.get('realtime', {}).get('dockets_processed', 0)} dockets audited")
        print(f"Ledger Integrity  : {'VALID' if res.get('realtime', {}).get('ledger_valid') else 'INVALID'}")
        print(f"Daily Orchestrator: {res.get('daily', {}).get('orchestrator_modes_run', 0)} modes in {res.get('daily', {}).get('orchestrator_time_s', 0)}s")
        print(f"Red Team Verdict  : {res.get('daily', {}).get('red_team_verdict')} ({res.get('daily', {}).get('red_team_survival_pct')}%)")
        print(f"Treasury Runway   : {res.get('hourly', {}).get('runway_months', 0):.1f} months")
        print("=" * 72)
        return

    # Default to status
    st = daemon.get_status()
    print("=" * 72)
    print("  OMEGA INFINITY — 24/7 SOVEREIGN AUTOPILOT STATUS")
    print("=" * 72)
    print(f"Engine State      : {'🟢 RUNNING (24/7 ACTIVE)' if st['is_running'] else '⏸️ STANDBY'}")
    print(f"Health Status     : {st['health_status']}")
    print(f"Resilience Verdict: {st['resilience_verdict']}")
    print(f"Uptime            : {st['uptime_seconds']:.1f}s ({st['uptime_seconds']/3600:.2f} hours)")
    print(f"Total Pulses      : {st['total_pulses']}")
    print(f"Cycles Executed   : Realtime: {st['realtime_cycles']} | Hourly: {st['hourly_cycles']} | Daily: {st['daily_cycles']} | Weekly: {st['weekly_cycles']}")
    print(f"Dockets Processed : {st['dockets_processed']}")
    print(f"Auto Revenue (INR): ₹{st['autonomous_revenue_inr']:,.2f}")
    print(f"Anomalies Healed  : {st['anomalies_healed']}")
    print(f"Last Pulse        : {st['last_pulse_timestamp']}")
    print("-" * 72)
    print("Active Cadences   :")
    for c in st['active_cadences']:
        print(f"  • {c}")
    print("-" * 72)
    print("Recent Logs       :")
    for log in st.get('recent_logs', [])[:5]:
        print(f"  [{log['timestamp'][11:19]}] [{log['category']}] {log['message']}")
    print("=" * 72)


def cmd_playbooks(args):
    from omega_infinity.omega_startup_mnc_matrix import get_playbook_engine
    engine = get_playbook_engine()

    if getattr(args, "inspect", None):
        pb = engine.get_playbook(args.inspect)
        if not pb:
            print(f"[ERROR] Playbook '{args.inspect}' not found.")
            return
        print("=" * 72)
        print(f"  STARTUP & MNC PLAYBOOK: {pb['entity_name'].upper()}")
        print("=" * 72)
        print(f"Type & Category   : {pb['entity_type']} | {pb['category']}")
        print(f"Foundational Thesis: {pb['foundational_thesis']}")
        print(f"Monetization Engine: {pb['monetization_engine']}")
        print(f"Unit Economics    : {pb['unit_economics_benchmark']}")
        print(f"Structural Moat   : {pb['structural_moat']}")
        print(f"1-Person Adaptation: {pb['autonomous_1person_adaptation']}")
        print(f"Agents Assigned   : {', '.join(pb['sovereign_agent_mapping'])}")
        print("Tactical Rules    :")
        for r in pb['tactical_rules']:
            print(f"  • {r}")
        print("=" * 72)
        return

    if getattr(args, "synthesize", False):
        industry = getattr(args, "industry", None) or "Precision Engineering & Metal Fabrication"
        hub = getattr(args, "hub", None) or "Peenya Industrial Estate & Hosur Auto-Corridor"
        goal = getattr(args, "goal", None) or "Top-1% Sovereign Cross-Border Trade OS"
        print(f"[SYNTHESIZE] Formulating sovereign venture blueprint for {industry} in {hub}...")
        bp = engine.synthesize_venture_blueprint(industry, hub, goal)
        print("=" * 72)
        print(f"  SOVEREIGN VENTURE BLUEPRINT: {bp['blueprint_id']}")
        print("=" * 72)
        print(f"Target Industry   : {bp['target_industry']}")
        print(f"Beachhead Hub     : {bp['beachhead_hub']}")
        print(f"Scale Goal        : {bp['scale_goal']}")
        print("Architecture Blend:")
        for a in bp['architecture_blend']:
            print(f"  • {a}")
        print("Recommended Tiers :")
        for k, v in bp['recommended_pricing_tiers'].items():
            print(f"  • {k.replace('_', ' ').title()}: {v}")
        print("Phases            :")
        for p, desc in bp['execution_phases'].items():
            print(f"  • {p.replace('_', ' ').title()}: {desc}")
        print("=" * 72)
        return

    # Default to list
    pbs = engine.get_all_playbooks()
    print("=" * 72)
    print("  OMEGA INFINITY — MASTER STARTUP & MNC PLAYBOOK MATRIX")
    print("=" * 72)
    for p in pbs:
        print(f"[{p['id'].upper():<10}] {p['entity_name']} ({p['entity_type']})")
        print(f"             Category: {p['category']}")
        print(f"             Moat    : {p['structural_moat']}")
        print(f"             1-Person: {p['autonomous_1person_adaptation']}")
        print("-" * 72)
    print(f"Total Playbooks Available: {len(pbs)}. Inspect with: python omega_cli.py playbooks --inspect <id>")
    print("=" * 72)


def cmd_trillion(args):
    engine = get_trillion_engine()
    
    if getattr(args, "simulate", False):
        trade_pct = getattr(args, "trade_pct", 12.5) / 100.0
        nodes = getattr(args, "nodes", 75000)
        float_bn = getattr(args, "float_bn", 120.0)
        mult = getattr(args, "multiple", 30.0)
        
        sim = engine.simulate_trillion_scenario(
            global_trade_penetration_pct=trade_pct,
            enterprise_agent_nodes=nodes,
            escrow_float_usd_bn=float_bn,
            multiple=mult
        )
        print("=" * 76)
        print("  OMEGA INFINITY — PLANETARY TRILLION-DOLLAR SCENARIO SIMULATION")
        print("=" * 76)
        print("SIMULATION INPUTS:")
        print(f"  • Global Trade Penetration : {sim['inputs']['global_trade_penetration_pct']:.2f}% of $32.0T Global Trade")
        print(f"  • Captured Trade Volume    : ${sim['inputs']['captured_trade_gmv_usd']/1e12:.2f} Trillion USD")
        print(f"  • Enterprise Agent Nodes   : {sim['inputs']['enterprise_agent_nodes']:,} MNCs")
        print(f"  • Escrow Float Capital     : ${sim['inputs']['escrow_float_usd_bn']:.1f} Billion USD")
        print(f"  • Valuation Multiple (ARR) : {sim['inputs']['valuation_multiple']:.1f}x EBITDA")
        print("-" * 76)
        print("ANNUAL RUN-RATE REVENUE BREAKDOWN:")
        for k, v in sim['revenue_breakdown_usd'].items():
            if k.startswith("total"):
                continue
            print(f"  • {k.replace('_', ' ').title():<28}: ${v/1e9:.2f} Billion USD (₹{v*engine.fx_rate/1e12:.2f} Lakh Cr)")
        print("-" * 76)
        tot = sim['revenue_breakdown_usd']['total_arr_usd']
        ebitda = sim['profitability']['ebitda_usd']
        val_usd = sim['valuation']['implied_valuation_usd']
        val_inr = sim['valuation']['implied_valuation_inr']
        print(f"CONSOLIDATED SOVEREIGN ARR   : ${tot/1e9:.2f} Billion USD (₹{tot*engine.fx_rate/1e12:.2f} Lakh Cr)")
        print(f"CONSOLIDATED EBITDA (85.0%)  : ${ebitda/1e9:.2f} Billion USD")
        print(f"IMPLIED ENTERPRISE VALUATION : ${val_usd/1e12:.3f} TRILLION USD (₹{val_inr/1e12:,.2f} Lakh Crore INR)")
        status = "BREACHED $1T THRESHOLD" if sim['valuation']['is_trillion_dollar_company'] else "BELOW $1T"
        print(f"TRILLION-DOLLAR STATUS       : {status}")
        print("=" * 76)
        return

    if getattr(args, "pillars", False):
        pillars = engine.get_planetary_pillars()
        print("=" * 76)
        print("  OMEGA INFINITY — 7 PLANETARY REVENUE PILLARS ($50B+ ARR)")
        print("=" * 76)
        for p in pillars:
            print(f"\n▼ [{p.pillar_id}] {p.name.upper()}")
            print(f"  Description: {p.description}")
            print(f"  Target TAM : ${p.target_gmv_or_market_usd/1e9:.1f}B | Model: {p.take_rate_or_pricing_model}")
            print(f"  ARR Target : ${p.annual_revenue_usd/1e9:.2f} Billion USD (₹{p.annual_revenue_inr/1e12:.2f} Lakh Cr) | Margin: {p.gross_margin_pct}%")
            print(f"  Moat       : {p.moat_mechanism}")
            print(f"  Agents     : {', '.join(p.active_agents)}")
        print("=" * 76)
        return

    if getattr(args, "epochs", False):
        epochs = engine.get_trillion_epochs()
        print("=" * 76)
        print("  OMEGA INFINITY — 7 TEMPORAL COMPOUNDING EPOCHS (2027 -> 2060)")
        print("=" * 76)
        for e in epochs:
            print(f"\n▼ [{e.epoch_id} — {e.year}] {e.designation.upper()}")
            print(f"  Classification : {e.scale_classification}")
            print(f"  Annual Revenue : ${e.annual_revenue_usd/1e6:.2f}M USD (₹{e.annual_revenue_inr/1e7:,.1f} Cr)")
            if e.valuation_usd >= 1e12:
                v_str = f"${e.valuation_usd/1e12:.2f} TRILLION USD (₹{e.valuation_inr/1e12:,.2f} Lakh Cr)"
            elif e.valuation_usd >= 1e9:
                v_str = f"${e.valuation_usd/1e9:.2f} Billion USD (₹{e.valuation_inr/1e7:,.1f} Cr)"
            else:
                v_str = f"${e.valuation_usd/1e6:.2f} Million USD (₹{e.valuation_inr/1e7:,.1f} Cr)"
            print(f"  Implied Value  : {v_str} @ {e.valuation_multiple:.0f}x")
            print(f"  Founder Equity : {e.founder_equity_pct:.0f}% (Net Worth: ${e.founder_net_worth_usd/1e9:.2f}B USD)")
            print(f"  Milestone      : {e.strategic_objective}")
        print("=" * 76)
        return

    # Default Overview
    d = engine.generate_trillion_dollar_dossier()
    summary = d['milestone_summary']
    print("=" * 76)
    print("  OMEGA INFINITY — THE PLANETARY TRILLION-DOLLAR ENTERPRISE DOSSIER")
    print("=" * 76)
    print(f"Founder & Sovereign Commander: {d['founder']}")
    print(f"Academic Origin              : {d['academic_origin']}")
    print(f"Holding Entity / OpCo        : {d['holding_entity']} / {d['operating_entity']}")
    print(f"Target Scale                 : {d['target_scale']}")
    print("-" * 76)
    print("CORE PLANETARY THESIS:")
    print(f"  {d['mathematical_thesis']}")
    print("-" * 76)
    print("TEMPORAL SCALE MILESTONES:")
    print(f"  • 2027 (Beachhead)       : ${summary['2027_beachhead_valuation_usd']/1e6:.2f}M USD (₹{summary['2027_beachhead_valuation_inr']/1e7:,.2f} Cr) [100% Equity]")
    print(f"  • 2050 (Trillion Titan)  : ${summary['2050_trillion_valuation_usd']/1e12:.2f} TRILLION USD (₹{summary['2050_trillion_valuation_inr']/1e12:,.2f} Lakh Cr)")
    print(f"  • 2050 Founder Net Worth : ${summary['2050_founder_net_worth_usd']/1e9:.1f} BILLION USD ({summary['2050_founder_equity_pct']:.0f}% Equity)")
    print("-" * 76)
    print("EXPLORATION COMMANDS:")
    print("  • View 7 Revenue Pillars : python omega_cli.py trillion --pillars")
    print("  • View 7 Scale Epochs    : python omega_cli.py trillion --epochs")
    print("  • Run Custom Simulation  : python omega_cli.py trillion --simulate --trade-pct 15.0 --nodes 100000")
    print("=" * 76)


def cmd_asi(args):
    engine = get_planetary_gdp_asi_engine()

    if getattr(args, "simulate", False):
        res = engine.simulate_asi_gdp_impact(
            year=args.year,
            custom_world_gdp_trillion=args.gdp_trillion,
            ai_penetration_pct=args.ai_pct,
            omega_gdp_capture_bps=args.capture_bps,
            valuation_multiple=args.multiple
        )
        print("=" * 76)
        print(f"  OMEGA INFINITY — DYNAMIC WORLD GDP & ASI SCENARIO SIMULATOR")
        print("=" * 76)
        print(f"Simulation Year         : {res['year']}")
        print(f"Projected World GDP     : ${res['world_gdp_nominal_usd_trillion']} Trillion USD")
        print(f"AI Contribution %       : {res['ai_penetration_pct']}% (${res['ai_economic_value_usd_trillion']} Trillion)")
        print(f"OMEGA Capture Rate      : {res['omega_gdp_capture_bps']} bps ({res['omega_gdp_capture_pct']}%)")
        print(f"Valuation Multiple      : {res['valuation_multiple']}x ARR")
        print("-" * 76)
        print(f"OMEGA Enterprise Value  : {res['omega_enterprise_valuation_usd_formatted']} (₹{res['omega_enterprise_valuation_inr_lakh_crore']:,.2f} Lakh Crore)")
        print(f"Founder Equity %        : {res['founder_equity_pct']}%")
        print(f"Founder Net Worth       : {res['founder_net_worth_usd_formatted']}")
        print(f"Classification Status   : {res['status']}")
        print("=" * 76)
        return

    if getattr(args, "levels", False):
        levels = engine.get_intelligence_levels()
        print("=" * 76)
        print("  OMEGA INFINITY — 6-LEVEL MACHINE INTELLIGENCE TAXONOMY (LEVEL 0 - 5)")
        print("=" * 76)
        for lvl in levels:
            print(f"\n▼ [{lvl.level_code}] {lvl.level_name.upper()} ({lvl.era_timeline})")
            print(f"  Autonomy Index : {lvl.autonomy_index_pct:.0f}% | Compute: {lvl.training_compute_flops}")
            print(f"  Human Parity   : {lvl.human_parity_ratio}")
            print(f"  Cognition      : {lvl.cognitive_definition}")
            print("  Capabilities   :")
            for cap in lvl.core_capabilities:
                print(f"    • {cap}")
            print(f"  OMEGA Status   : {lvl.omega_implementation_status}")
        print("=" * 76)
        return

    if getattr(args, "powers", False):
        powers = engine.get_sovereignty_powers()
        print("=" * 76)
        print("  OMEGA INFINITY — 8 SOVEREIGN SUPERINTELLIGENCE POWERS (POW 1 - 8)")
        print("=" * 76)
        for p in powers:
            print(f"\n▼ [{p.power_id}] {p.name.upper()} ({p.asi_tier})")
            print(f"  Classification : {p.classification}")
            print(f"  Mechanism      : {p.description}")
            print(f"  Planetary Moat : {p.planetary_impact}")
            print(f"  OMEGA Leverage : {p.omega_sovereign_leverage}")
            print(f"  Constitution   : {p.governing_directive}")
        print("=" * 76)
        return

    if getattr(args, "gdp", False):
        trajectory = engine.get_world_gdp_trajectory()
        print("=" * 76)
        print("  OMEGA INFINITY — MACROECONOMIC WORLD GDP EXPANSION (1990 -> 2060+)")
        print("=" * 76)
        for e in trajectory:
            print(f"\n▼ [{e.year}] {e.epoch_name.upper()}")
            print(f"  World GDP      : ${e.world_gdp_nominal_usd_trillion:.1f}T USD (₹{e.world_gdp_inr_crore:,.0f} Cr)")
            print(f"  AI Value Share : {e.ai_contribution_pct:.1f}% (${e.ai_value_usd_trillion:.1f}T USD)")
            if e.omega_valuation_usd >= 1e12:
                val_str = f"${e.omega_valuation_usd/1e12:.2f} Trillion USD ({e.omega_world_gdp_share_pct:.4f}% World GDP)"
            elif e.omega_valuation_usd >= 1e6:
                val_str = f"${e.omega_valuation_usd/1e6:.2f} Million USD"
            else:
                val_str = "Pre-incorporation"
            print(f"  OMEGA Valuation: {val_str}")
            print(f"  Driver         : {e.primary_production_driver}")
        print("=" * 76)
        return

    # Default Overview
    d = engine.generate_asi_gdp_dossier()
    summary = d['world_gdp_summary']
    print("=" * 76)
    print("  OMEGA INFINITY — WORLD GDP, AGI/ASI TAXONOMY & SOVEREIGN POWERS")
    print("=" * 76)
    print(f"Founder & Sovereign Commander: {d['founder']}")
    print(f"Holding / Operating Entity   : {d['holding_entity']} / {d['operating_entity']}")
    print("-" * 76)
    print("MACROECONOMIC GDP TRAJECTORY:")
    print(f"  • Present 2026 World GDP    : ${summary['current_2026_gdp_usd_trillion']} Trillion (AI: {summary['current_2026_ai_pct']}%)")
    print(f"  • 2050 Planetary ASI GDP    : ${summary['target_2050_gdp_usd_trillion']} Trillion (AI: {summary['target_2050_ai_pct']}%)")
    print(f"    -> OMEGA 2050 Valuation   : {summary['omega_2050_valuation_usd']} ({summary['omega_2050_gdp_share_pct']} of GWP)")
    print(f"  • 2060 Solar Singularity GDP: ${summary['target_2060_gdp_usd_trillion']} Trillion (AI: {summary['target_2060_ai_pct']}%)")
    print(f"    -> OMEGA 2060 Valuation   : {summary['omega_2060_valuation_usd']} ({summary['omega_2060_gdp_share_pct']} of GWP)")
    print("-" * 76)
    print("EXPLORATION SUB-COMMANDS:")
    print("  • 6 Intelligence Levels    : python omega_cli.py asi --levels")
    print("  • 8 Sovereign Superpowers  : python omega_cli.py asi --powers")
    print("  • Full World GDP Trajectory: python omega_cli.py asi --gdp")
    print("  • Dynamic ASI Simulation   : python omega_cli.py asi --simulate [--year 2050, --gdp-trillion 550]")
    print("=" * 76)


def cmd_workflow(args):
    engine = get_workflow_engine()

    if getattr(args, "run_all", False):
        print("=" * 76)
        print("  OMEGA INFINITY — EXECUTING ALL 10 CANONICAL ENTERPRISE WORKFLOWS")
        print("=" * 76)
        batch = engine.run_all_workflows()
        print(f"Batch Execution ID : {batch['batch_execution_id']}")
        print(f"Total Workflows    : {batch['workflows_executed']}")
        print(f"Batch Status       : {batch['status']}")
        print(f"Total Elapsed Time : {batch['total_elapsed_seconds']}s")
        print("-" * 76)
        for r in batch["results"]:
            print(f"  [{r['workflow_id']}] {r['name']:<48} | {r['status']:<9} | {r['elapsed_seconds']:.3f}s | Seal: {r['seal'][:16]}...")
        print("=" * 76)
        return

    if getattr(args, "run", None):
        wf_id = args.run.upper()
        print(f"Executing workflow {wf_id} through 8-Point Canonical Standard...")
        try:
            rec = engine.run_workflow(wf_id)
            print("=" * 76)
            print(f"  WORKFLOW EXECUTION: [{rec.workflow_id}] {rec.workflow_name}")
            print("=" * 76)
            print(f"Execution ID     : {rec.execution_id}")
            print(f"Maturity Level   : {rec.maturity}")
            print(f"Overall Status   : {rec.status}")
            print(f"Trigger Source   : {rec.trigger_source}")
            print(f"Elapsed Time     : {rec.elapsed_seconds}s")
            print(f"SHA-256 Seal     : {rec.verification_seal}")
            print("-" * 76)
            print("8-POINT EXECUTION TRAJECTORY (Section 27 Standard):")
            for s in rec.steps_executed:
                print(f"  [{s.point_index}] {s.point_name:<12} : {s.status:<6} ({s.latency_ms:>5.1f}ms) -> {s.details}")
            print("=" * 76)
        except Exception as e:
            print(f"Workflow execution failed: {e}")
        return

    if getattr(args, "inspect", None):
        wf_id = args.inspect.upper()
        wf = engine.get_workflow(wf_id)
        if not wf:
            print(f"Error: Workflow '{wf_id}' not found.")
            return
        print("=" * 76)
        print(f"  WORKFLOW SPECIFICATION: [{wf.workflow_id}] {wf.name}")
        print("=" * 76)
        print(f"Domain        : {wf.domain}")
        print(f"Maturity      : {wf.maturity}")
        print(f"Directive     : {wf.governing_directive}")
        print(f"Description   : {wf.description}")
        print("-" * 76)
        print("8-POINT UNIVERSAL SPECIFICATION (Section 27):")
        print(f"  1. TRIGGER      : {wf.spec.trigger}")
        print(f"  2. INPUT        : {wf.spec.input_desc}")
        print(f"  3. PROCESS      : {wf.spec.process_desc}")
        print(f"  4. DECISION     : {wf.spec.decision_rule}")
        print(f"  5. OUTPUT       : {wf.spec.output_desc}")
        print(f"  6. VERIFICATION : {wf.spec.verification_check}")
        print(f"  7. LOG          : {wf.spec.log_destination}")
        print(f"  8. ESCALATION   : {wf.spec.escalation_path}")
        print("=" * 76)
        return

    # Default: List all workflows
    workflows = engine.list_workflows()
    print("=" * 76)
    print("  OMEGA INFINITY — 10 CANONICAL AUTONOMOUS ENTERPRISE WORKFLOWS")
    print("  Enforcing Section 27 (8-Point Standard) & Section 28 (Maturity Framework)")
    print("=" * 76)
    for w in workflows:
        print(f"\n▼ [{w['workflow_id']}] {w['name'].upper()}")
        print(f"  Domain        : {w['domain']} | Maturity: {w['maturity']}")
        print(f"  Directive     : {w['governing_directive']}")
        print(f"  Summary       : {w['description']}")
        print(f"  Trigger       : {w['spec']['trigger']}")
        print(f"  Verification  : {w['spec']['verification_check']}")
    print("-" * 76)
    print("WORKFLOW CLI COMMANDS:")
    print("  • Run Specific Workflow : python omega_cli.py workflow --run WF-01")
    print("  • Run All Workflows     : python omega_cli.py workflow --run-all")
    print("  • Inspect 8-Point Spec  : python omega_cli.py workflow --inspect WF-01")
    print("=" * 76)


def cmd_plane(args):
    """Manage Plane Community Edition (CE) integration, boards, sync, backup, and changelog."""
    from omega.integrations.plane_connector import PlaneClient
    from omega.orchestration.plane_dispatcher import PlaneDispatcher
    from omega.orchestration.plane_boards import PlaneBoardEngine
    from omega.orchestration.plane_backup import PlaneBackupEngine
    from omega.orchestration.plane_git_bridge import PlaneGitBridge

    action = getattr(args, "action", "status")
    is_sync = getattr(args, "sync", False)
    client = PlaneClient(dry_run=not is_sync)

    print("=" * 76)
    print("  OMEGA INFINITY — PLANE COMMUNITY EDITION (CE) ENTERPRISE HUB")
    print("=" * 76)

    if action == "status":
        try:
            status = client.health_check()
            p_stat = status.get("status", "ONLINE").upper()
            ver = status.get("version", "v1.4.2")
            print(f"Target Plane Server : {client.base_url}")
            print(f"Health Probe Status : {p_stat} (Plane {ver})")
            print(f"Operating Mode      : {'LIVE HTTP' if is_sync else 'SIMULATION / DRY-RUN'}")
            print("-" * 76)
            projects = client.list_projects("omega")
            print(f"Active Projects     : {len(projects)} boards discovered")
            for p in projects[:6]:
                print(f"  • [{p.get('identifier', 'PROJ')}] {p.get('name', 'Untitled')}")
        except Exception as e:
            print(f"Target Plane Server : {client.base_url}")
            print(f"Health Probe Status : OFFLINE ({e})")
            print(f"Operating Mode      : {'LIVE HTTP' if is_sync else 'SIMULATION / DRY-RUN'}")
            print("-" * 76)
            print("Note: Start local Plane CE containers via: START_PLANE.bat [1] or START_PLANE.ps1")
        print("=" * 76)

    elif action == "sync":
        dispatcher = PlaneDispatcher(client=client)
        print(f"Executing task registry dispatch (Mode: {'LIVE' if is_sync else 'SIMULATION / DRY-RUN'})...")
        res = dispatcher.sync_all_tasks(workspace_slug="omega", project_id="CORE")
        print(f"[SUCCESS] Dispatched {res.get('tasks_dispatched', 0)} tasks into Plane CE.")
        print("=" * 76)

    elif action == "provision":
        engine = PlaneBoardEngine(client=client)
        print(f"Provisioning sovereign departmental boards and sprint cycles...")
        res = engine.provision_all("omega", sprint_count=3)
        print(f"[SUCCESS] Provisioned {len(res.get('projects', []))} boards & {res.get('total_sprints_provisioned', 0)} sprint cycles.")
        print("=" * 76)

    elif action == "backup":
        backup_engine = PlaneBackupEngine(client=client)
        print("Exporting complete workspace dossier and snapshot...")
        exp = backup_engine.export_workspace("omega")
        saved = backup_engine.save_backup(exp)
        dossier = backup_engine.generate_dossier_markdown(exp)
        print(f"[SUCCESS] Saved backup to: {saved}")
        print(f"Projects backed up: {len(exp['projects'])} | Issues: {sum(len(p['issues']) for p in exp['projects'])}")
        print("=" * 76)

    elif action == "changelog":
        bridge = PlaneGitBridge(client=client)
        sample_commits = [
            {"hash": "1865e97b", "author": "ApexEngineer", "date": "2026-10-01", "message": "[CORE] Deploy Plane CE stack"},
            {"hash": "18b608e7", "author": "ApexEngineer", "date": "2026-10-02", "message": "[CORE] Add Git bridge, backup engine & reactor"},
            {"hash": "c1a2b3c4", "author": "ApexEngineer", "date": "2026-10-04", "message": "CAP-10: Settle M2M multi-currency corridors"},
        ]
        log = bridge.generate_release_changelog(sample_commits)
        print(log)
        print("=" * 76)


def main():

    parser = argparse.ArgumentParser(description="OMEGA INFINITY (Ω-OS) Sovereign CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # status
    p_status = subparsers.add_parser("status", help="Display sovereign enterprise status")
    p_status.set_defaults(func=cmd_status)

    # mode
    p_mode = subparsers.add_parser("mode", help="Switch constitutional operating mode (A-M)")
    p_mode.add_argument("mode_code", help="Mode code letter A through M")
    p_mode.set_defaults(func=cmd_mode)

    # swarm
    p_swarm = subparsers.add_parser("swarm", help="Run 12-agent sovereign swarm cycle")
    p_swarm.set_defaults(func=cmd_swarm)

    # fleet
    p_fleet = subparsers.add_parser("fleet", help="Run 24-agent sovereign autonomous fleet cycle")
    p_fleet.set_defaults(func=cmd_fleet)

    # temporal
    p_temporal = subparsers.add_parser("temporal", help="Query past, present, and future temporal vectors")
    p_temporal.add_argument("--year", default="2027", help="Horizon year (2027, 2030, 2035, 2040, 2050)")
    p_temporal.set_defaults(func=cmd_temporal)

    # intel
    p_intel = subparsers.add_parser("intel", help="Search market and network intelligence")
    p_intel.add_argument("query", help="Search query string")
    p_intel.set_defaults(func=cmd_intel)

    # trade-audit
    p_audit = subparsers.add_parser("trade-audit", help="Audit a trade docket under UCP 600")
    p_audit.add_argument("file_path", help="Path to trade docket JSON file")
    p_audit.set_defaults(func=cmd_trade_audit)

    # ledger-verify
    p_verify = subparsers.add_parser("ledger-verify", help="Verify SHA-256 event ledger integrity")
    p_verify.set_defaults(func=cmd_ledger_verify)

    # finance
    p_finance = subparsers.add_parser("finance", help="Display MNC P&L, balance sheet, and unit economics")
    p_finance.add_argument("--generate-reports", action="store_true", help="Generate full markdown financial & portfolio reports")
    p_finance.set_defaults(func=cmd_finance)

    # orders
    p_orders = subparsers.add_parser("orders", help="List live export orders and consignment dockets")
    p_orders.set_defaults(func=cmd_orders)

    # clients
    p_clients = subparsers.add_parser("clients", help="List Tier-1 enterprise CRM client accounts")
    p_clients.set_defaults(func=cmd_clients)

    # do-everything
    p_everything = subparsers.add_parser("do-everything", help="Execute Supreme Constitutional DO EVERYTHING Protocol (Modes A - M)")
    p_everything.set_defaults(func=cmd_do_everything)

    # red-team
    p_redteam = subparsers.add_parser("red-team", help="Run 12 Section 14 adversarial stress-testing probes")
    p_redteam.set_defaults(func=cmd_red_team)

    # valuation
    p_val = subparsers.add_parser("valuation", help="Display sovereign venture valuation compounding (2027-2050)")
    p_val.set_defaults(func=cmd_valuation)

    # serve
    p_serve = subparsers.add_parser("serve", help="Launch the Glass Cockpit web server")
    p_serve.add_argument("--port", type=int, default=8888, help="Server port (default: 8888)")
    p_serve.set_defaults(func=cmd_serve)

    # autopilot
    p_auto = subparsers.add_parser("autopilot", help="Control 24/7 Sovereign Autonomous Engine")
    p_auto.add_argument("--start", action="store_true", help="Start the 24/7 autonomous autopilot")
    p_auto.add_argument("--foreground", action="store_true", help="Run 24/7 autopilot in foreground")
    p_auto.add_argument("--stop", action="store_true", help="Stop the 24/7 autonomous autopilot")
    p_auto.add_argument("--status", action="store_true", help="Display 24/7 autopilot telemetry")
    p_auto.add_argument("--once", action="store_true", help="Execute single multi-cadence autonomous pulse")
    p_auto.set_defaults(func=cmd_autopilot)

    # playbooks
    p_pb = subparsers.add_parser("playbooks", help="Inspect and synthesize from Startup & MNC master models")
    p_pb.add_argument("--list", action="store_true", help="List all available startup and MNC playbooks")
    p_pb.add_argument("--inspect", type=str, help="Inspect specific model (e.g. stripe, flexport, berkshire, asml)")
    p_pb.add_argument("--synthesize", action="store_true", help="Synthesize custom sovereign venture blueprint")
    p_pb.add_argument("--industry", type=str, help="Target industry for synthesis")
    p_pb.add_argument("--hub", type=str, help="Target beachhead hub")
    p_pb.add_argument("--goal", type=str, help="Scale goal for synthesis")
    p_pb.set_defaults(func=cmd_playbooks)

    # trillion
    p_trillion = subparsers.add_parser("trillion", help="Inspect Planetary Trillion-Dollar Enterprise Architecture ($1T-$5T USD)")
    p_trillion.add_argument("--pillars", action="store_true", help="Display 7 Planetary Revenue Pillars ($50B+ ARR)")
    p_trillion.add_argument("--epochs", action="store_true", help="Display 7 Compounding Epochs from 2027 to 2060")
    p_trillion.add_argument("--simulate", action="store_true", help="Simulate custom planetary scale parameters")
    p_trillion.add_argument("--trade-pct", type=float, default=12.5, help="Global trade penetration % (default: 12.5)")
    p_trillion.add_argument("--nodes", type=int, default=75000, help="Enterprise agent nodes count (default: 75,000)")
    p_trillion.add_argument("--float-bn", type=float, default=120.0, help="Escrow float balance in Billion USD (default: 120.0)")
    p_trillion.add_argument("--multiple", type=float, default=30.0, help="Valuation multiple on EBITDA (default: 30.0)")
    p_trillion.set_defaults(func=cmd_trillion)

    # asi
    p_asi = subparsers.add_parser("asi", help="Inspect World GDP, AGI/ASI Levels & Sovereign Superpowers")
    p_asi.add_argument("--levels", action="store_true", help="Display 6-level machine intelligence taxonomy (Level 0 - 5)")
    p_asi.add_argument("--powers", action="store_true", help="Display 8 sovereign superintelligence powers")
    p_asi.add_argument("--gdp", action="store_true", help="Display World GDP macroeconomic trajectory (1990 - 2060+)")
    p_asi.add_argument("--simulate", action="store_true", help="Simulate dynamic World GDP & ASI scale scenario")
    p_asi.add_argument("--year", type=int, default=2050, help="Simulation year (default: 2050)")
    p_asi.add_argument("--gdp-trillion", type=float, default=None, help="Custom World GDP in Trillion USD")
    p_asi.add_argument("--ai-pct", type=float, default=None, help="Custom AI economic contribution %")
    p_asi.add_argument("--capture-bps", type=float, default=18.5, help="OMEGA GDP capture rate in basis points (default: 18.5 bps = 0.185%)")
    p_asi.add_argument("--multiple", type=float, default=25.5, help="Valuation multiple (default: 25.5)")
    p_asi.set_defaults(func=cmd_asi)

    # workflow
    p_wf = subparsers.add_parser("workflow", help="Inspect and execute autonomous enterprise workflows (Section 27 & 28)")
    p_wf.add_argument("--run", type=str, help="Execute specific workflow through 8-point standard (e.g. WF-01)")
    p_wf.add_argument("--run-all", action="store_true", help="Execute all 10 canonical enterprise workflows")
    p_wf.add_argument("--inspect", type=str, help="Inspect 8-point specification of a workflow (e.g. WF-01)")
    p_wf.set_defaults(func=cmd_workflow)

    # plane
    p_plane = subparsers.add_parser("plane", help="Plane Community Edition (CE) Project Management Hub")
    p_plane.add_argument("action", nargs="?", choices=["status", "sync", "provision", "backup", "changelog"], default="status", help="Plane management action (default: status)")
    p_plane.add_argument("--sync", action="store_true", help="Connect to live HTTP Plane instance instead of dry-run simulation")
    p_plane.set_defaults(func=cmd_plane)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        cmd_status(args)


if __name__ == "__main__":
    main()
