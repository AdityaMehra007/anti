import json

with open("scratch/lowes_ddo_clean.json", "r", encoding="utf-8") as f:
    ddo = json.load(f)

eager = ddo.get("eagerLoadRefineSearch", {}).get("data", {})
jobs = eager.get("jobs", [])

with open("scratch/lowes_page1_jobs.txt", "w", encoding="utf-8") as out:
    out.write(f"Total jobs on page 1: {len(jobs)}\n\n")
    for idx, j in enumerate(jobs, 1):
        out.write(f"{idx}. [{j.get('reqId')}] {j.get('title')}\n")
        out.write(f"   City: {j.get('city')}, State: {j.get('state')}, Country: {j.get('country')}\n")
        out.write(f"   Category: {j.get('category')} | Subcategory: {j.get('subCategory')}\n")
        out.write(f"   JobId: {j.get('jobId')}\n")
        out.write(f"   JobSeqNo: {j.get('jobSeqNo')}\n")
        out.write(f"   URL: https://talent.lowes.com/in/en/job/{j.get('jobId')}\n")
        out.write(f"   Description Snippet: {j.get('descriptionTeaser', '')[:200]}\n\n")

print("Saved page 1 jobs to scratch/lowes_page1_jobs.txt")
