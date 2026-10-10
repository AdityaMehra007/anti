import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://careers.astrazeneca.com/job/bengaluru/assistant-manager-procurement/43991/101305298352'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
print("Title:", soup.title.string if soup.title else '')

# find job description section
desc = soup.find('div', class_=re.compile(r'job-description|ats-description|desc', re.I)) or soup.find('section', class_=re.compile(r'job-details', re.I))
if desc:
    text = desc.get_text(separator='\n', strip=True)
    print("Desc length:", len(text))
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for l in lines[:25]:
        print("  ", l[:100])
    print("--- Requirements ---")
    for l in lines:
        if any(k in l.lower() for k in ['qualification', 'bachelor', 'degree', 'experience', 'procurement', 'bba', 'mba', 'skill']):
            print("   *", l[:120])
else:
    print("No desc element found directly. Checking all divs...")
    for d in soup.find_all('div', class_=True):
        if 'desc' in ' '.join(d.get('class')).lower():
            print("Class:", d.get('class'), "len:", len(d.get_text()))

# Find apply link
for a in soup.find_all('a', href=True):
    href = a.get('href', '')
    if any(k in href.lower() for k in ['workday', 'taleo', 'apply', 'myworkdayjobs', 'successfactors']):
        print("Apply link:", a.get_text(strip=True)[:30], "->", href)
