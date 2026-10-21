"""
Founders Office & CXO Special Projects Triage Engine
Automates daily operational triage, unit economics runway analysis,
board update generation, and 14-day sprint resolution roadmaps for Bangalore unicorns.
"""

import json
from datetime import datetime

class FoundersOfficeTriageEngine:
    def __init__(self, company_name, monthly_burn_inr, cash_in_bank_inr, active_verticals):
        self.company_name = company_name
        self.monthly_burn_inr = monthly_burn_inr
        self.cash_in_bank_inr = cash_in_bank_inr
        self.active_verticals = active_verticals
        self.blockers = []

    def log_blocker(self, department, description, impact_level, estimated_daily_drag_inr):
        self.blockers.append({
            "department": department,
            "description": description,
            "impact_level": impact_level,  # CRITICAL, HIGH, MEDIUM
            "estimated_daily_drag_inr": estimated_daily_drag_inr,
            "timestamp": datetime.now().isoformat()
        })

    def analyze_runway(self):
        runway_months = round(self.cash_in_bank_inr / self.monthly_burn_inr, 1) if self.monthly_burn_inr > 0 else float('inf')
        total_monthly_drag = sum(b["estimated_daily_drag_inr"] * 30 for b in self.blockers)
        adjusted_burn = self.monthly_burn_inr + total_monthly_drag
        adjusted_runway = round(self.cash_in_bank_inr / adjusted_burn, 1)
        
        return {
            "gross_monthly_burn_inr": self.monthly_burn_inr,
            "total_monthly_drag_inr": total_monthly_drag,
            "adjusted_monthly_burn_inr": adjusted_burn,
            "nominal_runway_months": runway_months,
            "adjusted_runway_months": adjusted_runway,
            "runway_deficit_months": round(runway_months - adjusted_runway, 1)
        }

    def generate_cxO_triage_memo(self):
        # Sort blockers by daily financial drag descending
        sorted_blockers = sorted(self.blockers, key=lambda x: x["estimated_daily_drag_inr"], reverse=True)
        runway = self.analyze_runway()
        
        memo = f"""# EXECUTIVE FOUNDER'S OFFICE TRIAGE MEMO: {self.company_name.upper()}
**Date:** {datetime.now().strftime('%d %b %Y')} | **Prepared by:** Tiger Team Special Projects Lead

---

## 1. Executive Runway & Burn Telemetry
- **Cash in Bank:** INR {self.cash_in_bank_inr:,}
- **Nominal Monthly Burn:** INR {self.monthly_burn_inr:,} ({runway['nominal_runway_months']} Months Runway)
- **Operational Drag (Identified Bottlenecks):** INR {runway['total_monthly_drag_inr']:,}/month
- **Adjusted Real Burn:** INR {runway['adjusted_monthly_burn_inr']:,} ({runway['adjusted_runway_months']} Months Adjusted Runway)
- **Runway Compression Warning:** Operational friction is burning {runway['runway_deficit_months']} months of runway.

---

## 2. Priority Operational Bottleneck Triage
"""
        for idx, b in enumerate(sorted_blockers, 1):
            memo += f"""
### #{idx} [{b['impact_level']}] {b['department'].upper()}: {b['description']}
- **Daily Financial Drag:** INR {b['estimated_daily_drag_inr']:,} (~INR {b['estimated_daily_drag_inr'] * 30:,}/mo)
- **Recommended Tiger Team Intervention:** Deploy 14-day dedicated sprint pod to decouple operational dependencies, automate reconciliation, and enforce strict SLA metrics.
"""

        memo += f"""
---

## 3. 14-Day Sprint Resolution Action Plan
- **Days 1–3:** Audit root cause across logs and stakeholder interviews. Map single point of failure (SPOF).
- **Days 4–8:** Build automated mitigation scripts and eliminate manual handoffs.
- **Days 9–11:** Pilot verified process in 1 operational cluster (e.g. Koramangala / Indiranagar micro-hub).
- **Days 12–14:** Full rollback/rollforward validation, deliver revised SOP, and present Board-Ready memo to CXO.
"""
        return memo

if __name__ == "__main__":
    engine = FoundersOfficeTriageEngine(
        company_name="Zepto / Quick Commerce Scaleup",
        monthly_burn_inr=65000000,
        cash_in_bank_inr=520000000,
        active_verticals=["10-Min Grocery", "Cafe Quick Snacks", "Pharma OTC"]
    )
    
    engine.log_blocker("Dark Store Logistics", "Picking queue congestion during 18:00-21:00 peak hours causing 4.2 min delivery delay", "CRITICAL", 120000)
    engine.log_blocker("Vendor Procurement", "Discrepancy in FMCG vendor delivery invoices vs warehouse barcode scanning", "HIGH", 85000)
    engine.log_blocker("Rider Fleet Ops", "Rider churn in East Bangalore corridor resulting in surging surge-pay multipliers", "CRITICAL", 145000)
    
    memo = engine.generate_cxO_triage_memo()
    print(memo)
