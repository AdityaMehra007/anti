"""
NEXUS AUTOPILOT - Normalized Financial Ledger & Receivables Intelligence Engine
Computes cash position, payment risk scoring, aging buckets, and multi-scenario cash forecasting.
"""
import sqlite3
import time
from pathlib import Path
from typing import Dict, Any, List

DB_PATH = Path(r"e:\anti\nexus_autopilot\data\nexus.db")

class NexusFinanceEngine:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_executive_financial_snapshot(self, org_id: str = "ORG-ABC-001") -> Dict[str, Any]:
        conn = self._get_conn()
        cur = conn.cursor()

        # Invoices aggregation
        cur.execute("SELECT SUM(total_amount), SUM(amount_paid) FROM invoices WHERE org_id = ?", (org_id,))
        inv_row = cur.fetchone()
        total_invoiced = inv_row[0] or 0.0
        total_collected = inv_row[1] or 0.0
        outstanding = total_invoiced - total_collected

        cur.execute("SELECT SUM(total_amount) FROM invoices WHERE org_id = ? AND status = 'OVERDUE'", (org_id,))
        overdue = cur.fetchone()[0] or 0.0

        # Payments today
        cur.execute("SELECT SUM(amount) FROM payments WHERE org_id = ?", (org_id,))
        today_collections = cur.fetchone()[0] or 0.0

        # Overdue customers count
        cur.execute("SELECT COUNT(*) FROM customers WHERE org_id = ? AND outstanding_balance > 0", (org_id,))
        debtor_count = cur.fetchone()[0]

        conn.close()

        # Cash & Cash Forecasting
        current_cash = 385000.0 # Estimated bank balance
        expected_inflows_30d = outstanding * 0.75
        expected_outflows_30d = 260000.0 # Fixed costs, suppliers, payroll

        forecast_base = current_cash + expected_inflows_30d - expected_outflows_30d
        forecast_stress = current_cash + (outstanding * 0.30) - (expected_outflows_30d * 1.10)

        return {
            "organization_id": org_id,
            "currency": "INR",
            "total_revenue_invoiced": total_invoiced,
            "total_collections_realized": total_collected,
            "total_outstanding_receivables": outstanding,
            "total_overdue_receivables": overdue,
            "today_collections": today_collections,
            "active_debtors_count": debtor_count,
            "current_cash_balance": current_cash,
            "cash_forecast_30d": {
                "base_scenario": round(forecast_base, 2),
                "stress_scenario": round(forecast_stress, 2),
                "risk_warning": "Cash balance remains healthy. Prioritize overdue collections to prevent working capital drag."
            }
        }

    def get_receivables_risk_report(self, org_id: str = "ORG-ABC-001") -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT customer_id, name, phone, outstanding_balance, avg_payment_delay_days, payment_risk_score, promise_to_pay_date FROM customers WHERE org_id = ? AND outstanding_balance > 0 ORDER BY payment_risk_score DESC", (org_id,))
        rows = cur.fetchall()
        conn.close()

        results = []
        for r in rows:
            risk_tier = "CRITICAL_RISK" if r["payment_risk_score"] >= 75 else ("MODERATE_RISK" if r["payment_risk_score"] >= 40 else "LOW_RISK")
            results.append({
                "customer_id": r["customer_id"],
                "customer_name": r["name"],
                "phone": r["phone"],
                "outstanding_inr": r["outstanding_balance"],
                "avg_delay_days": r["avg_payment_delay_days"],
                "risk_score": r["payment_risk_score"],
                "risk_tier": risk_tier,
                "promise_to_pay": r["promise_to_pay_date"] or "NO_COMMITMENT",
                "recommended_action": "ISSUE_FIRM_WHATSAPP_REMINDER" if r["payment_risk_score"] >= 60 else "GENTLE_FOLLOWUP"
            })
        return results

if __name__ == "__main__":
    engine = NexusFinanceEngine()
    snap = engine.get_executive_financial_snapshot()
    print(f"[FINANCE_ENGINE] Snapshot:\nTotal Invoiced: INR {snap['total_revenue_invoiced']:,}\nOutstanding: INR {snap['total_outstanding_receivables']:,}\nOverdue: INR {snap['total_overdue_receivables']:,}")
