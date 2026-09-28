"""
OMEGA INFINITY (Ω-OS) — CONTINUOUS SOVEREIGN AUTOPILOT DAEMON
Background service executing:
1. Hot-Folder Trade Docket Ingestion (company/inbox/ -> company/outbox/)
2. 12-Agent Swarm Heartbeat & Telemetry Synchronization
3. Cryptographic Ledger Chain Integrity Validation
4. Executive Alert Dispatch
"""

import os
import sys
import time
import json
import glob
import shutil
import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import get_kernel
from omega_infinity.omega_vectis_adapter import VectisEnterpriseAdapter
from omega_infinity.omega_swarm_matrix import SwarmMatrix
from omega_infinity.omega_notifier import SovereignNotifier


class SovereignDaemon:
    """
    Continuous background autopilot for OMEGA INFINITY.
    """

    def __init__(self, poll_interval: float = 3.0):
        self.poll_interval = poll_interval
        self.kernel = get_kernel()
        self.adapter = VectisEnterpriseAdapter()
        self.swarm = SwarmMatrix()
        self.notifier = SovereignNotifier()

        self.inbox_dir = os.path.join(REPO_ROOT, "company", "inbox")
        self.outbox_dir = os.path.join(REPO_ROOT, "company", "outbox")
        self.processing_dir = os.path.join(REPO_ROOT, "company", "processing")

        os.makedirs(self.inbox_dir, exist_ok=True)
        os.makedirs(self.outbox_dir, exist_ok=True)
        os.makedirs(self.processing_dir, exist_ok=True)

        self.running = False
        self.iteration = 0

    def process_inbox_once(self) -> int:
        """Processes any pending JSON dockets in inbox."""
        files = glob.glob(os.path.join(self.inbox_dir, "*.json"))
        processed_count = 0

        for fpath in files:
            fname = os.path.basename(fpath)
            proc_path = os.path.join(self.processing_dir, fname)

            try:
                # Atomic move to processing
                shutil.move(fpath, proc_path)

                with open(proc_path, "r", encoding="utf-8") as f:
                    docket_data = json.load(f)

                # Run UCP 600 audit
                audit_res = self.adapter.audit_docket(docket_data)

                # Deposit result in outbox
                base_name = os.path.splitext(fname)[0]
                out_json = os.path.join(self.outbox_dir, f"{base_name}_audit_result.json")
                out_cert = os.path.join(self.outbox_dir, f"{base_name}_certificate.md")

                with open(out_json, "w", encoding="utf-8") as f:
                    json.dump(audit_res, f, indent=2)

                # Write markdown certificate
                cert_content = f"""# VECTIS TRADE COMPLIANCE AUDIT CERTIFICATE
**Docket ID**: `{audit_res.get('docket_id')}`  
**Status**: `{'PASSED' if audit_res.get('passed') else 'DISCREPANCIES DETECTED'}`  
**Discrepancy Count**: `{audit_res.get('discrepancy_count')}` (Fatal: `{audit_res.get('fatal_count')}`)  
**SHA-256 SEAL**: `{audit_res.get('certificate_seal')}`  
**Timestamp**: `{audit_res.get('audit_timestamp')}`  

---

### Discrepancy Findings
"""
                for d in audit_res.get("discrepancies", []):
                    cert_content += f"- **[{d['severity']}] {d['code']} ({d['rule']})**: {d['description']}\n  - *Remediation*: {d['remediation']}\n"

                with open(out_cert, "w", encoding="utf-8") as f:
                    f.write(cert_content)

                # Clean up processing
                if os.path.exists(proc_path):
                    os.remove(proc_path)

                processed_count += 1
                self.notifier.notify_trade_discrepancy(
                    docket_id=audit_res.get("docket_id", fname),
                    discrepancies=audit_res.get("discrepancies", [])
                )
            except Exception as e:
                print(f"[DAEMON ERROR] Failed to process {fname}: {e}")
                if os.path.exists(proc_path):
                    os.remove(proc_path)

        return processed_count

    def step(self):
        """Single loop step."""
        self.iteration += 1

        # 1. Process Inbox Dockets
        processed = self.process_inbox_once()

        # 2. Every 10 iterations, verify ledger chain
        if self.iteration % 10 == 0:
            v = self.kernel.ledger.verify_integrity()
            if not v["valid"]:
                self.notifier.dispatch_alert(
                    level="CRITICAL",
                    title="Ledger Integrity Alert",
                    message=f"Cryptographic chain issue: {v.get('reason')}"
                )

        # 3. Every 20 iterations, execute a swarm heartbeat
        if self.iteration % 20 == 0:
            self.swarm.run_full_swarm_cycle()

    def run_forever(self):
        self.running = True
        print(f"\n=======================================================")
        print(f"  OMEGA INFINITY (Ω-OS) AUTONOMOUS DAEMON ACTIVE")
        print(f"  Monitoring: company/inbox/ -> company/outbox/")
        print(f"  Poll Interval: {self.poll_interval}s")
        print(f"=======================================================\n")

        try:
            while self.running:
                self.step()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            print("\n[Ω-OS DAEMON] Autopilot gracefully terminated.")


def start_daemon(poll_interval: float = 3.0):
    daemon = SovereignDaemon(poll_interval=poll_interval)
    daemon.run_forever()


if __name__ == "__main__":
    start_daemon()
