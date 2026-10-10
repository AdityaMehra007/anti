import json

with open("scratch/walmart_non_tech_blr.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

print(f"Total Non-Tech / Business Ops / Analytics Jobs: {len(jobs)}")
for idx, j in enumerate(jobs, 1):
    req_id = j.get('bulletFields', [''])[0]
    title = j.get('title')
    loc = j.get('locationsText')
    path = j.get('externalPath')
    print(f"{idx}. [{req_id}] {title} | {loc}")
    print(f"   URL: https://walmart.wd504.myworkdayjobs.com/en-US/WalmartExternal{path}")
