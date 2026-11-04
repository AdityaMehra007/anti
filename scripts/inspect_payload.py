import json
import re

with open('data/bangalorestartupmap_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s18 = scripts[18]

# Extract the payload pushed into self.__next_f
# It is self.__next_f.push([1,"..."])
m = re.search(r'self\.__next_f\.push\(\[1,\s*\"(.*?)\"\]\)\s*$', s18, re.DOTALL)
if m:
    raw_str = m.group(1)
    print("Found payload string, length:", len(raw_str))
    
    # Next.js escape unescape
    unescaped = raw_str.encode('utf-8').decode('unicode_escape')
    print("Unescaped length:", len(unescaped))
    
    # Find startups list
    startup_match = re.search(r'\"startups\":\s*(\[\{.*?\}\])(?=,\"[a-zA-Z0-9_]+\":|\}\])', unescaped, re.DOTALL)
    if startup_match:
        print("Found startups array substring length:", len(startup_match.group(1)))
        try:
            startups = json.loads(startup_match.group(1))
            print("Successfully parsed startups! Total count:", len(startups))
            print("Sample startup:", json.dumps(startups[0], indent=2))
        except Exception as e:
            print("Direct JSON loads error on startups:", e)
            # Try to see where it breaks or use regex/json decoder
    
    # Check for other keys
    keys = re.findall(r'\"([a-zA-Z0-9_]+)\":\s*\[', unescaped)
    print("List keys found in unescaped:", set(keys))
else:
    print("Could not match next_f payload with simple regex")
