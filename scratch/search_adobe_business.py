import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

keywords = ["Associate", "Operations", "Finance", "Sales", "Analyst", "Marketing", "Business", "Customer", "Specialist"]
business_jobs = []
seen = set()

for kw in keywords:
    url = f"https://careers.adobe.com/us/en/search-results?keywords={kw}&qcity=Bangalore&qstate=Karn%C4%81taka&qcountry=India&s=1"
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
                        business_jobs.append(j)
    except Exception as e:
        print(f"Error {kw}: {e}")

print(f"Total business/ops/sales/analyst jobs collected: {len(business_jobs)}")
with open("scratch/adobe_bangalore_business_roles.json", "w", encoding="utf-8") as f:
    json.dump(business_jobs, f, indent=2)

for j in business_jobs:
    print(f"[{j.get('jobId')}] {j.get('title')} | {j.get('category')}")
