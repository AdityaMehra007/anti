import json
import csv
from pathlib import Path

root = Path(r"e:\anti")
pkgs_file = root / "omega" / "data" / "ready_to_apply_packages.json"
with open(pkgs_file, "r", encoding="utf-8") as f:
    pkgs = json.load(f)

# 1. Export CSV
csv_path = root / "data" / "TOP_50_MNC_TARGET_MATRIX.csv"
fields = ["Index", "Company Name", "Tier", "Tech Corridor", "Target Role", "Median CTC (INR)", "Hiring Lead", "Recruiter Email", "Dossier Folder", "EML File"]
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for i, p in enumerate(pkgs, 1):
        folder = p["folder_name"]
        eml_name = f"MNC_{i:02d}_{folder}.eml"
        w.writerow({
            "Index": i,
            "Company Name": p["company"],
            "Tier": p["tier"],
            "Tech Corridor": p["corridor"],
            "Target Role": p["role"],
            "Median CTC (INR)": p["median_ctc"],
            "Hiring Lead": p["hiring_lead"],
            "Recruiter Email": p["recruiter_email"],
            "Dossier Folder": folder,
            "EML File": eml_name
        })

# 2. Export Markdown Dossier
md_path = root / "TOP_50_MNC_STRIKE_DOSSIER.md"
lines = [
    "# TOP 50 MULTINATIONAL CORPORATIONS (MNCs) — APPLICATION & STRIKE DOSSIER",
    "",
    "**Candidate**: Aditya Mehra (BBA International Business, DSU Class of 2026)",
    f"**Total MNC Packages Prepared**: {len(pkgs)} Companies",
    f"**Direct Ready-to-Send Drafts**: {len(pkgs)} `.eml` Files in `applications_generated/eml_outbox/`",
    "",
    "---",
    "",
    "| # | Company | Tech Corridor | Target Role | Est CTC Band | Direct Email | Dossier Links | Ready EML |",
    "| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
]

for i, p in enumerate(pkgs, 1):
    co = p["company"]
    cor = p["corridor"]
    role = p["role"]
    ctc_val = p["median_ctc"] / 100000.0
    ctc = f"Rs {ctc_val:.1f}L"
    email = p["recruiter_email"]
    folder = p["folder_name"]
    eml = f"MNC_{i:02d}_{folder}.eml"
    resume_link = f"[Resume](file:///e:/anti/applications_generated/{folder}/tailored_resume.md)"
    letter_link = f"[Letter](file:///e:/anti/applications_generated/{folder}/cover_letter.md)"
    star_link = f"[STAR](file:///e:/anti/applications_generated/{folder}/interview_star_prep.md)"
    eml_link = f"[`{eml}`](file:///e:/anti/applications_generated/eml_outbox/{eml})"
    
    row = f"| {i} | **{co}** | {cor} | {role} | {ctc} | `{email}` | {resume_link} / {letter_link} / {star_link} | {eml_link} |"
    lines.append(row)

with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Successfully generated {len(pkgs)} MNC targets in {csv_path} and {md_path}")
