from bs4 import BeautifulSoup
import json

with open('e:/anti/scratch/jobspresso_page1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

soup = BeautifulSoup(data.get('html', ''), 'html.parser')
li = soup.find('li', class_='job_listing')

title = li.find('h3', class_='job_listing-title').get_text(strip=True) if li.find('h3', class_='job_listing-title') else ''
company = li.find('div', class_='job_listing-company').find('strong').get_text(strip=True) if li.find('div', class_='job_listing-company') else ''
tagline = li.find('span', class_='job_listing-company-tagline').get_text(strip=True) if li.find('span', class_='job_listing-company-tagline') else ''
location = li.find('div', class_='job_listing-location').get_text(strip=True) if li.find('div', class_='job_listing-location') else ''
job_types = [t.get_text(strip=True) for t in li.find_all('li', class_='job-type')]
date_elem = li.find('li', class_='job_listing-date') or li.find('span', class_='job_listing-date')
date = date_elem.get_text(strip=True) if date_elem else ''
url = li.get('data-href', '')

print(f"Title: {title}")
print(f"Company: {company}")
print(f"Location: {location}")
print(f"Job Types: {job_types}")
print(f"Date: {date}")
print(f"URL: {url}")
