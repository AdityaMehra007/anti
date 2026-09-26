#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY BATCH DISPATCHER CLI & TRACKER (v8.0)
========================================================================================
Usage:
  python batch_dispatcher.py --list
  python batch_dispatcher.py --dispatch 5
  python batch_dispatcher.py --export-csv
  python batch_dispatcher.py --show ACT-0001
========================================================================================
"""
import os, sys, json, csv, argparse
from datetime import datetime

class BatchDispatcher:
    def __init__(self, state_file=None):
        if state_file is None:
            if os.path.exists(r"e:\anti\data\outreach_pipeline_state.json"):
                self.state_file = r"e:\anti\data\outreach_pipeline_state.json"
            else:
                self.state_file = r"e:\anti\outreach_pipeline_state.json"
        else:
            self.state_file = state_file
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            self.records = self.data.get("records", [])
        else:
            self.data = {"records": []}
            self.records = []

    def list_ready(self, limit=10):
        ready = [r for r in self.records if r.get("current_stage") == "DISPATCH_READY"]
        print(f"\n[FOUND {len(ready)} DISPATCH_READY CONTACTS (Showing Top {min(limit, len(ready))}):]")
        print("-" * 80)
        for r in ready[:limit]:
            print(f"ID: {r['id']} | Company: {r['company']:<20} | Contact: {r['contact_name']:<22} | Tier 1: {r.get('is_tier_1')}")
            print(f"   Subject: {r['touch_1_initial']['subject']}")
            print(f"   Message: {r['touch_1_initial']['message'][:100]}...")
            print("-" * 80)
        return ready

    def show_payload(self, action_id):
        for r in self.records:
            if r["id"].upper() == action_id.upper():
                print("=" * 80)
                print(f"OUTREACH PAYLOAD FOR: {r['contact_name']} ({r['company']}) [ID: {r['id']}]")
                print("=" * 80)
                print(f"STAGE: {r['current_stage']} | PRIORITY: {r['priority']} | TIER 1: {r.get('is_tier_1')}")
                print(f"\n>>> TOUCH 1 (DAY 0):")
                print(f"Subject: {r['touch_1_initial']['subject']}")
                print(f"Message:\n{r['touch_1_initial']['message']}")
                print(f"\n>>> TOUCH 2 (DAY +3 FOLLOW-UP):")
                print(f"Subject: {r['touch_2_proof_of_work']['subject']}")
                print(f"Message:\n{r['touch_2_proof_of_work']['message']}")
                print("=" * 80)
                return r
        print(f"[ERROR] Action ID {action_id} not found.")
        return None

    def dispatch_batch(self, count=5):
        ready = [r for r in self.records if r.get("current_stage") == "DISPATCH_READY"]
        to_dispatch = ready[:count]
        if not to_dispatch:
            print("[NO CONTACTS IN DISPATCH_READY STAGE]")
            return []
        
        now = datetime.now().isoformat()
        dispatched_ids = []
        for r in to_dispatch:
            r["current_stage"] = "SENT"
            r["last_updated"] = now
            r["touch_1_initial"]["status"] = "SENT"
            r["touch_1_initial"]["sent_at"] = now
            r["touch_2_proof_of_work"]["status"] = "ACTIVE_COUNTDOWN"
            r["history"].append({
                "timestamp": now,
                "from": "DISPATCH_READY",
                "to": "SENT",
                "note": "Dispatched via Batch Dispatcher Engine v8.0"
            })
            dispatched_ids.append(r["id"])
            print(f"[DISPATCHED] {r['id']} -> {r['contact_name']} ({r['company']})")

        counts = {}
        for r in self.records:
            st = r["current_stage"]
            counts[st] = counts.get(st, 0) + 1
        self.data["funnel_summary"]["stage_breakdown"] = counts
        self.data["exported_at"] = now

        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

        print(f"\n[SUCCESS] Successfully advanced {len(dispatched_ids)} actions to SENT. Updated state saved.")
        return dispatched_ids

    def export_csv(self, output_csv=r"e:\anti\live_outreach_tracker.csv"):
        fieldnames = ["ID", "Contact Name", "Company", "Tier 1", "Priority", "Current Stage", "Action Type", "Last Updated", "Touch 1 Subject", "Touch 1 Message"]
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in self.records:
                writer.writerow({
                    "ID": r["id"],
                    "Contact Name": r["contact_name"],
                    "Company": r["company"],
                    "Tier 1": "YES" if r.get("is_tier_1") else "NO",
                    "Priority": r["priority"],
                    "Current Stage": r["current_stage"],
                    "Action Type": r["action_type"],
                    "Last Updated": r["last_updated"],
                    "Touch 1 Subject": r["touch_1_initial"]["subject"],
                    "Touch 1 Message": r["touch_1_initial"]["message"]
                })
        print(f"[SUCCESS] Exported live tracker CSV to {output_csv}")
        return output_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Antigravity Batch Outreach Dispatcher")
    parser.add_argument("--list", action="store_true", help="List contacts ready for dispatch")
    parser.add_argument("--dispatch", type=int, default=0, help="Number of contacts to advance to SENT")
    parser.add_argument("--show", type=str, help="Show full multi-touch copy for a specific Action ID")
    parser.add_argument("--export-csv", action="store_true", help="Export live CSV tracker")
    args = parser.parse_args()

    dispatcher = BatchDispatcher()
    if args.show:
        dispatcher.show_payload(args.show)
    elif args.dispatch > 0:
        dispatcher.dispatch_batch(args.dispatch)
    elif args.export_csv:
        dispatcher.export_csv()
    else:
        dispatcher.list_ready(limit=10)
