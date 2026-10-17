import urllib.request
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers/jobs"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

search_terms = [
    "Bengaluru New Associate",
    "Bengaluru Associate",
    "Bengaluru Procurement",
    "Bengaluru Sales Operations",
    "Bengaluru Customer Service",
    "Bengaluru Operations",
    "Bengaluru Trust & Safety",
    "Bengaluru Compliance",
    "Bengaluru Program Project Management",
    "Bengaluru Application Support",
    "Bengaluru Supply Chain",
    "Bengaluru HR"
]

all_jobs = []
seen_paths = set()

for term in search_terms:
    for offset in [0, 20]:
        payload = {
            "appliedFacets": {"locationCountry": ["c4f78be1a8f14da0ab49ce1162348a5e"]},
            "limit": 20,
            "offset": offset,
            "searchText": term
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobPostings", []):
                    path = j.get("externalPath", "")
                    title = j.get("title", "")
                    # filter to relevant roles
                    if path not in seen_paths and "Bengaluru" in path:
                        seen_paths.add(path)
                        # Extract jobReqId from bulletFields or path
                        m = re.search(r'_([A-Z0-9\-]+)$', path)
                        req_id = m.group(1) if m else "ACN-REQ"
                        all_jobs.append({
                            "req_id": req_id,
                            "title": title,
                            "posted": j.get("postedOn", "Active"),
                            "path": path,
                            "link": f"https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers{path}"
                        })
        except Exception as e:
            print(f"Error {term} offset {offset}: {e}")

print(f"Total unique Bengaluru jobs collected: {len(all_jobs)}")

with open("e:/anti/mega_bengaluru_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2, ensure_ascii=False)
