import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cli_path = os.path.join(REPO_ROOT, "omega_cli.py")

with open(cli_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update cmd_deals implementation
old_dispatch_block = '''    if is_dispatch:
        dispatch_ledger_path = os.path.join(REPO_ROOT, "data", "commercial_dispatch_ledger.json")
        if os.path.exists(dispatch_ledger_path):
            with open(dispatch_ledger_path, "r", encoding="utf-8") as f:
                ledger = json.load(f)
            t1 = sum(1 for x in ledger if "tier 1" in x.get("priority_tier", "").lower())
            t2 = sum(1 for x in ledger if "tier 2" in x.get("priority_tier", "").lower())
            print(f"Dispatch Ledger Status   : STAGED_READY (Outbound Batches Primed)")
            print(f"Total Dispatches Staged  : {len(ledger)} Accounts")
            print(f"Immediate Strike (Tier 1): {t1} accounts (<24h high-conviction cadence)")
            print(f"Secondary (Tier 2)       : {t2} accounts (48h high-velocity cadence)")
            print(f"Outbound Dispatch Board  : COMMERCIAL_DISPATCH_BOARD.md")
        else:
            print(f"Dispatch ledger ready. See COMMERCIAL_DISPATCH_BOARD.md for multi-touch cadences.")
        print("=" * 76)
        return'''

new_dispatch_block = '''    from omega_outbound_execution_engine import get_outbound_engine
    engine = get_outbound_engine()

    is_funnel = getattr(args, "funnel", False)
    if is_funnel:
        metrics = engine.compute_funnel_metrics()
        print("PIPELINE CONVERSION FUNNEL TELEMETRY:")
        print(f"  • Total Commercial Accounts   : {metrics.total_accounts}")
        print(f"  • Staged Ready for Strike     : {metrics.staged_ready}")
        print(f"  • Dispatched Touch 1 (InMail) : {metrics.dispatched_touch1}")
        print(f"  • Dispatched Touch 2 (Email)  : {metrics.dispatched_touch2}")
        print(f"  • Active Replies Inbound      : {metrics.replies_received}")
        print(f"  • Pilot POs Commissioned      : {metrics.pilots_commissioned}")
        print("-" * 76)
        print(f"  • Total Pipeline ARR (INR)    : ₹{metrics.total_pipeline_arr_inr:,}")
        print(f"  • Sub-5L Pilot PO Value (INR) : ₹{metrics.total_pilot_po_inr:,}")
        print(f"  • Active Dispatched Pipeline  : ₹{metrics.dispatched_pipeline_inr:,}")
        print("=" * 76)
        return

    if is_dispatch:
        is_execute = getattr(args, "execute", False)
        tier_opt = getattr(args, "tier", None)
        limit_opt = getattr(args, "limit", 10)
        touch_opt = getattr(args, "touch", 1)
        dry_run = getattr(args, "dry_run", False)

        if is_execute:
            print(f"Executing Outbound Commercial Batch (Tier: {tier_opt or 'All'}, Limit: {limit_opt}, Touch: {touch_opt}, Dry-Run: {dry_run})...")
            receipts = engine.dispatch_batch(tier=tier_opt, limit=limit_opt, touch_number=touch_opt, dry_run=dry_run)
            print("-" * 76)
            print(f"{'RECEIPT ID':<16} | {'ACCOUNT NAME':<26} | {'CHANNEL':<7} | {'STATUS':<9} | {'HASH'}")
            print("-" * 76)
            for r in receipts:
                print(f"{r.receipt_id:<16} | {r.company_name[:26]:<26} | {r.channel:<7} | {r.status:<9} | {r.verification_hash[:16]}...")
            print("-" * 76)
            print(f"[SUCCESS] Dispatched {len(receipts)} commercial touchpoints. Verified in data/outbound_audit_trail.jsonl")
            m = engine.compute_funnel_metrics()
            print(f"Dispatched Pipeline: ₹{m.dispatched_pipeline_inr:,} | Dispatched Pilot POs: ₹{m.dispatched_pilot_inr:,}")
            print("=" * 76)
            return

        dispatch_ledger_path = os.path.join(REPO_ROOT, "data", "commercial_dispatch_ledger.json")
        if os.path.exists(dispatch_ledger_path):
            with open(dispatch_ledger_path, "r", encoding="utf-8") as f:
                ledger = json.load(f)
            t1 = sum(1 for x in ledger if "tier 1" in x.get("priority_tier", "").lower())
            t2 = sum(1 for x in ledger if "tier 2" in x.get("priority_tier", "").lower())
            print(f"Dispatch Ledger Status   : STAGED_READY (Outbound Batches Primed)")
            print(f"Total Dispatches Staged  : {len(ledger)} Accounts")
            print(f"Immediate Strike (Tier 1): {t1} accounts (<24h high-conviction cadence)")
            print(f"Secondary (Tier 2)       : {t2} accounts (48h high-velocity cadence)")
            print(f"Outbound Dispatch Board  : COMMERCIAL_DISPATCH_BOARD.md")
        else:
            print(f"Dispatch ledger ready. See COMMERCIAL_DISPATCH_BOARD.md for multi-touch cadences.")
        print("=" * 76)
        return'''

# normalize CRLF for replacing
text = text.replace(old_dispatch_block.replace("\n", "\r\n"), new_dispatch_block.replace("\n", "\r\n"))
text = text.replace(old_dispatch_block, new_dispatch_block)

# 2. Update parser options for p_deals
old_p_deals = '''    # deals
    p_deals = subparsers.add_parser("deals", help="Manage 546-Account Commercial Deal Machine & Outbound Dispatch")
    p_deals.add_argument("--search", type=str, help="Search commercial accounts by name or stakeholder")
    p_deals.add_argument("--dispatch", action="store_true", help="View commercial outbound dispatch ledger")
    p_deals.add_argument("--sow", type=str, help="Inspect turnkey SOW contract for an enterprise account")
    p_deals.set_defaults(func=cmd_deals)'''

new_p_deals = '''    # deals
    p_deals = subparsers.add_parser("deals", help="Manage 546-Account Commercial Deal Machine & Outbound Dispatch")
    p_deals.add_argument("--search", type=str, help="Search commercial accounts by name or stakeholder")
    p_deals.add_argument("--dispatch", action="store_true", help="View commercial outbound dispatch ledger")
    p_deals.add_argument("--execute", action="store_true", help="Execute outbound batch dispatch with receipts")
    p_deals.add_argument("--tier", type=str, help="Target priority tier (e.g. 'Tier 1' or 'Tier 2')")
    p_deals.add_argument("--limit", type=int, default=10, help="Batch limit for dispatch (default: 10)")
    p_deals.add_argument("--touch", type=int, default=1, help="Touch sequence number (1: InMail, 2: Cold Email)")
    p_deals.add_argument("--dry-run", action="store_true", help="Execute dispatch in mock dry-run simulation mode")
    p_deals.add_argument("--funnel", action="store_true", help="Display full commercial conversion funnel")
    p_deals.add_argument("--sow", type=str, help="Inspect turnkey SOW contract for an enterprise account")
    p_deals.set_defaults(func=cmd_deals)'''

text = text.replace(old_p_deals.replace("\n", "\r\n"), new_p_deals.replace("\n", "\r\n"))
text = text.replace(old_p_deals, new_p_deals)

with open(cli_path, "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] omega_cli.py updated with dispatch execution options!")
