import urllib.request
import json

url = "https://walmart.wd504.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/jobs"
headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

payload = {"appliedFacets": {}, "limit": 20, "offset": 20, "searchText": "Bangalore"}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
with urllib.request.urlopen(req) as resp:
    d = json.loads(resp.read().decode('utf-8'))
    print("Offset 20 total:", d.get('total'))
    print("Offset 20 jobs count:", len(d.get('jobPostings', [])))
    print("Job titles:", [j.get('title') for j in d.get('jobPostings', [])[:5]])
