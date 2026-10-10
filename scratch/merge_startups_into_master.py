import csv

master_path = "e:/anti/ALL_BENGALURU_AND_GLOBAL_JOBS_MASTER_DATABASE.csv"
new_data_path = "e:/anti/startup_hubs_bengaluru_jobs.csv"

with open(master_path, mode="a", newline="", encoding="utf-8") as mf:
    writer = csv.DictWriter(mf, fieldnames=[
        "Universal Job ID", "Job Title / Role", "Company / Employer",
        "Portal Source Platform", "Industry Sector", "Work Location",
        "Experience / Batch", "Compensation Band", "Key Skills Required",
        "Job Description Summary & Deliverables", "Direct Application URL"
    ])
    
    with open(new_data_path, encoding="utf-8") as nf:
        reader = csv.DictReader(nf)
        for r in reader:
            writer.writerow({
                "Universal Job ID": r["Requisition ID"],
                "Job Title / Role": r["Job Title"],
                "Company / Employer": r["Company / Startup"],
                "Portal Source Platform": r["Platform"],
                "Industry Sector": r["Domain / Sector"],
                "Work Location": r["Work Location"],
                "Experience / Batch": r["Experience Level"],
                "Compensation Band": r["Compensation Band"],
                "Key Skills Required": r["Core Skills Required"],
                "Job Description Summary & Deliverables": f"Startup Operations & Execution for {r['Company / Startup']}",
                "Direct Application URL": r["Direct Portal Route URL"]
            })

print("Successfully merged startup hubs dataset into master database.")
