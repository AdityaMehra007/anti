import urllib.request
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

urls = [
    ('Hirist Product', 'https://www.hirist.tech/product-jobs?source=homepage'),
    ('Hirist Ecommerce', 'https://www.hirist.tech/ecommerce-jobs?source=catlist'),
    ('Hirist Fintech', 'https://www.hirist.tech/fintech-edtech-jobs?source=catlist')
]

for name, u in urls:
    try:
        html = urllib.request.urlopen(urllib.request.Request(u, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        print(f"=== {name} ===")
        print("Page title:", soup.title.string if soup.title else 'No Title')
        print("Text snippet:", text[:300])
        # Find all divs or elements with class containing 'job'
        job_cards = soup.find_all(lambda tag: tag.has_attr('class') and any('job' in c.lower() for c in tag['class']))
        print("Job-classed elements count:", len(job_cards))
        # Look for script tags with API endpoints
        api_matches = re.findall(r'https?://[^\s"\']+/api/[^\s"\']+', html)
        print("API endpoints mentioned in HTML:", set(api_matches))
    except Exception as e:
        print(f"Error {name}:", e)
