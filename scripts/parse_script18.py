import json
import re

with open('data/bangalorestartupmap_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s18 = scripts[18]

print('Script 18 snippet (first 1000 chars):')
print(s18[:1000])

print('\nScript 18 snippet (around phonepe or zerodha):')
idx = s18.lower().find('phonepe')
if idx != -1:
    print(s18[max(0, idx-200):idx+400])
