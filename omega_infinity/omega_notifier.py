"""
OMEGA INFINITY (Ω-OS) — SOVEREIGN NOTIFIER & ALERT DISPATCHER
Handles real-time executive alerts, terminal chimes, webhook notifications,
and event broadcasting for trade discrepancies, high-affinity leads, and system events.
"""

import os
import sys
import json
import time
import datetime
from typing import Dict, Any, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import get_kernel


class SovereignNotifier:
    """
    Alert and notification router for executive priority events.
    """

    def __init__(self):
        self.kernel = get_kernel()
        self.alert_history: List[Dict[str, Any]] = []

    def dispatch_alert(self, level: str, title: str, message: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Dispatches an executive alert across terminal, kernel ledger, and event history.
        Levels: INFO, SUCCESS, WARNING, CRITICAL
        """
        payload = payload or {}
        alert = {
            "id": f"ALERT-{int(time.time() * 1000)}",
            "timestamp": datetime.datetime.now().isoformat(),
            "level": level.upper(),
            "title": title,
            "message": message,
            "payload": payload
        }
        self.alert_history.append(alert)

        # Record in cryptographic ledger
        self.kernel.dispatch_event(
            event_name=f"ALERT_{alert['level']}",
            actor="SOVEREIGN_NOTIFIER",
            data=alert
        )

        # Formatted console output
        prefix = {
            "INFO": "ℹ️ [INFO]",
            "SUCCESS": "🟢 [SUCCESS]",
            "WARNING": "⚠️ [WARNING]",
            "CRITICAL": "🚨 [CRITICAL]"
        }.get(alert["level"], "🔔 [ALERT]")

        print(f"\n{prefix} {title}")
        print(f"   {message}")
        if payload:
            print(f"   Details: {json.dumps(payload, indent=2)}")

        return alert

    def notify_trade_discrepancy(self, docket_id: str, discrepancies: List[Dict[str, Any]]):
        fatal = [d for d in discrepancies if d.get("severity") == "FATAL"]
        if fatal:
            self.dispatch_alert(
                level="CRITICAL",
                title=f"Trade Finance Discrepancies Detected ({len(fatal)} Fatal)",
                message=f"Docket {docket_id} failed ICC UCP 600 validation. Export presentation blocked.",
                payload={"fatal_count": len(fatal), "rules_violated": [d.get("rule") for d in fatal]}
            )
        else:
            self.dispatch_alert(
                level="SUCCESS",
                title="Trade Docket Passed Clean",
                message=f"Docket {docket_id} verified under UCP 600 / ISBP 745. Ready for banking presentation.",
                payload={"docket_id": docket_id}
            )

    def notify_lead_match(self, lead_name: str, company: str, role: str):
        self.dispatch_alert(
            level="SUCCESS",
            title=f"High-Affinity Lead Identified: {lead_name}",
            message=f"{lead_name} ({role} at {company}) matches export decision-maker criteria.",
            payload={"lead": lead_name, "company": company, "role": role}
        )
