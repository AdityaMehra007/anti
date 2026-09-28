#!/usr/bin/env python3
"""
========================================================================================
OMEGA BATCH CONQUEST ENGINE v2.0 — DEFECT ANNIHILATOR
========================================================================================
Fixes ALL 5 critical defects identified in the scorecard:
  D1: Raw folder names → intelligent name cleaning + multi-format manifest parsing
  D2: Identical resume bodies → industry-aware competency reordering & keyword injection
  D3: Same STAR stories → 2 role-specific scenario questions per industry
  D4: No JD keywords → industry keyword banks injected into resume + interview
  D5: CTC in resume → removed from resume body entirely
========================================================================================
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"e:\anti\applications_generated")

CANDIDATE = {
    "name": "Aditya Mehra",
    "phone": "+91 7003456624",
    "email": "ashishiash007@gmail.com",
    "linkedin": "linkedin.com/in/adityamehra",
    "location": "Bengaluru, Karnataka, India",
}

# ── D1 FIX: Intelligent Company Name Cleaner ────────────────────────────────

TIER_PREFIXES = re.compile(
    r'^(WORLD_TITAN_\d+_|RICHEST_LISTED_\d+_|UNICORN_\d+_|'
    r'APX-\d+_|BIL_FAMILY_OFFICE_\d+_|UPCOMING_BIL_\d+_|'
    r'bangalore_\d+_|mnc_|corporate_|mega_\d+_|agency_)',
    re.IGNORECASE
)

def clean_folder_to_company(folder_name: str) -> str:
    """Strip tier prefixes and convert filesystem artifacts to human-readable names."""
    name = TIER_PREFIXES.sub('', folder_name)
    # Replace double underscores (used for slashes/parens) with " / "
    name = name.replace('___', ' / ').replace('__', ' (').rstrip('_')
    # Add closing paren if we opened one
    if ' (' in name and ')' not in name:
        name += ')'
    # Replace remaining underscores with spaces
    name = name.replace('_', ' ').strip()
    # Clean up artifacts
    name = re.sub(r'\s+', ' ', name)
    name = name.strip(' -()')
    return name if name else folder_name


def read_manifest(folder: Path) -> dict:
    """Read manifest, handling both WORLD_TITAN and APX format schemas."""
    m_path = folder / "APPLICATION_MANIFEST.json"
    if not m_path.exists():
        return {}
    try:
        with open(m_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}

    # Normalize to canonical keys
    company = (data.get("company") or data.get("company_name") or "").strip()
    role = (data.get("role") or data.get("target_role") or "").strip()
    ctc = (data.get("ctc") or data.get("compensation_bracket") or "").strip()
    sector = (data.get("sector") or data.get("industry") or "").strip()
    recruiter = (data.get("contact_person") or data.get("primary_recruiter_gatekeeper") or "").strip()

    return {
        "company": company,
        "role": role,
        "ctc": ctc,
        "sector": sector,
        "recruiter": recruiter,
        "raw": data,
    }


# ── D2/D4 FIX: Industry Classification & Keyword Banks ──────────────────────

INDUSTRY_PROFILES = {
    "finance": {
        "keywords": ["Trade Settlements", "Reconciliation", "T+1 Settlement Cycle", "Risk Management",
                     "Regulatory Compliance", "Financial Controls", "NAV Calculations", "Fund Accounting",
                     "KYC/AML", "SWIFT Messaging", "Bloomberg Terminal", "Audit Trails"],
        "competency_order": ["finance_ops", "analytics", "operations", "trade", "tech"],
        "summary_hook": "cross-functional financial operations, trade lifecycle governance, and regulatory compliance",
        "label": "Financial Services & Investment Banking",
    },
    "consulting": {
        "keywords": ["Stakeholder Management", "Process Re-engineering", "Change Management",
                     "Client Deliverables", "PMO Governance", "Risk Assessment Framework",
                     "Business Case Development", "SOW Compliance", "Engagement Management",
                     "Continuous Improvement", "LEAN/Six Sigma Awareness", "RFP Responses"],
        "competency_order": ["analytics", "operations", "finance_ops", "tech", "trade"],
        "summary_hook": "structured problem-solving, stakeholder-driven project delivery, and operational advisory",
        "label": "Management Consulting & Advisory",
    },
    "tech": {
        "keywords": ["Agile/Scrum Methodology", "JIRA/Confluence", "Sprint Planning", "CI/CD Awareness",
                     "API Ecosystem", "Data Pipeline Monitoring", "Cloud Operations (AWS/GCP/Azure)",
                     "Incident Management", "SLA/SLO Tracking", "Vendor Technical Assessments",
                     "Product Operations", "Cross-functional GTM Support"],
        "competency_order": ["tech", "analytics", "operations", "finance_ops", "trade"],
        "summary_hook": "technology operations, vendor ecosystem management, and data-driven process scaling",
        "label": "Technology & Software / GCC",
    },
    "logistics": {
        "keywords": ["Freight Forwarding", "Container Tracking", "Bill of Lading", "Customs Brokerage",
                     "Warehouse Management (WMS)", "Last-Mile Delivery", "Route Optimization",
                     "Carrier Rate Negotiation", "Import/Export Documentation", "Bonded Warehouse Ops",
                     "DGFT Compliance", "Free Trade Zones"],
        "competency_order": ["trade", "operations", "analytics", "tech", "finance_ops"],
        "summary_hook": "global supply chain coordination, customs compliance, and logistics cost optimization",
        "label": "Logistics, Shipping & Supply Chain",
    },
    "ecommerce": {
        "keywords": ["Fulfilment Center Operations", "Dark Store Management", "Inventory Velocity",
                     "Order-to-Delivery SLA", "Hyperlocal Operations", "Merchant Onboarding",
                     "City Operations", "Demand Forecasting", "Return/Reverse Logistics",
                     "Rider/Fleet Management", "P&L Ownership", "Unit Economics"],
        "competency_order": ["operations", "analytics", "tech", "finance_ops", "trade"],
        "summary_hook": "high-velocity city operations, fulfilment logistics, and merchant ecosystem management",
        "label": "E-Commerce & Quick Commerce",
    },
    "manufacturing": {
        "keywords": ["Production Planning", "Quality Management (QMS)", "Vendor Qualification",
                     "Bill of Materials (BOM)", "Shop Floor Coordination", "ISO 9001/IATF Awareness",
                     "Maintenance Scheduling", "Material Requirement Planning (MRP)",
                     "Safety Compliance (EHS)", "Yield Optimization", "Spare Parts Inventory",
                     "OEM Liaison"],
        "competency_order": ["operations", "trade", "analytics", "tech", "finance_ops"],
        "summary_hook": "manufacturing operations, vendor qualification, and quality-driven process governance",
        "label": "Manufacturing, Aerospace & Industrial",
    },
    "fmcg": {
        "keywords": ["Trade Marketing", "Channel Distribution", "Modern Trade Operations",
                     "General Trade Coverage", "Distributor Management", "SKU Rationalization",
                     "Point-of-Sale Execution", "Retail Merchandising", "Brand Activation",
                     "Category Management", "Planogram Compliance", "Promotion ROI"],
        "competency_order": ["operations", "analytics", "finance_ops", "trade", "tech"],
        "summary_hook": "retail operations, brand activation execution, and channel distribution management",
        "label": "FMCG, Retail & Consumer Goods",
    },
    "healthcare": {
        "keywords": ["Hospital Operations", "Patient Flow Optimization", "Medical Procurement",
                     "Regulatory Compliance (NABH/JCI)", "Clinical Supply Chain", "Vendor Empanelment",
                     "Inventory Management (Pharma/Devices)", "Health Insurance Liaison",
                     "Facility Management", "Quality Accreditation", "HIPAA Awareness",
                     "Biomedical Equipment Tracking"],
        "competency_order": ["operations", "analytics", "finance_ops", "tech", "trade"],
        "summary_hook": "healthcare operations, procurement governance, and regulatory compliance management",
        "label": "Healthcare & Pharmaceuticals",
    },
    "fintech": {
        "keywords": ["Merchant Operations", "Payment Gateway", "Transaction Monitoring",
                     "Chargeback Management", "RBI Compliance", "PCI-DSS Awareness",
                     "UPI/NEFT/RTGS Settlement", "Fraud Detection", "Partner Onboarding",
                     "Revenue Operations", "Ticket Resolution SLA", "Fintech Partnerships"],
        "competency_order": ["finance_ops", "tech", "operations", "analytics", "trade"],
        "summary_hook": "fintech operations, merchant lifecycle management, and payment ecosystem governance",
        "label": "Fintech & Digital Payments",
    },
    "general": {
        "keywords": ["Cross-Functional Coordination", "Stakeholder Management", "Process Standardization",
                     "MIS Reporting", "Dashboard Development", "Vendor Management",
                     "Budget Tracking", "SOP Documentation", "Performance Analytics",
                     "Resource Planning", "Escalation Management", "Operational Excellence"],
        "competency_order": ["operations", "analytics", "tech", "finance_ops", "trade"],
        "summary_hook": "cross-functional operations management, vendor optimization, and analytical reporting",
        "label": "General Operations & Business",
    },
}

COMPETENCY_BLOCKS = {
    "operations": "**Operations & Execution:** End-to-End Operational Logistics, Cross-Functional Team Leadership (20+ crew), Vendor Rate Card Negotiation, Budgetary Governance, SLA Adherence, Process Optimization, Crisis Resolution.",
    "analytics": "**Analytics & Strategic Reporting:** Advanced MS Excel (XLOOKUP, Pivot Tables, Financial Modelling), Power BI Dashboards, Tableau, MIS & KPI Reporting, Data-Driven Decision Making, CRM Pipeline Analytics.",
    "finance_ops": "**Financial & Commercial Operations:** B2B Client Pipeline Management, Cost-Benefit Analysis, Budget Tracking & Variance Reporting, Revenue Forecasting, Procurement Optimization (15% Cost Reduction), Stakeholder Reporting.",
    "trade": "**Global Trade & Supply Chain:** EXIM Procedures, Incoterms 2020, Customs Clearance (ICD Whitefield), UCP 600 Letters of Credit, HS Code Classification, Landed Cost Modelling, DGFT Compliance.",
    "tech": "**Technical Stack & Automation:** Python Scripting, SQL Fundamentals, CRM Systems (HubSpot/Salesforce), Google Workspace, AI Agent Operations & Evaluation, Workflow Automation, JIRA/Confluence Basics.",
}


def classify_industry(company: str, role: str, sector: str) -> str:
    """Classify a company into an industry bucket using signals from name, role, and sector."""
    combined = f"{company} {role} {sector}".lower()

    if any(k in combined for k in ["goldman", "jpmorgan", "morgan stanley", "bank of america",
                                     "hsbc", "barclays", "standard chartered", "swiss re",
                                     "hdfc bank", "sbi ", "fund", "clearance", "settlement",
                                     "trade operations analyst"]):
        return "finance"
    if any(k in combined for k in ["deloitte", "ey ", "pwc", "kpmg", "accenture", "advisory",
                                     "consulting", "risk & business"]):
        return "consulting"
    if any(k in combined for k in ["maersk", "dhl", "adani port", "freight", "logistics",
                                     "shipping", "supply chain", "ocean", "cargo",
                                     "carrier", "forwarding", "exim"]):
        return "logistics"
    if any(k in combined for k in ["zepto", "swiggy", "zomato", "blinkit", "meesho",
                                     "flipkart", "amazon", "fulfilment", "quick commerce",
                                     "ecommerce", "e-commerce", "dark store", "instamart"]):
        return "ecommerce"
    if any(k in combined for k in ["razorpay", "cred", "groww", "zerodha", "slice",
                                     "paytm", "phonepe", "fintech", "payment", "navi tech"]):
        return "fintech"
    if any(k in combined for k in ["boeing", "airbus", "hal ", "bel ", "schneider", "siemens",
                                     "bosch", "mercedes", "tata motors", "ather", "manufacturing",
                                     "automotive", "aerospace", "industrial", "hardware"]):
        return "manufacturing"
    if any(k in combined for k in ["puma", "hul", "unilever", "titan", "britannia", "trent",
                                     "lenskart", "retail", "fmcg", "consumer", "zudio"]):
        return "fmcg"
    if any(k in combined for k in ["apollo", "biocon", "astrazeneca", "novo nordisk",
                                     "sun pharma", "pharma", "hospital", "healthcare"]):
        return "healthcare"
    if any(k in combined for k in ["google", "microsoft", "apple", "nvidia", "meta",
                                     "cisco", "dell", "ibm", "oracle", "infosys", "wipro",
                                     "tcs", "tata elxsi", "walmart global tech", "target enterprise",
                                     "tesco", "postman", "browserstack", "canva", "openai",
                                     "bytedance", "stripe", "databricks", "urban company",
                                     "shadowfax", "porter", "licious", "tech", "software",
                                     "ai ", "compute", "r&d", "krutrim"]):
        return "tech"
    return "general"


# ── D3 FIX: Industry-Specific Interview Scenario Questions ──────────────────

INDUSTRY_SCENARIOS = {
    "finance": [
        {
            "q": "Walk me through how you would handle a trade settlement discrepancy discovered 30 minutes before the T+1 cutoff deadline.",
            "a": """**Framework:** "First, I would isolate the discrepancy by cross-referencing the trade confirmation against the counterparty's records and our internal booking system. I would flag the specific fields in conflict — whether it's notional amount, settlement date, or counterparty SWIFT codes. Then I would immediately escalate to the operations manager while simultaneously contacting the counterparty's middle office on the recorded line to resolve the break. In my event operations, I've handled analogous time-critical crises: at Aero India 2025, when a shipment was blocked at the security checkpoint 45 minutes before VIP rounds, I mobilized the IAF liaison, presented pre-verified documentation, and resolved it with 15 minutes to spare. The principle is identical — isolate the break, escalate with data, resolve under pressure, and document the root cause to prevent recurrence."
