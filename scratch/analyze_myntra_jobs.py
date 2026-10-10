import json

with open("scratch/myntra_all_jobs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entities = data.get("entities", [])
print(f"Total jobs: {len(entities)}\n")

for i, job in enumerate(entities, 1):
    job_id = job.get("id") or job.get("requisitionId") or job.get("displayId")
    title = job.get("title") or job.get("role") or job.get("jobTitle")
    location = job.get("location") or job.get("city") or job.get("locations")
    group = job.get("jobGroup") or job.get("department")
    exp = job.get("experience") or job.get("experienceLevel")
    emp_type = job.get("employmentType")
    skills = job.get("skills", [])
    
    print(f"{i}. [{job.get('displayId', job.get('id'))}] {title}")
    print(f"   Location: {location} | Group: {group} | Exp: {exp} | Type: {emp_type}")
    print(f"   Skills: {', '.join([s.get('name', str(s)) if isinstance(s, dict) else str(s) for s in skills[:6]])}")
    print(f"   Keys available: {list(job.keys())[:8]}")
    print()
    if i == 1:
        with open("scratch/job_1_full.json", "w", encoding="utf-8") as out:
            json.dump(job, out, indent=2)
