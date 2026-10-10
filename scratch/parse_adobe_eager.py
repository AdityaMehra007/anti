import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://careers.adobe.com/us/en/search-results?qcity=Bangalore&qstate=Karn%C4%81taka&qcountry=India"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

ddo = re.findall(r'phApp\.ddo\s*=\s*({.*?});', html, re.DOTALL)
if ddo:
    d = json.loads(ddo[0])
    el = d.get('eagerLoadRefineSearch', {})
    print("eagerLoadRefineSearch keys:", list(el.keys()))
    data = el.get('data', {})
    if isinstance(data, dict):
        print("data keys:", list(data.keys()))
        jobs = data.get('jobs', [])
        print(f"Found {len(jobs)} jobs in eagerLoadRefineSearch!")
        for j in jobs[:15]:
            print(f"[{j.get('jobId')}] {j.get('title')} | {j.get('type')} | {j.get('category')}")
        with open("scratch/adobe_eager_jobs.json", "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2)
