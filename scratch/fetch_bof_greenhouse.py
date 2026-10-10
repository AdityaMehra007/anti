import urllib.request
import ssl
import json

ctx = ssl._create_unverified_context()
url = "https://boards-api.greenhouse.io/v1/boards/businessoffashion/jobs"
headers = {"User-Agent": "Mozilla/5.0"}

req = urllib.request.Request(url, headers=headers)
try:
    res = urllib.request.urlopen(req, context=ctx)
    print("STATUS:", res.status)
    data = json.loads(res.read().decode("utf-8"))
    jobs = data.get("jobs", [])
    print(f"Total BoF internal jobs: {len(jobs)}")
    for j in jobs:
        print(f"  - [{j.get('id')}] {j.get('title')} | Location: {j.get('location', {}).get('name')}")
        print(f"    URL: {j.get('absolute_url')}")
    with open("scratch/bof_internal_jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)
except Exception as e:
    print("ERROR:", e)
