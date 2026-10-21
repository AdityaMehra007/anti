import os
import sys

old_email = 'adityamehra799@gmail.com'
new_email = 'adityamehra799@gmail.com'

files_to_check = []

# 1. Root folder files
root_dir = r'e:\anti'
for item in os.listdir(root_dir):
    p = os.path.join(root_dir, item)
    if os.path.isfile(p):
        ext = os.path.splitext(item)[1].lower()
        if ext in ['.md', '.html', '.json', '.py', '.txt', '.js', '.csv', '.xml']:
            files_to_check.append(p)

# 2. Targeted subdirectories
target_subdirs = [
    r'e:\anti\resumes',
    r'e:\anti\resumes_pdf',
    r'e:\anti\resume_variants',
    r'e:\anti\cover_letters',
    r'e:\anti\dossiers',
    r'e:\anti\Company_Tailored_CVs',
    r'e:\anti\applications_generated',
    r'e:\anti\application_packages',
    r'e:\anti\Email_Drafts',
    r'e:\anti\career-hub',
    r'e:\anti\omniverse_deliverables',
    r'e:\anti\client_deliverables',
    r'e:\anti\linkedin_export',
    r'e:\anti\bangalore-intelligence',
    r'e:\anti\outbox',
    r'e:\anti\templates',
    r'e:\anti\static',
    r'e:\anti\docs'
]

skip_dirs = {'.git', '__pycache__', '.venv', 'node_modules'}

for sub in target_subdirs:
    if os.path.exists(sub):
        for r, dirs, files in os.walk(sub):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in ['.md', '.html', '.json', '.py', '.txt', '.js', '.csv', '.xml']:
                    files_to_check.append(os.path.join(r, f))

print(f"Total candidate files to inspect: {len(files_to_check)}", flush=True)

updated = []
for fpath in files_to_check:
    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
        if old_email in content:
            new_content = content.replace(old_email, new_email)
            with open(fpath, 'w', encoding='utf-8', errors='ignore') as fp:
                fp.write(new_content)
            updated.append(fpath)
    except Exception as e:
        pass

print(f"Successfully replaced email in {len(updated)} files!", flush=True)
for u in updated:
    print(f" -> {u}", flush=True)
