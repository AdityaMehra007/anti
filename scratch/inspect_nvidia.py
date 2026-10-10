import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://jobs.nvidia.com/careers?start=0&pid=893398076243&sort_by=timestamp"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"HTML Length: {len(html)}")
        
        # Look for platform cues (eightfold, workday, etc.)
        if "eightfold" in html.lower():
            print("Eightfold detected!")
        if "workday" in html.lower():
            print("Workday detected!")
            
        # check for scripts or JSON data
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
        for s in scripts:
            if "job" in s.lower() and ("bengaluru" in s.lower() or "bangalore" in s.lower() or "positions" in s.lower()):
                print("Found relevant script block, len:", len(s))
                print(s[:300])
                
        # check for job links
        job_links = re.findall(r'href="([^"]*/careers/job/[^"]*|[^"]*position[^"]*)"', html)
        print("Job links found:", len(job_links))
        for l in job_links[:5]:
            print(" ", l)
except Exception as e:
    print(f"Error: {e}")
