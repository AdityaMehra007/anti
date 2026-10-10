import re

with open('scratch/mercedes_nuxt.js', 'r', encoding='utf-8') as f:
    js = f.read()

# search for gjb_search calls
for m in re.finditer(r'endpoint:\s*[\"\'\`/]gjb_search[\"\'\`]', js):
    start = max(0, m.start() - 300)
    end = min(len(js), m.end() + 300)
    print("--- ENDPOINT MATCH ---")
    print(js[start:end])

# search for fetch or axios with endpoint
for m in re.finditer(r'\$fetch|axios|ky\.|http', js):
    snippet = js[m.start():m.start()+80]
    if any(k in snippet.lower() for k in ['gjb', 'header', 'auth', 'token', 'key']):
        print("Fetch snippet:", snippet)
