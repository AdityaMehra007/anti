#!/usr/bin/env python3
"""
========================================================================================
OMNIVANTA B2B VENDOR SLA RECOVERY & MARGIN PROTECTION ENGINE
========================================================================================
Founding Practice: OmniVanta Global Logistics & Trade Advisory
Lead Architect: Aditya Mehra (BBA International Business '26)
Core Function:
  Autonomous audit and financial recovery engine for enterprise supply chain,
  event logistics, and commercial operations contracts.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

@dataclass
class AuditConfig:
    contingency_fee_pct: float = 20.0
    default_grace_minutes: float = 15.0
    default_max_penalty_pct: float = 30.0
    audit_title: str = "OmniVanta B2B Vendor SLA Recovery Audit"

class OmniVantaAuditEngine:
    """Core B2B contract reconciliation and margin recovery engine."""

    def __init__(self, rate_card: Dict[str, Any], config: Optional[AuditConfig] = None):
        self.rate_card = rate_card
        self.config = config or AuditConfig()

    def audit_batch(self, invoices: List[Dict[str, Any]]) -> Dict[str, Any]:
        audited_records = []
        seen_invoices = set()
        
        total_invoiced = 0.0
        total_approved = 0.0
        total_penalties_recovered = 0.0
        total_rate_variance_disallowed = 0.0

        for inv in invoices:
            inv_id = str(inv.get("invoice_id", "UNKNOWN"))
            code = str(inv.get("item_code", ""))
            rule = self.rate_card.get(code, {})

            inv_amount = float(inv.get("invoiced_amount_inr", 0.0))
            contracted = float(rule.get("contracted_rate_inr", inv_amount))
            grace_min = float(rule.get("grace_period_minutes", self.config.default_grace_minutes))
            penalty_rate = float(rule.get("penalty_per_hour_delay_pct", 5.0))
            max_penalty = float(rule.get("max_penalty_pct", self.config.default_max_penalty_pct))

            is_duplicate = inv_id in seen_invoices
            seen_invoices.add(inv_id)

            if is_duplicate:
                disallowed_overcharge = inv_amount
                base_payable = 0.0
                delay_minutes = 0.0
                penalty_pct = 0.0
                penalty_amount = 0.0
                approved_payable = 0.0
                status = "REJECTED_DUPLICATE_INVOICE"
            else:
                total_invoiced += inv_amount

                rate_variance = inv_amount - contracted
                disallowed_overcharge = max(0.0, rate_variance)
                base_payable = contracted if rate_variance > 0 else inv_amount
                total_rate_variance_disallowed += disallowed_overcharge

                delay_minutes = 0.0
                penalty_pct = 0.0
                penalty_amount = 0.0

                fmt = "%Y-%m-%d %H:%M:%S"
                sched_str = inv.get("scheduled_time")
                act_str = inv.get("actual_delivery_time")

                if sched_str and act_str:
                    try:
                        t_sched = datetime.strptime(sched_str, fmt)
                        t_act = datetime.strptime(act_str, fmt)
                        raw_delay = (t_act - t_sched).total_seconds() / 60.0
                        delay_minutes = max(0.0, raw_delay)
                    except Exception:
                        delay_minutes = 0.0

                if delay_minutes > grace_min:
                    effective_delay_hrs = (delay_minutes - grace_min) / 60.0
                    raw_penalty_pct = effective_delay_hrs * penalty_rate
                    penalty_pct = min(max_penalty, raw_penalty_pct)
                    penalty_amount = round(base_payable * (penalty_pct / 100.0), 2)

                total_penalties_recovered += penalty_amount
                approved_payable = round(base_payable - penalty_amount, 2)
                total_approved += approved_payable

                status = "ADJUSTED_FOR_PENALTY" if (penalty_amount > 0 or disallowed_overcharge > 0) else "APPROVED_CLEAN"

            record = {
                "invoice_id": inv_id,
                "item_code": code,
                "vendor": rule.get("vendor", "General Vendor"),
                "category": rule.get("category", "Operations"),
                "invoiced_inr": round(inv_amount, 2),
                "contracted_inr": round(contracted, 2),
                "delay_minutes": round(delay_minutes, 1),
                "penalty_pct": round(penalty_pct, 1),
                "penalty_inr": round(penalty_amount, 2),
                "disallowed_overcharge_inr": round(disallowed_overcharge, 2),
                "net_payable_inr": round(approved_payable, 2),
                "is_duplicate": is_duplicate,
                "status": status
            }
            audited_records.append(record)

        net_savings = total_rate_variance_disallowed + total_penalties_recovered
        margin_protection_pct = round((net_savings / total_invoiced * 100.0), 2) if total_invoiced > 0 else 0.0
        contingency_fee = round(net_savings * (self.config.contingency_fee_pct / 100.0), 2)

        fingerprint_payload = json.dumps(audited_records, sort_keys=True)
        audit_hash = hashlib.sha256(fingerprint_payload.encode("utf-8")).hexdigest()

        return {
            "title": self.config.audit_title,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "audit_hash_sha256": audit_hash,
            "summary": {
                "total_invoiced_inr": round(total_invoiced, 2),
                "total_approved_payable_inr": round(total_approved, 2),
                "total_disallowed_overcharge_inr": round(total_rate_variance_disallowed, 2),
                "total_sla_penalties_recovered_inr": round(total_penalties_recovered, 2),
                "total_margin_savings_inr": round(net_savings, 2),
                "margin_protection_percentage": f"{margin_protection_pct}%"
            },
            "contingency_fee_inr": contingency_fee,
            "contingency_rate_pct": self.config.contingency_fee_pct,
            "records": audited_records
        }

    def render_markdown(self, report: Dict[str, Any]) -> str:
        s = report["summary"]
        lines = [
            f"# {report['title']}\n\n",
            f"**Execution Timestamp:** `{report['generated_at']}`  \n",
            f"**Audit Integrity Hash (SHA-256):** `{report['audit_hash_sha256']}`  \n",
            f"**Lead Practice:** OmniVanta Global Logistics & Trade Advisory  \n",
            f"**Executive Practice Lead:** Aditya Mehra (BBA International Business '26)  \n\n",
            "---\n\n",
            "## 1. Executive Financial Recovery Summary\n\n",
            "| Audit Dimension | Amount (INR) | Financial Impact |\n",
            "| :--- | :---: | :--- |\n",
            f"| **Gross Invoiced Amount** | INR {s['total_invoiced_inr']:,.2f} | Baseline Billed Vendor Capital |\n",
            f"| **Disallowed Rate Overcharges** | INR {s['total_disallowed_overcharge_inr']:,.2f} | Billed Above Master Contracted Rate |\n",
            f"| **Enforced SLA Delay Penalties** | INR {s['total_sla_penalties_recovered_inr']:,.2f} | Liquidated Damages for Turnaround Breach |\n",
            f"| **Total Net Margin Preserved** | **INR {s['total_margin_savings_inr']:,.2f}** | **{s['margin_protection_percentage']} Bottom-Line Margin Recovery** |\n",
            f"| **Net Authorized Disbursements** | INR {s['total_approved_payable_inr']:,.2f} | Clean Reconciled Vendor Accounts Payable |\n",
            f"| **OmniVanta Advisory Success Fee ({report['contingency_rate_pct']}%)** | **INR {report['contingency_fee_inr']:,.2f}** | Pure Success-Based Contingency Fee |\n\n",
            "---\n\n",
            "## 2. Itemized Invoice Reconciliation Ledger\n\n",
            "| Invoice ID | Vendor | Category | Billed (INR) | Contracted (INR) | Delay | Net Payable (INR) | Status |\n",
            "| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |\n"
        ]

        for r in report["records"]:
            lines.append(
                f"| `{r['invoice_id']}` | **{r['vendor']}** | {r['category']} | INR {r['invoiced_inr']:,.2f} | "
                f"INR {r['contracted_inr']:,.2f} | {r['delay_minutes']}m | **INR {r['net_payable_inr']:,.2f}** | `{r['status']}` |\n"
            )

        lines.append("\n---\n*OmniVanta B2B Advisory -- Zero Risk, Pure Margin Recovery.*")
        return "".join(lines)

def main():
    rate_card = {
        "AV_FABRICATION": {
            "vendor": "Bangalore AudioVisuals and Staging Ltd",
            "category": "Stage Engineering",
            "contracted_rate_inr": 85000.0,
            "grace_period_minutes": 15.0,
            "penalty_per_hour_delay_pct": 5.0,
            "max_penalty_pct": 25.0
        },
        "PREMIUM_MERCHANDISE": {
            "vendor": "Apex Print and Apparel Works",
            "category": "Custom Event Collateral",
            "contracted_rate_inr": 120000.0,
            "grace_period_minutes": 30.0,
            "penalty_per_hour_delay_pct": 3.0,
            "max_penalty_pct": 20.0
        },
        "COLD_CHAIN_CATERING": {
            "vendor": "Yelahanka Fresh Logistics",
            "category": "F&B Cold Storage",
            "contracted_rate_inr": 95000.0,
            "grace_period_minutes": 15.0,
            "penalty_per_hour_delay_pct": 10.0,
            "max_penalty_pct": 30.0
        }
    }

    invoices = [
        {
            "invoice_id": "INV-2026-0891",
            "item_code": "AV_FABRICATION",
            "invoiced_amount_inr": 85000.0,
            "scheduled_time": "2026-02-12 04:00:00",
            "actual_delivery_time": "2026-02-12 05:30:00",
            "quality_score_pct": 98.0
        },
        {
            "invoice_id": "INV-2026-0892",
            "item_code": "PREMIUM_MERCHANDISE",
            "invoiced_amount_inr": 135000.0,
            "scheduled_time": "2026-02-12 06:00:00",
            "actual_delivery_time": "2026-02-12 06:00:00",
            "quality_score_pct": 100.0
        },
        {
            "invoice_id": "INV-2026-0893",
            "item_code": "COLD_CHAIN_CATERING",
            "invoiced_amount_inr": 95000.0,
            "scheduled_time": "2026-02-12 05:30:00",
            "actual_delivery_time": "2026-02-12 07:30:00",
            "quality_score_pct": 95.0
        }
    ]

    engine = OmniVantaAuditEngine(rate_card)
    report = engine.audit_batch(invoices)
    md = engine.render_markdown(report)
    print(md)

if __name__ == "__main__":
    main()
