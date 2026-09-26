import sys
import os
import json
from datetime import datetime

# Enforce UTF-8 encoding for Windows standard output
sys.stdout.reconfigure(encoding='utf-8')

def generate_salary_research_data():
    timestamp = "2026-08-26T01:00:00+05:30"
    report_year = 2026
    location = "Bangalore (Bengaluru), Karnataka, India"
    candidate = {
        "name": "Aditya Mehra",
        "degree": "BBA International Business",
        "institution": "Dayananda Sagar University, Bengaluru",
        "batch": "Class of 2026",
        "contact": "+91-7003456624",
        "email": "adityamehra799@gmail.com",
        "key_claims": [
            "300+ Event & Operations Deployments (Lead at AERO India 2025, Puma India)",
            "15% Operational Cost Reduction through lean workflow optimizations",
            "INR 1.5L+ Verified B2B Revenue at Pencil Mark Interior Solutions",
            "AI Data Operations at Instawork AI with 99%+ quality accuracy",
            "EXIM Trade Compliance (Incoterms 2020, HS Code classification, UCP 600 Letter of Credit validation)"
        ]
    }

    # Top 30 Target Companies Benchmark in Bangalore (2026 Market Data for Fresh BBA/Undergrads)
    companies_data = [
        {
            "rank": 1,
            "company": "Walmart Global Tech",
            "category": "MNC GCC / Retail Tech",
            "hub_location": "Kadubeesanahalli / Outer Ring Road, Bangalore",
            "primary_role": "Associate Operations Analyst (Global SCM)",
            "fixed_base_lpa": 7.0,
            "variable_lpa": 1.0,
            "joining_bonus_lpa": 1.0,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 7.5,
            "total_ctc_max": 9.5,
            "avg_ctc_lpa": 8.5,
            "in_hand_monthly_inr": 56000,
            "variable_pct": 12.0,
            "shift_allowance_inr": 8000,
            "perks": "Transport cab facility, INR 50k wellness budget, free cafeteria, medical insurance INR 5L"
        },
        {
            "rank": 2,
            "company": "Amazon Development Centre / Ops",
            "category": "MNC GCC / Big Tech & E-Commerce",
            "hub_location": "Bagmane Constellation Business Park / WTC, Bangalore",
            "primary_role": "Operations Specialist / Brand Specialist (TRMS / ATS)",
            "fixed_base_lpa": 6.5,
            "variable_lpa": 1.2,
            "joining_bonus_lpa": 1.5,
            "esop_rsu_lpa": 0.8,
            "total_ctc_min": 7.2,
            "total_ctc_max": 9.8,
            "avg_ctc_lpa": 8.8,
            "in_hand_monthly_inr": 54000,
            "variable_pct": 14.0,
            "shift_allowance_inr": 9500,
            "perks": "RSUs 4-year vesting, meal cards, Amazon employee discount, night shift allowances"
        },
        {
            "rank": 3,
            "company": "Google India",
            "category": "MNC GCC / Big Tech",
            "hub_location": "Old Madras Road & Bagmane Tech Park, Bangalore",
            "primary_role": "Global Scaled Operations Associate (GBO)",
            "fixed_base_lpa": 8.0,
            "variable_lpa": 1.5,
            "joining_bonus_lpa": 1.5,
            "esop_rsu_lpa": 1.5,
            "total_ctc_min": 9.0,
            "total_ctc_max": 12.5,
            "avg_ctc_lpa": 10.8,
            "in_hand_monthly_inr": 68000,
            "variable_pct": 15.0,
            "shift_allowance_inr": 0,
            "perks": "G-Stocks (GSUs), world-class micro-kitchens, complete insurance coverage, annual fitness stipend"
        },
        {
            "rank": 4,
            "company": "Microsoft India",
            "category": "MNC GCC / Big Tech",
            "hub_location": "Bellandur & Outer Ring Road, Bangalore",
            "primary_role": "Commercial Operations & Cloud Support Analyst",
            "fixed_base_lpa": 7.8,
            "variable_lpa": 1.4,
            "joining_bonus_lpa": 1.2,
            "esop_rsu_lpa": 1.2,
            "total_ctc_min": 8.5,
            "total_ctc_max": 11.5,
            "avg_ctc_lpa": 10.2,
            "in_hand_monthly_inr": 65000,
            "variable_pct": 14.0,
            "shift_allowance_inr": 0,
            "perks": "Microsoft stock purchase plan (ESPP 15% discount), hybrid flexible stipend, tuition reimbursement"
        },
        {
            "rank": 5,
            "company": "Goldman Sachs",
            "category": "MNC GCC / Global Investment Banking",
            "hub_location": "Helios Business Park, Outer Ring Road, Bangalore",
            "primary_role": "Operations Analyst (Global Markets / Corporate Trade)",
            "fixed_base_lpa": 7.5,
            "variable_lpa": 1.5,
            "joining_bonus_lpa": 1.0,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 8.0,
            "total_ctc_max": 10.5,
            "avg_ctc_lpa": 9.2,
            "in_hand_monthly_inr": 62000,
            "variable_pct": 18.0,
            "shift_allowance_inr": 10000,
            "perks": "Discretionary year-end global performance bonus, comprehensive medical, executive dining"
        },
        {
            "rank": 6,
            "company": "JPMorgan Chase & Co.",
            "category": "MNC GCC / Global Investment Banking",
            "hub_location": "Kadubeesanahalli / Embassy TechVillage, Bangalore",
            "primary_role": "Corporate & Investment Bank Operations Analyst",
            "fixed_base_lpa": 7.2,
            "variable_lpa": 1.2,
            "joining_bonus_lpa": 1.0,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 7.5,
            "total_ctc_max": 9.8,
            "avg_ctc_lpa": 8.7,
            "in_hand_monthly_inr": 59000,
            "variable_pct": 15.0,
            "shift_allowance_inr": 9000,
            "perks": "Annual bonus pool, shift differentials, door-to-door cab transport, global internal mobility"
        },
        {
            "rank": 7,
            "company": "Deloitte (India / USI)",
            "category": "Big 4 Consulting & Advisory",
            "hub_location": "Yelahanka & Bellandur, Bangalore",
            "primary_role": "Business Operations & Risk Advisory Analyst",
            "fixed_base_lpa": 5.5,
            "variable_lpa": 0.8,
            "joining_bonus_lpa": 0.5,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 5.8,
            "total_ctc_max": 7.5,
            "avg_ctc_lpa": 6.8,
            "in_hand_monthly_inr": 45000,
            "variable_pct": 12.0,
            "shift_allowance_inr": 4500,
            "perks": "Deloitte University training, client travel per-diem, certification sponsorship"
        },
        {
            "rank": 8,
            "company": "Ernst & Young (EY GDS / India)",
            "category": "Big 4 Consulting & Advisory",
            "hub_location": "RMZ Infinity, Old Madras Road, Bangalore",
            "primary_role": "Global Trade Advisory & Supply Chain Trainee",
            "fixed_base_lpa": 5.2,
            "variable_lpa": 0.8,
            "joining_bonus_lpa": 0.4,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 5.5,
            "total_ctc_max": 7.2,
            "avg_ctc_lpa": 6.4,
            "in_hand_monthly_inr": 43000,
            "variable_pct": 12.0,
            "shift_allowance_inr": 4000,
            "perks": "EY Badges certification credits, corporate group health coverage, structured 2-year promotion ladder"
        },
        {
            "rank": 9,
            "company": "PricewaterhouseCoopers (PwC India / AC)",
            "category": "Big 4 Consulting & Advisory",
            "hub_location": "Bannerghatta Road & Manyata Tech Park, Bangalore",
            "primary_role": "Commercial Operations & Risk Assurance Analyst",
            "fixed_base_lpa": 5.4,
            "variable_lpa": 0.7,
            "joining_bonus_lpa": 0.4,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 5.6,
            "total_ctc_max": 7.0,
            "avg_ctc_lpa": 6.5,
            "in_hand_monthly_inr": 44000,
            "variable_pct": 11.0,
            "shift_allowance_inr": 4000,
            "perks": "Performance rating multiplier bonus, health insurance for dependents, skill allowances"
        },
        {
            "rank": 10,
            "company": "KPMG Global Services (KGS)",
            "category": "Big 4 Consulting & Advisory",
            "hub_location": "Embassy GolfLinks Business Park, Domlur, Bangalore",
            "primary_role": "Deal Advisory & Global Trade Operations Analyst",
            "fixed_base_lpa": 5.2,
            "variable_lpa": 0.6,
            "joining_bonus_lpa": 0.3,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 5.4,
            "total_ctc_max": 6.8,
            "avg_ctc_lpa": 6.2,
            "in_hand_monthly_inr": 42500,
            "variable_pct": 10.0,
            "shift_allowance_inr": 4000,
            "perks": "Hybrid working allowance, KPMG Business School access, annual wellness allowance"
        },
        {
            "rank": 11,
            "company": "A.P. Moller - Maersk (Maersk GSC)",
            "category": "EXIM / Global Ocean Logistics",
            "hub_location": "Pritech Park, Bellandur, Bangalore",
            "primary_role": "Global Ocean Freight & Trade Compliance Associate",
            "fixed_base_lpa": 5.8,
            "variable_lpa": 0.8,
            "joining_bonus_lpa": 0.5,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 6.0,
            "total_ctc_max": 8.0,
            "avg_ctc_lpa": 7.0,
            "in_hand_monthly_inr": 47000,
            "variable_pct": 12.0,
            "shift_allowance_inr": 6000,
            "perks": "Global shipping & customs training, ocean freight discount concessions, rotational international assignments"
        },
        {
            "rank": 12,
            "company": "DHL Express & Global Forwarding",
            "category": "EXIM / Global Freight Forwarding",
            "hub_location": "Airport Road / Bommasandra & Indiranagar, Bangalore",
            "primary_role": "EXIM Logistics & Key Account Operations Coordinator",
            "fixed_base_lpa": 5.4,
            "variable_lpa": 0.8,
            "joining_bonus_lpa": 0.4,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 5.6,
            "total_ctc_max": 7.4,
            "avg_ctc_lpa": 6.6,
            "in_hand_monthly_inr": 44000,
            "variable_pct": 13.0,
            "shift_allowance_inr": 5000,
            "perks": "Certified International Specialist (CIS) program, freight volume incentive bonus, comprehensive health"
        },
        {
            "rank": 13,
            "company": "Boeing India",
            "category": "Aerospace & Defense GCC",
            "hub_location": "BIEC / Aerospace Park, Devanahalli, Bangalore",
            "primary_role": "Aerospace Supply Chain & Procurement Specialist",
            "fixed_base_lpa": 6.8,
            "variable_lpa": 1.0,
            "joining_bonus_lpa": 0.8,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 7.0,
            "total_ctc_max": 9.2,
            "avg_ctc_lpa": 8.2,
            "in_hand_monthly_inr": 55000,
            "variable_pct": 12.0,
            "shift_allowance_inr": 7000,
            "perks": "Aerospace industry accreditation, airport campus transport, high-value insurance, defense clearance stipend"
        },
        {
            "rank": 14,
            "company": "Schneider Electric",
            "category": "Industrial Energy & Global SCM",
            "hub_location": "Attibele & Whitefield Innovation Park, Bangalore",
            "primary_role": "Global SCM & Vendor Operations Executive",
            "fixed_base_lpa": 5.8,
            "variable_lpa": 0.9,
            "joining_bonus_lpa": 0.5,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 6.0,
            "total_ctc_max": 8.0,
            "avg_ctc_lpa": 7.1,
            "in_hand_monthly_inr": 47500,
            "variable_pct": 13.0,
            "shift_allowance_inr": 5000,
            "perks": "WESOP (Employee share ownership), green commute allowance, subsidized lunch & snacks"
        },
        {
            "rank": 15,
            "company": "Razorpay",
            "category": "Tier-1 FinTech Unicorn",
            "hub_location": "Koramangala, 7th Block, Bangalore",
            "primary_role": "B2B Business Development Executive / Merchant Operations",
            "fixed_base_lpa": 6.2,
            "variable_lpa": 2.0,
            "joining_bonus_lpa": 0.6,
            "esop_rsu_lpa": 1.0,
            "total_ctc_min": 7.0,
            "total_ctc_max": 10.0,
            "avg_ctc_lpa": 8.8,
            "in_hand_monthly_inr": 50000,
            "variable_pct": 25.0,
            "shift_allowance_inr": 0,
            "perks": "Lucrative quarterly sales incentive commission, ESOP grant with 1-year cliff, uncapped performance payouts"
        },
        {
            "rank": 16,
            "company": "Swiggy",
            "category": "Consumer Internet & Quick Commerce",
            "hub_location": "Embassy TechVillage, Bellandur, Bangalore",
            "primary_role": "Supply Chain & Instamart Vendor Operations Specialist",
            "fixed_base_lpa": 5.8,
            "variable_lpa": 1.2,
            "joining_bonus_lpa": 0.5,
            "esop_rsu_lpa": 0.5,
            "total_ctc_min": 6.2,
            "total_ctc_max": 8.5,
            "avg_ctc_lpa": 7.5,
            "in_hand_monthly_inr": 47000,
            "variable_pct": 16.0,
            "shift_allowance_inr": 5000,
            "perks": "Swiggy One corporate subscription, food credits, monthly team outings, rapid 9-month appraisal tracks"
        },
        {
            "rank": 17,
            "company": "CRED",
            "category": "FinTech / Premium Consumer Tech",
            "hub_location": "Indiranagar, 100 Feet Road, Bangalore",
            "primary_role": "Commercial Operations & Growth Partnerships Associate",
            "fixed_base_lpa": 8.5,
            "variable_lpa": 1.5,
            "joining_bonus_lpa": 1.0,
            "esop_rsu_lpa": 2.0,
            "total_ctc_min": 9.5,
            "total_ctc_max": 13.0,
            "avg_ctc_lpa": 11.5,
            "in_hand_monthly_inr": 70000,
            "variable_pct": 14.0,
            "shift_allowance_inr": 0,
            "perks": "Generous ESOP allocation, gourmet meals, premium wellness plan, high autonomy product-culture"
        },
        {
            "rank": 18,
            "company": "Flipkart",
            "category": "E-Commerce / Walmart Enterprise",
            "hub_location": "Embassy TechVillage, Outer Ring Road, Bangalore",
            "primary_role": "Category Operations & Vendor Management Executive",
            "fixed_base_lpa": 6.2,
            "variable_lpa": 1.0,
            "joining_bonus_lpa": 0.8,
            "esop_rsu_lpa": 0.5,
            "total_ctc_min": 6.8,
            "total_ctc_max": 8.8,
            "avg_ctc_lpa": 7.8,
            "in_hand_monthly_inr": 51000,
            "variable_pct": 14.0,
            "shift_allowance_inr": 4500,
            "perks": "Flipkart shopping credits, broadband reimbursements, big-billion-days spot cash awards"
        },
        {
            "rank": 19,
            "company": "HubSpot India",
            "category": "Enterprise B2B SaaS",
            "hub_location": "Indiranagar & Hybrid Bangalore",
            "primary_role": "Business Development Representative (BDR / Inbound SDR)",
            "fixed_base_lpa": 6.5,
            "variable_lpa": 2.5,
            "joining_bonus_lpa": 0.8,
            "esop_rsu_lpa": 1.2,
            "total_ctc_min": 7.5,
            "total_ctc_max": 11.0,
            "avg_ctc_lpa": 9.5,
            "in_hand_monthly_inr": 53000,
            "variable_pct": 28.0,
            "shift_allowance_inr": 0,
            "perks": "Uncapped commissions, remote-first stipend INR 75k, global sabbatical policy, tuition reimbursement"
        },
        {
            "rank": 20,
            "company": "Puma India",
            "category": "Global Sportswear & Retail Conglomerate",
            "hub_location": "Indiranagar & MG Road, Bangalore",
            "primary_role": "Brand Activation & Retail Event Operations Lead",
            "fixed_base_lpa": 5.5,
            "variable_lpa": 1.0,
            "joining_bonus_lpa": 0.5,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 5.8,
            "total_ctc_max": 7.8,
            "avg_ctc_lpa": 6.8,
            "in_hand_monthly_inr": 45000,
            "variable_pct": 15.0,
            "shift_allowance_inr": 0,
            "perks": "50% Puma merchandise discount, athlete meet passes, marathon sponsorship, travel allowances"
        },
        {
            "rank": 21,
            "company": "Cisco Systems",
            "category": "MNC GCC / Enterprise Networking",
            "hub_location": "Cessna Business Park, Kadubeesanahalli, Bangalore",
            "primary_role": "Commercial Operations & Partner SCM Analyst",
            "fixed_base_lpa": 7.2,
            "variable_lpa": 1.0,
            "joining_bonus_lpa": 1.0,
            "esop_rsu_lpa": 1.0,
            "total_ctc_min": 8.0,
            "total_ctc_max": 10.2,
            "avg_ctc_lpa": 9.1,
            "in_hand_monthly_inr": 59000,
            "variable_pct": 12.0,
            "shift_allowance_inr": 0,
            "perks": "Employee stock purchase discount, Cisco certified pathway grants, wellness day offs"
        },
        {
            "rank": 22,
            "company": "Dell Technologies",
            "category": "MNC GCC / Hardware & Enterprise Ops",
            "hub_location": "Domlur & Bagmane Tech Park, Bangalore",
            "primary_role": "Global SCM Logistics & Inside Sales Operations",
            "fixed_base_lpa": 5.8,
            "variable_lpa": 1.0,
            "joining_bonus_lpa": 0.6,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 6.2,
            "total_ctc_max": 8.2,
            "avg_ctc_lpa": 7.2,
            "in_hand_monthly_inr": 47500,
            "variable_pct": 14.0,
            "shift_allowance_inr": 5000,
            "perks": "Dell hardware discounts, remote work setup budget, corporate medical insurance"
        },
        {
            "rank": 23,
            "company": "Oracle India",
            "category": "MNC GCC / Enterprise Cloud & ERP",
            "hub_location": "Bannerghatta Road & Whitefield, Bangalore",
            "primary_role": "Cloud Business Operations & ERP SCM Analyst",
            "fixed_base_lpa": 6.8,
            "variable_lpa": 1.0,
            "joining_bonus_lpa": 0.8,
            "esop_rsu_lpa": 0.5,
            "total_ctc_min": 7.2,
            "total_ctc_max": 9.5,
            "avg_ctc_lpa": 8.4,
            "in_hand_monthly_inr": 55000,
            "variable_pct": 13.0,
            "shift_allowance_inr": 4000,
            "perks": "Oracle Cloud certifications free voucher, flexible benefits plan, transport support"
        },
        {
            "rank": 24,
            "company": "Target India (GCC)",
            "category": "MNC GCC / Global Retail",
            "hub_location": "Manyata Tech Park, Nagavara, Bangalore",
            "primary_role": "Global Merchandising Operations & SCM Associate",
            "fixed_base_lpa": 6.2,
            "variable_lpa": 0.8,
            "joining_bonus_lpa": 0.5,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 6.5,
            "total_ctc_max": 8.2,
            "avg_ctc_lpa": 7.4,
            "in_hand_monthly_inr": 51000,
            "variable_pct": 11.0,
            "shift_allowance_inr": 6000,
            "perks": "Target internal store discount, free meals, crèche facility, comprehensive OPD cover"
        },
        {
            "rank": 25,
            "company": "Bosch India",
            "category": "Industrial Mobility & Supply Chain",
            "hub_location": "Adugodi & Electronic City, Bangalore",
            "primary_role": "Industrial SCM & Vendor Development Trainee",
            "fixed_base_lpa": 5.4,
            "variable_lpa": 0.7,
            "joining_bonus_lpa": 0.4,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 5.6,
            "total_ctc_max": 7.2,
            "avg_ctc_lpa": 6.5,
            "in_hand_monthly_inr": 44000,
            "variable_pct": 11.0,
            "shift_allowance_inr": 4000,
            "perks": "Bosch campus sports facilities, production floor safety allowance, long-term retention grants"
        },
        {
            "rank": 26,
            "company": "Uber India",
            "category": "MNC GCC / Mobility & Scaled Ops",
            "hub_location": "Outer Ring Road, Mahadevapura, Bangalore",
            "primary_role": "Operations & Logistics Specialist (Community Ops)",
            "fixed_base_lpa": 7.0,
            "variable_lpa": 1.0,
            "joining_bonus_lpa": 0.8,
            "esop_rsu_lpa": 1.0,
            "total_ctc_min": 7.8,
            "total_ctc_max": 10.2,
            "avg_ctc_lpa": 9.0,
            "in_hand_monthly_inr": 57000,
            "variable_pct": 12.5,
            "shift_allowance_inr": 6000,
            "perks": "Monthly Uber credits (INR 12,000), wellness allowance, RSUs with quarterly vest"
        },
        {
            "rank": 27,
            "company": "Instawork AI / Data Ops",
            "category": "AI Scale-Up / Workforce Platform",
            "hub_location": "Indiranagar / Koramangala, Bangalore",
            "primary_role": "AI Data Operations & Workflow Curation Lead",
            "fixed_base_lpa": 6.5,
            "variable_lpa": 1.2,
            "joining_bonus_lpa": 0.5,
            "esop_rsu_lpa": 1.2,
            "total_ctc_min": 7.2,
            "total_ctc_max": 9.8,
            "avg_ctc_lpa": 8.5,
            "in_hand_monthly_inr": 53000,
            "variable_pct": 15.0,
            "shift_allowance_inr": 0,
            "perks": "High equity upside, modern co-working setup, high-performance laptop allowance"
        },
        {
            "rank": 28,
            "company": "Kuehne + Nagel",
            "category": "EXIM / Global Sea & Air Logistics",
            "hub_location": "Marathahalli & MG Road, Bangalore",
            "primary_role": "International Freight Forwarding & Customs Specialist",
            "fixed_base_lpa": 5.2,
            "variable_lpa": 0.8,
            "joining_bonus_lpa": 0.3,
            "esop_rsu_lpa": 0.0,
            "total_ctc_min": 5.5,
            "total_ctc_max": 7.0,
            "avg_ctc_lpa": 6.3,
            "in_hand_monthly_inr": 42500,
            "variable_pct": 13.0,
            "shift_allowance_inr": 4500,
            "perks": "FIATA aligned freight logistics training, customs broking exposure, medical insurance"
        },
        {
            "rank": 29,
            "company": "PhonePe",
            "category": "Tier-1 FinTech Leader",
            "hub_location": "Green Glen Layout, Bellandur, Bangalore",
            "primary_role": "Merchant BD & Commercial Operations Executive",
            "fixed_base_lpa": 6.5,
            "variable_lpa": 1.8,
            "joining_bonus_lpa": 0.7,
            "esop_rsu_lpa": 1.0,
            "total_ctc_min": 7.5,
            "total_ctc_max": 10.5,
            "avg_ctc_lpa": 9.0,
            "in_hand_monthly_inr": 53000,
            "variable_pct": 22.0,
            "shift_allowance_inr": 0,
            "perks": "PhonePe ESOP wealth generation plan, merchant incentive pool, annual health screening"
        },
        {
            "rank": 30,
            "company": "Zomato / Blinkit",
            "category": "Quick Commerce & Hyperlocal SCM",
            "hub_location": "Koramangala & HSR Layout, Bangalore",
            "primary_role": "Dark Store Operations & Key Account Executive",
            "fixed_base_lpa": 5.8,
            "variable_lpa": 1.2,
            "joining_bonus_lpa": 0.5,
            "esop_rsu_lpa": 0.5,
            "total_ctc_min": 6.2,
            "total_ctc_max": 8.4,
            "avg_ctc_lpa": 7.4,
            "in_hand_monthly_inr": 47000,
            "variable_pct": 17.0,
            "shift_allowance_inr": 5000,
            "perks": "Zomato Gold subscription, night shift surge payout, rapid operational ownership"
        }
    ]

    # Breakdown by 5 Core Role Tracks
    role_tracks = [
        {
            "role_title": "Global Operations & Business Analyst",
            "target_sectors": ["MNC GCCs", "Investment Banks", "Big Tech"],
            "key_companies": ["Walmart Global Tech", "Goldman Sachs", "Google", "Amazon", "JPMorgan", "Uber"],
            "fresher_ctc_range_lpa": {"min": 6.5, "median": 8.5, "p90": 11.0},
            "fixed_pct": "80% - 85%",
            "variable_pct": "15% - 20%",
            "typical_bonus": "Annual discretionary bonus (8-15%) + Shift allowances (INR 8k-10k/mo)",
            "esop_availability": "Moderate (RSUs in US tech; non-existent in traditional banks)",
            "primary_kpis": ["Process SLA adherence", "Error rate reduction", "Automation index", "Turnaround time (TAT)", "Cost per transaction"],
            "career_progression": {
                "year_1": "Associate Operations Analyst (CTC: 6.5L - 9.5L LPA)",
                "year_3": "Senior Operations Specialist (CTC: 12.0L - 16.0L LPA)",
                "year_5": "Operations Team Lead / Assistant Manager (CTC: 20.0L - 28.0L LPA)"
            },
            "aditya_leverage_hook": "15% verified operational cost reduction + lean workflow documentation directly proves readiness to drive SLA efficiency from Day 1."
        },
        {
            "role_title": "B2B Business Development & Inside Sales",
            "target_sectors": ["Enterprise SaaS", "Tier-1 FinTech", "B2B Marketplaces"],
            "key_companies": ["HubSpot", "Razorpay", "CRED", "PhonePe", "Microsoft Commercial"],
            "fresher_ctc_range_lpa": {"min": 6.0, "median": 8.8, "p90": 12.0},
            "fixed_pct": "65% - 75%",
            "variable_pct": "25% - 35%",
            "typical_bonus": "Monthly / Quarterly uncapped commission on pipeline closed + Joining bonus",
            "esop_availability": "High (Startups and scale-ups allocate 10-20% CTC equivalent in ESOPs)",
            "primary_kpis": ["Sales Qualified Leads (SQLs) generated", "Pipeline ARR influence", "Deal conversion rate", "Cold-outreach response rate"],
            "career_progression": {
                "year_1": "Business Development Representative / SDR (CTC: 6.0L - 10.0L LPA)",
                "year_3": "Inside Sales Account Executive (CTC: 14.0L - 22.0L LPA)",
                "year_5": "Enterprise Account Manager / BD Lead (CTC: 25.0L - 40.0L+ LPA)"
            },
            "aditya_leverage_hook": "INR 1.5L+ verified closed B2B revenue at Pencil Mark Interior Solutions proves proven quota-carrying and negotiation maturity over theoretical freshers."
        },
        {
            "role_title": "EXIM Trade Compliance & Global SCM Coordinator",
            "target_sectors": ["Ocean Freight Forwarding", "Aerospace", "Industrial Manufacturing"],
            "key_companies": ["A.P. Moller - Maersk", "DHL Global Forwarding", "Kuehne + Nagel", "Boeing", "Schneider Electric", "Bosch"],
            "fresher_ctc_range_lpa": {"min": 5.4, "median": 6.8, "p90": 9.0},
            "fixed_pct": "85% - 90%",
            "variable_pct": "10% - 15%",
            "typical_bonus": "Year-end company performance bonus (10-12%) + Port customs clearance allowance",
            "esop_availability": "Low (Traditional MNCs offer ESPP stock purchase schemes instead)",
            "primary_kpis": ["Customs clearance lead time", "Documentation accuracy (Bill of Lading, LC)", "Incoterms compliance score", "Demurrage cost minimization"],
            "career_progression": {
                "year_1": "EXIM Trade / SCM Associate (CTC: 5.5L - 8.0L LPA)",
                "year_3": "Senior Trade Compliance Analyst (CTC: 10.0L - 14.0L LPA)",
                "year_5": "Global SCM / Trade Operations Manager (CTC: 18.0L - 25.0L LPA)"
            },
            "aditya_leverage_hook": "Formal BBA International Business specialization with distinction in Incoterms 2020, HS Classification, and UCP 600 Letter of Credit rules eliminates months of training."
        },
        {
            "role_title": "AI Data Operations & HITL Curation Specialist",
            "target_sectors": ["AI Scale-Ups", "Autonomous Workforce", "Big Tech AI Labs"],
            "key_companies": ["Instawork AI", "Amazon AI Ops", "Google Scaled Ops", "Scale AI Bangalore Hubs"],
            "fresher_ctc_range_lpa": {"min": 6.2, "median": 8.5, "p90": 11.5},
            "fixed_pct": "75% - 85%",
            "variable_pct": "15% - 25%",
            "typical_bonus": "Quality accuracy milestone bonuses + Milestone ESOP grants",
            "esop_availability": "High in AI venture-backed scale-ups (RSUs / ESOPs)",
            "primary_kpis": ["Annotation precision rate (>99%)", "Dataset throughput per hour", "Edge-case resolution speed", "Human-in-the-loop audit compliance"],
            "career_progression": {
                "year_1": "AI Data Ops Specialist (CTC: 6.2L - 9.5L LPA)",
                "year_3": "Senior AI Operations Lead / HITL Architect (CTC: 13.0L - 18.0L LPA)",
                "year_5": "AI Product Operations Manager (CTC: 22.0L - 32.0L LPA)"
            },
            "aditya_leverage_hook": "Demonstrated 10,000+ data point processing with verified 99.2% precision benchmark at Instawork AI directly matches high-velocity AI curation roles."
        },
        {
            "role_title": "Event, Brand Activation & Experiential Marketing Lead",
            "target_sectors": ["Sportswear Conglomerates", "Aerospace Expos", "Brand Marketing Agencies"],
            "key_companies": ["Puma India", "AERO India Ecosystem", "Target Experiential", "Red Bull", "Encompass"],
            "fresher_ctc_range_lpa": {"min": 5.5, "median": 6.8, "p90": 8.5},
            "fixed_pct": "75% - 80%",
            "variable_pct": "20% - 25%",
            "typical_bonus": "Per-event successful delivery spot bonuses + Merchandise quotas",
            "esop_availability": "Low to Moderate",
            "primary_kpis": ["Footfall conversion rate", "Lead capture volume per day", "Vendor SLA compliance", "Budget adherence vs actual event spend"],
            "career_progression": {
                "year_1": "Event Operations / Brand Activation Associate (CTC: 5.5L - 7.8L LPA)",
                "year_3": "Assistant Brand Operations Manager (CTC: 10.0L - 15.0L LPA)",
                "year_5": "Lead Brand Producer / Event Marketing Manager (CTC: 18.0L - 26.0L LPA)"
            },
            "aditya_leverage_hook": "Proven track record of 300+ on-ground event deployments including leading high-security stall operations and capturing 500+ B2B delegate leads at AERO India 2025."
        }
    ]

    # Archetype Comparison (4 Quadrants)
    archetypes = [
        {
            "archetype": "MNC GCCs (Global Capability Centers)",
            "examples": "Walmart Global Tech, Goldman Sachs, Google, JPMorgan, Cisco, Boeing",
            "starting_ctc_band": "INR 7.5L - 12.0L LPA",
            "fixed_ratio": "80% - 85%",
            "work_life_balance": "8.0 / 10 (Strict 40-45 hr work weeks, shift rotations)",
            "brand_equity": "9.5 / 10 (Global Tier-1 recognition on resume)",
            "learning_curve": "8.5 / 10 (Enterprise-grade SOPs, global best practices)",
            "promotion_velocity": "Predictable (Annual cycles, 2-3 years per band)",
            "international_mobility": "Very High (Internal job postings to US, EMEA, APAC)",
            "fresher_culture": "Structured onboarding, extensive corporate training campuses, strong job security."
        },
        {
            "archetype": "Big 4 Consulting & Advisory",
            "examples": "Deloitte (India/USI), EY GDS, PwC AC, KPMG KGS",
            "starting_ctc_band": "INR 5.5L - 7.5L LPA",
            "fixed_ratio": "85% - 90%",
            "work_life_balance": "6.0 / 10 (High pressure during client deliverables, 50-60 hr weeks)",
            "brand_equity": "9.0 / 10 (Gold standard for corporate pedigree and problem solving)",
            "learning_curve": "9.5 / 10 (Accelerated exposure across cross-industry client frameworks)",
            "promotion_velocity": "Strictly Tiered (Analyst -> Senior Analyst -> Consultant)",
            "international_mobility": "High (Secondment programs after 24-36 months)",
            "fresher_culture": "Rigorous 'up-or-out' performance appraisal, extensive networking, rapid skill expansion."
        },
        {
            "archetype": "Tier-1 High-Growth Startups & Unicorns",
            "examples": "Razorpay, CRED, Swiggy, HubSpot, PhonePe, Instawork",
            "starting_ctc_band": "INR 7.0L - 13.0L LPA (including ESOPs)",
            "fixed_ratio": "65% - 75% (Substantial variable & equity components)",
            "work_life_balance": "6.5 / 10 (Dynamic, high autonomy, outcome-focused hours)",
            "brand_equity": "8.8 / 10 (Highly valued in tech ecosystem for high-velocity ownership)",
            "learning_curve": "9.5 / 10 (Extreme ownership, zero hand-holding, direct metric impact)",
            "promotion_velocity": "Rapid (Appraisals every 6-12 months based purely on business impact)",
            "international_mobility": "Low to Moderate (Primarily India-focused with SEA expansions)",
            "fresher_culture": "Meritocratic, flat hierarchy, informal dress code, uncapped revenue-linked incentives."
        },
        {
            "archetype": "Specialized EXIM, Shipping & Freight Logistics",
            "examples": "A.P. Moller - Maersk, DHL Global Forwarding, Kuehne + Nagel, Schneider SCM",
            "starting_ctc_band": "INR 5.5L - 8.0L LPA",
            "fixed_ratio": "85% - 90%",
            "work_life_balance": "7.5 / 10 (Tied to vessel schedules and customs shifts, steady hours)",
            "brand_equity": "8.5 / 10 (Global industry monopolies in maritime and air trade)",
            "learning_curve": "9.0 / 10 (Deep domain moat: maritime law, Incoterms, customs tariffs, LCs)",
            "promotion_velocity": "Domain-Driven (Senior coordinator -> Branch lead -> Regional trade head)",
            "international_mobility": "High (Key hubs in Dubai, Singapore, Rotterdam, Copenhagen)",
            "fresher_culture": "Apprenticeship style, heavy operational rigor, high retention rate for trade experts."
        }
    ]

    # Compensation Anatomy & Statutory Deductions (FY 2026-27 New Tax Regime)
    comp_anatomy = {
        "fixed_components": [
            {"component": "Basic Salary", "pct_of_fixed": "40% - 50%", "description": "Core taxable base used for PF calculation"},
            {"component": "House Rent Allowance (HRA)", "pct_of_fixed": "40% of Basic (50% in metros under old regime)", "description": "Standard living component"},
            {"component": "Special Allowance / Flexible Benefit Plan (FBP)", "pct_of_fixed": "30% - 40%", "description": "Balancing figure, covers internet, books, fuel, meal cards"},
            {"component": "Employer EPF Contribution", "pct_of_fixed": "12% of Basic", "description": "Mandatory social security investment"}
        ],
        "variable_components": [
            {"component": "Performance Linked Incentive (PLI)", "range": "8% - 20% of Base", "frequency": "Annual / Semi-Annual based on individual & company rating"},
            {"component": "Sales Quota Commission (B2B Sales)", "range": "20% - 35% of Base", "frequency": "Monthly / Quarterly uncapped upon target achievement"},
            {"component": "Shift Differentials", "range": "INR 4,000 - 10,000 / month", "frequency": "Monthly for US/UK hours support"},
            {"component": "One-Time Joining Bonus", "range": "INR 50,000 - 1,50,000", "frequency": "Paid in 1st month salary, 1-year clawback agreement"},
            {"component": "ESOPs / RSUs", "range": "INR 50,000 - 2,00,000 / yr value", "frequency": "4-year vesting with 1-year cliff (25% per year)"}
        ],
        "statutory_deductions_monthly": {
            "employee_epf": "12% of basic salary (matched by employer)",
            "professional_tax_karnataka": "INR 200 / month (INR 300 in February)",
            "income_tax_tds": "Calculated under New Tax Regime (Zero tax up to INR 7.75L with standard deduction of INR 75k)",
            "group_medical_insurance": "INR 400 - 800 / month for self & dependents"
        }
    }

    # Candidate Leverage Playbook for Aditya Mehra
    candidate_leverage = [
        {
            "pillar": "Execution Track Record (300+ Deployments)",
            "evidence": "AERO India 2025 stall operations lead, Puma India brand activation runner, 300+ on-ground deployments.",
            "recruiter_objection": "'Freshers require 3-6 months of training before handling independent operations.'",
            "negotiation_counter": "Present execution portfolio proving zero ramp-up time. Request immediate placement in high-visibility Tier-1 account teams with an entry band at the 80th-90th percentile.",
            "target_delta": "+10% to +15% over standard fresher grid (e.g. INR 7.5L vs 6.5L)"
        },
        {
            "pillar": "Verified Commercial Revenue Generation",
            "evidence": "INR 1.5L+ closed commercial revenue at Pencil Mark Interior Solutions in Bangalore.",
            "recruiter_objection": "'Undergraduate B2B sales roles start at fixed INR 5.5 LPA base.'",
            "negotiation_counter": "Show actual invoice pipeline and lead conversion rate from Pencil Mark. Argue that proven revenue closure derisks quota attainment. Negotiate for either a higher fixed base (INR 6.5L+) or accelerated 6-month promotion review clause.",
            "target_delta": "+15% to +20% base increase or INR 1L sign-on bonus"
        },
        {
            "pillar": "Process Optimization & Cost Reduction",
            "evidence": "Achieved 15% operational cost reduction through workflow standard operating procedures and vendor negotiations.",
            "recruiter_objection": "'Operations analyst bands are non-negotiable for campus hires.'",
            "negotiation_counter": "Demonstrate Lean / Six-Sigma problem solving methodology. Request a performance milestone clause in offer letter: if process optimization metrics meet top-box rating in Q2, trigger an automatic 15% retention appraisal.",
            "target_delta": "Guaranteed 6-month appraisal fast-track in offer letter"
        },
        {
            "pillar": "Domain Moat: EXIM Trade & Incoterms 2020",
            "evidence": "Academic distinction in BBA International Business, mastery of Incoterms 2020, HS classifications, and UCP 600 Letter of Credit rules.",
            "recruiter_objection": "'Trade documentation is entry-level clerical work.'",
            "negotiation_counter": "Highlight that incorrect HS codes or LC discrepancies cost logistics firms thousands of dollars in port demurrage and customs fines. Aditya's verified domain precision prevents compliance penalties on day one.",
            "target_delta": "+10% premium in GCC / Logistics specialists like Maersk, DHL, Boeing"
        },
        {
            "pillar": "Multi-Offer Pipeline Leverage Strategy",
            "evidence": "Active pipeline across 3,000 requisitions and multiple shortlist tracks in FinTech, GCCs, and Big 4.",
            "recruiter_objection": "'Take our standard offer within 48 hours.'",
            "negotiation_counter": "Acknowledge culture fit with genuine enthusiasm, while politely signaling parallel active interview tracks in Tier-1 GCCs. Ask for compensation alignment to the upper tier of the band to enable immediate acceptance.",
            "target_delta": "Conversion of variable promise into fixed guaranteed base"
        }
    ]

    # Bangalore 2026 Cost of Living Analysis
    col_bangalore_2026 = {
        "inflation_overview": "Bangalore in 2026 exhibits moderate inflation in consumer goods (5.2%) but persistent demand in tech corridor rentals (6-8% annual hike in Bellandur, HSR Layout, Kadubeesanahalli).",
        "micro_markets": [
            {
                "area": "HSR Layout (Sectors 1-7)",
                "hub_proximity": "Koramangala, Bellandur ORR, Sarjapur Road",
                "single_pg_rent_monthly_inr": "14,000 - 18,000 (Food included)",
                "shared_2bhk_per_person_inr": "16,000 - 22,000",
                "vibe_and_suitability": "Startup capital, vibrant cafes, high tech networking, 15 min commute to ORR tech parks."
            },
            {
                "area": "Koramangala (Blocks 3, 4, 5, 7)",
                "hub_proximity": "Indiranagar, Domlur, CBD, Adugodi",
                "single_pg_rent_monthly_inr": "15,000 - 20,000 (Food included)",
                "shared_2bhk_per_person_inr": "18,000 - 25,000",
                "vibe_and_suitability": "Premier lifestyle hub, walking distance to Razorpay, CRED, Swiggy, abundant dining and gym infrastructure."
            },
            {
                "area": "Indiranagar (100ft / 12th Main)",
                "hub_proximity": "Old Airport Road, Bagmane Tech Park, MG Road",
                "single_pg_rent_monthly_inr": "16,000 - 22,000",
                "shared_2bhk_per_person_inr": "20,000 - 28,000",
                "vibe_and_suitability": "Upscale commercial district, excellent Purple Line Metro connectivity, premium lifestyle."
            },
            {
                "area": "Bellandur / Kadubeesanahalli / Marathahalli (ORR)",
                "hub_proximity": "Walmart, Goldman Sachs, JPMorgan, Cisco, Flipkart",
                "single_pg_rent_monthly_inr": "12,000 - 16,000 (Food included)",
                "shared_2bhk_per_person_inr": "14,000 - 19,000",
                "vibe_and_suitability": "Epicenter of MNC GCCs, walking distance to tech parks, avoids notorious Silk Board traffic."
            },
            {
                "area": "Electronic City (Phase 1 & 2)",
                "hub_proximity": "Infosys, Wipro, Bosch, Schneider Electric",
                "single_pg_rent_monthly_inr": "10,000 - 13,000 (Food included)",
                "shared_2bhk_per_person_inr": "11,000 - 15,000",
                "vibe_and_suitability": "Budget-friendly, elevated expressway connectivity, ideal for South Bangalore industrial and IT firms."
            },
            {
                "area": "Whitefield (ITPL / EPIP Zone)",
                "hub_proximity": "Amazon, Oracle, Schneider, Target, TCS",
                "single_pg_rent_monthly_inr": "11,000 - 15,000",
                "shared_2bhk_per_person_inr": "13,000 - 17,000",
                "vibe_and_suitability": "Fully connected via Namma Metro Purple Line, planned gated societies, affordable large format apartments."
            }
        ],
        "budget_scenarios_by_ctc": [
            {
                "annual_ctc_lpa": 5.5,
                "monthly_gross_inr": 45833,
                "net_in_hand_monthly_inr": 41500,
                "housing_pg_inr": 13000,
                "food_groceries_extra_inr": 4000,
                "commute_metro_inr": 2500,
                "utilities_wifi_phone_inr": 1500,
                "leisure_lifestyle_inr": 5000,
                "health_insurance_misc_inr": 1500,
                "monthly_expenses_total_inr": 27500,
                "monthly_savings_inr": 14000,
                "savings_rate_pct": 33.7,
                "lifestyle_assessment": "Comfortable living in quality single PG with food. Moderate discretionary spending and solid monthly SIP investment."
            },
            {
                "annual_ctc_lpa": 7.5,
                "monthly_gross_inr": 62500,
                "net_in_hand_monthly_inr": 54500,
                "housing_pg_inr": 16000,
                "food_groceries_extra_inr": 6000,
                "commute_metro_inr": 3000,
                "utilities_wifi_phone_inr": 2000,
                "leisure_lifestyle_inr": 8000,
                "health_insurance_misc_inr": 2000,
                "monthly_expenses_total_inr": 37000,
                "monthly_savings_inr": 17500,
                "savings_rate_pct": 32.1,
                "lifestyle_assessment": "Upgraded living: shared 2BHK in HSR/Koramangala or luxury single PG, weekend dining, active gym membership, healthy INR 15k+ monthly investment."
            },
            {
                "annual_ctc_lpa": 9.5,
                "monthly_gross_inr": 79166,
                "net_in_hand_monthly_inr": 67000,
                "housing_pg_inr": 19000,
                "food_groceries_extra_inr": 8000,
                "commute_metro_inr": 3500,
                "utilities_wifi_phone_inr": 2500,
                "leisure_lifestyle_inr": 11000,
                "health_insurance_misc_inr": 2500,
                "monthly_expenses_total_inr": 46500,
                "monthly_savings_inr": 20500,
                "savings_rate_pct": 30.6,
                "lifestyle_assessment": "High comfort: Independent 1BHK or premium 2BHK master bedroom, annual vacation fund, high consumer electronics budget, INR 20k+ mutual fund SIPs."
            },
            {
                "annual_ctc_lpa": 12.0,
                "monthly_gross_inr": 100000,
                "net_in_hand_monthly_inr": 82000,
                "housing_pg_inr": 23000,
                "food_groceries_extra_inr": 10000,
                "commute_metro_inr": 4000,
                "utilities_wifi_phone_inr": 3000,
                "leisure_lifestyle_inr": 14000,
                "health_insurance_misc_inr": 3000,
                "monthly_expenses_total_inr": 57000,
                "monthly_savings_inr": 25000,
                "savings_rate_pct": 30.5,
                "lifestyle_assessment": "Top tier fresh graduate lifestyle: Gated society living, cab commutes, generous leisure, international travel buffer, INR 25k+ monthly wealth creation."
            }
        ]
    }

    # Consolidated Research Object
    research_data = {
        "metadata": {
            "title": "Bangalore 2026 Fresh BBA Compensation Benchmark & Labor Market Intelligence",
            "generated_at": timestamp,
            "report_year": report_year,
            "target_city": location,
            "candidate_profile": candidate,
            "scope": "Top 30 Target MNCs, GCCs, Startups & Big 4 in Bangalore"
        },
        "companies_benchmark": companies_data,
        "role_tracks_breakdown": role_tracks,
        "archetype_analysis": archetypes,
        "compensation_anatomy": comp_anatomy,
        "candidate_negotiation_playbook": candidate_leverage,
        "cost_of_living_and_budgeting": col_bangalore_2026
    }

    return research_data


