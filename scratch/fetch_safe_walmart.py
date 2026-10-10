import urllib.request
import json
import sys

sys.stdout.reconfigure(line_buffering=True)

url = "https://walmart.wd504.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/jobs"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

all_jobs = []
for offset in [0, 20, 40, 60, 80, 100]:
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

print(f"Collected total: {len(all_jobs)}")
with open("scratch/walmart_blr_sample_jobs.json", "w", encoding="utf-8") as out:
    json.dump(all_jobs, out, indent=2)
