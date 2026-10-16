"""
Generate tailored Cover Letters and EML drafts for newly verified target companies:
Boeing India, Schneider Electric, Tesco Bengaluru, Shell India, and Flipkart.
"""
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CL_DIR = os.path.join(ROOT_DIR, "cover_letters")
EML_DIR = os.path.join(ROOT_DIR, "Email_Drafts")

os.makedirs(CL_DIR, exist_ok=True)
os.makedirs(EML_DIR, exist_ok=True)

ASSETS = [
    {
        "company": "Boeing India",
        "cl_filename": "21_Boeing_India_Procurement_Agent.txt",
        "eml_filename": "21_Boeing_India_Procurement_Agent.eml",
        "role": "Associate Procurement Agent (Direct Materials / Global Services)",
        "address": "Boeing India Engineering & Technology Center (BIETC)\nAerospace Park, Devanahalli, Bengaluru",
        "hook": "Having served as VIP Defense Logistics Delegation Coordinator at AERO India 2025 at Yelahanka Air Force Station, I coordinated airside movement, multi-agency protocols, and tight milestone SLAs for international aerospace delegations. I am eager to apply this rigorous execution mindset to Boeing Global Services procurement in Bengaluru.",
        "p2p": "direct materials RFQ closures, vendor compliance auditing, and contract negotiation with zero-defect execution."
    },
    {
        "company": "Schneider Electric",
        "cl_filename": "22_Schneider_Electric_Procurement_Specialist.txt",
        "eml_filename": "22_Schneider_Electric_Procurement_Specialist.eml",
        "role": "Procurement & Sourcing Specialist",
        "address": "Schneider Electric India Global Hub\nBengaluru, Karnataka",
        "hook": "Throughout my operations work across 300+ events and corporate deployments, I restructured vendor rate cards to eliminate middleman markups—delivering an audited 15% procurement cost reduction and structuring advance payment milestones for maximum leverage. I am deeply impressed by Schneider Electric's global supply chain resilience.",
        "p2p": "prototype and spot-buy purchasing, should-cost model benchmarking, and supplier performance governance in SAP/Oracle environments."
    },
    {
        "company": "Tesco Bengaluru",
        "cl_filename": "23_Tesco_Bengaluru_Supply_Chain_Analyst.txt",
        "eml_filename": "23_Tesco_Bengaluru_Supply_Chain_Analyst.eml",
        "role": "Supply Chain Analyst - Retail Replenishment & Planning",
        "address": "Tesco Business Solutions\nWhitefield, Bengaluru",
        "hook": "Managing high-volume operations requiring precision stock staging, real-time inventory reconciliation, and tight SLA tracking has defined my operational experience. At Instawork AI, I maintained 99%+ quality compliance across 50,000+ bounding labels under strict SLA deadlines.",
        "p2p": "demand forecasting, inventory buffer modeling, supplier fill-rate audits, and retail logistics analytics."
    },
    {
        "company": "Shell India",
        "cl_filename": "24_Shell_India_Supply_Chain_Excellence.txt",
        "eml_filename": "24_Shell_India_Supply_Chain_Excellence.eml",
        "role": "Supply Chain Operational Excellence Specialist",
        "address": "Shell Technology Centre Bengaluru (STCB)\nDevanahalli & RMZ Ecoworld, Bengaluru",
        "hook": "With direct operational leadership across multi-day deployments and formal training in International Business at Dayananda Sagar University (8.2 GPA), I specialize in eliminating operational variance, standardizing multi-vendor workflows, and enforcing contract SLA penalties.",
        "p2p": "supply chain process standardization, vendor performance auditing, transit bottleneck elimination, and operational excellence."
    },
    {
        "company": "Flipkart",
        "cl_filename": "25_Flipkart_Ekart_Operations_Analyst.txt",
        "eml_filename": "25_Flipkart_Ekart_Operations_Analyst.eml",
        "role": "Operations Analyst - Ekart Supply Chain Network",
        "address": "Flipkart Internet Private Limited\nCessna Business Park, Outer Ring Road, Bengaluru",
        "hook": "Having coordinated high-velocity logistics across 300+ event deployments and high-throughput dataset quality operations at Instawork AI, I understand how crucial millisecond and transit tracking are to customer satisfaction and operational throughput in Bengaluru.",
        "p2p": "fulfillment center KPI tracking, line-haul transit exception handling, warehouse SLA enforcement, and root-cause bottleneck resolution."
    }
]

