import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.phonepe.com/careers/job-openings/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# look for script tag with component---src-pages-careers-job-openings-index-js
matches = re.findall(r'<script[^>]*src="([^"]*job-openings[^"]*)"', html)
print("Job openings scripts:", matches)

# look for any chunk urls in html
chunks = re.findall(r'https://www.phonepe.com/webstatic/[0-9]+/[^"]+\.js', html)
for c in chunks:
    print("Chunk:", c)
