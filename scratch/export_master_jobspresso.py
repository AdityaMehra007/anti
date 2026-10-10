import json
import csv

with open('e:/anti/scratch/jobspresso_deduped_master.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

output_file = 'e:/anti/jobspresso_master_all_remote_jobs.csv'

fieldnames = [
    'Job Title',
    'Company',
    'Company Tagline',
    'Category / Track',
    'Location Requirement',
    'Date Posted',
    'Estimated Compensation Band',
    'Jobspresso URL'
]

records = []
for j in jobs:
    title = j.get('title', '').strip()
    comp = j.get('company', '').strip()
    if not comp:
        comp = 'Tech / Remote Employer'
    
    tagline = j.get('tagline', '').strip()
    cat = j.get('categories', '').strip() or 'General Remote'
    loc = j.get('location', '').strip() or 'Remote'
    date = j.get('date', '').strip()
    url = j.get('url', '').strip()
    
    # Seniority-based compensation benchmark
    tl = title.lower()
    if any(k in tl for k in ['director', 'head of', 'vp']):
        comp_est = "$150,000 - $240,000 USD (₹1.2Cr - ₹2.0Cr INR)"
    elif any(k in tl for k in ['staff', 'principal']):
        comp_est = "$140,000 - $210,000 USD (₹1.1Cr - ₹1.7Cr INR)"
    elif any(k in tl for k in ['senior', 'lead', 'manager', 'architect']):
        comp_est = "$90,000 - $165,000 USD (₹75L - ₹1.4Cr INR)"
    elif any(k in tl for k in ['intern', 'assistant', 'associate', 'coordinator', 'junior', 'specialist', 'support']):
        comp_est = "$45,000 - $85,000 USD (₹38L - ₹70L INR)"
    else:
        comp_est = "$70,000 - $120,000 USD (₹58L - ₹1.0Cr INR)"
        
    records.append({
        'Job Title': title,
        'Company': comp,
        'Company Tagline': tagline,
        'Category / Track': cat,
        'Location Requirement': loc,
        'Date Posted': date,
        'Estimated Compensation Band': comp_est,
        'Jobspresso URL': url
    })

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in records:
        writer.writerow(r)

print(f"Successfully exported {len(records)} records to {output_file}")
