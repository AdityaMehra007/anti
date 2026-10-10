import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 1. Instahyre
try:
    html = urllib.request.urlopen(urllib.request.Request('https://www.instahyre.com/jobs-in-bangalore/', headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    titles = re.findall(r'<title>([^<]+)</title>', html)
    print('Instahyre Title:', titles)
    job_matches = re.findall(r'href="(/job-[^"]+)"', html)
    print('Instahyre Job Links:', len(job_matches), job_matches[:5])
    # check script tags
    scripts = re.findall(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    print('Instahyre NEXT_DATA:', len(scripts))
except Exception as e:
    print('Instahyre Error:', e)

# 2. Cutshort
try:
    html = urllib.request.urlopen(urllib.request.Request('https://cutshort.io/jobs/startup-jobs-in-bangalore-bengaluru', headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    titles = re.findall(r'<title>([^<]+)</title>', html)
    print('Cutshort Title:', titles)
    scripts = re.findall(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    print('Cutshort NEXT_DATA:', len(scripts))
    if scripts:
        data = json.loads(scripts[0])
        print('Cutshort NEXT_DATA keys:', list(data.keys()))
        props = data.get('props', {}).get('pageProps', {})
        print('Cutshort pageProps keys:', list(props.keys()))
except Exception as e:
    print('Cutshort Error:', e)

# 3. Hirist
try:
    html = urllib.request.urlopen(urllib.request.Request('https://www.hirist.tech/product-jobs?source=homepage', headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    titles = re.findall(r'<title>([^<]+)</title>', html)
    print('Hirist Title:', titles)
    scripts = re.findall(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    print('Hirist NEXT_DATA:', len(scripts))
    if scripts:
        data = json.loads(scripts[0])
        props = data.get('props', {}).get('pageProps', {})
        print('Hirist pageProps keys:', list(props.keys()))
except Exception as e:
    print('Hirist Error:', e)
