import urllib.request
import json
import re

paths = [
    '/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1',
    '/job/Bengaluru/Procure-to-Pay-Operations-Associate_AIOC-S01670867-1',
    '/job/Bengaluru/HR-Service-Delivery-Associate_AIOC-S01670860-1',
    '/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1',
    '/job/Bengaluru/Customer-Contact-Comms-Associate-Messaging_AIOC-S01665940-1'
]

base = 'https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json'
}

for p in paths:
    url = base + p
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            info = data.get('jobPostingInfo', {})
            title = info.get('title')
            req_id = info.get('jobReqId')
            posted = info.get('postedOn')
            desc = info.get('jobDescription', '')
            clean = re.sub('<[^<]+?>', ' ', desc)
            clean = ' '.join(clean.split())
            
            # Extract qualifications and experience
            exp_match = re.search(r'Years of Experience:\s*([^A-Z]+)', clean)
            qual_match = re.search(r'Qualifications:\s*([^A-Z]+)', clean)
            skill_match = re.search(r'Skill required:\s*([^D]+)Designation:', clean)
            
            print("==================================================")
            print("TITLE:", title)
            print("REQ ID:", req_id)
            print("POSTED:", posted)
            print("EXPERIENCE:", exp_match.group(1).strip() if exp_match else "N/A")
            print("QUALIFICATION:", qual_match.group(1).strip() if qual_match else "N/A")
            print("SKILL:", skill_match.group(1).strip() if skill_match else "N/A")
            print("SNIPPET:", clean[:250])
    except Exception as e:
        print(f"Error for {p}: {e}")
