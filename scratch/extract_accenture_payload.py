import re

with open('scratch/accenture_rad.js', encoding='utf-8') as f:
    text = f.read()

idx = text.find('/api/accenture/elastic/findjobs')
snippet = text[idx-1200:idx]
print('Snippet before findjobs:')
print(snippet)
