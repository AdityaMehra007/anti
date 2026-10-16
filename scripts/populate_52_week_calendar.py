"""
populate_52_week_calendar.py
============================
Creates and populates the `hiring_calendar_52_weeks` table in `data/aditya_global_career_intelligence.db`.
Maps all 52 weeks of the year to specific Bengaluru GCCs, MNCs, FMCGs, Consulting, Logistics, and Tech Unicorn hiring waves.
Tailored for Aditya Mehra | BBA International Business (DSU '26) | Bengaluru.
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = Path("data/aditya_global_career_intelligence.db")

CALENDAR_DATA = [
    # Q1: WEEKS 1 - 13 (January - March)
    {
        "week_number": 1,
        "month": "January",
        "quarter": "Q1",
        "hiring_season": "Q1 Corporate Budget Release & Global Off-Campus Kickoff",
        "week_title": "Boeing & Aerospace GCC Early Intake",
        "target_companies": [
            {"company": "Boeing India", "location": "BIETC, Whitefield", "role": "Supply Chain & Logistics Operations Intern/Associate", "portal": "https://jobs.boeing.com/location/bengaluru-jobs/185/1277333/4", "ats": "Workday"},
            {"company": "Collins Aerospace", "location": "Whitefield", "role": "Global Trade Compliance & Logistics Trainee", "portal": "https://careers.rtx.com/global/en", "ats": "Workday"}
        ],
        "role_categories": ["Aerospace Logistics", "EXIM Trade Compliance", "Operations"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Leverage Aero India 2025 Coordinator credential (EXP-001) for direct high-affinity match with BIETC hiring managers.",
        "verified_seam": "EXP-001"
    },
    {
        "week_number": 2,
        "month": "January",
        "quarter": "Q1",
        "hiring_season": "Q1 Corporate Budget Release & Global Off-Campus Kickoff",
        "week_title": "Shell & Energy Global Business Services Wave",
        "target_companies": [
            {"company": "Shell India", "location": "SICC, Bellandur ORR", "role": "Commercial Operations & Contracting Analyst", "portal": "https://www.shell.in/careers.html", "ats": "Workday"},
            {"company": "ExxonMobil Global Services", "location": "Bellandur", "role": "Supply Chain Optimization Specialist", "portal": "https://jobs.exxonmobil.com", "ats": "Workday"}
        ],
        "role_categories": ["Energy Operations", "Contracting & Procurement", "Analytics"],
        "cycle_stage": "Shortlisting & Screening",
        "action_playbook": "Highlight cross-border vendor negotiation and international trade compliance.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 3,
        "month": "January",
        "quarter": "Q1",
        "hiring_season": "Q1 Corporate Budget Release & Global Off-Campus Kickoff",
        "week_title": "Deloitte USI & Big 4 Risk Advisory Operations",
        "target_companies": [
            {"company": "Deloitte USI", "location": "Yelahanka & Whitefield", "role": "Supply Chain Risk & Operations Analyst", "portal": "https://jobsindia.deloitte.com", "ats": "Taleo"},
            {"company": "PwC Acceleration Center", "location": "Manyata Tech Park", "role": "Management Consulting Operations Associate", "portal": "https://www.pwc.in/careers.html", "ats": "Workday"}
        ],
        "role_categories": ["Risk Advisory", "Supply Chain Risk", "Operations"],
        "cycle_stage": "Assessment Tests",
        "action_playbook": "Stage tailored ATS package emphasizing quantitative operations and APAC market feasibility.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 4,
        "month": "January",
        "quarter": "Q1",
        "hiring_season": "Q1 Corporate Budget Release & Global Off-Campus Kickoff",
        "week_title": "Goldman Sachs & Bulge Bracket Global Ops",
        "target_companies": [
            {"company": "Goldman Sachs", "location": "Helios Business Park, ORR", "role": "Global Operations Analyst (Trade & Clearing)", "portal": "https://www.goldmansachs.com/careers/index.html", "ats": "Internal HCM"},
            {"company": "Morgan Stanley", "location": "Outer Ring Road", "role": "Institutional Operations Analyst", "portal": "https://www.morganstanley.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Trade Settlement", "Global Clearing", "Financial Ops"],
        "cycle_stage": "Superday Interviews",
        "action_playbook": "Rehearse high-precision trade reconciliation and zero-error operational workflows.",
        "verified_seam": "EXP-002"
    },
    {
        "week_number": 5,
        "month": "February",
        "quarter": "Q1",
        "hiring_season": "Retail GCC & Omnichannel Supply Chain Surge",
        "week_title": "Target India Omnichannel Supply Chain Drive",
        "target_companies": [
            {"company": "Target India", "location": "Manyata Tech Park", "role": "Supply Chain Operations & Inventory Analyst", "portal": "https://india.target.com/careers", "ats": "Workday"},
            {"company": "Lowe's India", "location": "Manyata Tech Park", "role": "Merchandising & Logistics Operations Specialist", "portal": "https://www.lowes.co.in/careers", "ats": "Workday"}
        ],
        "role_categories": ["Omnichannel Logistics", "Inventory Management", "Analytics"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Emphasize inventory turnover modeling, supplier lead-time compression, and EDI documentation.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 6,
        "month": "February",
        "quarter": "Q1",
        "hiring_season": "Retail GCC & Omnichannel Supply Chain Surge",
        "week_title": "Walmart Global Tech & E-Commerce Logistics Hub",
        "target_companies": [
            {"company": "Walmart Global Tech", "location": "Bellandur & Kadubeesanahalli", "role": "Fulfillment Operations & Logistics Analyst", "portal": "https://careers.walmart.com", "ats": "Workday"},
            {"company": "Amazon India", "location": "World Trade Center, Malleshwaram", "role": "Transportation Specialist & Operations Analyst", "portal": "https://www.amazon.jobs/en/locations/bangalore-india", "ats": "Internal iCIMS"}
        ],
        "role_categories": ["Fulfillment Operations", "Transportation", "Process Optimization"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Target Amazon Transportation Services (ATS) and Walmart logistics hubs with 1-click tailored resume.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 7,
        "month": "February",
        "quarter": "Q1",
        "hiring_season": "Retail GCC & Omnichannel Supply Chain Surge",
        "week_title": "Flipkart & Domestic E-Commerce Supply Chain",
        "target_companies": [
            {"company": "Flipkart", "location": "Bellandur ORR", "role": "Supply Chain Design & Operations Trainee", "portal": "https://www.flipkartcareers.com", "ats": "Internal Portal"},
            {"company": "Myntra", "location": "Hosur Road", "role": "Supply Chain Associate (Vendor & Logistics)", "portal": "https://careers.myntra.com", "ats": "Lever"}
        ],
        "role_categories": ["E-Commerce Logistics", "Vendor Operations", "Analytics"],
        "cycle_stage": "Assessments & Interviews",
        "action_playbook": "Present data-driven inventory metrics and vendor SLAs.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 8,
        "month": "February",
        "quarter": "Q1",
        "hiring_season": "Retail GCC & Omnichannel Supply Chain Surge",
        "week_title": "FMCG Supply Chain Operations Intake",
        "target_companies": [
            {"company": "Unilever (HUL)", "location": "Whitefield & Bellandur", "role": "Customer Operations & Logistics Trainee", "portal": "https://careers.unilever.com", "ats": "Workday"},
            {"company": "ITC Limited", "location": "ITC Infotech Park, Banaswadi", "role": "Supply Chain & Distribution Operations Associate", "portal": "https://www.itcportal.com/careers", "ats": "Internal Portal"}
        ],
        "role_categories": ["FMCG Distribution", "Logistics", "Operations"],
        "cycle_stage": "Shortlisting",
        "action_playbook": "Highlight FMCG primary/secondary distribution models and SKU-level accuracy.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 9,
        "month": "March",
        "quarter": "Q1",
        "hiring_season": "End-of-Financial-Year Global Freight & EXIM Clearance",
        "week_title": "A.P. Moller - Maersk Global Service Center Intake",
        "target_companies": [
            {"company": "Maersk GSC", "location": "Bellandur ORR", "role": "Ocean Freight Operations & Customs Specialist", "portal": "https://www.maersk.com/careers", "ats": "Workday"},
            {"company": "Hapag-Lloyd GBS", "location": "Manyata Tech Park", "role": "Vessel Operations & Booking Analyst", "portal": "https://www.hapag-lloyd.com/en/careers.html", "ats": "SuccessFactors"}
        ],
        "role_categories": ["Ocean Freight", "EXIM Documentation", "Bill of Lading"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Deploy EXIM credential (EXP-004) covering Bill of Lading, HS Codes, and demurrage mitigation.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 10,
        "month": "March",
        "quarter": "Q1",
        "hiring_season": "End-of-Financial-Year Global Freight & EXIM Clearance",
        "week_title": "DHL Global Forwarding & Air Cargo Logistics",
        "target_companies": [
            {"company": "DHL Global Forwarding", "location": "Kempegowda Airport Cargo Village", "role": "Air Freight & Customs Brokerage Trainee", "portal": "https://careers.dhl.com", "ats": "SuccessFactors"},
            {"company": "FedEx Express India", "location": "Electronic City", "role": "Clearance Operations & Gateway Specialist", "portal": "https://careers.fedex.com", "ats": "Workday"}
        ],
        "role_categories": ["Air Freight Logistics", "Customs Brokerage", "Gateway Ops"],
        "cycle_stage": "Screening & Interviews",
        "action_playbook": "Target air express clearance documentation, IATA standards, and DG handling.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 11,
        "month": "March",
        "quarter": "Q1",
        "hiring_season": "End-of-Financial-Year Global Freight & EXIM Clearance",
        "week_title": "Kuehne+Nagel & DB Schenker 3PL Solutions",
        "target_companies": [
            {"company": "Kuehne+Nagel", "location": "Varthur Road, Whitefield", "role": "Contract Logistics & Operations Analyst", "portal": "https://jobs.kuehne-nagel.com", "ats": "Workday"},
            {"company": "DB Schenker", "location": "Whitefield", "role": "Supply Chain & EXIM Solutions Associate", "portal": "https://www.dbschenker.com/global/careers", "ats": "Internal Portal"}
        ],
        "role_categories": ["3PL Contract Logistics", "Freight Forwarding", "Operations"],
        "cycle_stage": "Interviews & Offers",
        "action_playbook": "Emphasize 3PL warehouse management, cross-docking, and container freight stations (CFS).",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 12,
        "month": "March",
        "quarter": "Q1",
        "hiring_season": "End-of-Financial-Year Global Freight & EXIM Clearance",
        "week_title": "EY GDS & KPMG Global Delivery Spring Ingestion",
        "target_companies": [
            {"company": "EY Global Delivery Services (GDS)", "location": "RMZ Infinity & Manyata", "role": "Business Operations & Supply Chain Consultant", "portal": "https://www.ey.com/en_in/careers", "ats": "SuccessFactors"},
            {"company": "KPMG Global Services (KGS)", "location": "Manyata Tech Park & Bellandur", "role": "Operations & Analytics Associate", "portal": "https://home.kpmg/in/en/home/careers.html", "ats": "Workday"}
        ],
        "role_categories": ["Management Consulting", "Supply Chain", "Business Ops"],
        "cycle_stage": "Applications & Superdays",
        "action_playbook": "Position BBA International Business foundation and consulting project delivery.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 13,
        "month": "March",
        "quarter": "Q1",
        "hiring_season": "End-of-Financial-Year Global Freight & EXIM Clearance",
        "week_title": "Q1 Clearance Superday & Offer Commitments",
        "target_companies": [
            {"company": "Genpact", "location": "Pritech Park, Bellandur", "role": "International Trade & Supply Chain Management Trainee", "portal": "https://www.genpact.com/careers", "ats": "Taleo"},
            {"company": "WNS Global Services", "location": "Whitefield", "role": "Shipping & Logistics Operations Specialist", "portal": "https://www.wns.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Trade Operations", "BPS Management", "Analytics"],
        "cycle_stage": "Offer Rollouts",
        "action_playbook": "Engage Offer Defense Engine (Tab 9) to secure upper-quartile entry compensation.",
        "verified_seam": "EXP-004"
    },

    # Q2: WEEKS 14 - 26 (April - June)
    {
        "week_number": 14,
        "month": "April",
        "quarter": "Q2",
        "hiring_season": "Q2 Global Institutional Banking & Trade Finance Drive",
        "week_title": "Standard Chartered GBS Trade Finance Corridor",
        "target_companies": [
            {"company": "Standard Chartered GBS", "location": "Embassy GolfLinks, Domlur", "role": "Trade Finance Operations Analyst (LC / Guarantees)", "portal": "https://www.sc.com/en/careers", "ats": "Taleo"},
            {"company": "HSBC Electronic Data Processing", "location": "Manyata Tech Park", "role": "Global Trade & Receivables Finance Operations", "portal": "https://www.hsbc.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Trade Finance", "Letter of Credit", "Banking Ops"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Highlight Incoterms 2020, documentary credit rules (UCP 600), and EXIM compliance.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 15,
        "month": "April",
        "quarter": "Q2",
        "hiring_season": "Q2 Global Institutional Banking & Trade Finance Drive",
        "week_title": "JPMorgan Chase & Institutional Asset Operations",
        "target_companies": [
            {"company": "JPMorgan Chase", "location": "Prestige Tech Park, ORR", "role": "Commercial Banking Operations Specialist", "portal": "https://careers.jpmorgan.com", "ats": "Workday"},
            {"company": "Citi Global Service Center", "location": "Bellandur ORR", "role": "Treasury & Trade Solutions Analyst", "portal": "https://careers.citigroup.com", "ats": "Workday"}
        ],
        "role_categories": ["Treasury Operations", "Trade Solutions", "Cross-Border Settlement"],
        "cycle_stage": "Assessments",
        "action_playbook": "Focus on cross-border wire execution, FX hedging workflows, and regulatory filings.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 16,
        "month": "April",
        "quarter": "Q2",
        "hiring_season": "Q2 Global Institutional Banking & Trade Finance Drive",
        "week_title": "Wells Fargo & Northern Trust Asset Servicing",
        "target_companies": [
            {"company": "Wells Fargo India", "location": "Bagmane Constellation Business Park", "role": "Supply Chain Finance & Commercial Lending Analyst", "portal": "https://www.wellsfargojobs.com", "ats": "Workday"},
            {"company": "Northern Trust", "location": "Manyata Tech Park", "role": "Global Fund Operations Analyst", "portal": "https://www.northerntrust.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Supply Chain Finance", "Fund Operations", "Compliance"],
        "cycle_stage": "Interviews",
        "action_playbook": "Demonstrate knowledge of reverse factoring, vendor early-payment discounts, and audit trails.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 17,
        "month": "April",
        "quarter": "Q2",
        "hiring_season": "Q2 Global Institutional Banking & Trade Finance Drive",
        "week_title": "Barclays & Deutsche Bank Corporate Services",
        "target_companies": [
            {"company": "Barclays Global Service Centre", "location": "Bellandur ORR", "role": "Corporate Banking Operations Trainee", "portal": "https://home.barclays/careers", "ats": "Taleo"},
            {"company": "Deutsche Bank Group (DWS)", "location": "Electronic City", "role": "Trade Settlement & Institutional Operations Specialist", "portal": "https://careers.db.com", "ats": "Workday"}
        ],
        "role_categories": ["Settlement Operations", "Corporate Banking", "Risk"],
        "cycle_stage": "Offers & Onboarding",
        "action_playbook": "Present high-reliability operational track record (99.2% QA precision seam).",
        "verified_seam": "EXP-002"
    },
    {
        "week_number": 18,
        "month": "May",
        "quarter": "Q2",
        "hiring_season": "Strategy Consulting & Management Advisory Superdays",
        "week_title": "McKinsey & Co. Knowledge Center Intake",
        "target_companies": [
            {"company": "McKinsey & Company", "location": "Vittal Mallya Road, CBD", "role": "Operations & Supply Chain Research Analyst", "portal": "https://www.mckinsey.com/careers", "ats": "Internal Portal"},
            {"company": "Boston Consulting Group (BCG)", "location": "UB City, Vittal Mallya Road", "role": "Global Capability Operations Associate", "portal": "https://www.bcg.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Strategy Research", "Supply Chain Benchmarking", "Advisory"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Showcase structured problem-solving frameworks (MECE, Issue Trees, Cost-to-Serve modeling).",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 19,
        "month": "May",
        "quarter": "Q2",
        "hiring_season": "Strategy Consulting & Management Advisory Superdays",
        "week_title": "Bain & Company Capability Network (BCN)",
        "target_companies": [
            {"company": "Bain & Company (BCN)", "location": "Prestige Nebula, Infantry Road", "role": "Private Equity & Operations Due Diligence Analyst", "portal": "https://www.bain.com/careers", "ats": "Workday"},
            {"company": "Oliver Wyman", "location": "Lavelle Road, CBD", "role": "Logistics & Supply Chain Research Associate", "portal": "https://www.oliverwyman.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Commercial Due Diligence", "Operations Research", "Advisory"],
        "cycle_stage": "Shortlisting & Cases",
        "action_playbook": "Practice business case frameworks with STAR Simulator (Tab 7).",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 20,
        "month": "May",
        "quarter": "Q2",
        "hiring_season": "Strategy Consulting & Management Advisory Superdays",
        "week_title": "Accenture Strategy & Global Operations",
        "target_companies": [
            {"company": "Accenture India", "location": "Bannerghatta Road & Bellandur", "role": "Supply Chain Strategy & Operations Analyst", "portal": "https://www.accenture.com/in-en/careers", "ats": "Workday"},
            {"company": "Cognizant Consulting", "location": "Manyata Tech Park", "role": "Process Consulting Associate (Logistics)", "portal": "https://careers.cognizant.com", "ats": "Taleo"}
        ],
        "role_categories": ["Digital Supply Chain", "Process Optimization", "Consulting"],
        "cycle_stage": "Case Superdays",
        "action_playbook": "Emphasize supply chain digital twin concepts, control towers, and ERP integrations.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 21,
        "month": "May",
        "quarter": "Q2",
        "hiring_season": "Strategy Consulting & Management Advisory Superdays",
        "week_title": "Kearney & Roland Berger Operations Center",
        "target_companies": [
            {"company": "Kearney India", "location": "Residency Road, Bangalore", "role": "Procurement & Strategic Sourcing Analyst", "portal": "https://www.kearney.com/careers", "ats": "Workday"},
            {"company": "Alvarez & Marsal", "location": "MG Road, Bangalore", "role": "Performance Improvement Operations Associate", "portal": "https://www.alvarezandmarsal.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Strategic Sourcing", "Performance Improvement", "Procurement"],
        "cycle_stage": "Superday Interviews",
        "action_playbook": "Highlight spend analysis, vendor consolidation, and contract renegotiation case studies.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 22,
        "month": "June",
        "quarter": "Q2",
        "hiring_season": "High-Growth Unicorn & AI Scaleup Ingestion",
        "week_title": "Meesho & Social Commerce Operations Blitz",
        "target_companies": [
            {"company": "Meesho", "location": "Koramangala, Bangalore", "role": "Operations & Category Associate (Supply Chain)", "portal": "https://www.meesho.io/jobs", "ats": "Lever"},
            {"company": "Groww", "location": "Vaishnavi Tech Park, Bellandur", "role": "Customer & Brokerage Operations Associate", "portal": "https://groww.in/careers", "ats": "Greenhouse"}
        ],
        "role_categories": ["E-Commerce Operations", "Category Management", "Brokerage Ops"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Leverage Startup Operations credential (EXP-005) for high cultural and operational alignment.",
        "verified_seam": "EXP-005"
    },
    {
        "week_number": 23,
        "month": "June",
        "quarter": "Q2",
        "hiring_season": "High-Growth Unicorn & AI Scaleup Ingestion",
        "week_title": "Swiggy & Zepto Quick-Commerce Logistics Surge",
        "target_companies": [
            {"company": "Swiggy", "location": "Devarabisanahalli, ORR", "role": "Instamart Supply Chain & Dark Store Operations Analyst", "portal": "https://careers.swiggy.com", "ats": "Greenhouse"},
            {"company": "Zepto", "location": "Bellandur ORR", "role": "City Logistics & Micro-Fulfillment Operations Specialist", "portal": "https://www.zeptonow.com/careers", "ats": "Lever"}
        ],
        "role_categories": ["Quick Commerce", "Dark Store Operations", "Fleet Logistics"],
        "cycle_stage": "Screening & Case Studies",
        "action_playbook": "Demonstrate understanding of 10-minute dispatch routing, shrinkage control, and inventory replenishment.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 24,
        "month": "June",
        "quarter": "Q2",
        "hiring_season": "High-Growth Unicorn & AI Scaleup Ingestion",
        "week_title": "Razorpay & PhonePe Fintech Operations Wave",
        "target_companies": [
            {"company": "Razorpay", "location": "Koramangala, Bangalore", "role": "Merchant Operations & Risk Analyst", "portal": "https://razorpay.com/jobs", "ats": "Greenhouse"},
            {"company": "PhonePe", "location": "Bellandur ORR", "role": "Banking & Merchant Operations Associate", "portal": "https://www.phonepe.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Merchant Operations", "Fintech Risk", "Payment Settlement"],
        "cycle_stage": "Superdays",
        "action_playbook": "Highlight zero-tolerance transaction dispute handling and automated onboarding workflows.",
        "verified_seam": "EXP-002"
    },
    {
        "week_number": 25,
        "month": "June",
        "quarter": "Q2",
        "hiring_season": "High-Growth Unicorn & AI Scaleup Ingestion",
        "week_title": "Cred & Urban Company Premium Services Ops",
        "target_companies": [
            {"company": "CRED", "location": "Indiranagar, Bangalore", "role": "Operations & Member Experience Specialist", "portal": "https://careers.cred.club", "ats": "Lever"},
            {"company": "Urban Company", "location": "HSR Layout", "role": "Supply Operations & Partner Success Associate", "portal": "https://www.urbancompany.com/careers", "ats": "Greenhouse"}
        ],
        "role_categories": ["Premium Operations", "Partner Success", "Quality Assurance"],
        "cycle_stage": "Interviews & Offers",
        "action_playbook": "Focus on high-touch stakeholder operations and rigorous SLA compliance.",
        "verified_seam": "EXP-002"
    },
    {
        "week_number": 26,
        "month": "June",
        "quarter": "Q2",
        "hiring_season": "High-Growth Unicorn & AI Scaleup Ingestion",
        "week_title": "Mid-Year Graduation Clearance & Summer Finalization",
        "target_companies": [
            {"company": "Porter", "location": "HSR Layout, Bangalore", "role": "Intra-City Logistics Operations Trainee", "portal": "https://porter.in/careers", "ats": "Greenhouse"},
            {"company": "Shadowfax", "location": "Koramangala", "role": "Crowdsourced Logistics & Dispatch Analyst", "portal": "https://www.shadowfax.in/careers", "ats": "Lever"}
        ],
        "role_categories": ["Intra-City Logistics", "Dispatch Systems", "Operations"],
        "cycle_stage": "Offer Rollouts",
        "action_playbook": "Secure mid-year full-time commitments with pre-staged application packages.",
        "verified_seam": "EXP-004"
    },

    # Q3: WEEKS 27 - 39 (July - September)
    {
        "week_number": 27,
        "month": "July",
        "quarter": "Q3",
        "hiring_season": "Q3 Campus Kickoff & Early Bird Graduate Programs",
        "week_title": "Infosys BPM & ITES Global Operations Wave",
        "target_companies": [
            {"company": "Infosys BPM", "location": "Electronic City, Bangalore", "role": "Process Executive (Supply Chain & International Business)", "portal": "https://www.infosysbpm.com/careers", "ats": "Internal Portal"},
            {"company": "Wipro Global Operations", "location": "Sarjapur Doddakannelli", "role": "International Trade & Logistics Associate", "portal": "https://careers.wipro.com", "ats": "SuccessFactors"}
        ],
        "role_categories": ["Global Process Services", "International Operations", "ITES"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Target early off-campus batch slots with verified BBA IB transcripts and projects.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 28,
        "month": "July",
        "quarter": "Q3",
        "hiring_season": "Q3 Campus Kickoff & Early Bird Graduate Programs",
        "week_title": "TCS BPS & HCLTech Enterprise Services",
        "target_companies": [
            {"company": "Tata Consultancy Services (TCS BPS)", "location": "Whitefield & Electronic City", "role": "International Business Operations Analyst", "portal": "https://www.tcs.com/careers", "ats": "iBegin"},
            {"company": "HCLTech", "location": "Jigani / Electronic City", "role": "Global Sourcing & Procurement Associate", "portal": "https://www.hcltech.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Procurement Operations", "International Business", "Enterprise"],
        "cycle_stage": "Online Assessments",
        "action_playbook": "Take advantage of early registration drives before national off-campus pools open.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 29,
        "month": "July",
        "quarter": "Q3",
        "hiring_season": "Q3 Campus Kickoff & Early Bird Graduate Programs",
        "week_title": "Mercedes-Benz R&D (MBRDI) Procurement Hub",
        "target_companies": [
            {"company": "Mercedes-Benz R&D India (MBRDI)", "location": "Whitefield & Manyata", "role": "Global Supply Chain & Logistics Operations Trainee", "portal": "https://www.mbrdi.co.in/careers", "ats": "Workday"},
            {"company": "BMW Group TechHub", "location": "Whitefield", "role": "Automotive Logistics & Sourcing Associate", "portal": "https://www.bmwgroup.jobs", "ats": "SuccessFactors"}
        ],
        "role_categories": ["Automotive Supply Chain", "Parts Logistics", "Global Sourcing"],
        "cycle_stage": "Applications & Screening",
        "action_playbook": "Highlight German/EU import documentation standards, just-in-time (JIT) manufacturing logistics.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 30,
        "month": "July",
        "quarter": "Q3",
        "hiring_season": "Q3 Campus Kickoff & Early Bird Graduate Programs",
        "week_title": "Capgemini & Tech Mahindra Global Centers",
        "target_companies": [
            {"company": "Capgemini India", "location": "Whitefield & Manyata", "role": "Supply Chain & Business Operations Consultant", "portal": "https://www.capgemini.com/in-en/careers", "ats": "SuccessFactors"},
            {"company": "Tech Mahindra", "location": "Electronic City", "role": "International Trade Process Specialist", "portal": "https://careers.techmahindra.com", "ats": "Internal Portal"}
        ],
        "role_categories": ["Operations Consulting", "Trade Operations", "Analytics"],
        "cycle_stage": "Interviews",
        "action_playbook": "Present cross-cultural trade documentation and international market analysis.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 31,
        "month": "August",
        "quarter": "Q3",
        "hiring_season": "Aerospace, Defense & Heavy Industrial Monsoon Intake",
        "week_title": "Airbus India Global Sourcing & Logistics",
        "target_companies": [
            {"company": "Airbus India", "location": "Mahadevapura / Whitefield", "role": "Procurement & Aerospace Supply Chain Specialist", "portal": "https://www.airbus.com/en/careers", "ats": "Workday"},
            {"company": "Honeywell Aerospace", "location": "Bellandur ORR", "role": "Integrated Supply Chain & Logistics Associate", "portal": "https://careers.honeywell.com", "ats": "Workday"}
        ],
        "role_categories": ["Aerospace Logistics", "Sourcing Operations", "Aero Systems"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Primary target for Aero India 2025 Coordinator credential (EXP-001)! Unmatched direct relevance.",
        "verified_seam": "EXP-001"
    },
    {
        "week_number": 32,
        "month": "August",
        "quarter": "Q3",
        "hiring_season": "Aerospace, Defense & Heavy Industrial Monsoon Intake",
        "week_title": "General Electric (GE Aerospace) JFWTC Intake",
        "target_companies": [
            {"company": "GE Aerospace (JFWTC)", "location": "John F. Welch Technology Centre, Whitefield", "role": "Global Sourcing & Logistics Operations Associate", "portal": "https://jobs.gecareers.com", "ats": "Workday"},
            {"company": "Safran India", "location": "Whitefield", "role": "Supply Chain & Production Operations Trainee", "portal": "https://www.safran-group.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Aerospace Sourcing", "Heavy Industrial Logistics", "Operations"],
        "cycle_stage": "Assessments & Shortlisting",
        "action_playbook": "Direct outreach to GE Aerospace Whitefield talent acquisition team citing aviation expo management.",
        "verified_seam": "EXP-001"
    },
    {
        "week_number": 33,
        "month": "August",
        "quarter": "Q3",
        "hiring_season": "Aerospace, Defense & Heavy Industrial Monsoon Intake",
        "week_title": "Siemens & ABB Industrial Automation Supply Chain",
        "target_companies": [
            {"company": "Siemens Technology India", "location": "Electronic City", "role": "Supply Chain Excellence & Operations Analyst", "portal": "https://jobs.siemens.com", "ats": "Workday"},
            {"company": "ABB India", "location": "Peenya & Manyata", "role": "Export-Import & Logistics Operations Associate", "portal": "https://careers.abb/global/en", "ats": "Workday"}
        ],
        "role_categories": ["Industrial Automation", "EXIM Operations", "Customs"],
        "cycle_stage": "Interviews",
        "action_playbook": "Highlight capital goods import clearance, EPC project logistics, and tariff optimization.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 34,
        "month": "August",
        "quarter": "Q3",
        "hiring_season": "Aerospace, Defense & Heavy Industrial Monsoon Intake",
        "week_title": "Schneider Electric & Bosch Global Services",
        "target_companies": [
            {"company": "Schneider Electric", "location": "Attibele & Whitefield", "role": "Global Supply Chain Planning & Operations Trainee", "portal": "https://www.se.com/in/en/about-us/careers", "ats": "Workday"},
            {"company": "Robert Bosch India (BGSW)", "location": "Adugodi & Electronic City", "role": "International Sourcing & Logistics Specialist", "portal": "https://www.bosch.in/careers", "ats": "SmartRecruiters"}
        ],
        "role_categories": ["Planning Operations", "International Sourcing", "Supply Chain"],
        "cycle_stage": "Superdays",
        "action_playbook": "Focus on sales & operations planning (S&OP), safety stock calculations, and vendor OTIF.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 35,
        "month": "August",
        "quarter": "Q3",
        "hiring_season": "Aerospace, Defense & Heavy Industrial Monsoon Intake",
        "week_title": "Balfour Beatty & Infrastructure Operations",
        "target_companies": [
            {"company": "L&T Construction (B&F)", "location": "Hebbal, Bangalore", "role": "Project Logistics & Procurement Associate", "portal": "https://www.larsentoubro.com/corporate/careers", "ats": "Internal Portal"},
            {"company": "Cummins India", "location": "Electronic City", "role": "Engine Systems Supply Chain Analyst", "portal": "https://www.cummins.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Project Procurement", "Heavy Logistics", "Vendor Management"],
        "cycle_stage": "Offers & Onboarding",
        "action_playbook": "Demonstrate heavy project freight handling, road permits, and inter-state logistics compliance.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 36,
        "month": "September",
        "quarter": "Q3",
        "hiring_season": "Festive Season Peak Supply Chain & Logistics Expansion",
        "week_title": "Delhivery & E-Commerce Express Logistics Hub",
        "target_companies": [
            {"company": "Delhivery", "location": "Bommasandra & Whitefield", "role": "Hub Operations & Express Logistics Trainee", "portal": "https://www.delhivery.com/careers", "ats": "Internal Portal"},
            {"company": "Blue Dart Express", "location": "Airport Road & Peenya", "role": "Aviation Logistics & Gateway Operations Associate", "portal": "https://www.bluedart.com/careers", "ats": "Internal Portal"}
        ],
        "role_categories": ["Express Logistics", "Hub Operations", "Gateway Clearance"],
        "cycle_stage": "Mass Applications Open",
        "action_playbook": "Highlight high-volume sortation hub throughput, linehaul dispatch, and parcel tracking.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 37,
        "month": "September",
        "quarter": "Q3",
        "hiring_season": "Festive Season Peak Supply Chain & Logistics Expansion",
        "week_title": "Amazon ATS & Flipkart Hub Superday Wave",
        "target_companies": [
            {"company": "Amazon Transportation Services (ATS)", "location": "Whitefield Fulfillment Center", "role": "Area Manager / Shift Operations Lead", "portal": "https://www.amazon.jobs", "ats": "Internal iCIMS"},
            {"company": "Flipkart Ekart", "location": "Hosamane & Malur Mega Hub", "role": "Operations Executive - Linehaul & Logistics", "portal": "https://www.flipkartcareers.com", "ats": "Internal Portal"}
        ],
        "role_categories": ["Linehaul Operations", "Sortation Centers", "Logistics Leadership"],
        "cycle_stage": "Assessment & Rapid Interviews",
        "action_playbook": "Position operational grit, night-shift readiness, and KPI delivery under tight deadlines.",
        "verified_seam": "EXP-002"
    },
    {
        "week_number": 38,
        "month": "September",
        "quarter": "Q3",
        "hiring_season": "Festive Season Peak Supply Chain & Logistics Expansion",
        "week_title": "Xpressbees & Ecom Express Festive Surge",
        "target_companies": [
            {"company": "Xpressbees", "location": "Peenya Industrial Area", "role": "Last-Mile & Middle-Mile Operations Analyst", "portal": "https://www.xpressbees.com/careers", "ats": "Internal Portal"},
            {"company": "Ecom Express", "location": "Banaswadi", "role": "Network Operations & Logistics Specialist", "portal": "https://ecomexpress.in/careers", "ats": "Internal Portal"}
        ],
        "role_categories": ["Middle-Mile Logistics", "Last-Mile Delivery", "Operations"],
        "cycle_stage": "Superdays & Rolling Offers",
        "action_playbook": "Deploy metrics on SLA breach reduction, reverse pickup tracking, and COD reconciliation.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 39,
        "month": "September",
        "quarter": "Q3",
        "hiring_season": "Festive Season Peak Supply Chain & Logistics Expansion",
        "week_title": "End-of-Q3 Festive Clearance & Fast Onboarding",
        "target_companies": [
            {"company": "Gati KWE", "location": "Hosur Road", "role": "Multimodal Logistics & Supply Chain Associate", "portal": "https://www.gati.com/careers", "ats": "Internal Portal"},
            {"company": "TCI Freight (Transport Corp of India)", "location": "Kalasipalyam & Electronic City", "role": "Freight Operations & Fleet Coordinator", "portal": "https://www.tcil.com/tcil/careers.html", "ats": "Internal Portal"}
        ],
        "role_categories": ["Multimodal Transport", "Fleet Coordination", "Freight Ops"],
        "cycle_stage": "Offer Rollouts",
        "action_playbook": "Negotiate flexible start dates aligning with final semester requirements.",
        "verified_seam": "EXP-004"
    },

    # Q4: WEEKS 40 - 52 (October - December)
    {
        "week_number": 40,
        "month": "October",
        "quarter": "Q4",
        "hiring_season": "Q4 Technology GCC AI Ops & Data Intelligence Surge",
        "week_title": "Uber Bangalore Tech Center Operations Wave",
        "target_companies": [
            {"company": "Uber India", "location": "Ranka Junction, KR Puram", "role": "Operations Specialist (Driver & Marketplace Growth)", "portal": "https://www.uber.com/in/en/careers", "ats": "Greenhouse"},
            {"company": "Grab India R&D", "location": "Bellandur ORR", "role": "Transport & Food Operations Analyst", "portal": "https://grab.careers", "ats": "Workday"}
        ],
        "role_categories": ["Marketplace Operations", "Mobility Analytics", "Operations"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Showcase supply-demand marketplace matching, surge pricing mechanics, and driver onboarding.",
        "verified_seam": "EXP-005"
    },
    {
        "week_number": 41,
        "month": "October",
        "quarter": "Q4",
        "hiring_season": "Q4 Technology GCC AI Ops & Data Intelligence Surge",
        "week_title": "Instawork & On-Demand Labor Ops (Exact Seam!)",
        "target_companies": [
            {"company": "Instawork", "location": "Indiranagar, Bangalore", "role": "AI Data Operations & Quality Assurance Lead", "portal": "https://www.instawork.com/careers", "ats": "Lever"},
            {"company": "TaskUs India", "location": "Whitefield & Electronic City", "role": "AI Operations & Data Annotation Specialist", "portal": "https://www.taskus.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["AI Data Operations", "Quality Assurance", "Workforce Operations"],
        "cycle_stage": "Applications & Screenings",
        "action_playbook": "100% direct hit on Instawork AI Data Operations credential (EXP-002) with 99.2% QA Precision!",
        "verified_seam": "EXP-002"
    },
    {
        "week_number": 42,
        "month": "October",
        "quarter": "Q4",
        "hiring_season": "Q4 Technology GCC AI Ops & Data Intelligence Surge",
        "week_title": "Google India Business Operations & Trust/Safety",
        "target_companies": [
            {"company": "Google India", "location": "Bagmane Capital & RMZ Infinity", "role": "Business Operations & Strategy Associate", "portal": "https://careers.google.com/locations/bangalore", "ats": "Internal Portal"},
            {"company": "Microsoft India", "location": "Bagmane Constellation Business Park", "role": "Global Procurement & Commercial Operations Analyst", "portal": "https://careers.microsoft.com", "ats": "Workday"}
        ],
        "role_categories": ["Business Operations", "Strategic Procurement", "Global Sourcing"],
        "cycle_stage": "Superdays & Assessments",
        "action_playbook": "Highlight rigorous analytical modeling, spreadsheet automation, and global stakeholder management.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 43,
        "month": "October",
        "quarter": "Q4",
        "hiring_season": "Q4 Technology GCC AI Ops & Data Intelligence Surge",
        "week_title": "Cisco Systems & Intel Global Procurement Hubs",
        "target_companies": [
            {"company": "Cisco Systems", "location": "Cessna Business Park, Kadubeesanahalli", "role": "Supply Chain Operations & Manufacturing Partner Analyst", "portal": "https://jobs.cisco.com", "ats": "Workday"},
            {"company": "Intel India", "location": "Outer Ring Road, Bellandur", "role": "Global Sourcing Operations & Vendor Specialist", "portal": "https://jobs.intel.com", "ats": "Workday"}
        ],
        "role_categories": ["Semiconductor Supply Chain", "Vendor Sourcing", "Operations"],
        "cycle_stage": "Interviews",
        "action_playbook": "Present semiconductor supply chain resilience strategies, dual-sourcing, and inventory buffer math.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 44,
        "month": "October",
        "quarter": "Q4",
        "hiring_season": "Q4 Technology GCC AI Ops & Data Intelligence Surge",
        "week_title": "Dell Technologies & HP Global Sourcing",
        "target_companies": [
            {"company": "Dell Technologies", "location": "Domlur & Bagmane Tech Park", "role": "Global Fulfillment & Logistics Operations Trainee", "portal": "https://jobs.dell.com", "ats": "Workday"},
            {"company": "HP India", "location": "Electronic City", "role": "Supply Chain Operations & Distribution Associate", "portal": "https://jobs.hp.com", "ats": "Workday"}
        ],
        "role_categories": ["Hardware Logistics", "Global Fulfillment", "Operations"],
        "cycle_stage": "Offers & Onboarding",
        "action_playbook": "Focus on global ocean-to-air multimodal transit times and warranty parts reverse logistics.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 45,
        "month": "November",
        "quarter": "Q4",
        "hiring_season": "Winter Associate & Off-Campus Conversion Drive",
        "week_title": "NVIDIA & Semiconductor AI Operations Center",
        "target_companies": [
            {"company": "NVIDIA India", "location": "Bagmane Tech Park, CV Raman Nagar", "role": "Operations & Business Process Associate", "portal": "https://www.nvidia.com/en-in/about-nvidia/careers", "ats": "Workday"},
            {"company": "Qualcomm India", "location": "Bellandur ORR", "role": "Supply Chain & Material Operations Analyst", "portal": "https://www.qualcomm.com/company/careers", "ats": "Workday"}
        ],
        "role_categories": ["AI Operations", "Material Management", "Business Process"],
        "cycle_stage": "Applications Open",
        "action_playbook": "Position AI-assisted workflow optimization (EXP-005) and zero-error operational controls.",
        "verified_seam": "EXP-005"
    },
    {
        "week_number": 46,
        "month": "November",
        "quarter": "Q4",
        "hiring_season": "Winter Associate & Off-Campus Conversion Drive",
        "week_title": "Adobe & Salesforce India Enterprise Ops",
        "target_companies": [
            {"company": "Adobe India", "location": "Prestige Platina Tech Park, Marathahalli", "role": "Business Operations & Deal Desk Specialist", "portal": "https://www.adobe.com/careers.html", "ats": "Workday"},
            {"company": "Salesforce India", "location": "SJR I-Park, Whitefield", "role": "Revenue Operations & Contract Analyst", "portal": "https://www.salesforce.com/company/careers", "ats": "Workday"}
        ],
        "role_categories": ["Deal Desk Operations", "Revenue Operations", "Contracts"],
        "cycle_stage": "Assessments",
        "action_playbook": "Highlight contract compliance, commercial pricing rules, and cross-functional deal approvals.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 47,
        "month": "November",
        "quarter": "Q4",
        "hiring_season": "Winter Associate & Off-Campus Conversion Drive",
        "week_title": "SAP Labs India & Oracle Cloud Operations",
        "target_companies": [
            {"company": "SAP Labs India", "location": "Whitefield", "role": "Global Procurement & Commercial Services Trainee", "portal": "https://jobs.sap.com", "ats": "SuccessFactors"},
            {"company": "Oracle India", "location": "Bannerghatta Road & Bellandur", "role": "Supply Chain Applications & Operations Analyst", "portal": "https://www.oracle.com/in/corporate/careers", "ats": "Taleo"}
        ],
        "role_categories": ["Enterprise ERP", "Procurement Operations", "Supply Chain"],
        "cycle_stage": "Superdays",
        "action_playbook": "Demonstrate fluency in ERP procurement cycles (Procure-to-Pay, Order-to-Cash).",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 48,
        "month": "November",
        "quarter": "Q4",
        "hiring_season": "Winter Associate & Off-Campus Conversion Drive",
        "week_title": "Target & Lowe's Q4 Festive Wrap Intake",
        "target_companies": [
            {"company": "Target India", "location": "Manyata Tech Park", "role": "Global Inventory & Replenishment Analyst", "portal": "https://india.target.com/careers", "ats": "Workday"},
            {"company": "Lowe's India", "location": "Manyata Tech Park", "role": "Supply Chain Analytics & Demand Planning Specialist", "portal": "https://www.lowes.co.in/careers", "ats": "Workday"}
        ],
        "role_categories": ["Demand Planning", "Inventory Management", "Analytics"],
        "cycle_stage": "Superdays & Offers",
        "action_playbook": "Present seasonal demand forecasting models and safety stock optimization.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 49,
        "month": "December",
        "quarter": "Q4",
        "hiring_season": "Year-End Fast-Track Clearance & 2026 Commitments",
        "week_title": "EXL Service & Analytics Operations Superday",
        "target_companies": [
            {"company": "EXL Service", "location": "Pritech Park, Bellandur", "role": "Analytics & Supply Chain Operations Associate", "portal": "https://www.exlservice.com/careers", "ats": "Taleo"},
            {"company": "Mu Sigma", "location": "ITPL, Whitefield", "role": "Trainee Decision Scientist (Supply Chain & Operations)", "portal": "https://www.mu-sigma.com/careers", "ats": "Internal Portal"}
        ],
        "role_categories": ["Decision Sciences", "Operations Analytics", "Consulting"],
        "cycle_stage": "Applications & Superdays",
        "action_playbook": "Deploy quantitative case walk-throughs using STAR method (Tab 7).",
        "verified_seam": "EXP-002"
    },
    {
        "week_number": 50,
        "month": "December",
        "quarter": "Q4",
        "hiring_season": "Year-End Fast-Track Clearance & 2026 Commitments",
        "week_title": "Diageo & Global Shared Services Beverage Logistics",
        "target_companies": [
            {"company": "Diageo Business Services India", "location": "Karle Town Centre, Nagavara", "role": "Global Supply Operations & Logistics Specialist", "portal": "https://www.diageo.com/en/careers", "ats": "Workday"},
            {"company": "AB InBev GCC", "location": "Manyata Tech Park", "role": "Logistics & Fleet Operations Trainee", "portal": "https://www.abinbev.com/careers", "ats": "Workday"}
        ],
        "role_categories": ["Beverage Supply Chain", "Excise & Customs Logistics", "Operations"],
        "cycle_stage": "Interviews",
        "action_playbook": "Highlight bonded warehousing, state excise permit logistics, and route optimization.",
        "verified_seam": "EXP-004"
    },
    {
        "week_number": 51,
        "month": "December",
        "quarter": "Q4",
        "hiring_season": "Year-End Fast-Track Clearance & 2026 Commitments",
        "week_title": "Bespoke Consulting & Boutique Placement Ingestion",
        "target_companies": [
            {"company": "Michael Page India", "location": "MG Road, Bangalore", "role": "Supply Chain & Operations Talent Pool Intake", "portal": "https://www.michaelpage.co.in", "ats": "Agency Portal"},
            {"company": "Randstad India", "location": "Koramangala", "role": "GCC Operations & Logistics Specialist Register", "portal": "https://www.randstad.in", "ats": "Agency Portal"}
        ],
        "role_categories": ["Executive Placement", "Lateral Fast-Track", "Operations"],
        "cycle_stage": "Agency Intake & Registry",
        "action_playbook": "Upload print-ready 1-page ATS resumes (Tab 8) directly to premier Bangalore agency heads.",
        "verified_seam": "EXP-003"
    },
    {
        "week_number": 52,
        "month": "December",
        "quarter": "Q4",
        "hiring_season": "Year-End Fast-Track Clearance & 2026 Commitments",
        "week_title": "New Year Master Fast-Track Lock-in",
        "target_companies": [
            {"company": "Vectis Trade Technologies", "location": "Bangalore Urban", "role": "Founding Operations & Global Logistics Lead", "portal": "Internal Sovereign Track", "ats": "Direct Founder Track"},
            {"company": "DSU Industry Placement Cell", "location": "Kudlu Gate / Harohalli", "role": "Tier-1 Day-1 Corporate Placement Offer Lock", "portal": "DSU Official Portal", "ats": "Institutional"}
        ],
        "role_categories": ["Founding Operations", "Executive Placement", "Corporate"],
        "cycle_stage": "Final Contract Lock-in",
        "action_playbook": "Compare all offer letters using GCC Salary Benchmark Engine (Tab 9) and lock in maximum CTC.",
        "verified_seam": "EXP-005"
    }
]

def init_calendar_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hiring_calendar_52_weeks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_number INTEGER UNIQUE,
        month TEXT,
        quarter TEXT,
        hiring_season TEXT,
        week_title TEXT,
        target_companies TEXT,
        role_categories TEXT,
        cycle_stage TEXT,
        action_playbook TEXT,
        verified_seam TEXT,
        staged_applications_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'ACTIVE',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Insert or replace all 52 weeks
    for w in CALENDAR_DATA:
        cur.execute("""
        INSERT INTO hiring_calendar_52_weeks 
        (week_number, month, quarter, hiring_season, week_title, target_companies, role_categories, cycle_stage, action_playbook, verified_seam, staged_applications_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(week_number) DO UPDATE SET
            month = excluded.month,
            quarter = excluded.quarter,
            hiring_season = excluded.hiring_season,
            week_title = excluded.week_title,
            target_companies = excluded.target_companies,
            role_categories = excluded.role_categories,
            cycle_stage = excluded.cycle_stage,
            action_playbook = excluded.action_playbook,
            verified_seam = excluded.verified_seam
        """, (
            w["week_number"],
            w["month"],
            w["quarter"],
            w["hiring_season"],
            w["week_title"],
            json.dumps(w["target_companies"]),
            json.dumps(w["role_categories"]),
            w["cycle_stage"],
            w["action_playbook"],
            w["verified_seam"],
            len(w["target_companies"])
        ))
        
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM hiring_calendar_52_weeks").fetchone()[0]
    conn.close()
    print(f"Successfully populated hiring_calendar_52_weeks with {count} weeks!")

if __name__ == "__main__":
    init_calendar_table()
