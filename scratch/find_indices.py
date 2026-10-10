import re

with open('scratch/waas_resp.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Look for index names
for m in re.finditer(r'Job_[a-zA-Z0-9_]+', text):
    print('Found Job index:', m.group(0))

for m in re.finditer(r'Company_[a-zA-Z0-9_]+', text):
    print('Found Company index:', m.group(0))

# Search for any endpoint URL in JS
for m in re.finditer(r'https?://[a-zA-Z0-9_\-\.]*algolia[a-zA-Z0-9_\-\./]*', text):
    print('Found Algolia URL:', m.group(0))
