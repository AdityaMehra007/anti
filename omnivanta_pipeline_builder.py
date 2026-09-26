#!/usr/bin/env python3
"""
========================================================================================
OMNIVANTA B2B CLIENT ACQUISITION & PIPELINE BUILDER
========================================================================================
Founding Practice: OmniVanta Global Logistics & Trade Advisory
Lead Architect: Aditya Mehra (BBA International Business '26)
Core Capability:
  - Identifies and scores mid-market enterprise clients in Bengaluru with heavy
    3rd-party vendor, fabrication, and event logistics spend.
  - Quantifies potential vendor overbilling exposure and margin recovery.
  - Automatically synthesizes zero-risk, contingency-based C-Suite proposals.
  - Governs B2B pipeline velocity toward the target INR 50k - INR 200k monthly retainer/fee.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path

@dataclass
class ClientProspect:
    company_id: str
    company_name: str
    industry: str
    location: str
    estimated_annual_vendor_spend_inr: float
    contact_name: str
    contact_title: str
    contact_email: str
    typical_leakage_pct: float = 10.0
    status: str = "PROSPECT_IDENTIFIED"

class ProposalGenerator:
    """Generates high-converting, zero-risk contingency audit proposals."""

    def __init__(self, fee_pct: float = 20.0):
        self.fee_pct = fee_pct

    def generate_proposal(self, prospect: ClientProspect) -> str:
        est_recovery = prospect.estimated_annual_vendor_spend_inr * (prospect.typical_leakage_pct / 100.0)
        contingency_fee = est_recovery * (self.fee_pct / 100.0)

        lines = [
            f"# EXECUTIVE MARGIN RECOVERY AUDIT PROPOSAL\n\n",
            f"**To:** {prospect.contact_name}, {prospect.contact_title}  \n",
            f"**Organization:** {prospect.company_name} ({prospect.location})  \n",
            f"**From:** Aditya Mehra, Practice Lead -- OmniVanta Global Logistics & Trade Advisory  \n",
            f"**Engagement Model:** {self.fee_pct:.1f}% Success-Based Contingency Fee (Zero Out-of-Pocket Expense)  \n\n",
            "---\n\n",
            "## 1. Executive Context & Value Proposition\n\n",
            f"In high-tempo operations across {prospect.industry.lower()}, 3rd-party vendor rate drift, unmonitored SLA delays, ",
            "and duplicate billing typically cause **8% to 12% margin leakage** against master contracts.\n\n",
            f"For an organization with an estimated annual vendor disbursement of **INR {prospect.estimated_annual_vendor_spend_inr:,.2f}**, ",
            f"this represents an estimated **INR {est_recovery:,.2f}** in unrecovered liquidated damages and overbillings.\n\n",
            "---\n\n",
            "## 2. Quantitative Financial Projection\n\n",
            "| Assessment Metric | Projected Value | Operational Basis |\n",
            "| :--- | :---: | :--- |\n",
            f"| **Estimated Annual Vendor Spend** | INR {prospect.estimated_annual_vendor_spend_inr:,.2f} | 3rd-Party Staging, Fleet & Materials |\n",
            f"| **Targeted Margin Recovery ({prospect.typical_leakage_pct:.1f}%)** | **INR {est_recovery:,.2f}** | Direct Cash Flow Reclaimed to Balance Sheet |\n",
            f"| **OmniVanta Contingency Fee ({self.fee_pct:.1f}%)** | INR {contingency_fee:,.2f} | Billed ONLY Upon Realized Cash Recovery |\n",
            f"| **Net Client Preserved Capital** | **INR {(est_recovery - contingency_fee):,.2f}** | **Guaranteed Positive ROI** |\n\n",
            "---\n\n",
            "## 3. Scope of the Zero-Trust Vendor Audit\n\n",
            "OmniVanta executes a 48-hour algorithmic audit on a sample batch (last 60 days of vendor invoices):\n",
            "1. **Contracted Rate Card Reconciliation:** Identifies invoice line items billed above master agreements.\n",
            "2. **Timestamped SLA Delay Penalty Enforcement:** Calculates liquidated damages for delivery breaches beyond agreed grace periods.\n",
            "3. **Duplicate & Ghost Billing Identification:** Scans for double-invoicing across identical delivery milestones.\n",
            "4. **Cryptographic SHA-256 Audit Certificate:** Delivers a certified reconciliation dossier ready for CFO sign-off.\n\n",
            "---\n\n",
            "## 4. Next Step: Risk-Free 14-Day Pilot\n\n",
            "We propose a zero-risk pilot on your last 10 vendor invoices. If we find zero overcharges, you owe nothing. ",
            "If we recover capital, our fee is simply 20% of the funds returned to your accounts.\n\n",
            "To initiate, simply reply with a sample vendor rate sheet and the last batch of disbursement vouchers.\n\n",
            "Respectfully,\n\n",
            "**Aditya Mehra**  \n",
            "Lead Architect | OmniVanta Global Logistics & Trade Advisory  \n",
            "Operations Lead, Aero India 2025 | BBA International Business (DSU '26)\n"
        ]
        return "".join(lines)

class OmniVantaPipelineBuilder:
    """Manages prospect identification, opportunity sizing, and pipeline scoring."""

    def __init__(self, prospects: Optional[List[ClientProspect]] = None):
        self.prospects = prospects or []

    def total_pipeline_spend_inr(self) -> float:
        return sum(p.estimated_annual_vendor_spend_inr for p in self.prospects)

    def calculate_total_recoverable_capital_inr(self) -> float:
        return sum(
            p.estimated_annual_vendor_spend_inr * (p.typical_leakage_pct / 100.0)
            for p in self.prospects
        )

    def calculate_total_contingency_revenue_inr(self, fee_pct: float = 20.0) -> float:
        total_recovery = self.calculate_total_recoverable_capital_inr()
        return total_recovery * (fee_pct / 100.0)

    def export_json(self, file_path: str):
        data = [asdict(p) for p in self.prospects]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def render_pipeline_summary_markdown(self) -> str:
        total_spend = self.total_pipeline_spend_inr()
        total_rec = self.calculate_total_recoverable_capital_inr()
        total_fee = self.calculate_total_contingency_revenue_inr()

        lines = [
            "# OMNIVANTA B2B PIPELINE: QUALIFIED PROSPECT MATRIX\n\n",
            f"**Active Prospects Monitored:** {len(self.prospects)}  \n",
            f"**Total Monitored Vendor Spend:** INR {total_spend:,.2f}  \n",
            f"**Total Estimated Capital Recovery:** **INR {total_rec:,.2f}**  \n",
            f"**Total Projected Contingency Revenue (20%):** **INR {total_fee:,.2f}**  \n\n",
            "---\n\n",
            "| # | Target Enterprise | Industry | Annual Vendor Spend | Est. Recovery (10%) | Key Executive Contact | Status |\n",
            "| :---: | :--- | :--- | :---: | :---: | :--- | :---: |\n"
        ]

        for idx, p in enumerate(self.prospects, 1):
            rec = p.estimated_annual_vendor_spend_inr * (p.typical_leakage_pct / 100.0)
            lines.append(
                f"| **{idx}** | **{p.company_name}** | {p.industry} | INR {p.estimated_annual_vendor_spend_inr:,.2f} | "
                f"**INR {rec:,.2f}** | {p.contact_name} ({p.contact_title}) | `{p.status}` |\n"
            )

        return "".join(lines)

def get_default_bangalore_prospects() -> List[ClientProspect]:
    return [
        ClientProspect(
            company_id="BLR-PROSP-001",
            company_name="Apex Experiential & Staging Solutions",
            industry="Exhibition & Event Production",
            location="Whitefield, Bengaluru",
            estimated_annual_vendor_spend_inr=35000000.0,
            contact_name="Vikramaditya Rao",
            contact_title="VP of Operations",
            contact_email="vikram@apexstaging.in",
            typical_leakage_pct=10.0
        ),
        ClientProspect(
            company_id="BLR-PROSP-002",
            company_name="Kaveri Cold Chain & Logistics Ltd",
            industry="F&B Temperature-Controlled Freight",
            location="Peenya Industrial Area, Bengaluru",
            estimated_annual_vendor_spend_inr=60000000.0,
            contact_name="Sunil Gowda",
            contact_title="Chief Operating Officer",
            contact_email="sunil.gowda@kaverilogistics.com",
            typical_leakage_pct=9.5
        ),
        ClientProspect(
            company_id="BLR-PROSP-003",
            company_name="Silicon Workspaces & Infrastructure",
            industry="Commercial Facility Management",
            location="Koramangala, Bengaluru",
            estimated_annual_vendor_spend_inr=45000000.0,
            contact_name="Ananya Hegde",
            contact_title="Head of Vendor Procurement",
            contact_email="ananya.h@siliconspaces.in",
            typical_leakage_pct=8.0
        ),
        ClientProspect(
            company_id="BLR-PROSP-004",
            company_name="Urban Fleet Transports Private Ltd",
            industry="Intracity Cargo & Shuttles",
            location="Electronic City, Bengaluru",
            estimated_annual_vendor_spend_inr=25000000.0,
            contact_name="Deepak Menon",
            contact_title="Operations Director",
            contact_email="deepak.menon@urbanfleet.in",
            typical_leakage_pct=11.0
        )
    ]

def main():
    prospects = get_default_bangalore_prospects()
    builder = OmniVantaPipelineBuilder(prospects)
    summary_md = builder.render_pipeline_summary_markdown()
    print(summary_md)

    gen = ProposalGenerator(fee_pct=20.0)
    sample_proposal = gen.generate_proposal(prospects[0])
    print("\n" + "=" * 80)
    print("SAMPLE PROPOSAL PREVIEW:")
    print("=" * 80)
    print(sample_proposal[:600] + "\n...")

if __name__ == "__main__":
    main()
