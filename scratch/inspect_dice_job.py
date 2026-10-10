import urllib.request
import json
import re

url = 'https://www.dice.com/job-detail/109d63c2-18fb-4362-9463-0d2c446d4b58'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        m_title = re.search(r'<title>(.*?)</title>', html)
        print('Job Page Title:', m_title.group(1) if m_title else 'N/A')
        m_jsonld = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        if m_jsonld:
            data = json.loads(m_jsonld.group(1))
            print('JSON-LD Title:', data.get('title'))
            print('JSON-LD Org:', data.get('hiringOrganization', {}).get('name'))
            print('JSON-LD Location:', data.get('jobLocation'))
            print('JSON-LD Date:', data.get('datePosted'))
except Exception as e:
    print('Error:', e)
