import urllib.request
import json

paths = [
    '/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1',
    '/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1',
    '/job/Bengaluru/Sales-Operations-New-Associate_AIOC-S01669615-1',
    '/job/Bengaluru/Trust---Safety-New-Associate_AIOC-S01668350-1',
    '/job/Bengaluru/Regulatory-Compliance-New-Associate_AIOC-S01667647-1',
    '/job/Bengaluru/HR-Service-Delivery-New-Associate_AIOC-S01663367-1'
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
            job_info = data.get('jobPostingInfo', {})
            print("==================================================")
            print("TITLE:", job_info.get('title'))
            print("REQ ID:", job_info.get('jobReqId'))
            print("POSTED:", job_info.get('postedOn'))
            print("LOCATION:", job_info.get('location'))
            # Print first 500 chars of job description
            desc = job_info.get('jobDescription', '')
            # Clean html tags simply
            import re
            clean_desc = re.sub('<[^<]+?>', ' ', desc)
            clean_desc = ' '.join(clean_desc.split())
            print("SNIPPET:", clean_desc[:300])
    except Exception as e:
        print(f"Error for {p}: {e}")
