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

all_jobs = []

for page in range(1, 6):
    print(f"Fetching page {page}...")
    url = 'https://jobspresso.co/jm-ajax/get_listings/'
    data = urllib.parse.urlencode({
        'page': page,
        'per_page': 50,
        'orderby': 'featured',
        'order': 'DESC'
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8')
            j = json.loads(content)
            html = j.get('html', '')
            soup = BeautifulSoup(html, 'html.parser')
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
                loc = loc_elem.get_text(strip=True) if loc_elem else 'Anywhere / Remote'
                date = date_elem.get_text(strip=True) if date_elem else ''
                href = li.get('data-href', '')
                
                all_jobs.append({
                    'title': title,
                    'company': comp_name,
                    'tagline': tagline,
                    'location': loc,
                    'categories': ", ".join(types),
                    'date': date,
                    'url': href
                })
        time.sleep(1)
    except Exception as e:
        print(f"Error fetching page {page}: {e}")

print(f"Total jobs extracted: {len(all_jobs)}")
with open('e:/anti/scratch/jobspresso_all_extracted.json', 'w', encoding='utf-8') as out:
    json.dump(all_jobs, out, indent=2, ensure_ascii=False)