for a in ASSETS:
    # 1. Write Cover Letter
    cl_content = f"""ADITYA MEHRA
Bengaluru, Karnataka, India | Phone: +91-7003456624 | Email: adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/adityamehra
---------------------------------------------------------------------------
Date: October 16, 2026

To,
University Talent Acquisition & Operations Recruiting Team
{a['company']}
{a['address']}

Subject: Application for {a['role']} - Aditya Mehra

Dear {a['company']} Recruiting Team,

I am writing to express my enthusiastic application for the {a['role']} position at {a['company']}. Currently completing my final year of Bachelor of Business Administration (BBA) in International Business at Dayananda Sagar University (DSU), Bengaluru (Class of 2026, Cumulative GPA: 8.2 / 10), I combine international commercial training with on-ground operational rigor.

{a['hook']}

Throughout my academic and field experience, I have developed verified capabilities directly aligned with {a['company']}'s operational standards:
• Vendor Cost Optimization & SLA Audits: Achieved audited 15% cost reductions by eliminating broker markups, enforcing contract penalty formulas for milestone delays, and negotiating favorable advance mobilization terms.
• High-Pressure Coordination: Managed airside and on-ground logistics for international defense delegations at AERO India 2025 and 300+ large-scale corporate event stagings.
• Rigorous Quality & Data Compliance: Maintained 99%+ accuracy across 50,000+ spatial data instances at Instawork AI and earned a written B2B commendation from Pencil Mark for operational execution.
• Systems & Analytical Skills: Proficient in {a['p2p']}

I bring a relentless bias for action, zero tolerance for unverified assumptions, and a roll-up-your-sleeves work ethic. I would welcome the opportunity to discuss how my background and dedication can add tangible value to {a['company']} in Bengaluru.

Thank you for your time, consideration, and leadership.

Sincerely,

Aditya Mehra
BBA International Business | Class of 2026
Dayananda Sagar University, Bengaluru
Phone: +91-7003456624 | Email: adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/adityamehra
"""
    cl_path = os.path.join(CL_DIR, a['cl_filename'])
    with open(cl_path, "w", encoding="utf-8") as f:
        f.write(cl_content)

    # 2. Write EML draft
    eml_content = f"""From: Aditya Mehra <adityamehra799@gmail.com>
To: {a['company']} Operations Recruiting <talent-acquisition@{a['company'].lower().replace(' ', '')}.com>
Subject: Application: {a['role']} - Aditya Mehra (BBA DSU 2026, 8.2 GPA | AERO India 2025 Ops)
Date: Thu, 16 Oct 2026 07:35:00 +0530
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

Dear {a['company']} Talent Acquisition Team,

I am writing to formally apply for the {a['role']} position with {a['company']} in Bengaluru.

Brief Profile Summary:
- Education: Final Year BBA in International Business, Dayananda Sagar University (DSU, Class of 2026), GPA: 8.2 / 10.
- Operations Experience: Coordinated airside logistics at AERO India 2025 (VIP defense delegation movement) and 300+ high-stakes live events.
- Cost Optimization: Delivered 15% procurement savings by benchmarking vendor rate cards and structuring milestone SLAs.
- Data & Process Rigor: Instawork AI Robotics Dataset QA (99%+ compliance across 50k+ annotations); Pencil Mark Written B2B Client Commendation.

I have attached my tailored ATS resume and cover letter for your review. I am based in Bengaluru and available immediately for an interview.

Thank you for your time and consideration.

Warm regards,

Aditya Mehra
Bengaluru, Karnataka | +91-7003456624
LinkedIn: https://www.linkedin.com/in/adityamehra
"""
    eml_path = os.path.join(EML_DIR, a['eml_filename'])
    with open(eml_path, "w", encoding="utf-8") as f:
        f.write(eml_content)

print(f"[OK] Successfully generated {len(ASSETS)} cover letters and EML drafts.")
