import urllib.request
import json
import sys

sys.stdout.reconfigure(line_buffering=True)

with open("scratch/walmart_blr_sample_jobs.json", "r", encoding="utf-8") as f:
    all_jobs = json.load(f)

url = "https://walmart.wd504.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/jobs"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

for offset in [120, 140, 160, 180, 200]:
    payload = {
        "appliedFacets": {},
        "limit": 20,
        "offset": offset,
        "searchText": "Bangalore"
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            postings = data.get('jobPostings', [])
            if not postings:
                print(f"Empty at offset {offset}")
                break
            all_jobs.extend(postings)
            print(f"Offset {offset}: got {len(postings)} jobs (total {len(all_jobs)})")
    except Exception as e:
        print(f"Error at offset {offset}: {e}")
        break

print(f"Grand Total collected: {len(all_jobs)}")

# Deduplicate by externalPath
seen = set()
unique_jobs = []
for j in all_jobs:
    path = j.get('externalPath')
    if path not in seen:
        seen.add(path)
        unique_jobs.append(j)

print(f"Unique jobs count: {len(unique_jobs)}")
with open("scratch/walmart_bangalore_all_unique_jobs.json", "w", encoding="utf-8") as out:
    json.dump(unique_jobs, out, indent=2)

print("Saved scratch/walmart_bangalore_all_unique_jobs.json successfully!")
