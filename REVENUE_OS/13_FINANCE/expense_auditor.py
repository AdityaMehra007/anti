"""
Expense Auditor for REVENUE OS
Adheres strictly to Directives 121, 122, 123.
Runs monthly audit: 'WHAT CAN WE CANCEL?'
Flags underutilized SaaS subscriptions, zero-usage tools, and duplicate services.
"""

from typing import Any, Dict, List

class ExpenseAuditor:
    """
    Audits active recurring subscriptions to prevent SaaS bloat and cost leaks.
    """
    def audit_subscriptions(self, subscriptions: List[Dict[str, Any]]) -> Dict[str, Any]:
        cancellations = []
        total_potential_savings = 0.0
        
        for sub in subscriptions:
            name = sub.get("tool_name", "Unknown Tool")
            cost = float(sub.get("cost_usd", 0.0))
            usage_hours = float(sub.get("monthly_usage_hours", 0.0))
            is_essential = bool(sub.get("essential", False))
            
            # Rule: If monthly usage is 0 and tool is not marked strictly essential, recommend immediate cancellation
            if usage_hours == 0.0 and not is_essential:
                cancellations.append({
                    "tool_name": name,
                    "cost_usd": cost,
                    "reason": "Zero usage hours recorded in previous 30-day billing cycle.",
                    "recommendation": "CANCEL immediately before upcoming renewal."
                })
                total_potential_savings += cost
            elif usage_hours < 2.0 and cost > 50.0 and not is_essential:
                cancellations.append({
                    "tool_name": name,
                    "cost_usd": cost,
                    "reason": f"Underutilized: only {usage_hours} hours used for ${cost}/mo.",
                    "recommendation": "Downgrade to free tier or substitute with stdlib/open-source alternative."
                })
                total_potential_savings += cost
                
        return {
            "total_subscriptions_audited": len(subscriptions),
            "cancellation_recommendations": cancellations,
            "total_potential_savings_usd": round(total_potential_savings, 2),
            "annualized_savings_usd": round(total_potential_savings * 12.0, 2)
        }
