import json
from collections import Counter

with open('e:/anti/scratch/jobspresso_targeted_harvest.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total collected: {len(jobs)}")

india_jobs = [j for j in jobs if 'india' in j['location'].lower() or j['query_source'] == 'India']
worldwide_jobs = [j for j in jobs if any(k in j['location'].lower() for k in ['worldwide', 'anywhere', 'global', 'remote', 'apac', 'international', 'all'])]

print(f"India source/location jobs: {len(india_jobs)}")
print(f"Worldwide/Global location jobs: {len(worldwide_jobs)}")

print("\n--- Sample India Jobs ---")
for j in india_jobs[:10]:
    print(f"  [{j['company']}] {j['title']} | Loc: {j['location']} | Cat: {j['categories']} | URL: {j['url']}")

print("\n--- Sample Worldwide / Global Jobs ---")
for j in worldwide_jobs[:10]:
    print(f"  [{j['company']}] {j['title']} | Loc: {j['location']} | Cat: {j['categories']} | URL: {j['url']}")

print("\n--- Sample Operations & Support Jobs ---")
ops_support = [j for j in jobs if any(k in j['title'].lower() or k in j['categories'].lower() for k in ['operation', 'support', 'client', 'customer', 'analyst', 'coordinator', 'specialist', 'associate'])]
print(f"Total Ops & Support jobs: {len(ops_support)}")
for j in ops_support[:10]:
    print(f"  [{j['company']}] {j['title']} | Loc: {j['location']} | Cat: {j['categories']} | URL: {j['url']}")
