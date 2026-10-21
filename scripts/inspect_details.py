import json

with open('security_reports/gitleaks_git_history.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total findings: {len(data)}")
for i, d in enumerate(data):
    rule = d.get('RuleID', 'unknown')
    file = d.get('File', 'unknown')
    line = d.get('StartLine', '?')
    commit = d.get('Commit', '')[:10]
    author = d.get('Author', '')
    date = d.get('Date', '')[:10]
    secret = d.get('Secret', '')
    masked_sec = secret[:4] + '...' + secret[-4:] if len(secret) > 8 else '***'
    match = d.get('Match', '').replace('\n', ' ')
    print(f"[{i+1:02d}] {rule:<18} | {file}:{line} ({commit}, {date}) | Match: {match[:70]} | Masked: {masked_sec}")
