import json
from bs4 import BeautifulSoup

with open('e:/anti/scratch/jobspresso_page1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

soup = BeautifulSoup(data.get('html', ''), 'html.parser')
listings = soup.find_all('li', class_='job_listing')
print(f"Found {len(listings)} listings with class 'job_listing'")

for i, li in enumerate(listings[:10]):
    data_title = li.get('data-title', '')
    data_href = li.get('data-href', '')
    title_elem = li.find('h3', class_='job_listing-title')
    company_elem = li.find('strong', class_='job_listing-company')
    location_elem = li.find('div', class_='job_listing-location') or li.find('span', class_='location')
    category_elem = li.find('li', class_='job-type') or li.find('span', class_='job-type')
    date_elem = li.find('date') or li.find('time')
    
    print(f"\n--- Job {i+1} ---")
    print(f"Title: {title_elem.get_text(strip=True) if title_elem else data_title}")
    print(f"Company: {company_elem.get_text(strip=True) if company_elem else 'N/A'}")
    print(f"Location: {location_elem.get_text(strip=True) if location_elem else 'N/A'}")
    print(f"Category/Type: {category_elem.get_text(strip=True) if category_elem else 'N/A'}")
    print(f"Date: {date_elem.get_text(strip=True) if date_elem else 'N/A'}")
    print(f"URL: {data_href or (li.find('a')['href'] if li.find('a') else 'N/A')}")
