"""
REVENUE OS — FULL SYSTEM ACTIVATION
Runs ALL automations, prints executive brief, shows pipeline status,
and reports pending approval cards.

Usage:  python -m REVENUE_OS.activate_all
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from datetime import datetime
from REVENUE_OS.database.db import get_db
from REVENUE_OS.command_center.cli import RevenueOSCLI
from REVENUE_OS.automations.automations import AutomationEngine
from REVENUE_OS.founder_os.approval_center import ApprovalCenter

def activate():
    db = get_db()
    cli = RevenueOSCLI(db=db)
    engine = AutomationEngine(db=db)
    approval = ApprovalCenter(db=db)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print()
    print("=" * 66)
    print("   ANTIGRAVITY 24/7 REVENUE OS — FULL SYSTEM ACTIVATION")
    print(f"   Timestamp: {now}")
    print("=" * 66)

    # --- 1. RUN ALL 10 AUTOMATIONS ---
    print()
    print("▸ PHASE 1: EXECUTING ALL 10 AUTOMATED PIPELINES")
    print("-" * 50)
    automations = engine.list_automations()
    results = []
    for name in automations:
        res = engine.run_automation(name)
        status_icon = "✓" if res["status"] == "SUCCESS" else "✗"
        print(f"  {status_icon} {name:<30} {res['status']:<10} ({res['duration_sec']:.3f}s)")
        results.append(res)

    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    print(f"\n  Result: {success_count}/{len(results)} automations completed successfully.")

    # --- 2. DATABASE STATUS ---
    print()
    print("▸ PHASE 2: DATABASE & PIPELINE STATUS")
    print("-" * 50)
    with db.get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM leads")
        leads_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM leads WHERE status = 'QUALIFIED'")
        qualified = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*), COALESCE(SUM(deal_value_inr), 0), COALESCE(SUM(expected_revenue_inr), 0) FROM deals")
        row = cur.fetchone()
        deals_count, pipeline_total, pipeline_weighted = row[0], row[1], row[2]

        cur.execute("SELECT COUNT(*), COALESCE(SUM(deal_value_inr), 0) FROM deals WHERE stage = 'WON'")
        won_row = cur.fetchone()
        won_count, won_rev = won_row[0], won_row[1]

        cur.execute("SELECT stage, COUNT(*) as cnt FROM deals GROUP BY stage ORDER BY cnt DESC")
        stage_breakdown = [(r[0], r[1]) for r in cur.fetchall()]

    print(f"  Leads Total:       {leads_count}")
    print(f"  Qualified Leads:   {qualified}")
    print(f"  Deals Total:       {deals_count}")
    print(f"  Deals Won:         {won_count}")
    print(f"  Pipeline Total:    ₹{pipeline_total:,.0f}")
    print(f"  Pipeline Weighted: ₹{pipeline_weighted:,.0f}")
    print(f"  Won Revenue:       ₹{won_rev:,.0f}")
    if stage_breakdown:
        print(f"  Stage Breakdown:")
        for stage, cnt in stage_breakdown:
            print(f"    {stage:<20} {cnt}")

    # --- 3. PENDING APPROVALS ---
    print()
    print("▸ PHASE 3: FOUNDER APPROVAL CENTER")
    print("-" * 50)
    pending = db.get_pending_approvals()
    if pending:
        for p in pending:
            print(f"  🔔 ID={p['id']} | {p['title']}")
            print(f"     Requester: {p['requester_agent']}")
            print(f"     Cost: ₹{p.get('cost_inr', 0):,.0f} | Upside: ₹{p.get('upside_inr', 0):,.0f}")
            print(f"     Risk: {p.get('risk_level', 'N/A')} | Status: {p['status']}")
            print()
    else:
        print("  No pending approval requests.")

    # --- 4. OUTREACH DOSSIERS ---
    print()
    print("▸ PHASE 4: ACTIVE OUTREACH DOSSIERS")
    print("-" * 50)
    from pathlib import Path
    dossier_dir = Path(__file__).resolve().parent / "06_SALES" / "active_outreach_dossiers"
    if dossier_dir.exists():
        dossiers = sorted(dossier_dir.glob("*.md"))
        for d in dossiers:
            print(f"  📄 {d.name}")
        print(f"  Total: {len(dossiers)} dossier(s) ready for dispatch")
    else:
        print("  No dossier directory found.")

    # --- 5. AUTOMATION DETAIL OUTPUTS ---
    print()
    print("▸ PHASE 5: AUTOMATION INTELLIGENCE OUTPUTS")
    print("-" * 50)
    for r in results:
        if r["output"]:
            print(f"\n  [{r['name']}]")
            for k, v in r["output"].items():
                if isinstance(v, list):
                    print(f"    {k}:")
                    for item in v:
                        print(f"      • {item}")
                else:
                    print(f"    {k}: {v}")

    # --- 6. EXECUTIVE BRIEF ---
    print()
    print("▸ PHASE 6: EXECUTIVE BRIEF")
    print("-" * 50)
    brief = cli.get_executive_brief()
    print(brief)

    # --- 7. RECENT AUDIT LOG ---
    print()
    print("▸ PHASE 7: RECENT AUDIT LOG (last 15 entries)")
    print("-" * 50)
    logs = db.get_recent_audit_logs(limit=15)
    for log in logs:
        print(f"  [{log.get('id', '?')}] {log.get('agent_name', '?')} | {log.get('action_tier', '?')} | {log.get('action_name', '?')}")

    # --- 8. SYSTEM HEALTH SUMMARY ---
    print()
    print("=" * 66)
    print("   SYSTEM ACTIVATION COMPLETE")
    print("=" * 66)
    print(f"  Automations: {success_count}/{len(results)} ✓")
    print(f"  Pipeline:    ₹{pipeline_total:,.0f} total / ₹{pipeline_weighted:,.0f} weighted")
    print(f"  Approvals:   {len(pending)} pending")
    print(f"  Dossiers:    {len(dossiers) if dossier_dir.exists() else 0} ready")
    print(f"  Audit Trail: {len(logs)} recent entries")
    print()
    print("  → Web Command Center: python -m REVENUE_OS --serve --port 8765")
    print("  → Dashboard URL:      http://127.0.0.1:8765")
    print("=" * 66)

if __name__ == "__main__":
    activate()
