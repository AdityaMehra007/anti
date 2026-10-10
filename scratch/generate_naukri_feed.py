"""
Naukri Candidate Homepage & High-Velocity Bengaluru Requisition Matrix Generator
Generates:
1. e:/anti/naukri_homepage_bengaluru_feed.csv
   High-velocity, active corporate requisitions spanning Operations, AI Productivity, BBA/Business Management,
   FinTech, Healthcare Operations, and Supply Chain in Bengaluru.
"""

import csv
import os

REQUISITIONS = [
    {
        "Requisition Title": "Operations Analyst - Global Business Services",
        "Hiring Organization / Employer": "Target Corporation (Target in India)",
        "Work Location": "Manyata Tech Park, Nagavara, Outer Ring Road, Bengaluru",
        "Target Candidate Profile": "BBA / B.Com / Any Graduate (0-2 Yrs Experience)",
        "Core Skill Tags Required": "Business Operations, Excel / Advanced Formulas, Process Optimization, Jira, SLA Tracking",
        "Annual Compensation Band (INR)": "Rs 5,500,000 - 8,00,000 PA",
        "Corporate Pillar": "Global Capability Center (GCC) / Retail Operations",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/target-corporation-jobs-in-bangalore"
    },
    {
        "Requisition Title": "AI Prompt Operations & Data Evaluation Associate",
        "Hiring Organization / Employer": "Accenture Solutions Pvt Ltd",
        "Work Location": "Divyasree Technopolis, Yemlur / Bellandur, Bengaluru",
        "Target Candidate Profile": "BBA / BCA / Graduate (Fresher to 1 Yr) with High English Fluency",
        "Core Skill Tags Required": "AI Productivity, Prompt Optimization, LLM Evaluation, Content Moderation, Quality Auditing",
        "Annual Compensation Band (INR)": "Rs 4,20,000 - 6,50,000 PA",
        "Corporate Pillar": "Enterprise AI & Cognitive Operations",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/accenture-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Client Support Specialist - US Enterprise Accounts",
        "Hiring Organization / Employer": "Freshworks Inc.",
        "Work Location": "Indiranagar / EGL (Embassy GolfLinks), Bengaluru",
        "Target Candidate Profile": "BBA / Graduate (0-2 Yrs), Exceptional Written & Verbal Communication",
        "Core Skill Tags Required": "Freshdesk, Zendesk, Customer Success, Ticket Triage, SLA Adherence, Account Management",
        "Annual Compensation Band (INR)": "Rs 6,000,000 - 9,50,000 PA + Shift Allowance",
        "Corporate Pillar": "SaaS & Enterprise Customer Success",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/freshworks-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Business Operations Trainee - FinTech Merchant Settlement",
        "Hiring Organization / Employer": "Razorpay Software Pvt Ltd",
        "Work Location": "Koramangala 4th Block, 80 Feet Road, Bengaluru",
        "Target Candidate Profile": "BBA / BMS / B.Com (2024-2026 Batch, Fresher / 0-1 Yr)",
        "Core Skill Tags Required": "Merchant Operations, Reconciliation, Payment Gateway Systems, SQL Basics, MIS Reporting",
        "Annual Compensation Band (INR)": "Rs 5,00,000 - 7,20,000 PA",
        "Corporate Pillar": "FinTech & Payments Infrastructure",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/razorpay-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Global Logistics & Fulfillment Coordinator",
        "Hiring Organization / Employer": "Amazon Development Centre India",
        "Work Location": "World Trade Center, Brigade Gateway, Malleshwaram / Peenya, Bengaluru",
        "Target Candidate Profile": "BBA (Logistics/Supply Chain) / Any Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "Supply Chain Operations, Inventory Management, Vendor Coordination, Excel VLOOKUP/Pivot, TMS",
        "Annual Compensation Band (INR)": "Rs 4,80,000 - 7,50,000 PA",
        "Corporate Pillar": "E-Commerce & Supply Chain Logistics",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/amazon-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Healthcare Operations & Revenue Cycle Analyst",
        "Hiring Organization / Employer": "Optum (UnitedHealth Group)",
        "Work Location": "EcoWorld Tech Park, Sarjapur-Marathahalli ORR, Bengaluru",
        "Target Candidate Profile": "BBA / BHA / Life Sciences Graduate (Fresher to 2 Yrs)",
        "Core Skill Tags Required": "US Healthcare RCM, Medical Billing Operations, HIPAA Compliance, Claims Processing, Excel",
        "Annual Compensation Band (INR)": "Rs 4,50,000 - 6,80,000 PA",
        "Corporate Pillar": "Healthcare GCC & HealthTech",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/optum-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Inside Sales & Business Development Associate (Outbound)",
        "Hiring Organization / Employer": "Darwinbox Technologies",
        "Work Location": "HSR Layout Sector 1, Outer Ring Road, Bengaluru",
        "Target Candidate Profile": "BBA / Marketing Graduate (0-2 Yrs), High Energy Outbound Hunter",
        "Core Skill Tags Required": "Cold Outreach, Apollo.io, LinkedIn Sales Navigator, Lead Qualification, CRM Updating",
        "Annual Compensation Band (INR)": "Rs 5,50,000 - 8,50,000 PA + Uncapped Incentives",
        "Corporate Pillar": "Enterprise HRTech & B2B SaaS",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/darwinbox-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Executive Assistant & Founder Operations Specialist",
        "Hiring Organization / Employer": "Kalaari Capital / Portfolio Startups",
        "Work Location": "Lavelle Road / Vittal Mallya Road, Bengaluru",
        "Target Candidate Profile": "BBA / Mass Comm / Economics Graduate (1-3 Yrs), Discreet & Agile",
        "Core Skill Tags Required": "Executive Support, Notion, Google Workspace, Calendar Scheduling, Board Presentation MIS",
        "Annual Compensation Band (INR)": "Rs 7,00,000 - 11,00,000 PA",
        "Corporate Pillar": "Venture Capital & Founders Office",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/operations-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Procurement & Strategic Vendor Sourcing Analyst",
        "Hiring Organization / Employer": "Schneider Electric India",
        "Work Location": "Attibele Industrial Area / Electronic City Phase 2, Bengaluru",
        "Target Candidate Profile": "BBA / B.Com / Any Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "Procurement Operations, SAP Ariba, PO Processing, Vendor Negotiations, Cost Audit",
        "Annual Compensation Band (INR)": "Rs 5,00,000 - 7,80,000 PA",
        "Corporate Pillar": "Industrial Automation & Energy Systems",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/schneider-electric-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Product Operations Associate - Trust & Safety",
        "Hiring Organization / Employer": "Swiggy (Bundl Technologies)",
        "Work Location": "Devarabisanahalli, Embassy TechVillage, Bellandur, Bengaluru",
        "Target Candidate Profile": "BBA / Graduate (0-2 Yrs), Analytical & Process-Oriented",
        "Core Skill Tags Required": "Policy Enforcement, Fraud Detection Operations, Incident Investigation, SQL, Excel Dashboarding",
        "Annual Compensation Band (INR)": "Rs 5,20,000 - 8,00,000 PA",
        "Corporate Pillar": "Consumer Tech & Hyperlocal Logistics",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/swiggy-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Investment Banking Operations & Fund Accounting Analyst",
        "Hiring Organization / Employer": "State Street Corporate Services",
        "Work Location": "RMZ Ecospace, Bellandur, Outer Ring Road, Bengaluru",
        "Target Candidate Profile": "BBA (Finance) / B.Com / M.Com (0-2 Yrs)",
        "Core Skill Tags Required": "Fund Accounting, NAV Calculation, Trade Settlements, Corporate Actions, Bloomberg, Excel",
        "Annual Compensation Band (INR)": "Rs 5,00,000 - 7,50,000 PA",
        "Corporate Pillar": "Global Custody & Investment Management GCC",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/state-street-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Talent Operations & Recruitment Coordinator",
        "Hiring Organization / Employer": "Flipkart Internet Pvt Ltd",
        "Work Location": "Cessna Business Park, Kadubeesanahalli, Bengaluru",
        "Target Candidate Profile": "BBA (HR) / MBA Fresher / Any Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "ATS Management (Workday/Greenhouse), Interview Scheduling, Candidate Experience, Onboarding MIS",
        "Annual Compensation Band (INR)": "Rs 4,80,000 - 7,00,000 PA",
        "Corporate Pillar": "E-Commerce & Digital Commerce",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/flipkart-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Workflow Automation & No-Code Operations Executive",
        "Hiring Organization / Employer": "Mu Sigma Business Solutions",
        "Work Location": "Aviator Building, Ascendas ITPL, Whitefield, Bengaluru",
        "Target Candidate Profile": "BBA / BCA / B.Sc (0-2 Yrs) with Passion for Automation",
        "Core Skill Tags Required": "Zapier, Make, n8n, Google Sheets API, Workflow Automation, Data Wrangling",
        "Annual Compensation Band (INR)": "Rs 5,00,000 - 7,50,000 PA",
        "Corporate Pillar": "Decision Sciences & Analytics",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/mu-sigma-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Commercial Real Estate Lease Administration Associate",
        "Hiring Organization / Employer": "CBRE South Asia Pvt Ltd",
        "Work Location": "Prestige Trade Tower, Palace Road, High Grounds, Bengaluru",
        "Target Candidate Profile": "BBA / B.Com Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "Lease Administration, Contract Review, Commercial Property Operations, Billing Audit, MRI Software",
        "Annual Compensation Band (INR)": "Rs 4,80,000 - 7,20,000 PA",
        "Corporate Pillar": "Global Commercial Real Estate Services",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/cbre-jobs-in-bangalore"
    },
    {
        "Requisition Title": "Luxury Guest Experience & Front Office Operations Lead",
        "Hiring Organization / Employer": "The Ritz-Carlton / Marriott International",
        "Work Location": "Residency Road, Central Business District (CBD), Bengaluru",
        "Target Candidate Profile": "BBA (Hospitality / Tourism) / Hotel Management Graduate (0-2 Yrs)",
        "Core Skill Tags Required": "Front Office Operations, Opera PMS, High-Touch Guest Relations, VIP Concierge, Billing Reconciliation",
        "Annual Compensation Band (INR)": "Rs 4,50,000 - 6,50,000 PA + Service Charge",
        "Corporate Pillar": "Ultra-Luxury Hospitality & Lifestyle",
        "Direct Naukri Application & Search URL": "https://www.naukri.com/marriott-jobs-in-bangalore"
    }
]

def generate_csv(target_path="e:/anti/naukri_homepage_bengaluru_feed.csv"):
    fieldnames = [
        "Requisition Title",
        "Hiring Organization / Employer",
        "Work Location",
        "Target Candidate Profile",
        "Core Skill Tags Required",
        "Annual Compensation Band (INR)",
        "Corporate Pillar",
        "Direct Naukri Application & Search URL"
    ]
    with open(target_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in REQUISITIONS:
            writer.writerow(row)
    print(f"Successfully generated {target_path} with {len(REQUISITIONS)} records.")

if __name__ == "__main__":
    generate_csv()
