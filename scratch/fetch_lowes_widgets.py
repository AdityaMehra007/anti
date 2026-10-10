import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/lowes_ddo_clean.json", "r", encoding="utf-8") as f:
    ddo = json.load(f)

eager = ddo.get("eagerLoadRefineSearch", {}).get("data", {})
print("totalHits:", eager.get("totalHits"))
print("First page jobs:", len(eager.get("jobs", [])))

# Let's inspect aggregations
agg = eager.get("aggregations", [])
print(f"Aggregations: {len(agg)}")
for a in agg:
    print(f"  Field: {a.get('field')}")
    for val in a.get('values', [])[:5]:
        print(f"    - {val.get('value')} ({val.get('count')})")

# Let's query https://talent.lowes.com/widgets to fetch all 31 jobs!
url = "https://talent.lowes.com/widgets"
payload = {
    "lang": "en_in",
    "deviceType": "desktop",
    "country": "in",
    "pageName": "category",
    "ddoKey": "refineSearch",
    "sortBy": "",
    "subLocation": "",
    "from": 0,
    "size": 50,
    "categories": ["corporate-jobs"]
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("\nSuccess querying widgets API!")
        print("Widget response keys:", list(res.keys()))
        data = res.get("refineSearch", {}).get("data", {})
        jobs = data.get("jobs", [])
        print(f"Total jobs returned from widgets: {len(jobs)}")
        with open("scratch/lowes_all_jobs.json", "w", encoding="utf-8") as out:
            json.dump(jobs, out, indent=2)
except Exception as e:
    print("Error querying widgets:", e)
