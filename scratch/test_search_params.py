import urllib.request
import ssl
import json

ctx = ssl._create_unverified_context()

tests = [
    "page=1&size=50",
    "page=0&size=50",
    "offset=0&limit=50",
    "pageNo=1&pageSize=50",
    "pageNo=0&pageSize=50",
    "from=0&size=50",
    "start=0&rows=50",
    "searchQuery=",
    "query=",
    "keyword=",
    "q=",
    "all=true",
    "city=bangalore",
    "cities=bangalore",
    "location=bangalore",
]

base = "https://io.spire2grow.com/ies/v1/p/requisition/aggregation/_search?"

for t in tests:
    url = base + t
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "workspaceId": "MYNTRA-93as3"
    })
    try:
        res = urllib.request.urlopen(req, context=ctx)
        data = json.loads(res.read().decode("utf-8"))
        entities = data.get("entities", [])
        total = len(entities)
        print(f"[{t}] STATUS: {res.status}, entities count: {total}")
        if total > 0:
            print("  FOUND FIRST ENTITY:", list(entities[0].keys()) if isinstance(entities[0], dict) else entities[0])
            with open("scratch/sample_myntra_job.json", "w", encoding="utf-8") as f:
                json.dump(entities[0], f, indent=2)
            break
    except Exception as e:
        print(f"[{t}] ERROR: {e}")
