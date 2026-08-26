"""
NEXUS AUTOPILOT - Chartered Accountant (CA) & Partner Distribution Engine
Provides multi-client governance, aggregated receivables monitoring, GST status, and 20% recurring commission attribution.
"""
from typing import Dict, Any, List

class CAPartnerPortalEngine:
    def __init__(self):
        self.partner_records = {
            "PARTNER-CA-BLR-01": {
                "firm_name": "Kulkarni & Associates Chartered Accountants",
                "partner_name": "Suresh Kulkarni, FCA",
                "location": "Jayanagar, Bengaluru",
                "commission_rate_pct": 20.0,
                "managed_clients": [
                    {"org_id": "ORG-ABC-001", "name": "ABC Packaging Distributors", "plan": "PRO", "mrr_inr": 14999.0, "status": "ACTIVE", "gst_status": "RECONCILED", "overdue_inr": 400000.0},
                    {"org_id": "ORG-XYZ-002", "name": "Apex Clean Energy Solutions", "plan": "GROWTH", "mrr_inr": 4999.0, "status": "ACTIVE", "gst_status": "PENDING_AUDIT", "overdue_inr": 120000.0},
                    {"org_id": "ORG-BLR-003", "name": "Kiran Digital Media Agency", "plan": "GROWTH", "mrr_inr": 4999.0, "status": "ACTIVE", "gst_status": "RECONCILED", "overdue_inr": 85000.0}
                ]
            }
        }

    def get_partner_dashboard(self, partner_id: str = "PARTNER-CA-BLR-01") -> Dict[str, Any]:
        p = self.partner_records.get(partner_id)
        if not p:
            return {"error": "PARTNER_NOT_FOUND"}

        total_client_mrr = sum(c["mrr_inr"] for c in p["managed_clients"])
        monthly_commission = total_client_mrr * (p["commission_rate_pct"] / 100.0)
        total_overdue_supervised = sum(c["overdue_inr"] for c in p["managed_clients"])

        return {
            "partner_id": partner_id,
            "firm_name": p["firm_name"],
            "total_managed_clients": len(p["managed_clients"]),
            "total_client_mrr_inr": total_client_mrr,
            "monthly_commission_earned_inr": monthly_commission,
            "annualized_commission_inr": monthly_commission * 12,
            "total_overdue_receivables_supervised_inr": total_overdue_supervised,
            "clients": p["managed_clients"]
        }

if __name__ == "__main__":
    ca = CAPartnerPortalEngine()
    print("[CA_PORTAL] Partner Dashboard:\n", ca.get_partner_dashboard())
