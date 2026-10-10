import json

with open("scratch/lowes_ddo_raw.js", "r", encoding="utf-8") as f:
    content = f.read()

prefix = "phApp.ddo = "
idx = content.find(prefix)
if idx != -1:
    raw = content[idx + len(prefix):]
    decoder = json.JSONDecoder()
    obj, end_idx = decoder.raw_decode(raw)
    print("Parsed JSON successfully using raw_decode!")
    print("Keys in DDO:", list(obj.keys()))
    with open("scratch/lowes_ddo_clean.json", "w", encoding="utf-8") as out:
        json.dump(obj, out, indent=2)
    
    for k in obj:
        print(f"\nDDO Key: {k}")
        d = obj[k]
        if isinstance(d, dict) and "data" in d:
            sub = d["data"]
            if isinstance(sub, dict):
                print("  Subdata keys:", list(sub.keys())[:10])
                if "totalHits" in sub:
                    print(f"  totalHits: {sub['totalHits']}")
                if "jobs" in sub:
                    jobs = sub["jobs"]
                    print(f"  JOBS COUNT in this page: {len(jobs)}")
                    for j in jobs:
                        print(f"    - [{j.get('reqId')}] {j.get('title')}")
                        print(f"      Location: {j.get('city')}, {j.get('state')} | Category: {j.get('category')} | Subcat: {j.get('subCategory')}")
                        print(f"      Apply URL: {j.get('applyUrl') or j.get('jobUrl') or ('https://talent.lowes.com/in/en/job/' + j.get('jobId', ''))}")
