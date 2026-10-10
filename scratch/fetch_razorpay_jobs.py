import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://boards-api.greenhouse.io/v1/boards/razorpaysoftwareprivatelimited/jobs?content=true"
headers = {'User-Agent': 'Mozilla/5.0'}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        jobs = data.get("jobs", [])
        print(f"Total live Razorpay jobs: {len(jobs)}")
        
        with open("scratch/razorpay_all_jobs.json", "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2)
            
        # check departments and offices
        depts = {}
        for j in jobs:
            for d in j.get("departments", []):
                name = d.get("name", "Unknown")
                depts[name] = depts.get(name, 0) + 1
                
        print("\n--- Departments ---")
        for d, count in sorted(depts.items(), key=lambda x: -x[1]):
            print(f"{d}: {count}")
            
        print("\n--- Sample 20 Jobs ---")
        for j in jobs[:20]:
            bullet = j.get("id")
            title = j.get("title")
            loc = j.get("location", {}).get("name", "")
            dept_names = [d.get("name") for d in j.get("departments", [])]
            print(f"[{bullet}] {title} | Dept: {dept_names} | Loc: {loc}")
except Exception as e:
    print(f"Error fetching Razorpay Greenhouse jobs: {e}")
