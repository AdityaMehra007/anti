import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.phonepe.com/webstatic/15170/webpack-runtime-5d6bb6e7e41dfe087db4.js"
with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

# Search for 4339 in the chunk URL resolver
idx = js.find("4339:")
print("Matches for 4339:")
while idx != -1:
    print(js[idx-10:idx+60])
    idx = js.find("4339:", idx+1)
