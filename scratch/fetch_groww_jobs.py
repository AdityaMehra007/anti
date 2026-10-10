import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://boards-api.eu.greenhouse.io/v1/boards/groww/jobs?content=true",
    "https://boards-api.greenhouse.io/v1/boards/groww/jobs?content=true"
]

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            jobs = data.get("jobs", [])
            print(f"SUCCESS at {url}!")
            print(f"Total live Groww jobs: {len(jobs)}")
            with open("scratch/groww_all_jobs.json", "w", encoding="utf-8") as f:
                json.dump(jobs, f, indent=2)
                
            depts = {}
            offices = {}
            for j in jobs:
                for d in j.get("departments", []):
                    depts[d.get("name")] = depts.get(d.get("name"), 0) + 1
                for o in j.get("offices", []):
                    offices[f"{o.get('name')} ({o.get('id')})"] = offices.get(f"{o.get('name')} ({o.get('id')})", 0) + 1
                    
            print("\n--- Departments ---")
            for d, count in sorted(depts.items(), key=lambda x: -x[1])[:15]:
                print(f"{d}: {count}")
                
            print("\n--- Offices ---")
            for o, count in sorted(offices.items(), key=lambda x: -x[1]):
                print(f"{o}: {count}")
                
            print("\n--- Sample 20 Jobs ---")
            for j in jobs[:20]:
                bullet = j.get("id")
                title = j.get("title")
                loc = j.get("location", {}).get("name", "")
                dept_names = [d.get("name") for d in j.get("departments", [])]
                office_ids = [o.get("id") for o in j.get("offices", [])]
                print(f"[{bullet}] {title} | Dept: {dept_names} | OfficeIDs: {office_ids} | Loc: {loc}")
            break
    except Exception as e:
        print(f"Failed at {url}: {e}")
