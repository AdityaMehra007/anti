import urllib.request, re

req = urllib.request.Request('https://www.meesho.io/contact', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("Contact page length:", len(html))
        # Look for address or bangalore
        addresses = re.findall(r'[^<>]+(?:Bangalore|Bengaluru|560\d{3})[^<>]+', html, re.I)
        print("Address matches:", addresses[:5])
except Exception as e:
    print("Error:", e)
