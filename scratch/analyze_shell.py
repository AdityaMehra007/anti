import json
import re

with open('scratch/shell_jobs_detailed.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

targets = ['R205864', 'R205282', 'R211581', 'R208550', 'R210810', 'R211067', 'R200923']
for j in jobs:
    if j['req'] in targets:
        print('='*70)
        print(f"{j['req']}: {j['title']} | {j['location']}")
        print(f"URL: {j['url']}")
        desc = re.sub(r'<[^<]+?>', '\n', j['desc'])
        lines = [line.strip() for line in desc.splitlines() if line.strip()]
        for l in lines[:20]:
            print('  ', l)
        print('  --- [Requirements / Skills] ---')
        for l in lines:
            if any(k in l.lower() for k in ['qualification', 'requirement', 'degree', 'experience', 'bachelor', 'graduate', 'skill']):
                print('   *', l)
        print()
