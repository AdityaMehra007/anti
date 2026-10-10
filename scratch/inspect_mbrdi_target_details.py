import json
import re

with open('scratch/mbrdi_all_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

targets = ['235854', '238772', '238171', '240369', '232854', '241197']
with open('scratch/mbrdi_target_roles_details.txt', 'w', encoding='utf-8') as out:
    for j in jobs:
        if j.get('ID') in targets:
            out.write("="*75 + "\n")
            out.write(f"ID: {j.get('ID')} | {j.get('PositionTitle')}\n")
            out.write(f"Department: {j.get('DepartmentName')}\n")
            out.write(f"Start Date: {j.get('PositionStartDate')}\n")
            out.write(f"Apply/Short URI: {j.get('PositionShortURI') or j.get('PositionURI')}\n")
            out.write(f"Referral URL: {j.get('ReferralUrl')}\n")
            for c in j.get('Contact', []):
                out.write(f"Recruiter: {c.get('Name')} <{c.get('Email')}>\n")
            
            desc_list = j.get('PositionFormattedDescription', [])
            for desc_dict in desc_list:
                for k, v in desc_dict.items():
                    out.write(f"\n--- Section: {k} ---\n")
                    clean_v = re.sub(r'<[^<]+?>', '\n', v)
                    lines = [l.strip() for l in clean_v.splitlines() if l.strip()]
                    for l in lines:
                        out.write(f"  {l}\n")
            out.write("\n")

print("Saved detailed descriptions to scratch/mbrdi_target_roles_details.txt")
