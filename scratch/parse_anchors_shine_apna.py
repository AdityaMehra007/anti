import urllib.request
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

# 1. Parse Shine jobs
try:
    html = urllib.request.urlopen(urllib.request.Request('https://www.shine.com/job-search/jobs-in-bangalore', headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    anchors = soup.find_all('a', href=re.compile(r'/jobs/|/job/'))
    print("Shine job anchors count:", len(anchors))
    for a in anchors[:5]:
        print("  - Shine link:", a.get_text(strip=True), "-->", a.get('href'))
except Exception as e:
    print("Shine anchor error:", e)

# 2. Parse Apna jobs
try:
    apna_url = 'https://apna.co/jobs?minExperience=0&search=true&session_id=search_1791591649376_j39x38h&raw_text_correction=true&text=Fresher+jobs&entity_id=40&entity_type=CustomSearch&location_id=0&location_identifier=651d46ff83cff884b7404dad&location_type=NBCluster&location_name=Bengaluru+Region'
    html = urllib.request.urlopen(urllib.request.Request(apna_url, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    apna_anchors = soup.find_all('a', href=re.compile(r'/job/|/jobs/'))
    print("Apna job anchors count:", len(apna_anchors))
    for a in apna_anchors[:5]:
        print("  - Apna link:", a.get_text(strip=True), "-->", a.get('href'))
except Exception as e:
    print("Apna anchor error:", e)
