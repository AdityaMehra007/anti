import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json"
}

all_bengaluru_jobs = []

for offset in range(0, 220, 20):
    payload = {
        "appliedFacets": {},
        "limit": 20,
        "offset": offset,
        "searchText": "Bengaluru"
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            jobs = res.get("jobPostings", [])
            all_bengaluru_jobs.extend(jobs)
            if len(jobs) < 20:
                break
    except Exception as e:
        print(f"Error at offset {offset}: {e}")

print(f"Total NVIDIA Bengaluru jobs collected: {len(all_bengaluru_jobs)}")
with open("scratch/nvidia_bengaluru_all_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_bengaluru_jobs, f, indent=2)

# Find business / sales / ops / non-software roles
business_keywords = ["sales", "operations", "business", "program", "specialist", "account", "partner", "analyst", "services", "commercial", "finance", "marketing"]
matched = []
for j in all_bengaluru_jobs:
    title = j.get("title", "")
    if any(k in title.lower() for k in business_keywords):
        matched.append(j)

print(f"\nMatched {len(matched)} non-pure-silicon/business/sales/ops roles:")
for m in matched:
    bullet = m.get("bulletFields", ["NO_ID"])
    print(f"[{bullet[0]}] {m.get('title')} ({m.get('postedOn', '')})")
    print(f"   URL: https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite{m.get('externalPath')}")
