import os
import json
import csv
from datetime import datetime

root_dir = 'e:\\anti'
data_dir = os.path.join(root_dir, 'data')
project_dockets = os.path.join(root_dir, 'teamwork_projects', 'bangalore_referral_strike', 'bangalore_live_referral_dockets.json')
data_dockets = os.path.join(data_dir, 'bangalore_live_referral_dockets.json')
dockets_path = project_dockets if os.path.exists(project_dockets) else data_dockets
queue_csv = os.path.join(data_dir, 'approval_queue.csv')

with open(dockets_path, 'r', encoding='utf-8') as f:
    targets = json.load(f)

existing_actions = []
existing_keys = set()
with open(queue_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        existing_actions.append(r)
        p = (r.get('Person') or '').strip().lower()
        c = (r.get('Company') or '').strip().lower()
        j = (r.get('Job') or '').strip().lower()
        existing_keys.add((p, c, j))

max_id = 0
for r in existing_actions:
    act_id = r.get('Action ID', '')
    if '-' in act_id:
        try:
            num = int(act_id.split('-')[1])
            if num > max_id:
                max_id = num
        except ValueError:
            pass

print(f"Max existing ID number: {max_id}")

action_counter = max_id + 1
new_actions = []

for t in targets:
    comp = t.get('canonical_company', t.get('company'))
    job_id = t.get('job_id', '')
    job_title = t.get('job_title', '')
    job_desc = f"{job_id}: {job_title}"
    corridor = t.get('corridor', '')
    
    for c in t.get('contacts', []):
        person = c.get('full_name', '')
        key_norm = (person.strip().lower(), comp.strip().lower(), job_desc.strip().lower())
        if key_norm in existing_keys:
            continue
            
        act_id = f"REF-{action_counter:04d}"
        action_counter += 1
        
        pos = c.get('position', '').lower()
        is_rec = c.get('is_recruiter') is True or any(k in pos for k in ['recruiter', 'talent acquisition', 'sourcing', 'talent partner'])
        channel = 'LinkedIn Recruiter InMail' if is_rec else 'LinkedIn Employee Referral'
        
        draft_msg = c.get('referral_ask', '')
        reason = f"Bengaluru Tech Corridor: {corridor} | Verified Profile Match | LinkedIn Referral Target"
        
        packet = json.dumps({
            'linkedin_url': c.get('linkedin_url', ''),
            'connection_note': c.get('connection_note', ''),
            'referral_docket': c.get('referral_docket', ''),
            'job_url': t.get('job_url', '')
        })
        
        action_obj = {
            'Action ID': act_id,
            'Person': person,
            'Company': comp,
            'Job': job_desc,
            'Channel': channel,
            'Draft Message': draft_msg,
            'Reason / Evidence': reason,
            'Priority': 'P0 - Bangalore Live Opening',
            'Approval Required': 'TRUE',
            'Status': 'STAGED_READY',
            'Staged Timestamp': '2026-10-24 23:00:00',
            'Approved Timestamp': '',
            'Dispatched Timestamp': '',
            'Dispatch Packet': packet
        }
        new_actions.append(action_obj)
        existing_keys.add(key_norm)

print(f"New actions to be staged: {len(new_actions)}")
for a in new_actions:
    print(f"  {a['Action ID']} | {a['Person']} | {a['Company']} | {a['Job']} | {a['Channel']}")
