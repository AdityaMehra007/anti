import re
from bs4 import BeautifulSoup

with open('scratch/capgemini_page.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

for script in soup.find_all('script'):
    sid = script.get('id', '')
    content = script.string or ''
    if any(k in content.lower() for k in ['nonceendpoint', 'cgjobs', 'cg_jobs', 'jobs_data']):
        print('Matched script ID:', sid)
        print(content[:500])
        print('='*50)
