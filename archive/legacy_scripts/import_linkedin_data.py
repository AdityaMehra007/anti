"""
LinkedIn Data Archive Auto-Importer & Resume Personalizer
Scans e:\\anti for LinkedIn Data export files (ZIP or CSVs) and automatically
parses your profile, education, experience, and skills into your application files.
"""

import os
import sys
import csv
import json
import zipfile
from pathlib import Path

WORKSPACE = Path(__file__).parent

def find_linkedin_data():
    """Scans workspace for LinkedIn ZIP archive or extracted CSV files."""
    zip_files = list(WORKSPACE.glob("*.zip"))
    csv_files = list(WORKSPACE.glob("*.csv"))
    
    extracted = False
    # If a ZIP archive is present, extract it
    for zf in zip_files:
        try:
            print(f"Extracting LinkedIn archive: {zf.name}...")
            with zipfile.ZipFile(zf, 'r') as zip_ref:
                zip_ref.extractall(WORKSPACE / "linkedin_export")
            extracted = True
            break
        except Exception as e:
            print(f"Note: Could not extract {zf.name}: {e}")
            
    export_dir = WORKSPACE / "linkedin_export" if extracted else WORKSPACE
    return export_dir

def parse_profile(export_dir):
    data = {
        "name": "",
        "headline": "",
        "summary": "",
        "positions": [],
        "education": [],
        "skills": []
    }
    
    # 1. Parse Profile.csv
    profile_csv = export_dir / "Profile.csv"
    if profile_csv.exists():
        with open(profile_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                first = row.get("First Name", "")
                last = row.get("Last Name", "")
                data["name"] = f"{first} {last}".strip()
                data["headline"] = row.get("Headline", "")
                data["summary"] = row.get("Summary", "")

    # 2. Parse Positions.csv
    pos_csv = export_dir / "Positions.csv"
    if pos_csv.exists():
        with open(pos_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data["positions"].append({
                    "company": row.get("Company Name", ""),
                    "title": row.get("Title", ""),
                    "start": row.get("Started On", ""),
                    "end": row.get("Finished On", "Present"),
                    "description": row.get("Description", "")
                })

    # 3. Parse Education.csv
    edu_csv = export_dir / "Education.csv"
    if edu_csv.exists():
        with open(edu_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data["education"].append({
                    "school": row.get("School Name", ""),
                    "degree": row.get("Degree Name", ""),
                    "start": row.get("Start Date", ""),
                    "end": row.get("End Date", ""),
                    "notes": row.get("Notes", "")
                })

    # 4. Parse Skills.csv
    skills_csv = export_dir / "Skills.csv"
    if skills_csv.exists():
        with open(skills_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                skill_name = row.get("Name", "")
                if skill_name:
                    data["skills"].append(skill_name)
                    
    return data

def update_resume_with_linkedin(profile_data):
    resume_path = WORKSPACE / "Resume_BBA_International_Business.md"
    if not resume_path.exists():
        print("Resume template not found.")
        return

    name = profile_data.get("name") or "CANDIDATE NAME"
    headline = profile_data.get("headline") or "BBA International Business Specialization"
    summary = profile_data.get("summary") or "BBA graduate specializing in International Business, global trade, and operations."
    
    skills_str = ", ".join(profile_data.get("skills", [])[:15]) if profile_data.get("skills") else "Incoterms 2020, EXIM, MS Excel, Power BI, Business Analysis"

    content = f"""# {name.upper()}
**Bangalore, Karnataka, India** | **linkedin.com/in/profile**

---

## PROFESSIONAL SUMMARY
{summary}

**Headline Focus:** {headline}

---

## CORE SKILLS & COMPETENCIES
- **Imported Skills**: {skills_str}
- **Global Trade & EXIM**: Incoterms 2020, Customs Clearance, Export-Import Procedures, Trade Compliance.
- **Analytics & Tools**: MS Excel (VLOOKUP, Pivot Tables), Power BI, SQL Queries, Market Entry Research.

---

## WORK & INTERNSHIP EXPERIENCE
"""

    for pos in profile_data.get("positions", []):
        content += f"""
### {pos['title']} - {pos['company']}
*{pos['start']} to {pos['end']}*
{pos['description']}
"""

    content += "\n---\n\n## EDUCATION\n"
    for edu in profile_data.get("education", []):
        content += f"""
### {edu['degree']}
*{edu['school']} | {edu['start']} - {edu['end']}*
{edu['notes']}
"""

    with open(resume_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ Successfully updated {resume_path.name} with LinkedIn profile data for {name}!")

def main():
    print("=" * 60)
    print("LINKEDIN DATA IMPORTER & RESUME PERSONALIZER")
    print("=" * 60)
    
    export_dir = find_linkedin_data()
    profile = parse_profile(export_dir)
    
    if not profile["name"] and not profile["positions"] and not profile["skills"]:
        print("\n📌 No LinkedIn export files detected in e:\\anti yet.")
        print("Please place your LinkedIn export ZIP file or CSV files (Profile.csv, Positions.csv, etc.) into e:\\anti")
        print("Then run this script again: python import_linkedin_data.py")
    else:
        print(f"\nSuccessfully parsed LinkedIn profile for: {profile['name']}")
        print(f"- Positions found: {len(profile['positions'])}")
        print(f"- Education entries: {len(profile['education'])}")
        print(f"- Skills found: {len(profile['skills'])}")
        update_resume_with_linkedin(profile)

if __name__ == "__main__":
    main()
