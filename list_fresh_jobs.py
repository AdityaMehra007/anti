import json

with open('mega_bengaluru_jobs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Sort by freshness: Yesterday, 2 Days Ago, 3 Days Ago...
fresh_buckets = {}
for j in data:
    p = j.get('posted', '')
    fresh_buckets.setdefault(p, []).append(j)

print("Posting Date Distribution:")
for k in sorted(fresh_buckets.keys()):
    print(f"  {k}: {len(fresh_buckets[k])} jobs")

print("\n=======================================================")
print("ABSOLUTE LATEST POSTINGS (POSTED YESTERDAY TO 10 DAYS AGO):")
print("=======================================================")

priority_order = [
    'Posted Today',
    'Posted Yesterday',
    'Posted 2 Days Ago',
    'Posted 3 Days Ago',
    'Posted 4 Days Ago',
    'Posted 5 Days Ago',
    'Posted 6 Days Ago',
    'Posted 7 Days Ago',
    'Posted 8 Days Ago',
    'Posted 9 Days Ago',
    'Posted 10 Days Ago',
    'Posted 11 Days Ago',
    'Posted 12 Days Ago',
    'Posted 13 Days Ago',
    'Posted 14 Days Ago',
    'Posted 15 Days Ago',
    'Posted 16 Days Ago',
    'Posted 18 Days Ago',
    'Posted 22 Days Ago',
    'Posted 23 Days Ago',
    'Posted 26 Days Ago',
    'Posted 30 Days Ago'
]

for bucket in priority_order:
    if bucket in fresh_buckets:
        print(f"\n--- {bucket.upper()} ({len(fresh_buckets[bucket])} jobs) ---")
        for job in fresh_buckets[bucket]:
            print(f"• [{job['req_id']}] {job['title']}")
            print(f"  Link: {job['link']}")
