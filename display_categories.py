import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('e:/anti/categorized_mega_bengaluru_jobs.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

for cat_name, jobs in cats.items():
    print(f"\n### {cat_name} ({len(jobs)} active jobs)")
    for j in jobs[:6]:
        print(f"* **{j['title']}** (Job ID: `{j['req_id']}`)")
        print(f"  * Status: {j['posted']}")
        print(f"  * Link: {j['link']}")
