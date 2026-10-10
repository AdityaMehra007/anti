import re

with open('scratch/mercedes_nuxt.js', 'r', encoding='utf-8') as f:
    js = f.read()

for m in re.finditer(r'([a-zA-Z0-9_\$]+)\s*:\s*[\"\'\`]https?://[^\"\'\`]+', js):
    print(m.group(0))

for m in re.finditer(r'([a-zA-Z0-9_\$]+)\s*=\s*[\"\'\`]https?://[^\"\'\`]+', js):
    print(m.group(0))
