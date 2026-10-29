import json, csv

# Define the 11 target employers and their primary roles
targets = [
    {
        "company": "Accenture India",
        "canonical": "Accenture",
        "req_id": "BLR-JOB-001",
        "alt_req_id": "ACN-BLR-SCM-4821",
        "role": "Global Business Operations & BD Analyst",
        "alt_role": "Supply Chain & Procurement Operations Associate",
        "corridor": "Manyata Embassy Business Park / Bellandur (RMZ Ecospace)",
        "tech_park": "Manyata Embassy Business Park (Blocks G1/G3) & RMZ Ecospace",
        "domain": "Operations / Supply Chain",
        "link": "https://www.accenture.com/in-en/careers",
        "connections": 115,
        "recruiters": 24,
        "managers": 8,
        "top_contact": "Darshana Mahesh",
        "top_contact_url": "https://www.linkedin.com/in/darshana-mahesh-6906b6104",
        "exp_required": "0-1 Yrs",
        "ctc_inr": "₹6.5L - ₹11.0L"
    },
    {
        "company": "Deloitte US-India",
        "canonical": "Deloitte",
        "req_id": "BLR-JOB-002",
        "alt_req_id": "APX-037",
        "role": "Risk & Business Operations Advisory Analyst",
        "alt_role": "Supply Chain & Operations Transformation Consultant",
        "corridor": "Bellandur (RMZ Ecoworld) / Whitefield (Divyasree TechnoPark)",
        "tech_park": "RMZ Ecoworld, Building 7 (Bellandur) & Divyasree TechnoPark (Whitefield)",
        "domain": "Advisory/Risk / Operations",
        "link": "https://www2.deloitte.com/ui/en/careers/careers.html",
        "connections": 106,
        "recruiters": 14,
        "managers": 16,
        "top_contact": "Sinchana B / Sneha Patel",
        "top_contact_url": "https://www.linkedin.com/in/sinchana-b-730413256",
        "exp_required": "0-2 Yrs",
        "ctc_inr": "₹7.2L - ₹11.5L"
    },
    {
        "company": "Goldman Sachs Services India",
        "canonical": "Goldman Sachs",
        "req_id": "BLR-JOB-005",
        "alt_req_id": "APX-023",
        "role": "Global Markets Operations Analyst (Clearance & Trade Settlements)",
        "alt_role": "Global Operations Analyst - Prime Brokerage",
        "corridor": "Outer Ring Road (Helios Business Park, Kadubeesanahalli)",
        "tech_park": "Helios Business Park (Kadubeesanahalli / ORR)",
        "domain": "Trade Finance / Operations",
        "link": "https://www.goldmansachs.com/careers/",
        "connections": 78,
        "recruiters": 4,
        "managers": 12,
        "top_contact": "Akshitha R",
        "top_contact_url": "https://www.linkedin.com/in/akshitha-r-737228240",
        "exp_required": "0-1 Yrs",
        "ctc_inr": "₹9.0L - ₹14.0L"
    },
    {
        "company": "Amazon Development Center India",
        "canonical": "Amazon",
        "req_id": "BLR-JOB-004",
        "alt_req_id": "APX-022",
        "role": "Operations & Vendor Management Executive",
        "alt_role": "Operations Specialist / TRMS Risk Investigator",
        "corridor": "Bellandur (RMZ Ecoworld) / Rajajinagar (World Trade Center)",
        "tech_park": "RMZ Ecoworld (Bellandur) & Brigade Gateway WTC",
        "domain": "Operations / Supply Chain",
        "link": "https://www.amazon.jobs/en/locations/bangalore-india",
        "connections": 40,
        "recruiters": 9,
        "managers": 9,
        "top_contact": "Sreeja Govindankutty",
        "top_contact_url": "https://www.linkedin.com/in/sreeja-govindankutty",
        "exp_required": "0-2 Yrs",
        "ctc_inr": "₹7.2L - ₹9.8L"
    },
    {
        "company": "IBM India Global Services",
        "canonical": "IBM",
        "req_id": "BLR-JOB-009",
        "alt_req_id": "WORLD_TITAN_009",
        "role": "Supply Chain & Operations Consultant (Associate)",
        "alt_role": "Procurement Operations Specialist",
        "corridor": "Manyata Embassy Business Park (Hebbal) / Domlur (Embassy GolfLinks)",
        "tech_park": "Manyata Embassy Business Park (Blocks G2/D3) & Embassy GolfLinks (EGL)",
        "domain": "Supply Chain / Operations",
        "link": "https://www.ibm.com/in-en/employment/",
        "connections": 82,
        "recruiters": 14,
        "managers": 7,
        "top_contact": "Manisha Suna",
        "top_contact_url": "https://www.linkedin.com/in/manisha-suna-9769b2145",
        "exp_required": "0-2 Yrs",
        "ctc_inr": "₹7.0L - ₹11.0L"
    },
    {
        "company": "JPMorgan Chase & Co.",
        "canonical": "JPMorganChase",
        "req_id": "BLR-JOB-006",
        "alt_req_id": "JPMC-BLR-REF-9021",
        "role": "Global Operations & Trade Finance Associate",
        "alt_role": "Reference Data Operations Analyst",
        "corridor": "Outer Ring Road (Prestige Tech Park / Embassy TechVillage)",
        "tech_park": "Embassy TechVillage & Prestige Tech Park (Kadubeesanahalli)",
        "domain": "Trade Finance / Operations",
        "link": "https://careers.jpmorganchase.com/",
        "connections": 40,
        "recruiters": 1,
        "managers": 10,
        "top_contact": "Shweta Sheregar",
        "top_contact_url": "https://www.linkedin.com/in/shweta-sheregar-985b341a",
        "exp_required": "0-2 Yrs",
        "ctc_inr": "₹8.0L - ₹13.0L"
    },
    {
        "company": "KPMG Global Services (KGS)",
        "canonical": "KPMG",
        "req_id": "BLR-JOB-012",
        "alt_req_id": "APX-040",
        "role": "Global Risk & Management Trainee",
        "alt_role": "Procurement Advisory & Operations Analyst",
        "corridor": "Bellandur (RMZ Ecoworld / Ecospace) / Domlur (Embassy GolfLinks)",
        "tech_park": "RMZ Ecoworld (Building 6, Bellandur) & Embassy GolfLinks (EGL)",
        "domain": "Advisory/Risk / Operations",
        "link": "https://home.kpmg/in/en/home/careers.html",
        "connections": 49,
        "recruiters": 8,
        "managers": 4,
        "top_contact": "Kohely Ghosal",
        "top_contact_url": "https://www.linkedin.com/in/kohely-ghosal",
        "exp_required": "0-1 Yrs",
        "ctc_inr": "₹6.5L - ₹10.5L"
    },
    {
        "company": "PwC Service Delivery Center (SDC)",
        "canonical": "PwC",
        "req_id": "BLR-JOB-013",
        "alt_req_id": "APX-039",
        "role": "Business Operations Analyst - Global Client Delivery",
        "alt_role": "Supply Chain & Operations Advisory Associate",
        "corridor": "Manyata Embassy Business Park (Hebbal) / Bellandur (RMZ Ecospace)",
        "tech_park": "Manyata Tech Park & Prestige Tech Park (Marathahalli) & RMZ Ecospace",
        "domain": "Operations / Advisory/Risk",
        "link": "https://www.pwc.in/careers.html",
        "connections": 39,
        "recruiters": 4,
        "managers": 2,
        "top_contact": "Latha Dhananjay",
        "top_contact_url": "https://www.linkedin.com/in/latha-dhananjay-3867a41a4",
        "exp_required": "0-2 Yrs",
        "ctc_inr": "₹7.0L - ₹11.0L"
    },
    {
        "company": "Walmart Global Tech India",
        "canonical": "Walmart Global Tech",
        "req_id": "BLR-JOB-024",
        "alt_req_id": "APX-025",
        "role": "Supply Chain & Retail Operations Analyst",
        "alt_role": "Associate Operations Analyst (Global SCM)",
        "corridor": "Outer Ring Road (Cessna Business Park) / Bellandur (RMZ Ecospace)",
        "tech_park": "Cessna Business Park & RMZ Ecospace (Kadubeesanahalli/Bellandur)",
        "domain": "Supply Chain / Operations",
        "link": "https://careers.walmart.com/",
        "connections": 5,
        "recruiters": 1,
        "managers": 1,
        "top_contact": "Ammini Swetha Ravindran",
        "top_contact_url": "https://www.linkedin.com/in/ammini-swetha-ravindran-3a943a9a",
        "exp_required": "0-2 Yrs",
        "ctc_inr": "₹8.5L - ₹13.5L"
    },
    {
        "company": "Delhivery Bengaluru Mega-Hub",
        "canonical": "Delhivery",
        "req_id": "BLR-JOB-037",
        "alt_req_id": "DEL-BLR-LOG-01",
        "role": "Express Freight & Logistics Executive",
        "alt_role": "Express Parcel Logistics Operations Lead",
        "corridor": "Outer Ring Road / Whitefield Hub / Nelamangala Gateway",
        "tech_park": "Delhivery Bengaluru Hub (Whitefield & ORR Corridor)",
        "domain": "Supply Chain / Merchant BD",
        "link": "https://www.delhivery.com/careers",
        "connections": 3,
        "recruiters": 1,
        "managers": 1,
        "top_contact": "Chanchala Ugra",
        "top_contact_url": "https://www.linkedin.com/in/chanchala-ugra-a44029145",
        "exp_required": "0-2 Yrs",
        "ctc_inr": "₹5.5L - ₹8.5L"
    },
    {
        "company": "PhonePe (Walmart Group)",
        "canonical": "PhonePe",
        "req_id": "BLR-JOB-034",
        "alt_req_id": "PHONEPE-BD-01",
        "role": "Merchant Business Development Executive",
        "alt_role": "Merchant Onboarding & Risk Operations Analyst",
        "corridor": "Bellandur (Green Glen Layout / Outer Ring Road)",
        "tech_park": "Green Glen Layout & EcoWorld proximity (Bellandur)",
        "domain": "Merchant BD / Operations",
        "link": "https://www.phonepe.com/careers/",
        "connections": 6,
        "recruiters": 1,
        "managers": 0,
        "top_contact": "Anshika Kohli",
        "top_contact_url": "https://www.linkedin.com/in/anshika-kohli",
        "exp_required": "0-2 Yrs",
        "ctc_inr": "₹6.0L - ₹9.5L"
    }
]

