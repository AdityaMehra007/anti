import urllib.request
import ssl
import json

ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

domain = "jobs.myntra.com"
url = f"https://io.spire2grow.com/ies/v1/p/workspaceId?domain={domain}"

print(f"Testing URL: {url}")
try:
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req, context=ctx)
    print("STATUS:", res.status)
    body = res.read().decode("utf-8")
    print("BODY:", body)
except Exception as e:
    print("ERROR:", e)
