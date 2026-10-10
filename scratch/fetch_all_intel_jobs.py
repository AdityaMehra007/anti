import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

all_jobs = []
for offset in [0, 20, 40]:
    payload = {
        "appliedFacets": {
            "locations": ["1e4a4eb3adf101f44070f976bf8184cf"]
        },
        "limit": 20,
        "offset": offset,
        "searchText": ""
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            jobs = res.get("jobPostings", [])
            all_jobs.extend(jobs)
    except Exception as e:
        print(f"Error at offset {offset}: {e}")

print(f"Total jobs collected: {len(all_jobs)}")
with open("scratch/intel_bangalore_all_58_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2)

for idx, j in enumerate(all_jobs, 1):
    bullet = j.get("bulletFields", ["NO_ID"])
    print(f"{idx}. [{bullet[0]}] {j.get('title')} (Posted: {j.get('postedOn', '')})")
