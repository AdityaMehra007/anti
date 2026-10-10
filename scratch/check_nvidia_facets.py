import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# Search with "Bengaluru"
payload1 = {
    "appliedFacets": {},
    "limit": 20,
    "offset": 0,
    "searchText": "Bengaluru"
}
req1 = urllib.request.Request(url, data=json.dumps(payload1).encode('utf-8'), headers=headers)
with urllib.request.urlopen(req1, context=ctx) as resp:
    res1 = json.loads(resp.read().decode('utf-8'))
    print(f"Total jobs with 'Bengaluru': {res1.get('total')}")

# Search with "India"
payload2 = {
    "appliedFacets": {},
    "limit": 20,
    "offset": 0,
    "searchText": "India"
}
req2 = urllib.request.Request(url, data=json.dumps(payload2).encode('utf-8'), headers=headers)
with urllib.request.urlopen(req2, context=ctx) as resp:
    res2 = json.loads(resp.read().decode('utf-8'))
    print(f"Total jobs with 'India': {res2.get('total')}")
    facets = res2.get("facets", [])
    for f in facets:
        print(f"Facet: {f.get('facetParameter')}")
        if f.get('facetParameter') == 'locationHierarchy1':
            for v in f.get('values', [])[:10]:
                print(f"  {v.get('descriptor')} -> {v.get('id')} ({v.get('count')})")
