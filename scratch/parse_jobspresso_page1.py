import json
from bs4 import BeautifulSoup

with open('e:/anti/scratch/jobspresso_page1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

html = data.get('html', '')
soup = BeautifulSoup(html, 'html.parser')
jobs = soup.find_all('li')

print(f"Total list items parsed: {len(jobs)}")
for idx, job in enumerate(jobs[:10]):
    title_elem = job.find('h3', class_='job_listing-title') or job.find('div', class_='position')
    company_elem = job.find('div', class_='company') or job.find('strong')
    location_elem = job.find('div', class_='location')
    type_elem = job.find('li', class_='job-type') or job.find('div', class_='job-type')
    link_elem = job.find('a')
    
    title = title_elem.get_text(strip=True) if title_elem else 'N/A'
    company = company_elem.get_text(strip=True) if company_elem else 'N/A'
    location = location_elem.get_text(strip=True) if location_elem else 'N/A'
    jtype = type_elem.get_text(strip=True) if type_elem else 'N/A'
    link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else 'N/A'
    
    print(f"[{idx+1}] Title: {title} | Company: {company} | Loc: {location} | Type: {jtype} | URL: {link}")
