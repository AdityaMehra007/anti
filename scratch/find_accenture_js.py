import re
from bs4 import BeautifulSoup

with open('scratch/accenture_page.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
print('Total external scripts:', len(scripts))

for s in scripts:
    if any(k in s.lower() for k in ['job', 'career', 'search', 'radical']):
        print('Relevant script:', s)
