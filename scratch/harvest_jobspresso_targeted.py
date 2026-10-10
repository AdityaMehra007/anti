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

collected = {}

def harvest(keywords=None, max_pages=2):
    for p in range(1, max_pages + 1):
        params = {
            'page': p,
            'per_page': 50,
            'orderby': 'featured',
            'order': 'DESC'
        }
        if keywords:
            params['search_keywords'] = keywords
        
        data = urllib.parse.urlencode(params).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                j = json.loads(resp.read().decode('utf-8'))
                soup = BeautifulSoup(j.get('html', ''), 'html.parser')
                listings = soup.find_all('li', class_='job_listing')
                print(f"Harvest [{keywords or 'ALL'}] Page {p}: {len(listings)} items")
                for li in listings:
                    href = li.get('data-href', '')
                    if not href or href in collected:
                        continue
                    
                    t_elem = li.find('h3', class_='job_listing-title')
                    c_elem = li.find('div', class_='job_listing-company')
                    comp_name = c_elem.find('strong').get_text(strip=True) if c_elem and c_elem.find('strong') else ''
                    tagline = c_elem.find('span', class_='job_listing-company-tagline').get_text(strip=True) if c_elem and c_elem.find('span', class_='job_listing-company-tagline') else ''
                    loc_elem = li.find('div', class_='job_listing-location')
                    types = [t.get_text(strip=True) for t in li.find_all('li', class_='job-type')]
                    date_elem = li.find('li', class_='job_listing-date') or li.find('span', class_='job_listing-date')
                    
                    title = t_elem.get_text(strip=True) if t_elem else li.get('data-title', '')
                    loc = loc_elem.get_text(strip=True) if loc_elem else 'Worldwide / Remote'
                    date = date_elem.get_text(strip=True) if date_elem else ''
                    
                    collected[href] = {
                        'title': title,
                        'company': comp_name,
                        'tagline': tagline,
                        'location': loc,
                        'categories': ", ".join(types),
                        'date': date,
                        'url': href,
                        'query_source': keywords or 'browse'
                    }
            time.sleep(1)
        except Exception as e:
            print(f"Error harvesting {keywords} page {p}: {e}")

# Harvest targeted segments
harvest('India', max_pages=2)
harvest('Worldwide', max_pages=2)
harvest('Operations', max_pages=2)
harvest('Support', max_pages=2)

print(f"\nTotal unique listings collected: {len(collected)}")

with open('e:/anti/scratch/jobspresso_targeted_harvest.json', 'w', encoding='utf-8') as out:
    json.dump(list(collected.values()), out, indent=2, ensure_ascii=False)
