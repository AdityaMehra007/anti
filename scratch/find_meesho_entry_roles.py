import json

with open("scratch/meesho_bangalore_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

print(f"Total Bangalore jobs: {len(jobs)}")

keywords = ["trainee", "associate", "coordinator", "analyst", "assistant manager", "junior", "operations", "specialist", "executive"]

matches = []
for j in jobs:
    title = j.get('text', '').lower()
    desc = j.get('descriptionPlain', '').lower()
    
    matched_kws = [kw for kw in keywords if kw in title]
    if matched_kws or "fresher" in desc or "0-1" in desc or "0-2" in desc:
        matches.append(j)

print(f"Found {len(matches)} potential entry/early-career roles:\n")
for m in matches:
    title = m.get('text', '')
    jid = m.get('id', '')
    dept = m.get('categories', {}).get('department', '')
    team = m.get('categories', {}).get('team', '')
    url = m.get('hostedUrl', '')
    print(f"[{jid}] {title} | Dept: {dept} | Team: {team}")
    print(f"     URL: {url}")
