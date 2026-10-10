import urllib.request, re

req = urllib.request.Request('https://www.meesho.com/legal/privacy', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'[^<>]+(?:560\d{3}|Fashnear|Helios|Outer Ring Road)[^<>]+', html, re.I)
        print("Matches from privacy policy:", set([m.strip() for m in matches[:5]]))
except Exception as e:
    print("Error:", e)
