import urllib.request
import re
from bs4 import BeautifulSoup
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

# 1. Parse Hirist 0-1 Exp
try:
    url = 'https://www.hirist.tech/it-jobs-in-bangalore?minexp=0&maxexp=1'
    html = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    print("Hirist 0-1 Title:", soup.title.string if soup.title else "No Title")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if m:
        d = json.loads(m.group(1))
        initialState = d.get('props', {}).get('pageProps', {}).get('initialState', {})
        total = initialState.get('job', {}).get('totalJobs')
        print("Hirist totalJobs:", total)
except Exception as e:
    print("Hirist error:", e)

# 2. Parse Hasjob
try:
    url = 'https://hasjob.co/'
    html = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    print("Hasjob Title:", soup.title.string if soup.title else "No Title")
    posts = soup.find_all('a', class_=re.compile(r'stickie|post|job'))
    print("Hasjob posts count:", len(posts))
    for p in posts[:5]:
        print("  - Hasjob item:", p.get_text(strip=True)[:60], "-->", p.get('href'))
except Exception as e:
    print("Hasjob error:", e)
