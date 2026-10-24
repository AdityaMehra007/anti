"""
career_growth_architect.py - Agent 7: Beyond Finding Jobs — Career Velocity & Growth Architect
=============================================================================================
Maps the candidate's trajectory beyond landing the role: 30-60-90 day onboarding dominance,
multi-year promotion ladders (Associate -> Lead -> Chief of Staff / Founders' Office),
dynamic upskilling rungs, and executive personal brand compounding.
"""

from typing import Dict, List, Any
from apex_career_os.core.truth_layer import get_candidate_profile

class CareerGrowthArchitectAgent:
    def __init__(self):
        self.candidate = get_candidate_profile()

    def generate_30_60_90_day_blueprint(self, company: str, role: str) -> Dict[str, Any]:
        """Creates an aggressive onboarding and quick-win blueprint for the first 90 days."""
        return {
            "company": company,
            "role": role,
            "day_1_to_30_listen_and_map": {
                "theme": "Operational Absorption & Seam Discovery",
                "objectives": [
                    "Map end-to-end operational workflows, key stakeholders, and primary vendors.",
                    "Audit current SLA adherence and identify recurring bottleneck friction points.",
                    "Build relationships with cross-functional peers in Product, Finance, and Legal.",
                    "Deliver 100% on-time execution on all assigned baseline tasks with zero defect."
                ],
                "deliverable": "Comprehensive Operational Workflow Map & Pain-Point Inventory"
            },
            "day_31_to_60_optimize_and_standardize": {
                "theme": "Procurement Efficiency & Process Automation",
                "objectives": [
                    "Implement direct vendor accountability trackers and standardize rate card reviews.",
                    "Introduce automated Excel / Python reporting dashboards to eliminate manual status reporting.",
                    "Execute a small-scale pilot delivering a measurable 10-15% cost or time saving.",
                    "Document Standard Operating Procedures (SOPs) for team-wide knowledge sharing."
                ],
                "deliverable": "10-15% Cost/Time Optimization Case Study & Standardized Team SOP"
            },
            "day_61_to_90_expand_and_lead": {
                "theme": "Autonomy & Strategic Initiative Ownership",
                "objectives": [
                    "Proactively identify and pitch a high-leverage initiative directly to Department Head.",
                    "Take independent ownership of high-value accounts or critical event deployments.",
                    "Mentor incoming associates or interns on operational execution standards.",
                    "Conduct a 90-day performance review with manager to set fast-track promotion milestones."
                ],
                "deliverable": "Quarterly Impact Dossier showcasing hard ROI and promotion roadmap"
            }
        }

    def generate_5_year_career_ladder(self, initial_track: str = "Operations & BD") -> Dict[str, Any]:
        """Outlines the 5-year hyper-growth promotion trajectory."""
        return {
            "track": initial_track,
            "phases": [
                {
                    "timeline": "Year 1 (Months 1 - 12)",
                    "title": "High-Performance Associate / Operations Specialist",
                    "compensation_range_lpa": "₹7.0L - ₹11.0L CTC",
                    "core_milestones": [
                        "Flawless execution of core operational SLAs.",
                        "Direct vendor rate renegotiations saving company INR 5L-10L+.",
                        "Establish reputation as the most reliable, zero-drama operator on the floor."
                    ]
                },
                {
                    "timeline": "Year 2 - 3 (Months 13 - 36)",
                    "title": "Operations Lead / Senior Business Development Manager",
                    "compensation_range_lpa": "₹14.0L - ₹22.0L CTC",
                    "core_milestones": [
                        "Lead a cross-functional pod of 5-8 operators and analysts.",
                        "Manage multi-crore procurement budgets and primary enterprise client accounts.",
                        "Lead company-wide migration to automated workflow systems."
                    ]
                },
                {
                    "timeline": "Year 4 - 5 (Months 37 - 60)",
                    "title": "Founders' Office / Chief of Staff / Operations Director",
                    "compensation_range_lpa": "₹35.0L - ₹50.0L+ CTC + ESOPs",
                    "core_milestones": [
                        "Direct strategic capital allocation, cross-border expansion, and executive initiatives.",
                        "Full P&L accountability for key business units or geographic corridors.",
                        "Sovereign-grade executive presence representing company at industry summits."
                    ]
                }
            ],
            "upskilling_and_certifications": [
                {"credential": "Six Sigma Green Belt", "focus": "Process variance reduction & Lean methodology", "recommended_timeline": "Month 6"},
                {"credential": "PMP (Project Management Professional)", "focus": "Global project governance & risk modeling", "recommended_timeline": "Month 18"},
                {"credential": "Financial Modeling & Valuation Analyst (FMVA)", "focus": "Corporate finance, M&A, and P&L mastery", "recommended_timeline": "Month 24"}
            ]
        }
