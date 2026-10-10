import json
import re

with open("scratch/razorpay_all_jobs.json", encoding="utf-8") as f:
    jobs = json.load(f)

for j in jobs:
    jid = j.get("id")
    if jid in [4738311005, 4740728005, 4740722005]:
        print(f"=== [{jid}] {j.get('title')} ===")
        print("Apply URL:", j.get("absolute_url"))
        content = j.get("content", "")
        text = re.sub(r'<[^>]+>', '\n', content)
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        # find where job summary starts
        start_idx = 0
        for i, l in enumerate(lines):
            if any(k in l.lower() for k in ["role summary", "about the role", "roles & responsibilities", "job description"]):
                start_idx = i
                break
        for l in lines[start_idx:start_idx+25]:
            print("  ", l.encode('ascii', 'ignore').decode('ascii'))
        print()
