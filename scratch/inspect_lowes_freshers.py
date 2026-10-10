import urllib.request
import json
import re

url = "https://talent.lowes.com/in/en/search-results?keywords=FRESHERS%204"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Status: {resp.status}, HTML length: {len(html)}")
        
        pos = html.find("phApp.ddo =")
        if pos != -1:
            raw = html[pos + len("phApp.ddo = "):]
            decoder = json.JSONDecoder()
            obj, _ = decoder.raw_decode(raw)
            eager = obj.get("eagerLoadRefineSearch", {}).get("data", {})
            total_hits = eager.get("totalHits")
            jobs = eager.get("jobs", [])
            print(f"totalHits for 'FRESHERS 4': {total_hits}")
            print(f"Jobs returned: {len(jobs)}")
            for j in jobs:
                print(f"  - [{j.get('reqId')}] {j.get('title')} | {j.get('city')}, {j.get('state')}")
                print(f"    URL: https://talent.lowes.com/in/en/job/{j.get('jobId')}")
                print(f"    Teaser: {j.get('descriptionTeaser', '')[:200]}")
            with open("scratch/lowes_freshers_search.json", "w", encoding="utf-8") as out:
                json.dump(eager, out, indent=2)
        else:
            print("No phApp.ddo found in HTML")
            with open("scratch/lowes_freshers_page.html", "w", encoding="utf-8") as out:
                out.write(html)
except Exception as e:
    print("Error:", e)
