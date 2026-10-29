import json
import os

with open(r'e:\anti\teamwork_projects\bangalore_referral_strike\bangalore_live_referral_dockets.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entries: {len(data)}")
for i, item in enumerate(data, 1):
    c_name = item.get('canonical_company', '')
    comp = item.get('company', '')
    role = item.get('job_title', '')
    corridor = item.get('corridor', '')
    contacts_count = len(item.get('contacts', []))
    print(f"{i:2d}. {c_name:<25} | {comp:<30} | {corridor:<25} | {contacts_count} contacts | {role}")
