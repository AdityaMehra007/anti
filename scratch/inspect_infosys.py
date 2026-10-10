import re
from bs4 import BeautifulSoup

with open('scratch/infosys_page.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print('Title:', soup.title.string if soup.title else 'No Title')

# Look for API endpoints in scripts
scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
print('External scripts count:', len(scripts))
for s in scripts:
    if any(k in s.lower() for k in ['job', 'career', 'search', 'api', 'app', 'main', 'bundle']):
        print('Relevant script:', s)

# Look for inline scripts containing api calls or job endpoints
inline_scripts = [s.string for s in soup.find_all('script') if s.string]
print('Inline scripts count:', len(inline_scripts))
for idx, s in enumerate(inline_scripts):
    if any(k in s.lower() for k in ['api', 'endpoint', 'companyhiringtype', 'countrycode', 'jobs']):
        matches = [line.strip() for line in s.splitlines() if any(k in line.lower() for k in ['api', 'endpoint', 'fetch', 'url', 'http'])]
        if matches:
            print(f'Inline script {idx} matches:')
            for m in matches[:5]:
                print('   ', m[:120])
