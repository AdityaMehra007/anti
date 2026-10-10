import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://careers.astrazeneca.com/location/bengaluru-jobs/7684/1269750-1267701-1277333/4'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
print("Page Title:", soup.title.string if soup.title else '')

job_links = soup.find_all('a', href=re.compile(r'/job/'))
print(f"Total job links found: {len(job_links)}")

seen = set()
with open('scratch/az_bengaluru_jobs.txt', 'w', encoding='utf-8') as out:
    for a in job_links:
        t = re.sub(r'[^\x00-\x7F]+', ' ', a.get_text(strip=True))
        href = a.get('href')
        if t and 'view role' not in t.lower() and href not in seen:
            seen.add(href)
            parent = a.find_parent('li') or a.find_parent('div')
            loc = ''
            if parent:
                loc_el = parent.find(class_=re.compile(r'location', re.I))
                if loc_el:
                    loc = loc_el.get_text(strip=True)
            out.write(f"Title: {t}\n")
            out.write(f"  Location: {loc}\n")
            out.write(f"  URL: https://careers.astrazeneca.com{href}\n\n")

print(f"Unique jobs written: {len(seen)} to scratch/az_bengaluru_jobs.txt")
