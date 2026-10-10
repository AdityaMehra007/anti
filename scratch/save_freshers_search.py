import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://talent.lowes.com/in/en/search-results?keywords=FRESHERS%204"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

pos = html.find("phApp.ddo =")
if pos != -1:
    raw = html[pos + len("phApp.ddo = "):]
    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(raw)
    eager = obj.get("eagerLoadRefineSearch", {}).get("data", {})
    with open("scratch/lowes_freshers_search.json", "w", encoding="utf-8") as out:
        json.dump(eager, out, indent=2)
    print("Saved scratch/lowes_freshers_search.json successfully!")
    jobs = eager.get("jobs", [])
    print(f"Total jobs: {len(jobs)}")
    for idx, j in enumerate(jobs, 1):
        print(f"{idx}. [{j.get('reqId')}] {j.get('title')} | {j.get('city')}, {j.get('state')}")
        print(f"   URL: https://talent.lowes.com/in/en/job/{j.get('jobId')}")
        print(f"   Teaser: {j.get('descriptionTeaser', '')[:200]}")
