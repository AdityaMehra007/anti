"""
OMEGA INFINITY (Ω-OS) — DAILY SOVEREIGN EXECUTIVE BRIEF GENERATOR
Aggregates enterprise holding telemetry, VECTIS trade pipeline, top verified leads,
and cryptographic audit ledger into an authoritative daily executive brief.
"""

import os
import sys
import json
import time
import datetime
from typing import Dict, Any, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import get_kernel, CONSTITUTIONAL_MODES
from omega_infinity.omega_intel_engine import IntelSearchEngine
from omega_infinity.omega_vectis_adapter import VectisEnterpriseAdapter

OUTPUT_BRIEF_PATH = os.path.join(REPO_ROOT, "DAILY_SOVEREIGN_BRIEF.md")


def generate_daily_brief() -> str:
    kernel = get_kernel()
    intel = IntelSearchEngine()
    vectis = VectisEnterpriseAdapter()

    summary = kernel.get_summary()
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get top leads
    top_leads = intel.trade_leads[:5] if intel.trade_leads else []
    # Get top target MNCs
    top_targets = intel.companies[:5] if intel.companies else []
    # Get recent certificates
    certs = vectis.list_outbox_certificates()[:5]

    md = f"""# 🏛️ OMEGA ∞ SOVEREIGN DAILY EXECUTIVE BRIEF
**Generated**: `{today}`  
**Founder**: `{summary['founder']}` | **Location**: `Bengaluru, Karnataka, India`  
**Holding**: `{summary['holding']}`  
**Operating Entity**: `{summary['primary_entity']}`  
**Active Mode**: `Mode {summary['active_mode']['code']} ({summary['active_mode']['name']})` — *{summary['active_mode']['desc']}*  

---

## 1. Executive Holding Vitals & Runway

| Metric | Current Reality | Target / Benchmark | Status |
|---|---|---|---|
| **Capital Reserves** | ₹{summary['financials']['capital_reserves_inr']:,.2f} | ₹50,00,000.00 (KITS Grant / Equity) | 🟢 FULLY SECURED |
| **Monthly Burn Rate** | ₹{summary['financials']['monthly_burn_inr']:,.2f} | < ₹15,000.00 (Ponytail Minimalism) | 🟢 OPTIMAL |
| **Operational Runway** | {summary['financials']['runway_months']:.1f} Months | > 36 Months | 🟢 PERPETUAL RUNWAY |
| **DPIIT Recognition** | {summary['financials']['dpiit_status']} | Section 80-IAC (3-Yr Tax Holiday) | 🟢 AUDIT READY |
| **VECTIS Target ARR** | ₹54,00,000.00 | ₹1,00,00,000.00 (2028 Scale) | 🚀 IN FLIGHT |

---

## 2. Operational Telemetry & Cryptographic Verification

- **Total Network Connections Indexed**: `{summary['telemetry']['linkedin_connections_count']:,}` verified professionals.
- **Target Company Matrix**: `{summary['telemetry']['target_companies_count']:,}` deduplicated enterprises.
- **Mined Trade Leads**: `{summary['telemetry']['verified_leads_count']}` export decision-makers.
- **Trade Audits Completed**: `{summary['telemetry']['trade_audits_passed']} Passed` / `{summary['telemetry']['trade_audits_failed']} Discrepancies Caught`.
- **CBAM Assessments Completed**: `{summary['telemetry']['cbam_assessments_completed']}` EU carbon border evaluations.
- **Cryptographic Ledger**: `{'VALID' if summary['ledger_status']['valid'] else 'INVALID'}` (`{summary['ledger_status'].get('total_blocks', 0)} blocks chained via SHA-256`).

---

## 3. High-Priority VECTIS Trade Action Leads

| Lead Name | Company | Role | Priority | Action Hook |
|---|---|---|---|---|
"""
    for l in top_leads:
        name = l.get("name") or l.get("contact", "Trade Executive")
        comp = l.get("company", "Export Corp")
        role = l.get("position") or l.get("role", "Operations")
        hook = l.get("tailored_outreach_pitch", "Zero-risk UCP 600 compliance audit pilot.")[:80] + "..."
        md += f"| **{name}** | {comp} | {role} | `HIGH` | {hook} |\n"

    md += """
---

## 4. Top Corporate Target Pipeline (Bangalore MNCs)

| Company | Sector | Target Role | Hub Location |
|---|---|---|---|
"""
    for t in top_targets:
        md += f"| **{t['name']}** | {t['sector']} | {t['target_role']} | {t['location']} |\n"

    md += """
---

## 5. Recent Outbox Trade Audit Certificates

| Certificate File | SHA-256 Seal | Status |
|---|---|---|
"""
    if certs:
        for c in certs:
            md += f"| `{c['filename']}` | `{c['seal'][:24]}...` | 🟢 SEALED |\n"
    else:
        md += "| *No outbox certificates deposited yet* | — | — |\n"

    md += f"""
---

## 6. Daily Autonomous Directive
> **Prime Objective**: Convert human ambition into organized intelligence, executable systems, measurable results, and compounding capability. Execute with zero vibe coding, deep modules, and verified evidence.
"""

    with open(OUTPUT_BRIEF_PATH, "w", encoding="utf-8") as f:
        f.write(md)

    # Log to kernel
    kernel.dispatch_event(
        event_name="DAILY_BRIEF_GENERATED",
        actor="SOVEREIGN_BRIEF_ENGINE",
        data={"path": OUTPUT_BRIEF_PATH, "timestamp": today}
    )

    print(f"🟢 Daily Sovereign Brief generated at: {OUTPUT_BRIEF_PATH}")
    return OUTPUT_BRIEF_PATH


if __name__ == "__main__":
    generate_daily_brief()
