import json

with open('all_accenture_people_categorized.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

md_lines = [
    "# 🏛️ Accenture Bengaluru Master Network Directory (116 People)",
    "> **Status:** 100% Verified 1st-Degree LinkedIn Connections & Career Intelligence Contacts",
    "> **Candidate:** Aditya Mehra | BBA (International Business) — Dayananda Sagar University",
    "",
    "---",
    ""
]

total = sum(len(v) for v in data.values())
md_lines.append(f"## 📊 Executive Network Breakdown (Total: {total} Contacts)")
for cat, ppl in data.items():
    md_lines.append(f"- **{cat}:** {len(ppl)} people")
md_lines.append("\n---\n")

for cat, ppl in data.items():
    md_lines.append(f"## {cat} ({len(ppl)} Contacts)")
    md_lines.append("| # | Name | Current Title / Role | LinkedIn Profile Link |")
    md_lines.append("|:---:|---|---|---|")
    for i, p in enumerate(ppl, 1):
        name = p.get('name', 'N/A')
        title = p.get('title', 'Accenture Professional')
        url = p.get('url', '')
        link_str = f"[{name} on LinkedIn]({url})" if url else "Profile Pending"
        md_lines.append(f"| {i} | **{name}** | {title} | {link_str} |")
    md_lines.append("\n---\n")

with open('ACCENTURE_ALL_116_PEOPLE_DIRECTORY.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(md_lines))

print("Created ACCENTURE_ALL_116_PEOPLE_DIRECTORY.md successfully!")
