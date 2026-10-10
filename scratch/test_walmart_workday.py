import urllib.request
import json

url = "https://walmart.wd504.myworkdayjobs.com/wday/cxs/walmart/Walmart_External_Careers/jobs"

payload = {
    "appliedFacets": {
        "locationCountry": ["bc33aa3152ec42d49cf5f4d92416f461"]
    },
    "limit": 20,
    "offset": 0,
    "searchText": ""
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Success!")
        print(f"Total India Jobs: {data.get('total')}")
        facets = data.get('facets', [])
        for f in facets:
            facet_id = f.get('facetParameter')
            if facet_id in ['locations', 'jobFamilyGroup']:
                print(f"\nFacet {facet_id}:")
                for item in f.get('values', [])[:10]:
                    print(f"  - {item.get('descriptor')} ({item.get('id')}): {item.get('count')}")
        
        print("\nSample India Jobs:")
        for j in data.get('jobPostings', [])[:5]:
            print(f"  - [{j.get('bulletFields', [''])[0]}] {j.get('title')} ({j.get('locationsText')})")
            print(f"    URL: https://walmart.wd504.myworkdayjobs.com/Walmart_External_Careers{j.get('externalPath')}")

        with open("scratch/walmart_india_sample.json", "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
except Exception as e:
    print("Error querying Walmart Workday API:", e)
