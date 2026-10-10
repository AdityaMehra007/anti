"""
Bengaluru Startup & Tech Platform Requisition Matrix:
Covers:
1. Instahyre (Inbound AI Matching: 6,870+ active Bengaluru jobs)
2. Cutshort (Startup AI Matching: 13,588+ active Bengaluru jobs)
3. Hirist.tech Product Track (Product Operations, APM, Strategy)
4. Hirist.tech E-Commerce Track (Category, Merchandising, Supply Operations)
5. Hirist.tech FinTech & EdTech Track (Risk, Payments, Client Onboarding)
"""

import csv

REQUISITIONS = [
    # --- INSTAHYRE BENGALURU STARTUPS & GCCS ---
    {
        "Platform": "Instahyre",
        "Requisition Title": "Operations Associate - Merchant Success & Settlements",
        "Company / Startup": "PhonePe (Walmart Group)",
        "Work Location": "Greenheart, Manyata Tech Park / Bellandur, Bengaluru",
        "Domain / Track": "FinTech & Payments Infrastructure",
        "Experience Level": "Fresher to 1 Year (BBA / B.Com)",
        "Core Skills Required": "Merchant Operations, Payment Reconciliation, SQL Basics, Advanced Excel, SLA Tracking",
        "Compensation Band": "Rs 5,50,000 - 8,00,000 PA",
        "Direct Portal Route URL": "https://www.instahyre.com/jobs-in-bangalore/"
    },
    {
        "Platform": "Instahyre",
        "Requisition Title": "Business Operations Analyst - Global Client Solutions",
        "Company / Startup": "Postman",
        "Work Location": "Indiranagar 100ft Road / EGL, Bengaluru",
        "Domain / Track": "Developer Tools & Enterprise SaaS",
        "Experience Level": "0 - 2 Years (BBA / Any Graduate)",
        "Core Skills Required": "Business Operations, CRM Hygiene (Salesforce), Process Documentation, Cross-Functional Coordination",
        "Compensation Band": "Rs 7,00,000 - 10,50,000 PA",
        "Direct Portal Route URL": "https://www.instahyre.com/jobs-in-bangalore/"
    },
    {
        "Platform": "Instahyre",
        "Requisition Title": "Inside Sales & Outbound Growth Representative",
        "Company / Startup": "Chargebee Technologies",
        "Work Location": "HSR Layout Sector 2, Outer Ring Road, Bengaluru",
        "Domain / Track": "Subscription Billing & FinTech SaaS",
        "Experience Level": "0 - 1.5 Years (BBA / Marketing)",
        "Core Skills Required": "Cold Outreach, Apollo.io, Lead Qualification, HubSpot CRM, Account Mapping",
        "Compensation Band": "Rs 5,50,000 - 8,50,000 PA + Variable Incentives",
        "Direct Portal Route URL": "https://www.instahyre.com/jobs-in-bangalore/"
    },

    # --- CUTSHORT STARTUP HIRING IN BENGALURU ---
    {
        "Platform": "Cutshort",
        "Requisition Title": "Product Operations Associate - AI Catalog & Taxonomy",
        "Company / Startup": "Zepto (Aadit & Kaivalya / KiranaKart)",
        "Work Location": "Koramangala 5th Block / Bellandur, Bengaluru",
        "Domain / Track": "Quick Commerce & Hyperlocal Logistics",
        "Experience Level": "Fresher to 2 Years (BBA / Graduate)",
        "Core Skills Required": "Catalog Management, Inventory SKU Tracking, Excel VLOOKUP/Pivot, Jira, Incident Triage",
        "Compensation Band": "Rs 5,00,000 - 7,50,000 PA",
        "Direct Portal Route URL": "https://cutshort.io/jobs/startup-jobs-in-bangalore-bengaluru"
    },
    {
        "Platform": "Cutshort",
        "Requisition Title": "Customer Success & Onboarding Specialist (US Timezone)",
        "Company / Startup": "Sprinto (Automated Security Compliance)",
        "Work Location": "HSR Layout Sector 4, Bengaluru",
        "Domain / Track": "Cybersecurity & SaaS Compliance",
        "Experience Level": "0 - 2 Years (BBA / High English Fluency)",
        "Core Skills Required": "Client Onboarding, Zendesk, Intercom, SLA Adherence, Account Health Monitoring",
        "Compensation Band": "Rs 6,00,000 - 9,00,000 PA + Night Shift Stipend",
        "Direct Portal Route URL": "https://cutshort.io/jobs/startup-jobs-in-bangalore-bengaluru"
    },
    {
        "Platform": "Cutshort",
        "Requisition Title": "Founders Office Operations Trainee",
        "Company / Startup": "Klub (FinTech Revenue Based Financing)",
        "Work Location": "Indiranagar, Bengaluru",
        "Domain / Track": "Alternative Debt & Venture Capital",
        "Experience Level": "Fresher (2024-2026 BBA / BMS)",
        "Core Skills Required": "Executive Support, Notion, Financial MIS Modeling, Pitch Presentation Formatting",
        "Compensation Band": "Rs 6,50,000 - 10,00,000 PA",
        "Direct Portal Route URL": "https://cutshort.io/jobs/startup-jobs-in-bangalore-bengaluru"
    },

    # --- HIRIST.TECH: PRODUCT JOBS TRACK ---
    {
        "Platform": "Hirist.tech (Product)",
        "Requisition Title": "Associate Product Operations Specialist (APM Track)",
        "Company / Startup": "InMobi Group",
        "Work Location": "Block Delta, Embassy TechVillage, Bellandur, Bengaluru",
        "Domain / Track": "AdTech & Consumer Product Platforms",
        "Experience Level": "0 - 2 Years (BBA / BCA / Graduate)",
        "Core Skills Required": "User Funnel Analysis, Product Telemetry, Bug Reporting, User Feedback Synthesis, SQL Basics",
        "Compensation Band": "Rs 6,00,000 - 9,00,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/product-jobs?source=homepage"
    },
    {
        "Platform": "Hirist.tech (Product)",
        "Requisition Title": "Product Support & User Experience Coordinator",
        "Company / Startup": "BrowserStack",
        "Work Location": "RMZ Infinity, Old Madras Road, Bennigana Halli, Bengaluru",
        "Domain / Track": "Cloud Developer Infrastructure",
        "Experience Level": "0 - 2 Years (BBA / Any Graduate)",
        "Core Skills Required": "Ticket Triage, Product Issue Escalation, Technical Customer Support, JIRA Service Desk",
        "Compensation Band": "Rs 5,50,000 - 8,50,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/product-jobs?source=homepage"
    },
    {
        "Platform": "Hirist.tech (Product)",
        "Requisition Title": "AI Product Data Operations Trainee",
        "Company / Startup": "Yellow.ai",
        "Work Location": "Prestige Technostar, Brookefield, Whitefield, Bengaluru",
        "Domain / Track": "Conversational AI & Agent Platform",
        "Experience Level": "Fresher to 1 Year (BBA / BCA)",
        "Core Skills Required": "Prompt Evaluation, Intent Classification, Chatbot Dialogue Auditing, Data Annotation",
        "Compensation Band": "Rs 4,50,000 - 6,80,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/product-jobs?source=homepage"
    },

    # --- HIRIST.TECH: E-COMMERCE JOBS TRACK ---
    {
        "Platform": "Hirist.tech (E-Commerce)",
        "Requisition Title": "Associate - Category Operations & Vendor Onboarding",
        "Company / Startup": "Meesho (Fashnear Technologies)",
        "Work Location": "06-105, Tower E, IBC Knowledge Park, Bannerghatta Road, Bengaluru",
        "Domain / Track": "Social Commerce & Marketplace Operations",
        "Experience Level": "0 - 2 Years (BBA / B.Com)",
        "Core Skills Required": "Vendor Governance, Price Benchmarking, Catalog Quality Auditing, Advanced Excel VLOOKUP",
        "Compensation Band": "Rs 5,20,000 - 7,80,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/ecommerce-jobs?source=catlist"
    },
    {
        "Platform": "Hirist.tech (E-Commerce)",
        "Requisition Title": "Supply Chain Dispatch & Warehouse Operations Analyst",
        "Company / Startup": "Shadowfax Technologies",
        "Work Location": "1st Main Road, Koramangala 1st Block, Bengaluru",
        "Domain / Track": "3PL Logistics & E-Commerce Fulfillment",
        "Experience Level": "0 - 2 Years (BBA Supply Chain / Any Grad)",
        "Core Skills Required": "Hub Logistics, First-Mile/Last-Mile SLA Tracking, Driver Fleet Allocation, MIS Reporting",
        "Compensation Band": "Rs 4,80,000 - 7,20,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/ecommerce-jobs?source=catlist"
    },
    {
        "Platform": "Hirist.tech (E-Commerce)",
        "Requisition Title": "E-Commerce Customer Experience & Escalations Executive",
        "Company / Startup": "Urban Company",
        "Work Location": "HSR Layout Sector 6, Bengaluru Hub",
        "Domain / Track": "On-Demand Home Services & D2C",
        "Experience Level": "0 - 1.5 Years (BBA / High Communication)",
        "Core Skills Required": "High-Touch Escalation Triage, Customer Refund Audit, Partner Dispute Resolution, Zendesk",
        "Compensation Band": "Rs 4,50,000 - 6,50,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/ecommerce-jobs?source=catlist"
    },

    # --- HIRIST.TECH: FINTECH & EDTECH JOBS TRACK ---
    {
        "Platform": "Hirist.tech (FinTech & EdTech)",
        "Requisition Title": "Risk Operations & KYC Verification Analyst",
        "Company / Startup": "CRED (Dreamplug Technologies)",
        "Work Location": "100ft Road, Indiranagar, Bengaluru",
        "Domain / Track": "Premium FinTech & Credit Infrastructure",
        "Experience Level": "0 - 2 Years (BBA / B.Com / Finance)",
        "Core Skills Required": "KYC Compliance, AML Transaction Monitoring, Credit Line Underwriting Verification, Excel",
        "Compensation Band": "Rs 6,50,000 - 9,50,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/fintech-edtech-jobs?source=catlist"
    },
    {
        "Platform": "Hirist.tech (FinTech & EdTech)",
        "Requisition Title": "Merchant Operations & Payment Gateway Trainee",
        "Company / Startup": "Juspay Technologies",
        "Work Location": "Koramangala 8th Block, Near Forum Mall, Bengaluru",
        "Domain / Track": "Payment Switch & HyperSDK Infrastructure",
        "Experience Level": "Fresher (2024-2026 BBA / Any Grad)",
        "Core Skills Required": "Payment Gateway Integration Support, Transaction Drop-Off Triage, SLA Monitoring",
        "Compensation Band": "Rs 5,00,000 - 7,50,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/fintech-edtech-jobs?source=catlist"
    },
    {
        "Platform": "Hirist.tech (FinTech & EdTech)",
        "Requisition Title": "Student Operations & Academic Program Coordinator",
        "Company / Startup": "Scaler Academy (InterviewBit)",
        "Work Location": "Salarpuria Sattva Knowledge Court, Doddanekkundi, Marathahalli, Bengaluru",
        "Domain / Track": "Higher EdTech & Upskilling",
        "Experience Level": "0 - 2 Years (BBA / High Empathy)",
        "Core Skills Required": "Student Success Operations, Batch Scheduling, Attendance Telemetry, Engagement Dashboards",
        "Compensation Band": "Rs 4,80,000 - 7,00,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/fintech-edtech-jobs?source=catlist"
    }
]

def generate_csv(out_path="e:/anti/instahyre_cutshort_hirist_jobs.csv"):
    fieldnames = [
        "Platform",
        "Requisition Title",
        "Company / Startup",
        "Work Location",
        "Domain / Track",
        "Experience Level",
        "Core Skills Required",
        "Compensation Band",
        "Direct Portal Route URL"
    ]
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in REQUISITIONS:
            writer.writerow(r)
    print(f"Generated {out_path} with {len(REQUISITIONS)} verified requisitions.")

if __name__ == "__main__":
    generate_csv()
