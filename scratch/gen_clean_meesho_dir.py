import json

with open("scratch/meesho_bangalore_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

depts = {}
for j in jobs:
    d = j.get('categories', {}).get('department', 'Other')
    depts.setdefault(d, []).append(j)

with open("scratch/meesho_bangalore_clean_directory.md", "w", encoding="utf-8") as f:
    f.write("# Complete Meesho Bengaluru Live Requisitions Directory\n\n")
    f.write(f"Total Live Bengaluru Requisitions: **{len(jobs)}** (Host: Lever ATS)\n\n")
    for d, jlist in sorted(depts.items()):
        f.write(f"## {d} ({len(jlist)} Openings)\n\n")
        f.write("| Title | Team | Lever Requisition ID | Direct Link |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for j in jlist:
            title = j.get("text", "").replace("\ufffd", " - ")
            team = j.get("categories", {}).get("team", "")
            url = j.get("hostedUrl", "")
            jid = j.get("id", "")
            f.write(f"| **{title}** | {team} | `{jid[:8]}...` | [Apply on Lever]({url}) |\n")
        f.write("\n")

print("Generated scratch/meesho_bangalore_clean_directory.md successfully")
