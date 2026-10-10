import csv
import os

master_path = "e:/anti/ALL_BENGALURU_AND_GLOBAL_JOBS_MASTER_DATABASE.csv"
new_data_path = "e:/anti/national_boards_bengaluru_jobs.csv"

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
                "Company / Employer": r["Company / Employer"],
                "Portal Source Platform": r["Portal Source"],
                "Industry Sector": r["Industry Sector"],
                "Work Location": r["Work Location"],
                "Experience / Batch": r["Experience / Batch"],
                "Compensation Band": r["Compensation Band"],
                "Key Skills Required": r["Key Skills Required"],
                "Job Description Summary & Deliverables": r["Job Description & Scope"],
                "Direct Application URL": r["Direct Application URL"]
            })

print("Successfully merged national boards dataset into master database.")
