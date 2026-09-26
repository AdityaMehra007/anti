import re
from pathlib import Path

root = Path("e:/anti")
target_dirs = ["data", "apps", "applications_generated", "core", "scripts", "docs", "resume_variants", "resumes", "omega", ".scratch", "tests"]

substitutions = [
    ("CGPA 6.33/10", "CGPA 6.33/10"),
    ("CGPA 6.33 / 10", "CGPA 6.33 / 10"),
    ("CGPA 6.33 / 10.0", "CGPA 6.33 / 10.0"),
    ("CGPA 6.33", "CGPA 6.33"),
    ("CGPA: 6.33", "CGPA: 6.33"),
    ("CCGPA 6.33", "CGPA 6.33"),
    ("CCGPA: 6.33", "CGPA: 6.33"),
    ("6.33 / 10.0", "6.33 / 10.0"),
    ("6.33 / 10", "6.33 / 10"),
    ("6.33/10", "6.33/10"),
    ("6.33", "6.33")
]

updated_files = []

for d_name in target_dirs:
    dir_path = root / d_name
    if not dir_path.exists():
        continue
    for p in dir_path.rglob("*"):
        if p.is_file() and p.suffix in [".json", ".html", ".md", ".py", ".eml", ".txt", ".csv", ".bat"]:
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                new_content = content
                for old, new in substitutions:
                    if old in new_content:
                        new_content = new_content.replace(old, new)
                if new_content != content:
                    p.write_text(new_content, encoding="utf-8")
                    updated_files.append(str(p.relative_to(root)))
            except Exception as e:
                pass

for p in root.glob("*.*"):
    if p.is_file() and p.suffix in [".json", ".html", ".md", ".py", ".eml", ".txt", ".csv", ".bat"]:
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
            new_content = content
            for old, new in substitutions:
                if old in new_content:
                    new_content = new_content.replace(old, new)
            if new_content != content:
                p.write_text(new_content, encoding="utf-8")
                updated_files.append(str(p.relative_to(root)))
        except Exception as e:
            pass

print(f"Total files updated with CGPA 6.33: {len(updated_files)}")
for f in updated_files[:25]:
    print(f"  - {f}")
if len(updated_files) > 25:
    print(f"  ... and {len(updated_files) - 25} more")
