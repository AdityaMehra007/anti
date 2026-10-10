from bs4 import BeautifulSoup
import json

with open('scratch/wipro_page.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print('All scripts in Wipro page with src:')
for s in soup.find_all('script'):
    src = s.get('src', '')
    if src:
        print('  -', src)
