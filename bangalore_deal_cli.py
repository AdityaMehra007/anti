"""
Bengaluru Enterprise & Unicorn Deal CLI Management Console (OMEGA ∞)
Master CLI for managing 100 enterprise accounts, executing diagnostic harnesses,
generating custom SOWs, tracking dispatch status, and serving the Cockpit.
"""

import argparse
import csv
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path("e:/anti")
CRM_JSON = BASE_DIR / "data/bangalore_enterprise_crm_master_100.json"
QUEUE_CSV = BASE_DIR / "data/outbound_dispatch_queue.csv"
OUTPUT_DIR = BASE_DIR / "docs/generated_enterprise_deals"

def load_crm():
    if not CRM_JSON.exists():
        print(f"Error: CRM file {CRM_JSON} not found. Run scripts/scale_bangalore_crm_pipeline.py first.")
        sys.exit(1)
    with open(CRM_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def print_summary():
    crm = load_crm()
    total_val = sum(r["contract_inr"] for r in crm)
    gccs = [r for r in crm if r["type"] == "Fortune 500 GCC"]
    unis = [r for r in crm if r["type"] == "Bengaluru Tech Unicorn"]
    gcc_val = sum(r["contract_inr"] for r in gccs)
    uni_val = sum(r["contract_inr"] for r in unis)
    entry_total = sum(r["entry_po_inr"] for r in crm)
    
    print("\n========================================================")
    print("  BENGALURU ENTERPRISE COMMERCIAL OS (OMEGA INFINITY)")
    print("========================================================")
    print(f"Total Tracked Accounts:     {len(crm)}")
    print(f"Total Pipeline Value:       INR {total_val:,} (~${total_val/83.5:,.0f} USD)")
    print(f"Fortune 500 GCC Pipeline:   INR {gcc_val:,} ({len(gccs)} accounts)")
    print(f"Bengaluru Unicorn Pipeline: INR {uni_val:,} ({len(unis)} accounts)")
    print(f"Sub-Threshold Entry Total:  INR {entry_total:,} (< INR 5L Fast-Track)")
    print(f"Average Annual Retainer:    INR {round(total_val/len(crm)):,}")
    print("========================================================\n")

def list_targets(filter_type="ALL", limit=25):
    crm = load_crm()
    if filter_type.upper() == "GCC":
        crm = [r for r in crm if r["type"] == "Fortune 500 GCC"]
    elif filter_type.upper() in ["UNICORN", "STARTUP"]:
        crm = [r for r in crm if r["type"] == "Bengaluru Tech Unicorn"]
        
    print(f"\nListing top {min(limit, len(crm))} accounts (Filter: {filter_type}):")
    print(f"{'#':<3} {'Company Name':<35} {'Type':<22} {'Retainer (INR)':<15} {'Lead Contact'}")
    print("-" * 105)
    for idx, r in enumerate(crm[:limit], 1):
        cname = r['company'][:33]
        ctype = r['type'][:20]
        cval = f"INR {r['contract_inr']:,}"
        lead = r.get('lead_contact', 'N/A')[:30]
        print(f"{idx:<3} {cname:<35} {ctype:<22} {cval:<15} {lead}")
    print(f"\nTotal listed: {min(limit, len(crm))} / {len(crm)} accounts.\n")

def run_diagnostic_harness(harness_type):
    harness_map = {
        "sla": "vendor_sla_audit_harness.py",
        "eval": "llm_eval_regression_harness.py",
        "trade": "ucp600_trade_scrutiny_harness.py",
        "runway": "founders_office_triage_engine.py",
        "outbound": "autonomous_b2b_outbound_engine.py",
        "finops": "cloud_llm_finops_optimizer.py",
        "pod": "bot_engineering_pod_manager.py"
    }
    
    script_name = harness_map.get(harness_type.lower())
    if not script_name:
        print(f"Unknown harness '{harness_type}'. Available: {list(harness_map.keys())}")
        return
        
    script_path = BASE_DIR / "scripts/harnesses" / script_name
    print(f"\n--- Executing Diagnostic Harness: {script_name} ---\n")
    os.system(f"python {script_path}")

def generate_sow(company_name):
    crm = load_crm()
    target = None
    for r in crm:
        if company_name.lower() in r["company"].lower():
            target = r
            break
            
    if not target:
        print(f"Company '{company_name}' not found in CRM database.")
        return
        
    sow_content = f"""# STATEMENT OF WORK (SOW) — 14-DAY DISCRETIONARY PILOT
**Client Name:** {target['company']}  
**Campus Location:** {target['tech_park']}  
**Service Vector:** {target['service_vector']}  
**Procurement Rail:** {target['procurement_bypass']}  
**Total SOW Consideration:** INR {target['entry_po_inr']:,} + GST (< INR 5L Sub-Threshold PO)  

---

### 1. Scope & Objective
Execute a 14-day dedicated diagnostic sprint analyzing historical data across {target['company']}'s {target['tech_park'].split(',')[0]} operations to identify uncredited SLA penalties, benchmark AI reliability, or eliminate operational drag.

### 2. Milestone Deliverables & Payment Schedule
- **Milestone 1 (30% - INR {round(target['entry_po_inr']*0.3):,}):** Advance mobilization and environment setup within Client VPC/sandbox.
- **Milestone 2 (40% - INR {round(target['entry_po_inr']*0.4):,}):** Interim demonstration of identified discrepancies on Day 8.
- **Milestone 3 (30% - INR {round(target['entry_po_inr']*0.3):,}):** Final executive audit report, code handover, and retainer proposal on Day 14.

### 3. Acceptance & Retainer Transition
Upon verification of positive recovery or cost optimization, Client and Service Provider may transition to the annualized retainer of **INR {target['contract_inr']:,} / Year**.

---
**Accepted for {target['company']}:** _______________________  
**Accepted for Service Provider:** Aditya Mehra
"""
    clean_name = target['company'].lower().replace(' ', '_').replace('(', '').replace(')', '')
    sow_file = OUTPUT_DIR / f"{clean_name}_sub_threshold_sow.md"
    sow_file.write_text(sow_content, encoding="utf-8")
    print(f"\nSuccessfully generated customized SOW: {sow_file}\n")

def serve_cockpit(port=8888):
    os.chdir(BASE_DIR)
    print(f"\n========================================================")
    print(f" Serving Cockpit at: http://localhost:{port}/bangalore_enterprise_deal_cockpit.html")
    print(f" Press Ctrl+C to terminate.")
    print(f"========================================================\n")
    server = HTTPServer(("localhost", port), SimpleHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

def main():
    parser = argparse.ArgumentParser(description="Bengaluru Enterprise Deal CLI (OMEGA Infinity)")
    parser.add_argument("--summary", action="store_true", help="Display pipeline summary")
    parser.add_argument("--list", choices=["all", "gcc", "unicorn"], nargs="?", const="all", help="List target accounts")
    parser.add_argument("--run-audit", choices=["sla", "eval", "trade", "runway", "outbound", "finops", "pod"], help="Run diagnostic harness")
    parser.add_argument("--generate-sow", type=str, help="Generate customized SOW for company")
    parser.add_argument("--serve-cockpit", type=int, nargs="?", const=8888, help="Serve interactive HTML cockpit")

    args = parser.parse_args()

    if args.summary:
        print_summary()
    elif args.list:
        list_targets(args.list)
    elif args.run_audit:
        run_diagnostic_harness(args.run_audit)
    elif args.generate_sow:
        generate_sow(args.generate_sow)
    elif args.serve_cockpit:
        serve_cockpit(args.serve_cockpit)
    else:
        print_summary()
        parser.print_help()

if __name__ == "__main__":
    main()
