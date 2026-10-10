import json
import re

with open("scratch/lowes_page.html", "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r'phApp\.ddo\s*=\s*({.*?});\s*<\/script>', html, re.S)
if m:
    data = json.loads(m.group(1))
    print("phApp.ddo keys:", list(data.keys()))
    with open("scratch/lowes_ddo.json", "w", encoding="utf-8") as out:
        json.dump(data, out, indent=2)
    print("Saved scratch/lowes_ddo.json")
    for k in data:
        print(f"Key {k}: status={data[k].get('status')}")
        if "data" in data[k]:
            subdata = data[k]["data"]
            if isinstance(subdata, dict):
                print(f"  subdata keys: {list(subdata.keys())[:10]}")
                if "jobs" in subdata:
                    jobs = subdata["jobs"]
                    print(f"  FOUND {len(jobs)} JOBS in ddo[{k}]['data']['jobs']!")
                    for j in jobs[:5]:
                        print(f"    - [{j.get('jobId')}] {j.get('title')} | {j.get('city')}, {j.get('state')} | reqId: {j.get('reqId')}")
else:
    print("No ddo match found")
