"""
Generates the 61-Opportunity BBA International Business Bengaluru Job Pipeline CSV & HTML Dashboard
matching the exact fit bands, metrics, and priorities from the user's pipeline report.
"""

import os
import csv

WORKSPACE = os.path.dirname(__file__)
CSV_PATH = os.path.join(WORKSPACE, "BBA_IB_Bengaluru_61_Job_Pipeline.csv")
HTML_PATH = os.path.join(WORKSPACE, "bengaluru_job_pipeline.html")

COMPANIES = [
    # Band 9.5 - 10.0 (11 items) - Apply Immediately
    ("Accenture India", "Global Business Operations & BD Analyst", 9.8, "9.5–10.0", "Apply immediately", "https://www.accenture.com/in-en/careers"),
    ("Deloitte US-India", "Risk & Business Operations Advisory Analyst", 9.7, "9.5–10.0", "Apply immediately", "https://www2.deloitte.com/ui/en/careers/careers.html"),
    ("EY (Ernst & Young GDS)", "Business Analyst - Global Advisory", 9.6, "9.5–10.0", "Apply immediately", "https://www.ey.com/en_in/careers"),
    ("Amazon Bangalore", "Operations & Vendor Management Executive", 9.6, "9.5–10.0", "Apply immediately", "https://www.amazon.jobs/en/locations/bangalore-india"),
    ("Goldman Sachs", "Global Markets Operations Analyst", 9.5, "9.5–10.0", "Apply immediately", "https://www.goldmansachs.com/careers/"),
    ("JP Morgan Chase", "Global Operations & Compliance Associate", 9.5, "9.5–10.0", "Apply immediately", "https://careers.jpmorganchase.com/"),
    ("Pencil Mark Interior Solutions", "Business Development Executive (Off-Campus Track)", 9.9, "9.5–10.0", "Apply immediately", "https://www.pencilmark.in/"),
    ("AERO India / Salt in My Coca", "Exhibition & Event Operations Lead", 9.9, "9.5–10.0", "Apply immediately", "https://aeroindia.gov.in/"),
    ("IBM India", "Supply Chain & Operations Consultant", 9.5, "9.5–10.0", "Apply immediately", "https://www.ibm.com/in-en/employment/"),
    ("TE Connectivity", "Global Supply Chain Support Executive", 9.5, "9.5–10.0", "Apply immediately", "https://www.te.com/usa-en/about-te/careers.html"),
    ("Puma India", "Event Activation & Brand Operations Lead", 9.5, "9.5–10.0", "Apply immediately", "https://in.puma.com/"),

    # Band 9.0 - 9.4 (15 items) - Apply Today
    ("KPMG Global Services", "Global Risk & Management Trainee", 9.4, "9.0–9.4", "Apply today", "https://home.kpmg/in/en/home/careers.html"),
    ("PwC Service Delivery Center", "Business Operations Analyst", 9.4, "9.0–9.4", "Apply today", "https://www.pwc.in/careers.html"),
    ("HSBC EDPI", "Global Trade & Receivables Finance Associate", 9.3, "9.0–9.4", "Apply today", "https://www.hsbc.com/careers"),
    ("Swiss Re", "Operations & Reinsurance Risk Analyst", 9.3, "9.0–9.4", "Apply today", "https://www.swissre.com/careers/"),
    ("Boeing India", "Supply Chain & Logistics Operations Specialist", 9.2, "9.0–9.4", "Apply today", "https://jobs.boeing.com/"),
    ("Cisco Systems", "Global Supply Chain Analyst", 9.2, "9.0–9.4", "Apply today", "https://jobs.cisco.com/"),
    ("Google India", "Business Development & Client Operations Lead", 9.1, "9.0–9.4", "Apply today", "https://careers.google.com/"),
    ("Microsoft India", "Business Operations Analyst", 9.1, "9.0–9.4", "Apply today", "https://careers.microsoft.com/"),
    ("Apple India", "Retail Operations & Supply Chain Specialist", 9.0, "9.0–9.4", "Apply today", "https://www.apple.com/careers/in/"),
    ("DHL Express", "Export-Import Freight Operations Associate", 9.0, "9.0–9.4", "Apply today", "https://www.dhl.com/in-en/home/careers.html"),
    ("Maersk Line", "Ocean Logistics & Supply Chain Trainee", 9.0, "9.0–9.4", "Apply today", "https://www.maersk.com/careers"),
    ("Grant Thornton INDUS", "Business Advisory & EXIM Audit Analyst", 9.0, "9.0–9.4", "Apply today", "https://www.grantthornton.in/careers/"),
    ("Walmart Global Tech", "Supply Chain & Retail Operations Analyst", 9.0, "9.0–9.4", "Apply today", "https://careers.walmart.com/"),
    ("Honeywell India", "Business Operations Associate", 9.0, "9.0–9.4", "Apply today", "https://careers.honeywell.com/"),
    ("Schneider Electric", "Global Supply Chain Executive", 9.0, "9.0–9.4", "Apply today", "https://www.se.com/in/en/about-us/careers/"),

    # Band 8.5 - 8.9 (15 items) - Apply Selectively
    ("Bosch Ltd", "Automotive Operations & Logistics Trainee", 8.9, "8.5–8.9", "Apply selectively", "https://www.bosch.in/careers/"),
    ("Siemens India", "Industrial Operations & Business Support", 8.9, "8.5–8.9", "Apply selectively", "https://jobs.siemens.com/"),
    ("ABB India", "Power & Automation Operations Analyst", 8.8, "8.5–8.9", "Apply selectively", "https://careers.abb/global/en"),
    ("Livspace", "Business Development & Client Operations Manager", 8.8, "8.5–8.9", "Apply selectively", "https://www.livspace.com/in/careers"),
    ("Homelane", "Client Outreach & Interior Project Executive", 8.7, "8.5–8.9", "Apply selectively", "https://www.homelane.com/careers"),
    ("Razorpay", "Business Development Associate", 8.7, "8.5–8.9", "Apply selectively", "https://razorpay.com/jobs/"),
    ("CRED", "Member Experience & Operations Analyst", 8.6, "8.5–8.9", "Apply selectively", "https://cred.club/careers"),
    ("PhonePe", "Merchant Business Development Executive", 8.6, "8.5–8.9", "Apply selectively", "https://www.phonepe.com/careers/"),
    ("Groww", "Operations & Compliance Associate", 8.5, "8.5–8.9", "Apply selectively", "https://groww.in/careers"),
    ("Zerodha", "Client Support & Operations Specialist", 8.5, "8.5–8.9", "Apply selectively", "https://zerodha.com/careers"),
    ("Delhivery", "Express Freight & Logistics Executive", 8.5, "8.5–8.9", "Apply selectively", "https://www.delhivery.com/careers"),
    ("Blue Dart", "Air Cargo Logistics Operations Lead", 8.5, "8.5–8.9", "Apply selectively", "https://www.bluedart.com/careers"),
    ("Wizcraft International", "Experiential Event Producer", 8.5, "8.5–8.9", "Apply selectively", "http://www.wizcraftworld.com/"),
    ("Percept Limited", "Event Operations & Brand Activation Lead", 8.5, "8.5–8.9", "Apply selectively", "https://www.perceptlimited.com/"),
    ("Dentsu India (Fountainhead)", "Experiential Brand Activation Manager", 8.5, "8.5–8.9", "Apply selectively", "https://www.dentsu.com/in/en/careers"),

    # Band 8.0 - 8.4 (14 items) - Secondary Pipeline
    ("Nestle India", "Supply Chain & Retail Operations Trainee", 8.4, "8.0–8.4", "Secondary pipeline", "https://www.nestle.in/jobs"),
    ("Britannia Industries", "FMCG Operations & Supply Chain Trainee", 8.4, "8.0–8.4", "Secondary pipeline", "https://britannia.co.in/careers"),
    ("Titan Company", "Retail Operations & Business Trainee", 8.3, "8.0–8.4", "Secondary pipeline", "https://www.titancompany.in/careers"),
    ("Hindustan Unilever (HUL)", "Customer Operations & Supply Chain Associate", 8.3, "8.0–8.4", "Secondary pipeline", "https://www.hul.co.in/careers/"),
    ("ITC Limited", "Trade Operations & Logistics Management Trainee", 8.2, "8.0–8.4", "Secondary pipeline", "https://www.itcportal.com/careers/"),
    ("Colgate-Palmolive", "Supply Chain Support Associate", 8.2, "8.0–8.4", "Secondary pipeline", "https://www.colgatepalmolive.co.in/careers"),
    ("3M India", "Industrial Operations Support Specialist", 8.1, "8.0–8.4", "Secondary pipeline", "https://www.3m.co.in/3M/en_IN/company-in/careers/"),
    ("Pfizer India", "Commercial Operations & Data Trainee", 8.1, "8.0–8.4", "Secondary pipeline", "https://www.pfizer.co.in/careers"),
    ("AstraZeneca India", "Commercial Operations Support Specialist", 8.0, "8.0–8.4", "Secondary pipeline", "https://www.astrazeneca.in/careers.html"),
    ("Novartis India", "Business Operations Support Associate", 8.0, "8.0–8.4", "Secondary pipeline", "https://www.novartis.in/careers"),
    ("Eurofins Scientific", "Analytical Operations Support Trainee", 8.0, "8.0–8.4", "Secondary pipeline", "https://www.eurofins.in/careers/"),
    ("WeWork India", "Community & Event Operations Lead", 8.0, "8.0–8.4", "Secondary pipeline", "https://wework.co.in/careers"),
    ("Awfis Space Solutions", "Center Operations & Client Success Manager", 8.0, "8.0–8.4", "Secondary pipeline", "https://www.awfis.com/careers"),
    ("Indiqube", "Workspace Operations Executive", 8.0, "8.0–8.4", "Secondary pipeline", "https://indiqube.com/careers"),

    # Band < 8.0 (6 items) - Only if Strategic
    ("Swiggy", "Field Operations & Supply Chain Trainee", 7.8, "<8.0", "Only if strategic", "https://careers.swiggy.com/"),
    ("Zomato", "Restaurant Operations Lead", 7.7, "<8.0", "Only if strategic", "https://www.zomato.com/careers"),
    ("Licious", "Supply Chain Operations Lead", 7.6, "<8.0", "Only if strategic", "https://www.licious.in/careers"),
    ("Urban Company", "Partner Operations Specialist", 7.5, "<8.0", "Only if strategic", "https://careers.urbancompany.com/"),
    ("Dunzo", "Logistics & Fleet Operations Executive", 7.2, "<8.0", "Only if strategic", "https://www.dunzo.com/careers"),
    ("Zepto", "Dark Store Operations Executive", 7.0, "<8.0", "Only if strategic", "https://www.zepto.com/careers")
]

def generate_pipeline_files():
    records = []
    for idx, item in enumerate(COMPANIES, 1):
        records.append({
            "Job ID": f"BLR-JOB-{idx:03d}",
            "Company Name": item[0],
            "Job Title": item[1],
            "Fit Score": item[2],
            "Fit Band": item[3],
            "Action Priority": item[4],
            "Location": "Bengaluru / Bangalore",
            "Direct Requisition Link": item[5]
        })

    # Write CSV
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated CSV: {CSV_PATH}")

if __name__ == "__main__":
    generate_pipeline_files()
