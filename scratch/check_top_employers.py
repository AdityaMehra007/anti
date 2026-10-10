import json

with open('e:/anti/scratch/jobspresso_pages_6_to_15.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

for target in ['Atlassian', 'GitHub', 'Canva', 'Webflow', 'ModSquad', 'FreshBooks', 'Yelp']:
    target_jobs = [j for j in jobs if target.lower() in j['company'].lower()]
    print(f"\n=== {target} ({len(target_jobs)} roles) ===")
    for j in target_jobs[:5]:
        print(f"  - {j['title']} | Loc: {j['location']} | Cat: {j['categories']} | URL: {j['url']}")
