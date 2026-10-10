import urllib.request
import json
import re

url = 'https://boeing.wd1.myworkdayjobs.com/wday/cxs/boeing/EXTERNAL_CAREERS/jobs'
payload = {
    'appliedFacets': {},
    'limit': 20,
    'offset': 0,
    'searchText': 'India'
}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

print(f"Total jobs returned for India: {data.get('total')}")
jobs = data.get('jobPostings', [])
for i, j in enumerate(jobs, 1):
    title = j.get('title', '')
    loc = j.get('locationsText', '')
    req = j.get('bulletFields', [''])[0]
    path = j.get('externalPath', '')
    clean_title = re.sub(r'[^\x00-\x7F]+', ' ', title).strip()
    clean_loc = re.sub(r'[^\x00-\x7F]+', ' ', loc).strip()
    print(f"{i}. [{req}] {clean_title} | {clean_loc}")
    print(f"   URL: https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS{path}")

with open('scratch/boeing_workday_india_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(jobs, f, indent=2)
print("Saved to scratch/boeing_workday_india_jobs.json")
