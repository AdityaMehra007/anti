import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://job-boards.eu.greenhouse.io/groww"
headers = {'User-Agent': 'Mozilla/5.0'}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"HTML len: {len(html)}")
        
        # look for job links
        job_links = re.findall(r'href="([^"]*/jobs/[0-9]+)"', html)
        print("Job links found on EU board:", len(job_links))
        for l in job_links[:15]:
            print(" ", l)
            
        # check office filter names
        offices = re.findall(r'<option[^>]*value="([0-9]+)"[^>]*>(.*?)</option>', html)
        print("\nOffices in dropdown:")
        for oid, name in offices:
            print(f"  [{oid}] {name.strip()}")
except Exception as e:
    print(f"Error: {e}")
