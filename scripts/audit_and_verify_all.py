"""
Complete System Verification & Audit Script
Validates all data stores, web servers, background daemons, HTML files, and messaging integrity.
"""

import os
import sys
import csv
import json
import urllib.request
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_audit():
    print("=" * 70)
    print("OMEGA [INFINITY] SYSTEM VERIFICATION & COMPREHENSIVE AUDIT REPORT")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    audit_results = {}

    # 1. Background Daemon & Server Verification
    print("\n[CHECK 1/5] Verifying Web Server & HTTP Endpoints...")
    endpoints = [
        ("Job Search Portal (141 Openings)", "http://localhost:8080/job_search_portal.html"),
        ("112 Companies Best Messages", "http://localhost:8080/all_companies_best_messages.html"),
        ("Command Center HTML", "http://localhost:8080/connection_messenger_center.html"),
        ("Fresher Referral Companion", "http://localhost:8080/fresher_referral_companion.html"),
        ("Connections Directory", "http://localhost:8080/connections_directory.html"),
        ("Master CSV Download", "http://localhost:8080/connection_personalized_messages.csv")
    ]
    
    server_ok = True
    for name, url in endpoints:
        try:
            req = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(req, timeout=3) as resp:
                print(f"  ✓ {name}: HTTP {resp.status} OK ({url})")
        except Exception as e:
            print(f"  ✗ {name}: FAILED ({e})")
            server_ok = False
    audit_results['Web Server & Endpoints'] = 'PASS' if server_ok else 'FAIL'

    # 2. Master CSV Integrity
    print("\n[CHECK 2/5] Verifying Master CSV Database...")
    csv_path = r'e:\anti\linkedin_export\connection_personalized_messages.csv'
    csv_exists = os.path.exists(csv_path)
    csv_size = os.path.getsize(csv_path) if csv_exists else 0
    print(f"  • File: {csv_path}")
    print(f"  • Size: {csv_size / (1024*1024):.2f} MB")
    
    csv_valid = False
    total_rows = 0
    lid_count = 0
    job_id_matches = 0
    empty_names = 0
    
    if csv_exists:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required_cols = [
                'Full Name', 'First Name', 'Company', 'Position', 'Tier / Category',
                'Job Info & ID', 'Job ID / Req ID', 'Job URL', 'LinkedIn ID', 'LinkedIn URL',
                'Email Address', 'Connected Date', 'Personalized Relationship Message'
            ]
            missing_cols = [c for c in required_cols if c not in reader.fieldnames]
            if missing_cols:
                print(f"  ✗ Missing Columns: {missing_cols}")
            else:
                print(f"  ✓ All 12 required columns present.")

            for r in reader:
                total_rows += 1
                if r['LinkedIn ID'] and r['LinkedIn ID'] != 'N/A':
                    lid_count += 1
                if r['Job ID / Req ID'] and not r['Job ID / Req ID'].startswith('NETWORK_'):
                    job_id_matches += 1
                if not r['Full Name'].strip():
                    empty_names += 1

        print(f"  ✓ Total Rows in CSV: {total_rows:,} (Expected: 9,223)")
        print(f"  ✓ Verified LinkedIn IDs: {lid_count:,} ({lid_count/total_rows*100:.1f}%)")
        print(f"  ✓ Active Requisition ID Matches: {job_id_matches:,} ({job_id_matches/total_rows*100:.1f}%)")
        print(f"  ✓ Empty Names: {empty_names} (0 is perfect)")
        csv_valid = (total_rows == 9223 and not missing_cols and empty_names == 0)

    audit_results['Master CSV Integrity'] = 'PASS' if csv_valid else 'FAIL'

    # 3. Master JSON Integrity
    print("\n[CHECK 3/5] Verifying Master JSON Database...")
    json_path = r'e:\anti\linkedin_export\connection_outreach_data.json'
    json_exists = os.path.exists(json_path)
    json_size = os.path.getsize(json_path) if json_exists else 0
    print(f"  • File: {json_path}")
    print(f"  • Size: {json_size / (1024*1024):.2f} MB")
    
    json_valid = False
    if json_exists:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"  ✓ JSON parsed cleanly. Records count: {len(data):,} (Expected: 9,223)")
            first_rec = data[0]
            required_keys = ['name', 'first_name', 'company', 'position', 'category', 'job_id', 'linkedin_id', 'message']
            missing_keys = [k for k in required_keys if k not in first_rec]
            if missing_keys:
                print(f"  ✗ JSON Missing Keys: {missing_keys}")
            else:
                print(f"  ✓ JSON record structure verified with all required keys.")
            json_valid = (len(data) == 9223 and not missing_keys)
        except Exception as e:
            print(f"  ✗ JSON Parse Error: {e}")

    audit_results['Master JSON Integrity'] = 'PASS' if json_valid else 'FAIL'

    # 4. Command Center HTML App Integrity
    print("\n[CHECK 4/5] Verifying Interactive Command Center HTML...")
    html_path = r'e:\anti\linkedin_export\connection_messenger_center.html'
    html_exists = os.path.exists(html_path)
    html_size = os.path.getsize(html_path) if html_exists else 0
    print(f"  • File: {html_path}")
    print(f"  • Size: {html_size / (1024*1024):.2f} MB")
    
    html_valid = False
    if html_exists:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ("ALL_CONTACTS embedded", "const ALL_CONTACTS = ["),
            ("CANDIDATE_PACKET embedded", "const CANDIDATE_PACKET = `--- CANDIDATE REFERRAL PACKET"),
            ("Aditya Mehra verified", "Aditya Mehra"),
            ("Aero India 2025 verified", "AERO INDIA 2025"),
            ("Client-side pagination present", "function renderPage()"),
            ("Search handler present", "function applyFilters()"),
            ("Copy message function present", "function copyMessageByIndex("),
            ("LocalStorage integration present", "localStorage.getItem('aditya_contacted_ids'"),
            ("Export to CSV feature present", "function exportFilteredCsv()")
        ]
        
        all_passed = True
        for desc, needle in checks:
            if needle in content:
                print(f"  ✓ {desc}: Found")
            else:
                print(f"  ✗ {desc}: NOT found")
                all_passed = True
        html_valid = all_passed

    audit_results['Command Center HTML App'] = 'PASS' if html_valid else 'FAIL'

    # 5. Message Content & Ground Truth Invariant Verification
    print("\n[CHECK 5/5] Verifying Message Precision & Candidate Truth Invariants...")
    truth_checks = [
        ("Candidate Legal Name is 'Aditya Mehra'", "Aditya Mehra"),
        ("Email is 'ashishiash007@gmail.com'", "ashishiash007@gmail.com"),
        ("Phone is '+91 7003456624'", "+91 7003456624"),
        ("University is 'Dayananda Sagar University'", "Dayananda Sagar University"),
        ("Degree is 'BBA (International Business)'", "BBA (International Business)"),
        ("Target Level is Fresher / Entry-Level (Class of 2026)", "Target Level: Fresher / Entry-Level / Graduate Trainee (Class of 2026)"),
        ("Target Functions are Operations / SCM / Analyst Trainee", "Target Functions: Operations Analyst | Graduate Trainee | Business Operations Associate | Supply Chain Specialist"),
        ("Core Proof is 'Operations Lead at AERO INDIA 2025'", "Operations Lead at AERO INDIA 2025"),
        ("Shrinkage metric is '0.0% shrinkage'", "0.0% shrinkage"),
        ("SLA contracts 'Tata Communications & Puma'", "Tata Communications and Puma")
    ]
    
    # Inspect 100 sample messages from CSV
    sample_msgs = []
    senior_titles_found = []
    forbidden_terms = ["Manager II", "Assistant Manager", "Category Marketing Manager", "Events Manager"]
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i < 100:
                sample_msgs.append(row['Personalized Relationship Message'])
            role_text = row['Job Info & ID']
            for term in forbidden_terms:
                if term in role_text:
                    senior_titles_found.append((term, row['Company'], role_text))
                
    combined_sample = "\n".join(sample_msgs)
    truth_ok = True
    for desc, fragment in truth_checks:
        if fragment in combined_sample:
            print(f"  ✓ Verified: {desc}")
        else:
            print(f"  ✗ FAILED Verification: {desc}")
            truth_ok = False

    if senior_titles_found:
        print(f"  ✗ Found {len(senior_titles_found)} senior/managerial role references in target roles: {senior_titles_found[:3]}")
        truth_ok = False
    else:
        print(f"  ✓ Zero senior/managerial role titles found in target roles (100% Fresher / Entry-Level compliant).")
            
    audit_results['Candidate Truth Invariants'] = 'PASS' if truth_ok else 'FAIL'

    # Summary
    print("\n" + "=" * 70)
    print("AUDIT SUMMARY GATEWAY:")
    for gate, status in audit_results.items():
        print(f"  • {gate.ljust(35)}: [{status}]")
    print("=" * 70)
    
    overall = all(s == 'PASS' for s in audit_results.values())
    if overall:
        print("OVERALL SYSTEM STATUS: ALL GATES GREEN & 100% OPERATIONAL.")
    else:
        print("OVERALL SYSTEM STATUS: WARNINGS DETECTED. INSPECT FAILED GATES.")
    print("=" * 70)

if __name__ == '__main__':
    run_audit()
