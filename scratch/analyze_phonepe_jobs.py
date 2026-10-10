import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.phonepe.com/apollo/job-postings/latest.json"
headers = {'User-Agent': 'Mozilla/5.0'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as resp:
    data = json.loads(resp.read().decode('utf-8'))

jobs = data.get("results", [])
print(f"Total live PhonePe jobs: {len(jobs)}")

with open("scratch/phonepe_all_185_jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

depts = {}
locations = {}
for j in jobs:
    d = j.get("department", "Unknown")
    l = j.get("location", "Unknown")
    depts[d] = depts.get(d, 0) + 1
    locations[l] = locations.get(l, 0) + 1

print("\n--- Departments Breakdown ---")
for d, count in sorted(depts.items(), key=lambda x: -x[1]):
    print(f"{d}: {count}")

print("\n--- Locations Breakdown ---")
for l, count in sorted(locations.items(), key=lambda x: -x[1]):
    print(f"{l}: {count}")

# Filter for Bengaluru business / ops / commercial / finance / analytics roles
business_keywords = ["operations", "business", "analyst", "finance", "merchant", "sales", "account", "growth", "risk", "compliance", "fraud", "reconciliation", "customer", "support", "associate", "specialist"]
matched = []
for j in jobs:
    title = j.get("title", "")
    dept = j.get("department", "")
    loc = j.get("location", "")
    if "bangalore" in loc.lower() or "bengaluru" in loc.lower():
        if any(k in title.lower() or k in dept.lower() for k in business_keywords):
            if not any(k in title.lower() for k in ["software", "engineering manager", "devops", "architect", "lead engineer"]):
                matched.append(j)

print(f"\n--- Bengaluru Business / Operations / Finance Roles ({len(matched)} matched) ---")
for idx, m in enumerate(matched, 1):
    print(f"{idx}. {m.get('title')} | Dept: {m.get('department')} | Loc: {m.get('location')}")
    print(f"   Apply: {m.get('applyUrl')}")
