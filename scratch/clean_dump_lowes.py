import json

with open("scratch/lowes_all_corporate_unique.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

print(f"Total Lowe's India Corporate Jobs: {len(jobs)}")

with open("scratch/lowes_31_jobs_clean.txt", "w", encoding="utf-8") as out:
    for idx, j in enumerate(jobs, 1):
        req_id = j.get('reqId', '')
        title = j.get('title', '')
        city = j.get('city', '')
        state = j.get('state', '')
        url = f"https://talent.lowes.com/in/en/job/{j.get('jobId')}"
        teaser = j.get('descriptionTeaser', '').strip()
        
        out.write(f"{idx}. [{req_id}] {title}\n")
        out.write(f"   Location: {city}, {state}, India\n")
        out.write(f"   URL: {url}\n")
        out.write(f"   Teaser: {teaser[:250]}\n\n")

print("Wrote clean list to scratch/lowes_31_jobs_clean.txt")
