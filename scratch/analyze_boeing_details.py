import json
import re

with open('scratch/boeing_workday_india_details.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

with open('scratch/boeing_analysis_output.txt', 'w', encoding='utf-8') as out:
    for i, j in enumerate(jobs, 1):
        title = j['title']
        req = j['jobReqId']
        loc = j['location']
        desc = j['jobDescription']
        clean_desc = re.sub(r'<[^<]+?>', '\n', desc)
        lines = [l.strip() for l in clean_desc.splitlines() if l.strip()]
        
        out.write("="*75 + "\n")
        out.write(f"{i}. [{req}] {title}\n")
        out.write(f"   Location: {loc}\n")
        out.write(f"   Time Type: {j['timeType']} | Posted: {j['postedOn']}\n")
        out.write(f"   Workday URL: {j['workdayUrl']}\n")
        
        # Extract Key Sections
        out.write("   --- Description Snippets ---\n")
        for l in lines[:15]:
            out.write(f"     {l[:100]}\n")
            
        out.write("   --- Basic Qualifications & Requirements ---\n")
        capture = False
        count = 0
        for l in lines:
            if any(k in l.lower() for k in ['basic qualification', 'required qualification', 'typical education', 'skills & experience']):
                capture = True
            if capture:
                out.write(f"     * {l[:120]}\n")
                count += 1
                if count > 15 or any(k in l.lower() for k in ['preferred qualification', 'equal opportunity', 'relocation']):
                    capture = False
        out.write("\n")

print("Successfully written UTF-8 analysis to scratch/boeing_analysis_output.txt")
