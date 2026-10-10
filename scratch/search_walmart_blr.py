import urllib.request
import json

url = "https://walmart.wd504.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/jobs"

payload = {
    "appliedFacets": {},
    "limit": 20,
    "offset": 0,
    "searchText": "Bangalore"
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"Total Bangalore jobs in Walmart Workday: {data.get('total')}")
        print("\nFirst 10 Bangalore Jobs:")
        for j in data.get('jobPostings', [])[:10]:
            print(f"- {j.get('title')} | {j.get('locationsText')}")
            print(f"  URL: https://walmart.wd504.myworkdayjobs.com/en-US/WalmartExternal{j.get('externalPath')}")
        with open("scratch/walmart_bangalore_jobs.json", "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
except Exception as e:
    print("Error:", e)
