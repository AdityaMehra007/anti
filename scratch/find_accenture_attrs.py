import re
from bs4 import BeautifulSoup

with open('scratch/accenture_page.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

jobsearch_div = soup.find(class_=re.compile(r'jobsearch|careers-search|radical', re.I))
if jobsearch_div:
    print('Found container tag:', jobsearch_div.name, jobsearch_div.get('class'))
    for k, v in jobsearch_div.attrs.items():
        if k.startswith('data-'):
            print(f'  {k} = {v}')

# Find any element with data-job-country or similar
for el in soup.find_all(attrs=True):
    for a in el.attrs:
        if any(term in a.lower() for term in ['country', 'sort', 'findjobs', 'elastic']):
            print(f'Element {el.name} [{a}] = {el[a]}')
