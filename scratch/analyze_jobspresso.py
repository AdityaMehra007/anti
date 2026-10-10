import json
from collections import Counter

with open('e:/anti/scratch/jobspresso_all_extracted.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total jobs: {len(jobs)}")
companies = Counter([j['company'] for j in jobs if j['company']])
print("\nTop 20 Companies by Job Count:")
for comp, count in companies.most_common(20):
    print(f"  {comp}: {count}")

locations = Counter([j['location'] for j in jobs if j['location']])
print("\nTop 15 Location Filters:")
for loc, count in locations.most_common(15):
    print(f"  {loc}: {count}")

categories = Counter([j['categories'] for j in jobs if j['categories']])
print("\nTop Categories:")
for cat, count in categories.most_common(15):
    print(f"  {cat}: {count}")

# Check for India or Worldwide / Global / Anywhere
global_india_jobs = [j for j in jobs if any(k in j['location'].lower() for k in ['india', 'worldwide', 'anywhere', 'global', 'remote', 'apac', 'asia', 'all'])]
print(f"\nJobs matching Global / Worldwide / Anywhere / India: {len(global_india_jobs)}")
for j in global_india_jobs[:15]:
    print(f"  - [{j['company']}] {j['title']} ({j['location']}) | Cat: {j['categories']}")
