import json
import re

with open('scratch/az_detailed_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

with open('scratch/az_summary.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total jobs loaded: {len(jobs)}\n\n")

    for i, j in enumerate(jobs, 1):
        title = j['title']
        gcl = j.get('gcl', 'N/A')
        url = j['url']
        apply = j.get('apply_url', '')
        exp = j.get('experience', [])
        desc = j.get('description', '')
        
        # check qualifications / degree mentioned
        degrees = re.findall(r'(?:Bachelor|Master|BBA|B\.Com|BCom|MBA|Degree|graduate|B\.E|BTech)[^,.;\n]{0,50}', desc, re.IGNORECASE)
        clean_degrees = list(set([d.strip() for d in degrees[:3]]))
        
        out.write(f"{i}. {title}\n")
        out.write(f"   GCL Level: {gcl} | Exp: {exp[:2]}\n")
        out.write(f"   Degree: {clean_degrees}\n")
        out.write(f"   TalentBrew URL: {url}\n")
        out.write(f"   Eightfold Apply URL: {apply}\n\n")

print("Saved to scratch/az_summary.txt")
