"""24/7 Autonomous Background Scheduler for GLOBAL CAPITAL OS.

Manages recurring financial monitoring, anomaly scans, daily morning briefs,
and monthly closing routines.
"""

from typing import Any
from datetime import datetime
from ..agents.security_agent import security_agent
from ..agents.audit_agent import audit_agent
from ..agents.founder_chief_of_staff import founder_chief_of_staff
from ..agents.treasury_commander import treasury_commander
from ..core.audit import audit


class AutonomousScheduler:
    @staticmethod
    def run_hourly_security_pulse() -> dict[str, Any]:
        """Executes hourly anti-fraud, transaction velocity, and anomaly scans."""
        res = security_agent.scan_for_anomalies()
        audit.log_event("AutonomousScheduler", "HOURLY_PULSE_EXECUTED", res)
        return res

    @staticmethod
    def run_daily_financial_close() -> dict[str, Any]:
        """Executes daily 3-way reconciliation and generates the Morning CEO/CFO Brief."""
        recon = audit_agent.reconcile_ledger_and_bank()
        tax = treasury_commander.verify_tax_reserves()
        brief = founder_chief_of_staff.generate_daily_brief()

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "cycle": "DAILY_CLOSE",
            "reconciliation": recon,
            "tax_reserve_status": tax,
            "daily_brief": brief
        }
        audit.log_event("AutonomousScheduler", "DAILY_CLOSE_COMPLETED", report)
        return report


scheduler = AutonomousScheduler()
