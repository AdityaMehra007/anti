#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA — Automated HR 1,781 Outreach Orchestrator & Funnel Tracker
Manages daily outreach batches, follow-up cadences, and conversion analytics.
Zero external dependencies (pure Python standard library).
"""

import os
import sys
import csv
import json
import sqlite3
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_DB = os.path.join(REPO_ROOT, "data", "outreach_tracker.db")
DEFAULT_CSV = os.path.join(REPO_ROOT, "ALL_1781_HR_CONTACTS_MASTER.csv")

class HROutreachOrchestrator:
    def __init__(self, db_path: str = DEFAULT_DB, csv_path: str = DEFAULT_CSV):
        self.db_path = db_path
        self.csv_path = csv_path
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        self.init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS outreach_cadence (
                    contact_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    company TEXT,
                    position TEXT,
                    linkedin_url TEXT,
                    email TEXT,
                    status TEXT NOT NULL,
                    staged_at TEXT,
                    sent_at TEXT,
                    next_followup_at TEXT,
                    notes TEXT
                )
            """)
            conn.commit()

    def generate_daily_batch(self, batch_size: int = 25) -> List[Dict[str, Any]]:
        """Selects up to batch_size unprocessed contacts from the master CSV and stages them."""
        if not os.path.exists(self.csv_path):
            return []

        # Find already staged or processed IDs
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT contact_id FROM outreach_cadence")
            existing_ids = {row["contact_id"] for row in cur.fetchall()}

        staged_batch = []
        now = datetime.now().isoformat()
        followup_date = (datetime.now() + timedelta(days=3)).isoformat()

        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cid = str(row.get("id", ""))
                if not cid or cid in existing_ids:
                    continue

                contact_name = row.get("name", "Talent Leader")
                company = row.get("company", "Enterprise")
                position = row.get("position", "HR / Talent")
                linkedin = row.get("linkedin_url", "")
                email = row.get("email", "")

                staged_batch.append({
                    "contact_id": cid,
                    "name": contact_name,
                    "company": company,
                    "position": position,
                    "linkedin_url": linkedin,
                    "email": email,
                    "status": "STAGED",
                    "staged_at": now,
                    "next_followup_at": followup_date,
                    "notes": f"Staged for daily outreach batch."
                })

                if len(staged_batch) >= batch_size:
                    break

        if staged_batch:
            with self._get_connection() as conn:
                for item in staged_batch:
                    conn.execute("""
                        INSERT OR REPLACE INTO outreach_cadence 
                        (contact_id, name, company, position, linkedin_url, email, status, staged_at, next_followup_at, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        item["contact_id"], item["name"], item["company"], item["position"],
                        item["linkedin_url"], item["email"], item["status"], item["staged_at"],
                        item["next_followup_at"], item["notes"]
                    ))
                conn.commit()

        return staged_batch

    def update_contact_status(self, contact_id: str, new_status: str, notes: Optional[str] = None):
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            if new_status == "SENT":
                followup = (datetime.now() + timedelta(days=3)).isoformat()
                conn.execute("""
                    UPDATE outreach_cadence 
                    SET status = ?, sent_at = ?, next_followup_at = ?, notes = COALESCE(?, notes)
                    WHERE contact_id = ?
                """, (new_status, now, followup, notes, str(contact_id)))
            else:
                conn.execute("""
                    UPDATE outreach_cadence 
                    SET status = ?, notes = COALESCE(?, notes)
                    WHERE contact_id = ?
                """, (new_status, notes, str(contact_id)))
            conn.commit()

    def get_contact_status(self, contact_id: str) -> Optional[str]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT status FROM outreach_cadence WHERE contact_id = ?", (str(contact_id),))
            row = cur.fetchone()
            return row["status"] if row else None

    def get_funnel_stats(self) -> Dict[str, int]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT status, COUNT(*) as count FROM outreach_cadence GROUP BY status")
            rows = cur.fetchall()
            stats = {
                "total_staged": 0,
                "staged": 0,
                "sent": 0,
                "followup": 0,
                "replied": 0,
                "scheduled": 0
            }
            for r in rows:
                s = r["status"].lower()
                c = r["count"]
                stats["total_staged"] += c
                if s == "staged":
                    stats["staged"] += c
                elif s == "sent":
                    stats["sent"] += c
                elif "followup" in s:
                    stats["followup"] += c
                elif s == "replied":
                    stats["replied"] += c
                elif s == "scheduled":
                    stats["scheduled"] += c

            return stats

def main():
    parser = argparse.ArgumentParser(description="HR 1,781 Outreach Orchestrator")
    parser.add_argument("--batch", type=int, default=0, help="Generate a daily batch of N contacts")
    parser.add_argument("--stats", action="store_true", help="Print funnel analytics")
    parser.add_argument("--mark-sent", type=str, help="Mark contact ID as SENT")
    parser.add_argument("--mark-reply", type=str, help="Mark contact ID as REPLIED")
    args = parser.parse_args()

    orchestrator = HROutreachOrchestrator()

    if args.batch > 0:
        batch = orchestrator.generate_daily_batch(args.batch)
        print(f"[+] Successfully staged {len(batch)} contacts for outreach.")
        for item in batch[:5]:
            print(f"    - [{item['contact_id']}] {item['name']} ({item['position']}) @ {item['company'] or 'Enterprise'}")
        if len(batch) > 5:
            print(f"    ... and {len(batch) - 5} more.")

    if args.mark_sent:
        orchestrator.update_contact_status(args.mark_sent, "SENT")
        print(f"[+] Contact {args.mark_sent} marked as SENT.")

    if args.mark_reply:
        orchestrator.update_contact_status(args.mark_reply, "REPLIED")
        print(f"[+] Contact {args.mark_reply} marked as REPLIED.")

    if args.stats or len(sys.argv) == 1:
        stats = orchestrator.get_funnel_stats()
        print("\n=======================================================")
        print("     HR 1,781 STRIKE FORCE — LIVE OUTREACH FUNNEL      ")
        print("=======================================================")
        print(f"  Staged for Today:  {stats['staged']}")
        print(f"  Sent:              {stats['sent']}")
        print(f"  In Follow-Up:      {stats['followup']}")
        print(f"  Responses:         {stats['replied']}")
        print(f"  Interviews Booked: {stats['scheduled']}")
        print("=======================================================\n")

if __name__ == "__main__":
    main()
