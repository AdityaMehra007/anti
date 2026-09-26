"""
VECTIS TRADE — Founder Command Line & Terminal Operating Interface
Usage:
  python vectis_cli.py status
  python vectis_cli.py audit <path/to/docket.json>
  python vectis_cli.py swarm
  python vectis_cli.py mine
  python vectis_cli.py daemon
"""

import sys
import os
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from vectis_core import VectisComplianceEngine
from vectis_parser import parse_docket_dict
from vectis_agents import AgentHarness
from vectis_network_miner import mine_leads
from vectis_daemon import run_single_pass

def print_banner():
    print("""
=============================================================
  VECTIS TRADE TECHNOLOGIES PRIVATE LIMITED
  Autonomous Export Document & LC Compliance Terminal
=============================================================
""")

def cmd_status():
    print_banner()
    leads_file = os.path.join(BASE_DIR, "leads", "master_verified_leads.json")
    outbox_dir = os.path.join(BASE_DIR, "outbox")
    inbox_dir = os.path.join(BASE_DIR, "inbox")

    lead_count = 0
    if os.path.exists(leads_file):
        with open(leads_file, "r", encoding="utf-8") as f:
            lead_count = len(json.load(f))

    audited_count = len([f for f in os.listdir(outbox_dir) if f.endswith(".json")]) if os.path.exists(outbox_dir) else 0
    pending_count = len([f for f in os.listdir(inbox_dir) if f.endswith(".json")]) if os.path.exists(inbox_dir) else 0

    print(f"Pipeline & Operations Summary:")
    print(f"  - Verified Trade Leads in CRM:    {lead_count}")
    print(f"  - Dockets Awaiting Ingestion:      {pending_count}")
    print(f"  - Completed Audit Certificates:   {audited_count}")
    print(f"  - Target Gross Margin:             96.1%")
    print(f"  - Unit Contribution Margin:        ₹1,410 / Docket")
    print(f"  - Cash Runway Posture:             Infinite (Profitable at Unit Level)")
    print(f"  - Current Priority Bottleneck:     Customer #1 Peenya Pilot Sign-off")
    print("=============================================================")

def cmd_audit(filepath):
    print_banner()
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    lc, invoice, pl, bl, coo = parse_docket_dict(data)
    engine = VectisComplianceEngine()
    result = engine.audit_trade_docket(lc, invoice, pl, bl, coo)

    badge = "PASSED (BANK-READY)" if result.status == "PASSED" else f"REJECT ({result.fatal_discrepancies} FATAL)"
    print(f"DOCKET AUDIT RESULT: [{badge}]")
    print(f"  - Certificate ID: {result.docket_id}")
    print(f"  - Cryptographic Hash (SHA-256): {result.sha256_hash}")
    print(f"  - Total Discrepancies: {result.discrepancy_count}")
    print(f"  - Fatal Discrepancies: {result.fatal_discrepancies}\n")

    if result.discrepancies:
        print("Discrepancy Details:")
        for d in result.discrepancies:
            print(f"  * [{d.code}] {d.rule_reference} ({d.affected_document}): {d.description}")
            print(f"    FIX: {d.correction_suggestion}")
    else:
        print("  ✓ Perfect trade docket. Zero bank discrepancy rejections predicted.")

def main():
    if len(sys.argv) < 2:
        print_banner()
        print("Commands:")
        print("  status    - View live pipeline & operating metrics")
        print("  audit <f> - Run instant compliance audit on a trade docket JSON")
        print("  swarm     - Execute 9-agent autonomous operations cycle")
        print("  mine      - Mine verified leads from founder network")
        print("  daemon    - Run single pass of hot-folder ingestion")
        return

    cmd = sys.argv[1].lower()
    if cmd == "status":
        cmd_status()
    elif cmd == "audit":
        if len(sys.argv) < 3:
            print("Usage: python vectis_cli.py audit <path/to/docket.json>")
        else:
            cmd_audit(sys.argv[2])
    elif cmd == "swarm":
        print_banner()
        harness = AgentHarness()
        harness.run_daily_swarm_cycle()
    elif cmd == "mine":
        print_banner()
        mine_leads()
    elif cmd == "daemon":
        print_banner()
        count = run_single_pass()
        print(f"Hot-folder pass completed. Processed {count} dockets.")
    else:
        print(f"Unknown command: '{cmd}'")

if __name__ == "__main__":
    main()
