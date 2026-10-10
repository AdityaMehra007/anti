import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://careers.adobe.com/widgets"
payload = {
    "lang": "en_us",
    "deviceType": "desktop",
    "country": "us",
    "pageName": "search-results",
    "ddoKey": "refineSearch",
    "cityFacet": ["Bangalore"],
    "from": 0,
    "size": 25
}

data = json.dumps(payload).encode('utf-8')
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

req = urllib.request.Request(url, data=data, headers=headers)
with urllib.request.urlopen(req, context=ctx) as resp:
    res = json.loads(resp.read().decode('utf-8'))

ref = res.get("refineSearch", {})
print("refineSearch keys:", list(ref.keys()))
d = ref.get("data", {})
if isinstance(d, dict):
    print("data keys:", list(d.keys()))
    jobs = d.get("jobs", [])
    print("jobs length in data:", len(jobs))
    if not jobs:
        # check other fields
        for k, v in d.items():
            if isinstance(v, list) and len(v) > 0:
                print(f"Key {k} has list of len {len(v)}")
                print("First element:", v[0] if isinstance(v[0], dict) else str(v[0])[:100])
