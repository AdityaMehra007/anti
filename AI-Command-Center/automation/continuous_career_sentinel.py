"""
=============================================================================
ANTIGRAVITY OMNISYSTEM: CONTINUOUS CAREER SENTINEL & AUTONOMOUS DISPATCH LOOP
=============================================================================
Autonomous Sentinel Daemon that continuously audits, scores, optimizes,
and synchronizes the entire Antigravity Career Engine & Startup Lab Suite.

Modes:
  python continuous_career_sentinel.py --once   # Deterministic single-pass sweep
  python continuous_career_sentinel.py --loop   # Continuous autonomous monitoring
=============================================================================
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENGINE_DIR = os.path.join(BASE_DIR, "projects", "flagship-career-engine")
STARTUP_DIR = os.path.join(BASE_DIR, "startup-lab")
VAULT_PATH = os.path.join(ENGINE_DIR, "career_vault.db")

sys.path.insert(0, ENGINE_DIR)
sys.path.insert(0, STARTUP_DIR)

from career_engine import CareerVault, ScoringEngine
from rate_card_optimizer import RateCardOptimizer


class CareerSentinel:
    def __init__(self, db_path: str = VAULT_PATH):
        self.db_path = db_path
        self.cycle_count = 0

    def run_sweep(self) -> dict:
        self.cycle_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}] === SENTINEL CYCLE #{self.cycle_count} STARTING ===")

        # 1. Database Integrity & Concurrency Audit
        vault = CareerVault(self.db_path)
        cur = vault.conn.cursor()
        cur.execute("PRAGMA integrity_check;")
        integrity = cur.fetchone()[0]

        # 2. Score & Disqualification Audit
        cur.execute("SELECT id, job_id, company, title, location, experience_min, experience_max, required_skills, description, fit_score FROM jobs")
        jobs = cur.fetchall()
        total_jobs = len(jobs)
        rescore_updates = 0
        tier1_count = 0
        tier2_count = 0
        disqualified_count = 0

        for r in jobs:
            jid = r["job_id"]
            job_dict = {
                "job_id": jid,
                "company": r["company"],
                "title": r["title"],
                "location": r["location"],
                "experience_min": r["experience_min"],
                "experience_max": r["experience_max"],
                "required_skills": json.loads(r["required_skills"]) if r["required_skills"] else [],
                "description": r["description"] or ""
            }
            score, breakdown, flags = ScoringEngine.evaluate(job_dict)
            if score >= 80:
                tier1_count += 1
            elif score >= 70:
                tier2_count += 1
            if flags:
                disqualified_count += 1

            if score != r["fit_score"]:
                cur.execute(
                    "UPDATE jobs SET fit_score = ?, score_breakdown = ?, disqualification_flags = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (score, json.dumps(breakdown), json.dumps(flags), r["id"])
                )
                rescore_updates += 1

        if rescore_updates > 0:
            vault.conn.commit()

        # 3. Follow-Up Deadlines Audit
        today_str = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "SELECT COUNT(*) FROM applications WHERE follow_up_date <= ? AND outreach_status != 'FOLLOWED_UP'",
            (today_str,)
        )
        due_follow_ups = cur.fetchone()[0]

        vault.close()

        # 4. Ingest & Audit Pending Vendor Quotations in Startup Lab
        incoming_quotes_dir = os.path.join(STARTUP_DIR, "incoming_quotes")
        audits_dir = os.path.join(STARTUP_DIR, "audits")
        os.makedirs(incoming_quotes_dir, exist_ok=True)
        os.makedirs(audits_dir, exist_ok=True)

        benchmark_rates = {
            "German Tent Structure (sq ft)": 18.0,
            "JBL Line Array Sound Setup (day)": 35000.0,
            "P3 LED Video Wall (sq ft)": 120.0,
            "VIP Lounge Sofa Set (unit/day)": 1200.0,
            "Silent Generator 125 kVA (day)": 8500.0,
            "Security Marshal Deployment (shift)": 1100.0,
        }
        optimizer = RateCardOptimizer(benchmark_rates)
        quotes_audited = 0

        for q_file in os.listdir(incoming_quotes_dir):
            if q_file.endswith(".json"):
                q_path = os.path.join(incoming_quotes_dir, q_file)
                try:
                    with open(q_path, encoding="utf-8") as f:
                        q_data = json.load(f)
                    items = q_data.get("items", q_data)
                    vendor = q_data.get("vendor_name", "Vendor Partner")
                    event = q_data.get("event_name", "Bengaluru Corporate Summit 2026")
                    audit_res = optimizer.audit_quotation(items)
                    letter = optimizer.generate_counter_letter(audit_res, vendor, event)
                    
                    audit_out = os.path.join(audits_dir, f"AUDIT_{q_file}")
                    with open(audit_out, "w", encoding="utf-8") as f:
                        json.dump({"audit": audit_res, "counter_letter": letter}, f, indent=2)
                    quotes_audited += 1
                except Exception as e:
                    print(f"  [WARN] Failed to process quotation {q_file}: {e}")

        telemetry = {
            "timestamp": timestamp,
            "cycle": self.cycle_count,
            "database_integrity": integrity,
            "total_jobs_audited": total_jobs,
            "rescore_updates": rescore_updates,
            "tier1_high_fit": tier1_count,
            "tier2_potential": tier2_count,
            "disqualified_or_flagged": disqualified_count,
            "due_follow_ups": due_follow_ups,
            "vendor_quotes_audited": quotes_audited,
        }

        print(f"  [OK] Total Jobs Verified & Scored:  {total_jobs}")
        print(f"  [OK] Tier-1 High-Fit Roles (>=80):  {tier1_count}")
        print(f"  [OK] High-Potential Roles (>=70):  {tier1_count + tier2_count}")
        print(f"  [OK] Re-scored Record Updates:     {rescore_updates}")
        print(f"  [OK] Follow-up Actions Due Today:  {due_follow_ups}")
        print(f"  [OK] Vendor Quotes Processed:      {quotes_audited}")
        print(f"  [OK] Database Integrity Check:     {integrity}")

        return telemetry


def main():
    parser = argparse.ArgumentParser(description="Antigravity Continuous Career Sentinel")
    parser.add_argument("--loop", action="store_true", help="Run continuously in autonomous loop")
    parser.add_argument("--interval", type=int, default=60, help="Interval in seconds between sweeps (default: 60s)")
    parser.add_argument("--once", action="store_true", help="Execute single-pass audit sweep and exit")
    args = parser.parse_args()

    sentinel = CareerSentinel()

    if args.once or not args.loop:
        sentinel.run_sweep()
        print("\n[OK] Single-pass sentinel sweep completed successfully.")
        return 0

    print(f"[*] Starting Autonomous Sentinel Loop (Interval: {args.interval}s)...")
    print("[*] Press Ctrl+C to terminate.")
    try:
        while True:
            sentinel.run_sweep()
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[*] Sentinel loop terminated cleanly by operator.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
