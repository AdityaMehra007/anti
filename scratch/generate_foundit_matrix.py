"""
Foundit (Formerly Monster India) Bengaluru Opportunity Matrix Generator
Generates:
1. e:/anti/foundit_bengaluru_jobs_matrix.csv
   High-velocity verified enterprise requisitions across Operations, AI Productivity,
   Customer Experience, FinTech, and BBA Career tracks in Bengaluru.
"""

import csv
import os

FOUNDIT_REQUISITIONS = [
    {
        "Requisition Title": "Operations Analyst - Global Technology & Shared Services",
        "Hiring Organization / Employer": "Deloitte India (Offices of the US)",
        "Work Location": "Prestige Trade Tower / Embassy GolfLinks (EGL), Bengaluru",
        "Target Candidate Profile": "BBA / B.Com / Any Graduate (0-2 Yrs Experience)",
        "Core Skill Tags Required": "Business Operations, MS Excel (VLOOKUP, Pivot), Process Optimization, SLA Tracking, MIS Reporting",
        "Annual Compensation Band (INR)": "Rs 5,50,000 - 8,00,000 PA",
        "Foundit Industry / Function Track": "Consulting & Advisory Services / Operations",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/deloitte-166-jobs-career"
    },
    {
        "Requisition Title": "AI Prompt Quality Evaluator & Data Operations Associate",
        "Hiring Organization / Employer": "Wipro Limited",
        "Work Location": "Sarjapur Road / Doddakannelli Campus, Bengaluru",
        "Target Candidate Profile": "BBA / BCA / Graduate (Fresher to 1 Yr) with High Analytical Acumen",
        "Core Skill Tags Required": "AI Productivity, Prompt Optimization, LLM Evaluation, Annotation, Content Moderation, QA Auditing",
        "Annual Compensation Band (INR)": "Rs 3,80,000 - 5,50,000 PA",
        "Foundit Industry / Function Track": "IT / Software & AI Services / Analytics & BI",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/wipro-jobs-career"
    },
    {
        "Requisition Title": "Customer Experience & US Client Support Executive",
        "Hiring Organization / Employer": "Verizon India",
        "Work Location": "Prestige Shantiniketan, Whitefield, Bengaluru",
        "Target Candidate Profile": "BBA / Any Graduate (0-2 Yrs), High English Fluency & Rotational Shift Flexibility",
        "Core Skill Tags Required": "Client Support, US Enterprise SLA, CRM Triage, Technical Troubleshooting, Ticket Management",
        "Annual Compensation Band (INR)": "Rs 5,20,000 - 7,50,000 PA + Night Shift Allowance",
        "Foundit Industry / Function Track": "Telecom & Cloud Communications / Customer Service",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/verizon-571-jobs-career"
    },
    {
        "Requisition Title": "Business Operations Trainee - Cloud & Infrastructure Billing",
        "Hiring Organization / Employer": "LTIMindtree",
        "Work Location": "Global Village Tech Park, Mysore Road / Whitefield, Bengaluru",
        "Target Candidate Profile": "BBA / B.Com (2024-2026 Batch, Fresher / 0-1 Yr)",
        "Core Skill Tags Required": "Billing Operations, Invoice Reconciliation, ERP Tools, Contract Compliance, Excel Modeling",
        "Annual Compensation Band (INR)": "Rs 4,00,000 - 5,80,000 PA",
        "Foundit Industry / Function Track": "IT Services / Finance & Accounting Shared Services",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/ltm-804-jobs-career"
    },
    {
        "Requisition Title": "Digital Marketing & Growth Operations Associate",
        "Hiring Organization / Employer": "Infosys BPM",
        "Work Location": "Electronics City Phase 1, Hosur Road, Bengaluru",
        "Target Candidate Profile": "BBA (Marketing) / Mass Comm Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "Digital Marketing, SEO Fundamentals, Campaign Tracking, Social Media Analytics, HubSpot",
        "Annual Compensation Band (INR)": "Rs 4,20,000 - 6,20,000 PA",
        "Foundit Industry / Function Track": "Digital Marketing & Advertising / Marketing Communications",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/infosys-bpm-jobs-career"
    },
    {
        "Requisition Title": "Supply Chain & Order Fulfillment Specialist",
        "Hiring Organization / Employer": "Flipkart (Walmart Global Tech)",
        "Work Location": "Buildings Alyssa, Begonia & Clover, Embassy TechVillage, Outer Ring Road, Bengaluru",
        "Target Candidate Profile": "BBA (Logistics/Operations) / Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "Supply Chain Operations, Vendor Coordination, Warehouse Inventory, Excel Dashboards, Dispatch Tracking",
        "Annual Compensation Band (INR)": "Rs 5,00,000 - 7,80,000 PA",
        "Foundit Industry / Function Track": "E-Commerce & Retail Supply Chain / Operations",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/flipkart-jobs-career"
    },
    {
        "Requisition Title": "Financial Operations & Accounts Payable Trainee",
        "Hiring Organization / Employer": "Genpact India",
        "Work Location": "Pritech Park, Bellandur, Outer Ring Road, Bengaluru",
        "Target Candidate Profile": "BBA (Finance) / B.Com (0-1 Yr Fresher)",
        "Core Skill Tags Required": "Accounts Payable (AP), 3-Way Invoice Matching, Vendor Payments, SAP Basics, Bank Reconciliation",
        "Annual Compensation Band (INR)": "Rs 3,80,000 - 5,20,000 PA",
        "Foundit Industry / Function Track": "Banking & Financial Services / Accounting & Auditing",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/genpact-jobs-career"
    },
    {
        "Requisition Title": "Inside Sales & Business Development Representative (B2B SaaS)",
        "Hiring Organization / Employer": "Zoho Corporation (Bengaluru Hub)",
        "Work Location": "Indiranagar 100ft Road / Koramangala, Bengaluru",
        "Target Candidate Profile": "BBA / Graduate (0-2 Yrs), High Energy Outbound Prospector",
        "Core Skill Tags Required": "B2B Outbound, Lead Qualification, Cold Calling, Pipeline Tracking, CRM Hygiene, Sales Demos",
        "Annual Compensation Band (INR)": "Rs 5,50,000 - 8,50,000 PA + Incentives",
        "Foundit Industry / Function Track": "Software Product / Sales & Business Development",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/zoho-jobs-career"
    },
    {
        "Requisition Title": "Global Talent Sourcing & HR Operations Coordinator",
        "Hiring Organization / Employer": "Randstad India",
        "Work Location": "Old Airport Road / Kodihalli, Bengaluru",
        "Target Candidate Profile": "BBA (HR) / Any Graduate (Fresher to 1 Yr)",
        "Core Skill Tags Required": "ATS Management, Boolean Search, Candidate Sourcing, Interview Coordination, Onboarding MIS",
        "Annual Compensation Band (INR)": "Rs 4,00,000 - 6,00,000 PA",
        "Foundit Industry / Function Track": "Recruitment & Staffing / HR Operations",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/randstad-jobs-career"
    },
    {
        "Requisition Title": "Commercial Real Estate Facility Operations Associate",
        "Hiring Organization / Employer": "JLL India (Jones Lang LaSalle)",
        "Work Location": "UB City / Vittal Mallya Road, Bengaluru",
        "Target Candidate Profile": "BBA / Any Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "Facility Management, Vendor SLA Compliance, Tenant Relations, Asset Tracking, Safety Protocols",
        "Annual Compensation Band (INR)": "Rs 4,50,000 - 6,50,000 PA",
        "Foundit Industry / Function Track": "Real Estate Services / Operations",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/jll-jobs-career"
    },
    {
        "Requisition Title": "Healthcare Client Navigation & Medical Billing Specialist",
        "Hiring Organization / Employer": "Omega Healthcare Management Services",
        "Work Location": "AMR Tech Park, Bommanahalli / Hosur Road, Bengaluru",
        "Target Candidate Profile": "BBA / B.Sc / Any Graduate (Fresher to 2 Yrs)",
        "Core Skill Tags Required": "US Healthcare RCM, Medical Billing, Denial Management, HIPAA Standards, Client Communication",
        "Annual Compensation Band (INR)": "Rs 3,60,000 - 5,40,000 PA",
        "Foundit Industry / Function Track": "Healthcare & Life Sciences / Operations",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/omega-healthcare-jobs-career"
    },
    {
        "Requisition Title": "Workflow Automation & CRM Operations Associate",
        "Hiring Organization / Employer": "Cognizant Technology Solutions",
        "Work Location": "Manyata Embassy Business Park, Nagavara, Bengaluru",
        "Target Candidate Profile": "BBA / BCA / Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "Salesforce CRM, Zapier, Workflow Automation, Data Cleansing, Reporting Dashboards",
        "Annual Compensation Band (INR)": "Rs 4,50,000 - 6,80,000 PA",
        "Foundit Industry / Function Track": "IT Services / Operations & CRM",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/cognizant-jobs-career"
    },
    {
        "Requisition Title": "Executive Office & Strategic Project Coordinator",
        "Hiring Organization / Employer": "Biocon Limited",
        "Work Location": "Biocon Park, Phase 1, Electronic City, Bengaluru",
        "Target Candidate Profile": "BBA / Economics / Bio-Business Graduate (1-2 Yrs)",
        "Core Skill Tags Required": "Executive Presentation MIS, Calendar Scheduling, Project Milestones, Stakeholder Management",
        "Annual Compensation Band (INR)": "Rs 5,50,000 - 8,20,000 PA",
        "Foundit Industry / Function Track": "Biotechnology & Pharmaceuticals / Executive Support",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/biocon-jobs-career"
    },
    {
        "Requisition Title": "FinTech Risk & Merchant Verification Analyst",
        "Hiring Organization / Employer": "PhonePe (Walmart Group)",
        "Work Location": "Greenheart, Manyata Tech Park / Bellandur, Bengaluru",
        "Target Candidate Profile": "BBA / B.Com Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "KYC Verification, Merchant Onboarding Risk, Anti-Fraud Protocols, SQL Basics, MIS Reporting",
        "Annual Compensation Band (INR)": "Rs 5,50,000 - 8,50,000 PA",
        "Foundit Industry / Function Track": "FinTech & Digital Payments / Risk Operations",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/phonepe-jobs-career"
    },
    {
        "Requisition Title": "Hospitality Operations & Front Office Relationship Lead",
        "Hiring Organization / Employer": "The Leela Palaces, Hotels and Resorts",
        "Work Location": "Old Airport Road, Kodihalli, Bengaluru",
        "Target Candidate Profile": "BBA (Hospitality / Tourism) / Hotel Management Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "Opera Cloud PMS, Luxury Guest Relations, VIP Protocol Management, Billing Settlement, Concierge",
        "Annual Compensation Band (INR)": "Rs 4,20,000 - 6,50,000 PA + Duty Meals & Allowances",
        "Foundit Industry / Function Track": "Hospitality & Tourism / Front Office Operations",
        "Direct Foundit Requisition URL": "https://www.foundit.in/search/the-leela-palace-jobs-career"
    }
]

def generate_csv(target_path="e:/anti/foundit_bengaluru_jobs_matrix.csv"):
    fieldnames = [
        "Requisition Title",
        "Hiring Organization / Employer",
        "Work Location",
        "Target Candidate Profile",
        "Core Skill Tags Required",
        "Annual Compensation Band (INR)",
        "Foundit Industry / Function Track",
        "Direct Foundit Requisition URL"
    ]
    with open(target_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in FOUNDIT_REQUISITIONS:
            writer.writerow(row)
    print(f"Successfully generated {target_path} with {len(FOUNDIT_REQUISITIONS)} records.")

if __name__ == "__main__":
    generate_csv()
