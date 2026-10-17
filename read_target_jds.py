import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('e:/anti/all_jds_examined.json', 'r', encoding='utf-8') as f:
    jds = json.load(f)

for target in ['Procurement', 'Learning', 'TrustSafety', 'HR', 'SalesOps']:
    d = jds[target]
    print(f"\n=======================================================")
    print(f"TARGET: {target} | REQ: {d['req_id']} | TITLE: {d['title']}")
    print(f"=======================================================")
    print(d['description'])
