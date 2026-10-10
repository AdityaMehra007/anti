import json
from collections import Counter
import re

with open('scratch/mbrdi_all_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total jobs: {len(jobs)}")

# Analyze departments
depts = Counter()
job_cats = Counter()
career_levels = Counter()
locations = Counter()
recruiters = Counter()

for j in jobs:
    depts[j.get('DepartmentName', 'Unknown')] += 1
    for cat in j.get('JobCategory', []):
        job_cats[cat.get('Name', 'Unknown')] += 1
    for lvl in j.get('CareerLevel', []):
        career_levels[lvl.get('Name', 'Unknown')] += 1
    for loc in j.get('PositionLocation', []):
        locations[f"{loc.get('CityName', 'Unknown')} ({loc.get('PostalCode', '')})"] += 1
    for con in j.get('Contact', []):
        recruiters[f"{con.get('Name')} <{con.get('Email')}>"] += 1

print("\n--- Top Departments ---")
for d, c in depts.most_common(15):
    print(f"  {d}: {c}")

print("\n--- Job Categories ---")
for jc, c in job_cats.most_common(15):
    print(f"  {jc}: {c}")

print("\n--- Locations ---")
for loc, c in locations.most_common(10):
    print(f"  {loc}: {c}")

print("\n--- Top Recruiters / Contacts ---")
for r, c in recruiters.most_common(10):
    print(f"  {r}: {c}")

# Find Non-Tech / Corporate / Procurement / Supply Chain / Finance / PMO / Junior jobs
print("\n" + "="*70)
print("--- Non-Technical / Corporate / Business Ops / PMO / SCM Roles ---")
keywords = ['procurement', 'supply chain', 'buyer', 'purchase', 'logistics', 'finance', 'account', 'pmo', 'project', 'commercial', 'coordinator', 'analyst', 'hr', 'human resources', 'business', 'governance', 'planner', 'trainee', 'associate', 'intern']

non_tech = []
for j in jobs:
    title = j.get('PositionTitle', '')
    dept = j.get('DepartmentName', '')
    req = j.get('ID', '')
    ref_url = j.get('ReferralUrl', '')
    
    # Check if matches keywords
    if any(k in title.lower() or k in dept.lower() for k in keywords):
        non_tech.append(j)

print(f"Total matching non-tech / business / operations roles: {len(non_tech)}")
with open('scratch/mbrdi_non_tech_jobs.txt', 'w', encoding='utf-8') as out:
    for i, j in enumerate(non_tech, 1):
        contact_str = ""
        for c in j.get('Contact', []):
            contact_str = f"{c.get('Name')} ({c.get('Email')})"
        out.write(f"{i}. [{j.get('ID')}] {j.get('PositionTitle')}\n")
        out.write(f"   Department: {j.get('DepartmentName')}\n")
        out.write(f"   Contact: {contact_str}\n")
        out.write(f"   Referral/Taleo URL: {j.get('ReferralUrl')}\n")
        out.write(f"   Start Date: {j.get('PositionStartDate')}\n\n")

print("Saved to scratch/mbrdi_non_tech_jobs.txt")
