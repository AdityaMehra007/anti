import re
import json

with open('data/bangalorestartupmap_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s18 = scripts[18]

m = re.search(r'self\.__next_f\.push\(\[1,\s*\"(.*)\"\]\)\s*$', s18, re.DOTALL)
if not m:
    print("Match failed")
    exit(1)

raw_str = m.group(1)
# Unescape javascript string literal
# Notice that in Next.js push([1, "..."]), the string has \" and \\ and \n escaped
# A standard way to unescape is json.loads('"' + raw_str + '"')
try:
    unescaped = json.loads('"' + raw_str + '"')
except Exception as e:
    print("Standard json decode failed, fallback unescape:", e)
    # Manual unescape or strip
    unescaped = raw_str.encode('utf-8').decode('unicode_escape')

print("Unescaped string length:", len(unescaped))

# Now in unescaped string, let's find `"startups":[` and parse using JSONDecoder
idx = unescaped.find('"startups":[')
if idx != -1:
    decoder = json.JSONDecoder()
    startups_arr, end_idx = decoder.raw_decode(unescaped[idx + len('"startups":'):])
    print("Parsed startups array successfully!")
    print("Total startups count:", len(startups_arr))
    
    # Analyze sectors, stages, areas, and kinds
    kinds = set(s.get('kind', '') for s in startups_arr)
    sectors = set(s.get('sector', '') for s in startups_arr)
    stages = set(s.get('stage', '') for s in startups_arr)
    areas = set(s.get('area', '') for s in startups_arr)
    
    print("\nKinds:", kinds)
    print("\nSectors count:", len(sectors), list(sectors)[:10])
    print("\nStages count:", len(stages), stages)
    print("\nAreas count:", len(areas), list(areas)[:10])
    
    # Save startups to data/bangalorestartupmap_startups.json
    with open('data/bangalorestartupmap_startups.json', 'w', encoding='utf-8') as out:
        json.dump(startups_arr, out, indent=2, ensure_ascii=False)
    print("\nSaved to data/bangalorestartupmap_startups.json")

# Also look for featuredRoles, news, or VCs
for key in ['featuredRoles', 'news']:
    k_idx = unescaped.find(f'"{key}":[')
    if k_idx != -1:
        arr, _ = json.JSONDecoder().raw_decode(unescaped[k_idx + len(f'"{key}":'):])
        print(f"\nParsed {key} array successfully! Count: {len(arr)}")
        with open(f'data/bangalorestartupmap_{key}.json', 'w', encoding='utf-8') as out:
            json.dump(arr, out, indent=2, ensure_ascii=False)
        print(f"Saved to data/bangalorestartupmap_{key}.json")
