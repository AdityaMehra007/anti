import re
import json

with open("scratch/diageo_page.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML Length:", len(html))

# Look for workday, brassring, avature, oracle, greenhouse, lever, api, search endpoints
ats_keywords = ["workday", "brassring", "avature", "oraclecloud", "successfactors", "phenom", "eightfold", "smartrecruiters", "greenhouse", "lever", "myworkdayjobs"]
for kw in ats_keywords:
    matches = set(re.findall(rf'https?://[^\s"\'<>]*{kw}[^\s"\'<>]*', html, re.IGNORECASE))
    if matches:
        print(f"[{kw}] matches:", matches)

# Check for JSON objects or job data embedded in script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"Total script tags: {len(scripts)}")
for i, s in enumerate(scripts):
    if any(k in s.lower() for k in ["job", "requisition", "api", "workday", "bangalore", "bengaluru", "india"]):
        print(f"Script {i} contains keywords, len={len(s)}")
        # Check if contains urls or json
        urls = set(re.findall(r'https?://[^\s"\'<>]+', s))
        for u in urls:
            if "diageo" in u or "api" in u or "workday" in u:
                print("   Found URL:", u)
        if "var " in s or "window." in s or "{" in s:
            # show snippet
            lines = [l.strip() for l in s.split("\n") if any(k in l.lower() for k in ["api", "job", "endpoint", "url", "workday"])]
            for l in lines[:10]:
                print("   Line:", l[:120])
