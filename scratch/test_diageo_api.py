import urllib.request
import ssl
import json

ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

url = "https://diageo-prod-api.connectid.cloud/api/jobs?country=India&page=1"
print(f"Testing URL: {url}")

try:
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req, context=ctx)
    print("STATUS:", res.status)
    body = res.read().decode("utf-8")
    data = json.loads(body)
    print("KEYS:", list(data.keys()))
    meta = data.get("meta", {})
    print("META:", meta)
    facets = data.get("facets", {})
    print("FACET KEYS:", list(facets.keys()))
    if "location" in facets:
        print("LOCATIONS:", facets["location"])
    if "country" in facets:
        print("COUNTRIES:", facets["country"])
    jobs = data.get("data", [])
    print(f"JOBS on page 1: {len(jobs)}")
    with open("scratch/diageo_india_page1.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Saved scratch/diageo_india_page1.json")
except Exception as e:
    print("ERROR:", e)
