import json

with open("scratch/meesho_bangalore_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

depts = {}
for j in jobs:
    d = j.get('categories', {}).get('department', 'Other')
    depts.setdefault(d, []).append(j)

for d, jlist in sorted(depts.items()):
    print(f"\n### {d} ({len(jlist)} Openings)")
    for j in jlist:
        title = j.get("text", "").replace("\ufffd", "-").replace("", "-")
        team = j.get("categories", {}).get("team", "")
        url = j.get("hostedUrl", "")
        jid = j.get("id", "")
        print(f"- **{title}** — *{team}* | [Apply on Lever]({url})")
