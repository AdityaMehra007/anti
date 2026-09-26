"""Full system validation script - checks every component for correctness."""
import sys
import os
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("e:/anti")
passed = 0
failed = 0
issues = []

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name}")
    else:
        failed += 1
        issues.append(f"{name}: {detail}")
        print(f"  [FAIL] {name} -- {detail}")

print("=" * 70)
print("FULL SYSTEM VALIDATION")
print("=" * 70)

# 1. Data files
print("\n--- DATA FILES ---")
profile_path = ROOT / "data" / "verified_profile.json"
check("verified_profile.json exists", profile_path.exists())
if profile_path.exists():
    p = json.loads(profile_path.read_text(encoding="utf-8"))
    c = p.get("candidate", {})
    check("Profile name correct", c.get("full_name") == "Aditya Mehra")
    check("Profile email correct", c.get("email") == "adityamehra799@gmail.com")
    check("Profile phone correct", "70034" in c.get("phone", ""))
    edu = p.get("education", [])
    if edu:
        check("CGPA omitted from profile per directive", "cgpa" not in edu[0] or not edu[0].get("cgpa"))

agencies_path = ROOT / "data" / "bangalore_job_agencies.json"
check("bangalore_job_agencies.json exists", agencies_path.exists())
if agencies_path.exists():
    a = json.loads(agencies_path.read_text(encoding="utf-8"))
    check("Agencies count >= 15", len(a) >= 15, f"found {len(a)}")

roles_path = ROOT / "data" / "target_roles.json"
check("target_roles.json exists", roles_path.exists())

funded_path = ROOT / "data" / "bangalore_funded_startups_and_global_mncs.json"
check("bangalore_funded_startups_and_global_mncs.json exists", funded_path.exists())
if funded_path.exists():
    fc = json.loads(funded_path.read_text(encoding="utf-8"))
    check("Funded & Global MNCs count >= 40", len(fc) >= 40, f"found {len(fc)}")

mass_path = ROOT / "data" / "bangalore_mass_and_bulk_hiring.json"
check("bangalore_mass_and_bulk_hiring.json exists", mass_path.exists())
if mass_path.exists():
    mc = json.loads(mass_path.read_text(encoding="utf-8"))
    check("Mass & Bulk Hiring count >= 15", len(mc) >= 15, f"found {len(mc)}")

mega_path = ROOT / "data" / "bangalore_4500_companies_master.json"
check("bangalore_4500_companies_master.json exists", mega_path.exists())
if mega_path.exists():
    mega_data = json.loads(mega_path.read_text(encoding="utf-8"))
    check("Bangalore 4,500 Master count == 4500", len(mega_data) == 4500, f"found {len(mega_data)}")

tp_path = ROOT / "data" / "bangalore_tech_parks_master.json"
check("bangalore_tech_parks_master.json exists", tp_path.exists())
if tp_path.exists():
    tp_data = json.loads(tp_path.read_text(encoding="utf-8"))
    check("Bangalore Tech Parks count == 20", len(tp_data) == 20, f"found {len(tp_data)}")

inv_path = ROOT / "data" / "all_agents_and_skills_inventory.json"
check("all_agents_and_skills_inventory.json exists", inv_path.exists())
if inv_path.exists():
    inv_data = json.loads(inv_path.read_text(encoding="utf-8"))
    total_assets = inv_data.get("summary", {}).get("grand_total", 0)
    check("AI Assets Inventory grand_total >= 7000", total_assets >= 7000, f"found {total_assets}")

# 2. Core engines
print("\n--- CORE ENGINES ---")
core_engines = [
    "job_matching_100pt.py", "ats_optimizer.py", "skill_gap_engine.py",
    "interview_engine_30q.py", "resume_vault.py", "daily_cadence.py", "career_copilot.py"
]
for eng in core_engines:
    check(f"core/{eng} exists", (ROOT / "core" / eng).exists())

# 3. PDF Resumes
print("\n--- PDF RESUMES ---")
pdf_dir = ROOT / "resumes_pdf"
check("resumes_pdf/ directory exists", pdf_dir.exists())
if pdf_dir.exists():
    pdfs = list(pdf_dir.glob("*.pdf"))
    check(f"PDF count >= 13", len(pdfs) >= 13, f"found {len(pdfs)}")
    small_pdfs = [f.name for f in pdfs if f.stat().st_size < 5000]
    check("No corrupted/tiny PDFs", len(small_pdfs) == 0, f"small: {small_pdfs}")

