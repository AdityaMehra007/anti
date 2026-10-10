import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://careers.astrazeneca.com/search-jobs/India/7684/2'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
print("Page Title:", soup.title.string if soup.title else '')

# Look for headings
for h in soup.find_all(re.compile(r'h[1-4]')):
    t = h.get_text(strip=True)
    if t:
        print("Heading:", t)

# Look for job links
job_links = soup.find_all('a', href=re.compile(r'/job/'))
print(f"Total job links: {len(job_links)}")
for a in job_links:
    clean_t = re.sub(r'[^\x00-\x7F]+', ' ', a.get_text(strip=True))
    parent = a.find_parent('li') or a.find_parent('div')
    loc = ''
    if parent:
        loc_el = parent.find(class_=re.compile(r'location', re.I))
        if loc_el:
            loc = loc_el.get_text(strip=True)
    print(f"  {clean_t} | {loc} -> {a.get('href')}")

# Look for facets
for f in soup.find_all(class_=re.compile(r'filter|facet', re.I)):
    for li in f.find_all('li')[:10]:
        print("  Facet:", li.get_text(strip=True))
