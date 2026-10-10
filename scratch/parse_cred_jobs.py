import json

with open("scratch/cred_next_data.json", encoding="utf-8") as f:
    d = json.load(f)

pp = d.get('props', {}).get('pageProps', {})
print("pageProps keys:", list(pp.keys()))

jobs = pp.get('jobs', [])
if not jobs:
    for k in pp:
        if isinstance(pp[k], list):
            print(f"Key '{k}' has list of {len(pp[k])} items")
            jobs = pp[k]
            break

print(f"Total jobs: {len(jobs)}")
with open("scratch/cred_all_jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

teams = {}
for j in jobs:
    team = j.get("categories", {}).get("team") or j.get("team") or "Unknown"
    teams[team] = teams.get(team, 0) + 1

print("\n--- Teams Breakdown ---")
for t, count in sorted(teams.items(), key=lambda x: -x[1]):
    print(f"{t}: {count}")

print("\n--- All Jobs ---")
for idx, j in enumerate(jobs, 1):
    jid = j.get("id")
    title = j.get("text") or j.get("title")
    team = j.get("categories", {}).get("team") or j.get("team")
    loc = j.get("categories", {}).get("location") or j.get("location")
    url = j.get("hostedUrl") or f"https://jobs.lever.co/cred/{jid}"
    print(f"{idx}. [{jid}] {title} | Team: {team} | Loc: {loc}")
    print(f"   URL: {url}")
