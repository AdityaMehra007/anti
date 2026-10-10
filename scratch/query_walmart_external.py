import urllib.request
import json

url = "https://walmart.wd504.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/jobs"

payload = {
    "appliedFacets": {},
    "limit": 20,
    "offset": 0,
    "searchText": "India"
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("SUCCESS!!!")
        print(f"Total jobs matching 'India': {data.get('total')}")
        facets = data.get('facets', [])
        for f in facets:
            fid = f.get('facetParameter')
            print(f"\nFacet {fid}:")
            for item in f.get('values', [])[:10]:
                print(f"  - {item.get('descriptor')} ({item.get('id')}): {item.get('count')}")
                
        with open("scratch/walmart_india_jobs.json", "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
except Exception as e:
    print("Error:", e)
