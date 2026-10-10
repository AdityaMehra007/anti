import json

with open('scratch/shell_jobs_detailed.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

blr_jobs = []
chn_jobs = []
multi_jobs = []

for j in jobs:
    loc = j['location']
    if 'Bangalore' in loc:
        blr_jobs.append(j)
    elif '2 Locations' in loc or 'Locations' in loc:
        multi_jobs.append(j)
    else:
        chn_jobs.append(j)

print(f"Bengaluru specific jobs ({len(blr_jobs)}):")
for j in blr_jobs:
    print(f"  - [{j['req']}] {j['title']} | {j['location']}")

print(f"\nMulti-location (Bangalore + Chennai) jobs ({len(multi_jobs)}):")
for j in multi_jobs:
    print(f"  - [{j['req']}] {j['title']} | {j['location']}")

print(f"\nChennai specific jobs ({len(chn_jobs)}):")
for j in chn_jobs:
    print(f"  - [{j['req']}] {j['title']} | {j['location']}")
