import json

with open('e:/anti/scratch/jobspresso_resolved_deep.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total resolved jobs: {len(jobs)}")
for i, j in enumerate(jobs):
    print(f"[{i+1}] {j['company']} - {j['title']} | Loc: {j['location']} | Apply: {j['direct_apply_url']}")
