import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

all_jobs = []
seen = set()

# Iterate pages 0, 10, 20, 30, 40
for offset in [0, 10, 20, 30, 40]:
    url = f"https://careers.adobe.com/us/en/search-results?qcity=Bangalore&qstate=Karn%C4%81taka&qcountry=India&from={offset}&s=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            ddo = re.findall(r'phApp\.ddo\s*=\s*({.*?});', html, re.DOTALL)
            if ddo:
                d = json.loads(ddo[0])
                jobs = d.get('eagerLoadRefineSearch', {}).get('data', {}).get('jobs', [])
                for j in jobs:
                    jid = j.get('jobId')
                    if jid not in seen:
                        seen.add(jid)
                        all_jobs.append(j)
        print(f"Offset {offset}: Total unique collected so far = {len(all_jobs)}")
    except Exception as e:
        print(f"Offset {offset} error: {e}")

print(f"\nFinal count of collected jobs: {len(all_jobs)}")
with open("scratch/adobe_bangalore_live_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2)

for j in all_jobs[:25]:
    print(f"[{j.get('jobId')}] {j.get('title')} | {j.get('category')} | {j.get('type')}")
