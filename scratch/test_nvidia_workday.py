import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Test NVIDIA Workday endpoint
urls = [
    "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs",
    "https://nvidia.wd1.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"
]

for url in urls:
    payload = {
        "appliedFacets": {},
        "limit": 20,
        "offset": 0,
        "searchText": "Bangalore"
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            print(f"SUCCESS at {url}!")
            print(f"Total jobs for Bangalore: {res.get('total')}")
            for j in res.get("jobPostings", [])[:5]:
                bullet = j.get("bulletFields", ["NO_ID"])
                print(f"[{bullet[0]}] {j.get('title')} | {j.get('locationsText')}")
            with open("scratch/nvidia_bangalore_jobs.json", "w", encoding="utf-8") as f:
                json.dump(res, f, indent=2)
            break
    except Exception as e:
        print(f"Failed at {url}: {e}")
