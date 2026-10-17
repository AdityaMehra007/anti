import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('e:/anti/detailed_bengaluru_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

for j in jobs:
    desc = j.get('jobDescription', '')
    skill = re.search(r'Skill required:</b>\s*(.*?)(?:<br|<b>|$)', desc)
    desig = re.search(r'Designation:</b>\s*(.*?)(?:<br|<b>|$)', desc)
    qual = re.search(r'Qualifications:</b>\s*(.*?)(?:<br|<b>|$)', desc)
    exp = re.search(r'Years of Experience:</b>\s*(.*?)(?:<br|<b>|$)', desc)
    what = re.search(r'What would you do\?</b>\s*(.*?)(?:<b>|$)', desc, re.DOTALL)
    
    print('JOB ID:', j.get('jobReqId'))
    print('TITLE:', j.get('title'))
    print('POSTED:', j.get('postedOn'))
    print('LOCATION:', j.get('location'))
    print('SKILL:', skill.group(1).strip() if skill else 'N/A')
    print('DESIGNATION:', desig.group(1).strip() if desig else j.get('title'))
    print('QUALIFICATIONS:', qual.group(1).strip() if qual else 'Any Graduation / BBA')
    print('EXPERIENCE:', exp.group(1).strip() if exp else '0 to 1 years')
    clean_what = re.sub(r'<[^>]+>', ' ', what.group(1)) if what else ''
    print('WHAT WOULD YOU DO:', ' '.join(clean_what.split()[:40]))
    print('URL:', f"https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers{j.get('externalPath')}")
    print('-'*60)
