import json

with open("scratch/walmart_bangalore_all_unique_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

print(f"Total jobs: {len(jobs)}")

locations = {}
bullet_types = {}
for j in jobs:
    loc = j.get('locationsText', 'Unknown')
    locations[loc] = locations.get(loc, 0) + 1

print("\nLocations / Buildings:")
for l, c in sorted(locations.items(), key=lambda x: -x[1]):
    print(f"  - {l}: {c}")

# Search for Non-tech, Operations, Business, Coordinator, Analyst, Supply Chain, Finance
keywords = [
    "coordinator", "analyst", "operations", "resolution", "specialist", 
    "associate", "program", "project", "supply chain", "finance", 
    "business", "intern", "trainee", "contact center", "buyer", "merchant"
]

non_tech = []
tech = []

for j in jobs:
    title = j.get('title', '')
    title_lower = title.lower()
    
    # check if matches non-tech keywords and not pure software engineer / architect
    is_non_tech = any(k in title_lower for k in keywords)
    if is_non_tech:
        non_tech.append(j)
    else:
        tech.append(j)

print(f"\nNon-tech / Operations / Business / Analytics / Coordinator jobs: {len(non_tech)}")
print(f"Core Tech / Engineering / Data Science jobs: {len(tech)}")

print("\n--- NON-TECH & BUSINESS OPERATIONS ROLES SAMPLE ---")
for j in non_tech[:25]:
    req_id = j.get('bulletFields', [''])[0]
    title = j.get('title')
    loc = j.get('locationsText')
    path = j.get('externalPath')
    print(f"  - [{req_id}] {title} | {loc}")
    print(f"    https://walmart.wd504.myworkdayjobs.com/en-US/WalmartExternal{path}")

with open("scratch/walmart_non_tech_blr.json", "w", encoding="utf-8") as out:
    json.dump(non_tech, out, indent=2)
