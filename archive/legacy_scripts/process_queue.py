import csv
import json
from datetime import datetime

queue_file = r"e:\anti\approval_queue.csv"
output_file = r"e:\anti\outreach_execution_pack.json"

actions = []
priority_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

with open(queue_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('Status') == 'PENDING_APPROVAL':
            priority_raw = row.get('Priority', '')
            if 'P0' in priority_raw:
                priority = 'HIGH'
            elif 'P1' in priority_raw:
                priority = 'MEDIUM'
            else:
                priority = 'LOW'
                
            priority_counts[priority] += 1
            
            action_type = 'Recruiter Outreach' if 'Recruiter' in row.get('Reason / Evidence', '') else 'Connection Request'
            
            contact_name = row.get('Person', '').split(' ')[0]
            company = row.get('Company', '')
            job_full = row.get('Job', '')
            
            template = f"Hi {contact_name},\n\nI hope this message finds you well. I noticed your role at {company}. Given my background in BBA International Business and hands-on event operations experience (Tata Communications, Puma, Aero India), I am very interested in the {job_full} role. I would appreciate the opportunity to connect and learn more about your experience at {company}.\n\nBest regards,\nAditya Mehra"
            
            actions.append({
                "id": row.get('Action ID'),
                "contact_name": row.get('Person'),
                "company": company,
                "action_type": action_type,
                "priority": priority,
                "message_template": template,
                "subject_line": f"Connecting - Opportunities at {company}",
                "status": "TEMPLATE_READY"
            })

output = {
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "total_actions": len(actions),
    "priority_breakdown": priority_counts,
    "actions": actions
}

with open(output_file, mode='w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print("Mission 1 Complete")
