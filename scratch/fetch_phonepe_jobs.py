import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.phonepe.com/apollo/job-postings/latest.json"
headers = {'User-Agent': 'Mozilla/5.0'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as resp:
    data = json.loads(resp.read().decode('utf-8'))

print("Data type:", type(data))
if isinstance(data, dict):
    print("Keys:", list(data.keys()))
    for k, v in data.items():
        print(f"Key '{k}': type={type(v)}")
        if isinstance(v, list):
            print(f"  Length: {len(v)}")
            if v:
                print("  Sample item keys:", list(v[0].keys()) if isinstance(v[0], dict) else v[0])
elif isinstance(data, list):
    print("List length:", len(data))
    if data:
        print("First item:", data[0])
