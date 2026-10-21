import json
import os
import sys
from collections import Counter, defaultdict

def classify_severity(rule_id, description, secret, match):
    rule_lower = rule_id.lower()
    desc_lower = description.lower()
    
    # Critical / High: Live provider keys, private keys, cloud credentials
    critical_indicators = [
        'private-key', 'rsa', 'aws', 'github-pat', 'github-fine-grained',
        'slack-webhook', 'stripe', 'openai', 'gemini', 'anthropic',
        'azure', 'gcp', 'google-api', 'sendgrid', 'jwt', 'huggingface'
    ]
    if any(k in rule_lower for k in critical_indicators):
        # Check if it looks like an obvious placeholder or dummy
        secret_sample = secret.lower()
        if any(dummy in secret_sample for dummy in ['dummy', 'example', 'your_key', 'placeholder', 'xxxx', 'fake', 'test_key', 'mock']):
            return 'Low / Placeholder'
        return 'Critical / High'
    
    # Generic API Keys / Secrets / Tokens
    if 'generic' in rule_lower or 'token' in rule_lower or 'password' in desc_lower:
        secret_sample = secret.lower()
        if any(dummy in secret_sample for dummy in ['dummy', 'example', 'your_key', 'placeholder', 'xxxx', 'fake', 'test_key', 'mock', 'none', 'secret', 'changeme']):
            return 'Low / Placeholder'
        return 'Medium'
        
    return 'Low / Informational'

def analyze_report(report_path):
    if not os.path.exists(report_path):
        print(f"Error: {report_path} not found.")
        return None
    
    with open(report_path, 'r', encoding='utf-8') as f:
        try:
            findings = json.load(f)
        except Exception as e:
            print(f"Failed to load JSON: {e}")
            return None

    if not findings:
        print("No leaks detected! Repository is clean.")
        return {"total": 0, "findings": []}
    
    print(f"Total findings: {len(findings)}")
    
    rule_counts = Counter(item.get('RuleID', 'unknown') for item in findings)
    file_counts = Counter(item.get('File', 'unknown') for item in findings)
    
    by_severity = defaultdict(list)
    for item in findings:
        sev = classify_severity(
            item.get('RuleID', ''),
            item.get('Description', ''),
            item.get('Secret', ''),
            item.get('Match', '')
        )
        item['Severity'] = sev
        by_severity[sev].append(item)
        
    return {
        "total": len(findings),
        "rule_counts": dict(rule_counts.most_common()),
        "file_counts": dict(file_counts.most_common(20)),
        "by_severity": {k: len(v) for k, v in by_severity.items()},
        "findings": findings
    }

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "security_reports/gitleaks_git_history.json"
    res = analyze_report(path)
    if res and res["total"] > 0:
        print("\nSeverity Breakdown:")
        for sev, count in res["by_severity"].items():
            print(f"  {sev}: {count}")
        print("\nTop Rule IDs Triggered:")
        for rule, count in list(res["rule_counts"].items())[:10]:
            print(f"  {rule}: {count}")
        print("\nTop Affected Files:")
        for file, count in list(res["file_counts"].items())[:10]:
            print(f"  {file}: {count}")
