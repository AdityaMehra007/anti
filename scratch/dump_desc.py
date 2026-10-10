import json

with open("scratch/walmart_resolution_coord.json", "r", encoding="utf-8") as f:
    job = json.load(f)

desc = job.get('jobDescription', '')
with open("scratch/walmart_resolution_coord_desc.txt", "w", encoding="utf-8") as out:
    out.write(f"Title: {job.get('title')}\n")
    out.write(f"Job Req ID: {job.get('jobReqId')}\n")
    out.write(f"Location: {job.get('location')}\n")
    out.write(f"\n{desc}\n")

print("Saved description to scratch/walmart_resolution_coord_desc.txt")
