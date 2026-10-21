import csv
import json
import re
import os

csv_path = r'e:\anti\linkedin_export\Connections.csv'
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

header_idx = -1
for i, line in enumerate(lines[:10]):
    if 'First Name' in line:
        header_idx = i
        break

reader = csv.DictReader(lines[header_idx:])
connections = list(reader)

target_jobs_map = {
    'goldman': ('Goldman Sachs', '4452387165', 'Global Banking & Markets Operations - IB Ops Client Onboarding Analyst (Bengaluru)', 'http://www.linkedin.com/jobs/view/4452387165'),
    'jpmorgan': ('JPMorganChase', '4440836681', 'Data Management Associate', 'http://www.linkedin.com/jobs/view/4440836681'),
    'chase': ('JPMorganChase', '4440836681', 'Data Management Associate', 'http://www.linkedin.com/jobs/view/4440836681'),
    'ey': ('EY', '4444908737', 'GDS Meetings and Events - Events Manager', 'http://www.linkedin.com/jobs/view/4444908737'),
    'ernst': ('EY', '4444908737', 'GDS Meetings and Events - Events Manager', 'http://www.linkedin.com/jobs/view/4444908737'),
    'pwc': ('PwC India', '4409108662', 'Associate', 'http://www.linkedin.com/jobs/view/4409108662'),
    'pricewaterhouse': ('PwC India', '4409108662', 'Associate', 'http://www.linkedin.com/jobs/view/4409108662'),
    'amazon': ('Amazon', '4443027895 / 4455781999', 'Event Program Manager, AWS Global Events / Supply Chain BA', 'http://www.linkedin.com/jobs/view/4443027895'),
    'aws': ('Amazon Web Services', '4443027895', 'Event Program Manager, AWS Global Events', 'http://www.linkedin.com/jobs/view/4443027895'),
    'accenture': ('Accenture', '4429242140 / 4448338203', 'Business Advisory New Associate / Supply Chain Ops Analyst', 'http://www.linkedin.com/jobs/view/4429242140'),
    'microsoft': ('Microsoft', '4379272973', 'Research Sciences Intern / PM Intern', 'http://www.linkedin.com/jobs/view/4379272973'),
    'razorpay': ('Razorpay', '4439995783', 'Analyst - Business Operations / Merchant Ops Specialist', 'http://www.linkedin.com/jobs/view/4439995783'),
    'cisco': ('Cisco', '4446332173', 'Data Analyst', 'http://www.linkedin.com/jobs/view/4446332173'),
    'hsbc': ('HSBC', '4452434953', 'Business Analyst', 'http://www.linkedin.com/jobs/view/4452434953'),
    'swiggy': ('Swiggy', 'SWIGGY_OPS_001', 'Operations & Expansion Associate', 'https://careers.swiggy.com'),
    'zepto': ('Zepto', 'ZEPTO_OPS_002', 'City Operations Lead - Dark Store SCM', 'https://www.zeptonow.com/careers'),
    'ather': ('Ather Energy', 'ATHER_SC_001', 'Supply Chain & Operations Lead', 'https://www.atherenergy.com/careers'),
    'glean': ('Glean', '4453740312', 'Cost & Commercial Operations Associate', 'https://jobs.ashbyhq.com/glean'),
    'postman': ('Postman', 'POSTMAN_OPS_003', 'Business Operations Analyst', 'https://boards.greenhouse.io/postman'),
    'wrike': ('Wrike', '4440968428', 'Partner Operations Specialist', 'https://boards.greenhouse.io/wrike'),
    'hilton': ('Hilton', '4450278984', 'Events Executive | Conrad Bengaluru', 'http://www.linkedin.com/jobs/view/4450278984'),
    'conrad': ('Hilton', '4450278984', 'Events Executive | Conrad Bengaluru', 'http://www.linkedin.com/jobs/view/4450278984'),
    'marriott': ('JW Marriott', '4436777567', 'Assistant Events Manager', 'http://www.linkedin.com/jobs/view/4436777567'),
    'thomson reuters': ('Thomson Reuters', '4446747144', 'Events Coordinator', 'http://www.linkedin.com/jobs/view/4446747144'),
    'mathworks': ('MathWorks', '4406706536', 'Marketing Event Specialist', 'http://www.linkedin.com/jobs/view/4406706536'),
    'globallogic': ('GlobalLogic', '4451402094', 'Event Marketing Specialist IRC298882', 'http://www.linkedin.com/jobs/view/4451402094'),
    'oracle': ('Oracle', '4048014873', 'Student / Intern (Cloud & Tech)', 'http://www.linkedin.com/jobs/view/4048014873'),
    'coindcx': ('CoinDCX', '4424404412', 'Analyst - Operations', 'http://www.linkedin.com/jobs/view/4424404412'),
    'ust': ('UST', '4441571067', 'Business Operations Support', 'http://www.linkedin.com/jobs/view/4441571067'),
    'wns': ('WNS', '4430704372', 'Bangalore Walkins - Operations', 'http://www.linkedin.com/jobs/view/4430704372'),
    'blissclub': ('Blissclub', '4437012823', 'Business Analyst', 'http://www.linkedin.com/jobs/view/4437012823'),
    'bni': ('BNI Global', '4406514782', 'Event Logistics Coordinator', 'http://www.linkedin.com/jobs/view/4406514782'),
    'galaxeye': ('GalaxEye', '4373303563', 'Market Research Intern', 'http://www.linkedin.com/jobs/view/4373303563'),
    'tyfone': ('Tyfone, Inc.', '4371505461', 'Business Intelligence & Data Analyst Intern', 'http://www.linkedin.com/jobs/view/4371505461'),
    'expedify': ('Expedify', '4374985662', 'AI Product Analytics Intern', 'http://www.linkedin.com/jobs/view/4374985662'),
    'emergent': ('Emergent', '4439983503', 'AI Analyst', 'http://www.linkedin.com/jobs/view/4439983503'),
    'volvo': ('Volvo Construction Equipment', '4429029965', 'Graduate Apprentice Trainee', 'http://www.linkedin.com/jobs/view/4429029965'),
    'inspironlabs': ('InspironLabs', '4370182887', 'Management Trainee', 'http://www.linkedin.com/jobs/view/4370182887'),
    'englishbhashi': ('EnglishBhashi', '4377959748', 'Product Intern', 'http://www.linkedin.com/jobs/view/4377959748'),
    'tata consumer': ('Tata Consumer Products', '4021834253', 'Human Resources Intern', 'http://www.linkedin.com/jobs/view/4021834253'),
    'infrabyte': ('Infrabyte Consulting', '4381181841', 'Data / Business Analyst Intern', 'http://www.linkedin.com/jobs/view/4381181841'),
    'tokens': ('tokens&', '4449673093', 'Operations Associate – Founder Office', 'http://www.linkedin.com/jobs/view/4449673093')
}

