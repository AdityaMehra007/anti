import re

with open('scratch/infosys_main.js', encoding='utf-8') as f:
    text = f.read()

# Search for HttpClient post/get calls with companyhiringtype
matches = re.findall(r'[a-zA-Z0-9_\.]+\.(?:get|post)\([^\)]*companyhiringtype[^\)]*\)', text)
print('HTTP calls with companyhiringtype:', len(matches))
for m in matches[:5]:
    print('Match:', m)

# Search for exact string companyhiringtype
idx = text.find('companyhiringtype')
while idx != -1:
    print('Context of companyhiringtype:')
    print(text[max(0, idx-150):min(len(text), idx+250)])
    print('='*50)
    idx = text.find('companyhiringtype', idx+1)
    if idx > 0 and len(matches) > 3:
        break
