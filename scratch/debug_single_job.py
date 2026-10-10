import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://jobs.boeing.com/job/bengaluru/experienced-mechanical-system-design-and-analysis-engineer/185/101118145392'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
print("Title:", soup.title.string if soup.title else '')

# Find all divs with class containing 'desc' or 'job'
for d in soup.find_all(['div', 'section'], class_=True):
    cl = ' '.join(d.get('class'))
    if any(k in cl.lower() for k in ['desc', 'detail', 'info', 'content']):
        print(f"Tag: {d.name}, class: {cl}, text len: {len(d.get_text())}")

# Check for workday direct apply link!
for a in soup.find_all('a', href=True):
    href = a.get('href')
    if 'workday' in href.lower() or 'apply' in href.lower():
        print(f"Apply link: {a.get_text(strip=True)} -> {href[:120]}")
