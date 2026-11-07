import json
import csv
import os

print("--- Querying Top Job Opportunities ---")

# 1. Check bengaluru_startup_jobs.csv
print("\n[1] Bengaluru Startup Radar Priority Jobs:")
if os.path.exists("data/bengaluru_startup_jobs.csv"):
    with open("data/bengaluru_startup_jobs.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            print(f"  {row.get('job_id')}: {row.get('title')} @ {row.get('company')} | Loc: {row.get('location')} | Sal: {row.get('salary_range')} | Fit: {row.get('fit_score')}/100")
            if i >= 9:
                break

# 2. Check remote_active_jobs.json
print("\n[2] Remote Active Jobs:")
if os.path.exists("data/remote_active_jobs.json"):
    with open("data/remote_active_jobs.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        items = data if isinstance(data, list) else data.get("jobs", [])
        for i, job in enumerate(items[:10]):
            title = job.get("title") or job.get("role")
            comp = job.get("company")
            sal = job.get("salary") or job.get("compensation") or "Competitive"
            fit = job.get("score") or job.get("fit_score") or "N/A"
            url = job.get("url") or job.get("apply_url") or job.get("link")
            print(f"  {title} @ {comp} | Sal: {sal} | Fit: {fit} | URL: {url}")

# 3. Check BANGALORE_SCORED_JOBS_MASTER.json
print("\n[3] Top Non-Sales & High-Velocity Roles from Bangalore Scored Master:")
if os.path.exists("data/BANGALORE_SCORED_JOBS_MASTER.json"):
    with open("data/BANGALORE_SCORED_JOBS_MASTER.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        items = data if isinstance(data, list) else data.get("jobs", [])
        # Filter for top scores
        sorted_items = sorted(items, key=lambda x: x.get("final_score", 0) if isinstance(x, dict) else 0, reverse=True)
        for i, job in enumerate(sorted_items[:12]):
            title = job.get("title")
            company = job.get("company")
            score = job.get("final_score")
            track = job.get("role_track") or job.get("category")
            sal = job.get("salary") or "Industry Standard"
            url = job.get("apply_url") or job.get("url") or job.get("link")
            print(f"  Score: {score} | {title} @ {company} [{track}] | {sal}")
