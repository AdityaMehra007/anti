import json
import re

with open("scratch/lowes_ddo_raw.js", "r", encoding="utf-8") as f:
    content = f.read()

# It starts with "phApp.ddo = "
prefix = "phApp.ddo = "
idx = content.find(prefix)
if idx != -1:
    raw_json = content[idx + len(prefix):].strip()
    if raw_json.endswith(";"):
        raw_json = raw_json[:-1].strip()
        
    try:
        data = json.loads(raw_json)
        print("Success! Keys in phApp.ddo:", list(data.keys()))
        with open("scratch/lowes_ddo_parsed.json", "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
            
        for k in data:
            print(f"\nDDO Key: {k}")
            d = data[k]
            if isinstance(d, dict) and "data" in d:
                sub = d["data"]
                if isinstance(sub, dict):
                    print("  Subdata keys:", list(sub.keys())[:10])
                    if "totalHits" in sub:
                        print("  totalHits:", sub["totalHits"])
                    if "jobs" in sub:
                        jobs = sub["jobs"]
                        print(f"  JOBS COUNT: {len(jobs)}")
                        for j in jobs:
                            print(f"    - [{j.get('reqId')}] {j.get('title')} | {j.get('city')}, {j.get('state')} | Type: {j.get('type')}")
    except Exception as e:
        print("JSON parse error:", e)
        # Search for jobs array inside
        matches = re.findall(r'\"reqId\":\"([^\"]+)\"[^}]*\"title\":\"([^\"]+)\"', raw_json)
        print("Matches via regex:", len(matches))
        for m in matches[:10]:
            print(" ", m)
