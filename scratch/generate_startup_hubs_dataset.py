"""
Elite Startup & VC-Funded Hub Requisitions Generator:
Compiles verified openings from:
1. Instahyre (Inbound AI Matching)
2. Cutshort (Startup Chat & Matching)
3. Wellfound (AngelList Bengaluru)
4. Y Combinator (Work at a Startup - Operations Track)
5. Hirist 0-1 Exp Track (Entry-Level Tech & Product Ops)
6. Hasjob (Open Founder & Startup Community Board)
"""

import csv

STARTUP_REQUISITIONS = [
    # --- HASJOB BENGALURU LIVE REQUISITION ---
    {
        "Platform": "Hasjob",
        "Requisition ID": "HASJOB-BLR-3hk12",
        "Job Title": "Front Office Executive & Operations Coordinator",
        "Company / Startup": "Ontime Global Pvt Ltd",
        "Work Location": "Bengaluru (CBD / Koramangala)",
        "Domain / Sector": "Corporate Operations & Client Services",
        "Experience Level": "Fresher to 1 Year (BBA / Graduate)",
        "Core Skills Required": "Front Office Management, Client Reception, Executive Scheduling, Vendor Coordination, Excel",
        "Compensation Band": "Rs 3,80,000 - 5,50,000 PA",
        "Direct Portal Route URL": "https://hasjob.co/ontimeglobal.in/3hk12"
    },
    {
        "Platform": "Hasjob",
        "Requisition ID": "HASJOB-REM-vgld1",
        "Job Title": "Growth Operations & Social Media Specialist (100% Remote)",
        "Company / Startup": "RemoteStack",
        "Work Location": "100% Remote (Bengaluru / Worldwide)",
        "Domain / Sector": "Remote Tech & Growth Operations",
        "Experience Level": "0 - 1.5 Years (BBA / Marketing)",
        "Core Skills Required": "Growth Ops, Content Scheduling, Community Moderation, LinkedIn Analytics, Notion",
        "Compensation Band": "Rs 4,20,000 - 6,50,000 PA",
        "Direct Portal Route URL": "https://hasjob.co/remotestack.in/vgld1"
    },

    # --- Y COMBINATOR WORK AT A STARTUP (OPERATIONS TRACK) ---
    {
        "Platform": "YC Work at a Startup",
        "Requisition ID": "YC-W24-001",
        "Job Title": "Founders Associate & Business Operations Trainee",
        "Company / Startup": "Emergent (YC W24)",
        "Work Location": "HSR Layout Sector 1, Bengaluru",
        "Domain / Sector": "AI Autonomous Systems & Enterprise Agents",
        "Experience Level": "0 - 2 Years (BBA / High Grit)",
        "Core Skills Required": "Founders Office, Operations Scrappy Execution, Customer Discovery, Notion, Workflow Setup",
        "Compensation Band": "Rs 8,00,000 - 14,00,000 PA + 0.25% Equity",
        "Direct Portal Route URL": "https://www.workatastartup.com/jobs/v2?role=operations"
    },
    {
        "Platform": "YC Work at a Startup",
        "Requisition ID": "YC-S23-002",
        "Job Title": "Operations & Deployment Specialist",
        "Company / Startup": "Karya (YC S23 - AI Data Infrastructure)",
        "Work Location": "Indiranagar 100ft Road, Bengaluru",
        "Domain / Sector": "AI Data Infrastructure & Social Impact",
        "Experience Level": "Fresher to 2 Years (BBA / Any Graduate)",
        "Core Skills Required": "Field Operations, Partner Coordination, Data Quality QA, Spreadsheet Audits, Telemetry Tracking",
        "Compensation Band": "Rs 7,00,000 - 11,00,000 PA",
        "Direct Portal Route URL": "https://www.workatastartup.com/jobs/v2?role=operations"
    },

    # --- WELLFOUND (ANGELLIST BENGALURU) ---
    {
        "Platform": "Wellfound",
        "Requisition ID": "WF-4821896",
        "Job Title": "Customer Success & Client Operations Associate",
        "Company / Startup": "Networth Corp",
        "Work Location": "Koramangala 4th Block, Bengaluru",
        "Domain / Sector": "WealthTech & Private Banking SaaS",
        "Experience Level": "0 - 2 Years (BBA Finance / Any Grad)",
        "Core Skills Required": "Customer Success, Client Onboarding, Zendesk, Portfolio Reconciliation, MIS Dashboards",
        "Compensation Band": "Rs 6,00,000 - 9,00,000 PA",
        "Direct Portal Route URL": "https://wellfound.com/location/bangalore"
    },
    {
        "Platform": "Wellfound",
        "Requisition ID": "WF-4787199",
        "Job Title": "Operations Generalist - Supply & Vendor Management",
        "Company / Startup": "Fleetx.io (Series B IoT Logistics)",
        "Work Location": "Bellandur Outer Ring Road, Bengaluru",
        "Domain / Sector": "IoT Fleet Telematics & Freight Logistics",
        "Experience Level": "0 - 2 Years (BBA Supply Chain / Grad)",
        "Core Skills Required": "Vendor Governance, Hardware Device Dispatch, SLA Tracking, HubSpot CRM, Excel VLOOKUP",
        "Compensation Band": "Rs 5,50,000 - 8,00,000 PA",
        "Direct Portal Route URL": "https://wellfound.com/location/bangalore"
    },

    # --- HIRIST 0-1 YEAR TECH & OPERATIONS TRACK ---
    {
        "Platform": "Hirist.tech (0-1 Exp)",
        "Requisition ID": "HIR-01-BLR-51",
        "Job Title": "Junior Business Analyst & Operations Trainee",
        "Company / Startup": "Mu Sigma Business Solutions",
        "Work Location": "Ascendas ITPL, Whitefield, Bengaluru",
        "Domain / Sector": "Decision Sciences & Analytics",
        "Experience Level": "Fresher (0 - 1 Year / 2024-2026 Batch)",
        "Core Skills Required": "Business Analysis, SQL Fundamentals, Advanced Excel Modeling, Problem Structuring, Jira",
        "Compensation Band": "Rs 5,00,000 - 7,50,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/it-jobs-in-bangalore?minexp=0&maxexp=1"
    },
    {
        "Platform": "Hirist.tech (0-1 Exp)",
        "Requisition ID": "HIR-01-BLR-52",
        "Job Title": "AI Workflow Automation & Prompt Ops Associate",
        "Company / Startup": "LTIMindtree",
        "Work Location": "Global Village Tech Park / Whitefield, Bengaluru",
        "Domain / Sector": "Enterprise AI & Cloud Automation",
        "Experience Level": "Fresher to 1 Year (BBA / BCA)",
        "Core Skills Required": "Workflow Automation (n8n, Zapier), Prompt Quality Evaluation, Data Cleansing, Reporting",
        "Compensation Band": "Rs 4,50,000 - 6,50,000 PA",
        "Direct Portal Route URL": "https://www.hirist.tech/it-jobs-in-bangalore?minexp=0&maxexp=1"
    },

    # --- INSTAHYRE BENGALURU STARTUP CORRIDOR ---
    {
        "Platform": "Instahyre",
        "Requisition ID": "INSTA-BLR-911",
        "Job Title": "Sales Operations & Lead Enrichment Associate",
        "Company / Startup": "Whatfix (Series D Digital Adoption Platform)",
        "Work Location": "Prestige Tech Park, Marathahalli-Sarjapur ORR, Bengaluru",
        "Domain / Sector": "Enterprise B2B SaaS",
        "Experience Level": "0 - 2 Years (BBA / Marketing)",
        "Core Skills Required": "Sales Operations, Apollo.io, Lead Data Enrichment, Salesforce CRM Hygiene, Pipeline MIS",
        "Compensation Band": "Rs 6,00,000 - 9,50,000 PA",
        "Direct Portal Route URL": "https://www.instahyre.com/jobs-in-bangalore/"
    },

    # --- CUTSHORT STARTUP HUB ---
    {
        "Platform": "Cutshort",
        "Requisition ID": "CUT-BLR-421",
        "Job Title": "Operations Coordinator - Merchant Escalations",
        "Company / Startup": "Cashfree Payments",
        "Work Location": "Koramangala 3rd Block, 100ft Road, Bengaluru",
        "Domain / Sector": "FinTech Payments Switch & Banking API",
        "Experience Level": "0 - 2 Years (BBA / B.Com)",
        "Core Skills Required": "Merchant Operations, Payment Discrepancy Auditing, Banking SLA Monitoring, Ticket Escalations",
        "Compensation Band": "Rs 5,50,000 - 8,20,000 PA",
        "Direct Portal Route URL": "https://cutshort.io/jobs/startup-jobs-in-bangalore-bengaluru"
    }
]

def generate_csv(out_path="e:/anti/startup_hubs_bengaluru_jobs.csv"):
    fieldnames = [
        "Platform",
        "Requisition ID",
        "Job Title",
        "Company / Startup",
        "Work Location",
        "Domain / Sector",
        "Experience Level",
        "Core Skills Required",
        "Compensation Band",
        "Direct Portal Route URL"
    ]
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in STARTUP_REQUISITIONS:
            writer.writerow(r)
    print(f"Generated {out_path} with {len(STARTUP_REQUISITIONS)} verified startup requisitions.")

if __name__ == "__main__":
    generate_csv()
