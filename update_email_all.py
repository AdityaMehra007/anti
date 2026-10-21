import os
import subprocess

old_email = "adityamehra799@gmail.com"
new_email = "adityamehra799@gmail.com"

target_files = [
    "e:/anti/resumes/Aditya_Mehra_Accenture_CV.html",
    "e:/anti/ADITYA_MEHRA_ACCENTURE_CV.md",
    "e:/anti/compile_accenture_cv.py",
    "e:/anti/generate_individual_dossiers.py",
    "e:/anti/build_dispatch_console.py",
    "e:/anti/resume_adi.md",
    "e:/anti/ACCENTURE_INDIVIDUAL_DISPATCH_DOSSIER.md",
    "e:/anti/accenture_116_dispatch_console.html",
    "e:/anti/resumes/resume_accenture.html",
    "e:/anti/CONTEXT.md",
    "e:/anti/DATA_DICTIONARY.md"
]

updated_count = 0
for fpath in target_files:
    if os.path.exists(fpath):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            if old_email in content:
                new_content = content.replace(old_email, new_email)
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated email in: {fpath}")
                updated_count += 1
            else:
                print(f"Old email not found in: {fpath}")
        except Exception as e:
            print(f"Error reading {fpath}: {e}")

print(f"Total files updated: {updated_count}")

# 1. Regenerate Dossier
print("\n--- Regenerating Individual Dossier ---")
res_dossier = subprocess.run(["python", "e:/anti/generate_individual_dossiers.py"], capture_output=True, text=True)
print(res_dossier.stdout)

# 2. Regenerate Dispatch Console
print("--- Regenerating Dispatch Console ---")
res_console = subprocess.run(["python", "e:/anti/build_dispatch_console.py"], capture_output=True, text=True)
print(res_console.stdout)

# 3. Recompile PDF CV with Chrome headless
print("--- Recompiling PDF CV ---")
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_path = os.path.abspath("e:/anti/resumes/Aditya_Mehra_Accenture_CV.html")
pdf_path = os.path.abspath("e:/anti/resumes_pdf/Aditya_Mehra_Accenture_Operations_CV.pdf")
alias_pdf = os.path.abspath("e:/anti/resumes_pdf/Aditya_Mehra_Resume_001_accenture_india.pdf")

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    "--no-pdf-header-footer",
    html_path
]
subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_path):
    import shutil
    shutil.copyfile(pdf_path, alias_pdf)
    print(f"Successfully recompiled PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
    print(f"Synchronized alias PDF: {alias_pdf}")
