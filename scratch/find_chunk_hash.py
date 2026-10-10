import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.phonepe.com/webstatic/15170/webpack-runtime-5d6bb6e7e41dfe087db4.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

# look for component---src-pages-careers-job-openings
m = re.findall(r'component---src-pages-careers-job-openings[a-zA-Z0-9_-]*', js)
print("Matches in webpack runtime:", set(m))

# find chunk names or hashes
chunks = re.findall(r'\"([a-f0-9]{20})\"', js)
print("Hash samples:", chunks[:10])
