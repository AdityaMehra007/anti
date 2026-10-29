"""
Sync Bangalore Live Referral Dockets into data/approval_queue.csv & data/approval_queue.json
"""

import os
import json
import csv
from datetime import datetime

EXPECTED_QUEUE_HEADERS = [
    'Action ID', 'Person', 'Company', 'Job', 'Channel',
    'Draft Message', 'Reason / Evidence', 'Priority',
    'Approval Required', 'Status', 'Staged Timestamp',
    'Approved Timestamp', 'Dispatched Timestamp', 'Dispatch Packet'
]

def sync_queue(dry_run=False):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(root_dir, 'data')
    
    project_dockets = os.path.join(root_dir, 'teamwork_projects', 'bangalore_referral_strike', 'bangalore_live_referral_dockets.json')
    data_dockets = os.path.join(data_dir, 'bangalore_live_referral_dockets.json')
    dockets_path = project_dockets if os.path.exists(project_dockets) else data_dockets
    
    queue_csv = os.path.join(data_dir, 'approval_queue.csv')
    queue_json = os.path.join(data_dir, 'approval_queue.json')
    
    with open(dockets_path, 'r', encoding='utf-8') as f:
        targets = json.load(f)
        
    # Read existing queue
    existing_actions = []
    existing_keys = set()
    if os.path.exists(queue_csv):
        with open(queue_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing_actions.append(r)
                p = (r.get('Person') or '').strip().lower()
                c = (r.get('Company') or '').strip().lower()
                j = (r.get('Job') or '').strip().lower()
                existing_keys.add((p, c, j))
                
    staged_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_actions = []
    
    # Sequence numbering strictly continues after max existing ID
    max_id = 0
    for r in existing_actions:
        act_id = r.get('Action ID', '')
        if '-' in act_id:
            try:
                num = int(act_id.split('-')[1])
                if num > max_id:
                    max_id = num
            except (ValueError, IndexError):
                pass
                
    action_counter = max_id + 1
    
    for t in targets:
        comp = t.get('canonical_company', t.get('company'))
        job_title = t.get('job_title', '')
        job_id = t.get('job_id', '')
        job_descriptor = f"{job_id}: {job_title}"
        corridor = t.get('corridor', '')
        
        for c in t.get('contacts', []):
            person = c.get('full_name', '')
            key_norm = (person.strip().lower(), comp.strip().lower(), job_descriptor.strip().lower())
            if key_norm in existing_keys:
                continue
                
            act_id = f"REF-{action_counter:04d}"
            action_counter += 1
            
            pos = c.get('position', '').lower()
            is_recruiter = c.get('is_recruiter') is True or any(
                k in pos for k in ['recruiter', 'talent acquisition', 'sourcing', 'talent partner']
            )
            channel = 'LinkedIn Recruiter InMail' if is_recruiter else 'LinkedIn Employee Referral'
            
            draft_msg = c.get('referral_ask', '')
            reason = f"Bengaluru Tech Corridor: {corridor} | Verified Profile Match | LinkedIn Referral Target"
            
            dispatch_packet = json.dumps({
                'linkedin_url': c.get('linkedin_url', ''),
                'connection_note': c.get('connection_note', ''),
                'referral_docket': c.get('referral_docket', ''),
                'job_url': t.get('job_url', '')
            })
            
            action_obj = {
                'Action ID': act_id,
                'Person': person,
                'Company': comp,
                'Job': job_descriptor,
                'Channel': channel,
                'Draft Message': draft_msg,
                'Reason / Evidence': reason,
                'Priority': 'P0 - Bangalore Live Opening',
                'Approval Required': 'TRUE',
                'Status': 'STAGED_READY',
                'Staged Timestamp': staged_timestamp,
                'Approved Timestamp': '',
                'Dispatched Timestamp': '',
                'Dispatch Packet': dispatch_packet
            }
            new_actions.append(action_obj)
            existing_keys.add(key_norm)
            
    print(f"Existing actions in approval queue: {len(existing_actions)}")
    print(f"New referral actions to stage: {len(new_actions)}")
    
    if dry_run:
        print("[DRY RUN] No files written.")
        return len(new_actions)
        
    all_actions = existing_actions + new_actions
    
    # Write CSV
    with open(queue_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=EXPECTED_QUEUE_HEADERS)
        writer.writeheader()
        writer.writerows(all_actions)
        
    # Write JSON
    with open(queue_json, 'w', encoding='utf-8') as f:
        json.dump(all_actions, f, indent=2)
        
    print(f"Successfully synced {len(all_actions)} total actions to approval_queue.csv and approval_queue.json.")
    return len(new_actions)

if __name__ == '__main__':
    import sys
    dry = '--dry-run' in sys.argv
    sync_queue(dry_run=dry)
