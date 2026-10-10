import re

with open('scratch/mercedes_nuxt.js', 'r', encoding='utf-8') as f:
    js = f.read()

matches = [m.start() for m in re.finditer(r'gjb_search', js)]
print(f"Found {len(matches)} occurrences of gjb_search")

for idx in matches:
    start = max(0, idx - 200)
    end = min(len(js), idx + 400)
    print("--- SNIPPET ---")
    print(js[start:end])