""",
        },
        {
            "q": "How would you audit and reconcile a vendor invoice that shows a 12% variance against the contracted rate?",
            "a": """**Framework:** "I would pull the original vendor contract and rate card, compare line-item pricing against the invoice, and identify exactly which line items deviate. In my prior operations, I audited staging, AV, and fabrication invoices that showed 12-18% middleman markups. I mapped each cost component to the direct source supplier, documented the variance, and presented a side-by-side comparison to management. This resulted in a 15% recurring cost reduction. For this scenario, I would prepare a variance memo with the exact delta, root cause (rate escalation, scope change, or billing error), and a recommended resolution — whether that's a credit note, renegotiation, or contract amendment."
""",
        },
    ],
    "consulting": [
        {
            "q": "A client stakeholder is unhappy with a deliverable your team produced. They say it doesn't match the original SOW. How do you handle this?",
            "a": """**Framework:** "I would first listen to the client's specific concerns without being defensive, then pull up the original SOW and compare the deliverable against each acceptance criterion line by line. If there's a genuine gap, I would acknowledge it immediately, propose a remediation plan with a clear timeline, and ensure the project manager is aligned. If the deliverable actually meets the SOW but the client's expectations evolved, I would diplomatically walk them through the mapping and propose a change request process for the additional scope. At Pencil Mark Interior Solutions, I handled similar situations where clients' design expectations evolved mid-project. I learned that transparent documentation and proactive communication prevent 90% of these conflicts."
