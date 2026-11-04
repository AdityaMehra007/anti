import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

with open('bengaluru_startup_intelligence_cockpit.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in cockpit: {len(lines)}")
# Find where tabs nav is
for i, line in enumerate(lines):
    if 'tabs-nav' in line:
        print(f"tabs-nav at line {i+1}")
    if 'tab-jobs' in line:
        print(f"tab-jobs at line {i+1}")
    if 'tab-startups500' in line:
        print(f"tab-startups500 at line {i+1}")
    if '<script>' in line:
        print(f"<script> at line {i+1}")
