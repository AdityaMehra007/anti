import urllib.request
import ssl
import json

ctx = ssl._create_unverified_context()

tests = [
    ("workspaceId", "https://io.spire2grow.com/ies/v1/p/workspaceId?domain=jobs.myntra.com", "GET", None),
    ("static-content", "https://io.spire2grow.com/ies/v1/p/workspace/static-content/MYNTRA-93as3", "GET", None),
    ("theme", "https://io.spire2grow.com/ies/v1/p/workspace/theme/MYNTRA-93as3", "GET", None),
    ("count", "https://io.spire2grow.com/ies/v1/p/requisition/_count", "GET", None),
    ("count_with_ws", "https://io.spire2grow.com/ies/v1/p/requisition/_count?workspaceId=MYNTRA-93as3", "GET", None),
    ("search_empty", "https://io.spire2grow.com/ies/v1/p/requisition/aggregation/_search?", "GET", None),
    ("search_with_ws", "https://io.spire2grow.com/ies/v1/p/requisition/aggregation/_search?workspaceId=MYNTRA-93as3", "GET", None),
]

for name, url, method, data in tests:
    print(f"\n--- TESTING: {name} ---")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "workspaceId": "MYNTRA-93as3",
        "X-Workspace-Id": "MYNTRA-93as3"
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    try:
        res = urllib.request.urlopen(req, context=ctx)
        print("STATUS:", res.status)
        body = res.read().decode("utf-8")
        print("RESPONSE (first 300 chars):", body[:300])
        with open(f"scratch/res_{name}.json", "w", encoding="utf-8") as out:
            out.write(body)
    except urllib.error.HTTPError as e:
        print(f"HTTP ERROR {e.code}: {e.read().decode('utf-8', errors='ignore')[:200]}")
    except Exception as e:
        print("ERROR:", e)
