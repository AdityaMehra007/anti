import csv, json

# Let's inspect the exact roles and details for the 11 target companies across all repository files:
# 1. BBA_IB_Bengaluru_61_Job_Pipeline.csv
# 2. 61_job_complete_referral_audit.csv
# 3. BANGALORE_500_STARTUPS_AND_MNCS_DIRECTORY.json
# 4. LIVE_ONLINE_SCRAPED_ROLES_2026.json
# 5. applications_generated/ manifests
# 6. BANGALORE_SCORED_JOBS_MASTER.json

target_companies = [
    'Accenture', 'Deloitte', 'Goldman Sachs', 'Amazon', 'IBM',
    'JPMorganChase', 'KPMG', 'PwC', 'Walmart Global Tech', 'Delhivery', 'PhonePe'
]

with open('data/BBA_IB_Bengaluru_61_Job_Pipeline.csv', mode='r', encoding='utf-8') as f:
    pipe_rows = list(csv.DictReader(f))

with open('data/61_job_complete_referral_audit.csv', mode='r', encoding='utf-8') as f:
    audit_rows = list(csv.DictReader(f))

with open('data/BANGALORE_500_STARTUPS_AND_MNCS_DIRECTORY.json', 'r', encoding='utf-8') as f:
    dir_rows = json.load(f)

with open('data/LIVE_ONLINE_SCRAPED_ROLES_2026.json', 'r', encoding='utf-8') as f:
    scraped_rows = json.load(f)

with open('data/BANGALORE_SCORED_JOBS_MASTER.json', 'r', encoding='utf-8') as f:
    master_scored = json.load(f)

print("All files loaded successfully.")
