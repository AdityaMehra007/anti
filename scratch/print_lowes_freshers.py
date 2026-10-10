import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/lowes_freshers_search.json", "r", encoding="utf-8") as f:
    eager = json.load(f)

jobs = eager.get("jobs", [])
print(f"Total jobs returned for FRESHERS 4: {len(jobs)}\n")

for idx, j in enumerate(jobs, 1):
    req_id = j.get('reqId', '')
    title = j.get('title', '')
    city = j.get('city', '')
    state = j.get('state', '')
    country = j.get('country', '')
    job_id = j.get('jobId', '')
    url = f"https://talent.lowes.com/in/en/job/{job_id}"
    teaser = j.get('descriptionTeaser', '').strip()
    
    print(f"{idx}. [{req_id}] {title}")
    print(f"   Location: {city}, {state}, {country}")
    print(f"   URL: {url}")
    print(f"   Snippet: {teaser[:300]}")
    print("-" * 60)
