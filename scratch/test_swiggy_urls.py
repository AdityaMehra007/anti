import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://swiggy.darwinbox.in/ms/candidate/careers",
    "https://swiggy.darwinbox.in/jobs",
    "https://careers.swiggy.com",
    "https://careers.swiggy.in",
    "https://www.swiggy.com/careers"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"SUCCESS {u}: len {len(content)}")
            # check if jobs or title
            title_m = re.findall(r'<title>(.*?)</title>', content)
            print("  Title:", title_m)
    except Exception as e:
        print(f"Failed {u}: {e}")
