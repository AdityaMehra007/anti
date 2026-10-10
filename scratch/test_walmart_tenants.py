import urllib.request
import json

tenants = [
    "https://walmart.wd1.myworkdayjobs.com/WalmartExternal",
    "https://walmart.wd1.myworkdayjobs.com/Walmart_External_Careers",
    "https://walmart.wd1.myworkdayjobs.com/walmartcareers",
    "https://walmart.wd1.myworkdayjobs.com/en-US/WalmartExternal",
    "https://walmart.wd5.myworkdayjobs.com/WalmartExternal"
]

for t in tenants:
    try:
        req = urllib.request.Request(t, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            print(f"Success for {t}: code {resp.status}, final URL: {resp.geturl()}")
    except Exception as e:
        print(f"Failed for {t}: {e}")
