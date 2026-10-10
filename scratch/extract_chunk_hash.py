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

# Gatsby chunk mapping is like: {"component---src-pages-careers-job-openings-index-js":"<hash>"}
m = re.findall(r'["\']component---src-pages-careers-job-openings-index-js["\']\s*:\s*["\']([a-f0-9]+)["\']', js)
print("Mapping found:", m)
if not m:
    # check nearby characters
    idx = js.find("component---src-pages-careers-job-openings-index-js")
    if idx != -1:
        print("Context around match:")
        print(js[idx-50:idx+150])
