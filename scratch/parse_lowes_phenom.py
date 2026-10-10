import re
import json

with open("scratch/lowes_page.html", "r", encoding="utf-8") as f:
    html = f.read()

# Look for phApp
m = re.search(r'phApp\s*=\s*({.*?});\s*phApp', html, re.S)
if not m:
    m = re.search(r'window\.phApp\s*=\s*({.*?});', html, re.S)
if not m:
    m = re.search(r'phApp\.pageData\s*=\s*({.*?});', html, re.S)
if m:
    print("Found phApp regex match! Length:", len(m.group(1)))
    try:
        data = json.loads(m.group(1))
        print("Keys:", list(data.keys()))
        with open("scratch/lowes_phapp.json", "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
    except Exception as e:
        print("JSON parse error:", e)
        with open("scratch/lowes_raw_phapp.txt", "w", encoding="utf-8") as out:
            out.write(m.group(1))
else:
    print("No phApp regex match. Searching for widgets or refineSearch...")
    matches = re.findall(r'https?://[^\s"\'<>]+/widgets[^\s"\'<>]*', html)
    print("Widget URLs:", matches)
    
    # search for eVar or job info
    jobs_json = re.findall(r'(\{\"jobId\"[^\}]+\})', html)
    print("jobId JSONs found:", len(jobs_json))
