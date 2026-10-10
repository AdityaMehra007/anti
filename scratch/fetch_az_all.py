import urllib.request
from bs4 import BeautifulSoup
import json
import re
import time

urls = [
    'https://careers.astrazeneca.com/location/bengaluru-jobs/7684/1269750-1267701-1277333/4',
    'https://careers.astrazeneca.com/location/bengaluru-jobs/7684/1269750-1267701-1277333/4/2'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

jobs_list = []
seen_hrefs = set()

for page_url in urls:
    req = urllib.request.Request(page_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a', href=re.compile(r'/job/')):
                href = a.get('href')
                raw_title = a.get_text(strip=True)
                if not raw_title or 'view role' in raw_title.lower() or href in seen_hrefs:
                    continue
                seen_hrefs.add(href)
                # Clean title (remove trailing location if concatenated)
                clean_title = re.sub(r'Bengaluru.*$', '', raw_title).strip()
                clean_title = re.sub(r'[^\x00-\x7F]+', ' ', clean_title).strip()
                
                full_url = f"https://careers.astrazeneca.com{href}"
                jobs_list.append({
                    'title': clean_title,
                    'url': full_url,
                    'path': href
                })
    except Exception as e:
        print(f"Error fetching {page_url}: {e}")

print(f"Extracted {len(jobs_list)} unique Bengaluru jobs. Now fetching descriptions...")

detailed_jobs = []
for j in jobs_list:
    u = j['url']
    print(f"Fetching: {j['title']}...")
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract description
            desc_el = soup.find('div', class_=re.compile(r'job-description|ats-description|desc', re.I)) or soup.find('section', class_=re.compile(r'job-details', re.I))
            desc_text = desc_el.get_text(separator='\n', strip=True) if desc_el else ''
            
            # Find apply link
            apply_url = ''
            for a in soup.find_all('a', href=True):
                h = a.get('href', '')
                if any(k in h.lower() for k in ['eightfold.ai', 'jobs.alexion.com', 'apply']):
                    apply_url = h
                    break
            
            # Extract GCL level
            gcl_match = re.search(r'GCL\s*[:\-–]?\s*([A-Za-z0-9]+)', desc_text, re.I)
            gcl = gcl_match.group(1).upper() if gcl_match else 'Unspecified'
            
            # Extract experience
            exp_matches = re.findall(r'(\d+[\s\-\–to]+\d*\s*(?:years?|yrs?)(?:\s*of\s*experience)?)', desc_text, re.I)
            
            j['gcl'] = gcl
            j['apply_url'] = apply_url
            j['experience'] = exp_matches[:3]
            j['description'] = desc_text
            detailed_jobs.append(j)
    except Exception as e:
        print(f"Error fetching {u}: {e}")
    time.sleep(0.3)

with open('scratch/az_detailed_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(detailed_jobs, f, indent=2, ensure_ascii=False)

print(f"Successfully saved {len(detailed_jobs)} detailed AstraZeneca jobs!")
