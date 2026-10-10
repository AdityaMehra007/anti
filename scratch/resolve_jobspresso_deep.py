import json
import urllib.request
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://jobspresso.co/remote-work/'
}

with open('e:/anti/scratch/jobspresso_targeted_harvest.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

# Select priority candidates:
# 1. Any job with location India, or company HackerRank
# 2. Worldwide / Anywhere / Various Countries / APAC
priority_jobs = []
for j in jobs:
    loc = j['location'].lower()
    comp = j['company'].lower()
    is_global_or_india = any(k in loc for k in ['india', 'worldwide', 'anywhere', 'various countries', 'apac', 'asia']) or comp in ['hackerrank', 'synthflow ai', 'deel', 'quora', 'mattermost', 'chainlink labs', 'leonardo.ai', 'girls who code', 'wikimedia foundation']
    if is_global_or_india:
        priority_jobs.append(j)

print(f"Selected {len(priority_jobs)} priority global/India jobs for deep resolution.")

resolved = []
for i, j in enumerate(priority_jobs[:35]):
    url = j['url']
    comp = j['company']
    title = j['title']
    print(f"[{i+1}/{min(35, len(priority_jobs))}] Resolving {comp} - {title}...")
    
    direct_apply = url
    snippet = ""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
            app_btn = soup.find('a', class_='application_button_link') or soup.find('input', class_='application_button') or soup.find('a', class_='job_application_email')
            if app_btn and 'href' in app_btn.attrs:
                direct_apply = app_btn['href']
            
            app_details = soup.find('div', class_='application_details')
            if app_details and app_details.find('a') and 'href' in app_details.find('a').attrs:
                direct_apply = app_details.find('a')['href']
            
            # Extract description snippet
            desc_div = soup.find('div', class_='job_description') or soup.find('div', class_='entry-content')
            if desc_div:
                p_text = desc_div.get_text(separator=' ', strip=True)
                snippet = p_text[:300]
        time.sleep(0.5)
    except Exception as e:
        print(f"  Failed: {e}")
    
    resolved.append({
        'title': title,
        'company': comp,
        'tagline': j.get('tagline', ''),
        'location': j.get('location', 'Remote'),
        'categories': j.get('categories', ''),
        'date': j.get('date', ''),
        'jobspresso_url': url,
        'direct_apply_url': direct_apply,
        'description_snippet': snippet
    })

print(f"\nSuccessfully resolved {len(resolved)} jobs with direct ATS links.")
with open('e:/anti/scratch/jobspresso_resolved_deep.json', 'w', encoding='utf-8') as out:
    json.dump(resolved, out, indent=2, ensure_ascii=False)
