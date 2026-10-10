import urllib.request
import ssl
import json

ctx = ssl._create_unverified_context()

url = "https://io.spire2grow.com/ies/v1/p/requisition/_search?page=1&size=50"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "workspaceId": "MYNTRA-93as3"
}

req = urllib.request.Request(url, headers=headers)
try:
    res = urllib.request.urlopen(req, context=ctx)
    print("STATUS:", res.status)
    body = res.read().decode("utf-8")
    data = json.loads(body)
    print("Keys in response:", list(data.keys()) if isinstance(data, dict) else type(data))
    if isinstance(data, dict):
        total = data.get("total", "N/A")
        entities = data.get("entities", [])
        print(f"Total: {total}, Entities count: {len(entities)}")
        with open("scratch/myntra_all_jobs.json", "w", encoding="utf-8") as f:
            f.write(body)
        print("Saved scratch/myntra_all_jobs.json")
    elif isinstance(data, list):
        print(f"List length: {len(data)}")
        with open("scratch/myntra_all_jobs.json", "w", encoding="utf-8") as f:
            f.write(body)
except Exception as e:
    print("ERROR:", e)
