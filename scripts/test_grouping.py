import json
import csv
from collections import defaultdict

with open(r'e:\anti\linkedin_export\connection_outreach_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Group Tier 1
by_co = defaultdict(list)
for d in data:
    if 'Tier 1' in d['category']:
        co_name = d['job_info'].split(' | ')[0]
        by_co[co_name].append(d)

print(f"Total Companies with Mapped Tier 1 Openings: {len(by_co)}")
print(f"Total Tier 1 Connections: {sum(len(v) for v in by_co.values())}")
