with open("scratch/diageo_page.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Look for <main> or content area
main = re.findall(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
if main:
    print("Found <main>, length:", len(main[0]))
    with open("scratch/diageo_main.html", "w", encoding="utf-8") as f:
        f.write(main[0])
    # check script or bundle tags inside main
    scripts_in_main = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', main[0])
    print("Scripts in main:", scripts_in_main)
else:
    print("No <main> found")

# Look for any bundle JS files loaded on the page
js_files = re.findall(r'src=["\'](/[^"\']+\.js[^"\']*)["\']', html)
print("JS files:", js_files)
for j in js_files:
    if "career" in j.lower() or "job" in j.lower() or "search" in j.lower() or "app" in j.lower():
        print("  Relevant JS:", j)
