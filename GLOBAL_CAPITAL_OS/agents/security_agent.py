"""Security Agent - Anti-Fraud & Account Protection Sentinel.

Monitors financial velocity, detects account takeover indicators,
duplicate invoice scams, and enforces the emergency freeze mechanism.
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.config import settings
from ..core.models import ActionTier, RiskLevel
from ..core.security import security
from ..core.database import db


class SecurityAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="SecurityAgent",
            role_description="Financial systems security officer guarding against fraud, account takeovers, credential leakage, and unauthorized money movement."
        )

    def scan_for_anomalies(self) -> dict[str, Any]:
        """Scans recent transactions and approval requests for fraud or security anomalies."""
        self.check_permission(ActionTier.ANALYZE)
        anomalies = []

        with db.get_connection() as conn:
            cur = conn.cursor()
            # 1. Check for duplicate invoices/transactions (same counterparty & amount within 24 hours)
            cur.execute("""
                SELECT counterparty_name, amount, COUNT(*) as cnt
                FROM transactions
                WHERE timestamp >= datetime('now', '-24 hours')
                GROUP BY counterparty_name, amount
                HAVING cnt > 1
            """)
            dups = cur.fetchall()
            for d in dups:
                anomalies.append({
                    "type": "DUPLICATE_TRANSACTION_PATTERN",
                    "severity": "HIGH",
                    "details": f"Found {d['cnt']} identical transactions for {d['counterparty_name']} ({d['amount']}) in 24 hours."
                })

            # 2. Check daily transaction velocity against daily spending limits
            cur.execute("""
                SELECT COALESCE(SUM(amount_inr), 0.0) FROM transactions
                WHERE timestamp >= datetime('now', '-24 hours')
                AND category NOT IN ('REVENUE_CUSTOMER', 'REVENUE_PILOT', 'TRANSFER_INTERNAL')
            """)
            daily_outflow_inr = float(cur.fetchone()[0])
            if daily_outflow_inr > settings.DAILY_TRANSACTION_LIMIT_INR:
                anomalies.append({
                    "type": "DAILY_VELOCITY_LIMIT_EXCEEDED",
                    "severity": "CRITICAL",
                    "details": f"24-hour outflow ₹{daily_outflow_inr:,.2f} exceeded limit of ₹{settings.DAILY_TRANSACTION_LIMIT_INR:,.2f}."
                })

        is_threat_detected = len(anomalies) > 0
        if any(a["severity"] == "CRITICAL" for a in anomalies):
            security.trigger_emergency_freeze("Automatic freeze triggered by SecurityAgent: Critical transaction velocity limit breach.")

        report = {
            "threat_detected": is_threat_detected,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "system_frozen": security.is_system_frozen()
        }
        self.log_action("SECURITY_ANOMALY_SCAN_COMPLETED", report)
        return report

    def emergency_freeze(self, reason: str) -> dict[str, Any]:
        """Manually triggers emergency freeze on demand."""
        self.check_permission(ActionTier.RECOMMEND)
        return security.trigger_emergency_freeze(reason, triggered_by=self.agent_name)


security_agent = SecurityAgent()
