import json
import re

with open("scratch/groww_all_jobs.json", encoding="utf-8") as f:
    jobs = json.load(f)

for j in jobs:
    jid = j.get("id")
    print(f"=== [{jid}] {j.get('title')} ===")
    print("Dept:", [d.get("name") for d in j.get("departments", [])])
    print("Location:", j.get("location", {}).get("name"))
    print("URL:", f"https://job-boards.eu.greenhouse.io/groww/jobs/{jid}")
    content = j.get("content", "")
    text = re.sub(r'<[^>]+>', '\n', content)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for l in lines[:15]:
        print(" ", l.encode('ascii', 'ignore').decode('ascii'))
    print()
