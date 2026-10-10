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

# Facets to query: Sales, Business Development, Professional Services, IT, Program Manager, Univ Employment
family_ids = [
    "0c40f6bd1d8f10ae43ffcac5bbec7e90", # Sales
    "0c40f6bd1d8f10ae43ffac5fdfac7e76", # Business Development
    "e8bdc341a93101bd5f4d2b0a1c005e36", # Professional Services
    "0c40f6bd1d8f10ae43ffc668c6847e8c", # Program Manager
    "0c40f6bd1d8f10ae43ffda1e8d447e94"  # Univ Employment
]

payload = {
    "appliedFacets": {
        "jobFamilyGroup": family_ids
    },
    "limit": 50,
    "offset": 0,
    "searchText": "Bengaluru"
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
with urllib.request.urlopen(req, context=ctx) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    jobs = res.get("jobPostings", [])
    print(f"Total non-pure-engineering jobs in Bengaluru: {len(jobs)}")
    for j in jobs:
        bullet = j.get("bulletFields", ["NO_ID"])
        print(f"[{bullet[0]}] {j.get('title')} | {j.get('postedOn', '')} | {j.get('externalPath', '')}")
    with open("scratch/nvidia_bengaluru_business_roles.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)
