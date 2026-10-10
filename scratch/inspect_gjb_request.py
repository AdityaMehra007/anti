import re

with open('scratch/mercedes_nuxt.js', 'r', encoding='utf-8') as f:
    js = f.read()

# find definition of Py or hydrateRequest
matches = re.findall(r'hydrateRequest:[a-zA-Z0-9_\$]+', js)
print("hydrateRequest matches:", matches)

# look for gjb_search request method (GET or POST)
for m in re.finditer(r'endpoint:"/gjb_search"', js):
    start = max(0, m.start() - 300)
    end = min(len(js), m.end() + 300)
    print("--- CONTEXT ---")
    print(js[start:end])
