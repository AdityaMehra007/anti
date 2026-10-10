import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

chunks = [
    "https://flipkart.turbohire.co/18.dbc8e48216e40dca22f4.chunk.js",
    "https://flipkart.turbohire.co/30.83fbae2815ce51b795d9.chunk.js",
    "https://flipkart.turbohire.co/runtime-main.7abc5f79532e9fe369e5.js"
]

for c in chunks:
    try:
        req = urllib.request.Request(c, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            m = re.findall(r'.{0,40}isMatched.{0,40}', content, re.IGNORECASE)
            if m:
                print(f"Found in {c}:")
                for item in m[:3]:
                    print("  ", item.strip())
    except Exception as e:
        print(f"Error {c}: {e}")
