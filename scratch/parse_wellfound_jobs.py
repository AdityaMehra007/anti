import json
import csv

with open("scratch/wellfound_blr_apollo.json", "r", encoding="utf-8") as f:
    apollo = json.load(f).get("data", {})

startups_map = {}
jobs_list = []

for k, v in apollo.items():
    if isinstance(v, dict) and v.get("__typename") == "StartupResult":
        s_id = v.get("id")
        startups_map[s_id] = {
            "name": v.get("name"),
            "slug": v.get("slug"),
            "highConcept": v.get("highConcept"),
            "companySize": v.get("companySize"),
            "job_refs": [ref.get("__ref") for ref in v.get("highlightedJobListings", [])]
        }

for k, v in apollo.items():
    if isinstance(v, dict) and v.get("__typename") == "JobListingSearchResult":
        j_id = v.get("id")
        title = v.get("title")
        slug = v.get("slug")
        compensation = v.get("compensation", "")
        exp_min = v.get("yearsExperienceMin")
        remote = v.get("remote")
        locations = v.get("locationNames", [])
        primary_role = v.get("primaryRoleTitle")
        ats_source = v.get("atsSource", "Direct Wellfound")
        
        startup_name = "Unknown Startup"
        startup_slug = ""
        for s_id, s_data in startups_map.items():
            if f"JobListingSearchResult:{j_id}" in s_data["job_refs"]:
                startup_name = s_data["name"]
                startup_slug = s_data["slug"]
                break
                
        wellfound_job_url = f"https://wellfound.com/jobs/{j_id}-{slug}"
        startup_url = f"https://wellfound.com/company/{startup_slug}" if startup_slug else ""
        
        jobs_list.append({
            "id": j_id,
            "title": title,
            "startup_name": startup_name,
            "compensation": compensation if compensation else "Competitive Equity / Salary",
            "experience_min": f"{exp_min}+ yrs" if exp_min else "Not specified",
            "primary_role": primary_role,
            "locations": ", ".join(locations),
            "remote": "Remote / Hybrid" if remote else "Onsite",
            "ats_source": ats_source,
            "job_url": wellfound_job_url,
            "startup_url": startup_url
        })

with open("wellfound_bengaluru_jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "id", "title", "startup_name", "compensation", "experience_min",
        "primary_role", "locations", "remote", "ats_source", "job_url", "startup_url"
    ])
    writer.writeheader()
    writer.writerows(jobs_list)

print(f"Successfully generated wellfound_bengaluru_jobs.csv with {len(jobs_list)} records across {len(startups_map)} startups.\n")

# Group by category / startup
for i, j in enumerate(jobs_list[:25], 1):
    comp_clean = j['compensation'].replace('\u20b9', 'INR ').replace('\u2022', '|')
    print(f"{i}. [{j['startup_name']}] {j['title']}")
    print(f"   Comp: {comp_clean} | Exp: {j['experience_min']} | Mode: {j['remote']}")
    print(f"   URL: {j['job_url']}")
