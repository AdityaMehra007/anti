import csv
import json

with open('data/approval_queue.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

comps = set(r['Company'] for r in rows)
print("Existing companies in queue:")
for c in sorted(comps):
    matching_rows = [r for r in rows if r['Company'] == c]
    first_id = matching_rows[0]['Action ID']
    last_id = matching_rows[-1]['Action ID']
    print(f"  {c}: {len(matching_rows)} rows (IDs: {first_id} - {last_id})")