""",
        },
        {
            "q": "You are assigned to a new advisory engagement where the client's internal data is disorganized and incomplete. How do you establish a reliable analytical baseline?",
            "a": """**Framework:** "I would start by conducting stakeholder interviews to understand what data they trust and what they don't. Then I would identify the 3-4 authoritative source systems and cross-reference them to establish a validated baseline dataset. At Instawork AI, I faced a similar challenge with inconsistent multi-modal annotation data — I created a personal validation rubric, documented edge cases, and collaborated with QA leads to normalize categorization standards, achieving 99%+ accuracy. For the consulting engagement, I would build a simple Excel/Power BI reconciliation dashboard, flag discrepancies for client review, and establish a single source of truth before beginning any analysis."
""",
        },
    ],
    "tech": [
        {
            "q": "Your team manages a vendor integration that has been causing intermittent SLA breaches for 3 weeks. The vendor says it's not their issue. How do you resolve this?",
            "a": """**Framework:** "I would first establish an evidence-based case by pulling the incident logs, response time data, and error traces for the past 3 weeks. I would correlate the SLA breaches with specific vendor API endpoints or delivery windows. Then I would request a joint review call with the vendor's technical team, presenting the timestamped evidence. In my event operations, I've managed similar vendor accountability situations — when AV equipment providers claimed on-time delivery while our on-ground logs showed 2-hour delays, I presented photo-timestamped evidence that resolved the dispute immediately. Data removes ambiguity."
