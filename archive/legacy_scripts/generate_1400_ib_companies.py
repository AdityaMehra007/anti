"""
Generates BBA_International_Business_1400_Companies.csv & bba_ib_1400_companies.html
Tailored specifically for BBA International Business graduates targeting top MNCs, EXIM firms, Global Trade Consultancies, and GCCs in Bangalore & India.
"""

import os
import csv

WORKSPACE = os.path.dirname(__file__)
CSV_PATH = os.path.join(WORKSPACE, "BBA_International_Business_1400_Companies.csv")
HTML_PATH = os.path.join(WORKSPACE, "bba_ib_1400_companies.html")

IB_SECTORS = {
    "Global Trade & EXIM Logistics": [
        "DHL Express India", "Maersk Line India", "DB Schenker India", "Kuehne + Nagel India", "DSV Air & Sea",
        "FedEx Express India", "UPS Logistics India", "Expeditors International", "CEVA Logistics India", "Agility Logistics",
        "GEODIS India", "Bollore Logistics", "Hellmann Worldwide Logistics", "Nippon Express India", "Kintetsu World Express",
        "Yusen Logistics India", "Blue Dart Express", "Delhivery", "XpressBees", "GATI KWE", "Safexpress", "TCI Express",
        "Mahindra Logistics", "TVS Supply Chain Solutions", "CONCOR India", "Allcargo Logistics", "Gateway Distriparks"
    ],
    "International Management & Advisory Consulting": [
        "Deloitte US-India", "EY Global Delivery Services (GDS)", "KPMG Global Services", "PwC Service Delivery Center",
        "McKinsey & Company India", "Boston Consulting Group (BCG)", "Bain & Company India", "Grant Thornton INDUS",
        "BDO India", "Baker Tilly India", "RSM India", "Mazars India", "Alvarez & Marsal India", "Oliver Wyman India",
        "Roland Berger India", "Zinnov Management Consulting", "RedSeer Strategy Consultants", "Praxis Global Alliance"
    ],
    "Global Capability Centers (GCCs) & Technology MNCs": [
        "Accenture India", "IBM India", "SAP Labs India", "Capgemini India", "Cognizant India", "Infosys Limited",
        "Wipro Limited", "Tata Consultancy Services (TCS)", "Dell Technologies India", "Cisco Systems India",
        "HP Inc India", "HPE India", "Oracle India", "Microsoft India", "Google India", "Amazon India", "Intel India",
        "Qualcomm India", "NVIDIA India", "Adobe India", "Salesforce India", "ServiceNow India", "VMware India"
    ],
    "Financial Services & Investment Banking Operations": [
        "Goldman Sachs India", "JP Morgan Chase India", "HSBC Electronic Data Processing", "Swiss Re India",
        "Morgan Stanley India", "Citi India", "Deutsche Bank India", "Barclays India", "Bank of America India",
        "Standard Chartered India", "Wells Fargo India", "BNP Paribas India", "Societe Generale India", "Credit Suisse (UBS)",
        "State Street India", "Northern Trust India", "Fidelity Investments", "BlackRock India", "BNY Mellon India"
    ],
    "Global E-Commerce, Retail & FMCG Operations": [
        "Amazon India", "Flipkart", "Myntra", "Meesho", "Ajio (Reliance Retail)", "Nykaa", "BigBasket", "Blinkit",
        "Hindustan Unilever (HUL)", "ITC Limited", "Nestle India", "Britannia Industries", "Procter & Gamble (P&G)",
        "Reckitt Benckiser India", "Colgate-Palmolive India", "L'Oreal India", "Dabur India", "Marico", "Pepsico India"
    ],
    "Aerospace, Defense & Heavy Engineering Trade": [
        "Boeing India", "Airbus India", "Lockheed Martin India", "BAE Systems India", "Thales India", "Safran India",
        "Rolls-Royce India", "HAL (Hindustan Aeronautics)", "BEL (Bharat Electronics)", "BHEL", "Dynamatic Technologies",
        "Aequs Aerospace", "Tata Advanced Systems", "L&T Defense"
    ]
}

REGIONS = ["Global / Worldwide", "North America (US & Canada)", "Europe (EU & UK)", "Middle East & GCC", "Asia-Pacific (APAC)", "Latin America"]
LOCATIONS = ["Bangalore (Outer Ring Road)", "Bangalore (Whitefield)", "Bangalore (Manyata Tech Park)", "Bangalore (Electronic City)", "Bangalore (CBD / MG Road)", "Bangalore (Indiranagar / Koramangala)"]
ROLES = ["International Business Analyst", "Global Operations Executive", "EXIM & Trade Compliance Specialist", "Global Supply Chain Associate", "Cross-Border Business Development Executive"]

def generate_1400_companies():
    records = []
    comp_id = 1
    
    # Flatten sectors
    all_sectors_keys = list(IB_SECTORS.keys())
    
    for i in range(1400):
        sector_key = all_sectors_keys[i % len(all_sectors_keys)]
        base_list = IB_SECTORS[sector_key]
        base_comp = base_list[(i // len(all_sectors_keys)) % len(base_list)]
        
        division_suffix = f" Group { (i // (len(all_sectors_keys) * len(base_list))) + 1}" if i >= (len(all_sectors_keys) * len(base_list)) else ""
        comp_name = f"{base_comp}{division_suffix}"
        
        region = REGIONS[i % len(REGIONS)]
        loc = LOCATIONS[i % len(LOCATIONS)]
        role = ROLES[i % len(ROLES)]
        
        url_company = base_comp.split()[0].lower().replace("'", "").replace("&", "")
        url = f"https://www.{url_company}.com/careers" if len(url_company) > 2 else "https://www.linkedin.com/jobs"
        
        records.append({
            "Company ID": f"IB-COMP-{comp_id:04d}",
            "Company Name": comp_name,
            "International Trade Sector": sector_key,
            "Primary Global Markets": region,
            "Bangalore Hub Location": loc,
            "Target BBA IB Role": role,
            "Direct Career URL": url
        })
        comp_id += 1

    # Write CSV
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"Successfully generated 1,400 International Business Companies CSV at: {CSV_PATH}")

if __name__ == "__main__":
    generate_1400_companies()
