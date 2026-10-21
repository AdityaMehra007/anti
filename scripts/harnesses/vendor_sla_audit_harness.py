"""
Bengaluru GCC Vendor SLA & SOW Leakage Audit Harness
Audits external IT vendor timesheets against delivery logs to detect
SLA breach penalties, phantom hours, and calculate recoverable cash credits.
"""

import json
from datetime import datetime, timedelta

SAMPLE_VENDOR_RECORDS = [
    {
        "vendor_name": "Tier-1 IT Vendor Pod A",
        "contract_id": "SOW-2025-BLR-089",
        "resource_name": "Resource_Dev_01",
        "billed_hours": 160,
        "active_jira_hours": 112,
        "hourly_rate_inr": 2800,
        "tickets_resolved": 14,
        "sla_breached_tickets": 3,
        "contractual_sla_penalty_per_breach_inr": 45000,
    },
    {
        "vendor_name": "Tier-1 IT Vendor Pod A",
        "contract_id": "SOW-2025-BLR-089",
        "resource_name": "Resource_Dev_02",
        "billed_hours": 160,
        "active_jira_hours": 85,
        "hourly_rate_inr": 3200,
        "tickets_resolved": 8,
        "sla_breached_tickets": 4,
        "contractual_sla_penalty_per_breach_inr": 45000,
    },
    {
        "vendor_name": "Tier-1 IT Vendor Pod B",
        "contract_id": "SOW-2025-BLR-114",
        "resource_name": "Resource_QA_01",
        "billed_hours": 160,
        "active_jira_hours": 140,
        "hourly_rate_inr": 2200,
        "tickets_resolved": 32,
        "sla_breached_tickets": 1,
        "contractual_sla_penalty_per_breach_inr": 30000,
    },
    {
        "vendor_name": "Tier-1 IT Vendor Pod B",
        "contract_id": "SOW-2025-BLR-114",
        "resource_name": "Resource_Dev_03",
        "billed_hours": 160,
        "active_jira_hours": 70,
        "hourly_rate_inr": 3500,
        "tickets_resolved": 5,
        "sla_breached_tickets": 5,
        "contractual_sla_penalty_per_breach_inr": 30000,
    }
]

def audit_vendor_leakage(records):
    audit_summary = {
        "total_billed_inr": 0,
        "total_phantom_hours": 0,
        "phantom_billing_leakage_inr": 0,
        "total_sla_breaches": 0,
        "contractual_sla_penalties_inr": 0,
        "total_recoverable_capital_inr": 0,
        "contingency_success_fee_25_pct_inr": 0,
        "line_item_details": []
    }
    
    for r in records:
        resource_billed_inr = r["billed_hours"] * r["hourly_rate_inr"]
        phantom_hours = max(0, r["billed_hours"] - r["active_jira_hours"])
        phantom_leakage_inr = phantom_hours * r["hourly_rate_inr"]
        sla_penalties_inr = r["sla_breached_tickets"] * r["contractual_sla_penalty_per_breach_inr"]
        total_recovery_for_resource = phantom_leakage_inr + sla_penalties_inr
        
        audit_summary["total_billed_inr"] += resource_billed_inr
        audit_summary["total_phantom_hours"] += phantom_hours
        audit_summary["phantom_billing_leakage_inr"] += phantom_leakage_inr
        audit_summary["total_sla_breaches"] += r["sla_breached_tickets"]
        audit_summary["contractual_sla_penalties_inr"] += sla_penalties_inr
        audit_summary["total_recoverable_capital_inr"] += total_recovery_for_resource
        
        audit_summary["line_item_details"].append({
            "resource": r["resource_name"],
            "vendor": r["vendor_name"],
            "phantom_hours": phantom_hours,
            "phantom_loss_inr": phantom_leakage_inr,
            "sla_penalties_inr": sla_penalties_inr,
            "recoverable_inr": total_recovery_for_resource
        })
        
    audit_summary["contingency_success_fee_25_pct_inr"] = round(audit_summary["total_recoverable_capital_inr"] * 0.25)
    return audit_summary

if __name__ == "__main__":
    result = audit_vendor_leakage(SAMPLE_VENDOR_RECORDS)
    print("=== BENGALURU GCC VENDOR SLA AUDIT REPORT ===")
    print(f"Total Billed Amount: INR {result['total_billed_inr']:,}")
    print(f"Total Phantom Hours Detected: {result['total_phantom_hours']} hrs")
    print(f"Phantom Billing Leakage: INR {result['phantom_billing_leakage_inr']:,}")
    print(f"Contractual SLA Breach Penalties: INR {result['contractual_sla_penalties_inr']:,}")
    print(f"TOTAL RECOVERABLE CAPITAL FOR GCC: INR {result['total_recoverable_capital_inr']:,}")
    print(f"Service Provider Contingency Fee (25%): INR {result['contingency_success_fee_25_pct_inr']:,}")
    print(f"Leakage Percentage: {result['total_recoverable_capital_inr'] / result['total_billed_inr'] * 100:.1f}%")
