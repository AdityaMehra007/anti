import urllib.request
import json
import time

url = "https://walmart.wd504.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/jobs"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

all_jobs = []
limit = 20
offset = 0

print("Fetching all Bangalore jobs from Walmart Workday...")
while True:
    payload = {
        "appliedFacets": {},
        "limit": limit,
        "offset": offset,
        "searchText": "Bangalore"
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            postings = data.get('jobPostings', [])
            if not postings:
                print(f"No more postings at offset {offset}. Done!")
                break
            all_jobs.extend(postings)
            print(f"Fetched offset {offset}: {len(postings)} jobs (accumulated {len(all_jobs)})")
            offset += limit
            time.sleep(0.4)
    except Exception as e:
        print(f"Error at offset {offset}: {e}")
        break

print(f"\nTotal jobs successfully collected: {len(all_jobs)}")

with open("scratch/walmart_bangalore_all_208_jobs.json", "w", encoding="utf-8") as out:
    json.dump(all_jobs, out, indent=2)

print("Saved scratch/walmart_bangalore_all_208_jobs.json")
