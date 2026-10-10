import json

with open('scratch/mbrdi_all_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

target_depts = ['O2C, P2P, ProQ', 'Part Management', 'Car Sales - Operations & Transformation 1', 'Controlling', 'Logistics System & Processes', 'Customer Business & EoP+']

print("Jobs in Commercial, Procurement, Supply Chain & Operations departments:")
seen = set()
for j in jobs:
    dept = j.get('DepartmentName', '')
    title = j.get('PositionTitle', '')
    req = j.get('ID', '')
    if dept in target_depts:
        key = f"{title} | {dept}"
        if key not in seen:
            seen.add(key)
            print(f"Title: {title}")
            print(f"  Dept: {dept} | ID: {req}")
            print(f"  Taleo Req: {j.get('ReferralUrl')}")
            for c in j.get('Contact', []):
                print(f"  Recruiter: {c.get('Name')} <{c.get('Email')}>")
            print()
