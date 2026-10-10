import re

with open("scratch/walmart_page.html", "r", encoding="utf-8") as f:
    html = f.read()

inline = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
for idx, s in enumerate(inline):
    if "props" in s:
        print(f"Script {idx}: length {len(s)}")
        print(s[:500])
        with open("scratch/walmart_script_props.json", "w", encoding="utf-8") as out:
            out.write(s)
        break
