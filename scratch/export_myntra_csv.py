import json
import csv

with open("scratch/myntra_all_jobs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entities = data.get("entities", [])
output_file = "myntra_bengaluru_jobs.csv"

fieldnames = [
    "display_id",
    "requisition_id",
    "job_title",
    "department",
    "employment_type",
    "workplace_type",
    "experience_range",
    "city",
    "key_skills",
    "recruiter_name",
    "recruiter_email",
    "portal_apply_url"
]

rows = []
for job in entities:
    display_id = job.get("displayId", "")
    req_id = job.get("id", "")
    title = job.get("jobTitle", "")
    dept = job.get("departmentName", "")
    emp_type = job.get("employmentType", "")
    workplace = job.get("jobType", "")
    
    exp = job.get("requiredExperienceInMonths", {})
    if exp:
        exp_range = f"{exp.get('from', 0)//12}-{exp.get('to', 0)//12} yrs"
    else:
        exp_range = "N/A"
        
    locations = job.get("jobLocation", [])
    city_names = [loc.get("city", "Bangalore") for loc in locations]
    city_str = ", ".join(city_names) if city_names else "Bangalore"
    
    skills = [s.get("skill") for s in job.get("skills", []) if s.get("isMandatory")]
    skills_str = ", ".join(skills[:8])
    
    recruiter = job.get("recruiter", {})
    rec_name = recruiter.get("fullName", "")
    rec_email = recruiter.get("emailId", "")
    
    apply_url = f"https://jobs.myntra.com/home#/job-details/{display_id}"
    
    rows.append({
        "display_id": display_id,
        "requisition_id": req_id,
        "job_title": title,
        "department": dept,
        "employment_type": emp_type,
        "workplace_type": workplace,
        "experience_range": exp_range,
        "city": city_str,
        "key_skills": skills_str,
        "recruiter_name": rec_name,
        "recruiter_email": rec_email,
        "portal_apply_url": apply_url
    })

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Exported {len(rows)} Myntra jobs to {output_file}")
