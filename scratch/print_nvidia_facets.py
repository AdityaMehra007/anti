import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json"
}

payload = {
    "appliedFacets": {},
    "limit": 1,
    "offset": 0,
    "searchText": "Bengaluru"
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
with urllib.request.urlopen(req, context=ctx) as resp:
    res = json.loads(resp.read().decode('utf-8'))

for facet in res.get("facets", []):
    print("Facet:", facet.get("facetParameter"))
    for v in facet.get("values", []):
        print(f"   {v.get('descriptor')} ({v.get('count')}) -> id: {v.get('id')}")
