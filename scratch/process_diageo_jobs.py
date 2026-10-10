import urllib.request
import ssl
import json
import csv

ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

all_jobs = []
page = 1
total_pages = 1

while page <= total_pages:
    url = f"https://diageo-prod-api.connectid.cloud/api/jobs?country=India&page={page}"
    print(f"Fetching page {page} of {total_pages}...")
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req, context=ctx)
    data = json.loads(res.read().decode("utf-8"))
    
    meta = data.get("meta", {})
    total_pages = meta.get("totalPages", 1)
    jobs = data.get("data", [])
    all_jobs.extend(jobs)
    page += 1

print(f"\nTotal India jobs fetched: {len(all_jobs)}")

with open("scratch/diageo_all_india_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2)

# Filter for Bengaluru / Bangalore
bengaluru_jobs = []
for j in all_jobs:
    locs = j.get("Primary_Job_Posting_Location", [])
    loc_str = " ".join(locs).lower()
    add_locs = [str(x) for x in j.get("Job_Requisition_Additional_Job_Posting_Locations_group", [])]
    add_str = " ".join(add_locs).lower()
    
    if any(k in loc_str or k in add_str for k in ["bangalore", "bengaluru"]):
        bengaluru_jobs.append(j)

print(f"Total Bengaluru / Bangalore jobs: {len(bengaluru_jobs)}")

# Export Bengaluru jobs to CSV
output_csv = "diageo_bengaluru_jobs.csv"
fieldnames = [
    "reference_id",
    "job_title",
    "job_family",
    "job_family_group",
    "function_subtype",
    "management_level",
    "time_type",
    "location",
    "posting_start_date",
    "workday_apply_url"
]

rows = []
for j in bengaluru_jobs:
    ref_id = j.get("referenceID", "")
    title = j.get("Job_Posting_Title", "")
    family = j.get("Job_Family", "")
    group = j.get("Job_Family_Group", "")
    subtype = j.get("Function_Subtype", "")
    lvl = j.get("Management_Level", "")
    time_type = j.get("Time_Type", "")
    loc = ", ".join(j.get("Primary_Job_Posting_Location", []))
    start_date = j.get("Job_Posting_Start_Date", "")
    url = j.get("External_Posting_URL", "")
    
    rows.append({
        "reference_id": ref_id,
        "job_title": title,
        "job_family": family,
        "job_family_group": group,
        "function_subtype": subtype,
        "management_level": lvl,
        "time_type": time_type,
        "location": loc,
        "posting_start_date": start_date,
        "workday_apply_url": url
    })

with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Exported {len(rows)} Bengaluru jobs to {output_csv}")
