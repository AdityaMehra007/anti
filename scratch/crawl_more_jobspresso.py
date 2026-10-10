import urllib.request
import urllib.parse
import json
import time
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://jobspresso.co/remote-work/'
}

url = 'https://jobspresso.co/jm-ajax/get_listings/'

# Fetch pages 6 through 15 (500 additional listings)
more_jobs = []

for page in range(6, 16):
    print(f"Crawling page {page}...")
    data = urllib.parse.urlencode({
        'page': page,
        'per_page': 50,
        'orderby': 'featured',
        'order': 'DESC'
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            j = json.loads(resp.read().decode('utf-8'))
            soup = BeautifulSoup(j.get('html', ''), 'html.parser')
            listings = soup.find_all('li', class_='job_listing')
            print(f"Page {page}: found {len(listings)} listings")
            for li in listings:
                t_elem = li.find('h3', class_='job_listing-title')
                c_elem = li.find('div', class_='job_listing-company')
                comp_name = c_elem.find('strong').get_text(strip=True) if c_elem and c_elem.find('strong') else ''
                tagline = c_elem.find('span', class_='job_listing-company-tagline').get_text(strip=True) if c_elem and c_elem.find('span', class_='job_listing-company-tagline') else ''
                loc_elem = li.find('div', class_='job_listing-location')
                types = [t.get_text(strip=True) for t in li.find_all('li', class_='job-type')]
                date_elem = li.find('li', class_='job_listing-date') or li.find('span', class_='job_listing-date')
                
                title = t_elem.get_text(strip=True) if t_elem else li.get('data-title', '')
                loc = loc_elem.get_text(strip=True) if loc_elem else 'Remote'
                date = date_elem.get_text(strip=True) if date_elem else ''
                href = li.get('data-href', '')
                
                more_jobs.append({
                    'title': title,
                    'company': comp_name,
                    'tagline': tagline,
                    'location': loc,
                    'categories': ", ".join(types),
                    'date': date,
                    'url': href
                })
        time.sleep(0.5)
    except Exception as e:
        print(f"Error on page {page}: {e}")

print(f"Collected {len(more_jobs)} additional listings.")
with open('e:/anti/scratch/jobspresso_pages_6_to_15.json', 'w', encoding='utf-8') as out:
    json.dump(more_jobs, out, indent=2, ensure_ascii=False)
