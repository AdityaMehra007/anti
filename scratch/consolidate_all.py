import json
import csv
from collections import Counter

files = [
    'e:/anti/scratch/jobspresso_all_extracted.json',
    'e:/anti/scratch/jobspresso_pages_6_to_15.json',
    'e:/anti/scratch/jobspresso_targeted_harvest.json'
]

all_jobs = []
for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            all_jobs.extend(json.load(f))
    except Exception as e:
        print(f"Error reading {fpath}: {e}")

print(f"Total raw items loaded: {len(all_jobs)}")

# Deduplicate by URL
unique_jobs = {}
for j in all_jobs:
    url = j['url']
    if not url:
        continue
    if url not in unique_jobs:
        unique_jobs[url] = j
    else:
        # Merge if richer fields
        if len(j.get('tagline', '')) > len(unique_jobs[url].get('tagline', '')):
            unique_jobs[url]['tagline'] = j['tagline']

print(f"Total unique jobs: {len(unique_jobs)}")

companies = Counter([j['company'] for j in unique_jobs.values() if j['company']])
print(f"Total unique companies: {len(companies)}")
print("Top 15 Companies overall:")
for c, cnt in companies.most_common(15):
    print(f"  {c}: {cnt}")

locations = Counter([j['location'] for j in unique_jobs.values() if j['location']])
print("\nTop 10 Locations overall:")
for l, cnt in locations.most_common(10):
    print(f"  {l}: {cnt}")

with open('e:/anti/scratch/jobspresso_deduped_master.json', 'w', encoding='utf-8') as out:
    json.dump(list(unique_jobs.values()), out, indent=2, ensure_ascii=False)
