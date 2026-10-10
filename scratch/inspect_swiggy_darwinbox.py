import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://swiggy.darwinbox.in/ms/candidate/careers"
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=ctx) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print(f"Content len: {len(content)}")
        print("Content:", content[:500])
except Exception as e:
    print(f"Error: {e}")
