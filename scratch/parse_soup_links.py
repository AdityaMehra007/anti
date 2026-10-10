import urllib.request
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

portals = [
    ('Instahyre', 'https://www.instahyre.com/jobs-in-bangalore/'),
    ('Cutshort', 'https://cutshort.io/jobs/startup-jobs-in-bangalore-bengaluru'),
    ('Hirist Product', 'https://www.hirist.tech/product-jobs?source=homepage'),
    ('Hirist Ecommerce', 'https://www.hirist.tech/ecommerce-jobs?source=catlist'),
    ('Hirist Fintech', 'https://www.hirist.tech/fintech-edtech-jobs?source=catlist')
]

for name, u in portals:
    try:
        html = urllib.request.urlopen(urllib.request.Request(u, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        job_links = [l for l in links if any(k in l for k in ['/job/', '/j/', '/jobs/', '/company/']) and l != u]
        print(f"=== {name} ===")
        print(f"Total links: {len(links)} | Job/Company links: {len(job_links)}")
        print("Sample links:", job_links[:5])
    except Exception as e:
        print(f"Error {name}:", e)
