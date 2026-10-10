import urllib.request
import json

url = "https://careers.walmart.com/api/ai/search-ai/api/v1/combined/hybrid-search?page=0&size=20&locale=en-US"
payload = {
    "query": "India",
    "basicSearch": False,
    "filter": "",
    "locale": "en-US"
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("Success! Response keys:", res.keys())
        with open("scratch/walmart_search_res.json", "w", encoding="utf-8") as out:
            json.dump(res, out, indent=2)
except Exception as e:
    print("Error calling hybrid-search:", e)
