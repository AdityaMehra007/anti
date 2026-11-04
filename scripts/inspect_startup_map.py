import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request('https://www.bangalorestartupmap.com/', headers=headers)
with urllib.request.urlopen(req, timeout=20) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

print('HTML length:', len(html))

# Look for next_f scripts
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print('Total scripts:', len(scripts))

for i, s in enumerate(scripts):
    if '__NEXT_DATA__' in s:
        print(f'Script {i} has __NEXT_DATA__')
    if 'self.__next_f' in s:
        print(f'Script {i} has self.__next_f, len: {len(s)}')
        # check if it contains startup data
        if 'phonepe' in s.lower() or 'zerodha' in s.lower() or 'swiggy' in s.lower() or 'hsr' in s.lower():
            print(f'Script {i} contains startup keywords!')

# Save raw html for analysis
with open('data/bangalorestartupmap_raw.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Saved data/bangalorestartupmap_raw.html')
