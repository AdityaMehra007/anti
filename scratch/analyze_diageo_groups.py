import csv
from collections import defaultdict

with open("diageo_bengaluru_jobs.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    jobs = list(reader)

print(f"Total Bangalore jobs: {len(jobs)}\n")

by_group = defaultdict(list)
for j in jobs:
    group = j["job_family_group"] or "Other"
    by_group[group].append(j)

for group, glist in sorted(by_group.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n### {group} ({len(glist)} Openings)")
    for j in glist:
        print(f"  - [{j['reference_id']}] {j['job_title']} | Level: {j['management_level']} | Subtype: {j['function_subtype']}")
        print(f"    URL: {j['workday_apply_url']}")