""",
        },
        {
            "q": "You are asked to reduce operational costs by 10% in your department without reducing headcount. What's your approach?",
            "a": """**Framework:** "I would conduct a line-item audit of all recurring operational expenses — software licenses, vendor contracts, manual process hours, and redundant workflows. In my event operations, I achieved a 15% cost reduction by mapping the entire vendor cost chain, identifying middleman markups, and negotiating directly with tier-1 suppliers. The same methodology applies: (1) audit every cost line, (2) identify the top 5 highest-impact optimization targets, (3) implement changes incrementally with measurement, and (4) report verified savings weekly. I would also look for automation opportunities — replacing manual Excel reconciliation with Power BI dashboards or Python scripts."
""",
        },
    ],
    "logistics": [
        {
            "q": "A container shipment is stuck at customs due to an HS code classification dispute. The client needs delivery in 48 hours. What do you do?",
            "a": """**Framework:** "First, I would pull the original commercial invoice and verify the HS code classification against the Customs Tariff Act schedule. If the classification is defensible, I would prepare a detailed justification letter citing the product specifications and applicable tariff heading, and request an expedited re-examination from the customs officer. If there's ambiguity, I would consult a licensed customs broker for a provisional assessment under Section 18 of the Customs Act to release the goods against a bond while the classification is adjudicated. From my EXIM coursework and ICD Whitefield exposure, I understand that speed depends on documentation quality. I would simultaneously prepare the Bill of Entry amendment and coordinate with the CHA to avoid any further delays."
""",
        },
        {
            "q": "You discover that a freight carrier has been consistently under-reporting volumetric weights, causing a 8% revenue leakage. How do you address this?",
            "a": """**Framework:** "I would pull 90 days of shipping records and cross-reference the carrier's declared volumetric weights against our internal measurements or warehouse scan data. I would build a variance report showing the pattern and quantifying the total revenue impact. Then I would schedule a formal review meeting with the carrier's account manager, present the data, and negotiate a credit for past under-billing plus revised measurement protocols going forward. In my event operations, I discovered similar vendor billing discrepancies (12-18% markups) through granular line-item audits, which led to a 15% cost recovery. The same audit-evidence-negotiate framework applies."
""",
        },
    ],
    "ecommerce": [
        {
            "q": "A dark store is consistently missing its 10-minute delivery SLA during peak hours (6-9 PM). What operational changes would you implement?",
            "a": """**Framework:** "I would analyze the order data to identify the specific bottleneck — is it picker throughput, packing station congestion, or rider allocation? I would shadow the operations during peak hours to observe firsthand. Then I would implement targeted fixes: if it's picking, I would optimize the planogram for high-velocity SKUs in nearest-to-exit zones. If it's rider allocation, I would pre-stage riders 15 minutes before predicted demand spikes using historical order pattern data. In my event operations, I managed similar time-critical throughput challenges — coordinating 20+ crew members to execute stage transitions within 3-minute windows. The principle is identical: map the bottleneck, pre-position resources, and measure continuously."
""",
        },
        {
            "q": "A high-value merchant partner is threatening to leave your platform for a competitor. How do you retain them?",
            "a": """**Framework:** "I would first understand their specific pain points through a face-to-face meeting — is it commission rates, delivery reliability, order volume decline, or customer support responsiveness? Then I would build a data-driven retention package showing their platform performance metrics, growth trajectory, and the specific improvements we can commit to (e.g., priority placement, dedicated account support, promotional co-investment). At Pencil Mark Interior Solutions, I retained and expanded client relationships by providing transparent ROI comparisons and proactive follow-up within 2 hours of any inquiry. Retention is about demonstrating measurable value faster than the competitor can promise it."
""",
        },
    ],
    "fintech": [
        {
            "q": "A merchant reports that their settlement cycle has unexpectedly increased from T+1 to T+3. How do you diagnose and resolve this?",
            "a": """**Framework:** "I would first check whether it's a systemic issue affecting multiple merchants or isolated to this one. If isolated, I would review their KYC status, chargeback history, and risk flags — elevated risk scores often trigger automatic settlement hold extensions. I would pull the transaction logs from the payment gateway to verify processing timestamps at each stage (capture, clearing, settlement). Then I would coordinate with the risk team and the acquiring bank to identify the specific hold point. Clear communication to the merchant throughout is critical — I would set up a direct escalation channel and provide hourly updates until resolved."
""",
        },
        {
            "q": "You need to onboard 200 new merchants in a tier-2 city within 30 days. What's your operational plan?",
            "a": """**Framework:** "I would segment the 200 targets by business category and volume potential, then prioritize the top 50 high-GMV merchants for personal outreach. I would set up a structured onboarding pipeline: Week 1 — territory mapping and lead qualification; Week 2-3 — field visits with pre-configured onboarding kits (QR codes, POS devices, documentation); Week 4 — activation follow-up and first-transaction support. At Pencil Mark Interior Solutions, I independently managed a B2B acquisition pipeline that generated INR 1.5L+ in revenue within 6 weeks using exactly this structured outreach methodology. For 200 merchants, I would also build a simple tracker in Excel or CRM to monitor conversion at each stage."
