#!/usr/bin/env python3
"""
========================================================================================
OMEGA CAREER PATH SIMULATOR & SKILL GAP ENGINE (v8.0)
========================================================================================
Models 5 strategic trajectory scenarios and computes actionable skill-gap projects.
========================================================================================
"""

import os, json
from datetime import datetime
from typing import Dict, List, Any

class OmegaCareerSimulator:
    SCENARIOS = {
        "SAFE": {
            "title": "Established MNC Operations & Advisory Path",
            "target_employers": ["Accenture", "Deloitte", "EY GDS", "IBM India", "PwC"],
            "entry_role": "Global Operations Analyst / Advisory Trainee",
            "year_3_role": "Senior Operations Consultant",
            "year_5_role": "Operations Manager / Engagement Lead",
            "expected_compensation_inr": {"entry": "6.5L - 9.0L", "year_3": "14.0L - 18.0L", "year_5": "24.0L - 32.0L"},
            "optionality_score": 8.0,
            "risk_profile": "LOW (High Stability, Structured Brand Equity)",
            "key_strategic_focus": "Process standardisation, corporate governance, and client delivery."
        },
        "HIGH_GROWTH": {
            "title": "High-Velocity Brand & Event Operations Lead",
            "target_employers": ["Puma Global", "Red Bull", "Live Nation", "Zomato Events", "Hyper-Growth D2C"],
            "entry_role": "Event Operations & Activation Specialist",
            "year_3_role": "Head of Experiential Operations",
            "year_5_role": "Director of Brand Activations & Live Operations",
            "expected_compensation_inr": {"entry": "7.5L - 11.0L", "year_3": "18.0L - 26.0L", "year_5": "35.0L - 50.0L"},
            "optionality_score": 9.0,
            "risk_profile": "MEDIUM (High Velocity, Rapid Execution Accountability)",
            "key_strategic_focus": "Marquee expo governance (Aero India scale), sponsor revenue, and experiential production."
        },
        "HIGH_INCOME": {
            "title": "Global Markets & Financial Risk Track",
            "target_employers": ["Goldman Sachs", "JPMorgan Chase", "Swiss Re", "Morgan Stanley"],
            "entry_role": "Global Markets Operations Analyst",
            "year_3_role": "Senior Risk & Trade Operations Specialist",
            "year_5_role": "Vice President - Operations & Trading Support",
            "expected_compensation_inr": {"entry": "9.0L - 14.0L", "year_3": "22.0L - 30.0L", "year_5": "45.0L - 75.0L+"},
            "optionality_score": 8.5,
            "risk_profile": "MEDIUM-HIGH (High Performance Bar, Long Working Hours)",
            "key_strategic_focus": "Trade reconciliation, cross-border regulatory compliance, and risk containment."
        },
        "GLOBAL": {
            "title": "International Trade & Cross-Border Supply Chain Specialist",
            "target_employers": ["Boeing India", "TE Connectivity", "Cisco", "Maersk", "DHL Global"],
            "entry_role": "Global Supply Chain & EXIM Analyst",
            "year_3_role": "International Trade Compliance Manager",
            "year_5_role": "Regional Supply Chain Director (APAC / EMEA)",
            "expected_compensation_inr": {"entry": "7.0L - 10.5L", "year_3": "16.0L - 22.0L", "year_5": "30.0L - 48.0L (International Mobility)"},
            "optionality_score": 9.5,
            "risk_profile": "LOW-MEDIUM (Global Transferability, Essential Trade Infrastructure)",
            "key_strategic_focus": "Incoterms 2020, customs brokerage, landed cost arbitrage, and freight optimization."
        },
        "ENTREPRENEURIAL": {
            "title": "Sovereign Event Operations Agency & AI Automation Studio",
            "target_employers": ["Self-Founded (Nexus Omega / Sovereign Agency)"],
            "entry_role": "Founder & Managing Partner",
            "year_3_role": "Agency Principal (10-Person Team, 20+ Corporate Accounts)",
            "year_5_role": "Multi-Venture Holding Principal",
            "expected_compensation_inr": {"entry": "Variable (3L - 15L)", "year_3": "30L - 60L Profit", "year_5": "1.0 Cr+ Revenue / Equity Value"},
            "optionality_score": 10.0,
            "risk_profile": "HIGH (Requires Continuous Pipeline Generation & Capital Discipline)",
            "key_strategic_focus": "Productized event operations, automated B2B pipeline systems, and vendor arbitrage."
        }
    }

    SKILL_GAPS = [
        {
            "target_skill": "Advanced SQL & Relational Data Lakehouses",
            "current_status": "FOUNDATIONAL (SQLite & Python data scripting)",
            "gap_severity": "LOW-MEDIUM",
            "career_impact": "HIGH",
            "recommended_portfolio_project": "Build an automated SQLite/PostgreSQL ETL pipeline linking LinkedIn export to live job scraping APIs with automated deduplication."
        },
        {
            "target_skill": "Power BI / Tableau Interactive Financial Dashboards",
            "current_status": "INTERMEDIATE (Excel financial modeling & HTML/CSS dashboards)",
            "gap_severity": "LOW",
            "career_impact": "HIGH",
            "recommended_portfolio_project": "Publish a public Power BI dashboard analyzing Bangalore GCC hiring trends and Big 4 compensation distributions."
        },
        {
            "target_skill": "Formal Customs Brokerage & Advanced Incoterms Certification",
            "current_status": "ACADEMIC (DSU BBA-IB Coursework)",
            "gap_severity": "LOW",
            "career_impact": "MEDIUM-HIGH",
            "recommended_portfolio_project": "Author a 10-page verified whitepaper on Landed Cost Optimization for India-EU Defense & Aviation Components."
        }
    ]

    def generate_simulation_report(self, output_md: str = r"e:\anti\CAREER_SIMULATION_REPORT.md") -> str:
        now_str = datetime.now().strftime("%Y-%m-%d")
        md = f"""# ?? OMEGA CAREER PATH SIMULATOR
**Generated:** `{now_str}`  
**Candidate:** `Aditya Mehra` (BBA-IB, Dayananda Sagar University)  
**Evaluation Scope:** 5 Strategic Trajectory Models (5-Year Horizon)

---

## ??? 1. COMPARATIVE STRATEGY MATRIX

| Scenario | Entry Target Role | Year 3 Trajectory | Year 5 Compensation (INR) | Risk / Stability Profile | Optionality |
|---|---|---|---|---|---|
| **1. SAFE (MNC Advisory)** | Operations Analyst | Senior Consultant | **24.0L - 32.0L** | Low / High Stability | 8.0/10 |
| **2. HIGH-GROWTH (Live Ops)** | Event Ops Lead | Head of Activations | **35.0L - 50.0L** | Med / Rapid Acceleration | 9.0/10 |
| **3. HIGH-INCOME (Markets)** | Global Markets Analyst | VP Operations | **45.0L - 75.0L+** | Med-High / High Intensity | 8.5/10 |
| **4. GLOBAL (Trade & EXIM)** | Supply Chain Specialist | Regional Director | **30.0L - 48.0L (Global Mobility)** | Low-Med / International | 9.5/10 |
| **5. ENTREPRENEURIAL (Studio)** | Founder (Nexus Omega) | Agency Principal | **1.0 Cr+ Revenue / Equity** | High / Maximum Leverage | 10.0/10 |

---

## ?? 2. SCENARIO DEEP-DIVES

"""
        for code, sc in self.SCENARIOS.items():
            md += f"""### ?? Scenario: `{code}` ? {sc['title']}
- **Target Employers:** {', '.join(sc['target_employers'])}
- **Career Ladder:** `{sc['entry_role']}` ? `{sc['year_3_role']}` ? `{sc['year_5_role']}`
- **Compensation Trajectory (INR):** Entry: `{sc['expected_compensation_inr']['entry']}` | Year 3: `{sc['expected_compensation_inr']['year_3']}` | Year 5: `{sc['expected_compensation_inr']['year_5']}`
- **Strategic Focus:** {sc['key_strategic_focus']}
- **Risk Assessment:** {sc['risk_profile']}

---
"""
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Simulation Report saved at {output_md}")
        return output_md

    def generate_skill_gap_report(self, output_md: str = r"e:\anti\SKILL_GAP_ANALYSIS.md") -> str:
        now_str = datetime.now().strftime("%Y-%m-%d")
        md = f"""# ?? OMEGA SKILL GAP ANALYSIS & PORTFOLIO FACTORY
**Generated:** `{now_str}`  
**Framework:** Target Role Requirements vs. Master Verified Profile  

---

## 1. IDENTIFIED SKILL GAPS & MITIGATION MATRIX

"""
        for i, gap in enumerate(self.SKILL_GAPS, 1):
            md += f"""### {i}. `{gap['target_skill']}`
- **Current Standing:** {gap['current_status']}
- **Gap Severity:** `{gap['gap_severity']}` | **Career ROI Impact:** `{gap['career_impact']}`
- **Recommended Proof-of-Work Project:**  
  *{gap['recommended_portfolio_project']}*

---
"""
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Skill Gap Report saved at {output_md}")
        return output_md


if __name__ == "__main__":
    sim = OmegaCareerSimulator()
    sim.generate_simulation_report()
    sim.generate_skill_gap_report()
