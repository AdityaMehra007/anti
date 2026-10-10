import re

with open('scratch/infosys_main.js', encoding='utf-8') as f:
    text = f.read()

# Search for unauthURL usage
endpoints = []
for m in re.finditer(r'unauthURL', text):
    start = max(0, m.start() - 50)
    end = min(len(text), m.end() + 200)
    snippet = text[start:end]
    if any(k in snippet for k in ['http', 'get', 'post', '+', '/']):
        endpoints.append(snippet)

print(f'Total unauthURL occurrences with network calls: {len(endpoints)}')
for idx, ep in enumerate(endpoints[:10]):
    print(f'Occurrence {idx+1}: {ep}')
    print('-'*50)
