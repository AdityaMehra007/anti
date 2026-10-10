import re
from bs4 import BeautifulSoup

with open('scratch/accenture_page.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print('Title:', soup.title.string if soup.title else 'None')

# Check script tags for api endpoint
for script in soup.find_all('script'):
    src = script.get('src', '')
    content = script.string or ''
    if 'job' in src.lower() or 'search' in src.lower():
        print('Script src:', src)
    if 'api' in content.lower() or 'endpoint' in content.lower() or 'search' in content.lower():
        matches = [l.strip() for l in content.split('\n') if any(k in l.lower() for k in ['api', 'endpoint', 'jobsearch', 'services'])]
        if matches:
            print('Script match snippet:', matches[:5])

# Find links or data attributes
endpoints = re.findall(r'https?://[^\s\"\'\<\>]+(?:job|search|career)[^\s\"\'\<\>]*', html)
print('Endpoints found:', set(endpoints[:10]))