# 4. Email drafts
print("\n--- EMAIL DRAFTS ---")
eml_dir = ROOT / "applications_generated" / "agency_eml_outbox"
check("agency_eml_outbox/ exists", eml_dir.exists())
if eml_dir.exists():
    emls = list(eml_dir.glob("*.eml"))
    check(f"EML count >= 15", len(emls) >= 15, f"found {len(emls)}")
    for eml in emls:
        content = eml.read_text(encoding="utf-8")
        if "70034" not in content:
            issues.append(f"{eml.name}: missing correct phone")
            failed += 1
            print(f"  [FAIL] {eml.name} missing correct phone")
        if "adityamehra799@gmail.com" not in content:
            issues.append(f"{eml.name}: missing correct email")
            failed += 1
            print(f"  [FAIL] {eml.name} missing correct email")
    if all("70034" in e.read_text(encoding="utf-8") for e in emls):
        passed += 1
        print("  [PASS] All EMLs have correct phone")
    if all("adityamehra799@gmail.com" in e.read_text(encoding="utf-8") for e in emls):
        passed += 1
        print("  [PASS] All EMLs have correct email")

# 5. HTML apps
print("\n--- HTML APPS ---")
apps_to_check = {
    "Clipboard Assistant": ROOT / "apps" / "candidate_clipboard_assistant.html",
    "Fast-Track Portal": ROOT / "apps" / "fast_track_bangalore_portal.html",
    "Main Dashboard": ROOT / "apps" / "get_me_hired_dashboard" / "index.html",
    "Agency Studio": ROOT / "apps" / "job_application_studio" / "bangalore_agency_studio.html",
    "Global MNC & Startup Hub": ROOT / "apps" / "job_application_studio" / "global_mnc_and_startup_hub.html",
    "Non-Stop 4500 Outreach Studio": ROOT / "apps" / "job_application_studio" / "bangalore_non_stop_outreach_studio.html",
    "Tech Parks Studio": ROOT / "apps" / "job_application_studio" / "bangalore_tech_parks_studio.html",
    "AI Workforce Explorer": ROOT / "apps" / "job_application_studio" / "agents_and_skills_explorer.html",
    "Apps Index": ROOT / "apps" / "index.html",
}
for name, path in apps_to_check.items():
    check(f"{name} exists", path.exists())
    if path.exists():
        content = path.read_text(encoding="utf-8")
        check(f"{name} not empty", len(content) > 500, f"only {len(content)} bytes")
        # Check for stale data
        if "91483" in content:
            issues.append(f"{name}: contains OLD phone number 91483")
            failed += 1
            print(f"  [FAIL] {name} has old phone number")

# 6. Clipboard assistant content validation
print("\n--- CLIPBOARD ASSISTANT CONTENT ---")
clip_path = ROOT / "apps" / "candidate_clipboard_assistant.html"
if clip_path.exists():
    cc = clip_path.read_text(encoding="utf-8")
    check("Has correct phone", "70034" in cc)
    check("Has correct email", "adityamehra799@gmail.com" in cc)
    check("Has name", "Aditya Mehra" in cc)
    check("No old phone", "91483" not in cc)

# 7. Fast-track portal content
print("\n--- FAST-TRACK PORTAL CONTENT ---")
ft_path = ROOT / "apps" / "fast_track_bangalore_portal.html"
if ft_path.exists():
    fc = ft_path.read_text(encoding="utf-8")
    check("Has Naukri link", "naukri.com" in fc)
    check("Has LinkedIn link", "linkedin.com" in fc)
    check("Has Indeed link", "indeed.com" in fc)

# 8. HTML resumes
print("\n--- HTML RESUMES ---")
resume_dir = ROOT / "resumes"
if resume_dir.exists():
    html_resumes = list(resume_dir.glob("*.html"))
    check(f"HTML resume count >= 12", len(html_resumes) >= 12, f"found {len(html_resumes)}")
    stale_resumes = []
    for r in html_resumes:
        rc = r.read_text(encoding="utf-8")
        if "91483" in rc:
            stale_resumes.append(r.name)
    check("No HTML resumes with old phone", len(stale_resumes) == 0, f"stale: {stale_resumes}")

