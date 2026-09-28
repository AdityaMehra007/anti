import os
import re
import json
import csv
from urllib.parse import urlparse

def infer_tags(title, desc, category):
    text = f"{title} {desc} {category}".lower()
    tags = set()
    
    tag_keywords = {
        'AI/ML': ['ai ', 'ai/', 'machine learning', 'data science', 'llm', 'deep learning', 'dataaxy', 'moaijobs', 'aidevboard'],
        'Web3/Crypto': ['crypto', 'web3', 'blockchain', 'bitcoin', 'tokenjobs', 'solana', 'ethereum'],
        'DevOps/Cloud': ['devops', 'sre', 'cloud', 'platform engineering', 'kubernetes', 'infrastructure'],
        'Python': ['python', 'pyjobs', 'django'],
        'Frontend': ['frontend', 'front-end', 'vue', 'react', 'javascript', 'typescript', 'dribbble'],
        'Backend': ['backend', 'back-end', 'golang', 'ruby', 'clojure', 'java', 'c#', '.net', 'laravel'],
        'Design/UI/UX': ['design', 'ui/ux', 'dribbble', 'creative', 'art'],
        '4-Day Week': ['4 day', '4-day', 'four day'],
        'LATAM': ['latam', 'chile', 'spanish', 'portuguese', 'latin america'],
        'Europe': ['europe', 'german', 'poland', 'denmark', 'swiss', 'nordic', 'uk', 'spain'],
        'Canada': ['canada', 'canadian'],
        'Security': ['security', 'cyber', 'cyberjobhunt'],
        'Async/Remote-First': ['async', 'remote-first', 'distributed', 'remote dna', '100% remote', 'anywhere']
    }
    
    for tag, kws in tag_keywords.items():
        if any(kw in text for kw in kws):
            tags.add(tag)
            
    if not tags:
        tags.add('General Tech')
        
    return sorted(list(tags))

def parse_awesome_remote(raw_path):
    with open(raw_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    sections = {}
    current_section = None
    current_sub_section = None

    link_re = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for line in lines:
        line_str = line.strip()
        if line_str.startswith('## '):
            current_section = line_str[3:].strip()
            current_sub_section = None
            if current_section not in sections:
                sections[current_section] = []
            continue
        elif line_str.startswith('#### '):
            current_sub_section = line_str[5:].strip()
            continue
        elif line_str.startswith('### '):
            current_sub_section = line_str[4:].strip()
            continue

        if not current_section:
            continue
        if current_section in ['Languages', 'Table of Contents', 'License']:
            continue

        if line_str.startswith(('1.', '-', '*')) or re.match(r'^\d+\.', line_str):
            item_text = re.sub(r'^\d+\.\s*', '', line_str)
            item_text = re.sub(r'^[-*]\s*', '', item_text).strip()
            if not item_text:
                continue

            matches = list(link_re.finditer(item_text))
            if matches:
                first_match = matches[0]
                title = first_match.group(1).strip()
                url = first_match.group(2).strip()
                
                desc = item_text[first_match.end():].strip()
                desc = re.sub(r'^[\s\-—:–]+', '', desc).strip()
                
                extra_links = []
                careers_url = ""
                for m in matches[1:]:
                    ext_title = m.group(1).strip()
                    ext_url = m.group(2).strip()
                    extra_links.append({'title': ext_title, 'url': ext_url})
                    if any(c in ext_title.lower() for c in ['career', 'job', 'work with us', 'join us', 'hiring']):
                        careers_url = ext_url

                category = current_section
                if current_sub_section:
                    category = f"{current_section} - {current_sub_section}"

                tags = infer_tags(title, desc, category)

                sections[current_section].append({
                    'title': title,
                    'url': url,
                    'careers_url': careers_url,
                    'description': desc,
                    'extra_links': extra_links,
                    'section': current_section,
                    'sub_section': current_sub_section or '',
                    'category': category,
                    'tags': tags,
                    'raw': item_text
                })
            else:
                if sections.get(current_section) and not line_str.startswith(('1.', '-', '*')):
                    sections[current_section][-1]['description'] += " " + line_str

    return sections

def main():
    target_dir = os.path.join(os.path.dirname(__file__), 'remote-resources')
    os.makedirs(target_dir, exist_ok=True)
    raw_file = os.path.join(os.path.dirname(__file__), 'remote_awesome_raw.md')

    sections_data = parse_awesome_remote(raw_file)

    total_items = sum(len(v) for v in sections_data.values())
    print(f"Total extracted items: {total_items}")

    # Build Master JSON
    master_db = {
        "metadata": {
            "source": "https://github.com/lukasz-madon/awesome-remote-job",
            "extracted_at": "2026-09-28T16:15:00Z",
            "total_items": total_items,
            "section_counts": {k: len(v) for k, v in sections_data.items()}
        },
        "ecosystem": sections_data
    }

    json_path = os.path.join(target_dir, 'remote_ecosystem_master.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)
    print(f"Saved Master JSON to: {json_path}")

    # CSV 1: Companies with Remote DNA
    companies = sections_data.get('Companies with "remote DNA"', [])
    companies_csv_path = os.path.join(target_dir, 'remote_companies.csv')
    with open(companies_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Company Name', 'Website URL', 'Careers URL', 'Tags', 'Description', 'Extra Links'])
        for c in companies:
            extra_links_str = "; ".join([f"{el['title']}: {el['url']}" for el in c['extra_links']])
            writer.writerow([
                c['title'],
                c['url'],
                c['careers_url'],
                ", ".join(c['tags']),
                c['description'],
                extra_links_str
            ])
    print(f"Saved {len(companies)} companies to: {companies_csv_path}")

    # CSV 2: Job Boards & Aggregators
    job_boards = sections_data.get('Job boards', []) + sections_data.get('Job boards aggregators', [])
    boards_csv_path = os.path.join(target_dir, 'remote_job_boards.csv')
    with open(boards_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Board Name', 'URL', 'Type', 'Tags', 'Description'])
        for b in job_boards:
            writer.writerow([
                b['title'],
                b['url'],
                b['section'],
                ", ".join(b['tags']),
                b['description']
            ])
    print(f"Saved {len(job_boards)} job boards to: {boards_csv_path}")

    # CSV 3: Tools & Infrastructure
    tools = sections_data.get('Tools', [])
    tools_csv_path = os.path.join(target_dir, 'remote_tools.csv')
    with open(tools_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Tool Name', 'URL', 'Sub-Category', 'Tags', 'Description'])
        for t in tools:
            writer.writerow([
                t['title'],
                t['url'],
                t['sub_section'] or 'General',
                ", ".join(t['tags']),
                t['description']
            ])
    print(f"Saved {len(tools)} tools to: {tools_csv_path}")

    # CSV 4: Relocation Grants & Incentives
    incentives = sections_data.get('Relocation Incentives', [])
    incentives_csv_path = os.path.join(target_dir, 'relocation_incentives.csv')
    with open(incentives_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Program Name', 'URL', 'Description'])
        for inc in incentives:
            writer.writerow([inc['title'], inc['url'], inc['description']])
    print(f"Saved {len(incentives)} relocation incentives to: {incentives_csv_path}")

if __name__ == '__main__':
    main()
