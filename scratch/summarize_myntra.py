import json
from collections import defaultdict

with open("scratch/myntra_all_jobs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entities = data.get("entities", [])

print(f"Total jobs extracted: {len(entities)}\n")

by_dept = defaultdict(list)
by_city = defaultdict(int)

for job in entities:
    display_id = job.get("displayId")
    title = job.get("jobTitle")
    dept = job.get("departmentName", "General / Unspecified")
    emp_type = job.get("employmentType", "FULL_TIME")
    job_type = job.get("jobType", "ONSITE")
    exp = job.get("requiredExperienceInMonths", {})
    exp_str = f"{exp.get('from', 0)//12}-{exp.get('to', 0)//12} yrs" if exp else "N/A"
    
    locations = job.get("jobLocation", [])
    city_names = [loc.get("city", "Bangalore") for loc in locations]
    city_str = ", ".join(city_names) if city_names else "Bangalore"
    
    for c in city_names:
        by_city[c] += 1
        
    skills = [s.get("skill") for s in job.get("skills", []) if s.get("isMandatory")]
    recruiter = job.get("recruiter", {}).get("fullName", "Talent Acquisition")
    recruiter_email = job.get("recruiter", {}).get("emailId", "")
    
    by_dept[dept].append({
        "displayId": display_id,
        "title": title,
        "exp": exp_str,
        "type": emp_type,
        "workplace": job_type,
        "city": city_str,
        "skills": skills[:5],
        "recruiter": f"{recruiter} ({recruiter_email})" if recruiter_email else recruiter
    })

print("CITY DISTRIBUTION:")
for c, cnt in by_city.items():
    print(f"  {c}: {cnt}")

print("\nDEPARTMENT BREAKDOWN:")
for dept, jobs in sorted(by_dept.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n### {dept} ({len(jobs)} Openings)")
    for j in jobs:
        print(f"  - [{j['displayId']}] {j['title']} | {j['exp']} | {j['workplace']} | Recruiter: {j['recruiter']}")
        print(f"    Skills: {', '.join(j['skills'])}")
