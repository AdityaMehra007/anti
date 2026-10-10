import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://ibm.eightfold.ai/api/apply/v2/jobs?domain=ibm.com&location=Bengaluru%2C%20Karnataka%2C%20India&start=0&num=10"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.ibm.com/',
    'Origin': 'https://www.ibm.com'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(f"Total jobs: {res.get('total')}")
        for pos in res.get('positions', [])[:5]:
            print(f"[{pos.get('id')}] {pos.get('name')} | {pos.get('location')}")
except Exception as e:
    print(f"Eightfold API test failed: {e}")
