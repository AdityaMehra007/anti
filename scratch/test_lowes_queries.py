import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

for query in ["fresher", "intern", "associate", "analyst", "graduate"]:
    url = f"https://talent.lowes.com/in/en/search-results?keywords={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            pos = html.find("phApp.ddo =")
            if pos != -1:
                raw = html[pos + len("phApp.ddo = "):]
                decoder = json.JSONDecoder()
                obj, _ = decoder.raw_decode(raw)
                eager = obj.get("eagerLoadRefineSearch", {}).get("data", {})
                jobs = eager.get("jobs", [])
                print(f"Query '{query}': {len(jobs)} jobs returned (totalHits: {eager.get('totalHits')})")
                for j in jobs[:3]:
                    print(f"  - [{j.get('reqId')}] {j.get('title')} ({j.get('city')})")
    except Exception as e:
        print(f"Error for '{query}': {e}")
