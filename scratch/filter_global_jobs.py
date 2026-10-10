import json

with open('e:/anti/scratch/jobspresso_targeted_harvest.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total jobs evaluated: {len(jobs)}")
count = 0
for j in jobs:
    loc = j['location'].lower()
    if 'india' in loc or 'worldwide' in loc or 'anywhere' in loc or 'various countries' in loc or 'apac' in loc or 'asia' in loc:
        count += 1
        print(f"[{count}] [{j['company']}] {j['title']} | Loc: {j['location']} | Cat: {j['categories']} | URL: {j['url']}")
