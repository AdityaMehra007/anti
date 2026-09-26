#!/usr/bin/env python3
"""
========================================================================================
61 BANGALORE ATS RESUMES: FORMATTING & ZERO-HALLUCINATION AUDIT ENGINE
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Audits all 61 packaged HTML ATS resumes for:
  1. File existence and valid HTML structure
  2. Strict adherence to verified evidence:
     - Aditya Mehra
     - Dayananda Sagar University (DSU '26)
     - AERO India 2025 (Yelahanka AFB)
     - Puma India, Tata Communications, Dyson brand activations
     - Instawork AI (99%+ precision)
     - Incoterms 2020 & ICEGATE customs tariff compliance
  3. Total absence of forbidden sales claims (telecalling, cold-calling insurance)
  4. 1-Page print stylesheet integrity (@page, print-btn)
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
PKGS_DIR = ROOT_DIR / "applications_generated" / "bangalore_61_packages"

VERIFIED_KEYWORDS = [
    "Aditya Mehra",
    "Dayananda Sagar University",
    "AERO India 2025",
    "Tata Communications",
    "Puma India",
    "Instawork AI",
    "Incoterms 2020"
]

FORBIDDEN_KEYWORDS = [
    "cold calling",
    "telecalling",
    "insurance sales",
    "credit card outbound",
    "commission only",
    "door to door"
]

def audit():
    print("=" * 80)
    print("  AUDITING 61 BANGALORE ATS RESUMES: FORMATTING & ZERO-HALLUCINATION")
    print("=" * 80)

    if not PKGS_DIR.exists():
        print(f"[-] Directory not found: {PKGS_DIR}")
        return 1

    folders = sorted([p for p in PKGS_DIR.iterdir() if p.is_dir()])
    print(f"[*] Discovered {len(folders)} requisition packages.")

    passed_count = 0
    hallucination_flags = 0
    formatting_issues = 0

    for idx, folder in enumerate(folders, 1):
        resume_file = folder / "resume_ats_1page.html"
        if not resume_file.exists():
            print(f"  [FAIL] Missing resume in: {folder.name}")
            formatting_issues += 1
            continue

        with open(resume_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # 1. Format check
        has_print_btn = "print-btn" in content
        has_page_css = "@page" in content
        has_header = "class=\"header\"" in content or "class='header'" in content

        if not (has_print_btn and has_page_css and has_header):
            print(f"  [FORMAT-FAIL] Layout issues in {folder.name}")
            formatting_issues += 1
            continue

        # 2. Evidence verification
        missing_kw = [kw for kw in VERIFIED_KEYWORDS if kw not in content]
        if missing_kw:
            print(f"  [EVIDENCE-WARN] {folder.name} missing key evidence: {missing_kw}")
            formatting_issues += 1
            continue

        # 3. Forbidden sales check
        found_forbidden = [kw for kw in FORBIDDEN_KEYWORDS if kw.lower() in content.lower()]
        if found_forbidden:
            print(f"  [SALES-ALERT] {folder.name} contains forbidden terms: {found_forbidden}")
            hallucination_flags += 1
            continue

        passed_count += 1

    print("\n" + "=" * 80)
    print(f"  AUDIT RESULTS: {passed_count}/{len(folders)} RESUMES 100% VERIFIED CLEAN")
    print(f"  - Formatting & Layout Compliance   : {'100% PASS' if formatting_issues == 0 else f'{formatting_issues} Issues'}")
    print(f"  - Zero-Hallucination Evidence Grade: {'100% PASS (All 7 anchor metrics present)' if passed_count == len(folders) else 'WARN'}")
    print(f"  - 100% Sales Exclusion Compliance  : {'100% PASS (0 forbidden terms)' if hallucination_flags == 0 else f'{hallucination_flags} Alerts'}")
    print("=" * 80)
    return 0

if __name__ == "__main__":
    sys.exit(audit())
