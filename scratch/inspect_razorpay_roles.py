import json
import re

with open("scratch/razorpay_all_jobs.json", encoding="utf-8") as f:
    jobs = json.load(f)

target_ids = [4738311005, 4740728005, 4740722005, 4731060005, 4739576005]

for j in jobs:
    jid = j.get("id")
    if jid in target_ids:
        print(f"=== [{jid}] {j.get('title')} ===")
        print("Location:", j.get("location", {}).get("name"))
        print("Apply URL:", j.get("absolute_url"))
        content = j.get("content", "")
        text = re.sub(r'<[^>]+>', '\n', content)
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        for l in lines[:15]:
            print("  ", l.encode('ascii', 'ignore').decode('ascii'))
        print()
