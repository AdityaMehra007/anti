import json

with open("scratch/meesho_all_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

blr_jobs = [j for j in jobs if "Bangalore" in j.get('categories', {}).get('location', '')]
print(f"Total Bangalore jobs: {len(blr_jobs)}")

# Group by department and print titles and IDs
depts = {}
for j in blr_jobs:
    d = j.get('categories', {}).get('department', 'Other')
    depts.setdefault(d, []).append(j)

for d, jlist in sorted(depts.items()):
    print(f"\n=== Department: {d} ({len(jlist)} jobs) ===")
    for j in jlist:
        title = j.get('text', '')
        jid = j.get('id', '')
        team = j.get('categories', {}).get('team', '')
        url = j.get('hostedUrl', '')
        print(f"  - [{jid}] {title} | Team: {team} | {url}")

with open("scratch/meesho_bangalore_jobs.json", "w", encoding="utf-8") as f:
    json.dump(blr_jobs, f, indent=2)
