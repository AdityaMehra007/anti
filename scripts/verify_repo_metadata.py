import subprocess
import json

res = subprocess.run(['gh', 'repo', 'list', 'AdityaMehra007', '--limit', '50', '--json', 'name,description,repositoryTopics,isFork,visibility'], capture_output=True, text=True, encoding='utf-8')
data = json.loads(res.stdout)
for r in data:
    if not r['isFork']:
        topics = [t['name'] for t in (r.get('repositoryTopics') or [])]
        print(f"[{r['name']}] ({r['visibility']})")
        print(f"  Description: {r['description']}")
        print(f"  Topics: {topics}\n")
