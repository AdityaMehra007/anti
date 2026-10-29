"""
Windmill Production Script: Customer Churn Risk Radar & Retention Synthesizer
=============================================================================
Category: Revenue Operations & Customer Success
Language: Python 3.12 / 3.13 (Windmill Native / Docker Sandbox)

Analyzes enterprise account telemetry, product usage drop-offs, open support
tickets, and invoice payment delays to compute churn risk and recommend
automated retention playbooks.
"""

from typing import Dict, Any, List
import json
import math
from datetime import datetime, timezone


def calculate_churn_risk(
    active_users_30d: int,
    previous_active_users_30d: int,
    open_p1_tickets: int,
    days_past_due: int,
    nps_score: int,
    contract_renewal_days: int
) -> Dict[str, Any]:
    """Computes multidimensional churn probability score (0.0 to 1.0)."""
    # Factor 1: Usage velocity change
    if previous_active_users_30d > 0:
        usage_ratio = active_users_30d / previous_active_users_30d
        usage_drop = max(0.0, 1.0 - usage_ratio)
    else:
        usage_drop = 0.0

    # Factor 2: Support escalation severity
    support_penalty = min(0.4, open_p1_tickets * 0.15)

    # Factor 3: Billing delinquency
    billing_penalty = min(0.3, (days_past_due / 30.0) * 0.2)

    # Factor 4: Customer Sentiment (NPS)
    sentiment_penalty = max(0.0, (7 - nps_score) * 0.05) if nps_score < 7 else 0.0

    # Factor 5: Renewal proximity multiplier
    renewal_urgency = 1.25 if contract_renewal_days <= 60 else 1.0

    raw_score = (usage_drop * 0.4 + support_penalty + billing_penalty + sentiment_penalty) * renewal_urgency
    risk_score = round(min(1.0, max(0.05, raw_score)), 3)

    if risk_score >= 0.70:
        tier = "CRITICAL_RISK"
        action = "DISPATCH_EXECUTIVE_INTERVENTION"
    elif risk_score >= 0.40:
        tier = "ELEVATED_RISK"
        action = "SCHEDULE_CSM_HEALTH_CHECK"
    else:
        tier = "HEALTHY"
        action = "MONITOR_STANDARD_CADENCE"

    return {
        "risk_score": risk_score,
        "risk_tier": tier,
        "recommended_action": action,
        "metrics_breakdown": {
            "usage_drop_pct": round(usage_drop * 100, 1),
            "support_penalty": round(support_penalty, 3),
            "billing_penalty": round(billing_penalty, 3),
            "sentiment_penalty": round(sentiment_penalty, 3),
            "renewal_urgency_applied": renewal_urgency > 1.0
        }
    }


def main(
    account_id: str = "ACC-ENT-9042",
    company_name: str = "Global Logistics Technologies Ltd",
    annual_contract_value_inr: float = 3600000.0,
    active_users_30d: int = 142,
    previous_active_users_30d: int = 220,
    open_p1_tickets: int = 2,
    days_past_due: int = 14,
    nps_score: int = 4,
    contract_renewal_days: int = 45
) -> Dict[str, Any]:
    """Main entrypoint executed by Windmill workers."""
    eval_result = calculate_churn_risk(
        active_users_30d=active_users_30d,
        previous_active_users_30d=previous_active_users_30d,
        open_p1_tickets=open_p1_tickets,
        days_past_due=days_past_due,
        nps_score=nps_score,
        contract_renewal_days=contract_renewal_days
    )

    mrr_inr = round(annual_contract_value_inr / 12.0, 2)
    mrr_at_risk = round(mrr_inr * eval_result["risk_score"], 2)

    playbook = []
    if eval_result["risk_tier"] == "CRITICAL_RISK":
        playbook.append("Trigger automated Slack emergency alert to VP Customer Success")
        playbook.append(f"Hold collections on {days_past_due} days past due invoice; offer 14-day cure window")
        playbook.append("Schedule 30-minute executive sponsor alignment call")
    elif eval_result["risk_tier"] == "ELEVATED_RISK":
        playbook.append("Dispatch feature re-engagement sequence to inactive seat holders")
        playbook.append("Expedite resolution of open P1 support tickets with engineering lead")
    else:
        playbook.append("Candidate for quarterly expansion and upsell review")

    return {
        "account_id": account_id,
        "company_name": company_name,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "annual_contract_value_inr": annual_contract_value_inr,
        "monthly_recurring_revenue_inr": mrr_inr,
        "mrr_at_risk_inr": mrr_at_risk,
        "risk_evaluation": eval_result,
        "retention_playbook": playbook,
        "status": "EVALUATION_COMPLETE"
    }


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
