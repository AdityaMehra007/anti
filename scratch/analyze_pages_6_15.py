import json
from collections import Counter

with open('e:/anti/scratch/jobspresso_pages_6_to_15.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total jobs in pages 6-15: {len(jobs)}")
companies = Counter([j['company'] for j in jobs if j['company']])
print("\nTop 20 Companies:")
for comp, count in companies.most_common(20):
    print(f"  {comp}: {count}")

locations = Counter([j['location'] for j in jobs if j['location']])
print("\nTop 15 Locations:")
for loc, count in locations.most_common(15):
    print(f"  {loc}: {count}")

categories = Counter([j['categories'] for j in jobs if j['categories']])
print("\nTop Categories:")
for cat, count in categories.most_common(10):
    print(f"  {cat}: {count}")

# Worldwide / India jobs in pages 6-15
global_jobs = [j for j in jobs if any(k in j['location'].lower() for k in ['worldwide', 'anywhere', 'global', 'remote', 'india', 'apac', 'various countries'])]
print(f"\nWorldwide/India/Global jobs in pages 6-15: {len(global_jobs)}")
for j in global_jobs[:15]:
    print(f"  [{j['company']}] {j['title']} | Loc: {j['location']} | Cat: {j['categories']} | URL: {j['url']}")
