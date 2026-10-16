"""
=============================================================================
GENERATE ALL REMAINING TAILORED COVER LETTERS AND EMAIL DRAFTS
Generates verified, tailored application assets for all remaining corporate
targets in the career vault:
Genpact, Diageo, Lowe's India, Target, Capgemini, PhonePe, CRED, Swiggy,
Zepto, Groww, JPMorgan Chase, Morgan Stanley, KPMG, PwC, EY, Deloitte,
Myntra, TeamLease, etc.
=============================================================================
"""

import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CL_DIR = os.path.join(ROOT_DIR, "cover_letters")
EML_DIR = os.path.join(ROOT_DIR, "Email_Drafts")

os.makedirs(CL_DIR, exist_ok=True)
os.makedirs(EML_DIR, exist_ok=True)

TARGETS = [
    {
        "company": "Genpact India",
        "key": "Genpact",
        "prefix": "26_Genpact",
        "role": "Process Associate - Supply Chain & Operations Analytics",
        "address": "Genpact India Private Limited\nPrestige Shantiniketan, Whitefield / Salarpuria Softzone, Bellandur, Bengaluru",
        "hook": "Having orchestrated operational workflows and vendor rate-card restructuring across 300+ high-stakes live events and managed high-precision dataset QA at Instawork AI, I understand how lean process discipline drives measurable margin preservation.",
        "p2p": "order-to-cash (O2C) reconciliation, inventory exceptions management, supplier SLA compliance auditing, and process KPI governance."
    },
    {
        "company": "Diageo Global Business Operations",
        "key": "Diageo",
        "prefix": "27_Diageo",
        "role": "Supply Chain Logistics & Commercial Operations Analyst",
        "address": "Diageo Business Services India (DBSI)\nKarle Town Centre SEZ, Nagavara, Bengaluru",
        "hook": "With direct operational leadership across multi-vendor logistics deployments and rigorous academic grounding in International Business at Dayananda Sagar University (8.2 GPA), I specialize in eliminating transit friction, vendor penalty recovery, and cross-border customs compliance.",
        "p2p": "commercial logistics tracking, bonded warehouse reconciliation, multi-vendor rate audit, and export/import compliance documentation."
    },
    {
        "company": "Lowe's India",
        "key": "Lowes",
        "prefix": "28_Lowes_India",
        "role": "Operations & Supply Chain Inventory Analyst",
        "address": "Lowe's India Global Tech & Operations Center\nManyata Embassy Business Park, Nagavara, Bengaluru",
        "hook": "During my tenure leading high-throughput dataset quality operations at Instawork AI (99%+ compliance across 50,000+ annotations) and managing live inventory staging across 300+ events, I developed deep discipline in resolving supply chain discrepancies before they breach customer SLAs.",
        "p2p": "retail inventory replenishment modeling, vendor fill-rate audits, stockout risk mitigation, and distribution center throughput analytics."
    },
    {
        "company": "Target Corporation India",
        "key": "Target",
        "prefix": "29_Target_India",
        "role": "Business Operations & Inventory Planning Specialist",
        "address": "Target in India, Target Corporation\nManyata Tech Park, Hebbal Outer Ring Road, Bengaluru",
        "hook": "I have executed high-velocity staging and inventory reconciliation across complex multi-stakeholder deployments, as well as serving as VIP Defense Logistics Delegation Coordinator at AERO India 2025. I am drawn to Target's world-class supply chain intelligence.",
        "p2p": "SKU-level inventory health monitoring, lead-time variance analysis, vendor dispute resolution, and cross-dock logistics optimization."
    },
    {
        "company": "Capgemini",
        "key": "Capgemini",
        "prefix": "30_Capgemini",
        "role": "Procurement Operations & SCM Associate",
        "address": "Capgemini Technology Services India Limited\nWhitefield / EPIP Zone / Electronic City, Bengaluru",
        "hook": "Through rigorous hands-on procurement restructuring across 300+ event deployments, I secured an audited 15% cost reduction by eliminating intermediary brokerage layers and enforcing strict vendor milestone acceptance criteria.",
        "p2p": "procure-to-pay (P2P) process execution, purchase order lifecycle management, vendor dispute settlement, and supplier governance."
    },
    {
        "company": "PhonePe (Walmart Group)",
        "key": "PhonePe",
        "prefix": "31_PhonePe",
        "role": "Operations & Merchant Risk Operations Analyst",
        "address": "PhonePe Private Limited (Walmart Group)\nGreen Glen Layout, Bellandur, Outer Ring Road, Bengaluru",
        "hook": "At Instawork AI, I maintained a verified 99%+ compliance score across 50,000+ bounding labels under strict accuracy SLAs. My background in International Business (8.2 GPA) equips me to analyze transaction anomalies, enforce compliance, and streamline digital operational workflows.",
        "p2p": "merchant onboarding lifecycle governance, KYC risk validation, operational SLA tracking, and partner escalation triage."
    },
    {
        "company": "CRED (Dreamplug Technologies)",
        "key": "CRED",
        "prefix": "32_CRED",
        "role": "Business Operations & Member Trust Analyst",
        "address": "Dreamplug Technologies Private Limited (CRED)\n100 Feet Road, Indiranagar, Bengaluru",
        "hook": "Managing high-visibility VIP delegations at AERO India 2025 and coordinating complex physical logistics taught me that flawless execution demands relentless attention to detail and zero tolerance for operational defects.",
        "p2p": "partner settlement reconciliation, high-value transaction workflow audit, exception routing, and operational dispute management."
    },
    {
        "company": "Swiggy (Bundl Technologies)",
        "key": "Swiggy",
        "prefix": "33_Swiggy",
        "role": "Supply Chain & Hub Operations Analyst",
        "address": "Swiggy (Bundl Technologies Private Limited)\nTower D, IBC Knowledge Park, Bannerghatta Road, Bengaluru",
        "hook": "In fast-paced, high-density event operations across 300+ deployments, I specialized in real-time dispatch routing, buffer stock staging, and eliminating turnaround bottlenecks under strict clock constraints.",
        "p2p": "dark store inventory replenishment, hub turn-around time (TAT) optimization, driver partner staging, and order fulfillment SLA audits."
    },
    {
        "company": "Zepto (Kiranakart)",
        "key": "Zepto",
        "prefix": "34_Zepto",
        "role": "Dark Store Logistics & Inventory Operations Executive",
        "address": "Kiranakart Technologies Private Limited (Zepto)\nOuter Ring Road / HSR Layout, Bengaluru",
        "hook": "With direct experience managing rapid physical asset allocation and precision inventory control for 300+ events and high-precision AI data QA at Instawork, I excel at micro-fulfillment and inventory velocity management.",
        "p2p": "hyperlocal dark store picking accuracy, SKU expiry/damage auditing, inwarding gate check standardization, and delivery partner staging."
    },
    {
        "company": "Groww (Nextbillion Technology)",
        "key": "Groww",
        "prefix": "35_Groww",
        "role": "Brokerage Operations & Trade Settlement Analyst",
        "address": "Nextbillion Technology Private Limited (Groww)\nVaishnavi Tech Park, Outer Ring Road, Bellandur, Bengaluru",
        "hook": "My rigorous education in International Business (8.2 GPA) combined with hands-on reconciliation of thousands of vendor and data transactions gives me the analytical rigor required for depository participant and exchange clearing operations.",
        "p2p": "daily trade settlement reconciliation, client depository transfer audit, KYC regulatory reporting, and clearing exception resolution."
    },
    {
        "company": "JPMorgan Chase & Co. (GCC)",
        "key": "JPMorgan",
        "prefix": "36_JPMorgan_GCC",
        "role": "Corporate Operations & Regulatory Reporting Analyst",
        "address": "JPMorgan Chase Bank, N.A. (Global Capabilities Center)\nPrestige Tech Park, Outer Ring Road, Kadubeesanahalli, Bengaluru",
        "hook": "I coordinated VIP defense delegations at AERO India 2025 under strict military security protocols and audited compliance frameworks. I bring this unwavering standard of precision to corporate banking and regulatory operations.",
        "p2p": "cash management reconciliation, trade finance letter-of-credit verification, KYC audit trails, and international payment exception triage."
    },
    {
        "company": "Morgan Stanley Advantage Services",
        "key": "MorganStanley",
        "prefix": "37_Morgan_Stanley",
        "role": "Global Operations & Settlement Analyst",
        "address": "Morgan Stanley Advantage Services\nPrestige Nebula, Outer Ring Road, Bengaluru",
        "hook": "Holding an 8.2 GPA in BBA International Business and demonstrated operational leadership in high-pressure environments, I am committed to institutional operational integrity and zero-error trade processing.",
        "p2p": "collateral management reconciliation, multi-currency trade confirmation, client margin reporting, and depository interface governance."
    },
    {
        "company": "KPMG Global Services (KGS)",
        "key": "KPMG",
        "prefix": "38_KPMG_KGS",
        "role": "Global Risk & Operations Advisory Associate",
        "address": "KPMG Global Services Private Limited\nEmbassy GolfLinks Business Park (EGL), Off Intermediate Ring Road, Bengaluru",
        "hook": "Having spearheaded vendor audit processes that yielded an audited 15% procurement cost reduction and verified 50,000+ data rows with 99%+ compliance at Instawork AI, I bring structured testing and objective documentation to every engagement.",
        "p2p": "internal controls testing, vendor contract risk assessment, regulatory compliance sampling, and business process documentation."
    },
    {
        "company": "PwC Acceleration Centers (AC)",
        "key": "PwC",
        "prefix": "39_PwC_AC",
        "role": "Business Operations & Procurement Transformation Associate",
        "address": "PwC Acceleration Centers (PwC SDC)\nRMZ Ecoworld, Outer Ring Road, Bellandur, Bengaluru",
        "hook": "Combining formal BBA International Business coursework in Supply Chain Management with practical execution across 300+ enterprise events, I specialize in identifying structural inefficiencies and standardizing operational handoffs.",
        "p2p": "global procurement benchmarking, supplier scorecard evaluation, spend analytics categorization, and operational process re-engineering."
    },
    {
        "company": "EY Global Delivery Services (EY GDS)",
        "key": "EY_GDS",
        "prefix": "40_EY_GDS",
        "role": "Global Supply Chain & Operations Associate",
        "address": "EY Global Delivery Services India LLP\nRMZ Infinity, Old Madras Road / Divyasree Technopolis, Bengaluru",
        "hook": "My operational background includes managing logistics for international aerospace delegations at AERO India 2025 and driving vendor contract renegotiations with zero tolerance for contractual SLA drift.",
        "p2p": "supply chain risk matrix mapping, purchase order variance reconciliation, global vendor master data validation, and milestone tracking."
    },
    {
        "company": "Deloitte USI (Deloitte Support Services India)",
        "key": "Deloitte_USI",
        "prefix": "41_Deloitte_USI",
        "role": "Global Business Operations & SCM Analyst",
        "address": "Deloitte Support Services India Private Limited\nPritech Park SEZ, Bellandur, Outer Ring Road, Bengaluru",
        "hook": "With a strong 8.2 GPA in BBA International Business from DSU and proven operational execution across 300+ events, I possess the analytical and organizational discipline required for cross-border US-India operations delivery.",
        "p2p": "operational service-level agreement tracking, cross-functional project milestone audit, spend variance analysis, and workflow reporting."
    },
    {
        "company": "Myntra / Flipkart Group",
        "key": "Myntra",
        "prefix": "42_Myntra",
        "role": "Supply Chain & Omnichannel Logistics Analyst",
        "address": "Myntra Designs Private Limited (Flipkart Group)\nAKR Tech Park, Kudlu Gate, Hosur Road, Bengaluru",
        "hook": "Having led high-throughput operational staging across 300+ live events and audited 50,000+ dataset items at Instawork AI, I understand how critical inventory accuracy and warehouse throughput are to fashion e-commerce.",
        "p2p": "warehouse inwarding throughput tracking, vendor drop-ship SLA compliance, return-to-origin (RTO) root cause analysis, and hub dispatching."
    },
    {
        "company": "TeamLease Services",
        "key": "TeamLease",
        "prefix": "43_TeamLease",
        "role": "Corporate Operations & Workforce Logistics Associate",
        "address": "TeamLease Services Limited\nBMTC Complex, 6th Block, Koramangala, Bengaluru",
        "hook": "Over 300+ corporate events, I personally directed on-site staffing, role allocation, and incident resolution for thousands of attendees. I bring proven execution capability to large-scale workforce logistics and compliance.",
        "p2p": "client SLA adherence tracking, deployment roster reconciliation, vendor billing audits, and field operations governance."
    },
    {
        "company": "Quess Corp Limited",
        "key": "Quess",
        "prefix": "44_Quess_Corp",
        "role": "Operations & Service Delivery Associate",
        "address": "Quess Corp Limited\nQuess House, Sarjapur Main Road, Bellandur, Bengaluru",
        "hook": "Having managed field operations across 300+ events and coordinated VIP defense delegations at AERO India 2025, I possess proven competence in large-scale workforce deployment and client service-level agreements.",
        "p2p": "client operations coordination, workforce deployment tracking, billing reconciliation, and service-level governance."
    },
    {
        "company": "Randstad India",
        "key": "Randstad",
        "prefix": "45_Randstad_India",
        "role": "Enterprise Client Operations Associate",
        "address": "Randstad India Private Limited\nPrestige Tech Park, Outer Ring Road, Bengaluru",
        "hook": "With formal BBA training in International Business (8.2 GPA) and field operations across hundreds of live deployments, I specialize in eliminating SLA exceptions, standardizing client reporting, and managing vendor accounts.",
        "p2p": "enterprise client operations, vendor billing governance, operational reporting, and SLA compliance monitoring."
    }
]

