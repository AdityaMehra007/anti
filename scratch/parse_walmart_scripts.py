import re

with open("scratch/walmart_page.html", "r", encoding="utf-8") as f:
    html = f.read()

print("Searching scripts in walmart_page.html:")
scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
for s in scripts:
    print("Script:", s)

# Look for inline scripts containing endpoints
inline = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
print(f"Total inline scripts: {len(inline)}")
for idx, s in enumerate(inline):
    if any(k in s for k in ["api", "search", "results", "endpoint", "workday", "job", "india"]):
        print(f"\n--- Script {idx} match ---")
        lines = [l.strip() for l in s.split("\n") if any(k in l.lower() for k in ["api", "endpoint", "url", "search", "india"])]
        for l in lines[:10]:
            print("  ", l[:120])