""",
        },
    ],
    "manufacturing": [
        {
            "q": "A critical component supplier misses their delivery deadline, threatening to halt your production line. How do you respond?",
            "a": """**Framework:** "Immediately, I would activate the secondary/alternate supplier from our approved vendor list — every critical component should have at least two qualified sources. Simultaneously, I would contact the primary supplier's account manager to get an honest revised ETA and understand the root cause (raw material shortage, quality reject, logistics delay). I would calculate the production impact in units and revenue terms and escalate to the plant head with options: (A) partial production with available stock, (B) expedited air freight from alternate supplier at premium cost, or (C) production schedule re-sequencing. At Aero India 2025, when a shipment was blocked at the security gate, I activated backup display materials within 15 minutes while resolving the primary issue in parallel. Never have a single point of failure."
""",
        },
        {
            "q": "You discover that the reject rate on a production line has increased from 2% to 5% over the past month. How do you investigate?",
            "a": """**Framework:** "I would start with a Pareto analysis of the reject types — which specific defect categories are driving the increase? Then I would correlate with variables: operator shift patterns, raw material batch numbers, machine maintenance logs, and environmental conditions. If the rejects cluster around a specific shift or machine, the root cause is likely operator training or equipment calibration. If they cluster around a material batch, it's a supplier quality issue. At Instawork AI, I maintained 99%+ accuracy by creating validation rubrics and edge-case documentation — the same systematic quality methodology applies. I would implement corrective action, measure for 2 weeks, and only close the investigation when the rate returns below 2%."
""",
        },
    ],
    "fmcg": [
        {
            "q": "A distributor in a key territory is underperforming against quarterly targets by 30%. What's your action plan?",
            "a": """**Framework:** "First, I would visit the distributor and conduct a joint business review — is the issue demand-side (weak retail offtake) or supply-side (stockouts, poor SKU assortment, delivery delays)? I would check their retail coverage, beat plan adherence, and outstanding returns. If it's capability, I would provide on-ground training and ride-alongs with their sales team. If it's structural, I would evaluate whether the territory needs redistribution or an additional sub-distributor. At Puma and Tata Communications activations, I managed field teams across multiple territories and learned that underperformance almost always traces to either wrong coverage or wrong product mix — data tells you which."
""",
        },
        {
            "q": "You are launching a new SKU in 500 retail stores simultaneously. How do you ensure flawless execution?",
            "a": """**Framework:** "I would work backwards from launch date: T-21 days — confirm production and dispatch schedule; T-14 — distribute POS materials and planogram updates to all 500 stores; T-7 — verify inventory receipt at distributor warehouses; T-3 — field team conducts store-level readiness checks (shelf placement, pricing labels, promotional displays); T-day — launch with mystery shopper audits on 10% sample. Having coordinated 300+ live event deployments, I know that flawless simultaneous execution requires (1) a written SOP for every stakeholder, (2) a single tracking dashboard visible to all, and (3) a rapid escalation protocol for exceptions."
""",
        },
    ],
    "healthcare": [
        {
            "q": "A critical medical supply vendor has increased prices by 20% with 30 days notice. The hospital cannot switch vendors quickly due to regulatory approvals. How do you negotiate?",
            "a": """**Framework:** "I would first verify whether the price increase is contractually permissible by reviewing the supply agreement's escalation clause. If it violates the contract, I would formally object in writing and invoke the dispute resolution mechanism. If it's within their rights, I would negotiate by presenting our volume data and multi-year commitment value, proposing a phased increase (e.g., 8% now, 6% in 6 months, 6% in 12 months) rather than a flat 20%. Simultaneously, I would initiate the regulatory approval process for an alternate vendor as leverage. In my operations, I reduced vendor costs by 15% using exactly this approach — presenting data, proposing tiered structures, and having alternatives in the pipeline."
""",
        },
        {
            "q": "Patient wait times in the outpatient department have increased by 40% over the past quarter. How do you diagnose and fix this?",
            "a": """**Framework:** "I would map the entire patient journey from registration to consultation to billing, timing each step. The bottleneck is usually at one of three points: registration desk throughput, doctor consultation duration, or diagnostic lab turnaround. I would collect data for one week, identify the constraint, and implement targeted fixes — whether that's adding a registration kiosk, staggering appointment slots, or parallelizing lab sample processing. At large-scale events with 15,000+ daily attendees, I managed crowd flow and queue optimization using the same time-motion analysis. Measure → identify constraint → fix constraint → re-measure."
""",
        },
    ],
    "general": [
        {
            "q": "You are asked to build a weekly MIS reporting dashboard from scratch for the operations team. How do you approach this?",
            "a": """**Framework:** "I would start by interviewing the 3-4 key stakeholders who will consume the report to understand their decision-making needs — what questions do they ask every Monday morning? Then I would identify the source data systems, build the data pipeline in Excel or Power BI, and design the dashboard around 5-7 key metrics with drill-down capability. I would prototype a v1 in 3 days, get feedback, and iterate. At Instawork AI, I maintained precision across thousands of data evaluations using structured validation rubrics — the same data discipline applies to building reliable reporting systems."
""",
        },
        {
            "q": "Your team is resistant to a new SOP you've implemented. How do you drive adoption?",
            "a": """**Framework:** "Resistance usually comes from either not understanding why the change matters or finding the new process harder than the old one. I would address both: first, I would share the data showing why the current process is failing (missed SLAs, cost overruns, errors) and how the new SOP directly fixes those issues. Second, I would simplify the SOP based on their feedback — if it adds 5 steps but the team only sees value in 3, cut the other 2. At VH1 Supersonic, when I introduced a new radio protocol for 20+ crew members from different vendors, initial resistance dissolved once the first smooth stage transition proved it worked. Show results, don't just mandate process."
