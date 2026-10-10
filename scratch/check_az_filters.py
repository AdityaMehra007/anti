import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://careers.astrazeneca.com/search-jobs'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

# Check search filters section
filter_section = soup.find('section', id='search-filters') or soup.find(class_=re.compile(r'filter', re.I))
if filter_section:
    for cat in filter_section.find_all(['h3', 'h4', 'button']):
        print("Category:", cat.get_text(strip=True))
    for li in filter_section.find_all('li'):
        t = li.get_text(strip=True).encode('ascii', 'ignore').decode('ascii')
        if any(k in t.lower() for k in ['india', 'karnataka', 'bengaluru', 'bangalore', 'chennai']):
            print("  Facet match:", t)
else:
    print("No filter section found.")
