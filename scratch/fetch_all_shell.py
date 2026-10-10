import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://shell.wd3.myworkdayjobs.com/wday/cxs/shell/shellcareers/jobs"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

all_jobs = []
for offset in [0, 20]:
    payload = {
        "appliedFacets": {
            "locationCountry": ["c4f78be1a8f14da0ab49ce1162348a5e"]
        },
        "limit": 20,
        "offset": offset,
        "searchText": ""
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        postings = data.get('jobPostings', [])
        all_jobs.extend(postings)
        print(f"Offset {offset}: got {len(postings)} jobs (accumulated {len(all_jobs)})")

print(f"Total jobs: {len(all_jobs)}")

with open("scratch/shell_all_india_jobs.json", "w", encoding="utf-8") as out:
    json.dump(all_jobs, out, indent=2)

with open("scratch/shell_jobs_summary.txt", "w", encoding="utf-8") as out:
    for idx, j in enumerate(all_jobs, 1):
        req_id = j.get('bulletFields', [''])[0] if j.get('bulletFields') else ''
        title = j.get('title')
        loc = j.get('locationsText')
        path = j.get('externalPath')
        url = f"https://shell.wd3.myworkdayjobs.com/en-US/shellcareers{path}"
        out.write(f"{idx}. [{req_id}] {title}\n")
        out.write(f"   Location: {loc}\n")
        out.write(f"   URL: {url}\n\n")

print("Saved scratch/shell_jobs_summary.txt successfully!")
