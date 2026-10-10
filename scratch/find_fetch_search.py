import urllib.request
import re

url = "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/3334-09214f5396fa65c2.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    code = resp.read().decode('utf-8')

# Search for onFetchSearchResults
pos = code.find("onFetchSearchResults")
while pos != -1:
    print("--- onFetchSearchResults match ---")
    print(code[max(0, pos-200):min(len(code), pos+400)])
    pos = code.find("onFetchSearchResults", pos+1)