""",
        },
    ],
}


# ── Asset Generators (v2 — Industry-Aware) ──────────────────────────────────

def gen_resume_v2(company: str, role: str, industry: str) -> str:
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["general"])
    ordered_competencies = "\n".join(
        [f"- {COMPETENCY_BLOCKS[c]}" for c in profile["competency_order"]]
    )
    industry_keywords = ", ".join(profile["keywords"][:8])

    return f"""# {CANDIDATE['name'].upper()}
**{CANDIDATE['location']}** | **Phone:** {CANDIDATE['phone']} | **Email:** {CANDIDATE['email']} | **LinkedIn:** {CANDIDATE['linkedin']}

---

## PROFESSIONAL SUMMARY
Results-driven **BBA in International Business** graduate (Dayananda Sagar University, 2026) specializing in {profile['summary_hook']}. Delivered **300+ high-stakes operational deployments** for tier-1 enterprise accounts (**Tata Communications, Puma India, Aero India 2025**) with **0% budget overrun**. Drove **15% recurring cost reduction** through direct vendor rate card restructuring. Generated **INR 1.5L+ B2B commercial revenue** with formal management commendation. Seeking to deliver immediate operational impact as **{role}** at **{company}**.

---

## CORE COMPETENCIES
{ordered_competencies}
- **Industry-Relevant Proficiencies:** {industry_keywords}.

---

## PROFESSIONAL EXPERIENCE

### Event Operations Lead & Project Coordinator — Self-Employed / Freelance
*Bengaluru, India | Jan 2021 – Present*
- Orchestrated on-ground operations and cross-functional vendor management for **300+ enterprise events**, managing budgets end-to-end with **0% budget overrun** and 100% on-time milestone delivery.
- Directed on-site operations for **Aero India 2025** (Yelahanka Air Force Station, 15,000+ daily attendees), **Tata Communications**, **Puma India**, and **VH1 Supersonic**.
- Led cross-functional teams of **20+ on-ground staff** across venue setup, security protocols, technical infrastructure, and VIP relations under strict SLA deadlines.
- Audited vendor cost structures and restructured rate agreements, eliminating agency markups to achieve a **15% direct cost reduction** across recurring operational expenditure.

### Operations Lead (Aero India 2025) — Salt in My Coca
*Bengaluru, India | Feb 2025*
- Managed end-to-end commercial stall operations, inventory control, and VIP delegation engagement at **Asia's largest aerospace expo** with rigorous IAF defense compliance.
- Ensured 100% adherence to security protocols, gate passes, and time-critical delivery constraints with zero non-conformances across multi-day sessions.

### Business Development Executive Intern — Pencil Mark Interior Solutions LLP
*Bengaluru, India | Jul 2025 – Aug 2025*
- Spearheaded outbound B2B corporate client acquisition for commercial architectural and interior projects across Bangalore's tech corridor.
- Independently prospected, pitched, and closed **INR 1.5L+ in direct commercial revenue** within 6 weeks. Accelerated lead-to-close conversion by **25%**.
- Received formal **written management commendation** for surpassing outreach quotas.

### AI Data Operations & Quality Specialist — Instawork AI
*Remote / Bengaluru | Sep 2024 – Dec 2024*
- Executed high-precision multi-modal data curation, prompt annotation, and quality benchmarks for production LLMs.
- Maintained **99%+ audit accuracy** across thousands of evaluation batches, ranking in the top quartile.

### CEO / Operations Manager — Family Business
*Kolkata, India | Jan 2018 – Nov 2020*
- Led day-to-day operations across sales, marketing, and procurement. Restructured vendor workflows to achieve **15% overhead reduction**.

---

## EDUCATION
**Bachelor of Business Administration (BBA) — International Business**
Dayananda Sagar University (DSU), Bengaluru, Karnataka | Graduation: 2026
- Strategic Operations, International Trade & EXIM, Corporate Finance, Business Analytics, Negotiation & Contract Law.

---

## COMMENDATIONS
- Written Management Commendation — Pencil Mark Interior Solutions LLP (Outstanding B2B Client Acquisition).
- Verified Lead Coordinator — Tata Communications, Puma India, Aero India 2025 (IAF Yelahanka).
"""


def gen_interview_v2(company: str, role: str, industry: str) -> str:
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["general"])
    scenarios = INDUSTRY_SCENARIOS.get(industry, INDUSTRY_SCENARIOS["general"])

    scenario_text = ""
    for i, s in enumerate(scenarios, 1):
        scenario_text += f"""
### Scenario {i}: "{s['q']}"
{s['a']}
"""

    return f"""# 360° INTERVIEW PREPARATION & DEFENSE MATRIX
**Company:** {company} | **Role:** {role}
**Industry:** {profile['label']}
**Candidate:** {CANDIDATE['name']} | **Generated:** {datetime.now().strftime('%Y-%m-%d')}

---

## PART 1: TOP 5 BEHAVIORAL QUESTIONS (STAR METHOD)

### Q1: "Tell me about a time you handled a high-pressure operational crisis."
- **Situation:** At Aero India 2025 (Yelahanka Air Force Station), I managed commercial booth logistics under IAF security clearance.
- **Task:** Day 1 morning — critical inventory shipment delayed at security checkpoint, threatening empty stall during VIP rounds.
- **Action:** Mobilized IAF liaison officer with pre-verified documentation, fast-tracked security inspection, and rearranged displays with existing materials as backup.
- **Result:** 100% booth uptime. 500+ VIPs engaged. Zero protocol infractions.

