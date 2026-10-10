import urllib.request
import json
import re
from bs4 import BeautifulSoup
import time

with open('scratch/boeing_jobs_extracted.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

jobs = []
current_job = {}
for line in lines:
    line = line.strip()
    if re.match(r'^\d+\.', line):
        if current_job and 'url' in current_job:
            jobs.append(current_job)
        current_job = {'title': re.sub(r'^\d+\.\s*', '', line)}
    elif line.startswith('Location:'):
        current_job['loc'] = line.replace('Location:', '').strip()
    elif line.startswith('Date:'):
        current_job['date'] = line.replace('Date:', '').strip()
    elif line.startswith('URL:'):
        current_job['url'] = line.replace('URL:', '').strip()

if current_job and 'url' in current_job:
    jobs.append(current_job)

print(f"Total jobs to fetch details for: {len(jobs)}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

detailed_jobs = []
for j in jobs:
    url = j['url']
    safe_title = j['title'].encode('ascii', 'ignore').decode('ascii')
    print(f"Fetching: {safe_title} from {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            
            # find job description section
            desc_el = soup.find('div', class_=re.compile(r'job-description|ats-description|desc', re.I)) or soup.find('section', class_=re.compile(r'job-details', re.I))
            desc_text = desc_el.get_text(separator='\n', strip=True) if desc_el else ''
            
            # extract requisition ID / Job ID
            req_id_match = re.search(r'JR\d{10}', html)
            req_id = req_id_match.group(0) if req_id_match else ''
            
            j['req_id'] = req_id
            j['description'] = desc_text
            detailed_jobs.append(j)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    time.sleep(0.3)

with open('scratch/boeing_detailed_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(detailed_jobs, f, indent=2, ensure_ascii=False)

print(f"Successfully saved {len(detailed_jobs)} detailed Boeing jobs!")
