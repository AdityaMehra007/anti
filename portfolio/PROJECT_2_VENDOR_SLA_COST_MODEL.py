#!/usr/bin/env python3
"""
========================================================================================
PORTFOLIO PROJECT 2: TIER-1 VENDOR SLA GOVERNANCE & RATE CARD RECONCILIATION ENGINE
========================================================================================
Author: Aditya Mehra (BBA International Business '26)
Context: Operational vendor contract governance modeled on 300+ brand activations
         (Tata Communications, Puma, Dyson) and high-volume exhibition suppliers.
Core Capability:
  - Validates delivery timestamps against contracted SLAs.
  - Reconciles invoiced amounts against agreed Master Rate Cards.
  - Automatically calculates liquidated damages / SLA penalty deductions.
  - Generates executive variance summaries and margin protection reports.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Master Contracted Rate Card & Agreed SLAs
MASTER_RATE_CARD = {
    "AV_FABRICATION": {
        "vendor": "Bangalore AudioVisuals & Staging Ltd",
        "category": "Stage & Sound Engineering",
        "contracted_rate_inr": 85000.0,
        "max_turnaround_hours": 4.0,
        "penalty_per_hour_delay_pct": 5.0,  # 5% deduction per hour of delay
        "max_penalty_pct": 25.0
    },
    "PREMIUM_MERCHANDISE": {
        "vendor": "Apex Print & Apparel Works",
        "category": "Custom Event Collateral",
        "contracted_rate_inr": 120000.0,
        "max_turnaround_hours": 12.0,
        "penalty_per_hour_delay_pct": 3.0,
        "max_penalty_pct": 20.0
    },
    "COLD_CHAIN_CATERING": {
        "vendor": "Yelahanka Fresh Logistics",
        "category": "F&B Cold Storage & Supply",
        "contracted_rate_inr": 95000.0,
        "max_turnaround_hours": 2.0,
        "penalty_per_hour_delay_pct": 10.0,  # Strict temperature/freshness SLA
        "max_penalty_pct": 30.0
    },
    "CREW_TRANSPORT": {
        "vendor": "Silicon Cabs & Fleet Ops",
        "category": "Crew Logistics & Shuttle",
        "contracted_rate_inr": 45000.0,
        "max_turnaround_hours": 1.0,
        "penalty_per_hour_delay_pct": 15.0,
        "max_penalty_pct": 50.0
    }
}

# Inbound Delivery & Invoice Data
INVOICE_BATCH = [
    {
        "invoice_id": "INV-2025-0891",
        "item_code": "AV_FABRICATION",
        "invoiced_amount_inr": 85000.0,
        "scheduled_time": "2025-02-12 04:00:00",
        "actual_delivery_time": "2025-02-12 05:30:00",  # 1.5 hrs delay
        "quality_score_pct": 98.0
    },
    {
        "invoice_id": "INV-2025-0892",
        "item_code": "PREMIUM_MERCHANDISE",
        "invoiced_amount_inr": 135000.0,  # Rate card variance: billed ₹15k over contracted!
        "scheduled_time": "2025-02-12 06:00:00",
        "actual_delivery_time": "2025-02-12 06:00:00",  # On time
        "quality_score_pct": 100.0
    },
    {
        "invoice_id": "INV-2025-0893",
        "item_code": "COLD_CHAIN_CATERING",
        "invoiced_amount_inr": 95000.0,
        "scheduled_time": "2025-02-12 05:30:00",
        "actual_delivery_time": "2025-02-12 07:30:00",  # 2.0 hrs delay
        "quality_score_pct": 95.0
    },
    {
        "invoice_id": "INV-2025-0894",
        "item_code": "CREW_TRANSPORT",
        "invoiced_amount_inr": 45000.0,
        "scheduled_time": "2025-02-12 05:00:00",
        "actual_delivery_time": "2025-02-12 05:10:00",  # 10 min delay (within grace)
        "quality_score_pct": 100.0
    }
]

class VendorSLAReconciliationEngine:
    """Automates contract audit, SLA compliance, and cost variance modeling."""

    def __init__(self, rate_card: Dict[str, Any]):
        self.rate_card = rate_card

    def audit_batch(self, invoices: List[Dict[str, Any]]) -> Dict[str, Any]:
        audited_records = []
        total_invoiced = 0.0
        total_approved = 0.0
        total_penalties_recovered = 0.0
        total_rate_variance_disallowed = 0.0

        for inv in invoices:
            code = inv["item_code"]
            rule = self.rate_card.get(code)
            if not rule:
                continue

            inv_amount = float(inv["invoiced_amount_inr"])
            contracted = float(rule["contracted_rate_inr"])
            total_invoiced += inv_amount

            # 1. Rate Variance Check
            rate_variance = inv_amount - contracted
            disallowed_overcharge = max(0.0, rate_variance)
            base_payable = contracted if rate_variance > 0 else inv_amount
            total_rate_variance_disallowed += disallowed_overcharge

            # 2. Delay & SLA Audit
            fmt = "%Y-%m-%d %H:%M:%S"
            t_sched = datetime.strptime(inv["scheduled_time"], fmt)
            t_act = datetime.strptime(inv["actual_delivery_time"], fmt)
            delay_minutes = max(0.0, (t_act - t_sched).total_seconds() / 60.0)
            delay_hours = delay_minutes / 60.0

            penalty_pct = 0.0
            if delay_minutes > 15.0:  # 15-minute grace period
                effective_delay_hrs = (delay_minutes - 15.0) / 60.0
                raw_penalty = effective_delay_hrs * rule["penalty_per_hour_delay_pct"]
                penalty_pct = min(rule["max_penalty_pct"], raw_penalty)

            penalty_amount = round((base_payable * (penalty_pct / 100.0)), 2)
            total_penalties_recovered += penalty_amount

            approved_payable = round(base_payable - penalty_amount, 2)
            total_approved += approved_payable

            audited_records.append({
                "invoice_id": inv["invoice_id"],
                "vendor": rule["vendor"],
                "category": rule["category"],
                "invoiced_inr": inv_amount,
                "contracted_inr": contracted,
                "delay_minutes": round(delay_minutes, 1),
                "penalty_pct": round(penalty_pct, 1),
                "penalty_inr": penalty_amount,
                "disallowed_overcharge_inr": disallowed_overcharge,
                "net_payable_inr": approved_payable,
                "status": "ADJUSTED_FOR_PENALTY" if (penalty_amount > 0 or disallowed_overcharge > 0) else "APPROVED_CLEAN"
            })

        net_savings = total_rate_variance_disallowed + total_penalties_recovered
        margin_protection_pct = round((net_savings / total_invoiced) * 100.0, 2) if total_invoiced > 0 else 0.0

        return {
            "summary": {
                "total_invoiced_inr": round(total_invoiced, 2),
                "total_approved_payable_inr": round(total_approved, 2),
                "total_disallowed_overcharge_inr": round(total_rate_variance_disallowed, 2),
                "total_sla_penalties_recovered_inr": round(total_penalties_recovered, 2),
                "total_margin_savings_inr": round(net_savings, 2),
                "margin_protection_percentage": f"{margin_protection_pct}%"
            },
            "records": audited_records
        }

def main():
    engine = VendorSLAReconciliationEngine(MASTER_RATE_CARD)
    report = engine.audit_batch(INVOICE_BATCH)

    print("=" * 85)
    print("  TIER-1 VENDOR SLA AUDIT & INVOICE RECONCILIATION REPORT")
    print("  Architect: Aditya Mehra | Framework: Contract SLA Governance")
    print("=" * 85)
    print(f"\n{'Invoice ID':<15} {'Vendor':<30} {'Billed (INR)':<14} {'Approved':<14} {'Savings':<10} {'Status'}")
    print("-" * 95)
    for r in report["records"]:
        inv = r["invoice_id"]
        v = r["vendor"][:28]
        billed = f"₹{r['invoiced_inr']:,.2f}"
        approved = f"₹{r['net_payable_inr']:,.2f}"
        savings = f"₹{(r['disallowed_overcharge_inr'] + r['penalty_inr']):,.2f}"
        status = r["status"]
        print(f"{inv:<15} {v:<30} {billed:<14} {approved:<14} {savings:<10} {status}")
    print("-" * 95)
    print("\nEXECUTIVE FINANCIAL RECONCILIATION SUMMARY:")
    s = report["summary"]
    print(f"  • Total Gross Invoiced Amount : ₹{s['total_invoiced_inr']:,.2f}")
    print(f"  • Disallowed Rate Overcharges : ₹{s['total_disallowed_overcharge_inr']:,.2f}")
    print(f"  • SLA Delay Penalties Enforced : ₹{s['total_sla_penalties_recovered_inr']:,.2f}")
    print(f"  • Net Approved Disbursements  : ₹{s['total_approved_payable_inr']:,.2f}")
    print(f"  • Total Capital Preserved     : ₹{s['total_margin_savings_inr']:,.2f} ({s['margin_protection_percentage']} margin gain)")
    print("=" * 85)

if __name__ == "__main__":
    main()
