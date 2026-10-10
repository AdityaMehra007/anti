from bs4 import BeautifulSoup
import re
import csv

def build_enriched_dice():
    with open('scratch/dice_resp.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    seen = set()
    jobs = []
    
    # Check all job links
    for a in soup.find_all('a', href=re.compile(r'/job-detail/([a-f0-9\-]+)')):
        m = re.search(r'/job-detail/([a-f0-9\-]+)', a['href'])
        if not m:
            continue
        job_id = m.group(1)
        if job_id in seen:
            continue
            
        title = a.get_text(strip=True)
        if not title:
            continue
            
        seen.add(job_id)
        
        # Categorize by tech specialization
        t_lower = title.lower()
        if 'salesforce' in t_lower or 'mulesoft' in t_lower:
            category = 'Salesforce & Enterprise CRM'
        elif 'java' in t_lower or 'python' in t_lower or 'developer' in t_lower:
            category = 'Core Software & Backend Engineering'
        elif 'cloud' in t_lower or 'azure' in t_lower or 'aws' in t_lower or 'devops' in t_lower:
            category = 'Cloud Architecture & DevOps'
        elif 'data' in t_lower or 'ai' in t_lower or 'llm' in t_lower:
            category = 'AI, LLMs & Data Engineering'
        elif 'cisco' in t_lower or 'network' in t_lower or 'security' in t_lower:
            category = 'Cybersecurity & Infrastructure'
        elif 'manager' in t_lower or 'lead' in t_lower or 'director' in t_lower:
            category = 'Tech Leadership & Program Management'
        else:
            category = 'Specialized Technology Consulting'
            
        jobs.append({
            'Job Title': title,
            'Specialization': category,
            'Job ID': job_id,
            'Location': 'Bengaluru, Karnataka, India',
            'Sourcing Portal': 'Dice.com',
            'Direct Apply URL': f"https://www.dice.com/job-detail/{job_id}"
        })
        
    print(f"Total enriched Dice Bengaluru postings: {len(jobs)}")
    with open('dice_bengaluru_jobs.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Job Title', 'Specialization', 'Job ID', 'Location', 'Sourcing Portal', 'Direct Apply URL']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)
    print("Updated dice_bengaluru_jobs.csv successfully.")

if __name__ == '__main__':
    build_enriched_dice()