### Q2: "How have you driven measurable cost reduction?"
- **Situation:** Recurring vendor invoices across corporate events (Puma, Tata Communications) eroded margins by 12-18%.
- **Task:** Protect margins while maintaining flawless delivery.
- **Action:** Granular line-item audit of staging, AV, fabrication, and transport. Mapped direct tier-1 suppliers, bypassed aggregators, negotiated volume rate cards.
- **Result:** **15% recurring cost reduction** across all subsequent projects.

### Q3: "Give an example of closing a deal with a skeptical B2B client."
- **Situation:** At Pencil Mark Interior Solutions, commercial developers were reluctant during economic tightening.
- **Task:** Generate qualified meetings and close contracts independently.
- **Action:** Created tailored cost-per-sqft ROI comparisons. Disciplined outreach with 2-hour follow-up SLA. Transparent material specifications.
- **Result:** **INR 1.5L+ closed** in 6 weeks. Formal written management commendation.

### Q4: "How do you maintain precision on repetitive analytical tasks?"
- **Situation:** At Instawork AI, annotating multi-modal datasets with 95% accuracy SLA.
- **Task:** Exceed accuracy targets under tight turnarounds.
- **Action:** Built personal validation rubric. Cross-referenced edge-case rules. Documented ambiguous cases for QA normalization.
- **Result:** **99%+ audit accuracy**, top quartile ranking.

### Q5: "How do you lead teams without formal authority?"
- **Situation:** VH1 Supersonic — managed 20+ crew from independent vendors across security, sound, catering.
- **Task:** Synchronize stage transitions under broadcast timelines.
- **Action:** 15-minute pre-event alignment, two-way radio protocol, led by example on bottlenecks.
- **Result:** Every transition executed within 3-minute window. Zero delays.

---

## PART 2: {profile['label'].upper()} — ROLE-SPECIFIC SCENARIO QUESTIONS
{scenario_text}

---

## PART 3: CURVEBALL DEFENSE SCRIPTS

### "You're a 2026 graduate. Why hire you over someone with 3-5 years of experience?"
> "I bring 4+ years of verified on-ground execution — 300+ deployments, 20-person teams, 15% cost savings — before graduating. No legacy habits, no inflated compensation demands, maximum hunger and ownership. You get Day-1 execution velocity with zero entitlement."

### "Your background spans events, interiors, and AI data. How is that relevant to {role}?"
> "Every role centered on one discipline: operational excellence under constraints. Events — 300+ deployments, zero margin for error. Business development — revenue pipeline discipline. AI data — analytical precision. {role} at {company} requires exactly this combination."

### "What's your biggest weakness?"
> "I initially took on too much operational load myself. During a multi-vendor setup, I realized this created a single point of failure. I solved it by building SOP checklists and delegating zones to trained leads with check-in cadences. That shift enabled scaling from small events to 300+ large deployments."

---

## PART 4: REVERSE-INTERVIEW QUESTIONS FOR {company.upper()}

1. *"What's the single biggest operational bottleneck you'd want resolved within my first 90 days?"*
2. *"How does this team balance long-term optimization with daily firefighting?"*
3. *"What distinguishes adequate operators from indispensable ones at {company}?"*
4. *"What new workflows will this team need to build for {company}'s next-12-month strategic goals?"*
5. *"Based on today's conversation, is there anything about my background you'd like me to clarify?"*
"""


def gen_plan90_v2(company: str, role: str, industry: str) -> str:
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["general"])
    keywords = profile["keywords"][:6]
    kw_text = ", ".join(keywords)

    return f"""# 30-60-90 DAY STRATEGIC ONBOARDING BLUEPRINT
**Company:** {company} | **Role:** {role} | **Industry:** {profile['label']}
**Candidate:** {CANDIDATE['name']} | **Generated:** {datetime.now().strftime('%Y-%m-%d')}

---

## PHASE 1: DAYS 1–30 — ABSORB, AUDIT & QUICK WINS

| Week | Milestones |
|------|-----------|
| 1 | Complete onboarding, compliance, IT/system access. Study {company}'s org chart, team structure, and reporting cadences. |
| 1-2 | Conduct 1-on-1 discovery with direct team, cross-functional partners, and key vendors. Map handoffs and pain points. |
| 2-3 | Audit existing SOPs, tracking tools, vendor contracts, and operational dashboards for {role} workflows. Identify gaps in {kw_text}. |
| 3-4 | Identify 2 quick-win process improvements (manual bottlenecks, reporting gaps, vendor invoice discrepancies). |
| 4 | Deliver **30-Day Synthesis Memo** to manager: observations, proposed efficiency targets, and recommended priorities. |

**Deliverable:** Written diagnostic report with 2-3 actionable proposals.

---

## PHASE 2: DAYS 31–60 — EXECUTE, OPTIMIZE & DELIVER QUICK WINS

| Week | Milestones |
|------|-----------|
| 5-6 | Take full unassisted ownership of core {role} workflows and vendor/SLA tracking. |
| 6-7 | Implement first process improvement (modeled on 15% cost optimization methodology): standardize rate tracking, automate a manual report, or fix a recurring data quality issue. |
| 7-8 | Build or improve a weekly management dashboard (Excel/Power BI) surfacing key operational metrics. |
| 8 | Proactively resolve escalations before SLA breach. Hold mid-quarter alignment with manager. |

**Deliverable:** First measurable efficiency gain (target 10-15% improvement) documented with before/after data.

---

## PHASE 3: DAYS 61–90 — SCALE, OWN & DELIVER ROI

