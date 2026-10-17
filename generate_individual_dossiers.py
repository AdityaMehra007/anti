import json
import re

with open('all_accenture_people_master.json', 'r', encoding='utf-8') as f:
    people = json.load(f)

def clean_name(n):
    # Get first name
    parts = n.strip().split()
    if not parts:
        return "there"
    first = parts[0].capitalize()
    # If first name is single letter like 'C'
    if len(first) == 1 and len(parts) > 1:
        first = parts[1].capitalize()
    return first

dossier_lines = [
    "# 🚀 Accenture Bengaluru 116-Person Tailored Dispatch Dossier",
    "> **Status:** 100% Verified Job IDs, Live Workday URLs & Individualized 1-on-1 Messages",
    "> **Candidate:** Aditya Mehra | BBA (International Business) — Dayananda Sagar University",
    "> **Direct Contact:** adityamehra007@gmail.com | +91 7003456624 | Bengaluru",
    "",
    "---",
    ""
]

job_procurement = """• Role: Procurement Operations New Associate (Posted 2 Days Ago)
• Job ID: AIOC-S01664213-1  (Backup: AIOC-S01664212-1)
• Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1"""

job_p2p = """• Role: Procure to Pay Operations New Associate (Posted Yesterday)
• Job ID: AIOC-S01670871-1
• Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1"""

job_salesops = """• Role: Sales Operations New Associate (Order Management — 100% Non-Sales)
• Job ID: AIOC-S01669615-1
• Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Sales-Operations-New-Associate_AIOC-S01669615-1"""

job_trust = """• Role: Trust & Safety New Associate (Non-Voice / Content Moderation)
• Job ID: AIOC-S01668350-1
• Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Trust---Safety-New-Associate_AIOC-S01668350-1"""

candidate_details = """• Candidate Legal Name: Aditya Mehra
• Email: adityamehra007@gmail.com
• Phone: +91 7003456624
• Degree: BBA in International Business (Dayananda Sagar University, Bengaluru)
• Notice Period: Immediate Joiner (0 Days Notice)
• Shift Flexibility: 100% flexible with 24/7 rotational & night shifts
• Location: Bengaluru (Local resident)"""

for i, p in enumerate(people, 1):
    name = p.get('name', 'Accenture Colleague')
    first = clean_name(name)
    title = p.get('title', 'Accenture Professional')
    url = p.get('url', '')
    t_lower = title.lower()

    # Determine tailoring style
    if any(w in t_lower for w in ['recruiter', 'recruiting', 'talent acquisition', 'talent fulfilment']) or p.get('is_recruiter') == '1' or p.get('classification') == 'RECRUITER':
        # Recruiter Message
        msg = f"""Hi {first},

Hope you're having a great week!

I am reaching out as a 1st-degree connection regarding entry-level fresher hiring at Accenture Operations Bengaluru. I graduated with a BBA in International Business from Dayananda Sagar University and am available for immediate onboarding (0 Days Notice).

I am eager to be screened for these newly posted Level 13 non-sales operations requisitions:

1. Procurement Operations New Associate (Posted 2 Days Ago)
   • Job ID: AIOC-S01664213-1  (Backup: AIOC-S01664212-1)
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay Operations New Associate (Posted Yesterday)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

3. Sales Operations New Associate (Order Management — 100% Non-Sales)
   • Job ID: AIOC-S01669615-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Sales-Operations-New-Associate_AIOC-S01669615-1

Candidate Summary:
{candidate_details}

Could you guide me on the screening process or connect me with the aligned recruiter for these requisitions? I have my resume ready for review. Thank you for your time and guidance!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

    elif any(w in t_lower for w in ['procurement', 'sourcing', 'supply chain', 'order to cash', 'p2p']):
        # Procurement Peer Message
        msg = f"""Hi {first},

Hope you're doing well!

I noticed your work as {title} at Accenture Bengaluru. I recently graduated with a BBA specializing in International Business from Dayananda Sagar University and am looking to start my career in corporate procurement operations.

I saw these fresh Level 13 openings active on Workday:
1. Procurement Operations New Associate (Posted 2 Days Ago)
   • Job ID: AIOC-S01664213-1  (Backup: AIOC-S01664212-1)
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay Operations New Associate (Posted Yesterday)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

My details for the Workday MyReferrals portal:
{candidate_details}

Could you kindly submit a quick referral for me for Job ID AIOC-S01664213-1? Happy to share my updated resume right away. Would truly appreciate your support!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

    elif any(w in t_lower for w in ['manager', 'lead', 'director', 'head', 'vp']):
        # Leadership Message
        msg = f"""Dear {first},

I hope you are having a productive week.

I noticed your leadership as {title} at Accenture. I recently graduated with a BBA in International Business from Dayananda Sagar University, Bengaluru, and am seeking an entry-level operational role within Accenture Operations.

I have identified active Level 13 back-office requisitions aligned with my background:
1. Procurement Operations New Associate (Posted 2 Days Ago)
   • Job ID: AIOC-S01664213-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay Operations New Associate (Posted Yesterday)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

Candidate Summary:
{candidate_details}

I would be honored if you could refer me or direct my profile to the aligned hiring team. I have my resume ready for review. Thank you for your time and guidance!

Sincerely,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

    elif any(w in t_lower for w in ['trust', 'safety', 'moderation']):
        # Trust & Safety Peer Message
        msg = f"""Hi {first},

Hope you're doing well!

I noticed you're working in Trust & Safety at Accenture Bengaluru. I am a BBA graduate from DSU and an immediate joiner interested in entry-level Trust & Safety / Content Moderation roles.

Could you kindly submit an internal referral for:
• Trust & Safety New Associate (Non-Voice Screen Review)
• Job ID: AIOC-S01668350-1
• Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Trust---Safety-New-Associate_AIOC-S01668350-1

My details for Workday:
{candidate_details}

I have my resume ready to share right away. Thank you so much for your support!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

    else:
        # General Operations & Engineering Peer Message
        msg = f"""Hi {first},

Hope you're doing well!

I noticed you're working at Accenture Bengaluru. I am a fellow Bengaluru graduate (BBA in International Business from DSU) looking to start my career at Accenture in an entry-level back-office operations role.

Could you help me with a quick internal referral for:
1. Procurement Operations New Associate (Posted 2 Days Ago)
   • Job ID: AIOC-S01664213-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay Operations New Associate (Posted Yesterday)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

My details for Workday MyReferrals:
{candidate_details}

I have my resume ready to share immediately. Would truly appreciate your referral!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

    dossier_lines.append(f"### {i}. {name} — {title}")
    dossier_lines.append(f"• **LinkedIn Profile:** [{url}]({url})")
    dossier_lines.append("```text")
    dossier_lines.append(msg)
    dossier_lines.append("```\n")

with open('ACCENTURE_INDIVIDUAL_DISPATCH_DOSSIER.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(dossier_lines))

print(f"Generated individualized messages for all {len(people)} people successfully!")
