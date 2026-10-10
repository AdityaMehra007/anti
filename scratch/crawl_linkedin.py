import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import csv
import time
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Queries across technology, leadership, supply chain, luxury & data
SEARCH_SECTORS = [
    {"keyword": "Software Engineer", "tag": "Software Engineering"},
    {"keyword": "Director OR Vice President", "tag": "Executive Leadership"},
    {"keyword": "Supply Chain OR Logistics", "tag": "Supply Chain & Retail Operations"},
    {"keyword": "Data Scientist OR Machine Learning", "tag": "AI & Analytics"},
    {"keyword": "Product Manager", "tag": "Product & Growth"}
]

def crawl_linkedin_bengaluru():
    all_jobs = []
    seen_ids = set()
    
    for sector in SEARCH_SECTORS:
        kw = sector["keyword"]
        tag = sector["tag"]
        print(f"\n--- Scraping LinkedIn Bengaluru for: '{kw}' ({tag}) ---")
        
        # Paginate 0 to 50 (steps of 10 or 25)
        for start in [0, 10, 25, 50]:
            params = {
                'keywords': kw,
                'location': 'Bengaluru, Karnataka, India',
                'geoId': '105214831',
                'position': '1',
                'pageNum': '0',
                'start': str(start)
            }
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(url, headers=HEADERS)
            
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    html = resp.read().decode('utf-8')
            except Exception as e:
                print(f"Failed at start={start} for '{kw}': {e}")
                break
                
            soup = BeautifulSoup(html, 'html.parser')
            cards = soup.find_all('li')
            if not cards:
                print(f"No cards found at start={start}, stopping query.")
                break
                
            added = 0
            for card in cards:
                title_el = card.find('h3', class_='base-search-card__title')
                title = title_el.get_text(strip=True) if title_el else ""
                
                comp_el = card.find('h4', class_='base-search-card__subtitle')
                company = comp_el.get_text(strip=True) if comp_el else ""
                
                loc_el = card.find('span', class_='job-search-card__location')
                location = loc_el.get_text(strip=True) if loc_el else "Bengaluru, Karnataka, India"
                
                link_el = card.find('a', class_='base-card__full-link')
                raw_url = link_el['href'] if link_el and 'href' in link_el.attrs else ""
                clean_url = raw_url.split('?')[0] if raw_url else ""
                
                # Extract job ID from URL (e.g., -4369069660)
                m = re.search(r'-(\d+)$', clean_url)
                job_id = m.group(1) if m else clean_url
                
                time_el = card.find('time')
                posted_time = time_el.get_text(strip=True) if time_el else ""
                
                if job_id and job_id not in seen_ids and title:
                    seen_ids.add(job_id)
                    added += 1
                    all_jobs.append({
                        'Job Title': title,
                        'Company': company,
                        'Job ID': job_id,
                        'Vertical': tag,
                        'Posted': posted_time,
                        'Location': location,
                        'Apply URL': clean_url
                    })
                    
            print(f"start={start}: +{added} unique jobs (Cumulative: {len(all_jobs)})")
            time.sleep(1.5) # rate limit politeness
            
    print(f"\nScraping complete. Total unique LinkedIn Bengaluru requisitions: {len(all_jobs)}")
    
    with open('linkedin_bengaluru_jobs.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Job Title', 'Company', 'Job ID', 'Vertical', 'Posted', 'Location', 'Apply URL']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_jobs)
        
    print("Saved to linkedin_bengaluru_jobs.csv successfully.")

if __name__ == '__main__':
    crawl_linkedin_bengaluru()
