import re
from bs4 import BeautifulSoup
import json

with open('scratch/capgemini_page.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Check for job search form or data attributes
elements = soup.find_all(attrs={"data-api-endpoint": True})
for el in elements:
    print('data-api-endpoint:', el['data-api-endpoint'])

# Check for any script containing search or jobs
for script in soup.find_all('script'):
    src = script.get('src', '')
    content = script.string or ''
    if 'job' in src.lower() or 'career' in src.lower():
        print('Script src:', src)
    if 'job_search' in content.lower() or 'jobsearch' in content.lower() or 'endpoint' in content.lower():
        lines = [line.strip() for line in content.split('\n') if 'endpoint' in line.lower() or 'api' in line.lower() or 'search' in line.lower()]
        print('Script content match:', lines[:10])

# Look for jobs listed in the HTML directly
job_cards = soup.find_all(class_=re.compile(r'job|card|listing|career', re.I))
print('Potential job elements:', len(job_cards))
for c in job_cards[:5]:
    print('Card classes:', c.get('class'))
