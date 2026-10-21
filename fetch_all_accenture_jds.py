import requests
import json
import re

job_paths = [
    ("Procurement Operations New Associate", "Procurement-Operations-Associate_AIOC-S01664213-1"),
    ("Procure to Pay Operations New Associate", "Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1"),
    ("Sales Operations New Associate", "Sales-Operations-New-Associate_AIOC-S01669615-1"),
    ("Regulatory Compliance New Associate", "Regulatory-Compliance-New-Associate_AIOC-S01667647-1"),
    ("Supply Chain Operations New Associate", "Supply-Chain-Operations-New-Associate_AIOC-S01665657-1"),
    ("Trust & Safety New Associate", "Trust---Safety-New-Associate_AIOC-S01668350-1"),
    ("Customer Contact Comms New Associate", "Customer-Contact-Comms-Associate-Messaging_AIOC-S01665940-1"),
    ("HR Service Delivery New Associate", "HR-Service-Delivery-New-Associate_AIOC-S01663367-1")
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
base_api = "https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers/job/Bengaluru/"

results = {}

for name, slug in job_paths:
    url = base_api + slug
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json().get("jobPostingInfo", {})
            desc = data.get("jobDescription", "")
            # Clean HTML tags to readable text
            clean_desc = re.sub(r'<[^>]+>', '\n', desc)
            clean_desc = re.sub(r'\n+', '\n', clean_desc).strip()
            
            # Extract key sections
            skill_m = re.search(r'Skill required:\s*(.*?)(?:\n|$)', clean_desc, re.I)
            desig_m = re.search(r'Designation:\s*(.*?)(?:\n|$)', clean_desc, re.I)
            qual_m = re.search(r'Qualifications:\s*(.*?)(?:\n|$)', clean_desc, re.I)
            exp_m = re.search(r'Years of Experience:\s*(.*?)(?:\n|$)', clean_desc, re.I)
            looking_m = re.search(r'What are we looking for\?\s*(.*?)(?:Roles and Responsibilities|About Accenture|$)', clean_desc, re.S | re.I)
            roles_m = re.search(r'Roles and Responsibilities:\s*(.*?)(?:About Accenture|Equal Employment|$)', clean_desc, re.S | re.I)
            
            results[slug] = {
                "name": name,
                "title": data.get("title"),
                "jobReqId": data.get("jobReqId"),
                "location": data.get("location"),
                "postedOn": data.get("postedOn"),
                "externalUrl": data.get("externalUrl"),
                "skill_required": skill_m.group(1).strip() if skill_m else "N/A",
                "designation": desig_m.group(1).strip() if desig_m else "N/A",
                "qualifications": qual_m.group(1).strip() if qual_m else "N/A",
                "experience": exp_m.group(1).strip() if exp_m else "0 to 1 years",
                "looking_for": looking_m.group(1).strip() if looking_m else "N/A",
                "raw_desc_snippet": clean_desc[:1200]
            }
            print(f"[OK] {name} -> {data.get('jobReqId')}")
        else:
            print(f"[ERR {r.status_code}] {name}")
    except Exception as e:
        print(f"[EXC] {name}: {e}")

with open("e:/anti/scraped_accenture_all_jds.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\nSuccessfully collected {len(results)} exact Accenture JDs!")
