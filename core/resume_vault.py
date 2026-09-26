#!/usr/bin/env python3
"""
========================================================================================
RESUME VAULT & 12 SPECIALIZED 1-PAGE HARVARD ATS VARIANTS
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Implements Directive 15:
  Maintains and generates 12 specialized 1-page Harvard ATS resume variants:
    1. Master Operations Resume
    2. Global Business Operations & Process Analyst Resume
    3. Supply Chain, Logistics & Vendor Management Resume
    4. International Business & EXIM Operations Resume
    5. Project & Program Management Coordinator Resume
    6. Brand Activation & Ground Operations Lead Resume
    7. AI Data Quality & Platform Operations Resume
    8. Business Analyst (Global Advisory) Resume
    9. Management Trainee (Operations Track) Resume
   10. Customer Success Operations Associate Resume
   11. Consulting & Commercial Strategy Resume
   12. Startup Operations Generalist Resume
========================================================================================
"""

from typing import Dict, List, Any

class ResumeVault:
    """Manages the 12 specialized 1-page Harvard ATS resume configurations."""

    VARIANTS = {
        "1": {
            "key": "master_operations",
            "title": "Master Operations & Process Resume",
            "target_industry": "MNC Enterprise & Conglomerates",
            "summary": "Final-year BBA International Business candidate (DSU) with verified ground operations leadership at Aero India 2025, retail brand activation ops for Puma/Tata Comm, and AI data operations rigor at Instawork. Expert in Incoterms 2020, vendor SLA contracts, and SOP governance.",
            "skills_emphasized": ["Operations Management", "SOP Governance", "Vendor SLAs", "Aero India Lead Ops", "Incoterms 2020", "AI Data Quality"]
        },
        "2": {
            "key": "global_biz_ops",
            "title": "Global Business Operations & Process Analyst",
            "target_industry": "Global Capability Centers (GCCs) & IT/BPS",
            "summary": "Data-disciplined Business Operations Analyst specializing in cross-border workflow mapping, vendor rate card structuring, and SOP compliance. Proven track record managing multi-tier operational logistics with zero shrinkage and 100% milestone adherence.",
            "skills_emphasized": ["Business Process Mapping", "KPI Tracking", "SOP Governance", "Vendor Rate Structuring", "Variance Analysis"]
        },
        "3": {
            "key": "supply_chain_logistics",
            "title": "Supply Chain, Logistics & Vendor Management",
            "target_industry": "E-commerce, FMCG & Fulfillment",
            "summary": "Supply chain operations specialist with extensive ground experience managing high-velocity inventory flow, supplier SLAs, and load-in/load-out staging across high-density Bangalore venues.",
            "skills_emphasized": ["Inventory Staging", "Vendor Contract Enforcement", "Reverse Logistics", "Stockout Elimination", "Fulfillment SLAs"]
        },
        "4": {
            "key": "exim_trade_ops",
            "title": "International Business & EXIM Operations",
            "target_industry": "Global Trade, Freight Forwarding & Customs",
            "summary": "International Business graduate grounded in Incoterms 2020 (FOB, CIF, DDP), customs tariff compliance, and Letter of Credit (UCP 600) documentation. Deep knowledge of cross-border trade risk modeling.",
            "skills_emphasized": ["Incoterms 2020", "Customs Clearance Procedures", "HS Tariff Codes", "Letter of Credit (LC)", "Landed Cost Optimization"]
        },
        "5": {
            "key": "program_management",
            "title": "Project & Program Management Coordinator",
            "target_industry": "Enterprise Consulting & Tech Ops",
            "summary": "Execution-focused Program Coordinator adept at managing cross-functional dependencies, critical path scheduling, and stakeholder alignment. Directed 25+ ground crew across 300+ live deployments.",
            "skills_emphasized": ["Milestone Scheduling", "Run-of-Show Governance", "Stakeholder Triage", "Jira/Agile Coordination", "Risk Mitigation"]
        },
        "6": {
            "key": "event_ground_ops",
            "title": "Brand Activation & Ground Operations Lead",
            "target_industry": "Experiential Agencies & Large Venues",
            "summary": "Exhibition & Ground Operations Lead with verified credential managing Aero India 2025 (100k+ attendees at Yelahanka AFB) and on-ground activations for Puma, Tata Communications, and Decathlon.",
            "skills_emphasized": ["High-Security VIP Protocol", "Crowd Flow Triage", "Venue Safety Regulations", "Crisis Management", "On-Ground Staging"]
        },
        "7": {
            "key": "ai_data_ops",
            "title": "AI Data Quality & Platform Operations",
            "target_industry": "AI Startups & Data Infrastructure",
            "summary": "Operational Data Specialist with proven experience at Instawork AI conducting high-accuracy data annotation, QA validation, and error taxonomy structuring. Achieved 99%+ accuracy benchmarks.",
            "skills_emphasized": ["AI Data Annotation", "QA Validation Workflows", "Algorithmic Ground Truth", "Error Taxonomy", "Platform SOPs"]
        },
        "8": {
            "key": "business_analyst",
            "title": "Business Analyst (Global Advisory)",
            "target_industry": "Management Consulting & Advisory",
            "summary": "Analytical BBA IB candidate experienced in translating operational bottlenecks into structured business solutions. Proficient in quantitative variance analysis, landed cost modeling, and executive presentations.",
            "skills_emphasized": ["Quantitative Modeling", "Cost-Benefit Analysis", "Process Re-engineering", "Executive Pitch Decks", "Data Synthesis"]
        },
        "9": {
            "key": "management_trainee",
            "title": "Management Trainee (Operations Track)",
            "target_industry": "Top 100 Indian Enterprises & MNCs",
            "summary": "High-potential Management Trainee candidate bringing verified operational leadership from Asia's premier defense expo, strong commercial acumen, and rapid problem-solving capabilities.",
            "skills_emphasized": ["Rapid Learning Agility", "Cross-Functional Leadership", "Commercial Acumen", "Operational Rigor", "Ethics & Governance"]
        },
        "10": {
            "key": "customer_success_ops",
            "title": "Customer Success Operations Associate",
            "target_industry": "B2B SaaS & Tech Platforms",
            "summary": "Customer-facing Operations Associate focused on client onboarding speed, SLA governance, and operational handover efficiency. Improved commercial conversion timelines by 18% in B2B projects.",
            "skills_emphasized": ["Client Onboarding Workflows", "SLA Monitoring", "Escalation Triage", "Retention Operations", "CRM Data Hygiene"]
        },
        "11": {
            "key": "consulting_strategy",
            "title": "Consulting & Commercial Strategy Analyst",
            "target_industry": "B2B Advisory & Boutique Consulting",
            "summary": "Strategy Analyst with expertise in market research, commercial proposal structuring, and competitive intelligence for Bangalore commercial enterprises.",
            "skills_emphasized": ["Market Landscaping", "Proposal Structuring", "Commercial Quotation Models", "Competitive Benchmarking"]
        },
        "12": {
            "key": "startup_generalist",
            "title": "Startup Operations Generalist",
            "target_industry": "Early & Growth-Stage Startups",
            "summary": "Adaptable Operations Generalist capable of owning whatever needs to be executed: vendor staging, client proposals, event setup, data QA, and team coordination. Zero ego, 100% execution.",
            "skills_emphasized": ["High Operational Speed", "Resourcefulness", "Vendor Scrappy Negotiation", "Cross-Domain Agility", "Problem Ownership"]
        }
    }

    @classmethod
    def list_variants(cls) -> List[Dict[str, Any]]:
        return [{"id": k, **v} for k, v in cls.VARIANTS.items()]

    @classmethod
    def get_variant(cls, key_or_id: str) -> Dict[str, Any]:
        for k, v in cls.VARIANTS.items():
            if k == key_or_id or v["key"] == key_or_id:
                return {"id": k, **v}
        return {"id": "1", **cls.VARIANTS["1"]}