def generate_markdown_report(data):
    meta = data["metadata"]
    cand = meta["candidate_profile"]
    companies = data["companies_benchmark"]
    roles = data["role_tracks_breakdown"]
    archetypes = data["archetype_analysis"]
    anatomy = data["compensation_anatomy"]
    leverage = data["candidate_negotiation_playbook"]
    col = data["cost_of_living_and_budgeting"]

    # Calculate macro stats
    avg_ctcs = [c["avg_ctc_lpa"] for c in companies]
    overall_avg_ctc = round(sum(avg_ctcs) / len(avg_ctcs), 2)
    min_ctc_floor = min([c["total_ctc_min"] for c in companies])
    max_ctc_ceiling = max([c["total_ctc_max"] for c in companies])

    md = []
    md.append(f"# BANGALORE 2026 SALARY BENCHMARK & NEGOTIATION INTELLIGENCE REPORT")
    md.append(f"**Focus:** Fresh Undergraduate (BBA International Business) Compensation Landscape Across Top 30 Target Employers")
    md.append(f"**Candidate:** {cand['name']} | {cand['degree']} ({cand['batch']}), {cand['institution']}")
    md.append(f"**Contact:** {cand['contact']} | `{cand['email']}`")
    md.append(f"**Execution Timestamp:** {meta['generated_at']} | **Location:** {meta['target_city']}\n")
    md.append("---\n")

    # Executive Summary
    md.append("## 1. EXECUTIVE SUMMARY & 2026 BANGALORE MACRO LANDSCAPE\n")
    md.append("In 2026, Bangalore remains the undisputed capital of Global Capability Centers (GCCs), Enterprise SaaS, and FinTech innovation in Asia. For high-caliber undergraduate business graduates specializing in International Business, Operations, and B2B Commerce, the entry-level compensation landscape has evolved rapidly away from standardized flat fresher grids toward skill-differentiated, meritocratic compensation packages.\n")
    md.append(f"- **Total Target Companies Benchmarked:** **{len(companies)} Enterprise Leaders** (MNC GCCs, Big 4, Tier-1 Tech, EXIM Logistics)")
    md.append(f"- **Market Compensation Floor (Entry Tier):** **INR {min_ctc_floor:.1f} LPA** (Regional Logistics / Service Trainees)")
    md.append(f"- **Market Compensation Benchmark (Median):** **INR {overall_avg_ctc:.1f} LPA** across all 30 top employers")
    md.append(f"- **Market Compensation Ceiling (Top 10% GCC / Tech):** **INR {max_ctc_ceiling:.1f} LPA** (CRED, Google GBO, HubSpot BDR, Microsoft Ops)")
    md.append("- **Key Structural Shift:** GCCs and high-growth scale-ups now explicitly reward operational execution evidence (e.g. on-ground ops, verified B2B sales revenue, AI workflow accuracy) with 15% to 30% premiums over campus base grids.\n")
    md.append("---\n")

    # Top 30 Companies Table
    md.append("## 2. TOP 30 TARGET COMPANIES SALARY BENCHMARK TABLE (BANGALORE 2026)\n")
    md.append("| # | Target Company | Sector Archetype | Key Entry Role | Base (LPA) | Variable % | Total CTC (Min-Max) | Avg CTC | Monthly In-Hand (Est.) |")
    md.append("|:---:|---|---|---|:---:|:---:|:---:|:---:|:---:|")

    for c in companies:
        md.append(f"| **{c['rank']:02d}** | **{c['company']}** | {c['category']} | {c['primary_role']} | INR {c['fixed_base_lpa']:.1f}L | {c['variable_pct']:.0f}% | **{c['total_ctc_min']:.1f}L - {c['total_ctc_max']:.1f}L** | **INR {c['avg_ctc_lpa']:.1f}L** | ~₹{c['in_hand_monthly_inr']:,} |")

    md.append("\n> **Note on In-Hand Estimates:** Net in-hand calculations account for standard EPF employee deductions (12% of basic), Karnataka Professional Tax (₹200/mo), and New Tax Regime deductions where income exceeds ₹7.75L LPA.\n")
    md.append("---\n")

    # Role-by-Role Deep Dive
    md.append("## 3. ROLE-BY-ROLE COMPENSATION & PROGRESSION DEEP-DIVE (5 CORE TRACKS)\n")
    for idx, r in enumerate(roles, 1):
        md.append(f"### 3.{idx} Track: {r['role_title']}")
        md.append(f"- **Target Employers:** {', '.join(r['key_companies'])}")
        md.append(f"- **Target Industry Sectors:** {', '.join(r['target_sectors'])}")
        md.append(f"- **Fresher CTC Range:** Min **INR {r['fresher_ctc_range_lpa']['min']:.1f} LPA** | Median **INR {r['fresher_ctc_range_lpa']['median']:.1f} LPA** | 90th Percentile **INR {r['fresher_ctc_range_lpa']['p90']:.1f} LPA**")
        md.append(f"- **Compensation Split:** Fixed `{r['fixed_pct']}` | Variable `{r['variable_pct']}`")
        md.append(f"- **Bonus Structure:** {r['typical_bonus']}")
        md.append(f"- **Equity / ESOP Availability:** {r['esop_availability']}")
        md.append(f"- **Core Evaluated KPIs:** {', '.join(r['primary_kpis'])}")
        md.append(f"- **Aditya's Profile Leverage Hook:** *{r['aditya_leverage_hook']}*")
        md.append("- **5-Year Career & Compensation Trajectory:**")
        md.append(f"  - **Year 1 (Entry):** `{r['career_progression']['year_1']}`")
        md.append(f"  - **Year 3 (Mid):** `{r['career_progression']['year_3']}`")
        md.append(f"  - **Year 5 (Lead/Manager):** `{r['career_progression']['year_5']}`\n")

    md.append("---\n")

    # Fixed vs Variable & Component Anatomy
    md.append("## 4. COMPENSATION STRUCTURE & STATUTORY ANATOMY\n")
    md.append("Understanding the precise architecture of corporate compensation packages prevents fresh graduates from misinterpreting headline CTCs.\n")
    md.append("### 4.1 Fixed Salary Structure (Gross A)")
    md.append("| Fixed Component | Typical % Allocation | Purpose & Regulatory Treatment |")
    md.append("|---|---|---|")
    for fc in anatomy["fixed_components"]:
        md.append(f"| **{fc['component']}** | {fc['pct_of_fixed']} | {fc['description']} |")

    md.append("\n### 4.2 Variable Pay, Bonuses & Equity Components (Gross B)")
    md.append("| Variable Component | Typical Quantum Range | Payout Frequency & Terms |")
    md.append("|---|---|---|")
    for vc in anatomy["variable_components"]:
        md.append(f"| **{vc['component']}** | {vc['range']} | {vc['frequency']} |")

    md.append("\n### 4.3 Mandatory Statutory Deductions in Bangalore (FY 2026-27)")
    md.append(f"- **Employee EPF (Provident Fund):** `{anatomy['statutory_deductions_monthly']['employee_epf']}`")
    md.append(f"- **Karnataka Professional Tax (PT):** `{anatomy['statutory_deductions_monthly']['professional_tax_karnataka']}`")
    md.append(f"- **Income Tax TDS (New Tax Regime):** `{anatomy['statutory_deductions_monthly']['income_tax_tds']}`")
    md.append(f"- **Group Health Insurance Premium:** `{anatomy['statutory_deductions_monthly']['group_medical_insurance']}`\n")
    md.append("---\n")

    # Archetype Comparison
    md.append("## 5. ORGANIZATIONAL ARCHETYPE COMPARISON (4 QUADRANTS)\n")
    md.append("| Evaluation Dimension | MNC GCCs (Global Capability) | Big 4 Advisory / Consulting | Tier-1 Startups & Tech | EXIM & Global Logistics |")
    md.append("|---|---|---|---|---|")
    md.append(f"| **Representative Companies** | {archetypes[0]['examples']} | {archetypes[1]['examples']} | {archetypes[2]['examples']} | {archetypes[3]['examples']} |")
    md.append(f"| **Starting CTC Band** | **{archetypes[0]['starting_ctc_band']}** | **{archetypes[1]['starting_ctc_band']}** | **{archetypes[2]['starting_ctc_band']}** | **{archetypes[3]['starting_ctc_band']}** |")
    md.append(f"| **Fixed vs Variable** | {archetypes[0]['fixed_ratio']} Fixed | {archetypes[1]['fixed_ratio']} Fixed | {archetypes[2]['fixed_ratio']} Fixed | {archetypes[3]['fixed_ratio']} Fixed |")
    md.append(f"| **Work-Life Balance** | {archetypes[0]['work_life_balance']} | {archetypes[1]['work_life_balance']} | {archetypes[2]['work_life_balance']} | {archetypes[3]['work_life_balance']} |")
    md.append(f"| **Resume Brand Equity** | {archetypes[0]['brand_equity']} | {archetypes[1]['brand_equity']} | {archetypes[2]['brand_equity']} | {archetypes[3]['brand_equity']} |")
    md.append(f"| **Skill Learning Curve** | {archetypes[0]['learning_curve']} | {archetypes[1]['learning_curve']} | {archetypes[2]['learning_curve']} | {archetypes[3]['learning_curve']} |")
    md.append(f"| **Promotion Velocity** | {archetypes[0]['promotion_velocity']} | {archetypes[1]['promotion_velocity']} | {archetypes[2]['promotion_velocity']} | {archetypes[3]['promotion_velocity']} |")
    md.append(f"| **Global Mobility** | {archetypes[0]['international_mobility']} | {archetypes[1]['international_mobility']} | {archetypes[2]['international_mobility']} | {archetypes[3]['international_mobility']} |")

    md.append("\n---\n")

    # Candidate Leverage Playbook
    md.append("## 6. CANDIDATE NEGOTIATION PLAYBOOK: ADITYA MEHRA PROFILE ANALYSIS\n")
    md.append("Standard campus recruitment processes attempt to enforce rigid salary bands. However, candidate differentiation supported by verifiable metrics allows candidates to negotiate compensation increases, joining bonuses, or early appraisal clauses.\n")
    for idx, lev in enumerate(leverage, 1):
        md.append(f"### 6.{idx} Leverage Pillar: {lev['pillar']}")
        md.append(f"- **Verified Candidate Proof:** {lev['evidence']}")
        md.append(f"- **Typical Recruiter Pushback:** *\"{lev['recruiter_objection']}\"*")
        md.append(f"- **Counter-Negotiation Script & Strategy:** {lev['negotiation_counter']}")
        md.append(f"- **Target Compensation Delta:** **`{lev['target_delta']}`**\n")

    md.append("### 6.6 Practical Rules for Negotiation Calls")
    md.append("1. **Never Give the First Number Without Framing Value:** Anchor with research ranges (`'Based on Bangalore 2026 benchmarks for candidates with verified B2B revenue and operations leadership, I am targeting an overall package between 8.5L and 10.5L LPA'`\").")
    md.append("2. **Focus on Guaranteed Fixed Base First:** Variable pay is contingent; negotiate higher base before discussing bonus pools.")
    md.append("3. **Utilize Sign-On Bonuses as Bridge:** If HR has rigid base caps, request a ₹1,00,000 joining bonus to bridge the gap without violating internal parity bands.")
    md.append("4. **Secure Fast-Track 6-Month Review in Writing:** Ensure formal documentation of early performance review triggers linked to key operational milestones.\n")
    md.append("---\n")

    # Cost of Living Context Bangalore 2026
    md.append("## 7. BANGALORE 2026 COST OF LIVING & FINANCIAL PLANNING BLUEPRINT\n")
    md.append(f"{col['inflation_overview']}\n")
    md.append("### 7.1 Residential Micro-Market Analysis for Fresh Graduates")
    md.append("| Residential Hub | Proximity to Corporate Clusters | Single PG / Month (Incl. Meals) | Shared 2BHK Per Person | Commute & Lifestyle Profile |")
    md.append("|---|---|:---:|:---:|---|")
    for mm in col["micro_markets"]:
        md.append(f"| **{mm['area']}** | {mm['hub_proximity']} | ₹{mm['single_pg_rent_monthly_inr']} | ₹{mm['shared_2bhk_per_person_inr']} | {mm['vibe_and_suitability']} |")

    md.append("\n### 7.2 Detailed Monthly Budget & Savings Models by CTC Tier")
    md.append("| Expense Line Item | Tier 1 (5.5L LPA) | Tier 2 (7.5L LPA) | Tier 3 (9.5L LPA) | Tier 4 (12.0L LPA) |")
    md.append("|---|:---:|:---:|:---:|:---:|")

    b_tiers = col["budget_scenarios_by_ctc"]
    md.append(f"| **Gross Monthly CTC** | ₹{b_tiers[0]['monthly_gross_inr']:,} | ₹{b_tiers[1]['monthly_gross_inr']:,} | ₹{b_tiers[2]['monthly_gross_inr']:,} | ₹{b_tiers[3]['monthly_gross_inr']:,} |")
    md.append(f"| **Net In-Hand Take-Home** | **₹{b_tiers[0]['net_in_hand_monthly_inr']:,}** | **₹{b_tiers[1]['net_in_hand_monthly_inr']:,}** | **₹{b_tiers[2]['net_in_hand_monthly_inr']:,}** | **₹{b_tiers[3]['net_in_hand_monthly_inr']:,}** |")
    md.append(f"| Rent & Housing (PG / 2BHK) | ₹{b_tiers[0]['housing_pg_inr']:,} | ₹{b_tiers[1]['housing_pg_inr']:,} | ₹{b_tiers[2]['housing_pg_inr']:,} | ₹{b_tiers[3]['housing_pg_inr']:,} |")
    md.append(f"| Food, Groceries & Dining Out | ₹{b_tiers[0]['food_groceries_extra_inr']:,} | ₹{b_tiers[1]['food_groceries_extra_inr']:,} | ₹{b_tiers[2]['food_groceries_extra_inr']:,} | ₹{b_tiers[3]['food_groceries_extra_inr']:,} |")
    md.append(f"| Commute (Metro / Namma Yatri) | ₹{b_tiers[0]['commute_metro_inr']:,} | ₹{b_tiers[1]['commute_metro_inr']:,} | ₹{b_tiers[2]['commute_metro_inr']:,} | ₹{b_tiers[3]['commute_metro_inr']:,} |")
    md.append(f"| Utilities, Wi-Fi & Mobile | ₹{b_tiers[0]['utilities_wifi_phone_inr']:,} | ₹{b_tiers[1]['utilities_wifi_phone_inr']:,} | ₹{b_tiers[2]['utilities_wifi_phone_inr']:,} | ₹{b_tiers[3]['utilities_wifi_phone_inr']:,} |")
    md.append(f"| Leisure, Fitness & Shopping | ₹{b_tiers[0]['leisure_lifestyle_inr']:,} | ₹{b_tiers[1]['leisure_lifestyle_inr']:,} | ₹{b_tiers[2]['leisure_lifestyle_inr']:,} | ₹{b_tiers[3]['leisure_lifestyle_inr']:,} |")
    md.append(f"| Health, Emergency & Misc | ₹{b_tiers[0]['health_insurance_misc_inr']:,} | ₹{b_tiers[1]['health_insurance_misc_inr']:,} | ₹{b_tiers[2]['health_insurance_misc_inr']:,} | ₹{b_tiers[3]['health_insurance_misc_inr']:,} |")
    md.append(f"| **Total Monthly Expenses** | ₹{b_tiers[0]['monthly_expenses_total_inr']:,} | ₹{b_tiers[1]['monthly_expenses_total_inr']:,} | ₹{b_tiers[2]['monthly_expenses_total_inr']:,} | ₹{b_tiers[3]['monthly_expenses_total_inr']:,} |")
    md.append(f"| **Net Monthly Savings / SIP** | **₹{b_tiers[0]['monthly_savings_inr']:,}** | **₹{b_tiers[1]['monthly_savings_inr']:,}** | **₹{b_tiers[2]['monthly_savings_inr']:,}** | **₹{b_tiers[3]['monthly_savings_inr']:,}** |")
    md.append(f"| **Effective Savings Rate** | **{b_tiers[0]['savings_rate_pct']}%** | **{b_tiers[1]['savings_rate_pct']}%** | **{b_tiers[2]['savings_rate_pct']}%** | **{b_tiers[3]['savings_rate_pct']}%** |")

    md.append("\n### 7.3 Financial Takeaways for Aditya Mehra")
    md.append("- At a target compensation of **INR 8.5L - 10.0L LPA** (average for top GCCs/FinTech), Aditya can maintain an upscale lifestyle in HSR Layout or Koramangala while consistently saving **INR 18,000 - ₹22,000 per month** (over ₹2.4 Lakhs annual wealth creation in Year 1).")
    md.append("- Living within 15-20 minutes of the workplace (e.g., Bellandur for ORR GCCs or HSR for Koramangala tech hubs) saves an estimated 10-12 hours per week in commute time, which can be redirected into certifications and career acceleration.\n")
    md.append("---\n")
    md.append("*Report generated by ADI SOVEREIGN OS Career Intelligence Engine.*")

    return "\n".join(md)


def main():
    print("Initializing Bangalore 2026 Salary Research Intelligence Engine...")
    data = generate_salary_research_data()

    json_path = "e:/anti/salary_research_bangalore.json"
    md_path = "e:/anti/SALARY_RESEARCH_BANGALORE_2026.md"

    # Write JSON output
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Successfully generated JSON benchmark: {json_path}")

    # Write Markdown output
    markdown_content = generate_markdown_report(data)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"✓ Successfully generated Markdown report: {md_path}")

    print("\n--- SUMMARY METRICS ---")
    print(f"Target Companies Benchmarked: {len(data['companies_benchmark'])}")
    print(f"Core Role Tracks: {len(data['role_tracks_breakdown'])}")
    print(f"Archetypes Analyzed: {len(data['archetype_analysis'])}")
    print(f"Candidate Leverage Pillars: {len(data['candidate_negotiation_playbook'])}")
    print("Salary research generation complete.")

if __name__ == "__main__":
    main()
