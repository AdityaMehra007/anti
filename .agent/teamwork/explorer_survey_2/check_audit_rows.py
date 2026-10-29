import csv

with open('data/61_job_complete_referral_audit.csv', mode='r', encoding='utf-8') as f:
    audit_rows = list(csv.DictReader(f))

target_companies = [
    'accenture', 'deloitte', 'goldman', 'amazon', 'ibm',
    'jpmorgan', 'jp morgan', 'kpmg', 'pwc',
    'walmart', 'delhivery', 'phonepe'
]

print("=== 61_job_complete_referral_audit.csv FOR 11 TARGETS ===")
for r in audit_rows:
    comp = r['Target Company'].lower()
    for tc in target_companies:
        if tc in comp:
            print(f"[{r['Job ID']}] {r['Target Company']} | Role: {r['Job Role']}")
            print(f"   Matches: Total Emp: {r['Employee Match Count']}, Recruiters: {r['Recruiter Match Count']}, HM: {r['Hiring Manager Candidates Count']}, Confident: {r['High Confidence Contacts Count']}")
            print(f"   Top Contact: {r['Top Contact Name']} ({r['Top Contact LinkedIn URL']}) | Score: {r['Top Contact Opportunity Score']}")
            print(f"   Application Link: {r['Job Application Link']}")
            print(f"   Status: {r['Application Status']}")
            print()
            break
