import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://jobs.smartrecruiters.com/PHONEPELIMITED/1000000000003165-business-operations-analyst-payments-business"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

idx = html.find("Job Description")
if idx != -1:
    text = re.sub(r'<[^>]+>', '\n', html[idx:idx+2500])
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for l in lines[:40]:
        print(l.encode('ascii', 'ignore').decode('ascii'))
