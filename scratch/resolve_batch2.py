import json
import urllib.request
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://jobspresso.co/remote-work/'
}

with open('e:/anti/scratch/jobspresso_resolved_deep.json', 'r', encoding='utf-8') as f:
    existing = json.load(f)

existing_urls = {j['jobspresso_url'] for j in existing}

with open('e:/anti/scratch/jobspresso_targeted_harvest.json', 'r', encoding='utf-8') as f:
    all_jobs = json.load(f)

# Priority 2: Synthflow, Quora, Chainlink, Leonardo, Deel Support, Hinge Health, DuckDuckGo
priority_comps = ['synthflow ai', 'quora', 'chainlink labs', 'leonardo.ai', 'deel', 'hinge health', 'duckduckgo', 'binance', 'mozilla', 'invision']

batch2 = []
for j in all_jobs:
    url = j['url']
    if url in existing_urls:
        continue
    comp = j['company'].lower()
    loc = j['location'].lower()
    if any(c in comp for c in priority_comps) or 'worldwide' in loc or 'anywhere' in loc:
        batch2.append(j)

print(f"Resolving batch 2: {len(batch2[:25])} jobs...")

for i, j in enumerate(batch2[:25]):
    url = j['url']
    comp = j['company']
    title = j['title']
    print(f"[{i+1}/{min(25, len(batch2))}] Resolving {comp} - {title}...")
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
            
            desc_div = soup.find('div', class_='job_description') or soup.find('div', class_='entry-content')
            if desc_div:
                snippet = desc_div.get_text(separator=' ', strip=True)[:300]
        time.sleep(0.5)
    except Exception as e:
        print(f"  Failed: {e}")
    
    existing.append({
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

print(f"Total resolved deep jobs: {len(existing)}")
with open('e:/anti/scratch/jobspresso_resolved_deep.json', 'w', encoding='utf-8') as out:
    json.dump(existing, out, indent=2, ensure_ascii=False)
