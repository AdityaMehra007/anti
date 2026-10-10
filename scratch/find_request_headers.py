import re

with open('scratch/mercedes_nuxt.js', 'r', encoding='utf-8') as f:
    js = f.read()

# search for Py=
for m in re.finditer(r'Py\s*=\s*\{', js):
    start = max(0, m.start() - 50)
    end = min(len(js), m.end() + 500)
    print("--- Py snippet ---")
    print(js[start:end])

# search for headers or fetch/axios
for m in re.finditer(r'/gjb_search', js):
    start = max(0, m.start() - 500)
    end = min(len(js), m.end() + 500)
    print("--- gjb_search context ---")
    print(js[start:end])
