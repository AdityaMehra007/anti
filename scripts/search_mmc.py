import os
import re

matches = []
exclude_dirs = {'.git', 'node_modules', '.venv', 'venv', 'dist', 'build', '.gemini'}

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file.endswith(('.md', '.py', '.json', '.html', '.txt', '.csv')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if re.search(r'\bmmc\b', line, re.I):
                            matches.append((path, line_num, line.strip()))
                            if len(matches) >= 30:
                                break
            except Exception:
                pass
    if len(matches) >= 30:
        break

print(f"Total matches found: {len(matches)}")
for path, line_num, line in matches:
    print(f"{path}:{line_num}: {line[:120]}")
