import csv
import json
from pathlib import Path
from collections import defaultdict

root = Path(r"e:\anti")
matches_csv = root / "data" / "job_to_connection_matches.csv"

# Group recruiters and contacts by Job ID
jobs_map = {}
recruiters_by_job = defaultdict(list)

with open(matches_csv, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        jid = row["Job ID"]
        if jid not in jobs_map:
            jobs_map[jid] = {
                "id": jid,
                "company": row["Target Company"],
                "title": row["Job Title"],
                "url": row["Job URL"],
                "relevance": row.get("Total Contact Opportunity Score (100)", "75")
            }
        
        if "Recruiter" in row["Match Type"]:
            recruiters_by_job[jid].append({
                "name": row["Contact Name"],
                "position": row["Contact Position"],
                "linkedin": row["Contact LinkedIn URL"],
                "score": row.get("Total Contact Opportunity Score (100)", "75")
            })

# Sort recruiters by score
for jid in recruiters_by_job:
    recruiters_by_job[jid].sort(key=lambda x: float(x["score"]) if x["score"].replace(".","").isdigit() else 0, reverse=True)

# Build Markdown
md_path = root / "ACTIVE_HIRING_MNC_STRIKE_BOARD.md"
lines = [
    "# ACTIVE HIRING MNCs & HIGH-GROWTH ENTERPRISES (BENGALURU)",
    "",
    "**Candidate**: Aditya Mehra (BBA International Business, DSU Class of 2026)",
    f"**Total Verified Open Job Roles**: {len(jobs_map)} Roles",
    "**Matched Gatekeepers**: 96 Verified Recruiters & Talent Acquisition Partners",
    "",
    "---",
    "",
    "| Job ID | Company | Open Role | Verified Recruiters Matched | Career Portal Link | Top Recruiter on LinkedIn |",
    "| :-: | :--- | :--- | :-: | :--- | :--- |"
]

for jid, job in sorted(jobs_map.items()):
    recs = recruiters_by_job.get(jid, [])
    rec_count = len(recs)
    top_rec = recs[0] if recs else None
    
    if top_rec:
        rec_str = f"[{top_rec['name']}]({top_rec['linkedin']}) ({top_rec['position']})"
    else:
        rec_str = "Direct Portal Only"
        
    portal_link = f"[Apply on Portal]({job['url']})"
    
    lines.append(f"| `{jid}` | **{job['company']}** | {job['title']} | **{rec_count}** | {portal_link} | {rec_str} |")

with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Generated {md_path} with {len(jobs_map)} active hiring opportunities!")