# 9. Master orchestrator
print("\n--- MASTER ORCHESTRATOR ---")
orch = ROOT / "adi_career_os_ultimate.py"
check("adi_career_os_ultimate.py exists", orch.exists())
if orch.exists():
    oc = orch.read_text(encoding="utf-8")
    check("Has dashboard launcher", "launch_dashboard" in oc)
    check("Has payload generator", "get_full_dashboard_payload" in oc)
    check("Has CLI parser", "argparse" in oc)

# 10. Scripts
print("\n--- SCRIPTS ---")
scripts_needed = [
    "apply_all_agencies_bangalore.py",
    "dispatch_all_emails_smtp.py",
    "compile_all_resumes_to_pdf.py",
    "compile_mass_and_bulk_hiring.py",
    "compile_4500_non_stop_engine.py",
    "non_stop_outreach_dispatcher.py",
    "generate_4500_studio_html.py",
    "compile_bangalore_tech_parks_and_agent_catalog.py",
    "tech_park_dispatcher.py",
    "agent_skills_inspector.py",
    "generate_tech_parks_studio_html.py",
    "generate_agents_and_skills_explorer_html.py",
]
for s in scripts_needed:
    check(f"scripts/{s} exists", (ROOT / "scripts" / s).exists())

# 11. CSV export
print("\n--- CSV EXPORT ---")
csv_path = ROOT / "BANGALORE_JOB_AGENCIES_MASTER.csv"
check("Agency CSV exists", csv_path.exists())
if csv_path.exists():
    lines = csv_path.read_text(encoding="utf-8").strip().split("\n")
    check(f"CSV has header + data rows", len(lines) >= 16, f"found {len(lines)} lines")

global_csv_path = ROOT / "BANGALORE_FUNDED_STARTUPS_AND_GLOBAL_MNCS_MASTER.csv"
check("Funded & Global MNCs CSV exists", global_csv_path.exists())
if global_csv_path.exists():
    glines = global_csv_path.read_text(encoding="utf-8").strip().split("\n")
    check(f"Global MNC CSV has header + data rows", len(glines) >= 41, f"found {len(glines)} lines")

mass_csv_path = ROOT / "BANGALORE_MASS_AND_BULK_HIRING_MASTER.csv"
check("Mass & Bulk Hiring CSV exists", mass_csv_path.exists())
if mass_csv_path.exists():
    mlines = mass_csv_path.read_text(encoding="utf-8").strip().split("\n")
    check(f"Mass Hiring CSV has header + data rows", len(mlines) >= 16, f"found {len(mlines)} lines")

mega_csv_path = ROOT / "BANGALORE_4500_ALL_COMPANIES_NON_STOP_OUTREACH.csv"
check("4,500 All Companies Master CSV exists", mega_csv_path.exists())
if mega_csv_path.exists():
    megalines = mega_csv_path.read_text(encoding="utf-8-sig").strip().split("\n")
    check(f"4,500 Master CSV has header + data rows", len(megalines) >= 4501, f"found {len(megalines)} lines")

tp_csv_path = ROOT / "BANGALORE_TECH_PARKS_AND_COMPANIES_DIRECTORY.csv"
check("Tech Parks Directory CSV exists", tp_csv_path.exists())
if tp_csv_path.exists():
    tplines = tp_csv_path.read_text(encoding="utf-8").strip().split("\n")
    check(f"Tech Parks CSV has header + data rows", len(tplines) >= 71, f"found {len(tplines)} lines")

cat_csv_path = ROOT / "AGENTS_AND_SKILLS_MASTER_CATALOG.csv"
check("Agents & Skills Catalog CSV exists", cat_csv_path.exists())
if cat_csv_path.exists():
    catlines = cat_csv_path.read_text(encoding="utf-8").strip().split("\n")
    check(f"Catalog CSV has header + data rows", len(catlines) >= 7000, f"found {len(catlines)} lines")

# 12. Windows Batch Launchers
print("\n--- WINDOWS BATCH LAUNCHERS ---")
launchers = [
    "GET_ME_HIRED.bat",
    "APPLY_BBA_IB_BANGALORE.bat",
    "LAUNCH_NON_STOP_OUTREACH.bat",
]
for lb in launchers:
    check(f"{lb} exists", (ROOT / lb).exists())

# Summary
print("\n" + "=" * 70)
print(f"RESULTS: {passed} PASSED / {failed} FAILED")
print("=" * 70)
if issues:
    print("\nISSUES TO FIX:")
    for i in issues:
        print(f"  - {i}")
else:
    print("\nALL CLEAR - SYSTEM IS FULLY OPERATIONAL")
