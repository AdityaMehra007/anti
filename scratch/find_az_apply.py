import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://careers.astrazeneca.com/job/chennai/director-ets-global-software-asset-management/7684/101741126400'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
for a in soup.find_all('a', href=True):
    href = a.get('href', '')
    text = a.get_text(strip=True).encode('ascii', 'ignore').decode('ascii')
    if any(k in href.lower() for k in ['apply', 'job-search', 'workday', 'taleo', 'successfactors', 'icims']):
        print(f"Match: {text} -> {href}")

# Also check for forms or button actions
for btn in soup.find_all(['button', 'input']):
    print("Element:", btn.name, btn.get('class'), btn.get('id'), btn.get('value'))
