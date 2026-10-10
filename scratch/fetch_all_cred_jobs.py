import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. From Next data
with open("scratch/cred_next_data.json", encoding="utf-8") as f:
    d = json.load(f)

page_jobs = d['props']['pageProps']['data']['data']
print(f"Jobs from page data: {len(page_jobs)}")
for j in page_jobs:
    print(f"[{j.get('id')}] {j.get('text')} | Team: {j.get('categories', {}).get('team')} | Loc: {j.get('categories', {}).get('location')}")
    print(f"   Apply: {j.get('urls', {}).get('apply')}")

# 2. Check Lever public API
url = "https://api.lever.co/v0/postings/cred?mode=json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        lever_jobs = json.loads(resp.read().decode('utf-8'))
        print(f"\nJobs from Lever API: {len(lever_jobs)}")
        with open("scratch/cred_lever_jobs.json", "w", encoding="utf-8") as f:
            json.dump(lever_jobs, f, indent=2)
        for j in lever_jobs:
            print(f"[{j.get('id')}] {j.get('text')} | Team: {j.get('categories', {}).get('team')} | Loc: {j.get('categories', {}).get('location')}")
except Exception as e:
    print(f"Lever API error: {e}")
