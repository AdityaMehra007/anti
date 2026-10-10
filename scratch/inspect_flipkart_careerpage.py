import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://flipkart.turbohire.co/careerpage/4d757ba0-3d57-448a-b82c-238ed87ac90f"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Career page HTML length: {len(html)}")
        
        # look for job data or JSON embedded in page
        jobs_json = re.findall(r'<script[^>]*>\s*window\.__INITIAL_STATE__\s*=\s*({.*?});\s*</script>', html, re.DOTALL)
        if jobs_json:
            print("Found INITIAL_STATE!")
        
        # check any JSON arrays
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
        for s in scripts:
            if "jobTitle" in s or "jobDescription" in s or "jobId" in s or "jobs" in s:
                print("Found relevant script!")
                print(s[:300])
                
        # search for job listings or title text
        titles = re.findall(r'"jobTitle"\s*:\s*"([^"]+)"', html)
        print("Job titles found:", len(titles))
        for t in titles[:10]:
            print(" ", t)
except Exception as e:
    print(f"Error: {e}")
