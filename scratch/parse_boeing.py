import sys
from bs4 import BeautifulSoup
import re

with open('scratch/boeing_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print(f"Total HTML length: {len(html)}")

# Find all job links
job_links = soup.find_all('a', href=re.compile(r'/job/'))
seen = set()
jobs = []
for a in job_links:
    href = a.get('href', '')
    title = a.get_text(strip=True)
    if not title or href in seen:
        continue
    seen.add(href)
    parent = a.find_parent('li') or a.find_parent('div')
    loc = ''
    date = ''
    if parent:
        loc_el = parent.find(class_=re.compile(r'location', re.I))
        if loc_el:
            loc = loc_el.get_text(strip=True)
        date_el = parent.find(class_=re.compile(r'date', re.I))
        if date_el:
            date = date_el.get_text(strip=True)
    jobs.append({
        'title': title,
        'href': href,
        'loc': loc,
        'date': date
    })

print(f"Unique jobs extracted: {len(jobs)}")
with open('scratch/boeing_jobs_extracted.txt', 'w', encoding='utf-8') as out:
    for i, j in enumerate(jobs, 1):
        out.write(f"{i}. {j['title']}\n")
        out.write(f"   Location: {j['loc']}\n")
        out.write(f"   Date: {j['date']}\n")
        out.write(f"   URL: https://jobs.boeing.com{j['href']}\n\n")

print("Written to scratch/boeing_jobs_extracted.txt")
