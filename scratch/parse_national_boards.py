import urllib.request
import re
import json
import ssl
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

# 1. Inspect Shine
try:
    html = urllib.request.urlopen(urllib.request.Request('https://www.shine.com/job-search/jobs-in-bangalore', headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    print("Shine Title:", soup.title.string if soup.title else "No Title")
    # look for NEXT_DATA or script data
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    print("Shine NEXT_DATA present:", bool(m))
    if m:
        d = json.loads(m.group(1))
        print("Shine NEXT_DATA keys:", list(d.keys()))
        props = d.get('props', {}).get('pageProps', {})
        print("Shine pageProps keys:", list(props.keys()))
        job_data = props.get('jobData', {}) or props.get('data', {}) or props.get('jobs', [])
        print("Shine job_data type / keys:", type(job_data), list(job_data.keys()) if isinstance(job_data, dict) else len(job_data))
except Exception as e:
    print("Shine Error:", e)

# 2. Inspect Apna
try:
    apna_url = 'https://apna.co/jobs?minExperience=0&search=true&session_id=search_1791591649376_j39x38h&raw_text_correction=true&text=Fresher+jobs&entity_id=40&entity_type=CustomSearch&location_id=0&location_identifier=651d46ff83cff884b7404dad&location_type=NBCluster&location_name=Bengaluru+Region'
    html = urllib.request.urlopen(urllib.request.Request(apna_url, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    print("Apna Title:", soup.title.string if soup.title else "No Title")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    print("Apna NEXT_DATA present:", bool(m))
    if m:
        d = json.loads(m.group(1))
        props = d.get('props', {}).get('pageProps', {})
        print("Apna pageProps keys:", list(props.keys()))
except Exception as e:
    print("Apna Error:", e)

# 3. Inspect TimesJobs with relaxed SSL
try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request('https://www.timesjobs.com/job-search?txtLocation=Bangalore', headers=headers)
    html = urllib.request.urlopen(req, context=ctx, timeout=10).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    print("TimesJobs Title:", soup.title.string if soup.title else "No Title")
    job_cards = soup.find_all('li', class_=lambda c: c and 'clearfix' in c and 'job-bx' in c)
    print("TimesJobs job-bx count:", len(job_cards))
except Exception as e:
    print("TimesJobs Error:", e)
