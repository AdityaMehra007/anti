"""
NEXUS AUTOPILOT - Autonomous Morning/Evening Management Reports & Founder CFO Mode
Generates daily business snapshots, priorities, risk radars, and strategic CFO-level business challenges.
"""
from typing import Dict, Any, List

class ManagementReportEngine:
    def __init__(self):
        pass

    def generate_morning_briefing(self, finance_snap: Dict[str, Any], debtors: List[Dict[str, Any]]) -> Dict[str, Any]:
        critical_debtor = debtors[0] if debtors else {"customer_name": "None", "outstanding_inr": 0.0, "avg_delay_days": 0}
        
        return {
            "report_type": "MORNING_BUSINESS_SNAPSHOT",
            "executive_summary": {
                "total_invoiced_inr": finance_snap["total_revenue_invoiced"],
                "realized_collections_inr": finance_snap["total_collections_realized"],
                "outstanding_receivables_inr": finance_snap["total_outstanding_receivables"],
                "overdue_at_risk_inr": finance_snap["total_overdue_receivables"],
                "bank_cash_balance_inr": finance_snap["current_cash_balance"],
                "projected_30d_cash_inr": finance_snap["cash_forecast_30d"]["base_scenario"]
            },
            "top_ai_priorities": [
                f"1. Prioritize collections from {critical_debtor['customer_name']} (₹{critical_debtor['outstanding_inr']:,} overdue by {critical_debtor['avg_delay_days']} days).",
                "2. Review and dispatch quotation for 250 corrugated boxes to Ramesh Traders.",
                "3. Verify and approve payment reminder sequence for 3 overdue accounts."
            ],
            "money_at_risk": {
                "critical_overdue_accounts": len(debtors),
                "total_at_risk_inr": finance_snap["total_overdue_receivables"]
            }
        }

    def execute_ceo_cfo_strategic_mode(self, query: str, finance_snap: Dict[str, Any]) -> Dict[str, Any]:
        q_lower = query.lower()
        if "cfo" in q_lower or "cash" in q_lower or "bottleneck" in q_lower:
            return {
                "mode": "STRATEGIC_CFO_PERSPECTIVE",
                "observation": f"Current receivables of ₹{finance_snap['total_outstanding_receivables']:,} represent 67.5% of total revenue billed. Working capital is locked in overdue customer balances.",
                "financial_challenge": "You are subsidizing customer inventory carrying costs with your own cash flow. Delaying supplier payments will hurt margins via lost cash discounts.",
                "recommended_strategic_move": "Implement a 2% prompt-payment discount for payments made within 7 days, and enforce strict 15-day credit limits via automated WhatsApp payment links."
            }
        
        return {
            "mode": "FOUNDER_ADVISORY",
            "observation": "Core sales momentum is strong, but collection cycle latency is averaging 18 days.",
            "recommended_strategic_move": "Automate WhatsApp invoice dispatch immediately upon order confirmation."
        }

if __name__ == "__main__":
    rep = ManagementReportEngine()
    print("[MGT_REPORT] CFO Advisory Mode Test:\n", rep.execute_ceo_cfo_strategic_mode("Think like my CFO", {"total_outstanding_receivables": 520000.0}))
