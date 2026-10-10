import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

all_corporate_jobs = []

for offset in [0, 10, 20, 30]:
    url = f"https://talent.lowes.com/in/en/c/corporate-jobs?from={offset}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            pos = html.find("phApp.ddo =")
            if pos != -1:
                prefix = "phApp.ddo = "
                idx = html.find(prefix, pos)
                if idx != -1:
                    raw = html[idx + len(prefix):]
                    decoder = json.JSONDecoder()
                    obj, _ = decoder.raw_decode(raw)
                    eager = obj.get("eagerLoadRefineSearch", {}).get("data", {})
                    jobs = eager.get("jobs", [])
                    print(f"Offset {offset}: got {len(jobs)} jobs (totalHits: {eager.get('totalHits')})")
                    for j in jobs:
                        all_corporate_jobs.append(j)
    except Exception as e:
        print(f"Error at offset {offset}: {e}")

print(f"\nTotal corporate jobs collected: {len(all_corporate_jobs)}")

# Deduplicate by reqId
seen = set()
unique_jobs = []
for j in all_corporate_jobs:
    rid = j.get('reqId')
    if rid not in seen:
        seen.add(rid)
        unique_jobs.append(j)

print(f"Unique corporate jobs: {len(unique_jobs)}")
with open("scratch/lowes_all_corporate_unique.json", "w", encoding="utf-8") as out:
    json.dump(unique_jobs, out, indent=2)

print("Saved scratch/lowes_all_corporate_unique.json successfully!")
