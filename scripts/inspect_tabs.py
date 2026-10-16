with open('ADITYA_APEX_CAREER_SUITE.html', encoding='utf-8') as f:
    text = f.read()

import re
tabs = re.findall(r'id=["\']tab-([^"\']+)["\']', text)
print("Found tab IDs:", tabs)

for t in tabs:
    pos = text.find(f'id="tab-{t}"')
    if pos != -1:
        print(f"tab-{t} snippet:", text[pos:pos+100])
