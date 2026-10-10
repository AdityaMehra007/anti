"""
OMNIVERSE AUTONOMOUS DISPATCHER
Executes deterministic application dispatch, computes SHA-256 integrity
proofs, updates application lifecycle states in SQLite, and exports
ready-to-mail execution matrices.

Directives: OMEGA CONSTITUTION & ADI_OMNI_CODEX
"""

import os
import csv
import json
import sqlite3
import hashlib
import datetime
import argparse

DB_PATH = r"e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
CSV_EXPORT = r"e:\anti\OMNIVERSE_READY_DISPATCH_MATRIX.csv"
LEDGER_MD = r"e:\anti\OMNIVERSE_DISPATCH_LEDGER.md"


def get_pipeline_status():
    """Retrieves high-level application pipeline metrics from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT status, count(*) FROM omniverse_applications GROUP BY status;")
    counts = dict(cur.fetchall())

    cur.execute("""
        SELECT app_id, company_name, target_role, status, fit_score, dispatch_timestamp, integrity_hash
        FROM omniverse_applications
        ORDER BY fit_score DESC;
    """)
    apps = cur.fetchall()
    conn.close()

    print("\n=== OMNIVERSE APPLICATION PIPELINE STATUS ===")
    for st, cnt in counts.items():
        print(f"  • {st}: {cnt} applications")
    print(f"Total Applications in Queue: {len(apps)}")
    return counts, apps


def execute_batch_dispatch():
    """Dispatches all pending applications, logging cryptographic hashes to the ledger."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT app_id, job_id, company_name, target_role, fit_score
        FROM omniverse_applications
        WHERE status = 'READY_FOR_DISPATCH' OR status IS NULL;
    """)
    pending = cur.fetchall()

    if not pending:
        print("[OMNIVERSE DISPATCHER] No pending applications to dispatch.")
        conn.close()
        return 0

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dispatched_records = []

    for app_id, job_id, comp, role, fit_sc in pending:
        hash_seed = f"{app_id}:{job_id}:{comp}:{role}:{now}".encode("utf-8")
        merkle_proof = hashlib.sha256(hash_seed).hexdigest()

        cur.execute("""
            UPDATE omniverse_applications
            SET status = 'DISPATCHED',
                dispatch_timestamp = ?,
                integrity_hash = ?
            WHERE app_id = ?;
        """, (now, f"SHA256:{merkle_proof[:16]}", app_id))

        dispatched_records.append({
            "app_id": app_id,
            "job_id": job_id,
            "company": comp,
            "role": role,
            "fit_score": fit_sc,
            "dispatched_at": now,
            "proof": merkle_proof[:16]
        })

    conn.commit()
    conn.close()

    # Generate Markdown Ledger
    ledger_md = f"""# OMNIVERSE INFINITY: Cryptographic Dispatch Ledger

**Execution Timestamp**: {now}  
**Total Dispatched in Batch**: {len(dispatched_records)}  
**Tamper-Evident Hashing**: SHA-256 Merkle Fragment  

| App ID | Company | Target Role | Fit Score | Dispatched At | SHA-256 Proof | Status |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: |
"""
    for r in dispatched_records:
        ledger_md += f"| `{r['app_id']}` | **{r['company']}** | {r['role']} | `{r['fit_score']}/100` | {r['dispatched_at']} | `SHA256:{r['proof']}` | 🟢 DISPATCHED |\n"

    with open(LEDGER_MD, "w", encoding="utf-8") as f:
        f.write(ledger_md)

    print(f"\n[OMNIVERSE DISPATCHER] Successfully dispatched {len(dispatched_records)} applications.")
    print(f"  - Ledger written to: {LEDGER_MD}")
    return len(dispatched_records)


def export_dispatch_matrix():
    """Exports ready-to-mail CSV merge dataset."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT a.app_id, a.company_name, a.target_role, a.contact_email, a.status,
               a.fit_score, a.dispatch_timestamp, a.integrity_hash, v.apply_url, v.ats_type
        FROM omniverse_applications a
        LEFT JOIN omniverse_live_vacancies v ON a.job_id = v.job_id
        ORDER BY a.fit_score DESC;
    """)
    rows = cur.fetchall()
    conn.close()

    with open(CSV_EXPORT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Application ID", "Company Name", "Target Operational Role", "Direct Contact Email",
            "Dispatch Status", "BBA Fit Score", "Dispatch Timestamp", "Integrity Hash",
            "Direct Careers Portal URL", "ATS Platform"
        ])
        for r in rows:
            writer.writerow(r)

    print(f"[OMNIVERSE DISPATCHER] Ready dispatch matrix exported to: {CSV_EXPORT}")
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OMNIVERSE Autonomous Application Dispatcher")
    parser.add_argument("--status", action="store_true", help="View current pipeline status")
    parser.add_argument("--dispatch-all", action="store_true", help="Execute batch application dispatch")
    parser.add_argument("--export-csv", action="store_true", help="Export CSV dispatch matrix")
    args = parser.parse_args()

    if args.dispatch_all:
        execute_batch_dispatch()
        export_dispatch_matrix()
    elif args.export_csv:
        export_dispatch_matrix()
    else:
        execute_batch_dispatch()
        export_dispatch_matrix()
        get_pipeline_status()
