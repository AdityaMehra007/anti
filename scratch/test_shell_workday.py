import urllib.request
import json

url = "https://shell.wd3.myworkdayjobs.com/wday/cxs/shell/shellcareers/jobs"

payload = {
    "appliedFacets": {
        "locationCountry": ["c4f78be1a8f14da0ab49ce1162348a5e"]
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
        print("Success querying Shell Workday API!")
        print(f"Total India Jobs: {data.get('total')}")
        
        facets = data.get('facets', [])
        for f in facets:
            fid = f.get('facetParameter')
            print(f"\nFacet {fid}:")
            for item in f.get('values', [])[:10]:
                print(f"  - {item.get('descriptor')} ({item.get('id')}): {item.get('count')}")
                
        print("\nSample Jobs (First 5):")
        for j in data.get('jobPostings', [])[:5]:
            req_id = j.get('bulletFields', [''])[0] if j.get('bulletFields') else ''
            print(f"  - [{req_id}] {j.get('title')} ({j.get('locationsText')})")
            print(f"    URL: https://shell.wd3.myworkdayjobs.com/en-US/shellcareers{j.get('externalPath')}")

        with open("scratch/shell_india_page1.json", "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
            
except Exception as e:
    print("Error querying Shell Workday API:", e)
