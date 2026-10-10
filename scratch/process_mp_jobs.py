from bs4 import BeautifulSoup
import re
import csv
import json

with open("scratch/michaelpage_bangalore.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

jobs = []
seen_urls = set()

for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.startswith("/job-detail/") and href not in seen_urls:
        title = a.get_text(strip=True)
        if not title or title.lower() == "view job":
            continue
        seen_urls.add(href)
        
        # Parent card
        card = a.find_parent("li") or a.find_parent("div", class_=re.compile(r'job|card|row|item', re.I))
        full_text = card.get_text(" | ", strip=True) if card else ""
        
        # Extract salary if present
        salary_match = re.search(r'(INR\s*[\d,]+(?:\s*-\s*INR\s*[\d,]+)?\s*(?:per\s*year|per\s*month)?)', full_text, re.I)
        salary = salary_match.group(1) if salary_match else "Competitive / Market standard"
        
        # Extract ref code (e.g. jn-092026-7098840)
        ref_match = re.search(r'/ref/([a-zA-Z0-9_\-]+)', href)
        ref_code = ref_match.group(1).upper() if ref_match else ""
        
        # Extract work mode / type
        work_mode = "Permanent"
        if "Hybrid" in full_text:
            work_mode = "Hybrid"
        elif "WFO" in full_text:
            work_mode = "Onsite (WFO)"
        elif "Work from Home" in full_text:
            work_mode = "Remote / WFH"
            
        jobs.append({
            "ref_code": ref_code,
            "title": title,
            "salary": salary,
            "work_mode": work_mode,
            "url": "https://www.michaelpage.co.in" + href,
            "card_summary": full_text
        })

print(f"Parsed {len(jobs)} jobs.")

# Write to CSV
with open("michaelpage_bangalore_jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["ref_code", "title", "salary", "work_mode", "url"])
    writer.writeheader()
    for j in jobs:
        writer.writerow({
            "ref_code": j["ref_code"],
            "title": j["title"],
            "salary": j["salary"],
            "work_mode": j["work_mode"],
            "url": j["url"]
        })

print("Saved michaelpage_bangalore_jobs.csv")

# Print grouped preview
categories = {
    "Executive & Leadership (C-Suite / VP / Head)": [],
    "AI, Machine Learning & Engineering": [],
    "Finance, Tax & Controllership": [],
    "Product, Growth & Marketing": [],
    "Legal & Governance": []
}

for j in jobs:
    t = j["title"].lower()
    if any(k in t for k in ["head", "director", "ciso", "regional head", "vice president"]):
        categories["Executive & Leadership (C-Suite / VP / Head)"].append(j)
    elif any(k in t for k in ["ai", "architect", "engineer", "data", "application manager", "it head"]):
        categories["AI, Machine Learning & Engineering"].append(j)
    elif any(k in t for k in ["finance", "tax", "controller", "fp&a", "risk", "procurement"]):
        categories["Finance, Tax & Controllership"].append(j)
    elif any(k in t for k in ["product", "marketing", "growth"]):
        categories["Product, Growth & Marketing"].append(j)
    elif any(k in t for k in ["legal", "counsel"]):
        categories["Legal & Governance"].append(j)
    else:
        categories["Executive & Leadership (C-Suite / VP / Head)"].append(j)

for cat, clist in categories.items():
    print(f"\n### {cat} ({len(clist)} Roles)")
    for j in clist:
        print(f"  - [{j['ref_code']}] {j['title']} | {j['salary']} | {j['work_mode']}")
        print(f"    URL: {j['url']}")
