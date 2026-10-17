import json

with open('verified_fresher_accenture_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

by_cat = {}
for j in jobs:
    by_cat.setdefault(j['category'], []).append(j)

for cat in ['Procurement & Supply Chain Operations', 'Sales & Commercial Operations', 'Trust & Safety, AI & Content Operations', 'Project Management (PMO) & Tech Operations']:
    if cat in by_cat:
        print(f"=== {cat} ({len(by_cat[cat])} jobs) ===")
        for j in by_cat[cat]:
            print(f"  * {j['title']} | ID: {j['req_id']} | Posted: {j['posted']}")
            print(f"    URL: {j['link']}")
