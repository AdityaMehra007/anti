import re
import csv
import time
import urllib.request
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def crawl_randstad_pages(max_pages=8):
    all_jobs = []
    seen = set()
    pattern = re.compile(r'/jobs/([a-zA-Z0-9\-]+)_bangalore_([a-f0-9\-]+)/')
    
    for page in range(1, max_pages + 1):
        if page == 1:
            url = "https://www.randstad.in/jobs/re-karnataka/ci-bangalore/"
        else:
            url = f"https://www.randstad.in/jobs/re-karnataka/ci-bangalore/page-{page}/"
            
        print(f"Fetching page {page}: {url}")
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8')
        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
            break
            
        soup = BeautifulSoup(html, 'html.parser')
        page_jobs_count = 0
        
        for a in soup.find_all('a', href=True):
            m = pattern.search(a['href'])
            if m:
                slug = m.group(1)
                job_id = m.group(2)
                full_url = f"https://www.randstad.in{a['href']}"
                if job_id not in seen:
                    seen.add(job_id)
                    page_jobs_count += 1
                    
                    card = a.find_parent('li') or a.find_parent('article') or a.find_parent('div', class_=re.compile(r'card|search-result', re.I))
                    title = ""
                    snippet = ""
                    job_type = "Permanent / Contract"
                    
                    if card:
                        h3 = card.find('h3') or card.find('h2')
                        title = h3.get_text(strip=True) if h3 else slug.replace('-', ' ').title()
                        
                        card_text = card.get_text(separator=' | ', strip=True)
                        if 'permanent' in card_text.lower():
                            job_type = 'Permanent'
                        elif 'contract' in card_text.lower():
                            job_type = 'Contract'
                            
                        # Extract salary or skills snippet
                        snippet = card_text.replace('\n', ' ')[:250]
                    else:
                        title = slug.replace('-', ' ').title()
                        
                    all_jobs.append({
                        'Job Title': title.title(),
                        'Job ID': job_id,
                        'Contract Type': job_type,
                        'Details': snippet,
                        'Location': 'Bengaluru, Karnataka',
                        'Apply URL': full_url
                    })
                    
        print(f"Page {page} done: +{page_jobs_count} jobs (Cumulative: {len(all_jobs)})")
        time.sleep(1) # respectful rate limit
        
    print(f"\nCrawling complete. Total unique Bengaluru jobs: {len(all_jobs)}")
    
    with open('randstad_bengaluru_jobs.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Job Title', 'Job ID', 'Contract Type', 'Details', 'Location', 'Apply URL'])
        writer.writeheader()
        writer.writerows(all_jobs)
        
    print("Saved to randstad_bengaluru_jobs.csv successfully.")

if __name__ == '__main__':
    crawl_randstad_pages(8)