def generate_assets():
    print(f"[*] Generating tailored cover letters and email drafts for {len(TARGETS)} corporate targets...")
    created_cl = 0
    created_eml = 0

    for t in TARGETS:
        cl_path = os.path.join(CL_DIR, f"{t['prefix']}_{t['role'].replace(' ', '_').replace('/', '_')}.txt")
        eml_path = os.path.join(EML_DIR, f"{t['prefix']}_{t['role'].replace(' ', '_').replace('/', '_')}.eml")

        # 1. Cover Letter
        cl_body = f"""ADITYA MEHRA
Bengaluru, Karnataka, India | Phone: +91-7003456624 | Email: adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/adityamehra
---------------------------------------------------------------------------
Date: October 16, 2026

To,
The Talent Acquisition & Operations Hiring Team,
{t['company']}
{t['address']}

Subject: Application for {t['role']}

Dear Hiring Team,

I am writing to express my strong enthusiasm for the {t['role']} position at {t['company']}. As a final-year BBA International Business scholar at Dayananda Sagar University (DSU, Class of 2026) with a cumulative 8.2 GPA, I combine rigorous analytical training in international trade and logistics with proven, field-tested execution across 300+ high-stakes operational deployments.

{t['hook']}

Key Operational Strengths I Bring to {t['company']}:
1. End-to-End Operational Discipline: Managed ground operations, resource allocation, and multi-agency coordination across 300+ events and VIP defense delegations at AERO India 2025 with zero milestone delays.
2. High-Accuracy Process & Data Governance: At Instawork AI, audited 50,000+ bounding labels maintaining a verified 99%+ quality accuracy score under aggressive turn-around times.
3. Procurement & Commercial Rigor: Spearheaded vendor renegotiations and rate-card restructuring resulting in an audited 15% procurement cost reduction and client commendation at Pencil Mark.
4. Core Focus on {t['p2p']}

I am dedicated to corporate, non-sales operational excellence, inventory governance, and supply chain integrity. I am based locally in Bengaluru and immediately available for interviews and prompt onboarding.

Thank you for your time and consideration.

Sincerely,

ADITYA MEHRA
BBA International Business | Dayananda Sagar University
Phone: +91-7003456624 | Email: adityamehra799@gmail.com
"""

        # 2. Email Draft (.eml)
        eml_body = f"""From: Aditya Mehra <adityamehra799@gmail.com>
To: {t['key'].lower()}.careers@talentacquisition.com
Subject: Application: {t['role']} - Aditya Mehra (BBA DSU 2026, 8.2 GPA, Operations & SCM)
X-Unsent: 1
Content-Type: text/plain; charset="utf-8"

Dear {t['company']} Talent Acquisition Team,

I hope this email finds you well.

I am writing to apply for the {t['role']} opportunity with {t['company']} in Bengaluru.

As a final-year BBA International Business student at Dayananda Sagar University (Class of 2026, 8.2 GPA), I have built a strong track record of operational and procurement execution in high-stakes environments:

- Operations Leadership: Directed ground logistics and resource management across 300+ high-visibility events, including serving as VIP Defense Logistics Delegation Coordinator at AERO India 2025.
- Data Quality & SLA Precision: Maintained 99%+ quality compliance across 50,000+ data annotations under strict production SLAs at Instawork AI.
- Procurement & Vendor Savings: Restructured vendor rate cards to eliminate intermediary markups, delivering an audited 15% procurement savings and receiving a written commendation from Pencil Mark.
- Technical Skills: Advanced Excel (VLOOKUP, Pivot Tables, Power Query), SQL relational querying, SAP/Oracle ERP workflows, and SLA penalty modeling.

My resume and detailed portfolio are attached for your review. I am based in Bengaluru and available immediately for discussions.

Thank you for your consideration.

Warm regards,

Aditya Mehra
Phone: +91-7003456624
Email: adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/adityamehra
"""

        with open(cl_path, "w", encoding="utf-8") as f:
            f.write(cl_body)
        created_cl += 1

        with open(eml_path, "w", encoding="utf-8") as f:
            f.write(eml_body)
        created_eml += 1

    print(f"[OK] Generated {created_cl} cover letters and {created_eml} .eml drafts.")

if __name__ == "__main__":
    generate_assets()
