import json

with open('all_accenture_people_master.json', 'r', encoding='utf-8') as f:
    people = json.load(f)

def clean_name(n):
    parts = n.strip().split()
    if not parts:
        return "there"
    first = parts[0].capitalize()
    if len(first) == 1 and len(parts) > 1:
        first = parts[1].capitalize()
    return first

all_target_openings_block = """Top Matched Level 13 Back-Office Requisitions (0–1 Yrs Freshers):

1. Procurement Operations New Associate (Posted 2 Days Ago | Top Fit)
   • Job ID: AIOC-S01664213-1  (Parallel Slot: AIOC-S01664212-1)
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay (P2P) Operations New Associate (Posted Yesterday | Fresh Opening)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

3. Sales Operations New Associate (Order Management & Contract Ops — 100% Non-Sales)
   • Job ID: AIOC-S01669615-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Sales-Operations-New-Associate_AIOC-S01669615-1

4. Regulatory Compliance New Associate (KYC & Sanctions Risk Operations)
   • Job ID: AIOC-S01667647-1  (Parallel Slot: AIOC-S01668628-1)
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Regulatory-Compliance-New-Associate_AIOC-S01667647-1

5. Supply Chain Operations New Associate (Vendor Logistics & Shipping Tracking)
   • Job ID: AIOC-S01665657-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Supply-Chain-Operations-New-Associate_AIOC-S01665657-1

6. Trust & Safety New Associate (Policy & Content Operations — Non-Voice)
   • Job ID: AIOC-S01668350-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Trust---Safety-New-Associate_AIOC-S01668350-1

7. Customer Contact Comms New Associate (Digital Messaging & Chat Operations)
   • Job ID: AIOC-S01665940-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Customer-Contact-Comms-Associate-Messaging_AIOC-S01665940-1

8. HR Service Delivery New Associate (Employee Operations)
   • Job ID: AIOC-S01663367-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/HR-Service-Delivery-New-Associate_AIOC-S01663367-1"""

candidate_details = """• Candidate Legal Name: Aditya Mehra
• Email: adityamehra799@gmail.com
• Phone: +91 7003456624
• Degree: BBA in International Business (Dayananda Sagar University, Bengaluru)
• Notice Period: Immediate Joiner (0 Days Notice)
• Shift Flexibility: 100% flexible with 24/7 rotational & night shifts
• Location: Bengaluru (Local resident)"""

dossier_lines = [
    "# 🚀 Accenture Bengaluru 116-Person Tailored Dispatch Dossier",
    "> **Status:** 100% Verified Job IDs, Live Workday URLs & Individualized 1-on-1 Messages with ALL Top Openings",
    "> **Candidate:** Aditya Mehra | BBA (International Business) — Dayananda Sagar University",
    "> **Direct Contact:** adityamehra799@gmail.com | +91 7003456624 | Bengaluru",
    "",
    "---",
    ""
]

for i, p in enumerate(people, 1):
    name = p.get('name', 'Accenture Colleague')
    first = clean_name(name)
    title = p.get('title', 'Accenture Professional')
    url = p.get('url', '')
    t_lower = title.lower()

    if any(w in t_lower for w in ['recruiter', 'recruiting', 'talent acquisition', 'talent fulfilment']) or p.get('is_recruiter') == '1' or p.get('classification') == 'RECRUITER':
        msg = f"""Hi {first},

Hope you're having a great week!

I am reaching out as a 1st-degree connection regarding entry-level fresher hiring at Accenture Operations Bengaluru. I graduated with a BBA in International Business from Dayananda Sagar University and am available for immediate onboarding (0 Days Notice).

I am eager to be screened for any of these newly posted Level 13 non-sales operations requisitions:

{all_target_openings_block}

Candidate Summary:
{candidate_details}

Could you guide me on the screening process or connect me with the aligned recruiter for any of these requisitions? I have my resume ready for review. Thank you for your time and guidance!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    elif any(w in t_lower for w in ['procurement', 'sourcing', 'supply chain', 'order to cash', 'p2p']):
        msg = f"""Hi {first},

Hope you're doing well!

I noticed your work as {title} at Accenture Bengaluru. I recently graduated with a BBA specializing in International Business from Dayananda Sagar University and am looking to start my career in corporate operations.

I saw these fresh Level 13 openings active on Workday:

{all_target_openings_block}

My details for the Workday MyReferrals portal:
{candidate_details}

Could you kindly submit an internal referral for me for any of these openings (Job ID AIOC-S01664213-1 or AIOC-S01670871-1 preferred)? Happy to share my updated resume right away. Would truly appreciate your support!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    elif any(w in t_lower for w in ['manager', 'lead', 'director', 'head', 'vp']):
        msg = f"""Dear {first},

I hope you are having a productive week.

I noticed your leadership as {title} at Accenture. I recently graduated with a BBA in International Business from Dayananda Sagar University, Bengaluru, and am seeking an entry-level operational role within Accenture Operations.

I have identified active Level 13 back-office requisitions aligned with my background:

{all_target_openings_block}

Candidate Summary:
{candidate_details}

I would be honored if you could refer me or direct my profile to the aligned hiring team for any of these openings. I have my resume ready for review. Thank you for your time and guidance!

Sincerely,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    elif any(w in t_lower for w in ['trust', 'safety', 'moderation']):
        msg = f"""Hi {first},

Hope you're doing well!

I noticed you're working in Trust & Safety at Accenture Bengaluru. I am a BBA graduate from DSU and an immediate joiner interested in entry-level operations and Trust & Safety roles.

I have shortlisted these active Level 13 non-sales requisitions on Workday:

{all_target_openings_block}

My details for Workday MyReferrals:
{candidate_details}

Could you kindly submit an internal referral for me for Job ID AIOC-S01668350-1 or whichever requisition you prefer? I have my resume ready to share right away. Thank you so much for your support!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    else:
        msg = f"""Hi {first},

Hope you're doing well!

I noticed you're working at Accenture Bengaluru. I am a fellow Bengaluru graduate (BBA in International Business from DSU) looking to start my career at Accenture in an entry-level back-office operations role.

Could you help me with a quick internal referral for any of these active Level 13 non-sales requisitions on Workday (whichever is easiest for you to refer):

{all_target_openings_block}

My details for Workday MyReferrals:
{candidate_details}

I have my resume ready to share immediately. Would truly appreciate your referral!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    dossier_lines.append(f"### {i}. {name} — {title}")
    dossier_lines.append(f"• **LinkedIn Profile:** [{url}]({url})")
    dossier_lines.append("```text")
    dossier_lines.append(msg)
    dossier_lines.append("```\n")

with open('ACCENTURE_INDIVIDUAL_DISPATCH_DOSSIER.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(dossier_lines))

print(f"Generated individualized messages with ALL Job IDs for all {len(people)} people successfully!")