def clean_first_name(raw_fn):
    fn = raw_fn.strip()
    fn = re.sub(r'^[^\w]+', '', fn) # remove leading emojis or special chars
    parts = fn.split()
    return parts[0] if parts else 'there'

processed = []
for c in connections:
    raw_fn = c.get('First Name', '').strip()
    ln = c.get('Last Name', '').strip()
    full_name = f"{raw_fn} {ln}".strip()
    first_name = clean_first_name(raw_fn)
    company = c.get('Company', '').strip()
    position = c.get('Position', '').strip()
    url = c.get('URL', '').strip()
    email = c.get('Email Address', '').strip()
    connected_on = c.get('Connected On', '').strip()

    co_lower = company.lower()
    pos_lower = position.lower()

    # Check Tier 1: Target company with exact Job ID
    matched_job = None
    for k, val in target_jobs_map.items():
        if k in co_lower:
            matched_job = val
            break

    if matched_job:
        target_co, jid, jtitle, jurl = matched_job
        category = "Tier 1: Active Job ID Mapped"
        job_info = f"{target_co} | {jtitle} (Job ID: {jid})"
        
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope all is well with you! Always great following your updates and journey at {target_co}.\n\n"
            f"I'm wrapping up my final year in International Business at Dayananda Sagar University. Over the past year, I've had the opportunity to dive deep into high-density operational leadership—most recently leading ground logistics for AERO INDIA 2025 at Yelahanka Air Force Base (100k+ delegates, zero security infractions, 0.0% shrinkage) and managing run-of-show logistics for Tata Communications.\n\n"
            f"I came across the open {jtitle} role at {target_co} (Job ID: {jid}). I've submitted my application through the portal, but more than anything, I would love to connect with someone I know and respect in the organization. If you have 5 minutes sometime, I'd love to hear how your journey has been there and get your perspective on the team.\n\n"
            f"Regardless, wishing you continued success, and please let me know if I can ever support you or your team here in Bengaluru!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )
    elif any(rec_word in pos_lower for rec_word in ['talent', 'recruit', 'hr', 'human resources', 'sourcing', 'people partner']):
        category = "Tier 2: HR & Talent Acquisition"
        job_info = f"General Hiring & Referrals at {company or 'Firm'}"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you are having a productive week! I wanted to reach out, say hello, and strengthen our connection here on LinkedIn.\n\n"
            f"I am a final-year International Business candidate at Dayananda Sagar University, Bengaluru. My background is centered on disciplined operations, supply chain logistics, and high-stakes vendor management—recently leading ground operations at AERO INDIA 2025 (100,000+ attendees, 0 security breaches, 0.0% inventory loss) and enterprise activations for Tata Communications and Puma Global.\n\n"
            f"As your team plans upcoming hiring for operations, business analysis, or program specialist roles, I would love to stay on your radar for opportunities where rigorous operational execution is needed. Would be glad to share my resume whenever convenient.\n\n"
            f"Thank you for all the great work you do, and wishing you a wonderful week ahead!\n\n"
            f"Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )
    elif any(alumni_word in co_lower for alumni_word in ['christ', 'dayananda', 'dsu', 'iisc', 'student welfare', 'cusbma']):
        category = "Tier 3: University & Alumni Network"
        job_info = f"Alumni Reconnect & Mutual Growth"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you're doing great! It's always fantastic to stay connected with fellow peers and alumni from our campus community.\n\n"
            f"I'm currently concluding my degree in International Business at Dayananda Sagar University. Over the past year, I've had an incredible experience leading high-density operations for AERO INDIA 2025 at Yelahanka Air Force Station (100k+ footfall, 0 shrinkage) and corporate logistics for Tata Communications.\n\n"
            f"I'm actively exploring operations, business analysis, and program management opportunities across Bengaluru's leading firms. If you ever hear of relevant openings in your network or if I can ever help support any initiatives on your end, let's definitely catch up!\n\n"
            f"Wishing you the very best in your work, and let's stay in touch.\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    else:
        comp_display = company if company else "your organization"
        category = "Tier 4: Enterprise Network & Reconnect"
        job_info = f"Relationship Reconnect at {comp_display}"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you are having a great month! I'm reaching out to reconnect, strengthen our professional relationship, and share a quick update.\n\n"
            f"I'm currently finishing my final year in International Business at Dayananda Sagar University. Over the recent months, I've been focused on high-accountability execution—serving as Operations Lead at AERO INDIA 2025 (100,000+ attendees, zero security infractions, 0.0% shrinkage) and managing vendor SLA contracts for Tata Communications.\n\n"
            f"I'm currently exploring opportunities in operations, program management, and business analytics. If your team or network is ever looking for a disciplined, execution-oriented operator—or if there's ever any way I can assist you here in Bengaluru—I'd love to connect for a brief 5-minute chat.\n\n"
            f"Wishing you continued success in your journey!\n\n"
            f"Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    processed.append({
        'name': full_name,
        'first_name': first_name,
        'company': company or 'Independent / Not Disclosed',
        'position': position or 'Professional',
        'category': category,
        'job_info': job_info,
        'url': url,
        'email': email,
        'date': connected_on,
        'message': msg
    })

# Write to CSV
out_csv = r'e:\anti\linkedin_export\connection_personalized_messages.csv'
with open(out_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Full Name', 'First Name', 'Company', 'Position', 'Tier / Category', 'Job Info & ID', 'LinkedIn URL', 'Email Address', 'Connected Date', 'Personalized Relationship Message'])
    for p in processed:
        writer.writerow([
            p['name'], p['first_name'], p['company'], p['position'], p['category'],
            p['job_info'], p['url'], p['email'], p['date'], p['message']
        ])

print(f"Generated CSV with {len(processed)} records at {out_csv}")

# Write to JSON for frontend
out_json = r'e:\anti\linkedin_export\connection_outreach_data.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(processed, f, ensure_ascii=False)

print(f"Generated JSON with {len(processed)} records at {out_json}")