def score_target(t):
    # Dimension 1: Role Fit (25%)
    s_role = 98.0
    # Dimension 2: Skill Fit (20%)
    s_skill = 96.0
    # Dimension 3: Geo/Corridor Fit (15%)
    s_geo = 100.0  # In primary Bengaluru corridor
    # Dimension 4: Exp Fit (15%)
    s_exp = 95.0 if '0-1' in t['exp_required'] else 90.0
    # Dimension 5: Network Density (15%)
    if t['connections'] >= 50:
        s_net = 98.0
    elif t['connections'] >= 20:
        s_net = 92.0
    elif t['connections'] >= 5:
        s_net = 82.0
    else:
        s_net = 75.0
    # Dimension 6: Employer Tier (10%)
    s_tier = 98.0 if t['canonical'] not in ['Delhivery', 'PhonePe'] else 92.0

    total_100 = (s_role * 0.25) + (s_skill * 0.20) + (s_geo * 0.15) + (s_exp * 0.15) + (s_net * 0.15) + (s_tier * 0.10)
    score_10 = round(total_100 / 10.0, 1)
    
    tier = "P0 (Golden Strike)" if total_100 >= 90.0 else ("P1 (High Opportunity)" if total_100 >= 80.0 else "P2 (Standard)")
    return round(total_100, 1), score_10, tier

print(f"{'Company':25} | {'100-pt':6} | {'10-pt':5} | {'Tier':22} | {'Connections':11} | {'Domain'}")
print("-" * 95)
for t in targets:
    s100, s10, tier = score_target(t)
    t['score_100'] = s100
    t['score_10'] = s10
    t['priority_tier'] = tier
    print(f"{t['canonical']:25} | {s100:6.1f} | {s10:5.1f} | {tier:22} | {t['connections']:11} | {t['domain']}")

with open('.agents/teamwork/explorer_survey_2/scored_inventory.json', 'w', encoding='utf-8') as f:
    json.dump(targets, f, indent=2)
print("\nSaved scored inventory to .agents/teamwork/explorer_survey_2/scored_inventory.json")
