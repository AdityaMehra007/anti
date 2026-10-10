import urllib.request

url = "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/3334-09214f5396fa65c2.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    code = resp.read().decode('utf-8')

# Search for socket or wss or chat or converse
for term in ["wss://", "socket", "sse", "stream", "converse", "assistant", "graphql"]:
    pos = code.find(term)
    if pos != -1:
        print(f"Term '{term}' found at {pos}:")
        print(code[max(0, pos-100):min(len(code), pos+200)])
