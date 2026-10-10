import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://flipkart.turbohire.co/dashboardv2?orgId=4d757ba0-3d57-448a-b82c-238ed87ac90f&type=0"
headers = {'User-Agent': 'Mozilla/5.0'}
with urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# print all script srcs
scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
for s in scripts:
    print(s)
