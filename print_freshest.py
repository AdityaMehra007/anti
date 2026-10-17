import json

data = json.load(open('mega_bengaluru_jobs.json', encoding='utf-8'))
fresh_buckets = {}
for j in data:
    p = j.get('posted', '')
    fresh_buckets.setdefault(p, []).append(j)

recent_days = ['Posted Today', 'Posted Yesterday', 'Posted 2 Days Ago', 'Posted 8 Days Ago', 'Posted 10 Days Ago', 'Posted 16 Days Ago', 'Posted 18 Days Ago']
for r in recent_days:
    if r in fresh_buckets:
        print(f"=== {r} ({len(fresh_buckets[r])} jobs) ===")
        for x in fresh_buckets[r]:
            print(f"  * [{x['req_id']}] {x['title']}")
            print(f"    Link: {x['link']}")
