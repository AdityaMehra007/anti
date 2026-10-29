"""
Bengaluru Live Referral Strike CLI Runner (Standalone Project Copy)
"""

import os
import sys
import json
import argparse
import webbrowser
import http.server
import socketserver

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_DIR, 'bangalore_live_referral_dockets.json')

def load_data():
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}.")
        sys.exit(1)
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_targets(data):
    print("=" * 85)
    print(f"{'COMPANY':<28} {'CORRIDOR':<25} {'JOB ROLE':<22} {'CONTACTS':<8}")
    print("=" * 85)
    for t in data:
        comp = t['canonical_company'][:26]
        corr = t['corridor'][:24]
        role = t['job_title'][:20]
        cnt = len(t['contacts'])
        print(f"{comp:<28} {corr:<25} {role:<22} {cnt:<8}")
    print("=" * 85)
    total_contacts = sum(len(t['contacts']) for t in data)
    print(f"Total Companies: {len(data)} | Total Curated Referral Contacts: {total_contacts}")

def show_company(data, company_name):
    matches = [t for t in data if company_name.lower() in t['canonical_company'].lower() or company_name.lower() in t['company'].lower()]
    if not matches:
        print(f"No company found matching '{company_name}'.")
        return
    for t in matches:
        print("\n" + "=" * 80)
        print(f"Target Company: {t['canonical_company']} ({t['hub']} - {t['corridor']})")
        print(f"Target Role:    {t['job_title']} (ID: {t['job_id']})")
        print(f"Requisition URL:{t['job_url']}")
        print(f"Curated Contacts: {len(t['contacts'])}")
        print("=" * 80)
        for i, c in enumerate(t['contacts'], 1):
            rec_tag = " [RECRUITER]" if c['is_recruiter'] else ""
            print(f"\n[{i}] {c['full_name']} - {c['position']}{rec_tag}")
            print(f"    LinkedIn: {c['linkedin_url']}")
            print(f"    Connection Note (<= 290 chars):")
            print(f"      \"{c['connection_note']}\"")
            print(f"    Referral Ask:")
            for line in c['referral_ask'].split('\n')[:5]:
                print(f"      {line}")
            print("      ...")

def show_docket(data, company_name):
    matches = [t for t in data if company_name.lower() in t['canonical_company'].lower() or company_name.lower() in t['company'].lower()]
    if not matches:
        print(f"No company found matching '{company_name}'.")
        return
    t = matches[0]
    if t['contacts']:
        print(t['contacts'][0]['referral_docket'])
    else:
        print("No contacts available for docket.")

def serve_console(port=8899):
    console_file = os.path.join(CURRENT_DIR, 'index.html')
    if not os.path.exists(console_file):
        print("Error: Console index.html file not found.")
        return
    
    url = f"http://localhost:{port}/index.html"
    print(f"Serving Bengaluru Live Referral Console at {url}")
    print("Press Ctrl+C to stop.")
    
    os.chdir(CURRENT_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

def main():
    parser = argparse.ArgumentParser(description="Bengaluru Live Referral Strike CLI")
    parser.add_argument('--list-targets', action='store_true', help="List all target companies and contact counts")
    parser.add_argument('--company', type=str, help="Show contacts and outreach messages for a specific company")
    parser.add_argument('--docket', type=str, help="Show internal referral submission docket for a company")
    parser.add_argument('--serve-console', nargs='?', const=8899, type=int, help="Serve interactive web console on specified port (default: 8899)")
    args = parser.parse_args()

    data = load_data()

    if args.list_targets:
        list_targets(data)
    elif args.company:
        show_company(data, args.company)
    elif args.docket:
        show_docket(data, args.docket)
    elif args.serve_console:
        serve_console(args.serve_console)
    else:
        list_targets(data)

if __name__ == '__main__':
    main()
