import urllib.request
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

url = 'https://hasjob.co/'
html = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

items = soup.find_all('li')
print("Total <li> in Hasjob:", len(items))
for it in items:
    text = it.get_text(separator=' ', strip=True)
    if 'Bengaluru' in text or 'Bangalore' in text or 'Remote' in text:
        a = it.find('a')
        link = a.get('href') if a else 'No link'
        print("MATCH:", text[:120], "-->", link)
