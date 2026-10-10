import urllib.request
import ssl
import gzip
import io

url = "https://www.abcconsultants.in/executive-search/"
ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

req = urllib.request.Request(url, headers=headers)
try:
    res = urllib.request.urlopen(req, context=ctx)
    content = res.read()
    print("Content-Encoding:", res.headers.get("Content-Encoding"))
    
    # Try decompressing with gzip
    try:
        decompressed = gzip.decompress(content).decode("utf-8", errors="ignore")
        print("Successfully decompressed GZIP! Length:", len(decompressed))
    except Exception as e:
        decompressed = content.decode("utf-8", errors="ignore")
        print("Plain decode length:", len(decompressed))
        
    with open("scratch/abc_exec_search_decoded.html", "w", encoding="utf-8") as f:
        f.write(decompressed)
    print("Saved scratch/abc_exec_search_decoded.html")
    print(decompressed[:500])
except Exception as e:
    print("ERROR:", e)
