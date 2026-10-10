import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://careers.adobe.com/widgets"
payload = {
    "lang": "en_us",
    "deviceType": "desktop",
    "country": "us",
    "pageName": "search-results",
    "ddoKey": "eagerLoadRefineSearch",
    "cityFacet": ["Bangalore"],
    "from": 0,
    "size": 50
}

data = json.dumps(payload).encode('utf-8')
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

req = urllib.request.Request(url, data=data, headers=headers)
with urllib.request.urlopen(req, context=ctx) as resp:
    res = json.loads(resp.read().decode('utf-8'))

el = res.get("eagerLoadRefineSearch", {})
jobs = el.get("data", {}).get("jobs", [])
print(f"Total jobs returned from API: {len(jobs)}")
with open("scratch/adobe_bangalore_all_jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

for j in jobs[:20]:
    print(f"[{j.get('jobId')}] {j.get('title')} | {j.get('category')} | {j.get('experienceLevel', '')}")
