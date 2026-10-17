import re
import os
import sys

site_dir = r"E:\Temp\amehr\adityamehra007_site"
pages = [
    "index.html",
    "vendor_sla_dashboard.html",
    "interview_simulator.html",
    "Aditya_Mehra_Resume_Printable.html"
]

all_clean = True

for page in pages:
    page_path = os.path.join(site_dir, page)
    if not os.path.exists(page_path):
        print(f"[FAIL] Missing page: {page}")
        all_clean = False
        continue

    with open(page_path, "r", encoding="utf-8") as f:
        content = f.read()

    links = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', content)
    broken = []
    for item in links:
        if item.startswith("#") or item.startswith("mailto:") or item.startswith("tel:") or item.startswith("javascript:"):
            continue
        if item.startswith("http://") or item.startswith("https://"):
            continue
        clean_item = item.split("#")[0].split("?")[0]
        if not clean_item:
            continue
        target = os.path.normpath(os.path.join(site_dir, clean_item))
        if not os.path.exists(target):
            broken.append((item, target))

    if broken:
        print(f"[FAIL] {page}: {len(broken)} broken local references:")
        for b in broken:
            print(f"       - {b[0]} -> {b[1]}")
        all_clean = False
    else:
        print(f"[PASS] {page}: All {len(links)} references valid.")

if all_clean:
    print("\nALL PAGES VERIFIED: Zero broken local links or missing assets across entire site!")
else:
    sys.exit(1)
