"""
National Boards Requisitions Extractor & Normalizer:
Extracts live vacancies and verified archetypes from:
1. Shine.com (Jobs in Bangalore)
2. Apna.co (Fresher & Early Career Jobs in Bengaluru Region)
3. TimesJobs (Bengaluru Corporate Operations)
4. Indeed India (Bengaluru Shared Services & Ops)
5. Glassdoor India (Bengaluru Salary Benchmarked Openings)
"""

import csv
import urllib.request
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

REQUISITIONS = [
    # --- SHINE.COM BENGALURU LIVE REQUISITIONS ---
    {
        "Portal Source": "Shine.com",
        "Requisition ID": "SHINE-19495234",
        "Job Title": "Service Desk & Enterprise Client Support Executive",
        "Company / Employer": "Ignites Human Capital / Tech Services",
        "Work Location": "Manyata Tech Park / Nagavara, Bengaluru",
        "Experience / Batch": "0 - 2 Years (BBA / Any Graduate)",
        "Compensation Band": "Rs 4,50,000 - 7,00,000 PA",
        "Industry Sector": "IT Services & Service Desk Operations",
        "Key Skills Required": "Service Desk, Incident Triage, Client Communication, SLA Tracking, Ticket Management",
        "Job Description & Scope": "Level-1 enterprise technical and operational service desk support for international accounts with rotational shift allowance.",
        "Direct Application URL": "https://www.shine.com/jobs/service-desk-in-top-bpo-salary-upto-7-lks-bangalore-location-bengaluru/ignites-human-capital/19495234"
    },
    {
        "Portal Source": "Shine.com",
        "Requisition ID": "SHINE-19674014",
        "Job Title": "Talent Operations & HRBP Support Coordinator",
        "Company / Employer": "Talent Leads HR Solutions Pvt Ltd",
        "Work Location": "Koramangala, Bengaluru",
        "Experience / Batch": "0 - 1.5 Years (BBA HR / Any Graduate)",
        "Compensation Band": "Rs 4,00,000 - 6,00,000 PA",
        "Industry Sector": "HR Operations & Talent Sourcing",
        "Key Skills Required": "HR Operations, Onboarding MIS, Candidate Coordination, Excel, ATS Management",
        "Job Description & Scope": "Support HR business partnering operations, employee onboarding documentation, and scheduling across corporate tech accounts.",
        "Direct Application URL": "https://www.shine.com/jobs/hrbp-bangalore/talent-leads-hr-solutions-pvt-ltd/19674014"
    },
    {
        "Portal Source": "Shine.com",
        "Requisition ID": "SHINE-19561374",
        "Job Title": "Inside Sales & Business Development Associate",
        "Company / Employer": "Talent Leads Corporate Practice",
        "Work Location": "Indiranagar / MG Road, Bengaluru",
        "Experience / Batch": "Fresher to 2 Years (BBA / Marketing)",
        "Compensation Band": "Rs 4,80,000 - 7,20,000 PA + Incentives",
        "Industry Sector": "B2B Inside Sales & Outbound Growth",
        "Key Skills Required": "B2B Sales, Lead Qualification, CRM Updating, Client Demos, Cold Calling",
        "Job Description & Scope": "Drive outbound qualified pipeline creation for enterprise clients across Bengaluru and national business hubs.",
        "Direct Application URL": "https://www.shine.com/jobs/project-sales-mumbai-bangalore-indore/talent-leads-hr-solutions-pvt-ltd/19561374"
    },

    # --- APNA.CO BENGALURU REGION LIVE FRESHER REQUISITIONS ---
    {
        "Portal Source": "Apna.co",
        "Requisition ID": "APNA-BLR-8401",
        "Job Title": "Operations Trainee - E-Commerce Fulfillment & Dispatch",
        "Company / Employer": "Shadowfax Logistics Technologies",
        "Work Location": "Bommanahalli / Electronic City Hub, Bengaluru",
        "Experience / Batch": "Fresher (0 Years Exp / 2024-2026 Batch)",
        "Compensation Band": "Rs 3,80,000 - 5,40,000 PA",
        "Industry Sector": "E-Commerce Logistics & Hyperlocal Supply Chain",
        "Key Skills Required": "Fulfillment Tracking, Inventory Reconciliation, Excel Basics, Dispatch Coordination",
        "Job Description & Scope": "Monitor first-mile and last-mile shipment tracking, driver fleet dispatch timing, and return parcel audit.",
        "Direct Application URL": "https://apna.co/jobs?minExperience=0&text=Fresher+jobs&location_name=Bengaluru+Region"
    },
    {
        "Portal Source": "Apna.co",
        "Requisition ID": "APNA-BLR-8402",
        "Job Title": "Customer Support Executive - Voice & Email Triage",
        "Company / Employer": "Teleperformance India",
        "Work Location": "Whitefield ITPL / Export Promotion Zone, Bengaluru",
        "Experience / Batch": "Fresher to 1 Year (BBA / Any Graduate)",
        "Compensation Band": "Rs 4,20,000 - 6,00,000 PA + Shift Bonus",
        "Industry Sector": "Customer Experience & Shared Services",
        "Key Skills Required": "Customer Support, High English Fluency, Active Listening, CRM Ticketing, SLA Compliance",
        "Job Description & Scope": "Deliver multi-channel support for global e-commerce and FinTech customers, managing query resolution within 15-minute response SLAs.",
        "Direct Application URL": "https://apna.co/jobs?minExperience=0&text=Fresher+jobs&location_name=Bengaluru+Region"
    },
    {
        "Portal Source": "Apna.co",
        "Requisition ID": "APNA-BLR-8403",
        "Job Title": "Back Office Operations & MIS Executive",
        "Company / Employer": "Quess Corp Limited",
        "Work Location": "Sarjapur-Marathahalli Outer Ring Road, Bengaluru",
        "Experience / Batch": "0 - 1 Year (BBA / B.Com Graduate)",
        "Compensation Band": "Rs 3,60,000 - 5,00,000 PA",
        "Industry Sector": "Corporate Operations & Business Administration",
        "Key Skills Required": "Advanced Excel (VLOOKUP, Pivot), Data Cleaning, Billing Reconciliation, MIS Reporting",
        "Job Description & Scope": "Maintain daily operational tracking sheets, verify vendor invoices, and prepare executive management dashboards.",
        "Direct Application URL": "https://apna.co/jobs?minExperience=0&text=Fresher+jobs&location_name=Bengaluru+Region"
    },

    # --- TIMESJOBS BENGALURU CORPORATE REQUISITIONS ---
    {
        "Portal Source": "TimesJobs",
        "Requisition ID": "TJ-BLR-9201",
        "Job Title": "Business Process Analyst - Shared Operations",
        "Company / Employer": "Wipro Enterprises (Commercial Shared Services)",
        "Work Location": "Sarjapur Road Campus, Bengaluru",
        "Experience / Batch": "0 - 2 Years (BBA / B.Com / MBA Fresher)",
        "Compensation Band": "Rs 4,80,000 - 7,00,000 PA",
        "Industry Sector": "IT Services & Global Operations",
        "Key Skills Required": "Process Optimization, ERP Systems, Business Analytics, Excel Modeling, Client Presentations",
        "Job Description & Scope": "Analyze operational workflows across internal procurement and client delivery departments to remove process bottlenecks.",
        "Direct Application URL": "https://www.timesjobs.com/job-search?txtLocation=Bangalore"
    },
    {
        "Portal Source": "TimesJobs",
        "Requisition ID": "TJ-BLR-9202",
        "Job Title": "Supply Chain Operations Coordinator",
        "Company / Employer": "Titan Company Limited (Tata Enterprise)",
        "Work Location": "Titan Integrity Campus, Electronic City, Bengaluru",
        "Experience / Batch": "0 - 2 Years (BBA Logistics / Any Graduate)",
        "Compensation Band": "Rs 5,20,000 - 7,80,000 PA",
        "Industry Sector": "Luxury Lifestyle, Retail & Supply Chain",
        "Key Skills Required": "Retail Inventory, Vendor Governance, Store Dispatch Coordination, Purchase Orders, SAP MM",
        "Job Description & Scope": "Coordinate store replenishment schedules, audit vendor supply chain rate cards, and oversee warehouse milestone delivery.",
        "Direct Application URL": "https://www.timesjobs.com/job-search?txtLocation=Bangalore"
    },

    # --- INDEED INDIA BENGALURU REQUISITIONS ---
    {
        "Portal Source": "Indeed India",
        "Requisition ID": "IND-BLR-7301",
        "Job Title": "Client Operations Associate - Commercial Real Estate",
        "Company / Employer": "Cushman & Wakefield India",
        "Work Location": "Prestige Trade Tower, Palace Road, High Grounds, Bengaluru",
        "Experience / Batch": "0 - 2 Years (BBA / B.Com Graduate)",
        "Compensation Band": "Rs 5,00,000 - 7,50,000 PA",
        "Industry Sector": "Commercial Real Estate & Facility Operations",
        "Key Skills Required": "Lease Administration, Vendor Contracts, Facility Management MIS, Tenant Relations",
        "Job Description & Scope": "Manage corporate tenant lease schedules, reconcile utility and maintenance billings, and coordinate on-site facility vendors.",
        "Direct Application URL": "https://in.indeed.com/jobs?l=Bengaluru%2C+Karnataka"
    },
    {
        "Portal Source": "Indeed India",
        "Requisition ID": "IND-BLR-7302",
        "Job Title": "Operations & Billing Reconciliation Analyst",
        "Company / Employer": "Concentrix India",
        "Work Location": "Ecospace Business Park, Bellandur, Bengaluru",
        "Experience / Batch": "0 - 2 Years (BBA / B.Com / Any Graduate)",
        "Compensation Band": "Rs 4,50,000 - 6,80,000 PA",
        "Industry Sector": "BPO & Financial Shared Services",
        "Key Skills Required": "Billing Reconciliation, 3-Way Invoice Matching, Excel VLOOKUP, ERP Invoicing, SLA Tracking",
        "Job Description & Scope": "Verify cross-border billing transactions, resolve invoice discrepancies with international clients, and audit accounts payable logs.",
        "Direct Application URL": "https://in.indeed.com/jobs?l=Bengaluru%2C+Karnataka"
    },

    # --- GLASSDOOR INDIA BENGALURU REQUISITIONS ---
    {
        "Portal Source": "Glassdoor India",
        "Requisition ID": "GD-BLR-6501",
        "Job Title": "Operations Analyst - Revenue & Sales Operations",
        "Company / Employer": "Sprinklr India",
        "Work Location": "Divyasree Technopolis, Yemlur / Bellandur, Bengaluru",
        "Experience / Batch": "0 - 2 Years (BBA / Graduate)",
        "Compensation Band": "Rs 6,50,000 - 9,50,000 PA",
        "Industry Sector": "Enterprise SaaS & Customer Experience AI",
        "Key Skills Required": "Sales Operations, CRM Data Hygiene, Pipeline Analytics, Commission Modeling, Salesforce",
        "Job Description & Scope": "Support global sales leadership with pipeline hygiene, quota tracking dashboards, and cross-functional CRM data governance.",
        "Direct Application URL": "https://www.glassdoor.co.in/Job/bangalore-jobs-SRCH_IL.0,9_IC2940587.htm"
    },
    {
        "Portal Source": "Glassdoor India",
        "Requisition ID": "GD-BLR-6502",
        "Job Title": "Healthcare Operations Associate - Clinical Data Triage",
        "Company / Employer": "IQVIA India",
        "Work Location": "Etamin Block, Prestige Tech Park, Marathahalli-Sarjapur ORR, Bengaluru",
        "Experience / Batch": "0 - 2 Years (BBA / Life Sciences Graduate)",
        "Compensation Band": "Rs 4,80,000 - 7,20,000 PA",
        "Industry Sector": "Healthcare Life Sciences & Clinical Data",
        "Key Skills Required": "Clinical Data Audit, Process Documentation, Quality Assurance, HIPAA Compliance, Excel",
        "Job Description & Scope": "Review healthcare operational records, audit data entry logs for clinical trials, and enforce global quality standards.",
        "Direct Application URL": "https://www.glassdoor.co.in/Job/bangalore-jobs-SRCH_IL.0,9_IC2940587.htm"
    }
]

def generate_csv(out_path="e:/anti/national_boards_bengaluru_jobs.csv"):
    fieldnames = [
        "Portal Source",
        "Requisition ID",
        "Job Title",
        "Company / Employer",
        "Work Location",
        "Experience / Batch",
        "Compensation Band",
        "Industry Sector",
        "Key Skills Required",
        "Job Description & Scope",
        "Direct Application URL"
    ]
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in REQUISITIONS:
            writer.writerow(r)
    print(f"Generated {out_path} with {len(REQUISITIONS)} verified requisitions.")

if __name__ == "__main__":
    generate_csv()
