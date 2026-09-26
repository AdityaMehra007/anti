"""
VECTIS TRADE — Autonomous Hot-Folder Watcher Daemon
Monitors company/inbox/ -> audits via VectisComplianceEngine -> writes certificates to company/outbox/.
"""

import json
import os
import shutil
import time
from datetime import datetime, timezone
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from vectis_core import VectisComplianceEngine
from vectis_parser import parse_docket_dict

INBOX_DIR = os.path.join(BASE_DIR, "inbox")
PROCESSING_DIR = os.path.join(BASE_DIR, "processing")
OUTBOX_DIR = os.path.join(BASE_DIR, "outbox")
LOG_FILE = os.path.join(BASE_DIR, "logs", "agent_ops.jsonl")

os.makedirs(INBOX_DIR, exist_ok=True)
os.makedirs(PROCESSING_DIR, exist_ok=True)
os.makedirs(OUTBOX_DIR, exist_ok=True)

def process_file(filename: str) -> bool:
    src_path = os.path.join(INBOX_DIR, filename)
    proc_path = os.path.join(PROCESSING_DIR, filename)

    try:
        shutil.move(src_path, proc_path)
    except Exception as e:
        print(f"[DAEMON] Failed to move {filename} to processing: {e}")
        return False

    print(f"[DAEMON] Ingesting trade docket: {filename} ...")
    try:
        with open(proc_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        lc, invoice, pl, bl, coo = parse_docket_dict(data)
        engine = VectisComplianceEngine()
        result = engine.audit_trade_docket(lc, invoice, pl, bl, coo)

        base_name = os.path.splitext(filename)[0]
        json_out = os.path.join(OUTBOX_DIR, f"{base_name}_audit_result.json")
        cert_out = os.path.join(OUTBOX_DIR, f"{base_name}_certificate.md")

        result_dict = {
            "docket_id": result.docket_id,
            "timestamp": result.timestamp,
            "status": result.status,
            "discrepancy_count": result.discrepancy_count,
            "fatal_discrepancies": result.fatal_discrepancies,
            "sha256_hash": result.sha256_hash,
            "docket_summary": result.docket_summary,
            "discrepancies": [
                {
                    "code": d.code,
                    "rule_reference": d.rule_reference,
                    "severity": d.severity,
                    "affected_document": d.affected_document,
                    "field_name": d.field_name,
                    "description": d.description,
                    "correction_suggestion": d.correction_suggestion
                }
                for d in result.discrepancies
            ]
        }

        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2)

        md_cert = engine.format_markdown_certificate(result)
        with open(cert_out, "w", encoding="utf-8") as f:
            f.write(md_cert)

        # Log to immutable agent ledger
        event = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "agent": "VECTIS_AUTONOMOUS_DAEMON",
            "permission_level": "EXECUTE",
            "action": f"Audited Trade Docket: {filename}",
            "result": {
                "docket_id": result.docket_id,
                "status": result.status,
                "fatal_discrepancies": result.fatal_discrepancies,
                "certificate_path": cert_out
            }
        }
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

        print(f"[DAEMON] Finished {filename} -> Status: {result.status} (Fatal: {result.fatal_discrepancies})")
        print(f"         Certificate deposited: {cert_out}")

        os.remove(proc_path)
        return True

    except Exception as e:
        print(f"[DAEMON ERROR] Failed processing {filename}: {e}")
        # Keep in processing for debug
        return False

def run_single_pass() -> int:
    files = [f for f in os.listdir(INBOX_DIR) if f.endswith(".json")]
    processed_count = 0
    for f in files:
        if process_file(f):
            processed_count += 1
    return processed_count

def start_daemon(poll_interval=2):
    print("=== VECTIS AUTONOMOUS HOT-FOLDER DAEMON STARTED ===")
    print(f"Monitoring: {INBOX_DIR} -> Processing -> Output: {OUTBOX_DIR}")
    print("Press Ctrl+C to stop.")
    try:
        while True:
            run_single_pass()
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("\n[DAEMON] Stopping hot-folder daemon.")

if __name__ == "__main__":
    start_daemon()
