#!/usr/bin/env python3
"""
========================================================================================
SKILL GAP ENGINE (GREEN / YELLOW / RED QUALIFICATION AUDITOR)
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Implements Directive 19:
  - Classifies skills into:
      GREEN  = Already qualified with documented evidence
      YELLOW = Partially qualified / transferable
      RED    = Missing or optional stretch skills
  - Computes 7-Day High-Impact Skill Plan, 30-Day Plan, and 90-Day Compounding Plan
========================================================================================
"""

from typing import Dict, List, Any

class SkillGapEngine:
    """Audits skill readiness and builds actionable high-ROI skill roadmaps."""

    QUALIFIED_GREEN = [
        "Incoterms 2020 & International Trade Compliance",
        "High-Security Ground Operations & Protocol (Aero India 2025)",
        "Vendor SLA Contract Governance & Milestone Tracking",
        "On-Ground Brand Activation Execution (Puma, Tata Comm)",
        "AI Data Quality Assurance & Annotation Workflows (Instawork)",
        "Commercial Proposal Structuring & B2B Quotations",
        "Cross-Functional Crisis De-escalation & Crowd Logistics",
        "Excel Business Modeling, Variance & Landed Cost Analysis"
    ]

    PARTIALLY_QUALIFIED_YELLOW = [
        "ERP / SAP Fundamentals & Procurement Modules",
        "Jira & Agile Sprint Tracking for Business Operations",
        "SQL Querying for Operational KPI Reporting",
        "Tableau / Power BI Operational Dashboards",
        "Six Sigma Lean Process Flow Documentation"
    ]

    STRETCH_RED = [
        "Advanced Python Scripting for Supply Chain Optimization",
        "Enterprise Salesforce Admin Architecture",
        "Global Customs Broker Licensing Certification"
    ]

    @classmethod
    def audit_profile_against_role(cls, role_title: str) -> Dict[str, Any]:
        """Returns the readiness breakdown and targeted sprint plans."""
        return {
            "target_role": role_title,
            "readiness_badges": {
                "green": cls.QUALIFIED_GREEN,
                "yellow": cls.PARTIALLY_QUALIFIED_YELLOW,
                "red": cls.STRETCH_RED
            },
            "seven_day_high_impact_plan": [
                "Day 1-2: Complete Advanced Excel for Operations Certification (INDEX/MATCH, VLOOKUP, Pivot Dashboards).",
                "Day 3-4: Build a live Landed Cost & Incoterms 2020 Freight Calculation portfolio model in Google Sheets.",
                "Day 5-6: Master Jira workflows for Operations: create an agile board simulating vendor delivery sprints.",
                "Day 7: Record a 90-second Loom/video walkthrough of the Aero India 2025 ground operations triage model."
            ],
            "thirty_day_skill_plan": [
                "Week 1: Foundations of Enterprise ERP workflows (SAP/Oracle supply chain module overviews).",
                "Week 2: SQL for Business Operations (SELECT, GROUP BY, JOINs on orders and logistics tables).",
                "Week 3: Six Sigma White/Yellow Belt concepts applied to retail logistics shrinkage reduction.",
                "Week 4: Interactive Power BI dashboard connected to simulated Bangalore FMCG supply chain data."
            ],
            "ninety_day_career_compounding_plan": [
                "Month 1: Secure placement in Tier-1 Global Business Operations / SCM analyst role in Bangalore.",
                "Month 2: Document operational SOPs and claim ownership of high-impact vendor SLA reviews.",
                "Month 3: Earn internal recognition for cross-border process efficiency improvements."
            ]
        }
