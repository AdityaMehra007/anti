#!/usr/bin/env python3
"""
========================================================================================
OMEGA TARGET 300 JOB STRIKE DISPATCH QUEUE RUNNER
========================================================================================
Progressively advances staged strike applications through verified lifecycle states:
  STAGED_READY_FOR_DISPATCH -> TOUCH1_STAGED -> TOUCH1_DISPATCHED -> TOUCH2_SCHEDULED
Maintains cryptographic SHA-256 audit hashes in data/outreach_tracker.db.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import sqlite3
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
OUTREACH_DB = DATA_DIR / "outreach_tracker.db"
DOSSIERS_DIR = ROOT_DIR / "applications_generated" / "target_300_job_strike"

def init_tables(conn: sqlite3.Connection):
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS strike_300_dossiers (
                target_id TEXT PRIMARY KEY,
                company TEXT,
                job_title TEXT,
                contact_name TEXT,
                opportunity_score REAL,
                priority TEXT,
                dossier_path TEXT,
                proof_hash TEXT,
                status TEXT,
                staged_at TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS strike_300_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id TEXT,
                event_type TEXT,
                previous_status TEXT,
                new_status TEXT,
                timestamp TEXT,
                proof_hash TEXT
            )
        """)
        conn.commit()
    finally:
        cur.close()

def run_dispatch_cycle(batch_size: int = 10, dry_run: bool = False) -> dict:
    """Advances up to `batch_size` staged dossiers to the next lifecycle stage."""
    if not OUTREACH_DB.exists():
        return {"status": "error", "message": "outreach_tracker.db not found"}

    conn = sqlite3.connect(str(OUTREACH_DB))
    try:
        init_tables(conn)
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT target_id, company, job_title, contact_name, status, dossier_path, proof_hash
                FROM strike_300_dossiers
                WHERE status = 'STAGED_READY_FOR_DISPATCH'
                ORDER BY opportunity_score DESC, target_id ASC
                LIMIT ?
            """, (batch_size,))

            rows = cur.fetchall()
            now_iso = datetime.now(timezone.utc).isoformat()
            advanced = []

            for r in rows:
                target_id, company, role, contact, status, dossier_path, old_hash = r
                new_status = "TOUCH1_DISPATCHED"

                event_payload = {
                    "target_id": target_id,
                    "company": company,
                    "role": role,
                    "contact": contact,
                    "previous_status": status,
                    "new_status": new_status,
                    "timestamp": now_iso
                }
                event_hash = "sha256:" + hashlib.sha256(json.dumps(event_payload, sort_keys=True).encode()).hexdigest()

                if not dry_run:
                    cur.execute("""
                        UPDATE strike_300_dossiers
                        SET status = ?, proof_hash = ?
                        WHERE target_id = ?
                    """, (new_status, event_hash, target_id))

                    cur.execute("""
                        INSERT INTO strike_300_events 
                        (target_id, event_type, previous_status, new_status, timestamp, proof_hash)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (target_id, "STATUS_ADVANCED", status, new_status, now_iso, event_hash))

                advanced.append({
                    "target_id": target_id,
                    "company": company,
                    "contact": contact,
                    "new_status": new_status,
                    "proof_hash": event_hash
                })

            if not dry_run:
                conn.commit()

            # Get summary counts
            cur.execute("SELECT status, COUNT(*) FROM strike_300_dossiers GROUP BY status")
            counts = dict(cur.fetchall())
            return {
                "status": "success",
                "processed": len(advanced),
                "advanced_targets": advanced,
                "current_counts": counts,
                "dry_run": dry_run
            }
        finally:
            cur.close()
    finally:
        conn.close()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Target 300 Job Strike Dispatch Queue Runner")
    parser.add_argument("--batch", type=int, default=15, help="Number of applications to advance")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without database modification")
    parser.add_argument("--status", action="store_true", help="Show current queue status breakdown")
    args = parser.parse_args()

    conn = sqlite3.connect(str(OUTREACH_DB))
    init_tables(conn)
    cur = conn.cursor()

    if args.status:
        cur.execute("SELECT status, COUNT(*) FROM strike_300_dossiers GROUP BY status")
        rows = cur.fetchall()
        print("\n=== TARGET 300 JOB STRIKE STATUS BREAKDOWN ===")
        for s, c in rows:
            print(f"  {s:<30}: {c} targets")
        conn.close()
        return

    result = run_dispatch_cycle(batch_size=args.batch, dry_run=args.dry_run)
    print(f"\n[+] Executed Target 300 Dispatch Cycle:")
    print(f"    Processed: {result['processed']} targets")
    print(f"    Current Ledger Breakdown: {result['current_counts']}")
    for t in result["advanced_targets"][:5]:
        print(f"    -> {t['target_id']}: {t['company']} ({t['contact']}) => {t['new_status']}")
    if len(result["advanced_targets"]) > 5:
        print(f"    ... and {len(result['advanced_targets']) - 5} more.")

if __name__ == "__main__":
    main()