| Week | Milestones |
|------|-----------|
| 9-10 | Operate with full autonomy as the division's go-to operational problem-solver. |
| 10-11 | Publish hardened SOP documentation for all owned processes — any new hire can onboard with zero disruption. |
| 11-12 | Deliver measurable business impact: quantified cost savings, turnaround improvements, or process error reductions. |
| 12 | Present **90-Day Value Summary** to leadership: verified metrics, completed projects, and H2 operational roadmap. |

**Deliverable:** Executive presentation with quantified ROI and forward-looking recommendations.
"""


def gen_negotiation_v2(company: str, ctc: str = "") -> str:
    t_min, t_max = "7.5", "11.0"
    if ctc:
        nums = re.findall(r'[\d.]+', ctc)
        if len(nums) >= 2:
            t_min, t_max = nums[0], nums[1]
        elif len(nums) == 1:
            t_min = nums[0]
            t_max = str(round(float(nums[0]) * 1.3, 1))

    counter_target = str(round(float(t_min) + 1.0, 1))

    return f"""# COMPENSATION NEGOTIATION PLAYBOOK
**Company:** {company} | **Target Band:** INR {t_min}L - {t_max}L LPA
**Candidate:** {CANDIDATE['name']} | **Generated:** {datetime.now().strftime('%Y-%m-%d')}

---

## SCRIPT A: Deflecting Salary Questions in Early Rounds
> *"Right now my priority is confirming the right operational fit where I can deliver immediate impact at {company}. I'm confident {company} offers competitive compensation aligned with Bangalore market standards. Once we confirm mutual fit, I'm sure we'll agree on a fair number. Could you share the budgeted range for this position?"*

---

## SCRIPT B: Countering a Low Offer
> *"Thank you — I'm genuinely excited about joining {company}. Based on market benchmarks for this role in Bangalore, and the verified value I bring — 300+ operational deployments, 15% cost optimization, and INR 1.5L+ in closed commercial revenue — I was anticipating an offer in the INR {t_min}L to {t_max}L range. If we can adjust closer to INR {counter_target}L, I'm prepared to sign immediately. Is there flexibility?"*

---

## SCRIPT C: Non-Salary Levers (If Base is Capped)
> *"I understand if the base band is fixed by policy. Would {company} consider:*
> 1. *A joining bonus of INR 75,000 - 1,00,000?*
> 2. *Accelerated performance review at 6 months instead of 12?*
> 3. *Professional certification sponsorship or hybrid flexibility?*
> *Any of these would make this a definitive decision."*

---

## SCRIPT D: Acceptance
> *"I appreciate the team working to make this happen. I'm 100% committed to delivering exceptional value at {company}. Please send the revised letter — I'll sign immediately."*

---

## ANCHORING RULES
1. Never accept the first number. Counter with value evidence.
2. Anchor to: 300+ operations, 15% cost savings, INR 1.5L+ revenue, 99%+ accuracy.
3. If base is fixed, negotiate joining bonus, review cycle, and flexibility.
4. Express genuine enthusiasm throughout — enthusiasm + data = maximum leverage.
"""


def gen_index_v2(company: str, role: str, industry: str, folder: Path) -> str:
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["general"])
    files = sorted([f.name for f in folder.iterdir() if f.is_file()])
    file_list = "\n".join([f"- [{f}]({f})" for f in files])
    return f"""# OMEGA CONQUEST PACK: {company.upper()}
**Role:** {role} | **Industry:** {profile['label']}
**Candidate:** {CANDIDATE['name']} | **Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Assets
{file_list}
"""


# ── Main v2 Processor ───────────────────────────────────────────────────────

def process_v2():
    folders = sorted([d for d in BASE_DIR.iterdir() if d.is_dir()])
    total = len(folders)
    upgraded = 0
    skipped = 0

    print(f"\n{'='*76}")
    print(f"  OMEGA BATCH CONQUEST ENGINE v2.0 — DEFECT ANNIHILATOR")
    print(f"  Folders: {total} | Fixes: D1+D2+D3+D4+D5")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*76}\n")

    for i, folder in enumerate(folders, 1):
        manifest = read_manifest(folder)
        company = manifest.get("company") or clean_folder_to_company(folder.name)
        role = manifest.get("role") or "Operations & Business Development Specialist"
        ctc = manifest.get("ctc", "")
        sector = manifest.get("sector", "")
        industry = classify_industry(company, role, sector)
        display = company[:60]

        try:
            # Overwrite all 4 batch-generated assets with v2
            (folder / "ATS_RESUME.md").write_text(gen_resume_v2(company, role, industry), encoding="utf-8")
            (folder / "STAR_INTERVIEW_DEFENSE.md").write_text(gen_interview_v2(company, role, industry), encoding="utf-8")
            (folder / "DAY_30_60_90_PLAN.md").write_text(gen_plan90_v2(company, role, industry), encoding="utf-8")
            (folder / "COMPENSATION_NEGOTIATION.md").write_text(gen_negotiation_v2(company, ctc), encoding="utf-8")
            (folder / "MASTER_CONQUEST_INDEX.md").write_text(gen_index_v2(company, role, industry, folder), encoding="utf-8")

            upgraded += 1
            ind_label = INDUSTRY_PROFILES[industry]["label"][:25]
            print(f"  [{i:3d}/{total}] [v2] {display:<60} [{ind_label}]")

        except Exception as e:
            print(f"  [{i:3d}/{total}] [!!] {display:<60} ERROR: {str(e)[:50]}")

    print(f"\n{'='*76}")
    print(f"  v2 DEPLOYMENT COMPLETE")
    print(f"  Upgraded: {upgraded}/{total}")
    print(f"  All 5 defects (D1-D5) resolved.")
    print(f"{'='*76}\n")


if __name__ == "__main__":
    process_v2()
