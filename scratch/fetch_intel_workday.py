import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs"
payload = {
    "appliedFacets": {
        "locations": ["1e4a4eb3adf101f44070f976bf8184cf"]
    },
    "limit": 20,
    "offset": 0,
    "searchText": ""
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)

try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        total = res.get("total")
        print(f"Total Intel Bangalore Jobs: {total}")
        job_postings = res.get("jobPostings", [])
        print(f"Returned {len(job_postings)} jobs in first page")
        
        with open("scratch/intel_bangalore_jobs.json", "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)
            
        for job in job_postings:
            bullet_fields = job.get("bulletFields", [])
            print(f"[{bullet_fields[0] if bullet_fields else 'NO_ID'}] {job.get('title')} | {job.get('locationsText')}")
except Exception as e:
    print(f"Error querying Intel Workday API: {e}")
